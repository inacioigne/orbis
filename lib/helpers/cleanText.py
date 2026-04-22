from typing import Optional
from html import unescape
import re


def clean_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    value = str(value).strip()
    value = unescape(value)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    value = re.sub(r"\(\s+", "(", value)
    value = re.sub(r"\s+\)", ")", value)

    return value or None