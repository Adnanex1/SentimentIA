"""
Test d'acceptation — US05 Tableau de bord
Développeuse : Fatima-Zahra Tahiri
Sprint Backlog : Priorité 5 | Effort : 8 | Valeur : 35

Validation stricte des 2 critères d'acceptation de l'image :
  1. Le tableau affiche le nombre d'avis, les sentiments et les principaux thèmes.
  2. Les résultats se mettent à jour selon la période choisie.
"""

import sys
from dashboard_analytics import DashboardAnalyticsEngine

def run_acceptance_tests():
    print("=" * 65)
    print("TEST D'ACCEPTATION — US05 : TABLEAU DE BORD (Fatima-Zahra Tahiri)")
    print("=" * 65)

    engine = DashboardAnalyticsEngine()
    passed = 0
    total = 2

    # Calcul pour une période initiale (30 jours)
    metrics_30d = engine.compute_dashboard_metrics(period="30d")

    # -------------------------------------------------------------
    # CRITÈRE 1 : Le tableau affiche le nombre d'avis, les sentiments et les principaux thèmes
    # -------------------------------------------------------------
    print("\n[CRITÈRE 1] Vérification de la présence des indicateurs clés (Nombre, Sentiments, Thèmes)...")
    has_total = "total_reviews" in metrics_30d and metrics_30d["total_reviews"] > 0
    has_sentiments = ("sentiments" in metrics_30d and 
                      "positif" in metrics_30d["sentiments"] and 
                      "negatif" in metrics_30d["sentiments"])
    has_themes = "top_themes" in metrics_30d and len(metrics_30d["top_themes"]) > 0

    if has_total and has_sentiments and has_themes:
        print(f"  --> SUCCÈS : Tous les indicateurs obligatoires sont présents :")
        print(f"      • Nombre d'avis : {metrics_30d['total_reviews']}")
        print(f"      • Sentiments : Positifs={metrics_30d['sentiments']['positif']['percentage']}%, "
              f"Négatifs={metrics_30d['sentiments']['negatif']['percentage']}%, "
              f"Neutres={metrics_30d['sentiments']['neutre']['percentage']}%")
        print(f"      • Principaux thèmes : {', '.join([t['label'] for t in metrics_30d['top_themes'][:3]])}")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Éléments manquants dans la synthèse : {metrics_30d}")

    # -------------------------------------------------------------
    # CRITÈRE 2 : Les résultats se mettent à jour selon la période choisie
    # -------------------------------------------------------------
    print("\n[CRITÈRE 2] Test de mise à jour dynamique selon les différentes périodes (7d, 30d, 90d, all)...")
    m_7d = engine.compute_dashboard_metrics("7d")
    m_30d = engine.compute_dashboard_metrics("30d")
    m_90d = engine.compute_dashboard_metrics("90d")

    # Vérification que le volume d'avis et les métriques évoluent avec l'élargissement de la fenêtre
    periods_dynamic = (
        m_7d["total_reviews"] < m_30d["total_reviews"] < m_90d["total_reviews"]
    )

    if periods_dynamic:
        print(f"  --> SUCCÈS : Recalcul dynamique immédiat constaté :")
        print(f"      • Fenêtre 7 jours   : {m_7d['total_reviews']} avis | Satisfaction = {m_7d['satisfaction_rate']}%")
        print(f"      • Fenêtre 30 jours  : {m_30d['total_reviews']} avis | Satisfaction = {m_30d['satisfaction_rate']}%")
        print(f"      • Fenêtre 90 jours  : {m_90d['total_reviews']} avis | Satisfaction = {m_90d['satisfaction_rate']}%")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Les résultats ne se mettent pas à jour dynamiquement.")

    # -------------------------------------------------------------
    # SYNTHÈSE
    # -------------------------------------------------------------
    print("\n" + "-" * 65)
    print(f"RÉSULTAT : {passed}/{total} critères d'acceptation validés avec succès.")
    if passed == total:
        print(">>> TOUS LES TESTS D'ACCEPTATION US05 SONT VALIDÉS (100% SUCCÈS) <<<")
    print("-" * 65 + "\n")
    return passed == total

if __name__ == "__main__":
    success = run_acceptance_tests()
    sys.exit(0 if success else 1)
