from sqlalchemy.orm import Session

from lib.db.models import Affiliation

def get_affiliation(session: Session, data: dict) -> Affiliation:
    
    affiliation = session.query(Affiliation).filter_by(
        standard_name=data['standard_name']
    ).first()

    return affiliation