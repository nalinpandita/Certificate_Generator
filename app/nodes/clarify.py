from langgraph.types import interrupt

from app.state import CertState


def clarify_node(state: CertState) -> dict:
    """Pauses the graph and asks the user. The answer comes back via Command(resume=...)."""
    answer = interrupt({"message": state["clarify_message"], "missing": state["missing_fields"]})
    return {
        "prompt": f"{state['prompt']}\nAdditional info: {answer}",
        "clarify_rounds": state.get("clarify_rounds", 0) + 1,
    }
