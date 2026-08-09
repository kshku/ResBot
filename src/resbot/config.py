import os
from dataclasses import dataclass

from langchain_core.chat_models import BaseChatModel


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    model: str
    base_url: str | None
    api_key: str | None

DEFAULT_MODELS = {
    "openai": "gpt-4o-mini",
    "openrouter": "openai/gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-latest",
    "ollama": "llama3.1",
}

API_KEYS = {
    "openai": "OPENAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "ollama": None,
}

DEFAULT_BASE_URLS = {
    "openrouter": "https://openrouter.ai/api/v1",
    "ollama": "http://localhost:11434",
}

def load_config() -> LLMConfig:
    provider = os.getenv("RESBOT_LLM_PROVIDER", "openai").lower()
    if provider not in DEFAULT_MODELS:
        raise ValueError(f"unknown provider '{provider}' (expected one of {', '.join(DEFAULT_MODELS)})")
    model = os.getenv("RESBOT_LLM_MODEL") or DEFAULT_MODELS[provider]
    base_url = os.getenv("RESBOT_LLM_BASE_URL") or DEFAULT_BASE_URLS.get(provider)
    key_env = API_KEYS[provider]
    api_key = os.getenv(key_env) if key_env else None
    return LLMConfig(provider, model, base_url, api_key)

def get_chat_model(config: LLMConfig) -> BaseChatModel:
    match config.provider:
        case "openai" | "openrouter":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=config.model,
                base_url=config.base_url,
                api_key=config.api_key
            )
        case "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(
                model=config.model,
                base_url=config.base_url,
                api_key=config.api_key
            )
        case "ollama":
            from langchain_ollama import ChatOllama
            return ChatOllama(
                model=config.model,
                base_url=config.base_url
            )
        case _:
            raise RuntimeError("should not reach here")

