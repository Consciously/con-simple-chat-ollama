# Ollama LLM Container Base

A clean, reusable base container setup for local LLM experiments using Ollama. This template provides a lightweight, extendable foundation that runs selected LLMs locally, exposes them via an optional FastAPI interface, and allows direct Python-based interaction for scripts and tools.

## 🚀 Features

- **🦙 Ollama Integration**: Full Ollama setup with automatic model management
- **⚡ FastAPI Interface**: Optional REST API for remote access and integration
- **🐍 Direct Python Access**: Scripts for direct LLM interaction without API overhead
- **📦 Modern Package Management**: Uses `uv` for fast, reliable dependency management
- **🔧 Multiple Run Modes**: API server, interactive shell, Ollama-only, or custom commands
- **📊 Structured Logging**: Colorized request logging with Loguru
- **🔄 Auto Model Pulling**: Automatically downloads specified models on first run
- **🎯 Minimal Configuration**: Sensible defaults with easy customization

## 📋 Quick Start

### 1. Basic API Server

```bash
# Build and start the container with FastAPI + Ollama
docker-compose up llm-container

# Test the API
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2:1b", "prompt": "Hello, world!"}'
```

### 2. Interactive Development

```bash
# Start development environment with shell access
docker-compose --profile dev up llm-dev

# In another terminal, connect to the container
docker-compose exec llm-dev bash

# Run example scripts
python scripts/example_direct.py
python scripts/example_api.py
```

### 3. Ollama-Only Mode

```bash
# Run just Ollama service (no FastAPI)
docker-compose --profile ollama up ollama-only

# Access Ollama directly
curl http://localhost:11436/api/generate \
  -d '{"model": "llama3.2:1b", "prompt": "Explain containers"}'
```

## 🛠️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEFAULT_MODEL` | `llama3.2:1b` | Default LLM model to use |
| `OLLAMA_HOST` | `0.0.0.0` | Ollama server host |
| `OLLAMA_PORT` | `11434` | Ollama server port |

### Available Models

The container supports any model available in Ollama. Popular options:

- `llama3.2:1b` - Fast, lightweight (1.3GB)
- `llama3.2:3b` - Balanced performance (2.0GB)
- `llama3.1:8b` - High quality (4.7GB)
- `codellama:7b` - Code-focused (3.8GB)
- `mistral:7b` - Alternative architecture (4.1GB)

Models are automatically pulled on first use.

## 🎯 Usage Examples

### Command Line Interface

```bash
# Direct CLI usage
docker run --rm con-llm-container python -m app.ask_model "What is Docker?"

# With custom model
docker run --rm con-llm-container python -m app.ask_model \
  --model llama3.1:8b "Explain machine learning"

# JSON output for scripting
docker run --rm con-llm-container python -m app.ask_model \
  --json "List three programming languages"
```

### FastAPI Endpoints

#### POST `/ask`
```json
{
  "model": "llama3.2:1b",
  "prompt": "Your question here"
}
```

#### POST `/generate` (Legacy)
Same as `/ask` - maintained for backward compatibility.

#### GET `/`
Health check and service information.

### Python Scripts

#### Direct Ollama Interaction
```python
import ollama

client = ollama.Client(host="http://localhost:11434")
response = client.generate(
    model="llama3.2:1b",
    prompt="Explain containerization",
    stream=False
)
print(response['response'])
```

#### API Client
```python
import requests

response = requests.post("http://localhost:8000/ask", json={
    "model": "llama3.2:1b",
    "prompt": "What is the meaning of life?"
})
print(response.json()['response'])
```

## 🔧 Development

### Local Development Setup

```bash
# Clone and enter directory
git clone <repository>
cd con-llm-container-base

# Install dependencies with uv
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -e .

# Start development environment
docker-compose --profile dev up llm-dev
```

### Adding New Dependencies

```bash
# Add to pyproject.toml, then regenerate lock file
uv pip compile pyproject.toml -o requirements.lock
```

