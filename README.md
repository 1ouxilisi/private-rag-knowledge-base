# Private RAG Knowledge Base — Self-Hosted LLM + Document Q&A

A config-driven, ready-to-adapt private RAG template. Documents are chunked,
embedded, and retrieved locally; a local LLM answers only from the retrieved
context and cites the source file. No document or prompt is sent to a
third-party hosted model API.

Built as a clean, auditable delivery package — no LangChain / vector-DB
lock-in — with cross-platform deploy scripts, a health check, deployment
manual, SOW template, and handover checklist.

## Highlights

- **Fully local** — chat model and embedding model run through Ollama on your
  own infrastructure; the vector store is a local JSON file.
- **Grounded answers with citations** — the model answers only from retrieved
  chunks and lists the source file(s).
- **Controlled refusal** — questions unsupported by the documents return a
  fixed refusal phrase instead of hallucinating.
- **Config-driven** — model, embedding, chunking, top-K, temperature, paths,
  and port live in a single `.env` file.
- **Multi-format ingestion** — Markdown, TXT, CSV, PDF, DOCX, HTML.
- **Cross-platform** — setup scripts for Linux and Windows, plus a health
  check covering service, models, vector store, and app port.

## How it works

```
 Source documents (inputs/)
        │  parse + heading-aware chunk + embed (bge-m3, local Ollama)
        ▼
 chunks.json (local vector store, cosine similarity, top-5)
        │  retrieve relevant chunks
        ▼
 qwen3:8b (local Ollama) ──► Streamlit UI / source citations
```

## Tech stack

| Layer | Choice |
|---|---|
| Language / runtime | Python 3.11 / 3.12 |
| Model serving | Ollama (local) |
| Chat model | qwen3:8b (Q4) |
| Embedding model | bge-m3 (1024-dim) |
| Retrieval | stdlib cosine similarity, top-K configurable, heading-aware chunks |
| UI | Streamlit |
| HTTP | requests (direct Ollama REST API) |
| Parsers | pypdf, python-docx, beautifulsoup4, stdlib |

## Quick start

**Prerequisites:** Python 3.11/3.12, a local [Ollama](https://ollama.com)
install, and the models pulled (`qwen3:8b`, `bge-m3`). An 8 GB GPU is enough
for an 8B Q4 model; CPU-only works but is slower.

```bash
# 1. Prepare configuration
cp .env.example .env        # Windows: copy .env.example .env

# 2. Install dependencies (Linux)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Pull models and ingest documents
ollama pull qwen3:8b
ollama pull bge-m3
python rag/ingest.py

# 4. Start the UI
streamlit run rag/app.py --server.port 8501 --server.headless true
```

One-command setup scripts are also provided:

```bash
# Linux
bash scripts/deploy-linux.sh

# Windows PowerShell
powershell -ExecutionPolicy Bypass -File .\scripts\deploy-windows.ps1

# Verify service, models, vector store, and port
bash scripts/healthcheck.sh
```

## Example questions

The bundled sample knowledge base uses five public Ollama documentation pages
(quickstart, embeddings guide, API introduction, local FAQ, hardware support).
Verified against the ingested vector store:

- *What is the base URL for a local Ollama server?* → `http://localhost:11434` (api-introduction.md)
- *Does Ollama send my prompts and answers to ollama.com?* → local data is not transmitted; cloud content is not stored, logged, or used for training (local-faq.md)
- *What are embeddings used for?* → vectors for vector databases, cosine search, and RAG (embeddings.md)
- *Which Nvidia GPUs are supported?* → by compute capability, with driver requirements (hardware-support.md)
- *What is the capital of France?* → refused: *"I do not know based on the provided documents."*

## Benchmark (reference hardware)

| Item | Value |
|---|---|
| CPU / RAM / GPU | Ryzen 9 8940HX / 16 GB / RTX 5060 Laptop 8 GB |
| Chat model | qwen3:8b, context 4096, 100% GPU |
| Resident VRAM | ~5.0 GB (5078 MiB) |
| Generation speed | ~26.5 tok/s (long answer), ~34.3 tok/s (short smoke test) |
| Embedding dimension | 1024 |
| Sample knowledge base | 5 docs, 99 chunks, top-5 retrieval |

> Figures are planning references on consumer hardware; size VRAM from model
> size, quantization, context length, and concurrency for your target load.

## Project structure

```
.
├── .env.example          # All tunable settings; copy to .env
├── config.py             # Loads .env and exposes settings to the app
├── requirements.txt
├── rag/
│   ├── ollama_client.py  # Local Ollama HTTP wrapper (embed / chat)
│   ├── ingest.py         # Documents -> chunks.json (parse, chunk, embed)
│   ├── chain.py          # Retrieve top-K and generate grounded answer
│   └── app.py            # Streamlit UI
├── scripts/
│   ├── deploy-linux.sh
│   ├── deploy-windows.ps1
│   └── healthcheck.sh
├── docs/
│   ├── SOW-template.md
│   └── handover-checklist.md
├── inputs/               # Source documents go here
├── data/                 # chunks.json is generated here (git-ignored)
└── DEPLOYMENT.md
```

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `OLLAMA_BASE` | Ollama API address | `http://localhost:11434` |
| `CHAT_MODEL` | Answer-generation model | `qwen3:8b` |
| `EMBED_MODEL` | Embedding model | `bge-m3` |
| `TOP_K` | Retrieved chunks per question | `5` |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | Document splitting | `600` / `100` |
| `TEMPERATURE` | Generation randomness | `0.2` |
| `INPUT_DIR` / `DATA_DIR` | Document and vector store paths | `inputs` / `data` |
| `APP_PORT` | Streamlit port | `8501` |

## Customization

- **Model / embedding:** change `CHAT_MODEL`, `EMBED_MODEL` in `.env`.
- **Retrieval behavior:** tune `TOP_K`, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `TEMPERATURE`.
- **Prompt rules:** edit `SYSTEM_PROMPT` in `rag/chain.py`.
- **New document types:** add a parser branch in `rag/ingest.py` `read_text()`.

## Documentation

- [`DEPLOYMENT.md`](DEPLOYMENT.md) — prerequisites, service setup, operations, security, troubleshooting.
- [`docs/SOW-template.md`](docs/SOW-template.md) — statement of work and pricing milestones.
- [`docs/handover-checklist.md`](docs/handover-checklist.md) — sign-off checklist for delivery.

## Notes & disclaimer

- This repository is a personal portfolio project demonstrating a repeatable
  delivery template, not a paid client engagement.
- The bundled sample documents are public Ollama documentation
  (https://docs.ollama.com), included for demonstration only. In a client
  engagement the same template runs inside the client's own environment on
  their confidential documents, under an agreed NDA.
- `data/chunks.json` is a generated artifact and is not committed; rebuild it
  with `python rag/ingest.py` after placing documents in `inputs/`.
