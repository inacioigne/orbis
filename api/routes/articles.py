from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.schemas import ArticleOut
from lib.db.models import Author, Publication, PublicationContributor

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=list[ArticleOut])
def list_articles(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Publication]:
    return (
        db.query(Publication)
        .order_by(Publication.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/author/{author_id}", response_model=list[ArticleOut])
def list_articles_by_author(
    author_id: int = Path(..., ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Publication]:
    author = db.get(Author, author_id)
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    return (
        db.query(Publication)
        .join(
            PublicationContributor,
            PublicationContributor.publication_id == Publication.id,
        )
        .filter(PublicationContributor.author_id == author_id)
        .distinct()
        .order_by(Publication.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
