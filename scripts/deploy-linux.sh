#!/usr/bin/env bash
# Private RAG delivery package — Linux server deployment script.
# Idempotent: safe to re-run.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Project root: $ROOT"

# 1. Preflight: Python 3.11+ and Ollama
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 not found. Install Python 3.11 or 3.12 first."; exit 1
fi
if ! command -v ollama >/dev/null 2>&1; then
  echo "ERROR: ollama not found. Install Ollama from https://ollama.com first."; exit 1
fi

# 2. Environment file
if [ ! -f .env ]; then
  cp .env.example .env
  echo "==> Created .env from .env.example. Review and edit it before production use."
fi
# shellcheck disable=SC1091
set -a; . ./.env; set +a

# 3. Virtual environment
if [ ! -d .venv ]; then
  echo "==> Creating virtual environment"
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

echo "==> Installing Python dependencies"
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Pull required models
echo "==> Ensuring models are present: $CHAT_MODEL, $EMBED_MODEL"
ollama pull "$CHAT_MODEL"
ollama pull "$EMBED_MODEL"

# 5. Ingest documents
echo "==> Ingesting documents from inputs/"
python rag/ingest.py

cat <<EOF

==> Deployment setup complete.

Start the web UI with:
  streamlit run rag/app.py --server.port ${APP_PORT:-8501} --server.headless true

To run as a background service, see DEPLOYMENT.md (systemd section).
Run healthcheck:  bash scripts/healthcheck.sh
EOF
