from collections.abc import Iterable
from typing import Any

from sqlalchemy.orm import Session
# from lib.db.crud.affiliation import get_or_create_affiliation
from lib.db.crud.affiliation.get_or_create import get_or_create_affiliation
from lib.db.crud.authors.get import get_author
from lib.db.models import Author, Publication, PublicationContributor

from lib.db.models import Publication
    
def affiliation_to_author(
    session: Session, 
    author_db: Author, 
    affiliation: dict):
    
    affiliation_db = get_or_create_affiliation(session, affiliation)
    
    author_db.affiliation = affiliation_db
    session.flush()
    session.commit()
    return author_db