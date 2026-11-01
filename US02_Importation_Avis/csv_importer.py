"""
US02 — Module d'Importation des Avis & Ingestion CSV
Développeur responsable : Youssef El Amrani
Branche : feature/US02-importation-avis
Sprint Backlog : Priorité 2 | Effort : 5 | Valeur : 30
"""

import csv
import io
import re
import hashlib
from typing import List, Dict, Any, Tuple

class ReviewCSVImporter:
    """
    Gère l'importation de fichiers d'avis clients (CSV, TSV),
    détecte et signale les lignes incorrectes ou incomplètes,
    et assure la déduplication stricte pour éviter les doublons.
    """

    def __init__(self):
        # Base de données d'avis existants (stockés avec leur empreinte unique)
        self.existing_review_hashes = set()
        self.stored_reviews = []

    def _normalize_text(self, text: str) -> str:
        """Normalise le texte pour détecter les doublons même avec de légères variations d'espacement."""
        if not text:
            return ""
        return re.sub(r"\s+", " ", text.strip().lower())

    def _compute_hash(self, text: str) -> str:
        return hashlib.md5(self._normalize_text(text).encode("utf-8")).hexdigest()

    def preload_existing_reviews(self, reviews: List[Dict[str, Any]]):
        """Précharge des avis déjà présents dans la base de données."""
        for r in reviews:
            txt = r.get("text", "") or r.get("t", "")
            if txt:
                h = self._compute_hash(txt)
                self.existing_review_hashes.add(h)
                self.stored_reviews.append(r)

    def import_csv_content(self, csv_string_or_filepath: str, source_label: str = "Import CSV") -> Dict[str, Any]:
        """
        Importe les avis depuis un fichier ou une chaîne CSV.
        Critère 1 : Le fichier CSV est importé.
        Critère 2 : Les lignes incorrectes sont signalées avec la raison.
        Critère 3 : Les avis déjà présents ne sont pas ajoutés une deuxième fois.
        """
        # Détermination si c'est un chemin de fichier ou du contenu texte
        content = ""
        try:
            with open(csv_string_or_filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, FileNotFoundError):
            content = csv_string_or_filepath

        if not content.strip():
            return {
                "success": False,
                "error": "Le fichier CSV est vide.",
                "imported_count": 0,
                "errors": [],
                "duplicates": []
            }

        # Détection du délimiteur (, ou ;)
        sample_line = content.splitlines()[0] if content.splitlines() else ""
        delimiter = ";" if ";" in sample_line and "," not in sample_line else ","

        reader = csv.reader(io.StringIO(content), delimiter=delimiter)
        
        imported_reviews = []
        incorrect_lines = []
        duplicate_lines = []

        headers = None
        for line_num, row in enumerate(reader, start=1):
            if not row or all(cell.strip() == "" for cell in row):
                continue  # Ligne vide ignorée

            # Extraction ou détection de l'en-tête
            if headers is None:
                headers = [h.strip().lower() for h in row]
                # Vérifier si l'en-tête contient des colonnes d'avis
                if any(col in headers for col in ["text", "review", "avis", "comment", "commentaire"]):
                    continue
                else:
                    # Pas d'en-tête explicite, on traite comme la première ligne de données
                    headers = ["text", "date", "rating"]

            # Mapping des colonnes
            row_dict = {}
            for i, val in enumerate(row):
                key = headers[i] if i < len(headers) else f"col_{i}"
                row_dict[key] = val.strip()

            review_text = (
                row_dict.get("text") or 
                row_dict.get("review") or 
                row_dict.get("avis") or 
                row_dict.get("comment") or 
                row_dict.get("commentaire") or 
                (row[0].strip() if len(row) > 0 else "")
            )

            date_str = row_dict.get("date") or "Récemment"
            rating = row_dict.get("rating") or row_dict.get("note") or "N/A"

            # -------------------------------------------------------------
            # CRITÈRE 2 : Détection des lignes incorrectes
            # -------------------------------------------------------------
            if not review_text or len(review_text) < 5:
                incorrect_lines.append({
                    "line": line_num,
                    "row_raw": row,
                    "reason": "Texte d'avis manquant ou trop court (< 5 caractères)"
                })
                continue

            if review_text.lower() in ["null", "none", "n/a", "undefined"]:
                incorrect_lines.append({
                    "line": line_num,
                    "row_raw": row,
                    "reason": "Contenu invalide (valeur NULL ou N/A)"
                })
                continue

            # -------------------------------------------------------------
            # CRITÈRE 3 : Détection des doublons (déjà présents)
            # -------------------------------------------------------------
            review_hash = self._compute_hash(review_text)
            if review_hash in self.existing_review_hashes:
                duplicate_lines.append({
                    "line": line_num,
                    "text": review_text[:50] + "...",
                    "reason": "Avis identique déjà présent dans la base de données"
                })
                continue

            # Ajout aux avis valides importés
            self.existing_review_hashes.add(review_hash)
            review_item = {
                "id": len(self.stored_reviews) + len(imported_reviews) + 1,
                "text": review_text,
                "date": date_str,
                "rating": rating,
                "source": source_label,
                "hash": review_hash
            }
            imported_reviews.append(review_item)

        self.stored_reviews.extend(imported_reviews)

        return {
            "success": True,
            "total_lines_processed": line_num,
            "imported_count": len(imported_reviews),
            "incorrect_count": len(incorrect_lines),
            "duplicate_count": len(duplicate_lines),
            "imported_reviews": imported_reviews,
            "incorrect_lines": incorrect_lines,
            "duplicates": duplicate_lines
        }


if __name__ == "__main__":
    importer = ReviewCSVImporter()
    print("Module ReviewCSVImporter prêt.")
