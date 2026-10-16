import json
from datetime import datetime, timezone

from app.config import BASE_DIR, CONFIG
from app.state import CertState


def deliver_node(state: CertState) -> dict:
    """Writes an audit log entry and marks the run as done."""
    log = BASE_DIR / CONFIG["output_dir"] / "audit_log.jsonl"
    entry = {
        "time_utc": datetime.now(timezone.utc).isoformat(),
        "certificate_id": state["certificate_id"],
        "name": state["name"],
        "issue_date": state["issue_date"],
        "issue_time": state["issue_time"],
        "pdf": state["pdf_path"],
        "prompt": state["prompt"],
    }
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return {"status": "ok"}
