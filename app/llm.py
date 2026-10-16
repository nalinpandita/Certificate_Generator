import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


def get_llm():
    """Returns the chat model. Switch provider/model through .env."""
    return init_chat_model(
        os.getenv("LLM_MODEL", "claude-haiku-5-5"),
        model_provider=os.getenv("LLM_PROVIDER", "anthropic"),
        temperature=0,
    )
