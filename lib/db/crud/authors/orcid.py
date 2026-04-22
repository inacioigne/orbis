from lib.db.models import Author


def _maybe_set_orcid(author: Author, orcid: str | None) -> None:
    """Associa ORCID se o autor ainda não tem."""
    if orcid and not author.orcid:
        author.orcid = orcid
        