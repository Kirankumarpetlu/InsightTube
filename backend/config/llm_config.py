"""
Groq LLM configuration module for AutoGen agents.
Provides an OpenAIChatCompletionClient configured to use Groq's OpenAI-compatible API.
Compatible with autogen-agentchat 0.4+ / pyautogen 0.10+.
"""

import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY environment variable is not set. "
        "Please add it to your .env file."
    )


def get_model_client() -> OpenAIChatCompletionClient:
    """
    Create and return an OpenAIChatCompletionClient configured for Groq.
    Uses Groq's OpenAI-compatible endpoint so AutoGen agents can use it directly.
    """
    return OpenAIChatCompletionClient(
        model=MODEL_NAME,
        api_key=GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
            "structured_output": False,
        },
    )
