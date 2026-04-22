from datetime import datetime

from sqlalchemy.orm import Session

from lib.db.models import Author, Lattes
from sqlalchemy import select

def update_lattes(session: Session, lattes: dict, author_db: Author) -> Lattes:
    
    lattes_db = session.get(Lattes, author_db.lattes_profile.id)
    lattes_db.lattes_update = datetime.strptime(lattes['lattes_update'], "%Y-%m-%d")
    lattes_db.html = lattes['html']
    session.flush()
    session.refresh(lattes_db)
    # return lattes_db
    
def get_or_create_lattes(
    session: Session, 
    lattes: dict, 
    author_db: Author,) -> Lattes:
    
    lattes_id = lattes['lattes_id']
    lattes_update = datetime.strptime(lattes['lattes_update'], "%Y-%m-%d") 
  
    existing = session.execute(
        select(Lattes).where(Lattes.lattes_id == lattes_id)
    ).scalar_one_or_none()
    if existing:
        
        if existing.lattes_update == lattes_update:
            print(f"Encontrado Lattes com o mesmo Lattes ID: {lattes_id}.")
            return existing
        
    print(f"Criando novo Lattes com Lattes ID: {lattes_id}.")
    lattes_db = Lattes(**lattes)
    lattes_db.author_id = author_db.id
    session.add(lattes_db)
    session.flush() 
    return author_db

