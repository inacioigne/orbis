from datetime import datetime
import re
import json
from os import makedirs

from bs4 import BeautifulSoup

from lib.helpers.normalizeText import normalize_text


def get_profile(soup: BeautifulSoup, lattes_id: str) -> dict:
    
    profile = {'is_inpa_researcher': True}
    infpessoa = soup.find('div', class_='infpessoa')
    full_name = infpessoa.find('h2').text.strip()
    given_name = full_name.split()[0]
    family_name = " ".join(full_name.split()[1:]) if len(full_name.split()) > 1 else None
    profile["full_name"] = full_name
    profile["given_name"] = given_name
    profile["family_name"] = family_name
    profile['normalized_full_name'] = normalize_text(full_name)
    profile["lattes_id"] = lattes_id
    # Extract ORCID
    orcid_label = soup.find("b", string=lambda s: s and "orcid" in s.lower())
    if orcid_label:
        parent = orcid_label.find_parent().find_parent()
        sibling = parent.find_next_sibling("div")
        if sibling:
            orcid = sibling.find_all('a')[1].text.strip()
            orcid = orcid.replace("https://orcid.org/", "")
            profile["orcid"] = orcid
            
    cv = { "author": profile}

    return cv

def get_lattes_update(soup, cv):
    
    lattes = { 'lattes_id': cv['author']['lattes_id']}    
    infoautor = soup.find("ul", class_="informacoes-autor")
    infoupdate = infoautor.find_all("li")[-1].text
    match = re.search(r"(\d{2}/\d{2}/\d{4})", infoupdate)
    if match:
        lattes['lattes_update'] = datetime.strptime(match.group(1), "%d/%m/%Y").date()
    cv['lattes'] = lattes
    
    return cv

def save_profile(soup, lattes_id):
    
    profile = get_profile(soup, lattes_id)
    profile = get_lattes_update(soup, profile)
    profile['affiliation'] = {
        'name': 'Instituto Nacional de Pesquisas da Amazônia',
        'standard_name': 'instituto nacional de pesquisas da amazônia',
        'acronym': 'INPA',
        'state': 'Amazonas',
        'city': 'Manaus'
    }
    
    path_root = f'data/curriculos/{lattes_id}'    
    makedirs(path_root, exist_ok=True)
    
    with open(f'{path_root}/profile.json', 'w', encoding='utf-8') as f:
        json.dump(profile, f, indent=4, ensure_ascii=False, default=str)
        f.close()
        
    