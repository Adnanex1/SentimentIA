"""
US07 — Module de Réponses Assistées par IA
Développeuse responsable : Sarah Berrada
Branche : feature/US07-reponses-ia
Sprint Backlog : Priorité 7 | Effort : 8 | Valeur : 25
"""

import time
from typing import Dict, Any

class AIResponseAssistant:
    """
    Assiste les responsables dans la relation client :
    - Propose des brouillons personnalisés tenant compte des sentiments et thèmes de l'avis.
    - Permet au responsable de modifier ou refuser la proposition.
    - Interdit formellement toute publication sans validation humaine explicite (Human-in-the-loop).
    """

    def __init__(self):
        self.proposals = {}  # Stockage des propositions par ID

    def generate_response_proposal(self, review: Dict[str, Any], establishment_name: str = "Riad UEMF Fès") -> Dict[str, Any]:
        """
        Critère 1 : La réponse tient compte de l'avis (thèmes positifs et négatifs, ton et langue).
        """
        review_id = review.get("id", int(time.time() * 1000) % 100000)
        lang = review.get("lang", review.get("l", "FR")).upper()
        pos_aspects = review.get("pos_aspects", [])
        neg_aspects = review.get("neg_aspects", [])
        author = review.get("author", "Cher client")

        pos_str = ", ".join(pos_aspects).lower() if pos_aspects else ""
        neg_str = ", ".join(neg_aspects).lower() if neg_aspects else ""

        if lang == "AR":
            draft_text = f"مرحبا بك،\n\nنشكركم جزيلا على مشاركة تقييمكم لإقامتكم في {establishment_name}."
            if pos_str:
                draft_text += f" يسعدنا جدا أنكم استمتعتم بـ {pos_str}."
            if neg_str:
                draft_text += f" نعتذر بصدق بخصوص {neg_str}، ونؤكد لكم اتخاذ الإجراءات اللازمة فورا."
            draft_text += f"\n\nنتشرف باستقبالكم مرة أخرى.\nإدارة {establishment_name}"
        elif lang == "EN":
            draft_text = f"Dear Guest,\n\nThank you for sharing your feedback regarding your stay at {establishment_name}."
            if pos_str:
                draft_text += f" We are delighted to hear you appreciated our {pos_str}."
            if neg_str:
                draft_text += f" Regarding the issues encountered with {neg_str}, please accept our sincere apologies. Remedial actions are already underway."
            draft_text += f"\n\nWe look forward to welcoming you back soon.\nWarm regards,\nThe Management — {establishment_name}"
        else: # FR
            draft_text = f"Bonjour {author},\n\nNous vous remercions chaleureusement pour votre avis suite à votre séjour au {establishment_name}."
            if pos_str:
                draft_text += f" Nous sommes ravis que vous ayez apprécié notre {pos_str}."
            if neg_str:
                draft_text += f" Concernant les désagréments liés à {neg_str}, nous vous présentons toutes nos excuses et avons immédiatement mobilisé notre équipe pour y remédier."
            draft_text += f"\n\nAu plaisir de vous accueillir de nouveau très prochainement.\nBien cordialement,\nLa direction de {establishment_name}"

        proposal = {
            "id": review_id,
            "establishment_name": establishment_name,
            "lang": lang,
            "original_review_text": review.get("text", ""),
            "addressed_positives": pos_aspects,
            "addressed_negatives": neg_aspects,
            "draft_text": draft_text,
            "edited_text": None,
            "status": "PROPOSED",  # PROPOSED, MODIFIED, REJECTED, PUBLISHED
            "is_validated": False,
            "published_at": None
        }

        self.proposals[review_id] = proposal
        return proposal

    def modify_proposal(self, proposal_id: int, modified_text: str) -> Dict[str, Any]:
        """
        Critère 2a : Le responsable peut modifier la proposition.
        """
        if proposal_id not in self.proposals:
            return {"success": False, "error": "Proposition introuvable."}

        if not modified_text or len(modified_text.strip()) < 10:
            return {"success": False, "error": "Le texte modifié est trop court ou vide."}

        p = self.proposals[proposal_id]
        p["edited_text"] = modified_text.strip()
        p["status"] = "MODIFIED"
        return {
            "success": True,
            "message": "Proposition modifiée avec succès par le responsable.",
            "final_text": p["edited_text"]
        }

    def reject_proposal(self, proposal_id: int, reason: str = "Proposition non adaptée") -> Dict[str, Any]:
        """
        Critère 2b : Le responsable peut refuser la proposition.
        """
        if proposal_id not in self.proposals:
            return {"success": False, "error": "Proposition introuvable."}

        p = self.proposals[proposal_id]
        p["status"] = "REJECTED"
        p["is_validated"] = False
        p["rejection_reason"] = reason
        return {
            "success": True,
            "message": f"Proposition d'assistance IA refusée. Motif : {reason}",
            "status": "REJECTED"
        }

    def validate_and_publish(self, proposal_id: int, confirm_by_manager: bool = False) -> Dict[str, Any]:
        """
        Critère 3 : Aucune réponse n'est publiée sans sa validation.
        """
        if proposal_id not in self.proposals:
            return {"success": False, "error": "Proposition introuvable."}

        p = self.proposals[proposal_id]

        if p["status"] == "REJECTED":
            return {
                "success": False,
                "error": "Action impossible : Cette réponse a été expressément refusée par le responsable."
            }

        # CONTRÔLE CRITIQUE DE SÉCURITÉ HUMAINE
        if not confirm_by_manager:
            return {
                "success": False,
                "error": (
                    "Sécurité IA activée : Publication bloquée ! "
                    "Aucune réponse ne peut être publiée sans la validation expresse du responsable."
                )
            }

        # Publication autorisée
        final_content = p["edited_text"] if p["edited_text"] else p["draft_text"]
        p["is_validated"] = True
        p["status"] = "PUBLISHED"
        p["published_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "success": True,
            "message": "Réponse validée par le responsable et publiée avec succès sur la plateforme !",
            "published_text": final_content,
            "status": "PUBLISHED"
        }


if __name__ == "__main__":
    assistant = AIResponseAssistant()
    print("Module AIResponseAssistant prêt.")
