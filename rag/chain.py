"""Retrieval-augmented generation over chunks.json."""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
import ollama_client

SYSTEM_PROMPT = (
    "You are a strict retrieval-only assistant.\n"
    "Rules:\n"
    "- Answer using ONLY the provided context. Never use outside knowledge.\n"
    "- If the answer is not present in the context, reply exactly: "
    "\"I do not know based on the provided documents.\" Do not guess or add facts.\n"
    "- Quote numbers, dates, and names exactly as they appear in the context.\n"
    "- End your answer with the source file name(s)."
)


def _load_chunks() -> list[dict]:
    if not config.CHUNKS_FILE.exists():
        raise SystemExit("chunks.json not found. Run python rag/ingest.py first.")
    return json.loads(config.CHUNKS_FILE.read_text(encoding="utf-8"))


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def retrieve(question: str, chunks: list[dict]) -> list[dict]:
    q_emb = ollama_client.embed(question)
    scored = sorted(chunks, key=lambda c: _cosine(q_emb, c["embedding"]), reverse=True)
    return scored[: config.TOP_K]


def answer(question: str) -> tuple[str, list[dict]]:
    chunks = _load_chunks()
    top = retrieve(question, chunks)
    context = "\n\n".join(f"[{c['source']}]\n{c['text']}" for c in top)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]
    reply = ollama_client.chat(messages)
    return reply, top
