from sqlalchemy.orm import Session, sessionmaker

from lib.db.database import engine

def local_session() -> Session:
    
    SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
    )
    session = SessionLocal()
    
    return session