"""
Test d'acceptation — US03 Analyse des sentiments
Développeuse : Salma Mansouri
Sprint Backlog : Priorité 3 | Effort : 8 | Valeur : 35

Validation stricte des 3 critères d'acceptation de l'image :
  1. Le sentiment détecté apparaît pour chaque avis.
  2. Les cas incertains sont signalés.
  3. Le texte original reste consultable.
"""

import sys
from sentiment_analyzer import SentimentAnalyzer

def run_acceptance_tests():
    print("=" * 65)
    print("TEST D'ACCEPTATION — US03 : ANALYSE DES SENTIMENTS (Salma Mansouri)")
    print("=" * 65)

    analyzer = SentimentAnalyzer()
    passed = 0
    total = 3

    test_samples = [
        # Avis positif net
        {"id": 1, "text": "Superbe hôtel, personnel très aimable, literie confortable et chambre impeccable."},
        # Avis négatif net
        {"id": 2, "text": "Séjour catastrophique, chambre sale et odeur nauséabonde dans la salle de bain."},
        # Avis incertain / équilibré
        {"id": 3, "text": "L'hôtel est passable. Le lit est correct mais rien d'exceptionnel pour ce tarif."},
        # Avis mixte (ambigu)
        {"id": 4, "text": "Accueil magnifique et personnel adorable, mais la chambre était terriblement bruyante et sale."}
    ]

    results = [analyzer.analyze_review(item["text"]) for item in test_samples]

    # -------------------------------------------------------------
    # CRITÈRE 1 : Le sentiment détecté apparaît pour chaque avis
    # -------------------------------------------------------------
    print("\n[CRITÈRE 1] Vérification de l'attribution d'un sentiment à chaque avis...")
    all_have_sentiment = all(r.get("sentiment") in ["Positif", "Négatif", "Neutre"] for r in results)
    
    if all_have_sentiment:
        print("  --> SUCCÈS : Chaque avis possède un sentiment clairement identifié :")
        for i, r in enumerate(results, 1):
            print(f"      • Avis #{i} : Sentiment = {r['sentiment']} (Confiance : {r['confidence_score']*100:.1f}%)")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Certains avis n'ont pas de sentiment attribué : {results}")

    # -------------------------------------------------------------
    # CRITÈRE 2 : Les cas incertains sont signalés
    # -------------------------------------------------------------
    print("\n[CRITÈRE 2] Détection et signalement des cas incertains...")
    uncertain_cases = [r for r in results if r.get("is_uncertain") is True]

    if len(uncertain_cases) >= 1:
        print(f"  --> SUCCÈS : {len(uncertain_cases)} cas incertains détectés et signalés :")
        for uc in uncertain_cases:
            print(f"      • Texte : \"{uc['original_text'][:45]}...\"")
            print(f"        Signalement : {uc['uncertainty_reason']}")
        passed += 1
    else:
        print("  --> ÉCHEC : Aucun cas incertain n'a été détecté.")

    # -------------------------------------------------------------
    # CRITÈRE 3 : Le texte original reste consultable
    # -------------------------------------------------------------
    print("\n[CRITÈRE 3] Vérification de la conservation intégrale du texte d'origine...")
    all_original_preserved = all(
        r.get("original_text") == test_samples[i]["text"]
        for i, r in enumerate(results)
    )

    if all_original_preserved:
        print("  --> SUCCÈS : 100% des avis conservent leur texte source textuel sans altération.")
        print(f"      Exemple vérifié : \"{results[0]['original_text']}\"")
        passed += 1
    else:
        print("  --> ÉCHEC : Le texte d'origine a été modifié ou perdu.")

    # -------------------------------------------------------------
    # SYNTHÈSE
    # -------------------------------------------------------------
    print("\n" + "-" * 65)
    print(f"RÉSULTAT : {passed}/{total} critères d'acceptation validés avec succès.")
    if passed == total:
        print(">>> TOUS LES TESTS D'ACCEPTATION US03 SONT VALIDÉS (100% SUCCÈS) <<<")
    print("-" * 65 + "\n")
    return passed == total

if __name__ == "__main__":
    success = run_acceptance_tests()
    sys.exit(0 if success else 1)
