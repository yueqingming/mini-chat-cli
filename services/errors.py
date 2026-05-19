"""错误定义：MissingApiKeyError、AuthenticationError、RateLimitError、APIError、Exception。"""

class MissingApiKeyError(Exception):
    """未配置 DEEPSEEK_API_KEY。"""
