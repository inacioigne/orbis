from lib.db.helpers.normalize_name import normalize_for_search
from lib.helpers.clean import clean_text
from lib.helpers.full_name import build_full_name
from lib.helpers.norm_name_part import normalize_name_part
from lib.helpers.orcid import extract_orcid_id
from lib.parser.crossref.affiliation import get_affiliation


def parser_author_crossref(author: dict):
    given_name = normalize_name_part(author.get("given", ""))
    family_name = clean_text(author.get("family", ""))
    full_name = build_full_name(given_name, family_name)
    normalized_full_name = normalize_for_search(full_name)
    orcid = extract_orcid_id(author.get("ORCID", ""))
    affiliation = None
    
    parsed_author = {
        "given_name": given_name,
        "family_name": family_name,
        "full_name": full_name,
        "normalized_full_name": normalized_full_name,
        "orcid": orcid,
        'canonical_source': 'crossref'
    }
    
    affiliations = author['affiliation']
    if len(affiliations) > 0:
        first_aff = affiliations[0]
        name = clean_text(first_aff.get('name'))
        standard_name = normalize_for_search(name)
        affiliation = {
            "name": name,
            "standard_name": standard_name
            }
        # print(affiliation)
        # parsed_author['affiliation'] = affiliation
        
    return parsed_author, affiliation

def parser_contributor(author, parsed_author):
    contributor = {
                "role": "author",
                "position": author.get("sequence"),
                "raw_name": parsed_author.get("full_name"),
                "raw_affiliation": get_affiliation(author),
            }

    return contributor