"""
Test d'acceptation — US07 Réponses assistées par IA
Développeuse : Sarah Berrada
Sprint Backlog : Priorité 7 | Effort : 8 | Valeur : 25

Validation stricte des 3 critères d'acceptation de l'image :
  1. La réponse tient compte de l'avis.
  2. Le responsable peut la modifier ou la refuser.
  3. Aucune réponse n'est publiée sans sa validation.
"""

import sys
from ai_response_assistant import AIResponseAssistant

def run_acceptance_tests():
    print("=" * 65)
    print("TEST D'ACCEPTATION — US07 : RÉPONSES ASSISTÉES PAR IA (Sarah Berrada)")
    print("=" * 65)

    assistant = AIResponseAssistant()
    passed = 0
    total = 3

    review_sample = {
        "id": 501,
        "author": "Mme Bennani",
        "text": "L'accueil était formidable et le petit-déjeuner copieux, mais le bruit de la rue la nuit était gênant.",
        "lang": "FR",
        "pos_aspects": ["l'accueil formidable", "le petit-déjeuner copieux"],
        "neg_aspects": ["le bruit de la rue"]
    }

    # Génération initiale de la proposition
    proposal = assistant.generate_response_proposal(review_sample, establishment_name="Riad UEMF Fès")

    # -------------------------------------------------------------
    # CRITÈRE 1 : La réponse tient compte de l'avis
    # -------------------------------------------------------------
    print("\n[CRITÈRE 1] Prise en compte du contexte (points positifs et négatifs)...")
    draft = proposal["draft_text"].lower()
    takes_pos_into_account = any("accueil" in draft or "petit-déjeuner" in draft for _ in [1])
    takes_neg_into_account = any("bruit" in draft for _ in [1])

    if takes_pos_into_account and takes_neg_into_account:
        print("  --> SUCCÈS : La réponse générée intègre fidèlement le contexte de l'avis :")
        print(f"      • Points valorisés : {proposal['addressed_positives']}")
        print(f"      • Anomalies adressées : {proposal['addressed_negatives']}")
        print(f"      • Extrait de la réponse : \"{proposal['draft_text'][:120]}...\"")
        passed += 1
    else:
        print("  --> ÉCHEC : La réponse ne tient pas compte des spécificités de l'avis.")

    # -------------------------------------------------------------
    # CRITÈRE 2 : Le responsable peut la modifier ou la refuser
    # -------------------------------------------------------------
    print("\n[CRITÈRE 2] Possibilité de modification et de refus par le responsable...")
    # 2.a Test de modification
    custom_text = "Bonjour Mme Bennani, nous vous remercions pour vos compliments sur l'accueil. Des doubles vitrages sont en cours d'installation."
    res_mod = assistant.modify_proposal(proposal["id"], custom_text)

    # 2.b Test de refus sur un second cas
    p2 = assistant.generate_response_proposal({"id": 502, "text": "Service lent.", "lang": "FR"})
    res_rej = assistant.reject_proposal(p2["id"], reason="Ton trop générique")

    if res_mod.get("success") is True and res_rej.get("success") is True:
        print(f"  --> SUCCÈS : Modification autorisée et prise en compte : \"{res_mod['final_text'][:60]}...\"")
        print(f"  --> SUCCÈS : Refus pris en compte avec motif : \"{res_rej['message']}\"")
        passed += 1
    else:
        print("  --> ÉCHEC : Incapacité de modifier ou refuser la proposition.")

    # -------------------------------------------------------------
    # CRITÈRE 3 : Aucune réponse n'est publiée sans sa validation
    # -------------------------------------------------------------
    print("\n[CRITÈRE 3] Blocage strict de publication sans validation humaine préalable...")
    p3 = assistant.generate_response_proposal({"id": 503, "text": "Super hôtel.", "lang": "FR"})
    
    # Tentative 1 : Publication sans validation expresse du manager (doit échouer)
    res_blocked = assistant.validate_and_publish(p3["id"], confirm_by_manager=False)
    
    # Tentative 2 : Publication avec validation expresse du manager (doit réussir)
    res_allowed = assistant.validate_and_publish(p3["id"], confirm_by_manager=True)

    if res_blocked.get("success") is False and res_allowed.get("success") is True:
        print("  --> SUCCÈS : Tentative sans validation bloquée avec avertissement de sécurité :")
        print(f"      \"{res_blocked['error']}\"")
        print(f"  --> SUCCÈS : Publication validée uniquement après accord du gérant ({res_allowed['status']}).")
        passed += 1
    else:
        print("  --> ÉCHEC : Une réponse a été publiée sans validation humaine !")

    # -------------------------------------------------------------
    # SYNTHÈSE
    # -------------------------------------------------------------
    print("\n" + "-" * 65)
    print(f"RÉSULTAT : {passed}/{total} critères d'acceptation validés avec succès.")
    if passed == total:
        print(">>> TOUS LES TESTS D'ACCEPTATION US07 SONT VALIDÉS (100% SUCCÈS) <<<")
    print("-" * 65 + "\n")
    return passed == total

if __name__ == "__main__":
    success = run_acceptance_tests()
    sys.exit(0 if success else 1)
