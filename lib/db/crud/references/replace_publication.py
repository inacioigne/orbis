from typing import Any

from lib.db.crud.references.resolve_cited import resolve_cited_publication_id
from lib.db.models import Publication, PublicationReference

from sqlalchemy.orm import Session

def replace_publication_references(
    session: Session,
    publication: Publication,
    references_data: list[dict[str, Any]],
) -> Publication:
    """
    Remove as referências atuais da publicação e recria a lista com base
    no JSON normalizado.

    Isso combina com:
    - UniqueConstraint(citing_publication_id, position)
    - relationship(... cascade='all, delete-orphan')
    """
    publication.outgoing_references.clear()
    session.flush()

    for index, ref_data in enumerate(references_data, start=1):
        cited_publication_id, match_source = resolve_cited_publication_id(
            session, ref_data
        )
        print("REF:", cited_publication_id, match_source)

        ref = PublicationReference(
            citing_publication=publication,
            cited_publication_id=cited_publication_id,
            position=index,
            doi=ref_data.get("doi"),
            title=ref_data.get("title"),
            author=ref_data.get("author"),
            journal_title=ref_data.get("journal_title"),
            year=ref_data.get("year"),
            volume=ref_data.get("volume"),
            issue=ref_data.get("issue"),
            match_source=match_source,
        )

        publication.outgoing_references.append(ref)
    session.flush()
    session.commit()
    return publication