"""
Multi-round deliberation strategy.
Implements iterative refinement for higher quality answers.
"""

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


async def run_multi_round(
    query: str,
    search_context: str,
    models: List[str],
    rounds: int,
    query_model_func,
    get_council_temperature_func
) -> tuple:
    """
    Run multi-round deliberation with iterative refinement.
    
    Args:
        query: User's question
        search_context: Web search context
        models: List of council models
        rounds: Number of rounds (typically 2)
        query_model_func: Function to query models
        get_council_temperature_func: Function to get temperature setting
    
    Returns:
        (all_rounds, final_stage1_results) where all_rounds contains each round's data
    """
    all_rounds = []
    previous_responses = None
    
    for round_num in range(rounds):
        logger.info(f"Starting Round {round_num + 1}/{rounds}")
        
        # Build prompt for this round
        if round_num == 0:
            # Round 1: Fresh responses
            prompt = query
            if search_context:
                prompt = f"Context from web search:\n{search_context}\n\nQuestion: {query}"
        else:
            # Round 2+: Include peer responses for refinement
            peer_summary = "\n\n".join([
                f"Model {r['model']} said:\n{r.get('response', 'No response')}"
                for r in previous_responses
                if not r.get('error')
            ])
            
            refinement_prompt = f"""Previous round responses:

{peer_summary}

Original question: {query}

{f"Context: {search_context}" if search_context else ""}

Consider the previous responses and provide your refined answer. Build upon good insights and address any gaps or errors you noticed."""
            
            prompt = refinement_prompt
        
        # Get responses from all models
        messages = [{"role": "user", "content": prompt}]
        round_results = []
        
        council_temp = get_council_temperature_func()
        
        # Query models in parallel for this round
        import asyncio
        
        async def _query_safe(m: str):
            try:
                return m, await query_model_func(m, messages, temperature=council_temp)
            except Exception as e:
                return m, {"error": True, "error_message": str(e)}
        
        tasks = [_query_safe(m) for m in models]
        responses = await asyncio.gather(*tasks)
        
        for model, response in responses:
            if response is not None:
                if response.get('error'):
                    round_results.append({
                        "model": model,
                        "response": None,
                        "error": response.get('error'),
                        "error_message": response.get('error_message', 'Unknown error')
                    })
                else:
                    content = response.get('content', '')
                    if not isinstance(content, str):
                        content = str(content) if content is not None else ''
                    round_results.append({
                        "model": model,
                        "response": content,
                        "error": None
                    })
        
        all_rounds.append({
            "round": round_num + 1,
            "results": round_results
        })
        
        previous_responses = round_results
    
    # Return all rounds and the final round's results as the "stage1_results"
    final_round_results = all_rounds[-1]["results"] if all_rounds else []
    
    return all_rounds, final_round_results
