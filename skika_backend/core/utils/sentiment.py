"""Lightweight sentiment analysis utility.

This module implements a small lexicon-based sentiment analyzer so the
project can provide sentiment scores without external dependencies.

Functions:
- analyze_sentiment(text) -> dict: returns score float, label, and counts

The score is normalized to the range [-1.0, 1.0]. Labels: 'positive',
'negative', or 'neutral'.
"""
from __future__ import annotations
import re
from typing import Dict

# Minimal AFINN-like sentiment lexicon (subset). Values range roughly -5..+5.
# Expanded with common words to give reasonable coverage for user messages.
SENTIMENT_LEXICON = {
    'good': 3, 'great': 4, 'excellent': 5, 'awesome': 4, 'happy': 3,
    'love': 3, 'liked': 2, 'like': 2, 'thanks': 2, 'thank': 2,
    'bad': -3, 'terrible': -5, 'horrible': -4, 'sad': -2, 'angry': -3,
    'hate': -4, 'dislike': -2, 'problem': -2, 'issue': -2, 'delay': -1,
    'help': 1, 'support': 1, 'urgent': -1, 'failed': -3, 'failure': -3,
    'success': 3, 'resolved': 2, 'resolved.': 2, 'resolved!': 2,
    'improve': 1, 'improved': 2, 'safe': 2, 'unsafe': -2, 'danger': -3,
    'clean': 1, 'dirty': -2, 'poor': -2, 'better': 2, 'worse': -2,
    'slow': -1, 'fast': 1, 'satisfied': 3, 'unsatisfied': -3, 'ok': 0,
    'okay': 1, 'fine': 1, 'urgent': -1, 'emergency': -4
}

WORD_RE = re.compile(r"\b[\w']+\b", flags=re.UNICODE)


def analyze_sentiment(text: str) -> Dict:
    """Analyze sentiment of `text` using simple lexicon scoring.

    Returns a dict with:
    - score: float normalized to [-1.0, 1.0]
    - label: 'positive'|'neutral'|'negative'
    - positive_count, negative_count, token_count
    - tokens: list of lowercased tokens (for debugging)
    """
    if not text:
        return {'score': 0.0, 'label': 'neutral', 'positive_count': 0, 'negative_count': 0, 'token_count': 0, 'tokens': []}

    tokens = WORD_RE.findall(text.lower())
    if not tokens:
        return {'score': 0.0, 'label': 'neutral', 'positive_count': 0, 'negative_count': 0, 'token_count': 0, 'tokens': []}

    score = 0
    pos = 0
    neg = 0
    for t in tokens:
        val = SENTIMENT_LEXICON.get(t)
        if val is None:
            # Try simple stemming heuristics for common forms
            if t.endswith('ing') and t[:-3] in SENTIMENT_LEXICON:
                val = SENTIMENT_LEXICON[t[:-3]]
            elif t.endswith('ed') and t[:-2] in SENTIMENT_LEXICON:
                val = SENTIMENT_LEXICON[t[:-2]]
        if val is not None:
            score += val
            if val > 0:
                pos += 1
            elif val < 0:
                neg += 1

    # Normalize score by a rough ceiling to keep values reasonable
    # Use max_possible = 5 * sqrt(token_count) to reduce impact of long text
    import math
    token_count = len(tokens)
    if token_count == 0:
        normalized = 0.0
    else:
        ceiling = 5.0 * math.sqrt(token_count)
        normalized = max(-1.0, min(1.0, score / ceiling))

    # Decide label thresholds
    if normalized >= 0.05:
        label = 'positive'
    elif normalized <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'

    return {
        'score': round(normalized, 4),
        'label': label,
        'positive_count': pos,
        'negative_count': neg,
        'token_count': token_count,
        'tokens': tokens
    }
