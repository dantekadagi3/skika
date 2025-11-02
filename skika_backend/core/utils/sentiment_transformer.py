"""Transformer-based sentiment analyzer with lazy model loading.

This module tries to use Hugging Face's `transformers` pipeline for
sentiment-analysis (default model: distilbert-base-uncased-finetuned-sst-2-english).
It falls back to the lightweight lexicon analyzer in `core.utils.sentiment`
when transformers isn't installed or model loading fails.

Notes:
- Requires `transformers` and a backend (torch or tensorflow) installed to use.
- The model will be downloaded the first time it's used (internet required).
"""
from __future__ import annotations
import os
from typing import Dict

# Try to import transformers lazily
_TRANSFORMERS_AVAILABLE = True
try:
    from transformers import pipeline
except Exception:
    _TRANSFORMERS_AVAILABLE = False

# Default model to use for sentiment analysis
DEFAULT_MODEL = os.environ.get('SENTIMENT_MODEL', 'distilbert-base-uncased-finetuned-sst-2-english')

# Lazy pipeline instance
_PIPELINE = None
_MODEL_NAME = None


def _get_pipeline():
    global _PIPELINE, _MODEL_NAME
    if not _TRANSFORMERS_AVAILABLE:
        return None
    if _PIPELINE is None:
        try:
            _PIPELINE = pipeline('sentiment-analysis', model=DEFAULT_MODEL)
            _MODEL_NAME = DEFAULT_MODEL
        except Exception:
            # If model download or backend fails, mark as unavailable
            return None
    return _PIPELINE


def analyze_sentiment(text: str) -> Dict:
    """Analyze sentiment using a transformer pipeline if available.

    Returns a dict similar to the lightweight analyzer but with additional
    keys when using the transformer: 'model' and 'raw' containing the
    transformer output.

    If transformers are not available or loading fails, falls back to
    the lightweight lexicon analyzer in `core.utils.sentiment`.
    """
    if not text:
        return {'score': 0.0, 'label': 'neutral', 'token_count': 0}

    pipe = _get_pipeline()
    if pipe is None:
        # Lazy fallback to the built-in lexicon analyzer to avoid hard failures
        try:
            from .sentiment import analyze_sentiment as lex_analyze
            result = lex_analyze(text)
            result['model'] = 'lexicon_fallback'
            return result
        except Exception:
            return {'score': 0.0, 'label': 'neutral', 'token_count': 0, 'model': 'none'}

    # Use transformer pipeline
    try:
        out = pipe(text)
        # pipeline returns a list of predictions; use first
        if isinstance(out, list) and len(out) > 0:
            pred = out[0]
            label = pred.get('label', '').upper()
            score = float(pred.get('score', 0.0))
            # Normalize: POSITIVE -> +score, NEGATIVE -> -score
            if label == 'POSITIVE':
                normalized = round(min(1.0, max(-1.0, score)), 4)
                human_label = 'positive' if score >= 0.6 else 'neutral'
            elif label == 'NEGATIVE':
                normalized = round(-min(1.0, max(-1.0, score)), 4)
                human_label = 'negative' if score >= 0.6 else 'neutral'
            else:
                normalized = 0.0
                human_label = 'neutral'

            return {
                'score': normalized,
                'label': human_label,
                'raw_label': label,
                'raw_score': round(score, 4),
                'model': _MODEL_NAME or DEFAULT_MODEL,
                'token_count': len(text.split()),
                'raw': out,
            }
    except Exception:
        # If pipeline execution fails, fallback to lexicon analyzer
        try:
            from .sentiment import analyze_sentiment as lex_analyze
            result = lex_analyze(text)
            result['model'] = 'lexicon_fallback'
            return result
        except Exception:
            return {'score': 0.0, 'label': 'neutral', 'token_count': len(text.split()), 'model': 'none'}
