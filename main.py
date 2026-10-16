"""Run:  python main.py "Issue a certificate to <name>, <date>, <time>" """
import sys
import uuid

from langgraph.types import Command

from app.graph import build_graph


def run(prompt: str) -> dict:
    graph = build_graph()
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    result = graph.invoke({"prompt": prompt, "retries": 0, "clarify_rounds": 0}, config)

    # the graph pauses at the Clarify node until the user answers
    while "__interrupt__" in result:
        question = result["__interrupt__"][0].value["message"]
        answer = input(f"\n{question}\n> ")
        result = graph.invoke(Command(resume=answer), config)
    return result


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or input("Enter your request:\n> ")
    result = run(prompt)
    if result.get("status") == "ok":
        print(f"\nCertificate created: {result['pdf_path']}")
    else:
        print(f"\nFailed: {result.get('error')}")
        sys.exit(1)
