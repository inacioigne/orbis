from lib.db.make_session import local_session
from sqlalchemy.orm import Session
from sqlalchemy import select
from lib.db.models import Lattes

def get_lattes_by_id(session: Session, lattes_id: str):
    
    lattes = session.execute(
        select(Lattes).where(Lattes.lattes_id == lattes_id)
    ).scalar_one_or_none()
    
    return lattes