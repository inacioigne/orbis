from lib.helpers.findIssnByType import find_issn_by_type
from lib.helpers.firstStr import first_str


def parser_container(data):
    container = {
        "name": first_str(data.get("container-title")),
        "alternate_name": first_str(data.get("short-container-title")),
        "publisher": data.get("publisher"),
        "issn_print": find_issn_by_type(data.get("issn-type"), "print"),
        "issn_electronic": find_issn_by_type(data.get("issn-type"), "electronic"),
        "isbn": first_str(data.get("ISBN"))
        }
    return container