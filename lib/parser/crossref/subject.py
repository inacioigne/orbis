def parse_subject(obj):
    if isinstance(obj, list):
        if len(obj) == 0:
            return None
        return ", ".join(s.strip() for s in obj if s.strip())
    if isinstance(obj, str):
        v = obj.strip()
        return v or None
    return None