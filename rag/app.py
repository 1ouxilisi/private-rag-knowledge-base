"""Streamlit UI for the private RAG delivery package.

Run:  streamlit run rag/app.py --server.port <APP_PORT>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
import streamlit as st
import chain
import config

st.set_page_config(page_title="Private RAG Knowledge Base")
st.title("Private RAG — runs on your own infrastructure")
st.caption(
    f"LLM: {config.CHAT_MODEL} · Embedding: {config.EMBED_MODEL} · "
    f"Ollama: {config.OLLAMA_BASE}"
)

question = st.text_input("Ask a question about the documents:")

if question:
    with st.spinner("Retrieving context and generating answer..."):
        try:
            reply, sources = chain.answer(question)
        except requests.exceptions.ConnectionError:
            st.error(
                f"Cannot reach Ollama at {config.OLLAMA_BASE}. "
                "Check that the Ollama service is running and OLLAMA_BASE is correct."
            )
            st.stop()
        except SystemExit as exc:
            st.error(str(exc) or "Vector store missing. Run `python rag/ingest.py` first.")
            st.stop()
        except requests.exceptions.RequestException as exc:
            st.error(f"Request to the local model failed: {exc}")
            st.stop()
        except Exception as exc:  # noqa: BLE001
            st.error(f"Unexpected error: {exc}")
            st.stop()
    st.write(reply)
    with st.expander("Retrieved sources"):
        for src in sources:
            st.write("-", src["source"])
            st.caption(src["text"][:300])
