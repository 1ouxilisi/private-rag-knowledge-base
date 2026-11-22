#!/usr/bin/env bash
# Health check: Ollama service, required models, vector store, app port.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

set -a; . ./.env 2>/dev/null || true; set +a
OLLAMA_BASE="${OLLAMA_BASE:-http://localhost:11434}"
APP_PORT="${APP_PORT:-8501}"

fail=0

echo "==> Ollama service"
if curl -sf "$OLLAMA_BASE/api/tags" >/dev/null; then
  echo "OK: Ollama reachable at $OLLAMA_BASE"
else
  echo "FAIL: Ollama not reachable at $OLLAMA_BASE"; fail=1
fi

echo "==> Required models"
tags="$(curl -sf "$OLLAMA_BASE/api/tags" 2>/dev/null || echo "")"
for m in "${CHAT_MODEL:-qwen3:8b}" "${EMBED_MODEL:-bge-m3}"; do
  if echo "$tags" | grep -q "$m"; then echo "OK: $m present"; else echo "MISSING: $m"; fail=1; fi
done

echo "==> Vector store"
if [ -f data/chunks.json ]; then
  n="$(grep -o '"source"' data/chunks.json | wc -l | tr -d ' ')"
  echo "OK: chunks.json found ($n chunk references)"
else
  echo "MISSING: data/chunks.json — run python rag/ingest.py"; fail=1
fi

echo "==> App port $APP_PORT"
if curl -sf "http://localhost:$APP_PORT" >/dev/null; then
  echo "OK: app responding on :$APP_PORT"
else
  echo "WARN: app not responding on :$APP_PORT (start with streamlit)"
fi

[ "$fail" -eq 0 ] && echo "==> Health check passed" || { echo "==> Health check has issues"; exit 1; }
