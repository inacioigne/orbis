from lib.db.crud.lattes.get import get_lattes_by_id
from lib.parser.lattes.update import get_update_lattes
from lib.scrap_lattes.baixar import baixar_lattes
from lib.scrap_lattes.driver import make_driver


def check_cv_update(session, lattes_id):
    
    lattes = get_lattes_by_id(session, lattes_id)
    if lattes is None:
        print("CV não encontrado")
        return None, None
    lattes_update_db = lattes.lattes_update
    
    # Baixa Lattes
    driver = make_driver(headless=True)
    html = baixar_lattes(driver, lattes_id)
    lattes_update = get_update_lattes(html)
    if lattes_update > lattes_update_db.date():
        return html, True
    else:
        return html, False