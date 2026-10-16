import re
import unicodedata
from datetime import datetime

from app.state import CertState


def _clean_name(name: str | None) -> str | None:
    if not name:
        return None
    name = re.sub(r"\s+", " ", name).strip()
    ok = all(
        unicodedata.category(c)[0] in ("L", "M") or c in " .'-"
        for c in name
    )
    return name if ok and 2 <= len(name) <= 80 else None


def _valid(value: str | None, fmt: str) -> str | None:
    if not value:
        return None
    try:
        datetime.strptime(value, fmt)
        return value
    except ValueError:
        return None


def validate_node(state: CertState) -> dict:
    name = _clean_name(state.get("name"))
    date = _valid(state.get("issue_date"), "%Y-%m-%d")
    time = _valid(state.get("issue_time"), "%H:%M")

    labels = {"name": name, "issue date": date, "issue time": time}
    missing = [label for label, value in labels.items() if not value]

    message = None
    if missing:
        message = f"I couldn't determine the following: {', '.join(missing)}."
        if state.get("ambiguity_note"):
            message += f" Note: {state['ambiguity_note'].rstrip('. ')}."
        message += " Please provide them."

    return {
        "name": name,
        "issue_date": date,
        "issue_time": time,
        "missing_fields": missing,
        "clarify_message": message,
    }
