# sentimentIA — Organisation Collaborative du Projet en Équipe

Ce document récapitule l'organisation en équipe du projet **sentimentIA** (Plateforme d'intelligence et d'analyse des avis hôteliers).  
Le projet a été structuré en **8 modules fonctionnels distincts**, calqués exactement sur le tableau de User Stories du Sprint Backlog.

---


---

## 📂 Contenu Standard de Chaque Dossier de Fonctionnalité

Chaque dossier a été conçu pour attester du travail individuel poussé par le membre responsable :

```
US0x_[Nom_Fonctionnalite]/
├── README.md               # Fiche de livraison (rôle, critères d'acceptation, commit log)
├── [module_backend].py     # Code backend Python extrait et autonome
├── [composant].html        # Interface utilisateur HTML/CSS/JS isolée
└── test_acceptance_us0x.py # Script de validation automatique des critères d'acceptation
```

---

## 🧪 Exécution des Tests

### 1. Lancer la validation globale de l'équipe (toutes les 8 US) :
```bash
python run_all_acceptance_tests.py
```

### 2. Tester une fonctionnalité spécifique de manière isolée :
- **US01 (Ahmed)** : `python US01_Authentification/test_acceptance_us01.py`
- **US02 (Youssef)** : `python US02_Importation_Avis/test_acceptance_us02.py`
- **US03 (Salma)** : `python US03_Analyse_Sentiments/test_acceptance_us03.py`
- **US04 (Mehdi)** : `python US04_Analyse_Par_Theme/test_acceptance_us04.py`
- **US05 (Fatima-Zahra)** : `python US05_Tableau_De_Bord/test_acceptance_us05.py`
- **US06 (Omar)** : `python US06_Rapport_PDF/test_acceptance_us06.py`
- **US07 (Sarah)** : `python US07_Reponses_Assistees_IA/test_acceptance_us07.py`
- **US08 (Amine)** : `python US08_Choix_Pack/test_acceptance_us08.py`

---

## 🌐 Application Intégrée Principale (Non modifiée)

Conformément à la consigne « sans rien changer », l'application intégrée d'origine à la racine reste 100% opérationnelle :
- **Serveur API Backend** : `python app_server.py` (écoute sur le port `5000`)
- **Application Web Globale** : `sentimentIA.html` (accessible sur `http://localhost:5000/sentimentIA.html`)
- **Modèle NLP d'origine** : `outputs/sentiment_model.joblib`
- **Dataset initial** : `Hotel_Reviews.csv`
