def build_full_name(given: str, family: str) -> str:
    return f"{given} {family}".strip() if given else family.strip()