"""Retrieval pipeline: search the vector store and generate an answer with Gemini."""

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

import config

load_dotenv()

SYSTEM_PROMPT = "You are a helpful assistant."

RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "user",
            """Based on the following context, answer the query.

Context:
{context}

Query:
{query}

Provide a clear and concise answer based on the context. If the answer is not in the context, say so.""",
        ),
    ]
)


def load_vector_store() -> Chroma:
    """Load the persisted Chroma vector store."""
    if not config.VECTOR_STORE_DIR.exists():
        raise FileNotFoundError(
            f"Vector store not found at: {config.VECTOR_STORE_DIR}. "
            "Run the ingestion pipeline first."
        )

    embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL)

    return Chroma(
        persist_directory=str(config.VECTOR_STORE_DIR),
        embedding_function=embeddings,
        collection_metadata={"hnsw:space": "cosine"},
    )


def retrieve_documents(vector_store: Chroma, query: str, k: int = config.RETRIEVAL_K) -> list:
    """Retrieve the top-k relevant document chunks for a query."""
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    return retriever.invoke(query)


def create_llm() -> ChatGoogleGenerativeAI:
    """Create the Gemini chat model."""
    return ChatGoogleGenerativeAI(
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
    )


def generate_answer(query: str, relevant_docs: list, llm: ChatGoogleGenerativeAI) -> str:
    """Generate an answer from retrieved context and the user query."""
    context = "\n\n".join(doc.page_content for doc in relevant_docs)
    messages = RAG_PROMPT.format_messages(context=context, query=query)
    response = llm.invoke(messages)
    return response.content


def print_retrieved_documents(query: str, relevant_docs: list) -> None:
    """Print retrieved chunks for inspection."""
    print(f"User query: {query}\n")

    for index, doc in enumerate(relevant_docs, start=1):
        print(f"Document {index}: {doc.metadata}")
        print(f"Content: {doc.page_content}\n")


def run_retrieval_pipeline(query: str = config.DEFAULT_QUERY) -> str:
    """Run retrieval and generation, returning the model response."""
    vector_store = load_vector_store()
    relevant_docs = retrieve_documents(vector_store, query)
    print_retrieved_documents(query, relevant_docs)

    llm = create_llm()
    answer = generate_answer(query, relevant_docs, llm)

    print("Generated response:\n")
    print(answer)
    return answer


def main() -> None:
    run_retrieval_pipeline()


if __name__ == "__main__":
    main()
