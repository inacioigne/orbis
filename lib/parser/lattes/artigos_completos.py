# from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse


def get_artigos_completos(soup):
    
    # soup = BeautifulSoup(html, "html.parser")
    artigos_completos = soup.find("div", {"id": "artigos-completos"})
    list_artigos = artigos_completos.find_all("div", class_="artigo-completo")
    
    return list_artigos


def slipt_artigos(list_artigos):
    
    c_doi = []
    s_doi = []
    for artigo in list_artigos:
        citacao = artigo.find("span", class_="citacoes")
        parsed = urlparse(citacao['cvuri'])
        params = parse_qs(parsed.query, keep_blank_values=True)
        [doi] = params['doi'] 
        if doi == '':
            params['raw_artigo'] = artigo
            s_doi.append(params)
        else:
            c_doi.append(params)
            
    return c_doi, s_doi