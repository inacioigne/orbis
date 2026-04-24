# from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse


def get_artigos_completos(soup):
    
    # soup = BeautifulSoup(html, "html.parser")
    artigos_completos = soup.find("div", {"id": "artigos-completos"})
    list_artigos = artigos_completos.find_all("div", class_="artigo-completo")
    
    return list_artigos

def get_autores(raw_artigo):
    autores = []
    for tag in raw_artigo.find_all(["a", "b"]):
        name = tag.get_text(strip=True)
        if "," in name and any(c.isupper() for c in name):
            d_a = {'name': name}
            href = tag.attrs.get('href')
            if href:
                id_lattes = href.split('/')[-1]
                d_a['id_lattes'] = id_lattes
            autores.append(d_a)
    return autores

def slipt_artigos(list_artigos):
    
    c_doi = []
    s_doi = []
    for artigo in list_artigos:
        citacao = artigo.find("span", class_="citacoes")
        parsed = urlparse(citacao['cvuri'])
        params = parse_qs(parsed.query, keep_blank_values=True)
        [doi] = params['doi'] 
        if doi == '':
            params['autores'] = get_autores(artigo)
            params['date_published'] = artigo.find("span", {"data-tipo-ordenacao": "ano"}).get_text(strip=True)
            # params['raw_artigo'] = artigo
            s_doi.append(params)
        else:
            c_doi.append(params)
            
    return c_doi, s_doi