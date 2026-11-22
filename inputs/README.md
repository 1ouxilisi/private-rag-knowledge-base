# Place client documents in this folder.

Supported formats: `.md`, `.txt`, `.csv`, `.pdf`, `.docx`, `.html` / `.htm`.

After adding or replacing files, re-run:

```bash
python rag/ingest.py
```

The bundled files are public Ollama documentation pages used as a demonstration
knowledge base. For a client delivery, replace them with the client's own
documents and re-run the ingest step.
