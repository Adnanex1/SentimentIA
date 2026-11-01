"""
US04 — Module d'Analyse par Thème & Extraction d'Extraits
Développeur responsable : Mehdi Chraibi
Branche : feature/US04-analyse-par-theme
Sprint Backlog : Priorité 4 | Effort : 13 | Valeur : 40
"""

import re
from typing import Dict, List, Any

class ThemeAspectExtractor:
    """
    Extrait les thèmes hôteliers clés (notamment Propreté, Accueil, Confort),
    détermine la polarité spécifique à chaque thème au sein d'un même avis,
    et isole les extraits de texte justificatifs.
    """

    # Définition des règles thématiques avec focus obligatoire sur Propreté, Accueil et Confort
    THEME_DEFINITIONS = {
        "proprete": {
            "label": "Propreté",
            "regex": r"propr[eé]|sale\b|salet[eé]|nettoy|tache|poussi[eè]re|odeur|drap|serviette|clean|dirty|spotless|hygi[eè]n|dust|stain|نظيف|متسخ",
            "pos_indicators": [r"\bpropre\b", r"impeccable", r"\bclean\b", r"spotless", r"irréprochable", r"bien nettoy[eé]", r"نظيف"],
            "neg_indicators": [r"\bsale\b", r"\bdirty\b", r"tache", r"odeur", r"poussi[eè]re", r"insalubre", r"n[eé]glig[eé]", r"douteu[xs]", r"laissait [aà] d[eé]sirer", r"متسخ"]
        },
        "accueil": {
            "label": "Accueil & Personnel",
            "regex": r"accueil|personnel|r[eé]ception|h[oô]te|staff|service|souri|aimable|attente|check[\s-]?in|receptionist|friendly|helpful|استقبال|موظف",
            "pos_indicators": [r"chaleureux", r"souriant", r"aimable", r"aux petits soins", r"remarquable", r"friendly", r"helpful", r"rapide", r"gentil", r"محترم"],
            "neg_indicators": [r"froid", r"d[eé]sagr[eé]able", r"attente", r"lent", r"rude", r"incomp[eé]tent", r"mauvais accueil", r"بطيء"]
        },
        "confort": {
            "label": "Confort & Chambre",
            "regex": r"confort|chambre|lit|literie|matelas|oreiller|espace|clim|room|bed|mattress|pillow|spacious|cozy|comfort|suite|غرفة|مريح",
            "pos_indicators": [r"confortable", r"spacieu[xse]", r"douillet", r"plush", r"cosy", r"agr[eé]able", r"bien [eé]quip[eé]", r"مريح"],
            "neg_indicators": [r"inconfortable", r"\bdur\b", r"[eé]troit", r"petit", r"v[eé]tuste", r"climatisation bruyante", r"matelas d[eé]fonc[eé]", r"غير مريح"]
        },
        "bruit": {
            "label": "Bruit & Isolation",
            "regex": r"bruit|bruyant|calme|isolation|rue|soundproof|noise|noisy|loud|quiet|هدوء|ضجيج",
            "pos_indicators": [r"calme", r"silencieu[xse]", r"paisible", r"quiet", r"soundproof", r"bien isol[eé]", r"هدوء"],
            "neg_indicators": [r"bruyant", r"tapage", r"cloisons fines", r"noisy", r"loud", r"bruit de rue", r"ضجيج"]
        },
        "restauration": {
            "label": "Restauration / Petit-déjeuner",
            "regex": r"petit[\s-]?d[eé]j|buffet|d[eé]jeuner|caf[eé]|repas|restaurant|croissant|breakfast|فطور",
            "pos_indicators": [r"d[eé]licieu[xse]", r"copieu[xse]", r"frais", r"vari[eé]", r"excellent", r"tasty", r"fresh"],
            "neg_indicators": [r"froid", r"fade", r"m[eé]diocre", r"sans saveur", r"limit[eé]", r"poor"]
        }
    }

    def _split_into_sentences(self, text: str) -> List[str]:
        """Découpe un avis en phrases pour isoler précisément les extraits."""
        sentences = re.split(r"(?<=[.!?;\n])\s+", text.strip())
        return [s.strip() for s in sentences if len(s.strip()) > 3]

    def extract_themes(self, text: str) -> Dict[str, Any]:
        """
        Critère 1 : La propreté, l'accueil et le confort sont identifiés.
        Critère 2 : Un avis peut avoir plusieurs thèmes avec des sentiments différents.
        Critère 3 : Les extraits correspondants sont affichés.
        """
        if not text:
            return {"themes_detected": [], "theme_details": {}}

        sentences = self._split_into_sentences(text)
        detected_themes = []
        theme_details = {}

        for theme_key, cfg in self.THEME_DEFINITIONS.items():
            pattern = cfg["regex"]
            if re.search(pattern, text, flags=re.IGNORECASE):
                detected_themes.append(theme_key)

                matching_snippets = []
                for s in sentences:
                    if re.search(pattern, s, flags=re.IGNORECASE):
                        matching_snippets.append(s)

                if not matching_snippets:
                    matching_snippets = [text]

                combined_snippet_text = " ".join(matching_snippets).lower()
                
                pos_score = sum(1 for p in cfg["pos_indicators"] if re.search(p, combined_snippet_text, flags=re.IGNORECASE))
                neg_score = sum(1 for n in cfg["neg_indicators"] if re.search(n, combined_snippet_text, flags=re.IGNORECASE))

                if pos_score > neg_score:
                    theme_sentiment = "Positif"
                    polarity = +1
                elif neg_score > pos_score:
                    theme_sentiment = "Négatif"
                    polarity = -1
                else:
                    is_neg_fallback = any(re.search(w, combined_snippet_text, flags=re.IGNORECASE) for w in [r"pas\b", r"non\b", r"manque", r"mauvais", r"n[eé]glig", r"tache", r"douteu", r"odeur"])
                    theme_sentiment = "Négatif" if is_neg_fallback else "Positif"
                    polarity = -1 if is_neg_fallback else +1

                theme_details[theme_key] = {
                    "label": cfg["label"],
                    "sentiment": theme_sentiment,
                    "polarity": polarity,
                    "excerpts": matching_snippets
                }

        return {
            "text": text,
            "themes_count": len(detected_themes),
            "themes_detected": detected_themes,
            "theme_details": theme_details
        }


if __name__ == "__main__":
    extractor = ThemeAspectExtractor()
    print("Module ThemeAspectExtractor prêt.")
