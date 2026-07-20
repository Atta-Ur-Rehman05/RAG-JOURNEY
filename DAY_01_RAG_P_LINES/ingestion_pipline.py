"""Ingestion pipeline: load documents, chunk, embed, and persist to Chroma."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

import config

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()


def load_documents(docs_path: Path | None = None) -> list:
    """Load all `.txt` files from the docs directory."""
    docs_dir = docs_path or config.DOCS_DIR

    if not docs_dir.exists():
        raise FileNotFoundError(f"Data directory not found at: {docs_dir}")

    loader = DirectoryLoader(
        path=str(docs_dir),
        glob="*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} documents")

    if not documents:
        raise ValueError("No documents found")

    for index, doc in enumerate(documents[:2], start=1):
        preview = doc.page_content[:100]
        print(f"\nDocument {index} metadata: {doc.metadata}")
        print(f"Content length: {len(doc.page_content)}")
        print(f"Preview: {preview}...")

    return documents


def split_documents(documents: list) -> list:
    """Split documents into overlapping chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks


def create_embeddings() -> GoogleGenerativeAIEmbeddings:
    """Create the Google Generative AI embedding model."""
    return GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )


def create_vector_store(chunks: list, embeddings: GoogleGenerativeAIEmbeddings) -> Chroma:
    """Persist document chunks in a Chroma vector store."""
    config.VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(config.VECTOR_STORE_DIR),
    )


def run_ingestion_pipeline(docs_path: Path | None = None) -> Chroma:
    """Run the full ingestion pipeline and return the vector store."""
    documents = load_documents(docs_path)
    chunks = split_documents(documents)
    embeddings = create_embeddings()
    vector_store = create_vector_store(chunks, embeddings)

    print(f"Vector store saved to: {config.VECTOR_STORE_DIR}")
    return vector_store


def main() -> None:
    run_ingestion_pipeline()


if __name__ == "__main__":
    main()
