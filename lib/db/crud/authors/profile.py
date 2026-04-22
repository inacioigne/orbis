from datetime import datetime
import json

from lib.db.crud.authors.create import create_author
from lib.db.crud.authors.get import get_author
from lib.db.crud.authors.vinculate_affiliation import affiliation_to_author
from lib.db.crud.lattes import get_or_create_lattes, update_lattes
from lib.db.crud.lattes import update_lattes
from lib.db.helpers.normalize_name import normalize_for_search

from sqlalchemy.orm import Session
from pathlib import Path


def get_or_create_profile(session: Session, id_lattes: str):
    path_root = Path('data/curriculos')
    path_cv = Path(path_root / id_lattes)
    path_html = Path(path_cv / "curriculo.html")
    path_json = Path(path_cv / "profile.json")
    
    if not path_html.exists() or not path_json.exists():
        raise FileNotFoundError(f"O arquivo {path_cv} não foi encontrado.") 
    
    with open(path_html, "r", encoding="utf-8") as f:
        html_content = f.read()

    with open(path_json, "r", encoding="utf-8") as f:
        json_content = json.load(f)
        
    author = json_content['author']
    lattes = json_content['lattes']
    lattes['html'] = html_content
    affiliation = json_content['affiliation']
    
    author_db = get_author(session, author)
    if author_db:
        print(f"Author {author_db.full_name} already exists in the database.")
        # return author_db
    else:
        author_db = create_author(session, author)
    lattes_update = datetime.strptime(lattes['lattes_update'], "%Y-%m-%d")
    cv_lattes = author_db.lattes_profile
    if cv_lattes:
        if cv_lattes.lattes_update < lattes_update:
            # Atualiza lattes
            update_lattes(session, lattes, author_db)
            print(f"Encontrado Lattes com o mesmo Lattes ID: {lattes['lattes_id']}.")
            return author_db
    else:
        author_db = get_or_create_lattes(session, lattes, author_db)
        
    affiliation_db = author_db.affiliation
    if affiliation_db:
        if affiliation_db.name != affiliation['name']:
            author_db = affiliation_to_author(session, author_db, affiliation)
    else:
        print(f"Vinculando afiliação {affiliation['name']} ao autor {author_db.full_name}.")
        author_db = affiliation_to_author(session, author_db, affiliation)

    return author_db