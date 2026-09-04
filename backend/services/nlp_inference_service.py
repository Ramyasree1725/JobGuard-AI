"""
JobGuard Backend Service - NLP Inference Pipeline & Scam Classifier
Wraps TF-IDF featurizer, RoBERTa transformer, and rule signatures into unified inference service.
"""

from typing import Dict, List, Any, Optional
from core.ml_inference.feature_encoder import TFIDFVectorizer, TextFeatureExtractor
from core.nlp.roberta_encoder import RoBERTaJobClassifier
from core.nlp.sentiment_lexicon import UrgencySentimentAnalyzer


class NLPInferenceService:
    """Master multi-model NLP text classification orchestrator."""

    def __init__(self):
        self.feature_extractor = TextFeatureExtractor()
        self.sentiment_analyzer = UrgencySentimentAnalyzer()
        self.roberta = RoBERTaJobClassifier(vocab_size=1000, embed_dim=32, num_layers=2)

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Perform comprehensive linguistic, statistical, and neural scam analysis."""
        stats = self.feature_extractor.extract_features(text)
        sentiment = self.sentiment_analyzer.analyze_pressure_score(text)
        
        # Token ids approximation
        words = text.lower().split()
        token_ids = [hash(w) % 1000 for w in words]
        preds = self.roberta.forward(token_ids)
        neural_scam_prob = round(preds.data[1], 4)

        return {
            "lexical_features": stats,
            "urgency_analysis": sentiment,
            "neural_scam_probability": neural_scam_prob,
            "is_suspicious_language": sentiment["is_coercive"] or neural_scam_prob > 0.6
        }
