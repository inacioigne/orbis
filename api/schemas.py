from datetime import date

from pydantic import BaseModel


class ArticleOut(BaseModel):
    id: int
    title: str
    doi: str | None = None
    publication_type: str | None = None
    date_published: date | None = None

    class Config:
        from_attributes = True


class ArticleCountOut(BaseModel):
    total: int
