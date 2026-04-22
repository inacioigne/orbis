import re

from lib.db.models import Author
from lib.helpers.clean import clean_text

def is_abbreviated(given: str) -> bool:
    """Verifica se o given name é só iniciais (ex: 'A. L.', 'W.')."""
    given = clean_text(given)
    # Remove pontos e espaços, sobra só letras — se todas têm 1 char, é abreviação
    parts = re.split(r"[\s.]+", given)
    parts = [p for p in parts if p]
    return all(len(p) == 1 for p in parts) if parts else False

def _maybe_upgrade_name(author_db: Author, author_json: dict) -> bool:
    """Atualiza o registro se o novo dado tem given name mais completo."""
    given = author_json.get("given", "")
    # family = author_json.get("family", "")
    full_name = author_json.get("full_name", "")
    if not author_db.given_name:
        author_db.given_name = given
        author_db.full_name = full_name
        return True
    if given and not is_abbreviated(given) and is_abbreviated(author_db.given_name):
        author_db.given_name = given
        author_db.full_name = full_name
        author_db.needs_review = False  # resolvido
        return True
    return False