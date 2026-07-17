# this is the ingestion pipline for the RAG system


from langchain_community.document_loaders import TextLoader,DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os
import sys

# Ensure print statements can output utf-8 (like emojis) on Windows
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

# 1 load the document

def load_document(docs_path="docs"):
    # Get absolute path of docs directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_docs_path = os.path.join(script_dir, docs_path)
    
    # check if directory exists
    if not os.path.exists(absolute_docs_path):
       raise FileNotFoundError(f"Data directory not found at: {absolute_docs_path}")
    

    loader = DirectoryLoader(
        path = absolute_docs_path, 
        glob="*.txt", 
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
        )
    documents = loader.load()
    print(f"Loaded {len(documents)} documents")

    if len(documents) == 0:
        raise ValueError("No documents found")  

    for i , doc in enumerate(documents[:2]):
        print("\n")
        print(f"Document {i+1}: {doc.metadata}")
        print("\n")
        print(f" content length: {len(doc.page_content)}    ")
        print("\n")
        print(f"metadata: {doc.metadata}")
        print("\n")
        print(f"Document {i+1}: {doc.page_content[:100]}")

    return documents



# 2 split the document into chunks

def split_document(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_documents(documents)

    
    print(f"Split {len(chunks)} chunks")
    return chunks


# 3 create embeddings

def create_embeddings():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )
    return embeddings


# 4 create a Chroma vector store

def create_vector_store(chunks, embeddings):
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="vector_store"
    )
    return vector_store
 


# main function
def main():
#    this contains the whole pipline
#    1. Load the document
    documents = load_document(docs_path="docs") 
#    2. Split the document into chunks
    chunks = split_document(documents)

#    3. Create embeddings
    embeddings = create_embeddings()
#    4. Create a Chroma vector store
    vector_store = create_vector_store(chunks, embeddings)

if __name__ == "__main__":
    main()
    