from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rag.chatbot import RAGChatbot

app = FastAPI(
    title="E-Commerce AI Assistant",
    description="RAG chatbot using PostgreSQL, Pinecone and Ollama",
    version="1.0.0",
)

# React frontend will run on localhost:5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading RAG chatbot...")
chatbot = RAGChatbot(top_k=5)
print("RAG chatbot ready.")

class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    answer: str

@app.get("/")
def root():
    return {
        "message": "E-Commerce AI Assistant API",
        "status": "running",
    }

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
    }

@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = chatbot.ask(
        request.question
    )

    return {
         "question": result["question"],
         "answer": result["answer"],
    }    

