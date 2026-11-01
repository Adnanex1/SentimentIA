# US02 — Importation des avis

## 📌 Informations du Sprint Backlog
- **Numéro & Nom** : `US02 — Importation des avis`
- **Priorité** : 2
- **Effort estimé** : 5 Story Points
- **Valeur métier** : 30
- **Responsable de la fonctionnalité** : **Youssef El Amrani** (Développeur Ingestion & Data Pipelines)
- **Branche Git associée** : `feature/US02-importation-avis`

---

## 🎯 Description & User Story
> **En tant que** responsable,  
> **je veux** importer les avis de mes clients  
> **pour** les retrouver au même endroit.

---

## ✅ Tests d'Acceptation (Critères de Validation)

| # | Critère d'acceptation (selon backlog) | Statut de validation |
|---|---|---|
| **1** | Le fichier CSV est importé. | ✅ **Validé** (`csv_importer.py:import_csv_content`) |
| **2** | Les lignes incorrectes sont signalées. | ✅ **Validé** (Rapport d'erreurs avec motif et numéro de ligne) |
| **3** | Les avis déjà présents ne sont pas ajoutés une deuxième fois. | ✅ **Validé** (Filtrage strict par hachage MD5 du texte normalisé) |

---

## 💻 Fichiers & Extraits de Code Développés et Pushés par Youssef

1. **`csv_importer.py` (Backend)** :
   - Moteur d'ingestion tolérant aux délimiteurs (virgules, points-virgules).
   - Validateur de structure rejetant les avis vides, trop courts ou malformés.
   - Système de déduplication par empreinte numérique garantissant l'unicité de chaque avis dans la base de données.

2. **`sample_import.csv` (Jeu de données)** :
   - Fichier de test contenant un mix représentatif d'avis valides, de lignes corrompues et de doublons intentionnels pour vérifier les contrôles qualité.

3. **`import_component.html` (Frontend)** :
   - Interface de glisser-déposer de fichiers CSV avec compteur d'avis acceptés, d'erreurs signalées et de doublons évités.

4. **`test_acceptance_us02.py` (Tests Unitaires & d'Acceptation)** :
   - Automatisation complète des tests vérifiant l'import, le signalement d'erreurs et la non-redondance.

---

## 🧪 Comment Exécuter et Valider la Fonctionnalité

### Exécution du test d'acceptation :
```bash
python US02_Importation_Avis/test_acceptance_us02.py
```

### Visualisation de l'interface :
Ouvrez directement dans votre navigateur :
`US02_Importation_Avis/import_component.html`

---

## 🚀 Historique des Commits Git (Youssef El Amrani)
```
commit b2c93817e (HEAD -> feature/US02-importation-avis)
Author: Youssef El Amrani <youssef.elamrani@equipe-avis.ma>
Date:   Thu Oct 29 10:15:42 2026 +0100

    feat(import): implémentation US02 Importation des avis CSV
    
    - Implémentation du parseur CSV robuste et tolérant
    - Détection et signalement des lignes incorrectes (< 5 carac, NaN, missing)
    - Déduplication automatique évitant l'insertion double d'avis existants
    - Création du dataset de test sample_import.csv
    - Ajout des tests d'acceptation (3/3 critères validés)
```
