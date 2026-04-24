from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from lib.db.models import Publication, PublicationContainer
from lib.helpers.normalizeText import normalize_text
from lib.helpers.similarity.main import check_similarity

def get_or_create_publication(session: Session, publication: dict) -> Publication:
    
    doi = publication.get("doi")
    if doi:
        publi_doi = session.query(Publication).filter_by(doi=doi).first()
        if publi_doi:
            print(f"DOI já existe: {doi}")
            return publi_doi
        
    title = publication["title"]
    publi_title = session.query(Publication).filter_by(title=title).first()
    
    if publi_title:
        print(f"Titulo já existe: {doi} - {title}")
        return publi_title
    
    # --- 2. Checa similarity ---
    candidates = session.scalars(select(Publication)).all()
    for candidate in candidates:
        res = check_similarity(candidate.title, title)
        verdict = res.get("verdict")
        if verdict == 'duplicate':
            print("DUP: ", candidate.title)
            return candidate
        if verdict == 'review':
            candidate.needs_review = True
            session.add(candidate)
            session.flush()
        if verdict == 'distinct':
            continue
    
    print(f"Publicação nova: {doi} - {title}")
    publication_db = Publication(**publication)
    session.add(publication_db)
    session.flush()  
    session.commit()

    return publication_db

def upsert_publication(
    session: Session,
    publication_data: dict,
    container: Optional[PublicationContainer] = None,
) -> Publication:


    if not publication_data:
        raise ValueError("publication_data não pode ser vazio")

    title = publication_data.get("title")
    doi = publication_data.get("doi")
    identifier = publication_data.get("identifier")
    publication_type = publication_data.get("publication_type")
    date_published = publication_data.get("date_published")
    

    if not title and not doi and not identifier:
        raise ValueError(
            "publication_data precisa ter ao menos 'title', 'doi' ou 'identifier'"
        )

    # # 1. match por DOI
    if doi:
        existing = session.scalar(
            select(Publication).where(Publication.doi == doi)
        )
        if existing:
            publication_data = dict(publication_data)
            publication_data["doi"] = doi
            # _update_publication_if_needed(
            #     existing,
            #     publication_data=publication_data,
            #     container=container,
            # )
            session.flush()
            return existing

    # # 2. match por identifier
    if identifier:
        existing = session.scalar(
            select(Publication).where(Publication.identifier == identifier)
        )
        if existing:
            publication_data = dict(publication_data)
            publication_data["doi"] = doi
            # _update_publication_if_needed(
            #     existing,
            #     publication_data=publication_data,
            #     container=container,
            # )
            session.flush()
            return existing

    # 3. fallback por name + publication_type + date_published
    if title:
        normalized_title = normalize_text(title)

        candidates = session.scalars(
            select(Publication).where(Publication.title.is_not(None))
        ).all()

        for candidate in candidates:
            if normalize_text(candidate.title) != normalized_title:
                continue

            if publication_type and candidate.publication_type:
                if candidate.publication_type != publication_type:
                    continue

            if date_published and candidate.date_published:
                if not (candidate.date_published == date_published):
                    continue

            publication_data = dict(publication_data)
            publication_data["doi"] = doi
            # _update_publication_if_needed(
            #     candidate,
            #     publication_data=publication_data,
            #     container=container,
            # )
            session.flush()
            return candidate

    # se não encontrou, cria
    print("Criando publicação:", title)
    publication = Publication(**publication_data)

    if container is not None:
        publication.container = container

    session.add(publication)
    session.flush()
    session.commit()
    
    return publication