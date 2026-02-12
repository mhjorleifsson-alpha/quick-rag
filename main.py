from __future__ import annotations

import os
from pathlib import Path
from typing import List, Tuple

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama


DOCS_DIR = Path("./docs")               # put your .md, .txt docs here
CHROMA_DIR = Path("./.chroma_index")    # persisted vector store on disk

CHAT_MODEL = "kimi-k2.5:cloud "
EMBED_MODEL = "embeddinggemma:latest"

# Ollama default base url is http://127.0.0.1:11434
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")


def load_documents(docs_dir: Path):
    """
    Loads .md and .txt files from docs_dir, returning LangChain Document objects.
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

    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    return docs


def build_or_load_vectorstore(docs_dir: Path, chroma_dir: Path) -> Chroma:
    """
    Creates a Chroma index on first run, then loads it from disk on later runs.
    """
    embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)

    if chroma_dir.exists():
        return Chroma(
            persist_directory=str(chroma_dir),
            embedding_function=embeddings,
        )

    raw_docs = load_documents(docs_dir)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
    )
    chunks = splitter.split_documents(raw_docs)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(chroma_dir),
    )
    vectordb.persist()
    return vectordb


def format_context(docs) -> Tuple[str, List[str]]:
    """
    Builds a context string and a list of human citations from retrieved docs.
    """
    citations = []
    parts = []
    for i, d in enumerate(docs, start=1):
        src = d.metadata.get("source", "unknown_source")
        citations.append(f"[{i}] {src}")
        parts.append(f"Source [{i}] ({src})\n{d.page_content}")
    return "\n\n".join(parts), citations


def answer_question(vectordb: Chroma, question: str) -> str:
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    retrieved = retriever.get_relevant_documents(question)

    context, citations = format_context(retrieved)

    llm = ChatOllama(model=CHAT_MODEL, base_url=OLLAMA_BASE_URL)

    prompt = (
        "You are answering questions using the provided project documents.\n"
        "Use the context to answer. If the context does not contain the answer, say you do not know.\n"
        "Cite sources using bracket numbers like [1] or [2].\n\n"
        f"Question:\n{question}\n\n"
        f"Context:\n{context}\n"
    )

    response = llm.invoke(prompt)
    text = response.content if hasattr(response, "content") else str(response)

    cites_block = "Sources:\n" + "\n".join(citations)
    return f"{text}\n\n{cites_block}"


if __name__ == "__main__":
    if not DOCS_DIR.exists():
        raise SystemExit(f"Docs folder not found: {DOCS_DIR.resolve()}")

    db = build_or_load_vectorstore(DOCS_DIR, CHROMA_DIR)

    while True:
        q = input("\nAsk a question (or type exit): ").strip()
        if q.lower() == "exit":
            break
        print("\n" + answer_question(db, q))