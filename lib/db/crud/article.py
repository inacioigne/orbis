from lib.db.crud.authors.get_or_create import get_or_create_author
from lib.db.crud.container import get_or_create_container
from lib.db.crud.publication import get_or_create_publication
from lib.parser.author_crossref import parser_author_crossref, parser_contributor
from lib.parser.container import parser_container
from lib.parser.funders import parse_funder
from lib.parser.publication import parser_publication

from sqlalchemy.orm import Session, sessionmaker
from lib.db.database import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)
session = SessionLocal()


def injest_article(article):
    for artigo in article:
        publication = parser_publication(artigo)
        container = parser_container(artigo)
        funders = parse_funder(artigo)
        
        publication_db = get_or_create_publication(session, publication)
        container_db = get_or_create_container(session, container)
        publication_db.container = container_db
        # authors
        authors = artigo["author"]
        for author in authors:
            parsed_author, affiliation = parser_author_crossref(author)
            contributor = parser_contributor(author, parsed_author)
            author_db, created = get_or_create_author(session, parsed_author)
            # affiliation
            if affiliation and not author_db.affiliation:
                author_db = affiliation_to_author(session, author_db, affiliation)
            link = authors_to_publication(session, publication_db, author_db, contributor )
            
        # funders
        if funders:
            publication_db = ingest_publication_funders(session, publication_db, funders)
            
        # references
        references = parser_references(artigo)
        if references:
            publication_db = replace_publication_references(session, publication_db, references)
        # metrics
        metrics = extract_metrics(artigo)
        metrics_db = PublicationMetric(**metrics)
        session.add(publication_db)
        session.commit()
        
        
        print("INJET --->>>>:",artigos.index(artigo))