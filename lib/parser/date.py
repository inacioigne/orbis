from datetime import date


def parse_date(obj):
    if not obj:
        return None
    parts = obj.get("date-parts") if isinstance(obj, dict) else None
    if not parts or not parts[0]:
        return None
    p = parts[0]
    year = p[0]
    month = p[1] if len(p) > 1 else 1
    day = p[2] if len(p) > 2 else 1
    return date(year, month, day)