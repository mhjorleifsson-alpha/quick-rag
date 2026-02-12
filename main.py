"""QuickRAG — local Retrieval-Augmented Generation with Ollama.

Single-file RAG application that loads .md and .txt documents from a local
directory, indexes them into a ChromaDB vector store, and provides an
interactive Q&A loop powered by an Ollama-hosted LLM.

Conversation history is maintained for the duration of the session so that
follow-up questions can reference earlier answers.

Usage:
    uv run python main.py

Configuration constants are defined at the top of this file. The Ollama
base URL can also be overridden via the OLLAMA_BASE_URL environment variable.
"""

from __future__ import annotations

import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import List, Tuple

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama


DOCS_DIR = Path("./docs")               # put your .md, .txt docs here
CHROMA_DIR = Path("./.chroma_index")     # persisted vector store on disk

CHAT_MODEL = "kimi-k2.5:cloud"
EMBED_MODEL = "embeddinggemma:latest"

# Ollama default base url is http://127.0.0.1:11434
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

# Maximum number of past Q&A turns to include in the LLM prompt.
# Keeps token usage bounded while preserving conversational context.
MAX_HISTORY_TURNS = 10

SYSTEM_PROMPT = (
    "You are answering questions using the provided project documents.\n"
    "Use the context to answer. If the context does not contain the answer, "
    "say you do not know.\n"
    "Cite sources using bracket numbers like [1] or [2].\n"
    "You have access to the conversation history so you can resolve references "
    "to earlier questions and answers."
)


def _check_ollama_reachable(base_url: str) -> None:
    """Verify that the Ollama server is reachable before doing any real work.

    Args:
        base_url: The Ollama server URL to probe (hits the root endpoint).

    Raises:
        SystemExit: If the server cannot be reached within 5 seconds.
    """
    try:
        urllib.request.urlopen(base_url, timeout=5)  # noqa: S310 — trusted local URL
    except (urllib.error.URLError, OSError) as exc:
        raise SystemExit(
            f"Cannot reach Ollama at {base_url} — is the server running?\n"
            f"  Detail: {exc}"
        )


def load_documents(docs_dir: Path) -> list:
    """Load .md and .txt files from *docs_dir* (recursively).

    Uses LangChain ``DirectoryLoader`` with multithreading for faster I/O.

    Args:
        docs_dir: Root directory to scan. Subdirectories are included via
            ``**/*.md`` and ``**/*.txt`` glob patterns.

    Returns:
        A list of LangChain ``Document`` objects.

    Raises:
        SystemExit: If no documents are found in *docs_dir*.
    """
    loaders = [
        DirectoryLoader(
            str(docs_dir),
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
            show_progress=True,
            use_multithreading=True,
        ),
        DirectoryLoader(
            str(docs_dir),
            glob="**/*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
            show_progress=True,
            use_multithreading=True,
        ),
    ]

    docs: list = []
    for loader in loaders:
        docs.extend(loader.load())

    if not docs:
        raise SystemExit(
            f"No .md or .txt documents found in {docs_dir.resolve()}. "
            "Add documents and try again."
        )

    return docs


def build_or_load_vectorstore(docs_dir: Path, chroma_dir: Path) -> Chroma:
    """Create or reload the ChromaDB vector store.

    On first run the documents are loaded, chunked, embedded, and persisted
    to *chroma_dir*. On subsequent runs the existing index is loaded from disk.

    Args:
        docs_dir:   Directory containing source documents.
        chroma_dir: Directory where the ChromaDB index is persisted.

    Returns:
        A ready-to-query ``Chroma`` vector store instance.
    """
    embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)

    if chroma_dir.exists():
        return Chroma(
            persist_directory=str(chroma_dir),
            embedding_function=embeddings,
        )

    raw_docs = load_documents(docs_dir)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,      # characters per chunk — balances context vs. noise
        chunk_overlap=150,   # overlap keeps sentence boundaries intact
    )
    chunks = splitter.split_documents(raw_docs)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(chroma_dir),
    )
    # ChromaDB auto-persists when a persist_directory is provided — no
    # explicit persist() call needed (deprecated since ChromaDB 0.4+).
    return vectordb


def format_context(docs) -> Tuple[str, List[str]]:
    """Build a numbered context block and citation list from retrieved docs.

    Args:
        docs: List of LangChain ``Document`` objects from the retriever.

    Returns:
        A ``(context_string, citations_list)`` tuple where *context_string*
        is the concatenated chunk text with source labels and *citations_list*
        contains human-readable ``[n] path`` entries.
    """
    citations: list[str] = []
    parts: list[str] = []
    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("source", "unknown_source")
        citations.append(f"[{i}] {src}")
        parts.append(f"Source [{i}] ({src})\n{d.page_content}")
    return "\n\n".join(parts), citations


def answer_question(
    vectordb: Chroma,
    question: str,
    chat_history: list[Tuple[str, str]],
) -> Tuple[str, str]:
    """Retrieve relevant chunks and generate an LLM answer with citations.

    Conversation history is included so the LLM can resolve follow-up
    questions that reference prior exchanges.

    Args:
        vectordb:      The ChromaDB vector store to search.
        question:      The user's natural-language question.
        chat_history:  List of ``(user_question, assistant_answer)`` tuples
                       from earlier turns in this session.

    Returns:
        A ``(display_text, raw_answer)`` tuple.  *display_text* includes the
        sources block for printing; *raw_answer* is the LLM reply without
        sources, stored in history so it doesn't bloat future prompts.
    """
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})  # top-5 chunks
    retrieved = retriever.invoke(question)

    if not retrieved:
        msg = (
            "No relevant documents were found for your question. "
            "Try rephrasing or check that the document set covers this topic."
        )
        return msg, msg

    context, citations = format_context(retrieved)

    # Build the message list: system → history → current question with context
    messages: list = [SystemMessage(content=SYSTEM_PROMPT)]

    # Include the most recent MAX_HISTORY_TURNS exchanges
    for past_q, past_a in chat_history[-MAX_HISTORY_TURNS:]:
        messages.append(HumanMessage(content=past_q))
        messages.append(AIMessage(content=past_a))

    # Current turn: question + retrieved context
    user_content = f"Question:\n{question}\n\nContext:\n{context}"
    messages.append(HumanMessage(content=user_content))

    llm = ChatOllama(model=CHAT_MODEL, base_url=OLLAMA_BASE_URL)

    try:
        response = llm.invoke(messages)
    except Exception as exc:  # noqa: BLE001 — surface any LLM backend failure
        err = f"LLM call failed: {exc}"
        return err, err

    content = response.content if hasattr(response, "content") else response
    raw_answer = content if isinstance(content, str) else str(content)

    cites_block = "Sources:\n" + "\n".join(citations)
    display_text = f"{raw_answer}\n\n{cites_block}"
    return display_text, raw_answer


if __name__ == "__main__":
    if not DOCS_DIR.exists():
        raise SystemExit(f"Docs folder not found: {DOCS_DIR.resolve()}")

    _check_ollama_reachable(OLLAMA_BASE_URL)

    db = build_or_load_vectorstore(DOCS_DIR, CHROMA_DIR)

    history: list[Tuple[str, str]] = []

    while True:
        try:
            q = input("\nAsk a question (or type exit): ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not q or q.lower() == "exit":
            break

        try:
            display, raw = answer_question(db, q, history)
            history.append((q, raw))
            print("\n" + display)
        except Exception as exc:  # noqa: BLE001
            print(f"\nError: {exc}")
