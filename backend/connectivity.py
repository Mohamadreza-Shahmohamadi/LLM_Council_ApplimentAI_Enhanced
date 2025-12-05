"""
Robust connectivity with retry logic and circuit breaker.
Improves API reliability and error handling.
"""

import asyncio
import time
import httpx
from typing import Dict, Optional
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class CircuitBreaker:
    """Circuit breaker to prevent cascading failures."""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = defaultdict(int)
        self.last_failure_time = defaultdict(float)
    
    def is_open(self, provider: str) -> bool:
        """Check if circuit is open (provider is temporarily blocked)."""
        if self.failures[provider] >= self.failure_threshold:
            elapsed = time.time() - self.last_failure_time[provider]
            if elapsed < self.timeout:
                logger.warning(f"Circuit breaker OPEN for {provider} ({self.failures[provider]} failures)")
                return True
            else:
                # Reset after timeout period
                logger.info(f"Circuit breaker RESET for {provider}")
                self.failures[provider] = 0
                return False
        return False
    
    def record_failure(self, provider: str):
        """Record a failure."""
        self.failures[provider] += 1
        self.last_failure_time[provider] = time.time()
    
    def record_success(self, provider: str):
        """Reset failure count on success."""
        if self.failures[provider] > 0:
            self.failures[provider] = 0


class RobustHTTPClient:
    """HTTP client with retry logic and circuit breaker."""
    
    def __init__(self):
        self.retry_config = {
            "max_retries": 3,
            "backoff_factor": 2,  # Exponential: 1s, 2s, 4s
            "timeout": 60,
            "rate_limit_backoff": 60
        }
        self.circuit_breaker = CircuitBreaker()
    
    async def post_with_retry(
        self,
        url: str,
        json_data: Dict,
        headers: Dict,
        provider: str,
        timeout: Optional[float] = None
    ) -> Dict:
        """
        Make POST request with retry logic.
        
        Handles:
        - Timeouts (exponential backoff)
        - Rate limits (429)
        - Server errors (500-599)
        - Network failures
        """
        # Check circuit breaker
        if self.circuit_breaker.is_open(provider):
            raise Exception(f"Circuit breaker open for {provider} - too many recent failures")
        
        request_timeout = timeout or self.retry_config["timeout"]
        last_error = None
        
        for attempt in range(self.retry_config["max_retries"]):
            try:
                async with httpx.AsyncClient(timeout=request_timeout) as client:
                    response = await client.post(url, json=json_data, headers=headers)
                    
                    # Handle rate limits
                    if response.status_code == 429:
                        wait = self.retry_config["rate_limit_backoff"]
                        logger.warning(f"Rate limited by {provider}, waiting {wait}s...")
                        await asyncio.sleep(wait)
                        continue
                    
                    # Handle server errors with retry
                    if 500 <= response.status_code < 600:
                        if attempt < self.retry_config["max_retries"] - 1:
                            wait = self.retry_config["backoff_factor"] ** attempt
                            logger.warning(f"Server error {response.status_code} from {provider}, retry in {wait}s...")
                            await asyncio.sleep(wait)
                            continue
                    
                    # Check for errors
                    response.raise_for_status()
                    
                    # Success!
                    self.circuit_breaker.record_success(provider)
                    return response.json()
                    
            except httpx.TimeoutException as e:
                last_error = e
                if attempt < self.retry_config["max_retries"] - 1:
                    wait = self.retry_config["backoff_factor"] ** attempt
                    logger.warning(f"Timeout from {provider} (attempt {attempt+1}), retry in {wait}s...")
                    await asyncio.sleep(wait)
                else:
                    logger.error(f"Timeout from {provider} after {self.retry_config['max_retries']} attempts")
                    self.circuit_breaker.record_failure(provider)
            
            except httpx.HTTPStatusError as e:
                last_error = e
                logger.error(f"HTTP error from {provider}: {e.response.status_code}")
                self.circuit_breaker.record_failure(provider)
                raise
            
            except Exception as e:
                last_error = e
                if attempt < self.retry_config["max_retries"] - 1:
                    wait = self.retry_config["backoff_factor"] ** attempt
                    logger.warning(f"Error from {provider}: {e}, retry in {wait}s...")
                    await asyncio.sleep(wait)
                else:
                    logger.error(f"Failed after {self.retry_config['max_retries']} attempts: {e}")
                    self.circuit_breaker.record_failure(provider)
        
        # All retries exhausted
        raise Exception(f"Failed after {self.retry_config['max_retries']} attempts: {last_error}")


# Global singleton instance
robust_client = RobustHTTPClient()
