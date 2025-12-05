"""Query classifier for categorizing user queries to recommend strategies.

Ported from CrazyDubya/llm-council - Classifies queries to recommend execution mode.
"""

import re
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class QueryCategory:
    """Category for a user query."""
    category: str
    confidence: float
    indicators: List[str]


class QueryClassifier:
    """
    Classifies user queries into categories to help recommend
    the most appropriate execution strategy.

    Categories:
    - technical: Programming, debugging, code-related queries
    - analytical: Data analysis, comparison, evaluation queries
    - creative: Writing, brainstorming, open-ended questions
    - factual: Information lookup, definitions, facts
    - reasoning: Complex logic, mathematics, multi-step problems
    """

    def __init__(self):
        # Keyword patterns for each category
        self.patterns = {
            'technical': {
                'keywords': [
                    r'\bcode\b', r'\bprogram(ming)?\b', r'\bdebug\b', r'\bfunction\b',
                    r'\bapi\b', r'\balgorithm\b', r'\bsyntax\b', r'\berror\b',
                    r'\bbug\b', r'\bframework\b', r'\blibrary\b', r'\bclass\b',
                    r'\bmethod\b', r'\bvariable\b', r'\bloop\b', r'\barray\b',
                    r'\bpython\b', r'\bjavascript\b', r'\breact\b', r'\bnode\b',
                    r'\bgit\b', r'\bdocker\b', r'\bsql\b', r'\bdatabase\b'
                ],
                'weight': 1.0
            },
            'reasoning': {
                'keywords': [
                    r'\bcalculate\b', r'\bprove\b', r'\bderive\b', r'\bsolve\b',
                    r'\btheorem\b', r'\bequation\b', r'\bsteps?\b', r'\blogic\b',
                    r'\bif.*then\b', r'\bgiven.*find\b', r'\bproof\b',
                    r'\bassume\b', r'\bconclude\b', r'\binfer\b', r'\bdeduce\b',
                    r'\bmathematics\b', r'\bcalculus\b', r'\balgebra\b',
                    r'\bstrategy\b', r'\bplan\b', r'\bapproach\b', r'\bmethod\b',
                    r'why\s+is\b', r'how\s+does\b', r'explain.*process'
                ],
                'weight': 1.2  # Higher weight for reasoning
            },
            'analytical': {
                'keywords': [
                    r'\bcompare\b', r'\bcontrast\b', r'\banalyze\b', r'\bevaluate\b',
                    r'\bassess\b', r'\btradeoff\b', r'\bpros\s+and\s+cons\b',
                    r'\bdifference\b', r'\bsimilarity\b', r'\bbetter\b', r'\bworse\b',
                    r'\badvantage\b', r'\bdisadvantage\b', r'\bmetric\b',
                    r'\bperformance\b', r'\bbenchmark\b', r'\bstatistic\b',
                    r'\btrend\b', r'\bpattern\b', r'\bcorrelation\b'
                ],
                'weight': 1.0
            },
            'creative': {
                'keywords': [
                    r'\bwrite\b', r'\bstory\b', r'\bpoem\b', r'\bessay\b',
                    r'\bbrainstorm\b', r'\bidea\b', r'\bimaginative\b', r'\bcreative\b',
                    r'\binvent\b', r'\bdesign\b', r'\bnovel\b', r'\boriginal\b',
                    r'\bnarrative\b', r'\bcharacter\b', r'\bplot\b', r'\bscenario\b',
                    r'\bslogan\b', r'\bmarketing\b', r'\bcampaign\b',
                    r'\bmetaphor\b', r'\banalogy\b'
                ],
                'weight': 0.9
            },
            'factual': {
                'keywords': [
                    r'\bwhat\s+is\b', r'\bwhen\s+did\b', r'\bwho\s+is\b',
                    r'\bwhere\s+is\b', r'\bdefine\b', r'\bdefinition\b',
                    r'\bexplain\b', r'\bdescribe\b', r'\blist\b', r'\bname\b',
                    r'\bhistory\b', r'\bfact\b', r'\binformation\b',
                    r'\bcapital\b', r'\bpopulation\b', r'\bdate\b',
                    r'\bmean\b', r'\brefer\b', r'\bstand for\b'
                ],
                'weight': 0.8
            }
        }

    def classify(self, query: str) -> QueryCategory:
        """Classify a query into a category."""
        if not query or len(query.strip()) < 3:
            return QueryCategory(
                category='factual',
                confidence=0.0,
                indicators=[]
            )

        query_lower = query.lower()
        scores = {}
        matches = {}

        for category, config in self.patterns.items():
            category_matches = []
            score = 0

            for pattern in config['keywords']:
                if re.search(pattern, query_lower):
                    category_matches.append(pattern)
                    score += config['weight']

            scores[category] = score
            matches[category] = category_matches

        if not scores or max(scores.values()) == 0:
            return QueryCategory(
                category='factual',
                confidence=0.3,
                indicators=[]
            )

        best_category = max(scores, key=scores.get)
        best_score = scores[best_category]
        total_score = sum(scores.values())

        confidence = min(best_score / (total_score + 1e-6), 1.0)

        return QueryCategory(
            category=best_category,
            confidence=round(confidence, 2),
            indicators=matches[best_category]
        )

    def get_recommended_strategy(self, query: str) -> Dict[str, Any]:
        """
        Recommend an execution strategy based on query classification.
        
        Returns:
            Dict with recommended strategy and explanation
        """
        category = self.classify(query)

        recommendations = {
            'reasoning': {
                'strategy': 'full_deliberation',
                'use_chairman': True,
                'explanation': 'Complex reasoning benefits from full council deliberation with synthesis.'
            },
            'technical': {
                'strategy': 'full_deliberation',
                'use_chairman': True,
                'explanation': 'Technical queries benefit from multiple expert perspectives and synthesis.'
            },
            'analytical': {
                'strategy': 'full_deliberation',
                'use_chairman': True,
                'explanation': 'Analytical questions benefit from diverse viewpoints and aggregation.'
            },
            'creative': {
                'strategy': 'full_deliberation',
                'use_chairman': True,
                'explanation': 'Creative queries benefit from varied perspectives and synthesis.'
            },
            'factual': {
                'strategy': 'chat_only',
                'use_chairman': False,
                'explanation': 'Simple factual queries can be answered by chairman alone for speed.'
            }
        }

        recommendation = recommendations.get(category.category, recommendations['factual'])

        return {
            'strategy': recommendation['strategy'],
            'use_chairman': recommendation['use_chairman'],
            'explanation': recommendation['explanation'],
            'query_category': category.category,
            'confidence': category.confidence,
            'indicators': category.indicators
        }


# Singleton instance
_classifier = None


def get_classifier() -> QueryClassifier:
    """Get or create the singleton classifier instance."""
    global _classifier
    if _classifier is None:
        _classifier = QueryClassifier()
    return _classifier


def classify_query(query: str) -> QueryCategory:
    """Convenience function to classify a query."""
    return get_classifier().classify(query)


def should_use_full_council(query: str) -> bool:
    """
    Determine if query warrants full council deliberation vs simple chat.
    
    Returns True for complex queries needing multiple perspectives.
    Returns False for simple factual questions.
    """
    recommendation = get_classifier().get_recommended_strategy(query)
    return recommendation['strategy'] == 'full_deliberation'
