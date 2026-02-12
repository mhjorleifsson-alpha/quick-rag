# QuickRAG

Local Retrieval-Augmented Generation app powered by Ollama and ChromaDB.

Drop `.md` and `.txt` files into `docs/`, run the app, and ask questions — answers are generated from your documents with source citations.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- [Ollama](https://ollama.com/) running locally (default: `http://127.0.0.1:11434`)

## Quick Start

```bash
# Install dependencies
uv sync

# Start Ollama (in another terminal, if not already running)
ollama serve

# Run QuickRAG
uv run python main.py
```

On first run the app indexes all documents in `docs/` into a ChromaDB vector store (persisted to `.chroma_index/`). Subsequent runs load the existing index.

The chat maintains conversation history for the duration of the session, so you can ask follow-up questions that reference earlier answers.

## Configuration

Edit the constants at the top of `main.py`:

| Constant            | Purpose                     | Default                  |
| ------------------- | --------------------------- | ------------------------ |
| `DOCS_DIR`          | Source documents directory  | `./docs`                 |
| `CHROMA_DIR`        | Persisted vector store path | `./.chroma_index`        |
| `CHAT_MODEL`        | Ollama chat model name      | `kimi-k2.5:cloud`        |
| `EMBED_MODEL`       | Ollama embedding model name | `embeddinggemma:latest`  |
| `OLLAMA_BASE_URL`   | Ollama server URL           | `http://127.0.0.1:11434` |
| `MAX_HISTORY_TURNS` | Chat history turns kept     | `10`                     |

The Ollama URL can also be set via the `OLLAMA_BASE_URL` environment variable.

## Re-indexing

Delete the persisted store and re-run:

```bash
rm -rf .chroma_index && uv run python main.py
```
