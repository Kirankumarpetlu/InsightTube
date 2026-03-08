"""
InsightTube AI Backend - FastAPI Server
Main entry point for the YouTube video analysis chatbot API.
"""

import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.coordinator_agent import handle_message


# --- FastAPI App ---
app = FastAPI(
    title="InsightTube AI",
    description="AI-powered YouTube video analysis chatbot using Groq LLM",
    version="1.0.0",
)

# --- CORS Middleware ---
# Allow the Lovable frontend (localhost:8080) and common dev origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "*",  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request/Response Models ---
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


# --- Endpoints ---
@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "running",
        "service": "InsightTube AI Backend",
        "version": "1.0.0",
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint. Accepts a user message and returns an AI response.
    
    - If the message contains a YouTube URL, the video is analyzed
      (transcript extraction → LLM analysis → structured response).
    - Otherwise, a conversational response is generated using Groq LLM.
    """
    # Validate input
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty. Please provide a valid message.",
        )
    
    try:
        # Process the message through the coordinator agent
        response_text = handle_message(request.message.strip())
        return ChatResponse(response=response_text)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}",
        )


# --- Run with: uvicorn main:app --reload ---
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
