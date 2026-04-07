from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from lib.db.models import Author

def _find_existing_author(session: Session, author_data: dict[str, Any]) -> Author | None:
    """
    Procura autor existente por:
    1. ORCID
    2. Lattes ID
    3. Nome completo
    """
    orcid = author_data.get("orcid")
    lattes_id = author_data.get("lattes_id")
    full_name = author_data.get("name")

    if orcid:
        author = session.scalar(
            select(Author).where(Author.orcid == orcid)
        )
        if author:
            return author

    if lattes_id:
        author = session.scalar(
            select(Author).where(Author.lattes_id == lattes_id)
        )
        if author:
            return author

    if full_name:
        author = session.scalar(
            select(Author).where(Author.full_name == full_name)
        )
        if author:
            return author

    return None