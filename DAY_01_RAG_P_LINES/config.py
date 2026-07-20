"""Shared configuration for the Day 01 RAG pipelines."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"

EMBEDDING_MODEL = "gemini-embedding-001"
LLM_MODEL = "gemini-3.5-flash"
LLM_TEMPERATURE = 0.7

CHUNK_SIZE = 400
CHUNK_OVERLAP = 80
RETRIEVAL_K = 3

DEFAULT_QUERY = (
    "what are the topics discussed in phase 1 of ai generalist?"
)
