import re

from lib.helpers.cleanText import clean_text
from lib.helpers.normalizeDoi import normalize_doi

def normalize_org_name(name):
    if not name:
        return None
    name = re.sub(r"\s+", " ", name).strip().lower()
    return name

def parse_funder(data):
    funders = []
    funder = data.get("funder")
    if funder:
        for item in data.get("funder"):
            funder_doi = normalize_doi(item.get("DOI"))
            name = clean_text(item.get("name"))
            funder = {
                    "name": name,
                    "standard_name": normalize_org_name(name),
                    "doi": funder_doi,
                }
            f = {"funder": funder}
            awards = item.get("award")
            if isinstance(awards, list):
                award = awards[0] 
                f['publication_funder'] = {
                    "award_number": clean_text(award)
                }
            funders.append(f)
    
    if len(funders) == 0:
        return None
        
    return funders