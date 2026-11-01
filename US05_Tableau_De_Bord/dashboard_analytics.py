"""
US05 — Module Tableau de Bord & Synthèse Analytique
Développeuse responsable : Fatima-Zahra Tahiri
Branche : feature/US05-tableau-de-bord
Sprint Backlog : Priorité 5 | Effort : 8 | Valeur : 35
"""

import time
from datetime import datetime, timedelta
from typing import List, Dict, Any

class DashboardAnalyticsEngine:
    """
    Génère la synthèse décisionnelle pour la direction hôtelière :
    - Nombre total d'avis
    - Répartition des sentiments (Positifs, Négatifs, Neutres)
    - Principaux thèmes / aspects
    - Filtrage dynamique et recalcul instantané selon la période sélectionnée.
    """

    def __init__(self, sample_reviews: List[Dict[str, Any]] = None):
        if sample_reviews is not None:
            self.reviews = sample_reviews
        else:
            self.reviews = self._generate_sample_dataset()

    def _generate_sample_dataset(self) -> List[Dict[str, Any]]:
        """Génère un jeu représentatif d'avis horodatés pour les tests de périodes."""
        now = datetime.now()
        data = []
        
        # Avis récents (derniers 7 jours)
        for i in range(12):
            dt = now - timedelta(days=i % 7, hours=i * 2)
            data.append({
                "id": 100 + i,
                "date": dt,
                "sentiment": "Positif" if i % 4 != 0 else "Négatif",
                "themes": ["accueil", "confort"] if i % 2 == 0 else ["proprete", "accueil"]
            })

        # Avis du mois (entre 8 et 30 jours)
        for i in range(25):
            dt = now - timedelta(days=8 + (i % 22))
            data.append({
                "id": 200 + i,
                "date": dt,
                "sentiment": "Positif" if i % 3 != 0 else ("Négatif" if i % 5 == 0 else "Neutre"),
                "themes": ["proprete", "confort", "bruit"] if i % 2 == 0 else ["accueil"]
            })

        # Avis trimestriels (entre 31 et 90 jours)
        for i in range(50):
            dt = now - timedelta(days=32 + (i % 55))
            data.append({
                "id": 300 + i,
                "date": dt,
                "sentiment": "Positif" if i % 2 == 0 else "Négatif",
                "themes": ["accueil", "proprete", "restauration"]
            })

        return data

    def compute_dashboard_metrics(self, period: str = "30d") -> Dict[str, Any]:
        """
        Critère 1 : Le tableau affiche le nombre d'avis, les sentiments et les principaux thèmes.
        Critère 2 : Les résultats se mettent à jour selon la période choisie (7d, 30d, 90d, all).
        """
        now = datetime.now()
        
        # Filtrage par période temporelle
        if period == "7d":
            limit = now - timedelta(days=7)
            filtered = [r for r in self.reviews if r["date"] >= limit]
            period_label = "Derniers 7 jours"
        elif period == "30d":
            limit = now - timedelta(days=30)
            filtered = [r for r in self.reviews if r["date"] >= limit]
            period_label = "Derniers 30 jours"
        elif period == "90d":
            limit = now - timedelta(days=90)
            filtered = [r for r in self.reviews if r["date"] >= limit]
            period_label = "Dernier trimestre (90 jours)"
        else:
            filtered = list(self.reviews)
            period_label = "Tout l'historique"

        total_reviews = len(filtered)
        if total_reviews == 0:
            return {
                "period": period,
                "period_label": period_label,
                "total_reviews": 0,
                "sentiments": {"positif": 0, "negatif": 0, "neutre": 0},
                "satisfaction_rate": 0,
                "top_themes": []
            }

        # 1. Calcul des sentiments
        pos_count = sum(1 for r in filtered if r["sentiment"] == "Positif")
        neg_count = sum(1 for r in filtered if r["sentiment"] == "Négatif")
        neu_count = sum(1 for r in filtered if r["sentiment"] == "Neutre")

        pos_rate = round((pos_count / total_reviews) * 100, 1)
        neg_rate = round((neg_count / total_reviews) * 100, 1)
        neu_rate = round((neu_count / total_reviews) * 100, 1)

        # 2. Calcul des principaux thèmes
        theme_counts = {}
        theme_labels = {
            "accueil": "Accueil & Service",
            "proprete": "Propreté",
            "confort": "Confort de la literie",
            "bruit": "Calme & Bruit",
            "restauration": "Petit-déjeuner"
        }

        for r in filtered:
            for th in r.get("themes", []):
                theme_counts[th] = theme_counts.get(th, 0) + 1

        top_themes = [
            {
                "theme_key": k,
                "label": theme_labels.get(k, k.capitalize()),
                "mentions": count,
                "share_pct": round((count / total_reviews) * 100, 1)
            }
            for k, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        ]

        return {
            "period": period,
            "period_label": period_label,
            "total_reviews": total_reviews,
            "sentiments": {
                "positif": {"count": pos_count, "percentage": pos_rate},
                "negatif": {"count": neg_count, "percentage": neg_rate},
                "neutre": {"count": neu_count, "percentage": neu_rate}
            },
            "satisfaction_rate": pos_rate,
            "top_themes": top_themes
        }


if __name__ == "__main__":
    engine = DashboardAnalyticsEngine()
    print("Module DashboardAnalyticsEngine prêt.")
