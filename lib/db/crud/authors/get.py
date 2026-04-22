from sqlalchemy.orm import Session

from lib.db.models import Author
from sqlalchemy import select

def get_author(session: Session, author: dict ) -> Author:
    lattes_id = author.get("lattes_id")
    orcid = author.get("orcid")
    normalized_full_name = author['normalized_full_name']
    
    existing = None

    if lattes_id:
        existing = session.execute(
            select(Author).where(Author.lattes_id == lattes_id)
        ).scalar_one_or_none()
        # if existing:
        #     # print(f"Encontrado autor com o mesmo Lattes ID: {lattes_id}.")
        #     return existing
    if orcid:
        existing = session.execute(
            select(Author).where(Author.orcid == orcid)
        ).scalar_one_or_none()
        
    existing = session.execute(
            select(Author).where(Author.normalized_full_name == normalized_full_name)
        ).scalar_one_or_none()

    return existing