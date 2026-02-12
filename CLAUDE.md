# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

QuickRAG is a single-file local RAG (Retrieval-Augmented Generation) application. It loads `.md` and `.txt` documents from a local directory, chunks and indexes them into a ChromaDB vector store, then provides an interactive Q&A loop using Ollama-hosted LLMs.

## Commands

```bash
# Install dependencies
uv sync

# Run the app (requires Ollama running locally)
uv run python main.py

# Re-index documents (delete persisted store first)
rm -rf .chroma_index && uv run python main.py
```

## Architecture

Everything lives in `main.py` — there are no modules or packages. The flow is:

1. **Document loading** — `load_documents()` reads `.md`/`.txt` files from `docs/CFIS/` via LangChain `DirectoryLoader`
2. **Indexing** — `build_or_load_vectorstore()` chunks documents (900 chars, 150 overlap) and persists a ChromaDB index to `.chroma_index/`. On subsequent runs, it loads from disk instead of re-indexing
3. **Retrieval + Generation** — `answer_question()` retrieves top-5 chunks via similarity search, builds a prompt with citations, and sends to Ollama's chat model
4. **Interactive loop** — `__main__` block runs a REPL that takes questions until "exit"

## Key Configuration (top of main.py)

| Constant          | Purpose                                             | Default                  |
| ----------------- | --------------------------------------------------- | ------------------------ |
| `DOCS_DIR`        | Source documents path                               | `./docs/CFIS`            |
| `CHROMA_DIR`      | Persisted vector store                              | `./.chroma_index`        |
| `CHAT_MODEL`      | Ollama chat model name                              | `kimi-k2.5:cloud`        |
| `EMBED_MODEL`     | Ollama embedding model                              | `embeddinggemma:latest`  |
| `OLLAMA_BASE_URL` | Ollama server URL (env override: `OLLAMA_BASE_URL`) | `http://127.0.0.1:11434` |

## Dependencies

- **LangChain** ecosystem: `langchain`, `langchain-community`, `langchain-ollama`, `langchain-text-splitters`
- **ChromaDB**: Vector store with SQLite persistence
- **Ollama**: Local LLM inference (must be running separately)

## Notes

- The `docs/CFIS/` directory contains the knowledge base documents (project documentation for a "CFIS" system)
- `.chroma_index/` is the persisted vector store — delete it to force re-indexing
- No tests exist yet
- Python 3.11 required (`.python-version`)
