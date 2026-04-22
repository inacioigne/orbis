import re
import html


def normalize_abstract(texto: str|None) -> str:
    """
    Normaliza string XML/HTML (ex: JATS) para salvar no banco.

    - remove aspas externas extras
    - converte escapes (\n, \t)
    - remove tags XML/HTML
    - decodifica entidades HTML
    - normaliza aspas especiais
    - remove espaços duplicados
    """

    if not texto:
        return None

    # Remove aspas externas
    texto = texto.strip().strip("'").strip('"')

    # Converte caracteres escapados
    texto = (
        texto.replace("\\n", " ")
             .replace("\\t", " ")
             .replace('\\"', '"')
             .replace("\\'", "'")
    )

    # Remove tags XML/HTML
    texto = re.sub(r"<[^>]+>", " ", texto)

    # Decodifica entidades HTML
    texto = html.unescape(texto)

    # Normaliza aspas especiais
    texto = (
        texto.replace("‘", "'")
             .replace("’", "'")
             .replace("“", '"')
             .replace("”", '"')
    )

    # Remove espaços duplicados
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto