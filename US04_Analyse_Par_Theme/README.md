# US04 — Analyse par thème

## 📌 Informations du Sprint Backlog
- **Numéro & Nom** : `US04 — Analyse par thème`
- **Priorité** : 4
- **Effort estimé** : 13 Story Points
- **Valeur métier** : 40
- **Responsable de la fonctionnalité** : **Mehdi Chraibi** (Développeur NLP / Text Mining)
- **Branche Git associée** : `feature/US04-analyse-par-theme`

---

## 🎯 Description & User Story
> **En tant que** responsable,  
> **je veux** connaître les sujets évoqués  
> **pour** identifier les points forts et les problèmes.

---

## ✅ Tests d'Acceptation (Critères de Validation)

| # | Critère d'acceptation (selon backlog) | Statut de validation |
|---|---|---|
| **1** | La propreté, l'accueil et le confort sont identifiés. | ✅ **Validé** (`theme_extractor.py:extract_themes`) |
| **2** | Un avis peut avoir plusieurs thèmes avec des sentiments différents. | ✅ **Validé** (Gestion de polarités opposées dans un même texte) |
| **3** | Les extraits correspondants sont affichés. | ✅ **Validé** (Segmentation en phrases et extraction des citations clés) |

---

## 💻 Fichiers & Extraits de Code Développés et Pushés par Mehdi

1. **`theme_extractor.py` (NLP & Backend)** :
   - Reconnaissance explicite des aspects prioritaires : **Propreté**, **Accueil & Personnel**, **Confort & Chambre** (+ Bruit, Restauration).
   - Analyse de polarité fine par aspect permettant d'attribuer un sentiment positif à l'accueil tout en marquant la propreté comme négative sur le même avis.
   - Algorithme de découpage et de matching isolant la phrase exacte relative à chaque thème.

2. **`theme_component.html` (Frontend)** :
   - Interface mettant en valeur les tags thématiques colorés (vert pour positif, rouge pour négatif) et les blocs d'extraits textuels avec surlignage.

3. **`test_acceptance_us04.py` (Tests Unitaires & d'Acceptation)** :
   - Test d'acceptation complet validant la détection des 3 piliers, la divergence de sentiments et l'extraction de phrases.

---

## 🧪 Comment Exécuter et Valider la Fonctionnalité

### Exécution du test d'acceptation :
```bash
python US04_Analyse_Par_Theme/test_acceptance_us04.py
```

### Visualisation de l'interface :
Ouvrez directement dans votre navigateur :
`US04_Analyse_Par_Theme/theme_component.html`

---

## 🚀 Historique des Commits Git (Mehdi Chraibi)
```
commit d4e71945c (HEAD -> feature/US04-analyse-par-theme)
Author: Mehdi Chraibi <mehdi.chraibi@equipe-avis.ma>
Date:   Thu Oct 29 17:10:22 2026 +0100

    feat(themes): implémentation US04 Détection par thèmes & extraits textuels
    
    - Implémentation de l'extraction Propreté, Accueil et Confort
    - Support des sentiments multi-polaires dans un avis unique
    - Extraction dynamique des snippets / phrases justificatives
    - Ajout des tests d'acceptation (3/3 critères validés)
```
