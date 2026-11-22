"""Thin wrapper around the local Ollama HTTP API (no LangChain dependency)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
import config


def embed(text: str) -> list[float]:
    resp = requests.post(
        f"{config.OLLAMA_BASE}/api/embeddings",
        json={"model": config.EMBED_MODEL, "prompt": text},
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]


def chat(messages: list[dict], temperature: float | None = None) -> str:
    resp = requests.post(
        f"{config.OLLAMA_BASE}/api/chat",
        json={
            "model": config.CHAT_MODEL,
            "messages": messages,
            "stream": False,
            "options": {"temperature": config.TEMPERATURE if temperature is None else temperature},
        },
        timeout=180,
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]
