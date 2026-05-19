# mini-chat-cli
<<<<<<< HEAD

基于 DeepSeek API 的迷你对话项目：支持终端多轮聊天、结构化 JSON 抽取，以及 FastAPI HTTP 接口。

## 功能

- **CLI 多轮对话**（`main.py`）：流式输出，自动裁剪最近 5 轮历史
- **结构化抽取**（`structured_demo.py`）：从自然语言抽取 JSON 字段
- **HTTP API**（FastAPI）：
  - `GET /health` — 健康检查
  - `POST /api/extract` — 信息抽取
  - `POST /api/chat` — 多轮对话（返回 `reply` 与完整 `messages`）

## 项目结构

```text
mini-chat-cli/
  config.py              # 读取 .env，创建 OpenAI 客户端
  llm.py                 # chat_stream / chat_once
  main.py                # 终端多轮聊天
  structured_demo.py     # 结构化抽取 CLI
  services/
    chat_service.py      # 聊天业务
    extract_service.py   # 抽取业务
    history.py           # trim_messages（限制上下文长度）
    errors.py            # MissingApiKeyError 等
  api/
    app.py               # FastAPI 入口
    schemas.py           # 请求体模型
    routes/
      chat.py
      extract.py
```

## 环境要求

- Python 3.10+
- DeepSeek API Key（或兼容 OpenAI SDK 的接口）

## 快速开始

### 1. 克隆并进入项目

```bash
cd mini-chat-cli
```

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

### 3. 配置环境变量

在项目根目录创建 `.env` 文件：

```env
DEEPSEEK_API_KEY=你的密钥
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-v4-flash
```


### 4. 运行方式

**终端多轮聊天：**

```bash
python main.py
```

输入 `exit` 或 `quit` 退出。

**结构化抽取 demo：**

```bash
python structured_demo.py
```

**启动 HTTP 服务：**

```bash
uvicorn api.app:app --reload
```

- 接口文档（Swagger）：<http://127.0.0.1:8000/docs>
- 健康检查：<http://127.0.0.1:8000/health>

## API 示例

### 健康检查

```bash
curl http://127.0.0.1:8000/health
```

### 结构化抽取 `POST /api/extract`

请求：

```json
{
  "text": "我叫小明，住在杭州，你们家快递太慢了，我很生气。"
}
```

响应字段示例：`name`、`city`、`sentiment`（`positive` / `negative` / `neutral`）、`summary`。

```bash
curl -X POST http://127.0.0.1:8000/api/extract \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"我叫小明，住在杭州，快递太慢了。\"}"
```

### 多轮对话 `POST /api/chat`

**第 1 轮** — 可只传当前用户消息：

```json
{
  "messages": [
    {
      "role": "user",
      "content": "我叫小明，请记住我的名字"
    }
  ]
}
```

响应示例：

```json
{
  "reply": "好的，小明，我会记住你的名字。",
  "messages": [
    {"role": "system", "content": "你是一个简洁的助手。"},
    {"role": "user", "content": "我叫小明，请记住我的名字"},
    {"role": "assistant", "content": "好的，小明，我会记住你的名字。"}
  ]
}
```

**第 2 轮** — 将上一轮响应中的 `messages` 完整复制到请求体，并在末尾追加新的 `user`：

```json
{
  "messages": [
    {"role": "system", "content": "你是一个简洁的助手。"},
    {"role": "user", "content": "我叫小明，请记住我的名字"},
    {"role": "assistant", "content": "好的，小明，我会记住你的名字。"},
    {"role": "user", "content": "我叫什么名字？"}
  ]
}
```

后续轮次同理：始终使用上一次返回的 `messages`，再 append 新的 `user`。

> 对话历史超过 5 轮问答时会自动裁剪（保留 `system` 与最近 5 轮），见 `services/history.py`。

## 常见 HTTP 状态码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 401 | API Key 认证失败 |
| 422 | 请求体无效或模型返回无法解析为 JSON（extract） |
| 429 | 限流 |
| 502 | 上游 API 错误 |
| 503 | 未配置 `DEEPSEEK_API_KEY` |

## 技术栈

- [OpenAI Python SDK](https://github.com/openai/openai-python)（兼容 DeepSeek）
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)

## License

学习与个人作品集用途；使用 API 时请遵守 DeepSeek 服务条款。
=======
一个AI部署测试
>>>>>>> 67026ae0c0b5c2e7e054eb5312b94fd9cd853d97
