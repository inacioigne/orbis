import re


def extract_orcid_id(orcid_raw: str) -> str | None:
    """Extrai só o ID do ORCID (ex: '0000-0001-9509-1678') de uma URL ou string."""
    if not orcid_raw:
        return None
    match = re.search(r"(\d{4}-\d{4}-\d{4}-\d{3}[\dX])", orcid_raw)
    return match.group(1) if match else None