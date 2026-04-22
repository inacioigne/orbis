from lib.helpers.clean import clean_text


def normalize_name_part(name: str) -> str:
    """Limpa e coloca em title case consistente."""
    name = clean_text(name)
    # Title case respeitando partículas comuns em nomes brasileiros/ibéricos
    return name.title()