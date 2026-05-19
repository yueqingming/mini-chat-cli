"""聊天业务：组装 messages、调用 llm、返回助手回复（供 CLI 与 API 共用）。"""

from openai import APIError, AuthenticationError, RateLimitError

from config import get_client, get_model
from llm import chat_stream
from services.errors import MissingApiKeyError
from services.history import trim_messages

CHAT_SYSTEM_PROMPT = "你是一个简洁的助手。"


def chat(messages: list[dict]) -> dict:
    """根据 messages 调用模型，返回本轮回复与更新后的完整对话列表。"""
    client = get_client()
    if client is None:
        raise MissingApiKeyError()
    model = get_model()

    messages = list(messages)
    if not messages or messages[0].get("role") != "system":
        messages.insert(0, {"role": "system", "content": CHAT_SYSTEM_PROMPT})

    try:
        stream = chat_stream(client, model, messages)
    except AuthenticationError:
        raise
    except RateLimitError:
        raise
    except APIError:
        raise

    reply_parts = []
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            reply_parts.append(delta)

    reply = "".join(reply_parts)
    messages.append({"role": "assistant", "content": reply})
    trim_messages(messages)
    return {"reply": reply, "messages": messages}
