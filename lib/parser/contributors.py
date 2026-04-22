from lib.helpers.cleanText import clean_text
from lib.parser.affiliation import get_affiliation
from lib.parser.orcid import normalize_orcid

def join_name(given, family):
    return " ".join([p for p in [given, family] if p]) or None


def parser_contributor(data):
    contributors = []
    for item in data.get("author"):
        given = clean_text(item.get("given"))
        family = clean_text(item.get("family"))
        full_name = join_name(given, family)
        orcid = normalize_orcid(item.get("ORCID"))
        c = { "author": {
                "full_name": full_name,
                "given_name": given,
                "family_name": family,
                "orcid": orcid,
                "lattes_id": None,
                "is_inpa_researcher": None,
            },
            "contributor": {
                "role": "author",
                "position": item.get("sequence"),
                "raw_name": full_name,
                "raw_affiliation": get_affiliation(item),
            }}
        contributors.append(c)

    return contributors