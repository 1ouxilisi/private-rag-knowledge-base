"""Central configuration, loaded from .env with environment variable override."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


_load_env(ROOT / ".env")

# Ollama
OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://localhost:11434")
CHAT_MODEL = os.getenv("CHAT_MODEL", "qwen3:8b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "bge-m3")

# RAG
TOP_K = int(os.getenv("TOP_K", "5"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "600"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "100"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))

# Paths
INPUT_DIR = ROOT / os.getenv("INPUT_DIR", "inputs")
DATA_DIR = ROOT / os.getenv("DATA_DIR", "data")
CHUNKS_FILE = DATA_DIR / "chunks.json"

# App
APP_PORT = os.getenv("APP_PORT", "8501")
