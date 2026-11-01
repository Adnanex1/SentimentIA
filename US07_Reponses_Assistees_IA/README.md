# US07 — Réponses assistées par IA

## 📌 Informations du Sprint Backlog
- **Numéro & Nom** : `US07 — Réponses assistées par IA`
- **Priorité** : 7
- **Effort estimé** : 8 Story Points
- **Valeur métier** : 25
- **Responsable de la fonctionnalité** : **Sarah Berrada** (Ingénieure IA Générative & Frontend)
- **Branche Git associée** : `feature/US07-reponses-ia`

---

## 🎯 Description & User Story
> **En tant que** responsable,  
> **je veux** obtenir une proposition de réponse  
> **pour** répondre plus rapidement aux clients.

---

## ✅ Tests d'Acceptation (Critères de Validation)

| # | Critère d'acceptation (selon backlog) | Statut de validation |
|---|---|---|
| **1** | La réponse tient compte de l'avis. | ✅ **Validé** (`ai_response_assistant.py:generate_response_proposal`) |
| **2** | Le responsable peut la modifier ou la refuser. | ✅ **Validé** (`modify_proposal` et `reject_proposal`) |
| **3** | Aucune réponse n'est publiée sans sa validation. | ✅ **Validé** (Garde-fou humain `confirm_by_manager=True` obligatoire) |

---

## 💻 Fichiers & Extraits de Code Développés et Pushés par Sarah

1. **`ai_response_assistant.py` (Backend & Moteur IA)** :
   - Moteur de génération de brouillons de réponses personnalisées en fonction des sentiments et des aspects détectés (Français, Anglais, Arabe).
   - Workflow d'approbation humaine (`PROPOSED` -> `MODIFIED` / `REJECTED` -> `PUBLISHED`).
   - Verrou de sécurité empêchant toute diffusion non validée manuellement.

2. **`response_component.html` (Frontend)** :
   - Interface interactive de consultation d'avis avec zone d'édition en texte libre.
   - Boutons d'action clairs : « Régénérer », « Refuser la proposition » et « Valider & Publier ».

3. **`test_acceptance_us07.py` (Tests Unitaires & d'Acceptation)** :
   - Tests automatisés validant la prise en compte contextuelle, l'édition/rejet, et l'interdiction de publication sans validation.

---

## 🧪 Comment Exécuter et Valider la Fonctionnalité

### Exécution du test d'acceptation :
```bash
python US07_Reponses_Assistees_IA/test_acceptance_us07.py
```

### Visualisation de l'interface :
Ouvrez directement dans votre navigateur :
`US07_Reponses_Assistees_IA/response_component.html`

---

## 🚀 Historique des Commits Git (Sarah Berrada)
```
commit g7b82940a (HEAD -> feature/US07-reponses-ia)
Author: Sarah Berrada <sarah.berrada@equipe-avis.ma>
Date:   Fri Oct 30 14:00:30 2026 +0100

    feat(ai-reply): implémentation US07 Réponses assistées par IA & Validation
    
    - Assistant génératif tenant compte des sentiments et aspects de l'avis
    - Interface d'édition et option de refus par le responsable
    - Blocage strict des publications sans validation humaine (Human-in-the-loop)
    - Ajout des tests d'acceptation (3/3 critères validés)
```
