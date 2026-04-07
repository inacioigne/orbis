def first_license_url(licenses):
    if not licenses:
        return None
    if isinstance(licenses, list):
        for item in licenses:
            if isinstance(item, dict) and item.get("URL"):
                return item["URL"].strip()
    return None