import uuid
from datetime import datetime

from app.config import CONFIG
from app.state import CertState


def template_node(state: CertState) -> dict:
    """Builds the exact values that will be printed on the certificate."""
    date = datetime.strptime(state["issue_date"], "%Y-%m-%d").strftime(CONFIG["date_format"])
    time = datetime.strptime(state["issue_time"], "%H:%M").strftime(CONFIG["time_format"])
    cert_id = state.get("certificate_id") or (
        f"CERT-{state['issue_date'][:4]}-{uuid.uuid4().hex[:6].upper()}"
    )
    return {
        "certificate_id": cert_id,
        "display": {
            "candidate_name": state["name"],
            "issue_date": date,
            "issue_time": time,
            "certificate_id": cert_id,
            **CONFIG["fixed_fields"],
        },
    }
