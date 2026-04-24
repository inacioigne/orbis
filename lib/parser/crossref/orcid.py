def normalize_orcid(value):
    if not value:
        return None
    value = str(value).strip()
    value = value.replace("https://orcid.org/", "").replace("http://orcid.org/", "")
    return value or None