from datetime import datetime


def parser_publi_sem_doi(article):
    
    raw_artigo = article.get('raw_artigo')
    [title] = article.get('titulo')
    # date_published = raw_artigo.find("span", {"data-tipo-ordenacao": "ano"}).get_text(strip=True)
    year = article.get('date_published')
    data = datetime.strptime(year, "%Y").date()
    [volume] = article.get('volume')
    # [issue] = article.get('issue')
    d_p = {
        'publication_type': 'journal-article',
        'title': title,
        'date_published': data,
        'volume_number': volume
    }
    
    return d_p