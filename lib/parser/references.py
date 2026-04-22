from lib.helpers.cleanText import clean_text
from lib.helpers.normalizeDoi import normalize_doi


def parser_references(data):
    references = []
    for item in data.get("reference", []):
        title = clean_text(item.get("article-title"))
        if not title:
            continue
        
        r = {
            "doi": normalize_doi(item.get("DOI")),
            "title": title,
            "author": clean_text(item.get("author")),
            "journal_title": clean_text(item.get("journal-title")),
            "year": item.get("year"),
            "volume": clean_text(item.get("volume")),
            "issue": clean_text(item.get("issue")),
            "match_source": None,
            }
        references.append(r)
    if len(references) == 0:
        return None
    return references