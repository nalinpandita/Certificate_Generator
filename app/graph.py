from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.config import CONFIG
from app.nodes.clarify import clarify_node
from app.nodes.deliver import deliver_node
from app.nodes.parse import parse_node
from app.nodes.render import render_node
from app.nodes.template import template_node
from app.nodes.validate import validate_node
from app.nodes.verify import verify_node
from app.state import CertState


def fail(message: str):
    def node(state: CertState) -> dict:
        return {"status": "error", "error": message}
    return node


def after_validate(state: CertState) -> str:
    if not state["missing_fields"]:
        return "template"
    if state.get("clarify_rounds", 0) >= CONFIG["max_clarify_rounds"]:
        return "fail_input"
    return "clarify"


def after_verify(state: CertState) -> str:
    if state["verified"]:
        return "deliver"
    if state.get("retries", 0) <= CONFIG["max_render_retries"]:
        return "render"
    return "fail_render"


def build_graph():
    g = StateGraph(CertState)
    g.add_node("parse", parse_node)
    g.add_node("validate", validate_node)
    g.add_node("clarify", clarify_node)
    g.add_node("template", template_node)
    g.add_node("render", render_node)
    g.add_node("verify", verify_node)
    g.add_node("deliver", deliver_node)
    g.add_node("fail_input", fail("Could not get all required details from the user."))
    g.add_node("fail_render", fail("PDF verification kept failing after retries."))

    g.add_edge(START, "parse")
    g.add_edge("parse", "validate")
    g.add_conditional_edges("validate", after_validate, ["template", "clarify", "fail_input"])
    g.add_edge("clarify", "parse")
    g.add_edge("template", "render")
    g.add_edge("render", "verify")
    g.add_conditional_edges("verify", after_verify, ["deliver", "render", "fail_render"])
    g.add_edge("deliver", END)
    g.add_edge("fail_input", END)
    g.add_edge("fail_render", END)

    # a checkpointer is required for interrupt() to work
    return g.compile(checkpointer=MemorySaver())
