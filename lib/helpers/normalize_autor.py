from lib.db.helpers.normalize_name import normalize_for_search
from lib.helpers.clean import clean_text
from lib.helpers.full_name import build_full_name
from lib.helpers.norm_name_part import normalize_name_part


def normalize_autor(name):
    name = clean_text(name)
    if ',' in name:
        name = name.split(',')
        given_name = name[1]
        given_name = normalize_name_part(given_name)
        family_name = name[0].capitalize()
    else:
        name = name.split()
        given_name = " ".join(name[:-1])
        given_name = normalize_name_part(given_name)
        family_name = name[-1].capitalize()
        
    full_name = build_full_name(given_name, family_name)
    normalized_full_name = normalize_for_search(full_name)
    
    return {
        "given_name": given_name,
        "family_name": family_name,
        "full_name": full_name,
        "normalized_full_name": normalized_full_name,
        'canonical_source': 'lattes'
    }