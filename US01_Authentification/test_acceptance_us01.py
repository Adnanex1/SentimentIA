"""
Test d'acceptation — US01 Authentification
Développeur : Ahmed Bennani
Sprint Backlog : Priorité 1 | Effort : 5 | Valeur : 20

Validation stricte des 3 critères d'acceptation de l'image :
  1. Les identifiants valides permettent la connexion.
  2. Un message apparaît en cas d'erreur.
  3. Les données des autres établissements restent inaccessibles.
"""

import sys
from auth_manager import AuthManager

def run_acceptance_tests():
    print("=" * 65)
    print("TEST D'ACCEPTATION — US01 : AUTHENTIFICATION (Ahmed Bennani)")
    print("=" * 65)

    auth = AuthManager()
    passed = 0
    total = 3

    # -------------------------------------------------------------
    # CRITÈRE 1 : Les identifiants valides permettent la connexion
    # -------------------------------------------------------------
    print("\n[CRITÈRE 1] Test avec identifiants valides...")
    res_valid = auth.login("karim.alami@riad-uemf.ma", "RiadUemf2026!")
    if res_valid.get("success") is True and "session" in res_valid:
        token_riad = res_valid["session"]["token"]
        print(f"  --> SUCCÈS : Connexion autorisée. Token : {token_riad}")
        print(f"  --> Message retourné : {res_valid.get('message')}")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Connexion refusée avec identifiants valides : {res_valid}")

    # -------------------------------------------------------------
    # CRITÈRE 2 : Un message apparaît en cas d'erreur
    # -------------------------------------------------------------
    print("\n[CRITÈRE 2] Test avec identifiants invalides (mot de passe erroné)...")
    res_invalid_pwd = auth.login("karim.alami@riad-uemf.ma", "FauxMotDePasse123")
    res_invalid_user = auth.login("inconnu@hotel.ma", "Quelconque")

    has_error_msg_1 = (res_invalid_pwd.get("success") is False and len(res_invalid_pwd.get("error", "")) > 0)
    has_error_msg_2 = (res_invalid_user.get("success") is False and len(res_invalid_user.get("error", "")) > 0)

    if has_error_msg_1 and has_error_msg_2:
        print(f"  --> SUCCÈS : Message d'erreur explicite généré : '{res_invalid_pwd.get('error')}'")
        print(f"  --> SUCCÈS : Message d'erreur utilisateur inconnu : '{res_invalid_user.get('error')}'")
        passed += 1
    else:
        print("  --> ÉCHEC : Aucun message d'erreur ou connexion indue.")

    # -------------------------------------------------------------
    # CRITÈRE 3 : Les données des autres établissements restent inaccessibles
    # -------------------------------------------------------------
    print("\n[CRITÈRE 3] Test d'accès aux données des autres établissements...")
    # Karim Alami (Riad UEMF) tente d'accéder aux données confidentielles de l'Atlas Budget Hotel
    riad_token = res_valid["session"]["token"]
    
    # 3.1 Accès à son propre établissement (autorisé)
    own_data = auth.get_establishment_data(riad_token, "riad_uemf")
    # 3.2 Tentative d'accès à un autre établissement (doit être STRICTEMENT REFUSÉ)
    foreign_data = auth.get_establishment_data(riad_token, "atlas_budget")

    if own_data.get("success") is True and foreign_data.get("success") is False:
        print(f"  --> SUCCÈS : Accès à son propre établissement accordé : {own_data.get('establishment_name')}")
        print(f"  --> SUCCÈS : Tentative d'intrusion bloquée avec message de sécurité :")
        print(f"      \"{foreign_data.get('error')}\"")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Fuite de données multi-tenant détectée ! {foreign_data}")

    # -------------------------------------------------------------
    # SYNTHÈSE
    # -------------------------------------------------------------
    print("\n" + "-" * 65)
    print(f"RÉSULTAT : {passed}/{total} critères d'acceptation validés avec succès.")
    if passed == total:
        print(">>> TOUS LES TESTS D'ACCEPTATION US01 SONT VALIDÉS (100% SUCCÈS) <<<")
    print("-" * 65 + "\n")
    return passed == total

if __name__ == "__main__":
    success = run_acceptance_tests()
    sys.exit(0 if success else 1)
