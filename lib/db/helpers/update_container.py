from typing import Optional

from lib.db.models import PublicationContainer


def _update_container_if_needed(
    container: PublicationContainer,
    *,
    name: Optional[str],
    alternate_name: Optional[str],
    publisher: Optional[str],
    issn_print: Optional[str],
    issn_electronic: Optional[str],
    isbn: Optional[str],
    url: Optional[str],
) -> None:
    """
    Preenche campos faltantes sem sobrescrever informação já existente.
    """

    if not container.name and name:
        container.name = name

    if not container.alternate_name and alternate_name:
        container.alternate_name = alternate_name

    if not container.publisher and publisher:
        container.publisher = publisher

    if not container.issn_print and issn_print:
        container.issn_print = issn_print

    if not container.issn_electronic and issn_electronic:
        container.issn_electronic = issn_electronic

    if not container.isbn and isbn:
        container.isbn = isbn

    if not container.url and url:
        container.url = url