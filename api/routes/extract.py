import json

from fastapi import APIRouter, HTTPException
from openai import APIError, AuthenticationError, RateLimitError

from api.schemas import ExtractRequest
from config import MISSING_API_KEY_MESSAGE
from services.errors import MissingApiKeyError
from services.extract_service import extract

router = APIRouter(prefix="/api", tags=["extract"])


@router.post("/extract")
def extract_endpoint(body: ExtractRequest) -> dict:
    try:
        return extract(body.text)
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
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=422, detail=f"JSON 解析失败：{e}")
