"""
US03 — Module d'Analyse des Sentiments (NLP)
Développeuse responsable : Salma Mansouri
Branche : feature/US03-analyse-sentiments
Sprint Backlog : Priorité 3 | Effort : 8 | Valeur : 35
"""

import os
import re
from typing import Dict, Any, List

class SentimentAnalyzer:
    """
    Analyse les sentiments des avis hôteliers (Positif, Négatif, Neutre),
    identifie et signale les cas d'incertitude / ambivalence,
    tout en préservant l'intégrité du texte original pour consultation.
    """

    def __init__(self, model_path: str = None):
        self.model = None
        # Recherche du modèle entraîné outputs/sentiment_model.joblib
        possible_paths = [
            model_path,
            os.path.join(os.path.dirname(__file__), "..", "outputs", "sentiment_model.joblib"),
            "outputs/sentiment_model.joblib"
        ]
        for p in possible_paths:
            if p and os.path.exists(p):
                try:
                    import joblib
                    self.model = joblib.load(p)
                    break
                except Exception:
                    pass

        # Lexique multilingue (Français, Anglais, Arabe) pour scoring direct et fallback
        self.lexicon_pos = {
            "bon", "excellent", "superbe", "magnifique", "parfait", "propre", "chaleureux", "calme",
            "top", "aimable", "accueillant", "recommande", "agreable", "confortable", "delicieux",
            "good", "great", "superb", "lovely", "clean", "spotless", "helpful", "friendly", "best", "quiet",
            "ممتاز", "رائع", "نظيف", "جميل", "هادئ", "مريح", "محترم", "لذيذ"
        }
        self.lexicon_neg = {
            "mauvais", "terrible", "sale", "bruyant", "horrible", "cher", "decevant", "lent", "nul",
            "odeur", "insalubre", "froid", "attente", "catastrophique", "inacceptable", "desagreable",
            "bad", "terrible", "dirty", "noisy", "poor", "horrible", "overpriced", "slow", "disappointing",
            "سيء", "كارثي", "متسخ", "ضجيج", "بطيء", "غالي", "غير مريح"
        }

    def analyze_review(self, text: str) -> Dict[str, Any]:
        """
        Critère 1 : Le sentiment détecté apparaît pour chaque avis (Positif, Négatif, Neutre).
        Critère 2 : Les cas incertains sont signalés (seuil de confiance équilibré ou avis mixte).
        Critère 3 : Le texte original reste strictement consultable sans modification.
        """
        if not text or not isinstance(text, str):
            return {
                "original_text": text or "",
                "sentiment": "Neutre",
                "score_pos": 0.5,
                "score_neg": 0.5,
                "is_uncertain": True,
                "uncertainty_reason": "Texte vide ou non renseigné."
            }

        original_text = text  # Préservation intégrale du texte d'origine (Critère 3)
        clean_text = text.strip()

        p_pos = 0.5
        # Utilisation du modèle scikit-learn si chargé
        if self.model:
            try:
                probs = self.model.predict_proba([clean_text])[0]
                p_pos = float(probs[1])
            except Exception:
                p_pos = self._lexical_score(clean_text)
        else:
            p_pos = self._lexical_score(clean_text)

        p_neg = round(1.0 - p_pos, 3)
        p_pos = round(p_pos, 3)

        # Classification en 3 classes
        if p_pos >= 0.60:
            sentiment = "Positif"
        elif p_pos <= 0.40:
            sentiment = "Négatif"
        else:
            sentiment = "Neutre"

        # Détection des cas incertains (Critère 2)
        # Un cas est incertain si la probabilité est trop proche de 0.50 (zone d'indécision 0.44 - 0.56)
        # ou si l'avis présente à la fois des termes très élogieux et très critiques (avis mixte)
        is_uncertain = False
        uncertainty_reason = None

        has_pos_words = any(w in clean_text.lower() for w in self.lexicon_pos)
        has_neg_words = any(w in clean_text.lower() for w in self.lexicon_neg)

        if 0.44 <= p_pos <= 0.56:
            is_uncertain = True
            uncertainty_reason = "Probabilité équilibrée (zone d'indécision 50/50). Nécessite validation humaine."
        elif has_pos_words and has_neg_words:
            # Avis mixte avec sentiments contradictoires
            is_uncertain = True
            uncertainty_reason = "Avis mixte contenant des retours contrastés à la fois très positifs et négatifs."

        return {
            "original_text": original_text,
            "sentiment": sentiment,
            "confidence_score": max(p_pos, p_neg),
            "score_pos": p_pos,
            "score_neg": p_neg,
            "is_uncertain": is_uncertain,
            "uncertainty_reason": uncertainty_reason
        }

    def _lexical_score(self, text: str) -> float:
        t_low = text.lower()
        pos_hits = sum(1 for w in self.lexicon_pos if w in t_low)
        neg_hits = sum(1 for w in self.lexicon_neg if w in t_low)

        diff = pos_hits - neg_hits
        if diff > 0:
            return min(0.65 + diff * 0.1, 0.98)
        elif diff < 0:
            return max(0.35 + diff * 0.1, 0.05)
        return 0.50

    def analyze_batch(self, reviews: List[str]) -> List[Dict[str, Any]]:
        return [self.analyze_review(r) for r in reviews]


if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    print("Module SentimentAnalyzer initialisé.")
