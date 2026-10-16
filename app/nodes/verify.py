import re
from pypdf import PdfReader

from app.state import CertState


def _norm(text: str) -> str:
    return re.sub(r"\s+", "", text).lower()


def verify_node(state: CertState) -> dict:
    """Re-reads the PDF and checks the requested values really appear in it."""
    reader = PdfReader(state["pdf_path"])
    text = _norm(" ".join(page.extract_text() or "" for page in reader.pages))

    d = state["display"]
    checks = ["candidate_name", "issue_date", "issue_time", "certificate_id", "course_name", "instructor_name"]
    ok = len(reader.pages) == 1 and all(_norm(d[k]) in text for k in checks)

    if ok:
        return {"verified": True}
    return {"verified": False, "retries": state.get("retries", 0) + 1}
