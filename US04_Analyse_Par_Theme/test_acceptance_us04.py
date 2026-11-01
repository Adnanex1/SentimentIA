"""
Test d'acceptation — US04 Analyse par thème
Développeur : Mehdi Chraibi
Sprint Backlog : Priorité 4 | Effort : 13 | Valeur : 40

Validation stricte des 3 critères d'acceptation de l'image :
  1. La propreté, l'accueil et le confort sont identifiés.
  2. Un avis peut avoir plusieurs thèmes avec des sentiments différents.
  3. Les extraits correspondants sont affichés.
"""

import sys
from theme_extractor import ThemeAspectExtractor

def run_acceptance_tests():
    print("=" * 65)
    print("TEST D'ACCEPTATION — US04 : ANALYSE PAR THÈME (Mehdi Chraibi)")
    print("=" * 65)

    extractor = ThemeAspectExtractor()
    passed = 0
    total = 3

    # Avis de test typique combinant les 3 thèmes majeurs avec des sentiments distincts
    multi_theme_review = (
        "L'accueil de l'équipe et le personnel étaient remarquables et très chaleureux. "
        "Cependant, la propreté de la douche était négligée avec des taches suspectes. "
        "Pour le confort, le lit et le matelas de la chambre étaient particulièrement douillets et spacieux."
    )

    result = extractor.extract_themes(multi_theme_review)
    detected = result["themes_detected"]
    details = result["theme_details"]

    # -------------------------------------------------------------
    # CRITÈRE 1 : La propreté, l'accueil et le confort sont identifiés
    # -------------------------------------------------------------
    print("\n[CRITÈRE 1] Identification obligatoire de la Propreté, l'Accueil et le Confort...")
    req_themes = ["proprete", "accueil", "confort"]
    all_three_found = all(t in detected for t in req_themes)

    if all_three_found:
        print(f"  --> SUCCÈS : Les 3 thèmes clés requis sont parfaitement identifiés :")
        for t in req_themes:
            print(f"      • {details[t]['label']} (Clé : {t})")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Thèmes manquants parmi {req_themes}. Trouvés : {detected}")

    # -------------------------------------------------------------
    # CRITÈRE 2 : Un avis peut avoir plusieurs thèmes avec des sentiments différents
    # -------------------------------------------------------------
    print("\n[CRITÈRE 2] Multi-thèmes avec sentiments différents au sein du même avis...")
    accueil_sentiment = details.get("accueil", {}).get("sentiment")
    proprete_sentiment = details.get("proprete", {}).get("sentiment")
    confort_sentiment = details.get("confort", {}).get("sentiment")

    has_different_sentiments = (accueil_sentiment != proprete_sentiment)

    if has_different_sentiments:
        print("  --> SUCCÈS : Sentiments distincts et contrastés détectés pour cet avis :")
        print(f"      • Accueil : {accueil_sentiment} (Polarité : {details['accueil']['polarity']})")
        print(f"      • Propreté : {proprete_sentiment} (Polarité : {details['proprete']['polarity']})")
        print(f"      • Confort : {confort_sentiment} (Polarité : {details['confort']['polarity']})")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Tous les thèmes ont reçu le même sentiment sans nuance : {details}")

    # -------------------------------------------------------------
    # CRITÈRE 3 : Les extraits correspondants sont affichés
    # -------------------------------------------------------------
    print("\n[CRITÈRE 3] Extraction et affichage des extraits textuels correspondants...")
    all_have_excerpts = all(
        len(details[t].get("excerpts", [])) > 0
        for t in req_themes
    )

    if all_have_excerpts:
        print("  --> SUCCÈS : Des extraits textuels spécifiques ont été isolés pour chaque thème :")
        for t in req_themes:
            ex = details[t]["excerpts"][0]
            print(f"      • Extrait [{details[t]['label']}] : \"{ex}\"")
        passed += 1
    else:
        print("  --> ÉCHEC : Extraits manquants pour certains thèmes.")

    # -------------------------------------------------------------
    # SYNTHÈSE
    # -------------------------------------------------------------
    print("\n" + "-" * 65)
    print(f"RÉSULTAT : {passed}/{total} critères d'acceptation validés avec succès.")
    if passed == total:
        print(">>> TOUS LES TESTS D'ACCEPTATION US04 SONT VALIDÉS (100% SUCCÈS) <<<")
    print("-" * 65 + "\n")
    return passed == total

if __name__ == "__main__":
    success = run_acceptance_tests()
    sys.exit(0 if success else 1)
