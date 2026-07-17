# this is the retrieval pipline for the RAG system


from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

persist_directory = "vector_store"

# load embeddings and vector store

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
   
)

db = Chroma(
    persist_directory=persist_directory,
    embedding_function=embeddings,
    collection_metadata={"hnsw:space": "cosine"}
    )

# search the vector store

query = "what are the technical requirements for task manager?"





retriever = db.as_retriever(search_kwargs={"k": 3})

relevant_docs = retriever.invoke(query)
print(f"user query: {query}")

# display results

for i, doc in enumerate(relevant_docs):
    print(f"Document {i+1}: {doc.metadata}")
    print(f"Content: {doc.page_content}")


# synthetic data for testing
# """
# ✅ Task Manager — Functional Feature Checklist

# 🔐 User Authentication
# User Registration (create account with name, email, password)
# User Login (secure sign-in with email & password)
# User Logout (secure session termination & cookie clearing)
# Persistent Session (JWT stored in HTTP-only cookies)
# Auth Guard (redirect unauthenticated users to login/register)

# 🗂️ Task Management
# Task Creation (title, description, due date, priority, tags)
# Task Editing (update task details via modal interface)
# Task Completion Toggle (Todo ↔ Completed with live updates)
# Task Deletion (remove tasks permanently)
# Task Persistence (stored in local storage for browser persistence)

# 🧭 Navigation & Organization
# Smart Filters (Today, Upcoming, Completed)
# Global Search (search tasks by title or description)
# Task Counting (dynamic sidebar badges per category)
# Project Categorization (group tasks by project/context)

# 📊 Dashboard & Analytics
# Task Statistics (daily/weekly/monthly completion counts)
# Priority Distribution (visual breakdown of task priorities)
# Streak Tracking (consecutive days of task completion)
# Progress Charts (visualize task completion trends over time)

# 🌙 UI/UX Features
# Dark Mode / Light Mode Toggle
# Responsive Design (mobile, tablet, desktop support)
# Toast Notifications (for task creation, updates, deletion)
# Empty State Illustrations (for no tasks, no search results)

# 🛠️ Technical Requirements
# Frontend: React + Vite
# Backend: Node.js + Express
# Database: MongoDB (local)
# Authentication: JWT + bcrypt
# State Management: React Context API
# Styling: Tailwind CSS
# Deployment: Localhost only (no production deployment)
# """