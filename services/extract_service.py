"""结构化信息抽取：调模型 → 解析 JSON。"""

import json
import re

from openai import APIError, AuthenticationError, RateLimitError

from config import get_client, get_model
from llm import chat_once
from services.errors import MissingApiKeyError

SYSTEM_PROMPT = """你是一个信息抽取助手。用户会给你一段自然语言。
你必须只输出一个 JSON 对象，不要 markdown、不要解释、不要其它文字。

字段：
- name: 人名，没有则为 null
- city: 城市，没有则为 null
- sentiment: 只能是 "positive"、"negative"、"neutral" 之一
- summary: 一句话概括（中文，不超过 30 字）
"""




def parse_json_from_reply(text: str) -> dict:
    """从模型回复中解析 JSON（兼容被 ```json ... ``` 包裹的情况）。"""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
    return json.loads(text)


def extract(text: str) -> dict:
    """对用户文本做结构化抽取，返回解析后的字典。"""
    client = get_client()
    if client is None:
        raise MissingApiKeyError()

    model = get_model()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ]

    try:
        response = chat_once(client, model, messages)
    except AuthenticationError:
        raise
    except RateLimitError:
        raise
    except APIError:
        raise

    raw = response.choices[0].message.content or ""
    return parse_json_from_reply(raw)
