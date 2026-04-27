from collections.abc import Iterable
from typing import Any

from sqlalchemy.orm import Session
from lib.db.crud.authors.get import get_author
from lib.db.models import Author, Publication, PublicationContributor

from lib.db.models import Publication

def authors_to_publication(
    session: Session,
    publication: Publication,
    author: Author,
    contributor: dict):
    
    link = PublicationContributor(
            publication=publication,
            author=author,
            role=contributor.get("role"),
            # position=contributor.get("position"),
            raw_name=author.full_name,
            raw_affiliation=contributor.get("raw_affiliation"),
        )
    session.add(link)
    session.flush()
    return link