"""从 .env / 环境变量读取 DeepSeek 配置，并创建 OpenAI 客户端。"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-v4-flash"

MISSING_API_KEY_MESSAGE = "未找到 DEEPSEEK_API_KEY，请在项目根目录配置 .env 文件"


def get_model() -> str:
    return os.environ.get("DEEPSEEK_MODEL", DEFAULT_MODEL)


def get_client() -> OpenAI | None:
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        return None
    base_url = os.environ.get("DEEPSEEK_BASE_URL", DEFAULT_BASE_URL)
    return OpenAI(base_url=base_url, api_key=api_key)
