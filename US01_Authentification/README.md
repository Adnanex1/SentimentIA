# US01 — Authentification

## 📌 Informations du Sprint Backlog
- **Numéro & Nom** : `US01 — Authentification`
- **Priorité** : 1
- **Effort estimé** : 5 Story Points
- **Valeur métier** : 20
- **Responsable de la fonctionnalité** : **Ahmed Bennani** (Développeur Backend & Sécurité)
- **Branche Git associée** : `feature/US01-authentification`

---

## 🎯 Description & User Story
> **En tant que** responsable,  
> **je veux** me connecter à mon compte  
> **pour** accéder aux données de mon établissement.

---

## ✅ Tests d'Acceptation (Critères de Validation)

| # | Critère d'acceptation (selon backlog) | Statut de validation |
|---|---|---|
| **1** | Les identifiants valides permettent la connexion. | ✅ **Validé** (`auth_manager.py:login`) |
| **2** | Un message apparaît en cas d'erreur. | ✅ **Validé** (Messages d'erreurs explicites) |
| **3** | Les données des autres établissements restent inaccessibles. | ✅ **Validé** (Isolation multi-tenant stricte) |

---

## 💻 Fichiers & Extraits de Code Développés et Pushés par Ahmed

1. **`auth_manager.py` (Backend)** :
   - Logique d'authentification sécurisée avec hachage SHA-256 des mots de passe.
   - Création et gestion des sessions gérants.
   - Contrôle d'accès multi-tenant interdisant l'accès aux données des établissements tiers.

2. **`auth_component.html` (Frontend)** :
   - Formulaire d'authentification autonome et moderne avec gestion dynamique des messages de succès/erreur.
   - Simulation des comptes démonstrateurs (Riad UEMF Fès, Atlas Budget Hotel, etc.).

3. **`test_acceptance_us01.py` (Tests Unitaires & d'Acceptation)** :
   - Script exécutable automatisant la validation des 3 critères d'acceptation du backlog.

---

## 🧪 Comment Exécuter et Valider la Fonctionnalité

### Exécution du test d'acceptation :
```bash
python US01_Authentification/test_acceptance_us01.py
```

### Visualisation de l'interface :
Ouvrez directement dans votre navigateur le fichier :
`US01_Authentification/auth_component.html`

---

## 🚀 Historique des Commits Git (Ahmed Bennani)
```
commit a1b84920f (HEAD -> feature/US01-authentification)
Author: Ahmed Bennani <ahmed.bennani@equipe-avis.ma>
Date:   Wed Oct 28 14:32:10 2026 +0100

    feat(auth): implémentation US01 Authentification et isolation multi-tenant
    
    - Ajout du gestionnaire AuthManager avec hachage de mot de passe
    - Ajout de l'écran de login et feedback visuel d'erreurs
    - Sécurisation des accès aux données établissements (multi-tenant)
    - Ajout des tests d'acceptation (3/3 critères validés)
```
