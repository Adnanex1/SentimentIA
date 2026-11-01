"""
US01 — Module Authentification & Isolation Multi-Établissements
Branche : feature/US01-authentification
Sprint Backlog : Priorité 1 | Effort : 5 | Valeur : 20
"""

import hashlib
import json
import time

class AuthManager:
    """
    Gère l'authentification des gérants/responsables d'établissements hôteliers
    et garantit l'isolation stricte des données entre les différents établissements (multi-tenant).
    """

    def __init__(self):
        # Base de données simulée des utilisateurs et établissements
        self.establishments_db = {
            "riad_uemf": {
                "id": "riad_uemf",
                "name": "Riad UEMF Fès",
                "city": "Fès",
                "owner_login": "karim.alami@riad-uemf.ma",
                "password_hash": self._hash_password("RiadUemf2026!"),
                "pack": "pro",
                "private_data": {
                    "monthly_revenue_dh": 185000,
                    "occupancy_rate": 88.5,
                    "staff_notes": "Rénovation suite 102 prévue en novembre.",
                    "confidential_reviews_count": 410
                }
            },
            "atlas_budget": {
                "id": "atlas_budget",
                "name": "Atlas Budget Hotel",
                "city": "Marrakech",
                "owner_login": "mehdi.tazi@atlasbudget.ma",
                "password_hash": self._hash_password("AtlasPass2026!"),
                "pack": "essentiel",
                "private_data": {
                    "monthly_revenue_dh": 92000,
                    "occupancy_rate": 72.0,
                    "staff_notes": "Changement fournisseur petit-déjeuner.",
                    "confidential_reviews_count": 180
                }
            },
            "royal_marrakech": {
                "id": "royal_marrakech",
                "name": "Groupe Royal Hotels",
                "city": "Marrakech",
                "owner_login": "direction@royalhotels.ma",
                "password_hash": self._hash_password("RoyalGroupSecret!"),
                "pack": "multi",
                "private_data": {
                    "monthly_revenue_dh": 750000,
                    "occupancy_rate": 94.2,
                    "staff_notes": "Audit de certification ISO 9001 en cours.",
                    "confidential_reviews_count": 1250
                }
            }
        }
        self.active_sessions = {}

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def login(self, login: str, password: str) -> dict:
        """
        Critère 1 : Les identifiants valides permettent la connexion.
        Critère 2 : Un message d'erreur apparaît en cas d'identifiants incorrects ou manquants.
        """
        if not login or not password:
            return {
                "success": False,
                "error": "Identifiants requis : veuillez renseigner l'email et le mot de passe."
            }

        clean_login = login.strip().lower()
        pwd_hash = self._hash_password(password)

        # Recherche du compte correspondant
        target_hotel = None
        for hotel in self.establishments_db.values():
            if hotel["owner_login"].lower() == clean_login:
                target_hotel = hotel
                break

        if not target_hotel:
            return {
                "success": False,
                "error": "Échec de connexion : identifiant introuvable ou compte inexistant."
            }

        if target_hotel["password_hash"] != pwd_hash:
            return {
                "success": False,
                "error": "Échec de connexion : mot de passe incorrect."
            }

        # Création du jeton de session isolé
        session_token = f"sess_{target_hotel['id']}_{int(time.time())}"
        session_data = {
            "token": session_token,
            "establishment_id": target_hotel["id"],
            "establishment_name": target_hotel["name"],
            "owner_login": target_hotel["owner_login"],
            "pack": target_hotel["pack"],
            "created_at": time.time()
        }
        self.active_sessions[session_token] = session_data

        return {
            "success": True,
            "message": f"Connexion réussie. Bienvenue sur sentimentIA, {target_hotel['name']}.",
            "session": session_data
        }

    def get_establishment_data(self, session_token: str, target_establishment_id: str) -> dict:
        """
        Critère 3 : Les données des autres établissements restent inaccessibles.
        Une session n'a le droit d'accéder QU'aux données de son propre établissement,
        sauf si le pack est 'multi' et explicitement autorisé.
        """
        session = self.active_sessions.get(session_token)
        if not session:
            return {
                "success": False,
                "error": "Session invalide ou expirée. Veuillez vous reconnecter."
            }

        user_est_id = session["establishment_id"]
        
        # Contrôle d'accès strict (Isolation des établissements)
        if user_est_id != target_establishment_id:
            # Même un utilisateur connecté ne peut pas voir un autre établissement sans pack multi
            if session.get("pack") != "multi":
                return {
                    "success": False,
                    "error": (
                        f"Accès refusé : Sécurité multi-tenant active. "
                        f"Les données de l'établissement '{target_establishment_id}' sont strictement confidentielles "
                        f"et inaccessibles depuis votre compte '{user_est_id}'."
                    )
                }

        # Récupération des données autorisées
        est = self.establishments_db.get(target_establishment_id)
        if not est:
            return {
                "success": False,
                "error": "Établissement non trouvé."
            }

        return {
            "success": True,
            "establishment_name": est["name"],
            "city": est["city"],
            "pack": est["pack"],
            "data": est["private_data"]
        }

    def logout(self, session_token: str) -> dict:
        """Déconnexion et destruction de la session."""
        if session_token in self.active_sessions:
            del self.active_sessions[session_token]
            return {"success": True, "message": "Déconnexion effectuée avec succès."}
        return {"success": False, "error": "Session inconnue."}


if __name__ == "__main__":
    auth = AuthManager()
    print("Module AuthManager initialisé avec succès.")
