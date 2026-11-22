# Deployment Manual — Private RAG Delivery Package

## 1. Architecture

```
 Customer documents (inputs/)
        │  chunk + embed (bge-m3, local Ollama)
        ▼
 chunks.json (local vector store, cosine similarity search)
        │  retrieve top-K
        ▼
 qwen3:8b (local Ollama) ──► Streamlit UI / API
```

Everything runs inside the customer's own environment. No document or prompt is
sent to a third-party hosted model API.

## 2. Prerequisites

| Component | Requirement |
|---|---|
| OS | Ubuntu 22.04/24.04, Debian 12, or Windows 10/11; cloud VM or on-prem server |
| Python | 3.11 or 3.12 (3.13 may have unresolved wheel issues) |
| Ollama | Latest release, service reachable at `OLLAMA_BASE` |
| GPU (recommended) | 8 GB VRAM for 7B–8B Q4; 12–16 GB for 14B Q4; CPU-only works but is slow |
| RAM | 16 GB minimum |
| Disk | 10 GB+ for models, dependencies, and the vector store |

## 3. Quick start

### Linux server
```bash
chmod +x scripts/deploy-linux.sh
bash scripts/deploy-linux.sh
# then:
streamlit run rag/app.py --server.port 8501 --server.headless true
```

### Windows
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\deploy-windows.ps1
```

### Verify
```bash
bash scripts/healthcheck.sh
```

## 4. Configuration (`.env`)

Copy `.env.example` to `.env` and adjust:

| Variable | Purpose | Example |
|---|---|---|
| `OLLAMA_BASE` | Ollama API address | `http://localhost:11434` |
| `CHAT_MODEL` | Answer-generation model | `qwen3:8b` |
| `EMBED_MODEL` | Embedding model | `bge-m3` |
| `TOP_K` | Retrieved chunks per question | `3` |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | Document splitting | `600` / `100` |
| `TEMPERATURE` | Generation randomness | `0.2` |
| `INPUT_DIR` / `DATA_DIR` | Document and vector store paths | `inputs` / `data` |
| `APP_PORT` | Streamlit port | `8501` |

After changing models, paths, or documents, re-run `python rag/ingest.py`.

## 5. Running as a background service (Linux, systemd)

Create `/etc/systemd/system/private-rag.service`:

```ini
[Unit]
Description=Private RAG Streamlit
After=network.target ollama.service

[Service]
WorkingDirectory=/opt/private-rag
EnvironmentFile=/opt/private-rag/.env
ExecStart=/opt/private-rag/.venv/bin/streamlit run rag/app.py --server.port 8501 --server.headless true
Restart=always
User=rag

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now private-rag
sudo systemctl status private-rag
```

## 6. Operations

- **Add new documents:** drop files into `inputs/`, re-run `python rag/ingest.py`.
- **Backup:** back up `inputs/` and `data/chunks.json`; models can be re-pulled with `ollama pull`.
- **Update model:** change `CHAT_MODEL`/`EMBED_MODEL` in `.env`, `ollama pull <model>`, re-ingest if the embedding model changed.
- **Logs:** systemd journal (`journalctl -u private-rag -f`) or the terminal output when running manually.
- **Uninstall:** stop the service, remove the project directory, and `ollama rm <models>` if no longer needed.

## 7. Security & data handling

- Documents stay in the customer's environment; do not copy raw data to the developer's machine.
- Use a read-only database/user when connecting external sources.
- Store any credentials in `.env`, never commit `.env` to version control.
- Sign an NDA before handling client-confidential material.
- Expose the UI only on the internal network or behind the customer's SSO/VPN.

## 8. Troubleshooting

| Symptom | Check |
|---|---|
| `Ollama not reachable` | Is the Ollama service running? Is `OLLAMA_BASE` correct? |
| `chunks.json not found` | Run `python rag/ingest.py` after adding documents |
| Out of VRAM | Use a smaller model or lower quantization (Q4), shorten context, or move to a larger GPU |
| Slow answers | Confirm the model is running on GPU (`ollama ps` shows `100% GPU`); CPU inference is slow |
| Wrong / hallucinated answers | Increase `TOP_K`, refine chunks, verify the source text, keep temperature low |
| Model speaks outside the documents | Confirm the system prompt is active; the chain already rejects unsupported answers |
