#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

# Function to start Ollama service
start_ollama() {
    log "Starting Ollama service..."
    ollama serve &
    OLLAMA_PID=$!
    
    # Wait for Ollama to be ready
    log "Waiting for Ollama to be ready..."
    for i in {1..30}; do
        if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
            log "Ollama is ready!"
            break
        fi
        if [ $i -eq 30 ]; then
            error "Ollama failed to start within 30 seconds"
            exit 1
        fi
        sleep 1
    done
}

# Function to pull default model if specified
pull_default_model() {
    if [ -n "$DEFAULT_MODEL" ]; then
        log "Checking if default model '$DEFAULT_MODEL' is available..."
        if ! ollama list | grep -q "$DEFAULT_MODEL"; then
            log "Pulling default model: $DEFAULT_MODEL"
            ollama pull "$DEFAULT_MODEL"
        else
            log "Default model '$DEFAULT_MODEL' already available"
        fi
    fi
}

# Function to start FastAPI
start_api() {
    log "Starting FastAPI server..."
    exec python -m uvicorn app.ask_model:app --host 0.0.0.0 --port 8000
}

# Function to run interactive shell
run_shell() {
    log "Starting interactive shell..."
    exec /bin/bash
}

# Function to run Python script
run_python() {
    log "Running Python script: $1"
    shift
    exec python "$@"
}

# Main execution logic
case "${1:-api}" in
    "api")
        log "Starting in API mode..."
        start_ollama
        pull_default_model
        start_api
        ;;
    "ollama-only")
        log "Starting Ollama service only..."
        start_ollama
        log "Ollama is running. Container will keep running..."
        wait $OLLAMA_PID
        ;;
    "shell")
        log "Starting in shell mode..."
        start_ollama
        pull_default_model
        run_shell
        ;;
    "python")
        log "Starting in Python mode..."
        start_ollama
        pull_default_model
        run_python "$@"
        ;;
    *)
        log "Starting custom command: $*"
        start_ollama
        pull_default_model
        exec "$@"
        ;;
esac
