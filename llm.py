from openai import OpenAI

def chat_stream(client, model, messages):
    return client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )

def chat_once(client, model, messages):
    return client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
    )
