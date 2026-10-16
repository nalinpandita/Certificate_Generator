from typing import TypedDict


class CertState(TypedDict, total=False):
    # input
    prompt: str
    # parsed from the prompt (Parse node)
    name: str | None
    issue_date: str | None          # YYYY-MM-DD
    issue_time: str | None          # HH:MM (24h)
    ambiguity_note: str | None
    # validation / clarification
    missing_fields: list[str]
    clarify_message: str | None
    clarify_rounds: int
    # template + render
    certificate_id: str
    display: dict                   # values exactly as printed on the certificate
    pdf_path: str | None
    # verification
    verified: bool
    retries: int
    # result
    status: str                     # "ok" | "error"
    error: str | None
