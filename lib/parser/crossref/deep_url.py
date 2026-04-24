def deep_get_url(data):
    resource = data.get("resource")
    if not isinstance(resource, dict):
        return None
    primary = resource.get("primary")
    if not isinstance(primary, dict):
        return None
    return primary.get("URL")