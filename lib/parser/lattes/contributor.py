from lib.db.helpers.normalize_name import normalize_for_search
from lib.helpers.full_name import build_full_name
from lib.helpers.norm_name_part import normalize_name_part


def parser_contributor_lattes(author):
    name = author.get('name').split(', ')
    id_lattes = author.get('id_lattes')
    given_name = name[1]
    given_name = normalize_name_part(given_name)
    family_name = name[0].capitalize()
    full_name = build_full_name(given_name, family_name)
    normalized_full_name = normalize_for_search(full_name)
    
    return {
        "given_name": given_name,
        "family_name": family_name,
        "full_name": full_name,
        "normalized_full_name": normalized_full_name,
        "lattes_id": id_lattes,
        'canonical_source': 'lattes'
    }