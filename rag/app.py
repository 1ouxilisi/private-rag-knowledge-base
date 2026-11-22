"""Streamlit UI for the private RAG delivery package.

Run:  streamlit run rag/app.py --server.port <APP_PORT>
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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
        reply, sources = chain.answer(question)
    st.write(reply)
    with st.expander("Retrieved sources"):
        for src in sources:
            st.write("-", src["source"])
            st.caption(src["text"][:300])