### Running Tests

```bash
# In development container
python scripts/example_direct.py
python scripts/example_api.py

# Or run specific tests
python -m pytest tests/  # If you add tests
```

## 🏗️ Container Run Modes

The container supports multiple execution modes via the entrypoint:

### API Mode (Default)
```bash
docker run -p 8000:8000 -p 11434:11434 con-llm-container api
```
Starts both Ollama and FastAPI services.

### Shell Mode
```bash
docker run -it con-llm-container shell
```
Interactive shell with Ollama running in background.

### Ollama-Only Mode
```bash
docker run -p 11434:11434 con-llm-container ollama-only
```
Just the Ollama service, no FastAPI.

### Python Script Mode
```bash
docker run con-llm-container python scripts/example_direct.py
```
Run custom Python scripts with Ollama available.

### Custom Command Mode
```bash
docker run con-llm-container your-custom-command
```
Run any custom command with Ollama started first.

## 🔌 Extending the Container

### Adding New Models

1. **Environment Variable**:
   ```bash
   docker run -e DEFAULT_MODEL=codellama:7b con-llm-container
   ```

2. **Pre-pull in Dockerfile**:
   ```dockerfile
   RUN ollama pull codellama:7b
   ```

### Custom Python Scripts

1. Add scripts to the `scripts/` directory
2. Mount as volume: `-v ./my-scripts:/app/scripts`
3. Run: `docker run con-llm-container python scripts/my-script.py`

### API Extensions

Modify `app/ask_model.py` to add new endpoints:

```python
@app.post("/custom-endpoint")
async def custom_function(request: CustomRequest):
    # Your custom logic here
    return custom_response
```

### Model-Specific Configurations

Create model-specific configurations:

```python
# In your scripts
MODEL_CONFIGS = {
    "codellama:7b": {"temperature": 0.1, "top_p": 0.9},
    "llama3.1:8b": {"temperature": 0.7, "top_p": 0.95},
}
```

## 📊 Performance Tips

1. **Model Size**: Start with smaller models (`llama3.2:1b`) for development
2. **Memory**: Ensure adequate RAM (4GB+ for 3B models, 8GB+ for 7B models)
3. **Storage**: Models are cached in volumes for faster subsequent starts
4. **GPU**: For GPU acceleration, use Ollama's GPU-enabled images

## 🐛 Troubleshooting

### Common Issues

**Container fails to start**:
- Check available memory (models require significant RAM)
- Verify Docker has sufficient resources allocated

**Model download fails**:
- Check internet connection
- Verify model name exists in Ollama registry

**API not responding**:
- Wait for Ollama to fully start (check logs)
- Verify ports are not already in use

**Permission errors**:
- Ensure Docker has proper permissions
- Check volume mount permissions

### Debugging

```bash
# Check container logs
docker-compose logs llm-container

# Connect to running container
docker-compose exec llm-container bash

# Check Ollama status
curl http://localhost:11434/api/tags

# Test API directly
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2:1b", "prompt": "test"}'
```

## 📄 License

This project is open source. See LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

---

**Happy experimenting with local LLMs! 🦙✨**

## 📋 Using This Repository as a Template

This repository is designed to be a **reusable template** for creating custom LLM-powered applications. Whether you're building agents, RAG systems, evaluation frameworks, or specialized LLM tools, this template provides a solid foundation.

### 🎯 Template Use Cases

- **🤖 AI Agents**: Build autonomous agents with tool integration
- **📚 RAG Systems**: Create document-based question answering systems
- **🧪 LLM Evaluation**: Develop model testing and benchmarking tools
- **🔧 Custom LLM Tools**: Build specialized applications with local LLM access
- **📊 Data Processing**: Create LLM-powered data analysis pipelines
- **🎓 Research Projects**: Prototype and experiment with LLM capabilities

### 🚀 Quick Template Setup

#### 1. Create New Project from Template

