from collections.abc import Iterable
from typing import Any

from sqlalchemy.orm import Session
from lib.db.crud.authors.get import get_author
from lib.db.models import Author, Publication, PublicationContributor

from lib.db.models import Publication

def authors_to_publication(
    session: Session,
    publication: Publication,
    author: Author,
    contributor: dict):
    
    link = PublicationContributor(
            publication=publication,
            author=author,
            role=contributor.get("role"),
            position=contributor.get("position"),
            raw_name=author.full_name,
            raw_affiliation=contributor.get("raw_affiliation"),
        )
    session.add(link)
    session.flush()
    return link

# def authors_to_publication(
#     session: Session,
#     publication: Publication,
#     contributors_data: Iterable[dict[str, Any]],
# ) -> list[PublicationContributor]:

#     created_links: list[PublicationContributor] = []

#     for item in contributors_data:
        
#         author_data = item.get("author")
#         full_name = author_data.get('full_name')
#         contributor_data = item.get("contributor")

#         author = get_author(session, author)
#         if author is None:
#             print("Criando novo autor:", full_name )
#             author = Author(**author_data)
#             session.add(author)
#             session.flush()
#             # session.commit()
#         else:
#             print(f'Author encontrado: {full_name}')
#             # _update_author_fields(author, author_data)
#             # session.flush()
#             # session.commit()

#         link = PublicationContributor(
#             publication=publication,
#             author=author,
#             role=contributor_data.get("role"),
#             position=contributor_data.get("position"),
#             raw_name=contributor_data.get("raw_name") or full_name,
#             raw_affiliation=contributor_data.get("raw_affiliation"),
#         )

#         session.add(link)
#         created_links.append(link)

#     session.flush()
#     session.commit()
#     return created_links

