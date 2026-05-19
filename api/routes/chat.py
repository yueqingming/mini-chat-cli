"""POST /api/chat 路由：校验请求、调用 chat_service、返回 HTTP 响应。"""

from fastapi import APIRouter, HTTPException
from openai import APIError, AuthenticationError, RateLimitError

from api.schemas import ChatRequest
from config import MISSING_API_KEY_MESSAGE
from services.errors import MissingApiKeyError
from services.chat_service import chat

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat")
def chat_endpoint(body: ChatRequest) -> dict:
    try:
        return chat([m.model_dump() for m in body.messages])
    except MissingApiKeyError:
        raise HTTPException(status_code=503, detail=MISSING_API_KEY_MESSAGE)
    except AuthenticationError:
        raise HTTPException(
            status_code=401,
            detail="认证失败：请检查 .env 中的 DEEPSEEK_API_KEY",
        )
    except RateLimitError:
        raise HTTPException(status_code=429, detail="请求过于频繁或被限流，请稍后再试")
    except APIError as e:
        raise HTTPException(status_code=502, detail=f"API 调用失败：{e}")
