# Multi-stage build for clean, lightweight Ollama + Python container
FROM python:3.12-slim as base

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        procps \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
RUN UV_UNMANAGED_INSTALL=1 curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:/root/.cargo/bin:${PATH}"

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Create working directory
WORKDIR /app

# ─────────────────────────────
# Install Python dependencies
# ─────────────────────────────
COPY pyproject.toml ./
COPY requirements.lock ./

RUN if [ -s requirements.lock ]; then \
        echo "Using requirements.lock for dependency installation" && \
        uv pip sync requirements.lock; \
    else \
        echo "No requirements.lock found, installing from pyproject.toml..." && \
        uv pip install --system .; \
    fi

# Copy application code
COPY app ./app
COPY scripts ./scripts

# Create directories for Ollama
RUN mkdir -p /root/.ollama

# Environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_PORT=11434
ENV OLLAMA_MODELS=/root/.ollama/models
ENV DEFAULT_MODEL=llama3.2:1b

# Expose ports
EXPOSE 8000 11434

# Copy startup script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Default command: start both Ollama and FastAPI
ENTRYPOINT ["/entrypoint.sh"]
CMD ["api"]