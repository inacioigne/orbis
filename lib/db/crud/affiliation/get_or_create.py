from sqlalchemy.orm import Session

from lib.db.models import Affiliation, Author
from sqlalchemy import select

from lib.helpers.similarity.main import check_similarity

def get_affiliation(session: Session, data: dict) -> Affiliation:
    
    affiliation = session.query(Affiliation).filter_by(
        standard_name=data['standard_name']
    ).first()

    return affiliation

def get_or_create_affiliation(session: Session, data: dict) -> Affiliation:
    
    existing = get_affiliation(session, data)
    if existing:
        return existing
    
    # --- Checa similarity ---
    candidates = session.scalars(select(Affiliation)).all()
    for candidate in candidates:
        standard_name = data['standard_name']
        res = check_similarity(standard_name, candidate.standard_name)
        verdict = res.get("verdict")
        if verdict == 'duplicate':
            return candidate
        if verdict == 'review':
            candidate.needs_review = True
            session.add(candidate)
            session.flush()
        if verdict == 'distinct':
            continue

    affiliation = Affiliation(**data)
    session.add(affiliation)
    session.flush()  

    return affiliation