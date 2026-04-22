from lib.db.crud.authors.create import create_author
from lib.db.crud.authors.helpers import _maybe_upgrade_name
from lib.db.crud.authors.orcid import _maybe_set_orcid

from sqlalchemy import select
from sqlalchemy.orm import Session

from lib.db.models import Author
from lib.helpers.similarity.main import check_similarity


def get_or_create_author(session: Session, author: dict):
  
    orcid = author.get("orcid")
    normalized_full_name = author['normalized_full_name']
    
    # --- 1. Verifica ORCID ---
    if orcid:
      author_db = session.scalar(select(Author).where(Author.orcid == orcid))
      if author_db:
        upgraded = _maybe_upgrade_name(author_db, author)
        return author_db, False
    
    # --- 2. Checa similarity ---
    candidates = session.scalars(select(Author)).all()
    for candidate in candidates:
      res = check_similarity(normalized_full_name, candidate.normalized_full_name)
      verdict = res.get("verdict")
      if verdict == 'duplicate':
        if orcid:
          _maybe_set_orcid(candidate, orcid)
        return candidate, False
      if verdict == 'review':
          candidate.needs_review = True
          session.add(candidate)
          session.flush()
      if verdict == 'distinct':
          continue
    # --- 3. Create a new author ---
    author_db = create_author(session, author)
    session.commit()
      
    return author_db, True