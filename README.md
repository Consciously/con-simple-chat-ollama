# Ollama LLM Container Base

A clean, reusable base container for running Ollama-powered LLMs locally with optional REST API for remote access and integration.

## Features

* **🐍 Direct Python API**: Utilize the container as a Python library for seamless model inference within your scripts.
* **🚀 FastAPI Integration**: Optional REST API endpoint for chat interactions, health checks, and metrics.
* **📦 pyproject.toml Setup**: Declarative dependency management using Poetry or any `pyproject.toml` compatible tool.
* **🔄 Multi-Stage Docker Builds**: Optimized image layers for faster builds and smaller runtimes.
* **🧪 Test Scripts**: Example scripts in `scripts/` for quick smoke tests and demos.

## Folder Structure

```
/
├── README.md           # Project overview and instructions
├── pyproject.toml      # Python project & dependencies configuration
├── docker-compose.yml  # Orchestration for backend & optional proxy
├── Dockerfile          # Multi-stage Docker build for the backend service
├── api/                # FastAPI application code
│   └── main.py         # Entry point for API service
├── scripts/            # Utility scripts for testing and development
│   └── ask_model.py    # Example script to test model inference
└── models/             # Optional: custom models or embeddings
```

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone <repo-url> && cd <project-folder>
   ```

2. **Configure environment variables:**

   Copy `.env.example` to `.env` and adjust values:

   ```env
   MODEL_NAME=mistral
   API_PORT=8000
   ```

3. **Build and run with Docker Compose:**

   ```bash
   docker-compose up --build
   ```

4. **Use the Python API:**

   ```python
   from container_base import OllamaClient

   client = OllamaClient(model_name="mistral")
   response = client.chat("Hello world")
   print(response)
   ```

5. **Interact via REST API:**

   * `POST /chat` with JSON payload `{ "prompt": "Hello" }`
   * `GET /health` for service status

## Command Line Examples

```bash
python -m backend.ask_model  # was python -m app.ask_model
python -m backend.ask_model  # was python -m app.ask_model
python -m backend.ask_model  # was python -m app.ask_model
```

## API Extensions

Modify `backend/ask_model.py` to adjust prompt handling and logging.

## Project Setup Examples

```bash
mkdir -p backend/your_module  # was mkdir -p app/your_module
touch backend/your_module/__init__.py  # was touch app/your_module/__init__.py
touch backend/your_module/main.py  # was touch app/your_module/main.py
```

## Code Examples

```python
# backend/agent/main.py  # was # app/agent/main.py
# backend/rag/main.py    # was # app/rag/main.py
# backend/custom_api.py  # was # app/custom_api.py
```

## Project Structure

```
/
├── README.md
├── pyproject.toml
├── docker-compose.yml
├── Dockerfile
├── api/
│   └── main.py
├── backend/       # was app/
│   └── ask_model.py
├── scripts/
│   └── ask_model.py
└── models/
```

## Template Maintenance

```bash
git checkout template/main -- backend/ask_model.py  # was git checkout template/main -- app/ask_model.py
```

## Example Projects

```bash
# Add your agent code in backend/agent/  # was # Add your agent code in app/agent/
mkdir -p backend/rag data/documents tests/rag  # was mkdir -p app/rag data/documents tests/rag
```

## Contributing

Contributions welcome! Please open issues or pull requests.

## License

This project is licensed under the MIT License.
