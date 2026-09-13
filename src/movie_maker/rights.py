"""Fail-closed checks for source material before adaptation work begins."""

from .models import SourceMaterial

ALLOWED_RIGHTS_STATUSES = {"public_domain", "licensed", "user_owned"}
KNOWN_RIGHTS_STATUSES = ALLOWED_RIGHTS_STATUSES | {"unknown", "blocked"}


class RightsError(ValueError):
    """Raised when source material is not eligible for generation."""


def validate_source(source: SourceMaterial) -> list[str]:
    """Return actionable validation errors without making a legal conclusion."""

    errors: list[str] = []
    if not source.title.strip():
        errors.append("source title is required")
    if not source.author.strip():
        errors.append("source author is required")
    if not source.text.strip():
        errors.append("source text is required")
    if source.rights_status not in KNOWN_RIGHTS_STATUSES:
        errors.append(f"unknown rights status: {source.rights_status!r}")
    elif source.rights_status not in ALLOWED_RIGHTS_STATUSES:
        errors.append(
            f"rights status {source.rights_status!r} is not eligible; "
            "use public_domain, licensed, or user_owned"
        )
    if source.rights_status == "licensed" and not source.rights_notes.strip():
        errors.append("licensed source material requires rights_notes for auditability")
    return errors


def assert_source_is_producible(source: SourceMaterial) -> None:
    errors = validate_source(source)
    if errors:
        raise RightsError("Source material failed the rights/intake gate: " + "; ".join(errors))
