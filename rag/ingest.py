"""Ingest documents from inputs/ into a local vector store (chunks.json).

Run:  python rag/ingest.py
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config
import ollama_client


def read_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt", ".csv"}:
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    if suffix == ".docx":
        import docx

        doc = docx.Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs)
    if suffix in {".html", ".htm"}:
        from bs4 import BeautifulSoup

        return BeautifulSoup(
            path.read_text(encoding="utf-8", errors="ignore"), "html.parser"
        ).get_text()
    return ""


def _sections(text: str) -> list[tuple[str, str]]:
    """Split markdown into (heading, body) blocks, tracking the latest heading."""
    blocks: list[tuple[str, str]] = []
    heading = ""
    cur: list[str] = []
    for line in text.splitlines():
        if line.strip().startswith("#"):
            if cur:
                blocks.append((heading, "\n".join(cur).strip()))
                cur = []
            heading = line.strip().lstrip("#").strip()
        else:
            cur.append(line)
    if cur:
        blocks.append((heading, "\n".join(cur).strip()))
    return blocks


def _make_chunk(source: str, heading: str, body: str) -> dict:
    text = f"[{heading}] {body}" if heading else body
    return {"source": source, "heading": heading, "text": text}


def split_text(text: str, source: str) -> list[dict]:
    chunks: list[dict] = []
    for heading, body in _sections(text):
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
        buf = ""
        for para in paragraphs:
            if len(buf) + len(para) <= config.CHUNK_SIZE:
                buf = f"{buf}\n{para}".strip()
            else:
                if buf:
                    chunks.append(_make_chunk(source, heading, buf))
                overlap = buf[-config.CHUNK_OVERLAP:] if buf else ""
                buf = f"{overlap}\n{para}".strip()
        if buf:
            chunks.append(_make_chunk(source, heading, buf))
    return chunks


def main() -> None:
    if not config.INPUT_DIR.exists():
        raise SystemExit(f"Input directory not found: {config.INPUT_DIR}")

    skip_names = {"readme.md", "readme.txt", ".gitkeep", ".gitignore"}
    all_chunks: list[dict] = []
    files = [
        p
        for p in config.INPUT_DIR.rglob("*")
        if p.is_file() and p.name.lower() not in skip_names
    ]
    for path in files:
        text = read_text(path)
        if not text.strip():
            continue
        pieces = split_text(text, path.name)
        all_chunks.extend(pieces)
        print(f"  {path.name}: {len(pieces)} chunks")

    print(f"Embedding {len(all_chunks)} chunks with {config.EMBED_MODEL} ...")
    for i, chunk in enumerate(all_chunks):
        chunk["embedding"] = ollama_client.embed(chunk["text"])
        if (i + 1) % 10 == 0:
            print(f"  embedded {i + 1}/{len(all_chunks)}")

    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.CHUNKS_FILE.write_text(
        json.dumps(all_chunks, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Saved {len(all_chunks)} chunks -> {config.CHUNKS_FILE}")


if __name__ == "__main__":
    main()
