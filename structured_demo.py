"""结构化输出示例：让模型只返回 JSON，再由 Python 解析并执行业务逻辑。"""

import json
import re

from openai import APIError, AuthenticationError, RateLimitError

from config import MISSING_API_KEY_MESSAGE, get_client, get_model

from lim import chat_stream,chat_once

SYSTEM_PROMPT = """你是一个信息抽取助手。用户会给你一段自然语言。
你必须只输出一个 JSON 对象，不要 markdown、不要解释、不要其它文字。

字段：
- name: 人名，没有则为 null
- city: 城市，没有则为 null
- sentiment: 只能是 "positive"、"negative"、"neutral" 之一
- summary: 一句话概括（中文，不超过 30 字）
"""

DEFAULT_TEXT = "我叫小明，住在杭州，你们家快递太慢了，我很生气。"


def extract_json(text: str) -> dict:
    """从模型回复中解析 JSON（兼容被 ```json ... ``` 包裹的情况）。"""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
    return json.loads(text)


def run_business_logic(data: dict) -> None:
    """根据解析后的字段做程序判断（聊天字符串很难可靠地做这件事）。"""
    sentiment = data.get("sentiment")
    if sentiment == "negative":
        print("\n[业务] 负面情绪 → 可触发：转人工 / 发补偿券")
    elif sentiment == "positive":
        print("\n[业务] 正面情绪 → 可触发：感谢问卷 / 推荐商品")
    else:
        print("\n[业务] 中性 → 常规跟进即可")

    if data.get("city"):
        print(f"[业务] 记录城市：{data['city']}（例如按地区分配客服）")


def main():
    client = get_client()
    if client is None:
        print(MISSING_API_KEY_MESSAGE)
        return
    model = get_model()

    print("结构化抽取 demo（直接回车使用默认例句）\n")
    user_text = input("输入一段话: ").strip() or DEFAULT_TEXT
    print(f"\n待分析: {user_text}\n")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_text},
    ]

    try:
        response = chat_once(client, model, messages)
    except AuthenticationError:
        print("认证失败：请检查 .env 中的 DEEPSEEK_API_KEY")
        return
    except RateLimitError:
        print("请求过于频繁或被限流，请稍后再试")
        return
    except APIError as e:
        print(f"API 调用失败：{e}")
        return

    raw = response.choices[0].message.content or ""
    print("模型原始返回:")
    print(raw)
    print()

    try:
        data = extract_json(raw)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败：{e}")
        print("（实际项目里可：重试一次、换更强模型、或开启 API 的 JSON mode）")
        return

    print("解析后的 dict（程序可直接用）:")
    for key, value in data.items():
        print(f"  {key}: {value!r}")

    print(f"\n类型检查: sentiment 是 {data.get('sentiment')!r}")
    run_business_logic(data)


if __name__ == "__main__":
    main()
