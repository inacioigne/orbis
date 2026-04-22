from sqlalchemy.orm import Session
from sqlalchemy import select

from lib.db.helpers.update_container import _update_container_if_needed
from lib.db.models import PublicationContainer
from lib.helpers.normalizeText import normalize_text


def get_or_create_container(session: Session, container_data: dict,) -> PublicationContainer:
    """
    Procura um PublicationContainer existente e, se não encontrar,
    cria um novo.
    """

    if not container_data:
        raise ValueError("container_data não pode ser vazio")
    
    name = container_data.get('name')
    alternate_name = container_data.get('alternate_name')
    issn_print = container_data.get('issn_print')
    issn_electronic = container_data.get('issn_electronic')
    isbn = container_data.get('isbn')
    publisher = container_data.get('publisher')
    url = container_data.get('url')


    if not name and not any([issn_print, issn_electronic, isbn]):
        raise ValueError(
            "container_data precisa ter ao menos 'name' ou algum identificador (ISSN/ISBN)"
        )
    # 1. match por ISSN print
    if issn_print:
        existing = session.scalar(
            select(PublicationContainer).where(
                PublicationContainer.issn_print == issn_print
            )
        )
        if existing:
            print(f"Encontrado container com o mesmo ISSN print: {issn_print}.")
            _update_container_if_needed(
                    existing,
                    name=name,
                    alternate_name=alternate_name,
                    publisher=publisher,
                    issn_print=issn_print,
                    issn_electronic=issn_electronic,
                    isbn=isbn,
                    url=url,
                )
            return existing
    # 2. match por ISSN eletrônico
    if issn_electronic:
        existing = session.scalar(
            select(PublicationContainer).where(
                PublicationContainer.issn_electronic == issn_electronic
            )
        )
        if existing:
            # _update_container_if_needed(
            #     existing,
            #     name=name,
            #     alternate_name=alternate_name,
            #     publisher=publisher,
            #     issn_print=issn_print,
            #     issn_electronic=issn_electronic,
            #     issn_l=issn_l,
            #     isbn=isbn,
            #     url=url,
            # )
            return existing
    # 3. match por ISBN
    if isbn:
        existing = session.scalar(
            select(PublicationContainer).where(
                PublicationContainer.isbn == isbn
            )
        )
        if existing:
            # _update_container_if_needed(
            #     existing,
            #     name=name,
            #     alternate_name=alternate_name,
            #     publisher=publisher,
            #     issn_print=issn_print,
            #     issn_electronic=issn_electronic,
            #     issn_l=issn_l,
            #     isbn=isbn,
            #     url=url,
            # )
            return existing
    # 4. fallback por name + publisher
    normalized_name = normalize_text(name)
    normalized_publisher = normalize_text(publisher)

    if normalized_name:
        candidates = session.scalars(
            select(PublicationContainer).where(
                PublicationContainer.name.is_not(None)
            )
        ).all()

        for candidate in candidates:
            if normalize_text(candidate.name) != normalized_name:
                continue

            cand_pub = normalize_text(candidate.publisher)
            if normalized_publisher and cand_pub and cand_pub != normalized_publisher:
                continue

            # _update_container_if_needed(
            #     candidate,
            #     name=name,
            #     alternate_name=alternate_name,
            #     publisher=publisher,
            #     issn_print=issn_print,
            #     issn_electronic=issn_electronic,
            #     issn_l=issn_l,
            #     isbn=isbn,
            #     url=url,
            # )
            return candidate
    # se não encontrou, cria
    # print("Criando novo container:", name, issn_print, issn_electronic, isbn)
    container = PublicationContainer(**container_data)
    session.add(container)
    session.flush()
    session.commit()
    return container