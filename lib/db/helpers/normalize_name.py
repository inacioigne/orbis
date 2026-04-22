import re
import unicodedata


def normalize_for_search(name: str) -> str:
    """Remove acentos e lowercaseiza para índice de busca."""
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_name = "".join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", ascii_name).strip().lower()