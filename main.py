from openai import APIError, AuthenticationError, RateLimitError

from config import MISSING_API_KEY_MESSAGE, get_client, get_model

from lim import chat_stream,chat_once


def main():
    client = get_client()
    if client is None:
        print(MISSING_API_KEY_MESSAGE)
        return
    model = get_model()

    # 在循环外创建，整段对话共用同一个列表
    messages = [
        {"role": "system", "content": "你是一个简洁的助手。"},
    ]

    print("多轮对话已启动，输入 exit 或 quit 退出\n")

    while True:
        user_text = input("你: ").strip()
        if not user_text:
            print("输入不能为空")
            continue  # 继续下一轮，不要 return 结束整个程序
        if user_text.lower() in ("exit", "quit"):
            print("再见")
            break

        messages.append({"role": "user", "content": user_text})

        try:
            stream = chat_stream(client, model, messages)

        except AuthenticationError:
            print("认证失败：请检查 .env 中的 DEEPSEEK_API_KEY 是否正确")
            break
        except RateLimitError:
            print("请求过于频繁或被限流，请稍后再试")
            continue
        except APIError as e:
            print(f"API 调用失败：{e}")
            continue
        except Exception as e:
            print(f"未知错误：{e}")
            continue

        reply_parts = []
        print("助手：", end="", flush=True)

        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                print(delta, end="", flush=True)
                reply_parts.append(delta)

        print()
        reply = "".join(reply_parts)
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
