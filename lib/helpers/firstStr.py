import html


def first_str(value):
    v = None
    if isinstance(value, list):
        v = value[0].strip() if value else None
    if isinstance(value, str):
        v = value.strip()
    if v:
        v = html.unescape(v)
        return v
    return None