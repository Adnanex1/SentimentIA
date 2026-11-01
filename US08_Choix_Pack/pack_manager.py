from typing import Dict, Any, List

class SubscriptionPackManager:
    """
    Gère les formules d'abonnements hôteliers :
    - Exposition des tarifs et fonctionnalités des 3 offres (Essentiel, Pro, Multi-établissements)
    - Affichage clair et dynamique du pack actuellement actif
    - Contrôle strict des permissions et blocage des modules hors forfait.
    """

    PACKS_CATALOG = {
        "essentiel": {
            "key": "essentiel",
            "name": "Pack Essentiel",
            "price_dh": 490,
            "billing_cycle": "mois",
            "price_display": "490 DH / mois",
            "target": "Établissements indépendants démarrant la veille e-réputation",
            "features": [
                "Jusqu'à 500 avis analysés par mois",
                "Analyse des sentiments de base (Positif / Négatif)",
                "Tableau de bord synthétique des notes",
                "Import de fichiers CSV",
                "Support technique par email sous 48h"
            ],
            "allowed_features": {
                "dashboard_view": True,
                "csv_import": True,
                "basic_sentiment": True,
                "ai_copilot": False,
                "pdf_executive_reports": False,
                "ai_auto_replies": False,
                "multi_establishment_access": False
            }
        },
        "pro": {
            "key": "pro",
            "name": "Pack Pro",
            "price_dh": 1190,
            "billing_cycle": "mois",
            "price_display": "1 190 DH / mois",
            "target": "Hôtels et riads souhaitant automatiser leur relation client et reporting",
            "is_recommended": True,
            "features": [
                "Volume d'avis illimité (Google, Booking, Airbnb, etc.)",
                "Analyse thématique avancée (Propreté, Accueil, Confort, Bruit)",
                "Copilot IA conversationnel avec preuves textuelles",
                "Générateur de rapports exécutifs PDF téléchargeables",
                "Brouillons de réponses IA en 3 langues (FR, AR, EN)",
                "Plan d'action opérationnel Kanban"
            ],
            "allowed_features": {
                "dashboard_view": True,
                "csv_import": True,
                "basic_sentiment": True,
                "ai_copilot": True,
                "pdf_executive_reports": True,
                "ai_auto_replies": True,
                "multi_establishment_access": False
            }
        },
        "multi": {
            "key": "multi",
            "name": "Pack Multi-établissements",
            "price_dh": 2490,
            "billing_cycle": "mois",
            "price_display": "2 490 DH / mois",
            "target": "Groupes hôteliers, chaînes et propriétaires de plusieurs riads",
            "features": [
                "Gestion centralisée de tous vos établissements dans un seul compte",
                "Toutes les fonctionnalités du Pack Pro incluses en illimité",
                "Tableau de bord de réputation consolidé multi-hôtels",
                "Accès multi-utilisateurs et rôles gérants",
                "Support dédié prioritaire 24/7 et accompagnement IA"
            ],
            "allowed_features": {
                "dashboard_view": True,
                "csv_import": True,
                "basic_sentiment": True,
                "ai_copilot": True,
                "pdf_executive_reports": True,
                "ai_auto_replies": True,
                "multi_establishment_access": True
            }
        }
    }

    def __init__(self):
        # Base des abonnements utilisateurs actifs
        self.user_subscriptions = {
            "user_karim_riad": {"user": "Karim Alami", "hotel": "Riad UEMF Fès", "active_pack": "pro"},
            "user_atlas_budget": {"user": "Mehdi Tazi", "hotel": "Atlas Budget Hotel", "active_pack": "essentiel"},
            "user_royal_group": {"user": "Direction Générale", "hotel": "Groupe Royal Hotels", "active_pack": "multi"}
        }

    def get_catalog_packs(self) -> Dict[str, Any]:
        """
        Critère 1 : Les packs Essentiel, Pro et Multi-établissements affichent leurs prix et fonctionnalités.
        """
        return {
            "success": True,
            "total_packs": len(self.PACKS_CATALOG),
            "packs": self.PACKS_CATALOG
        }

    def get_user_active_pack(self, user_id: str) -> Dict[str, Any]:
        """
        Critère 2 : Le pack actif est visible.
        """
        sub = self.user_subscriptions.get(user_id)
        if not sub:
            # Fallback par défaut
            return {
                "user_id": user_id,
                "active_pack_key": "essentiel",
                "pack_details": self.PACKS_CATALOG["essentiel"],
                "badge_label": "Pack Actif : Essentiel (490 DH/mois)"
            }

        pack_key = sub["active_pack"]
        pack_data = self.PACKS_CATALOG[pack_key]

        return {
            "user_id": user_id,
            "user_name": sub["user"],
            "hotel_name": sub["hotel"],
            "active_pack_key": pack_key,
            "pack_details": pack_data,
            "badge_label": f"Pack Actif : {pack_data['name']} ({pack_data['price_display']})"
        }

    def check_feature_access(self, user_id: str, feature_key: str) -> Dict[str, Any]:
        """
        Critère 3 : Les accès respectent le pack choisi.
        """
        sub_info = self.get_user_active_pack(user_id)
        pack_key = sub_info["active_pack_key"]
        pack_data = self.PACKS_CATALOG[pack_key]

        is_allowed = pack_data["allowed_features"].get(feature_key, False)

        if is_allowed:
            return {
                "access_granted": True,
                "feature": feature_key,
                "active_pack": pack_key,
                "message": f"Accès autorisé au module '{feature_key}' sous la formule '{pack_data['name']}'."
            }
        else:
            required_pack = "Pack Pro" if feature_key in ["ai_copilot", "pdf_executive_reports", "ai_auto_replies"] else "Pack Multi-établissements"
            return {
                "access_granted": False,
                "feature": feature_key,
                "active_pack": pack_key,
                "required_pack": required_pack,
                "error": f"Accès restreint : Le module '{feature_key}' n'est pas inclus dans votre '{pack_data['name']}'. Veuillez passer au {required_pack} pour débloquer cette fonctionnalité."
            }

    def switch_user_pack(self, user_id: str, new_pack_key: str) -> Dict[str, Any]:
        """Permet à l'utilisateur de changer de formule d'abonnement."""
        if new_pack_key not in self.PACKS_CATALOG:
            return {"success": False, "error": "Pack inexistant."}

        if user_id not in self.user_subscriptions:
            self.user_subscriptions[user_id] = {"user": "Gérant", "hotel": "Mon Établissement", "active_pack": new_pack_key}
        else:
            self.user_subscriptions[user_id]["active_pack"] = new_pack_key

        return {
            "success": True,
            "message": f"Formule mise à jour avec succès vers : {self.PACKS_CATALOG[new_pack_key]['name']}",
            "active_pack": self.PACKS_CATALOG[new_pack_key]
        }


if __name__ == "__main__":
    pm = SubscriptionPackManager()
    print("Module SubscriptionPackManager prêt.")
