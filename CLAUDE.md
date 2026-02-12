# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

QuickRAG is a single-file local RAG (Retrieval-Augmented Generation) application. It loads `.md` and `.txt` documents from a local directory, chunks and indexes them into a ChromaDB vector store, then provides an interactive Q&A loop using Ollama-hosted LLMs. The chat LLM can optionally be switched to any OpenAI-compatible API (e.g. OpenWebUI) via environment variables; embeddings always use Ollama.

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

1. **Document loading** — `load_documents()` reads `.md`/`.txt` files recursively from `docs/` via LangChain `DirectoryLoader`
2. **Indexing** — `build_or_load_vectorstore()` chunks documents (900 chars, 150 overlap) and persists a ChromaDB index to `.chroma_index/`. On subsequent runs, it loads from disk instead of re-indexing
3. **Retrieval + Generation** — `answer_question()` retrieves top-5 chunks via similarity search, builds a message list with conversation history and context, and sends to the configured chat LLM
4. **Chat memory** — Session-level conversation history (last `MAX_HISTORY_TURNS` exchanges) is passed as `HumanMessage`/`AIMessage` pairs so the LLM can resolve follow-up questions
5. **Interactive loop** — `__main__` block runs a REPL that takes questions until "exit", maintaining history across turns

## Key Configuration (top of main.py)

| Constant / Env Var  | Purpose                                             | Default                  |
| ------------------- | --------------------------------------------------- | ------------------------ |
| `DOCS_DIR`          | Source documents path                               | `./docs`                 |
| `CHROMA_DIR`        | Persisted vector store                              | `./.chroma_index`        |
| `CHAT_MODEL`        | Default Ollama chat model name                      | `kimi-k2.5:cloud`        |
| `EMBED_MODEL`       | Ollama embedding model (always Ollama)              | `embeddinggemma:latest`  |
| `OLLAMA_BASE_URL`   | Ollama server URL (env override: `OLLAMA_BASE_URL`) | `http://127.0.0.1:11434` |
| `MAX_HISTORY_TURNS` | Number of past Q&A turns kept in LLM context        | `10`                     |
| `LLM_PROVIDER`      | Chat LLM provider: `ollama` or any OpenAI-compatible name | `ollama`            |
| `LLM_MODEL`         | Chat model name (overrides `CHAT_MODEL`)            | Falls back to `CHAT_MODEL` |
| `LLM_BASE_URL`      | API base URL for non-Ollama providers               | `""` (required if not ollama) |
| `LLM_API_KEY`       | API key for non-Ollama providers                    | `""` (required if not ollama) |

## Dependencies

- **LangChain** ecosystem: `langchain`, `langchain-community`, `langchain-chroma`, `langchain-ollama`, `langchain-openai`, `langchain-text-splitters`
- **ChromaDB**: Vector store with SQLite persistence (via `langchain-chroma`)
- **Ollama**: Local LLM inference — always required for embeddings, optional for chat (must be running separately)
- **OpenAI-compatible APIs**: Optional chat provider via `langchain-openai` (e.g. OpenWebUI, LiteLLM, vLLM)
- **python-dotenv**: Loads `.env` file from project root into `os.environ` at startup (shell env vars take precedence)

## Notes

- The `docs/` directory (and its subdirectories) contains the knowledge base documents — any `.md` or `.txt` files placed here are indexed
- `.chroma_index/` is the persisted vector store — delete it to force re-indexing
- At startup the app checks that Ollama is reachable and that documents exist, exiting with a clear message on failure
- No tests exist yet
- Python 3.11 required (`.python-version`)
