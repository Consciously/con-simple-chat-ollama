"""FastAPI Scaffold for LLM Container Base

This is an optional, minimal FastAPI application that provides a clean REST API
interface. It's designed to be easily activated when needed without interfering
with the container's default behavior.

To start the API server:
    uvicorn backend.api_scaffold:app --host 0.0.0.0 --port 8000

The scaffold includes:
- Single /ask POST endpoint
- JSON request/response handling
- Basic error handling
- Health check endpoint

NOTE: This is a template/scaffold. The main service is in ask_model.py
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# Initialize FastAPI app
app = FastAPI(
    title="LLM Container API Scaffold",
    description="Minimal REST API for LLM interactions",
    version="1.0.0"
)


# Request/Response models
class AskRequest(BaseModel):
    prompt: str
    model_name: str = "default-model"


class AskResponse(BaseModel):
    response: str
    model_used: str


# Main API endpoint
@app.post("/ask", response_model=AskResponse)
async def ask_llm(request: AskRequest) -> AskResponse:
    """
    Process a prompt and return a response from the specified model.
    
    This is a dummy implementation that echoes the prompt.
    Replace this with actual LLM integration when ready.
    """
    try:
        # Dummy response - replace with actual LLM call
        dummy_response = f"Echo from {request.model_name}: {request.prompt}"
        
        return AskResponse(
            response=dummy_response,
            model_used=request.model_name
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "healthy", "service": "llm-api-scaffold"}


# Root endpoint
@app.get("/")
async def root() -> Dict[str, Any]:
    """API information endpoint."""
    return {
        "name": "LLM Container API Scaffold",
        "version": "1.0.0",
        "endpoints": {
            "ask": "POST /ask - Send prompts to LLM",
            "health": "GET /health - Health check",
            "docs": "GET /docs - Interactive API documentation"
        }
    }
