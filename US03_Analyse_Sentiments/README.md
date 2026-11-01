# US03 — Analyse des sentiments

## 📌 Informations du Sprint Backlog
- **Numéro & Nom** : `US03 — Analyse des sentiments`
- **Priorité** : 3
- **Effort estimé** : 8 Story Points
- **Valeur métier** : 35
- **Responsable de la fonctionnalité** : **Salma Mansouri** (Data Scientist & Ingénieure NLP)
- **Branche Git associée** : `feature/US03-analyse-sentiments`

---

## 🎯 Description & User Story
> **En tant que** responsable,  
> **je veux** savoir si les avis sont positifs, négatifs ou neutres  
> **pour** mieux comprendre les retours des clients.

---

## ✅ Tests d'Acceptation (Critères de Validation)

| # | Critère d'acceptation (selon backlog) | Statut de validation |
|---|---|---|
| **1** | Le sentiment détecté apparaît pour chaque avis. | ✅ **Validé** (`sentiment_analyzer.py:analyze_review`) |
| **2** | Les cas incertains sont signalés. | ✅ **Validé** (Alerte sur score proche du seuil neutre ou avis mixtes) |
| **3** | Le texte original reste consultable. | ✅ **Validé** (Champ `original_text` préservé sans troncature ni altération) |

---

## 💻 Fichiers & Extraits de Code Développés et Pushés par Salma

1. **`sentiment_analyzer.py` (NLP & Backend)** :
   - Pipeline de traitement du langage naturel s'appuyant sur le modèle entraîné `outputs/sentiment_model.joblib`.
   - Classification à 3 niveaux : Positif, Négatif et Neutre.
   - Système de détection de l'ambiguïté signalant les avis contradictoires ou proches du seuil 50/50.
   - Préservation stricte de la citation textuelle originale de chaque client.

2. **`sentiment_component.html` (Frontend)** :
   - Interface de visualisation des avis enrichis avec badges d'évaluation (Positif en vert, Négatif en rouge, Neutre en bleu, Incertain en jaune).
   - Zone de citation originale et avertissement pour modération humaine.

3. **`test_acceptance_us03.py` (Tests Unitaires & d'Acceptation)** :
   - Suite de tests validant la détection de sentiments, l'identification de cas incertains et l'intégrité textuelle.

---

## 🧪 Comment Exécuter et Valider la Fonctionnalité

### Exécution du test d'acceptation :
```bash
python US03_Analyse_Sentiments/test_acceptance_us03.py
```

### Visualisation de l'interface :
Ouvrez directement dans votre navigateur :
`US03_Analyse_Sentiments/sentiment_component.html`

---

## 🚀 Historique des Commits Git (Salma Mansouri)
```
commit c3d82716a (HEAD -> feature/US03-analyse-sentiments)
Author: Salma Mansouri <salma.mansouri@equipe-avis.ma>
Date:   Thu Oct 29 14:45:00 2026 +0100

    feat(nlp): implémentation US03 Détection des sentiments & cas incertains
    
    - Intégration du modèle NLP et pipeline d'inférence
    - Classification 3 classes (Positif, Négatif, Neutre)
    - Détection et marquage des cas incertains et avis ambivalents
    - Garantie de conservation du verbatim original client
    - Ajout des tests d'acceptation (3/3 critères validés)
```
