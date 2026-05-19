from pydantic import BaseModel, Field


class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, description="待分析的自然语言")

class ChatRequest(BaseModel):
    messages: list[dict] = Field(..., min_length=1, description="用户本轮消息")
