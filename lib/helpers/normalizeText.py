import re
from typing import Optional

from lib.helpers.cleanText import clean_text


def normalize_text(value: Optional[str]) -> Optional[str]:
    value = clean_text(value)
    if not value:
        return None
    value = re.sub(r"\s+", " ", value)
    return value.strip().lower()