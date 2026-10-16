from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field

from app.config import CONFIG
from app.llm import get_llm
from app.state import CertState


class CertRequest(BaseModel):
    name: str | None = Field(None, description="Candidate's full name exactly as written")
    issue_date: str | None = Field(None, description="YYYY-MM-DD, or null if missing/ambiguous")
    issue_time: str | None = Field(None, description="HH:MM in 24-hour format, or null if missing/ambiguous")
    ambiguity_note: str | None = Field(None, description="Short note if anything was ambiguous")


SYSTEM = """You extract certificate details from a user's request.
Today is {today} ({weekday}). Timezone: {tz}.

Rules:
- name: the candidate's full name exactly as written. Do not invent or correct it.
- issue_date: output YYYY-MM-DD. Resolve words like "today" or "tomorrow" using today's date.
- issue_time: output 24-hour HH:MM (e.g. "3 pm" -> "15:00").
- If a value is missing, or ambiguous (e.g. "03/04/2026" could be 3 April or 4 March), return null
  for it and explain briefly in ambiguity_note. Never guess.
- Later lines in the request that start with "Additional info:" are the user's answers to
  earlier questions. They override earlier values."""


def get_parser():
    return get_llm().with_structured_output(CertRequest)


def parse_node(state: CertState) -> dict:
    now = datetime.now(ZoneInfo(CONFIG["timezone"]))
    system = SYSTEM.format(
        today=now.strftime("%Y-%m-%d"),
        weekday=now.strftime("%A"),
        tz=CONFIG["timezone"],
    )
    result: CertRequest = get_parser().invoke(
        [("system", system), ("human", state["prompt"])]
    )
    return {
        "name": result.name,
        "issue_date": result.issue_date,
        "issue_time": result.issue_time,
        "ambiguity_note": result.ambiguity_note,
    }
