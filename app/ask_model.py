"""ask_model.py
A lightweight module that provides two interfaces to a local Ollama LLM service:

1. HTTP API via FastAPI (so the container can expose an endpoint)
2. Command-line interface allowing quick interactive calls during development

Both interfaces rely on the same `generate_response` helper, which integrates
with Ollama to provide real LLM inference capabilities.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict

import ollama
from fastapi import FastAPI, HTTPException, Request
from loguru import logger
from pydantic import BaseModel

app = FastAPI(title="Ollama LLM Container", version="0.2.0")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "localhost")
OLLAMA_PORT = os.getenv("OLLAMA_PORT", "11434")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama3.2:1b")

# Initialize Ollama client
ollama_client = ollama.Client(host=f"http://{OLLAMA_HOST}:{OLLAMA_PORT}")

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
# Remove default handler and add our own with colorized output to stderr.
logger.remove()
logger.add(
    sys.stderr, 
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
    colorize=True  # Force colors even in non-TTY
)


# ---------------------------------------------------------------------------
# Logging middleware
# ---------------------------------------------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):  # noqa: D401
    """Log each incoming request with method, path, status and latency."""

    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "{method} {path} -> {status} {duration:.2f}ms",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration=duration_ms,
    )
    return response


# ---------------------------------------------------------------------------
# Core inference helper
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    model: str
    prompt: str


class GenerateResponse(BaseModel):
    response: str


def generate_response(model: str, prompt: str) -> str:  # noqa: D401
    """Return a model response using Ollama.

    Connects to the local Ollama service to generate responses using the specified model.
    Falls back to DEFAULT_MODEL if the requested model is not available.
    """
    try:
        # Use default model if none specified or if model is "local-model" (legacy)
        if not model or model == "local-model":
            model = DEFAULT_MODEL
        
        # Check if model is available, if not try to pull it
        try:
            available_models = [m['name'] for m in ollama_client.list()['models']]
            if model not in available_models:
                logger.warning(f"Model '{model}' not found locally. Attempting to pull...")
                ollama_client.pull(model)
        except Exception as e:
            logger.warning(f"Could not check/pull model '{model}': {e}. Using default model.")
            model = DEFAULT_MODEL
        
        # Generate response
        logger.info(f"Generating response using model: {model}")
        response = ollama_client.generate(
            model=model,
            prompt=prompt,
            stream=False
        )
        
        return response['response']
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        # Fallback response
        return f"Error: Unable to generate response using model '{model}'. {str(e)}"


# ---------------------------------------------------------------------------
# HTTP routes
# ---------------------------------------------------------------------------

@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest) -> GenerateResponse:  # noqa: D401
    """FastAPI endpoint that proxies to :pyfunc:`generate_response`."""

    try:
        answer = generate_response(req.model, req.prompt)
    except Exception as exc:  # pragma: no cover – catch-all for user errors
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return GenerateResponse(response=answer)


# Alias endpoint to comply with API design guidelines --------------------------------
# The new /ask route behaves identically to /generate but follows a clearer naming
# convention requested by users. Maintaining both endpoints preserves backward
# compatibility for any tooling that may already rely on /generate.

@app.post("/ask", response_model=GenerateResponse)
async def ask(req: GenerateRequest) -> GenerateResponse:  # noqa: D401
    """FastAPI endpoint that mirrors :pyfunc:`generate` for compatibility."""

    return await generate(req)


@app.get("/")
async def root() -> Dict[str, str]:  # noqa: D401
    """Basic health check endpoint."""

    return {"message": "Ollama LLM container is up"}


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def _parse_cli(argv: list[str] | None = None) -> argparse.Namespace:  # noqa: D401
    parser = argparse.ArgumentParser(description="Query the running Ollama LLM")
    parser.add_argument("prompt", help="Prompt to send to the model")
    parser.add_argument(
        "--model",
        default="local-model",
        help="Model identifier (default: %(default)s)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output response as JSON for scripting purposes",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:  # noqa: D401
    """CLI wrapper around :pyfunc:`generate_response`."""

    args = _parse_cli(argv)
    answer = generate_response(args.model, args.prompt)

    if args.json:
        print(json.dumps({"response": answer}, ensure_ascii=False))
    else:
        print(answer)


if __name__ == "__main__":  # pragma: no cover
    # Pass through sys.argv[1:] to keep behaviour consistent when invoked as
    # `python -m app.ask_model ...` as well as `python app/ask_model.py ...`.
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:  # graceful exit on Ctrl-C
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)