```bash
# Option A: Use GitHub template (if this is a GitHub repo)
# Click "Use this template" button on GitHub

# Option B: Clone and customize
git clone https://github.com/your-username/con-llm-container-base.git my-llm-project
cd my-llm-project
rm -rf .git
git init
```

#### 2. Customize for Your Project

```bash
# Update project metadata
vim pyproject.toml  # Change name, description, author
vim README.md       # Update title and description
vim docker-compose.yml  # Adjust service names if needed
```

#### 3. Add Your Custom Code

```bash
# Add your application logic
mkdir -p app/your_module
touch app/your_module/__init__.py
touch app/your_module/main.py

# Add custom scripts
touch scripts/your_custom_script.py

# Add tests
mkdir -p tests
touch tests/test_your_module.py
```

### 🔧 Common Customization Patterns

#### **Agent Development Template**

```python
# app/agent/main.py
import ollama
from typing import List, Dict, Any

class LLMAgent:
    def __init__(self, model: str = "llama3.2:1b"):
        self.client = ollama.Client(host="http://localhost:11434")
        self.model = model
        self.tools = {}
    
    def add_tool(self, name: str, func: callable):
        """Add a tool that the agent can use"""
        self.tools[name] = func
    
    def execute(self, prompt: str) -> str:
        """Execute agent with tool access"""
        # Your agent logic here
        response = self.client.generate(
            model=self.model,
            prompt=f"Tools available: {list(self.tools.keys())}\n{prompt}",
            stream=False
        )
        return response['response']
```

#### **RAG System Template**

```python
# app/rag/main.py
import ollama
from typing import List

class RAGSystem:
    def __init__(self, model: str = "llama3.2:1b"):
        self.client = ollama.Client(host="http://localhost:11434")
        self.model = model
        self.documents = []
    
    def add_documents(self, docs: List[str]):
        """Add documents to the knowledge base"""
        self.documents.extend(docs)
    
    def query(self, question: str) -> str:
        """Query the RAG system"""
        # Simple retrieval (enhance with vector search)
        context = "\n".join(self.documents[:3])  # Top 3 docs
        
        prompt = f"""Context: {context}
        
Question: {question}

Answer based on the context provided:"""
        
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            stream=False
        )
        return response['response']
```

#### **Custom FastAPI Endpoints**

```python
# app/custom_api.py
from fastapi import FastAPI
from pydantic import BaseModel
import ollama

app = FastAPI()
client = ollama.Client(host="http://localhost:11434")

class CustomRequest(BaseModel):
    text: str
    task_type: str  # "summarize", "translate", "analyze"

@app.post("/process")
async def process_text(request: CustomRequest):
    """Custom text processing endpoint"""
    
    prompts = {
        "summarize": f"Summarize this text: {request.text}",
        "translate": f"Translate to Spanish: {request.text}",
        "analyze": f"Analyze the sentiment: {request.text}"
    }
    
    prompt = prompts.get(request.task_type, request.text)
    
    response = client.generate(
        model="llama3.2:1b",
        prompt=prompt,
        stream=False
    )
    
    return {"result": response['response'], "task": request.task_type}
```

### 📁 Recommended Project Structure

```
my-llm-project/
├── app/
│   ├── __init__.py
│   ├── ask_model.py          # Keep base functionality
│   ├── your_module/          # Your custom module
│   │   ├── __init__.py
│   │   ├── main.py          # Core logic
│   │   └── utils.py         # Helper functions
│   └── api/                 # Custom API endpoints
│       ├── __init__.py
│       └── custom_routes.py
├── scripts/
│   ├── example_direct.py    # Keep examples
│   ├── example_api.py
│   └── your_script.py       # Your custom scripts
├── tests/
│   ├── __init__.py
│   ├── test_base.py         # Test base functionality
│   └── test_your_module.py  # Test your code
├── data/                    # For RAG/training data
│   └── documents/
├── config/                  # Configuration files
│   └── models.yaml
├── Dockerfile               # Customize as needed
├── docker-compose.yml       # Adjust services
├── pyproject.toml          # Update dependencies
└── README.md               # Document your project
```

