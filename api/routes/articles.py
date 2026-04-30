from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy import distinct, func
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.schemas import ArticleCountOut, ArticleOut
from lib.db.models import Author, Publication, PublicationContainer, PublicationContributor

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


@router.get("/count", response_model=ArticleCountOut)
def count_articles(
    author_id: int | None = Query(default=None, ge=1),
    author: str | None = Query(default=None, min_length=1),
    year: int | None = Query(default=None, ge=1, le=9999),
    journal: str | None = Query(default=None, min_length=1),
    db: Session = Depends(get_db),
) -> dict[str, int]:
    query = db.query(func.count(distinct(Publication.id)))

    if author_id is not None or author is not None:
        query = query.join(
            PublicationContributor,
            PublicationContributor.publication_id == Publication.id,
        )

    if author is not None:
        query = query.join(Author, Author.id == PublicationContributor.author_id)

    if journal is not None:
        query = query.join(
            PublicationContainer,
            PublicationContainer.id == Publication.is_part_of_id,
        )

    if author_id is not None:
        query = query.filter(PublicationContributor.author_id == author_id)

    if author is not None:
        author_filter = f"%{author}%"
        query = query.filter(
            Author.full_name.ilike(author_filter)
            | Author.normalized_full_name.ilike(author_filter)
        )

    if year is not None:
        query = query.filter(
            Publication.date_published >= date(year, 1, 1),
            Publication.date_published <= date(year, 12, 31),
        )

    if journal is not None:
        journal_filter = f"%{journal}%"
        query = query.filter(
            PublicationContainer.name.ilike(journal_filter)
            | PublicationContainer.alternate_name.ilike(journal_filter)
        )

    return {"total": query.scalar() or 0}


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
