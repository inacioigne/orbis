from typing import Any

from lib.db.models import Author


def _update_author_fields(author: Author, payload: dict[str, Any]) -> None:
    """
    Atualiza o Author sem apagar valores existentes com None.
    """
    full_name = payload.get("full_name")
    given_name = payload.get("given_name")
    family_name = payload.get("family_name")
    orcid = payload.get("orcid")
    lattes_id = payload.get("lattes_id")
    is_inpa_researcher = payload.get("is_inpa_researcher")

    if full_name:
        author.full_name = full_name

    if given_name:
        author.given_name = given_name

    if family_name:
        author.family_name = family_name

    if orcid:
        author.orcid = orcid

    if lattes_id:
        author.lattes_id = lattes_id

    if is_inpa_researcher is not None:
        author.is_inpa_researcher = is_inpa_researcher