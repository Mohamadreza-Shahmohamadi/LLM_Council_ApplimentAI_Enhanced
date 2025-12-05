"""
Stage 0: Message Classification
Determines if query needs full deliberation or can be answered directly.

Two-tier classification:
1. Fast heuristic classifier (no API call) - catches obvious cases
2. LLM-based classifier (if heuristic is uncertain)
"""

from typing import Dict
import json
import logging

logger = logging.getLogger(__name__)


def fast_classify_message(message: str) -> Dict:
    """
    Fast heuristic classification using the query_classifier module.
    No API calls - purely rule-based.
    
    Returns:
        Dict with type, confidence, reasoning, and 'certain' flag
    """
    try:
        from .query_classifier import classify_query, QueryCategory
        
        result = classify_query(message)
        
        # Map category to classification type
        direct_categories = {'factual'}  # Simple factual = direct answer
        deliberation_categories = {'technical', 'analytical', 'reasoning', 'creative'}
        
        if result.category in direct_categories and result.confidence > 0.6:
            return {
                "type": "direct",
                "confidence": result.confidence,
                "reasoning": f"Fast classifier: {result.category} query with clear signals",
                "certain": True  # High confidence, skip LLM
            }
        elif result.category in deliberation_categories and result.confidence > 0.7:
            return {
                "type": "deliberation",
                "confidence": result.confidence,
                "reasoning": f"Fast classifier: {result.category} query requires analysis",
                "certain": True  # High confidence, skip LLM
            }
        else:
            # Low confidence - needs LLM verification
            return {
                "type": "deliberation" if result.category in deliberation_categories else "direct",
                "confidence": result.confidence,
                "reasoning": f"Fast classifier uncertain: {result.category}",
                "certain": False
            }
    except Exception as e:
        logger.warning(f"Fast classifier failed: {e}")
        return {
            "type": "deliberation",
            "confidence": 0.5,
            "reasoning": "Fast classifier error, needs LLM",
            "certain": False
        }


async def classify_message(message: str, query_model_func) -> Dict:
    """
    Two-tier classification: Fast heuristic first, then LLM if uncertain.
    
    Args:
        message: User's input message
        query_model_func: Function to query a model
    
    Returns:
        {
            "type": "direct" | "deliberation",
            "confidence": float (0.0-1.0),
            "reasoning": str
        }
    """
    # Step 1: Try fast classification first (no API cost)
    fast_result = fast_classify_message(message)
    
    if fast_result.get("certain", False):
        logger.info(f"Fast classification succeeded: {fast_result['type']} ({fast_result['confidence']:.2f})")
        # Remove internal flag before returning
        del fast_result["certain"]
        return fast_result
    
    # Step 2: Fall back to LLM classification for uncertain cases
    logger.info("Fast classifier uncertain, using LLM classification")
    
    classification_prompt = f"""Analyze this user message and determine if it requires full council deliberation or can be answered directly.

DIRECT RESPONSE (answer immediately):
- Simple factual questions ("What is the capital of France?")
- Basic greetings or casual conversation ("Hello", "Thank you")
- Simple calculations ("What is 2+2?")
- Clear, objective questions with single correct answers

COUNCIL DELIBERATION (full multi-model process):
- Complex questions requiring analysis or opinions
- Questions with multiple valid perspectives
- Comparisons that need evaluation ("Compare X vs Y")
- Subjective topics requiring diverse viewpoints
- Ambiguous or nuanced questions

User message: "{message}"

Respond with ONLY this JSON format (no markdown, no code blocks):
{{"type": "direct", "confidence": 0.85, "reasoning": "Simple factual question"}}
or
{{"type": "deliberation", "confidence": 0.90, "reasoning": "Complex comparison requiring multiple perspectives"}}"""

    try:
        # Use chairman model for classification with low temperature
        from .config import get_chairman_model
        chairman_model = get_chairman_model()
        
        response = await query_model_func(
            chairman_model,
            [{"role": "user", "content": classification_prompt}],
            temperature=0.3,
            timeout=15.0
        )
        
        if response and not response.get('error'):
            content = response.get('content', '').strip()
            
            # Remove markdown code blocks if present
            if content.startswith('```'):
                lines = content.split('\n')
                content = '\n'.join(lines[1:-1]) if len(lines) > 2 else content
            
            # Parse JSON
            classification = json.loads(content)
            
            # Validate
            if classification.get('type') in ['direct', 'deliberation']:
                confidence = float(classification.get('confidence', 0.5))
                classification['confidence'] = max(0.0, min(1.0, confidence))
                return classification
    
    except Exception as e:
        logger.warning(f"LLM classification failed: {e}, defaulting to deliberation")
    
    # Fallback: default to deliberation (safer)
    return {
        "type": "deliberation",
        "confidence": 0.5,
        "reasoning": "Classification failed, using full deliberation for safety"
    }

