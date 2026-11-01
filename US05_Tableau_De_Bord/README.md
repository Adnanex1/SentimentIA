# US05 — Tableau de bord

## 📌 Informations du Sprint Backlog
- **Numéro & Nom** : `US05 — Tableau de bord`
- **Priorité** : 5
- **Effort estimé** : 8 Story Points
- **Valeur métier** : 35
- **Responsable de la fonctionnalité** : **Fatima-Zahra Tahiri** (Développeuse Frontend & Analytics)
- **Branche Git associée** : `feature/US05-tableau-de-bord`

---

## 🎯 Description & User Story
> **En tant que** directeur,  
> **je veux** consulter une synthèse des avis  
> **pour** suivre la satisfaction des clients.

---

## ✅ Tests d'Acceptation (Critères de Validation)

| # | Critère d'acceptation (selon backlog) | Statut de validation |
|---|---|---|
| **1** | Le tableau affiche le nombre d'avis, les sentiments et les principaux thèmes. | ✅ **Validé** (`dashboard_analytics.py:compute_dashboard_metrics`) |
| **2** | Les résultats se mettent à jour selon la période choisie. | ✅ **Validé** (Recalcul dynamique selon filtres 7j, 30j, 90j et historique complet) |

---

## 💻 Fichiers & Extraits de Code Développés et Pushés par Fatima-Zahra

1. **`dashboard_analytics.py` (Backend & Moteur de Métriques)** :
   - Agrégation du volume total d'avis et taux de satisfaction en temps réel.
   - Ventilation fine des sentiments (positif, négatif, neutre en % et volume).
   - Détection et classement des thèmes les plus prévalents dans les retours clients.
   - Système de fenêtrage temporel dynamique filtrant les données selon la période sélectionnée.

2. **`dashboard_component.html` (Frontend)** :
   - Interface de pilotage directionnelle avec cartes KPI (KPI Total, Satisfaction %, Positifs, Négatifs).
   - Jauge proportionnelle des sentiments et liste des thèmes dominants.
   - Sélecteur de période dynamique avec rafraîchissement réactif sans rechargement de page.

3. **`test_acceptance_us05.py` (Tests Unitaires & d'Acceptation)** :
   - Validation automatisée des métriques calculées et de l'ajustement dynamique des résultats lors du changement de période.

---

## 🧪 Comment Exécuter et Valider la Fonctionnalité

### Exécution du test d'acceptation :
```bash
python US05_Tableau_De_Bord/test_acceptance_us05.py
```

### Visualisation de l'interface :
Ouvrez directement dans votre navigateur :
`US05_Tableau_De_Bord/dashboard_component.html`

---

## 🚀 Historique des Commits Git (Fatima-Zahra Tahiri)
```
commit e5f61829d (HEAD -> feature/US05-tableau-de-bord)
Author: Fatima-Zahra Tahiri <fatimazahra.tahiri@equipe-avis.ma>
Date:   Fri Oct 30 09:30:15 2026 +0100

    feat(dashboard): implémentation US05 Tableau de bord directionnel
    
    - Moteur de calcul des KPI (volume, sentiments %, top thèmes)
    - Ajout du filtrage temporel dynamique (7j, 30j, 90j, tout)
    - Conception de l'interface responsive pour la direction
    - Ajout des tests d'acceptation (2/2 critères validés)
```
