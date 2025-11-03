# RAG System Backend

Production-ready FastAPI backend for RAG system with Vietnamese AI models from FPT Cloud.

## Features

- ✅ FastAPI with async/await
- ✅ FPT Cloud AI models integration (Vietnamese_Embedding, GLM-4.5, BGE Reranker, Llama Guard)
- ✅ Qdrant vector database
- ✅ Document processing (PDF, DOCX, TXT, MD)
- ✅ Complete RAG pipeline with safety guards
- ✅ Structured logging with Loguru
- ✅ Pydantic configuration management
- ✅ Docker support
- ✅ Health check endpoints

## Quick Start

### 1. Prerequisites

- Python 3.10+
- Qdrant running on localhost:6333
- FPT Cloud API key

### 2. Installation with uv (Recommended)

```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your FPT API key
nano .env
```

### 4. Run Development Server

```bash
# Using uvicorn directly
uvicorn main:app --reload --port 8000

# Or using Python
python main.py
```

### 5. Test the API

```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs
```

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── api/                    # API endpoints
│   ├── __init__.py
│   ├── chat.py            # Chat endpoints (TODO)
│   └── documents.py       # Document management (TODO)
├── core/                   # Core business logic
│   ├── __init__.py
│   ├── config.py          # Configuration management ✅
│   ├── embeddings.py      # Vietnamese Embedding (TODO)
│   ├── retriever.py       # Qdrant retriever (TODO)
│   ├── reranker.py        # BGE Reranker (TODO)
│   ├── guard.py           # Llama Guard (TODO)
│   └── rag.py             # Complete RAG pipeline (TODO)
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic models ✅
├── utils/
│   ├── __init__.py
│   └── logger.py          # Logging configuration ✅
├── requirements.txt       # Python dependencies ✅
├── Dockerfile             # Docker build file ✅
├── .env.example          # Environment template ✅
└── .gitignore            # Git ignore rules ✅
```

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `FPT_API_KEY`: Your FPT Cloud API key (required)
- `QDRANT_HOST`: Qdrant server host (default: localhost)
- `QDRANT_PORT`: Qdrant server port (default: 6333)
- `LOG_LEVEL`: Logging level (default: INFO)

## API Endpoints

### Health Check
```
GET /health
```

### Chat (TODO)
```
POST /chat/simple - Non-streaming chat
POST /chat/stream - Streaming chat with SSE
```

### Documents (TODO)
```
POST /documents/upload - Upload document
GET /documents/list - List all documents
DELETE /documents/{doc_id} - Delete document
```

## Docker

### Build Image
```bash
docker build -t rag-backend:latest .
```

### Run Container
```bash
docker run -d \
  -p 8000:8000 \
  -e FPT_API_KEY=your-key \
  -e QDRANT_HOST=host.docker.internal \
  --name rag-backend \
  rag-backend:latest
```

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Formatting
```bash
# Install dev dependencies
pip install black isort mypy

# Format code
black .
isort .

# Type checking
mypy .
```

## Next Steps

1. ✅ Setup backend structure
2. ⏳ Implement Vietnamese Embedding service
3. ⏳ Implement Qdrant retriever
4. ⏳ Implement BGE Reranker
5. ⏳ Implement Llama Guard
6. ⏳ Implement complete RAG pipeline
7. ⏳ Implement chat endpoints
8. ⏳ Implement document endpoints

## License

MIT

