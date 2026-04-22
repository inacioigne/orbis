from lib.db.models import Author
from sqlalchemy.orm import Session


def create_author(session: Session, author: dict ) -> Author:
    
    author_db = Author(**author)
    session.add(author_db)
    session.flush()
    
    return author_db