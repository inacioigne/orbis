import re
import unicodedata


def clean_text(text: str) -> str:
    """Remove espaços não-quebráveis, espaços duplos e faz strip."""
    if not text:
        return ""
    # Normaliza unicode: \xa0, \u00a0 → espaço comum
    text = unicodedata.normalize("NFKC", text)
    # Remove espaços múltiplos
    text = re.sub(r"\s+", " ", text).strip()
    return text