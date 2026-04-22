from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from lib.db.models import Publication
from lib.db.models import Funder
from lib.db.models import PublicationFunder


def ingest_publication_funders(
    session: Session,
    publication_db: Publication,
    funders: List[Dict[str, Any]]
) -> dict:
    
    createds = []
    
    for item in funders:
        funder_info = item.get("funder", {}) or {}
        rel_info = item.get("publication_funder", {}) or {}
        name = (funder_info.get("name") or "").strip()
        standard_name = (funder_info.get("standard_name") or "").strip()
        doi = (funder_info.get("doi") or "").strip()
        award_number = (rel_info.get("award_number") or "").strip() or None
        
        if not name:
            continue
        
        # 1. Procurar funder existente
        funder: Optional[Funder] = None
        if doi:
            funder = session.query(Funder).filter(Funder.doi == doi).first()
        if not funder and standard_name:
            funder = session.query(Funder).filter(
                    Funder.standard_name == standard_name
                ).first()
            
        # 2. Criar funder se não existir
        if not funder:
            funder = Funder(
                name=name,
                standard_name=standard_name or None,
                doi=doi or None
            )
            session.add(funder)
            session.flush() 
            createds.append(funder)
        else:
            if not funder.doi and doi:
                funder.doi = doi
        
        # 3. Evitar duplicidade no relacionamento
        existing_link = session.query(PublicationFunder).filter(
            PublicationFunder.publication_id == publication_db.id,
            PublicationFunder.funder_id == funder.id,
            PublicationFunder.award_number == award_number
        ).first()
        if existing_link:
            continue
        
        link = PublicationFunder(
            publication_id=publication_db.id,
            funder_id=funder.id,
            award_number=award_number
        )
        session.add(link)
        session.flush() 
    session.commit()
            
    return publication_db