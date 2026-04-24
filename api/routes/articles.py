from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.schemas import ArticleOut
from lib.db.models import Publication

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
