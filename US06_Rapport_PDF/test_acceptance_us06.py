"""
Test d'acceptation — US06 Rapport PDF
Développeur : Omar Alaoui
Sprint Backlog : Priorité 6 | Effort : 5 | Valeur : 25

Validation stricte des 3 critères d'acceptation de l'image :
  1. Le PDF présente la période, les points forts et les problèmes avec des exemples.
  2. Les chiffres correspondent au tableau de bord.
  3. Le rapport est lisible et téléchargeable.
"""

import os
import sys
from pdf_report_generator import PDFReportGenerator

def run_acceptance_tests():
    print("=" * 65)
    print("TEST D'ACCEPTATION — US06 : RAPPORT PDF (Omar Alaoui)")
    print("=" * 65)

    generator = PDFReportGenerator()
    passed = 0
    total = 3

    # Données issues directement du tableau de bord (US05)
    dashboard_kpi = {
        "total_reviews": 37,
        "satisfaction_rate": 73.0,
        "sentiments": {
            "positif": {"count": 27, "percentage": 73.0},
            "negatif": {"count": 10, "percentage": 27.0}
        }
    }

    report_result = generator.generate_report(
        establishment_name="Riad UEMF Fès",
        period_label="01 Oct 2026 - 30 Oct 2026 (30 jours)",
        dashboard_metrics=dashboard_kpi
    )

    # -------------------------------------------------------------
    # CRITÈRE 1 : Le PDF présente la période, les points forts et les problèmes avec des exemples
    # -------------------------------------------------------------
    print("\n[CRITÈRE 1] Présence de la période, des forces et des faiblesses avec exemples...")
    has_period = len(report_result.get("period", "")) > 0
    has_strengths_with_ex = (
        len(report_result.get("points_forts", [])) > 0 and 
        all("exemple" in item for item in report_result["points_forts"])
    )
    has_problems_with_ex = (
        len(report_result.get("problemes", [])) > 0 and 
        all("exemple" in item for item in report_result["problemes"])
    )

    if has_period and has_strengths_with_ex and has_problems_with_ex:
        print(f"  --> SUCCÈS : Période mentionnée : \"{report_result['period']}\"")
        print(f"  --> SUCCÈS : {len(report_result['points_forts'])} points forts documentés avec exemples :")
        for pf in report_result["points_forts"]:
            print(f"      • {pf['theme']} ({pf['score']}) -> {pf['exemple']}")
        print(f"  --> SUCCÈS : {len(report_result['problemes'])} problèmes documentés avec exemples :")
        for pb in report_result["problemes"]:
            print(f"      • {pb['theme']} ({pb['score']}) -> {pb['exemple']}")
        passed += 1
    else:
        print("  --> ÉCHEC : Éléments descriptifs ou exemples manquants.")

    # -------------------------------------------------------------
    # CRITÈRE 2 : Les chiffres correspondent au tableau de bord
    # -------------------------------------------------------------
    print("\n[CRITÈRE 2] Concordance stricte des chiffres avec le tableau de bord...")
    matched = report_result.get("matched_kpi", {})
    is_total_exact = matched.get("total_reviews") == dashboard_kpi["total_reviews"]
    is_sat_exact = matched.get("satisfaction_rate") == dashboard_kpi["satisfaction_rate"]
    is_pos_exact = matched.get("positive_count") == dashboard_kpi["sentiments"]["positif"]["count"]
    is_neg_exact = matched.get("negative_count") == dashboard_kpi["sentiments"]["negatif"]["count"]

    if is_total_exact and is_sat_exact and is_pos_exact and is_neg_exact:
        print("  --> SUCCÈS : Concordance 100% exacte avec le Dashboard :")
        print(f"      • Total avis : {matched['total_reviews']} (Dashboard : {dashboard_kpi['total_reviews']})")
        print(f"      • Satisfaction : {matched['satisfaction_rate']}% (Dashboard : {dashboard_kpi['satisfaction_rate']}%)")
        print(f"      • Positifs / Négatifs : {matched['positive_count']} / {matched['negative_count']}")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Discordance entre le rapport et le dashboard : {matched}")

    # -------------------------------------------------------------
    # CRITÈRE 3 : Le rapport est lisible et téléchargeable
    # -------------------------------------------------------------
    print("\n[CRITÈRE 3] Vérification de la lisibilité et de la disponibilité au téléchargement...")
    pdf_path = report_result.get("report_file_pdf")
    html_path = report_result.get("report_file_html")

    is_accessible = (
        pdf_path is not None and 
        os.path.exists(pdf_path) and 
        os.path.getsize(pdf_path) > 500
    )

    if is_accessible:
        print("  --> SUCCÈS : Fichier rapport généré, lisible et disponible pour téléchargement :")
        print(f"      • Fichier PDF : {pdf_path} ({os.path.getsize(pdf_path)} octets)")
        print(f"      • Version HTML : {html_path} ({os.path.getsize(html_path)} octets)")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Fichier introuvable ou illisible.")

    # -------------------------------------------------------------
    # SYNTHÈSE
    # -------------------------------------------------------------
    print("\n" + "-" * 65)
    print(f"RÉSULTAT : {passed}/{total} critères d'acceptation validés avec succès.")
    if passed == total:
        print(">>> TOUS LES TESTS D'ACCEPTATION US06 SONT VALIDÉS (100% SUCCÈS) <<<")
    print("-" * 65 + "\n")
    return passed == total

if __name__ == "__main__":
    success = run_acceptance_tests()
    sys.exit(0 if success else 1)