### 🔄 Template Maintenance

#### **Keep Base Template Updated**

```bash
# Add original template as upstream remote
git remote add template https://github.com/original/con-llm-container-base.git

# Fetch updates from template
git fetch template

# Merge template updates (resolve conflicts as needed)
git merge template/main
```

#### **Selective Updates**

```bash
# Cherry-pick specific improvements
git cherry-pick <commit-hash>

# Update specific files only
git checkout template/main -- docker/entrypoint.sh
git checkout template/main -- app/ask_model.py
```

### 🎨 Environment Customization

#### **Development Environment**

```yaml
# docker-compose.override.yml (for local development)
version: '3.8'
services:
  llm-container:
    environment:
      - DEFAULT_MODEL=codellama:7b  # Use code-focused model
      - OLLAMA_DEBUG=true
    volumes:
      - ./data:/app/data           # Mount your data
      - ./config:/app/config       # Mount configuration
    ports:
      - "8080:8000"               # Different port to avoid conflicts
```

#### **Production Environment**

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  llm-container:
    environment:
      - DEFAULT_MODEL=llama3.1:8b  # Production model
      - OLLAMA_KEEP_ALIVE=30m      # Longer keep-alive
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 16G              # Adequate memory
        reservations:
          memory: 8G
```

### 📚 Example Project Templates

#### **Minimal Agent Project**

```bash
# Quick setup for agent development
mkdir my-agent && cd my-agent
curl -O https://raw.githubusercontent.com/your-repo/con-llm-container-base/main/Dockerfile
curl -O https://raw.githubusercontent.com/your-repo/con-llm-container-base/main/docker-compose.yml
# Add your agent code in app/agent/
```

#### **RAG Research Project**

```bash
# Setup for RAG experiments
git clone con-llm-container-base rag-research
cd rag-research
mkdir -p app/rag data/documents tests/rag
# Implement RAG components
```

#### **Multi-Model Evaluation**

```bash
# Setup for model comparison
git clone con-llm-container-base model-eval
cd model-eval
# Modify docker-compose.yml to support multiple models
# Add evaluation scripts in scripts/eval/
```

### 🚀 Deployment Options

#### **Single Container Deployment**

```bash
# Build and deploy your custom container
docker build -t my-llm-app .
docker run -d -p 8080:8000 -p 11434:11434 my-llm-app
```

#### **Docker Swarm/Kubernetes**

```yaml
# kubernetes-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-llm-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-llm-app
  template:
    metadata:
      labels:
        app: my-llm-app
    spec:
      containers:
      - name: llm-container
        image: my-llm-app:latest
        ports:
        - containerPort: 8000
        - containerPort: 11434
        resources:
          requests:
            memory: "4Gi"
          limits:
            memory: "8Gi"
```

### 💡 Best Practices for Template Usage

1. **🔒 Keep Secrets Secure**: Use environment variables for API keys and sensitive data
2. **📝 Document Changes**: Maintain clear documentation of your customizations
3. **🧪 Test Thoroughly**: Add tests for your custom functionality
4. **🔄 Version Control**: Tag releases and maintain changelog
5. **📊 Monitor Performance**: Add logging and metrics for your custom components
6. **🛡️ Security**: Review and update dependencies regularly

---

This template provides a robust foundation - customize it to build amazing LLM-powered applications! 🚀

## 📊 Performance Tips
1. **Model Size**: Start with smaller models (`llama3.2:1b`) for development
2. **Memory**: Ensure adequate RAM (4GB+ for 3B models, 8GB+ for 7B models)
3. **Storage**: Models are cached in volumes for faster subsequent starts
4. **GPU**: For GPU acceleration, use Ollama's GPU-enabled images
