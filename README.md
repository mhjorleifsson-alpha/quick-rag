# QuickRAG

Local Retrieval-Augmented Generation app powered by Ollama and ChromaDB.

Drop `.md` and `.txt` files into `docs/`, run the app, and ask questions — answers are generated from your documents with source citations. Supports pluggable chat LLM providers via any OpenAI-compatible API.

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

Settings can be configured via a `.env` file in the project root (recommended) or via shell environment variables. Copy the template to get started:

```bash
cp .env.example .env
```

Edit `.env` with your values — shell environment variables take precedence over `.env` entries.

Constants at the top of `main.py`:

| Constant            | Purpose                     | Default                  |
| ------------------- | --------------------------- | ------------------------ |
| `DOCS_DIR`          | Source documents directory  | `./docs`                 |
| `CHROMA_DIR`        | Persisted vector store path | `./.chroma_index`        |
| `CHAT_MODEL`        | Ollama chat model name      | `kimi-k2.5:cloud`        |
| `EMBED_MODEL`       | Ollama embedding model name | `embeddinggemma:latest`  |
| `OLLAMA_BASE_URL`   | Ollama server URL           | `http://127.0.0.1:11434` |
| `MAX_HISTORY_TURNS` | Chat history turns kept     | `10`                     |

## Using an OpenAI-Compatible Provider

To use an OpenAI-compatible API (e.g. OpenWebUI, LiteLLM, vLLM) for chat instead of Ollama, add the following to your `.env` file:

```
LLM_PROVIDER=openwebui
LLM_MODEL=gpt-5.2-alpha
LLM_BASE_URL=https://your-provider.example.com/api/v1/
LLM_API_KEY=sk-your-api-key
```

| Env Var        | Purpose                                | Default               |
| -------------- | -------------------------------------- | --------------------- |
| `LLM_PROVIDER` | `ollama` (default) or any other value  | `ollama`              |
| `LLM_MODEL`    | Chat model name                        | `CHAT_MODEL` constant |
| `LLM_BASE_URL` | API base URL (required for non-Ollama) | `""`                  |
| `LLM_API_KEY`  | API key (required for non-Ollama)      | `""`                  |

Ollama is still required for embeddings regardless of the chat provider.

## Re-indexing

Delete the persisted store and re-run:

```bash
rm -rf .chroma_index && uv run python main.py
```
