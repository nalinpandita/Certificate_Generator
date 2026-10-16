import re
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.config import BASE_DIR, CONFIG
from app.state import CertState


def _safe(name: str) -> str:
    return re.sub(r"[^\w\-]+", "_", name, flags=re.UNICODE).strip("_")


def render_node(state: CertState) -> dict:
    try:
        from weasyprint import HTML
    except OSError as e:  # missing GTK/Pango libraries (common on Windows)
        raise RuntimeError(
            "WeasyPrint system libraries are missing. See README (Windows notes)."
        ) from e

    tpl_path = BASE_DIR / CONFIG["template"]["path"]
    env = Environment(
        loader=FileSystemLoader(tpl_path.parent),
        autoescape=select_autoescape(["html"]),
    )
    html = env.get_template(tpl_path.name).render(**state["display"])

    out_dir = BASE_DIR / CONFIG["output_dir"]
    out_dir.mkdir(exist_ok=True)
    pdf = out_dir / f"certificate_{_safe(state['display']['candidate_name'])}_{state['certificate_id']}.pdf"
    HTML(string=html, base_url=str(tpl_path.parent)).write_pdf(pdf)
    return {"pdf_path": str(pdf)}
