# US08 — Choix d'un pack

## 🎯 Description & User Story
> **En tant que** responsable,  
> **je veux** choisir un pack adapté à mes besoins  
> **pour** accéder aux fonctionnalités correspondantes.

---

## ✅ Tests d'Acceptation (Critères de Validation)

| # | Critère d'acceptation (selon backlog) | Statut de validation |
|---|---|---|
| **1** | Les packs Essentiel, Pro et Multi-établissements affichent leurs prix et fonctionnalités. | ✅ **Validé** (`pack_manager.py:get_catalog_packs`) |
| **2** | Le pack actif est visible. | ✅ **Validé** (`badge_label` et statut dynamique utilisateur) |
| **3** | Les accès respectent le pack choisi. | ✅ **Validé** (`check_feature_access` bloquant/autorisant selon formule) |

---

## 💻 Fichiers & Extraits de Code Développés et Pushés par Amine

1. **`pack_manager.py` (Backend & Gestion des Droits)** :
   - Définition du catalogue des 3 formules d'abonnement (Essentiel 490 DH/mois, Pro 1 190 DH/mois, Multi-établissements 2 490 DH/mois).
   - Matrice de contrôle d'accès (RBAC basée sur le forfait actif).
   - Gestion dynamique du changement de formule (upgrade/downgrade).

2. **`pack_component.html` (Frontend)** :
   - Grille comparative des offres tarifaires avec cartes d'abonnements interactives.
   - Badge d'identification visuelle du pack actif.
   - Simulation en direct des blocages d'accès selon le forfait en vigueur.

3. **`test_acceptance_us08.py` (Tests Unitaires & d'Acceptation)** :
   - Script exécutable validant l'exhaustivité de l'offre commerciale, la visibilité du statut et l'étanchéité des droits d'accès.

---

## 🧪 Comment Exécuter et Valider la Fonctionnalité

### Exécution du test d'acceptation :
```bash
python US08_Choix_Pack/test_acceptance_us08.py
```

### Visualisation de l'interface :
Ouvrez directement dans votre navigateur :
`US08_Choix_Pack/pack_component.html`

---