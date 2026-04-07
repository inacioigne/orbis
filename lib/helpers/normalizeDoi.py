from typing import Optional

from lib.helpers.cleanText import clean_text


def normalize_doi(value: Optional[str]) -> Optional[str]:
    value = clean_text(value)
    if not value:
        return None

    value = value.replace("https://doi.org/", "")
    value = value.replace("http://doi.org/", "")
    value = value.replace("doi:", "")
    value = value.strip().lower()
    return value or None