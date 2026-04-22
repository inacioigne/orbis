from typing import Any, Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from lib.db.models import Publication, PublicationReference


def resolve_cited_publication_id(
    session: Session,
    ref_data: dict[str, Any],
) -> tuple[Optional[int], Optional[str]]:
    """
    Tenta resolver a referência para uma Publication já existente no banco.
    Estratégia atual:
    - match por DOI
    Se encontrar, retorna (publication_id, 'doi')
    Se não encontrar, retorna (None, valor_original_match_source)
    """
    doi = ref_data.get("doi")
    original_match_source = ref_data.get("match_source")

    if doi:
        cited = session.scalar(
            select(Publication.id).where(Publication.doi == doi)
        )
        if cited is not None:
            return cited, "doi"

    return None, original_match_source