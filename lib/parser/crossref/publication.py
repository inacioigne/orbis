from lib.helpers.abstract import normalize_abstract
from lib.helpers.cleanText import clean_text
from lib.helpers.firstStr import first_str
from lib.helpers.normalizeDoi import normalize_doi
from lib.parser.crossref.conditions_of_access import build_conditions_of_access, infer_free_access
from lib.parser.crossref.date import parse_date
from lib.parser.crossref.deep_url import deep_get_url
from lib.parser.crossref.license import first_license_url
from lib.parser.crossref.page import parse_page_range
from lib.parser.crossref.subject import parse_subject


def parser_publication(data):
    
    title = clean_text(first_str(data.get("title")))
    
    publication = {
        "publication_type": data.get("type"),
        "title": title,
        "subtitle": first_str(data.get("subtitle")),
        "alternative_title": first_str(data.get("short-title")) or first_str(data.get("original-title")),
        "abstract": normalize_abstract(data.get("abstract")),
        "date_published": parse_date(
                data.get("published")
                or data.get("published-print")
                or data.get("issued")
            ),
        "language": data.get("language"),
        "subject": parse_subject(data.get("subject")),
        "doi": normalize_doi(data.get("DOI")),
        "isbn": first_str(data.get("ISBN")),
        "identifier": first_str(data.get("alternative-id")),
        "publisher": data.get("publisher"),
        "url": (deep_get_url(data)
                or data.get("URL")
            ),
        "license": first_license_url(data.get("license")),
        "conditions_of_access": build_conditions_of_access(data),
        "is_accessible_for_free": infer_free_access(data),
        "page_start": parse_page_range(data.get("page"))[0],
        "page_end": parse_page_range(data.get("page"))[1],
        "volume_number": data.get("volume"),
        "issue_number": data.get("issue"),
        "edition": data.get("edition-number") or data.get("special_numbering"),
        "source": "crossref",
        "raw_json": data,
    }
    return publication