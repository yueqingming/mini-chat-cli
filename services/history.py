"""对话历史：裁剪 messages（如 trim_messages）、保留 system + 最近 N 轮。"""



MAX_TURNS = 5  # 保留最近 5 轮问答（10 条 user/assistant）
def trim_messages(messages: list) -> None:
    if len(messages) <= 1:
        return
    system = messages[0]
    rest = messages[1:]
    # 每轮 2 条：user + assistant
    max_msgs = MAX_TURNS * 2
    if len(rest) > max_msgs:
        rest = rest[-max_msgs:]
    messages[:] = [system, *rest]