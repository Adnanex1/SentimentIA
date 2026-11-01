"""
Test d'acceptation — US02 Importation des avis
Développeur : Youssef El Amrani
Sprint Backlog : Priorité 2 | Effort : 5 | Valeur : 30

Validation stricte des 3 critères d'acceptation de l'image :
  1. Le fichier CSV est importé.
  2. Les lignes incorrectes sont signalées.
  3. Les avis déjà présents ne sont pas ajoutés une deuxième fois.
"""

import os
import sys
from csv_importer import ReviewCSVImporter

def run_acceptance_tests():
    print("=" * 65)
    print("TEST D'ACCEPTATION — US02 : IMPORTATION DES AVIS (Youssef El Amrani)")
    print("=" * 65)

    importer = ReviewCSVImporter()
    csv_file_path = os.path.join(os.path.dirname(__file__), "sample_import.csv")
    
    passed = 0
    total = 3

    print(f"\nChargement du fichier CSV de test : {csv_file_path}")
    res = importer.import_csv_content(csv_file_path, source_label="CSV Import Test")

    # -------------------------------------------------------------
    # CRITÈRE 1 : Le fichier CSV est importé
    # -------------------------------------------------------------
    print("\n[CRITÈRE 1] Test d'importation globale du fichier CSV...")
    if res.get("success") is True and res.get("imported_count", 0) > 0:
        print(f"  --> SUCCÈS : Fichier CSV importé avec succès.")
        print(f"  --> Nombre d'avis valides intégrés : {res['imported_count']}")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Impossible d'importer le CSV : {res}")

    # -------------------------------------------------------------
    # CRITÈRE 2 : Les lignes incorrectes sont signalées
    # -------------------------------------------------------------
    print("\n[CRITÈRE 2] Test de détection et signalement des lignes incorrectes...")
    incorrect_lines = res.get("incorrect_lines", [])
    if len(incorrect_lines) >= 2:
        print(f"  --> SUCCÈS : {len(incorrect_lines)} lignes incorrectes correctement détectées et signalées :")
        for err in incorrect_lines:
            print(f"      • Ligne {err['line']} : {err['reason']}")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Les anomalies n'ont pas été signalées : {incorrect_lines}")

    # -------------------------------------------------------------
    # CRITÈRE 3 : Les avis déjà présents ne sont pas ajoutés une deuxième fois
    # -------------------------------------------------------------
    print("\n[CRITÈRE 3] Test de déduplication (doublons non ajoutés)...")
    duplicates = res.get("duplicates", [])
    first_import_dup_count = len(duplicates)
    
    # Tentative d'importer une deuxième fois le même fichier
    print("  --> Tentative de ré-importation immédiate du même fichier...")
    res_second_pass = importer.import_csv_content(csv_file_path, source_label="CSV Import 2nd pass")
    second_imported = res_second_pass.get("imported_count", 0)

    if first_import_dup_count >= 2 and second_imported == 0:
        print(f"  --> SUCCÈS : {first_import_dup_count} doublons internes ignorés lors du premier import.")
        print(f"  --> SUCCÈS : 0 avis ajoutés lors de la 2ème passe (100% des avis déjà présents rejetés).")
        passed += 1
    else:
        print(f"  --> ÉCHEC : Des doublons ont été injectés (2ème passe a inséré {second_imported} avis).")

    # -------------------------------------------------------------
    # SYNTHÈSE
    # -------------------------------------------------------------
    print("\n" + "-" * 65)
    print(f"RÉSULTAT : {passed}/{total} critères d'acceptation validés avec succès.")
    if passed == total:
        print(">>> TOUS LES TESTS D'ACCEPTATION US02 SONT VALIDÉS (100% SUCCÈS) <<<")
    print("-" * 65 + "\n")
    return passed == total

if __name__ == "__main__":
    success = run_acceptance_tests()
    sys.exit(0 if success else 1)
