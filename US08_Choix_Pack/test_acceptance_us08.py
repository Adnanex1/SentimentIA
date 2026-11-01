import sys
from pack_manager import SubscriptionPackManager

def run_acceptance_tests():
    print("=" * 65)
    print("TEST D'ACCEPTATION — US08 : CHOIX D'UN PACK")
    print("=" * 65)

    pm = SubscriptionPackManager()
    passed = 0
    total = 3

    # -------------------------------------------------------------
    # CRITÈRE 1 : Les packs Essentiel, Pro et Multi-établissements affichent leurs prix et fonctionnalités
    # -------------------------------------------------------------
    print("\n[CRITÈRE 1] Vérification de l'exposition des 3 packs, de leurs prix et fonctionnalités...")
    catalog = pm.get_catalog_packs()
    packs = catalog.get("packs", {})

    has_essentiel = "essentiel" in packs and "features" in packs["essentiel"] and "price_display" in packs["essentiel"]
    has_pro = "pro" in packs and "features" in packs["pro"] and "price_display" in packs["pro"]
    has_multi = "multi" in packs and "features" in packs["multi"] and "price_display" in packs["multi"]

    if has_essentiel and has_pro and has_multi:
        print("  --> SUCCÈS : Les 3 formules sont parfaitement configurées :")
        for key in ["essentiel", "pro", "multi"]:
            p = packs[key]
            print(f"      • {p['name']} : {p['price_display']} ({len(p['features'])} fonctionnalités)")
            print(f"        Exemple : \"{p['features'][0]}\"")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Packs manquants ou informations incomplètes : {packs.keys()}")

    # -------------------------------------------------------------
    # CRITÈRE 2 : Le pack actif est visible
    # -------------------------------------------------------------
    print("\n[CRITÈRE 2] Visibilité du pack actif pour l'utilisateur connecté...")
    sub_karim = pm.get_user_active_pack("user_karim_riad")
    badge = sub_karim.get("badge_label", "")

    if "Pack Actif" in badge and "Pack Pro" in badge:
        print(f"  --> SUCCÈS : Le pack actif est clairement affiché :")
        print(f"      • Établissement : {sub_karim['hotel_name']}")
        print(f"      • Clé du pack : {sub_karim['active_pack_key']}")
        print(f"      • Badge visuel : \"{badge}\"")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Pack actif invisible ou erroné : {sub_karim}")

    # -------------------------------------------------------------
    # CRITÈRE 3 : Les accès respectent le pack choisi
    # -------------------------------------------------------------
    print("\n[CRITÈRE 3] Contrôle strict des autorisations d'accès selon le pack...")
    # Test A : Utilisateur Essentiel tente d'accéder au Rapport PDF (doit être REFUSÉ)
    access_essentiel_pdf = pm.check_feature_access("user_atlas_budget", "pdf_executive_reports")
    
    # Test B : Utilisateur Pro tente d'accéder au Rapport PDF (doit être AUTORISÉ)
    access_pro_pdf = pm.check_feature_access("user_karim_riad", "pdf_executive_reports")

    # Test C : Utilisateur Pro tente d'accéder au Multi-établissements (doit être REFUSÉ)
    access_pro_multi = pm.check_feature_access("user_karim_riad", "multi_establishment_access")

    # Test D : Utilisateur Multi tente d'accéder au Multi-établissements (doit être AUTORISÉ)
    access_multi_multi = pm.check_feature_access("user_royal_group", "multi_establishment_access")

    rule_a = (access_essentiel_pdf["access_granted"] is False)
    rule_b = (access_pro_pdf["access_granted"] is True)
    rule_c = (access_pro_multi["access_granted"] is False)
    rule_d = (access_multi_multi["access_granted"] is True)

    if rule_a and rule_b and rule_c and rule_d:
        print("  --> SUCCÈS : Les restrictions d'accès sont rigoureusement appliquées :")
        print(f"      • Essentiel -> PDF Reports       : REFUSÉ ({access_essentiel_pdf['required_pack']} requis)")
        print(f"      • Pro       -> PDF Reports       : ACCORDÉ ({access_pro_pdf['message']})")
        print(f"      • Pro       -> Multi-établis.   : REFUSÉ ({access_pro_multi['required_pack']} requis)")
        print(f"      • Multi     -> Multi-établis.   : ACCORDÉ ({access_multi_multi['message']})")
        passed += 1
    else:
        print("  --> ÉCHEC : Violation de la politique de contrôle d'accès selon le pack.")

    # -------------------------------------------------------------
    # SYNTHÈSE
    # -------------------------------------------------------------
    print("\n" + "-" * 65)
    print(f"RÉSULTAT : {passed}/{total} critères d'acceptation validés avec succès.")
    if passed == total:
        print(">>> TOUS LES TESTS D'ACCEPTATION US08 SONT VALIDÉS (100% SUCCÈS) <<<")
    print("-" * 65 + "\n")
    return passed == total

if __name__ == "__main__":
    success = run_acceptance_tests()
    sys.exit(0 if success else 1)
