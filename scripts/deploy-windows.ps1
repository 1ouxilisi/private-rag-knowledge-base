<#
.SYNOPSIS
  Private RAG delivery package — Windows deployment + smoke test.
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File .\scripts\deploy-windows.ps1
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

# 1. Preflight
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw "python not found. Install Python 3.11 or 3.12 first."
}
if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
  throw "ollama not found. Install Ollama first."
}

# 2. Environment file
if (-not (Test-Path ".env")) {
  Copy-Item ".env.example" ".env"
  Write-Host "Created .env from .env.example. Review it before production use."
}

# 3. Virtual environment
if (-not (Test-Path ".venv")) {
  python -m venv .venv
}
$py = ".\.venv\Scripts\python.exe"

Write-Host "==> Installing dependencies"
& $py -m pip install --upgrade pip
& $py -m pip install -r requirements.txt

# 4. Models (read from .env when available)
$envFile = Get-Content ".env"
$chat = ($envFile | Where-Object { $_ -match "^CHAT_MODEL=" }) -replace "CHAT_MODEL=", ""
$embed = ($envFile | Where-Object { $_ -match "^EMBED_MODEL=" }) -replace "EMBED_MODEL=", ""
$chat = ($chat.Trim()); $embed = ($embed.Trim())
if (-not $chat) { $chat = "qwen3:8b" }
if (-not $embed) { $embed = "bge-m3" }

Write-Host "==> Ensuring models: $chat, $embed"
ollama pull $chat
ollama pull $embed

# 5. Ingest
Write-Host "==> Ingesting documents"
& $py rag/ingest.py

# 6. Smoke test
$body = @{ model = $chat; prompt = "Reply with: deployment check OK."; stream = $false } | ConvertTo-Json
$r = Invoke-RestMethod "http://localhost:11434/api/generate" -Method Post -Body $body `
  -ContentType "application/json" -TimeoutSec 180
$tps = if ($r.eval_duration -gt 0) { [math]::Round($r.eval_count / ($r.eval_duration / 1e9), 2) } else { 0 }
Write-Host "Smoke test OK. tokens=$($r.eval_count) generation=$tps tokens/s"
Write-Host "--- response ---"; Write-Host $r.response

Write-Host "`nStart the UI:  .\.venv\Scripts\python.exe -m streamlit run rag/app.py --server.port 8501 --server.headless true"
