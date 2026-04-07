def find_issn_by_type(issn_types, desired_type):
    if not isinstance(issn_types, list):
        return None
    for item in issn_types:
        if not isinstance(item, dict):
            continue
        if item.get("type") == desired_type:
            return item.get("value")
    return None