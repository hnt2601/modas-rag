# Backend - MODAS RAG System

> **Version:** 2.0 (Clean Architecture Refactoring)
> **Status:** Migration Planning Complete
> **Architecture:** Clean Architecture + Domain-Driven Design

Production-ready FastAPI backend for RAG system, optimized for Vietnamese AI models from FPT Cloud, following Clean Architecture principles.

---

## 🎯 Architecture Status

### Current State (v1.0 - Functional Architecture)

**Status:** ~30% Complete - Foundation Ready

**✅ Completed:**
- Backend structure (FastAPI + Pydantic)
- Configuration management (`core/config.py`)
- Vietnamese Embedding service (`core/embeddings.py`)
- Logging infrastructure (`utils/logger.py`)
- API schemas (`models/schemas.py`)
- Docker support
- Health check endpoint

**⚠️ Missing:**
- Core RAG logic (retriever, reranker, guard, pipeline)
- API endpoints (chat, documents)
- Qdrant integration
- Testing infrastructure

**Issues:**
- No layer separation
- Business logic mixed with infrastructure
- No dependency injection
- Functional programming only
- Hard to test and extend

### Target State (v2.0 - Clean Architecture)

**Status:** Migration Plan Ready - Implementation Starting

**Target Structure:**
```
backend/
├── domain/                 # Pure business logic (no deps)
├── application/            # Use cases & orchestration
├── infrastructure/         # AI, DB, external services
├── api/                    # FastAPI routes & schemas
├── shared/                 # Cross-cutting concerns
└── tests/                  # Comprehensive testing
```

**Benefits:**
- Clear layer separation
- Testable business logic (90%+ coverage)
- Flexible provider switching
- Domain-Driven Design
- Production-ready patterns

**Timeline:** 2.5 weeks (12 working days)

**See:** [`../docs/migration-plan.md`](../docs/migration-plan.md) for complete plan

---

## 📁 Current Structure

```
backend/
├── main.py                          # FastAPI entry point ✅
├── requirements.txt                 # 111 packages ✅
├── Dockerfile                       # Production build ✅
├── .env                            # Environment config ✅
├── test_embeddings.py              # Embedding tests ✅
│
├── api/                            # API endpoints
│   └── __init__.py                 # ⏳ TODO: Routes not implemented
│
├── core/                           # Core business logic
│   ├── config.py                   # ✅ Pydantic Settings
│   └── embeddings.py               # ✅ Vietnamese Embedding
│
├── models/                         # Data models
│   └── schemas.py                  # ✅ Pydantic schemas
│
├── utils/                          # Utilities
│   └── logger.py                   # ✅ Loguru logging
│
└── logs/                           # Log files
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Qdrant (Docker or local)
- FPT Cloud API key

### Installation

```bash
# Navigate to backend
cd backend

# Install uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment & install dependencies
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your credentials
nano .env

# Required variables:
# FPT_API_KEY=your-fpt-cloud-api-key
# QDRANT_HOST=localhost
# QDRANT_PORT=6333
```

### Run Development Server

```bash
# Option 1: Using uvicorn
uvicorn main:app --reload --port 8000

# Option 2: Using python
python main.py

# Server will start at: http://localhost:8000
```

### Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs

# Root endpoint
curl http://localhost:8000/
```

---

## 🏗️ Clean Architecture Migration

### Target Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    API LAYER (Presentation)                  │
│  Routes, Schemas, Middleware, DI Container                   │
└────────────────────────┬────────────────────────────────────┘
                         ↓ DTOs
┌─────────────────────────────────────────────────────────────┐
│              APPLICATION LAYER (Use Cases)                   │
│  UploadDocument, ProcessQuery, DeleteDocument...             │
└────────────────────────┬────────────────────────────────────┘
                         ↓ Domain Models
┌─────────────────────────────────────────────────────────────┐
│                  DOMAIN LAYER (Core)                         │
│  Entities, Value Objects, Interfaces, Events                 │
└────────────────────────↑────────────────────────────────────┘
                         ↑ Implements
┌─────────────────────────────────────────────────────────────┐
│               INFRASTRUCTURE LAYER                           │
│  AI Adapters, Repositories, Vector Stores, File System       │
└─────────────────────────────────────────────────────────────┘
```

### New Folder Structure

```
backend/
├── domain/                          # 🔵 Pure business logic
│   ├── entities/                    # Document, Query, ChatMessage
│   ├── value_objects/               # DocumentId, Embedding, Content
│   ├── interfaces/                  # Repository & Service contracts
│   ├── events/                      # Domain events
│   └── exceptions/                  # Business exceptions
│
├── application/                     # 🟢 Use cases
│   ├── use_cases/
│   │   ├── documents/               # Upload, Delete, List
│   │   └── chat/                    # ProcessQuery, Stream
│   ├── services/                    # Application services
│   └── dtos/                        # Internal DTOs
│
├── infrastructure/                  # 🟡 External integrations
│   ├── ai/
│   │   ├── embeddings/              # FPT, OpenAI adapters
│   │   ├── llm/                     # GLM, GPT adapters
│   │   ├── reranking/               # BGE reranker
│   │   └── guard/                   # Llama Guard
│   ├── persistence/
│   │   ├── vector_stores/           # Qdrant, Pinecone
│   │   └── database/                # PostgreSQL (optional)
│   ├── file_system/                 # Document loaders
│   └── config/                      # Infrastructure configs
│
├── api/                             # 🔴 HTTP interface
│   ├── routes/                      # FastAPI endpoints
│   ├── schemas/                     # API request/response models
│   ├── dependencies/                # DI container
│   ├── middleware/                  # CORS, auth, logging
│   └── mappers/                     # DTO ↔ Domain mapping
│
├── shared/                          # Cross-cutting
│   ├── logger.py
│   └── utils.py
│
└── tests/                           # Comprehensive testing
    ├── unit/                        # Fast, isolated (75%)
    ├── integration/                 # With real infra (20%)
    └── e2e/                         # Full API flow (5%)
```

### Migration Phases

**Phase 1: Domain Layer (2 days)** - START HERE
- Value Objects: DocumentId, Embedding, Content
- Entities: Document, Query, ChatMessage
- Domain Exceptions
- 100% test coverage

**Phase 2: Domain Interfaces (1 day)**
- Repository interfaces
- Service interfaces (Embedding, LLM, Reranker, Guard)
- Strategy interfaces (Chunking)

**Phase 3: Infrastructure (3 days)**
- Configuration refactoring
- Embedding adapters (FPT, OpenAI)
- Qdrant repository
- LLM adapters
- Integration tests

**Phase 4: Use Cases (2 days)**
- UploadDocumentUseCase
- ProcessQueryUseCase
- DeleteDocumentUseCase
- Unit tests with mocks

**Phase 5: Dependency Injection (1 day)**
- DI container (dependency-injector)
- Provider factories
- FastAPI integration

**Phase 6: API Layer (2 days)**
- API schemas & DTOs
- Routes (chat, documents)
- Middleware
- E2E tests

**Phase 7: Testing & Docs (2 days)**
- 90%+ test coverage
- Architecture Decision Records
- Developer guide

**Total:** 12 working days (2.5 weeks)

**See:** [`../docs/migration-plan.md`](../docs/migration-plan.md) for complete details

---

## 📦 Current Features

### Configuration Management ✅

**File:** `core/config.py`

Centralized Pydantic Settings:

```python
from core.config import settings

# Access configuration
settings.fpt_api_key
settings.chunk_size
settings.embedding_dimensions
```

**Features:**
- Type-safe configuration
- Environment variable validation
- Field validators
- Defaults for all values

### Vietnamese Embedding Service ✅

**File:** `core/embeddings.py`

Complete embedding pipeline:

```python
from core.embeddings import (
    get_embeddings,
    embed_query,
    embed_documents,
    load_document,
    split_documents,
    process_document
)

# Embed query
embedding = await embed_query("Vietnamese query text")

# Process document
result = await process_document("document.pdf")
# Returns: {texts, embeddings, metadata, stats}
```

**Features:**
- Vietnamese_Embedding (1024 dimensions)
- Multi-format support (PDF, DOCX, TXT, MD)
- Async/await operations
- Text chunking (1000 chars, 200 overlap)
- Comprehensive error handling

### API Schemas ✅

**File:** `models/schemas.py`

Pydantic models for all endpoints:

```python
# Chat models
ChatRequest, ChatResponse, StreamChunk

# Document models
DocumentUploadResponse, DocumentInfo, DocumentListResponse

# Health check
HealthCheck

# Error handling
ErrorResponse
```

### Logging ✅

**File:** `utils/logger.py`

Structured logging with Loguru:

```python
from utils.logger import get_logger

logger = get_logger(__name__)

logger.info("Processing document", document_id=doc_id)
logger.error("Failed to embed", error=str(e))
```

**Features:**
- JSON formatting
- File rotation
- Console + file output
- Colored console logs
- Context fields

### Main Application ✅

**File:** `main.py`

FastAPI app with:

```python
# Features
✅ CORS middleware
✅ Global exception handler (Vietnamese errors)
✅ Health check endpoint
✅ API documentation (/docs, /redoc)
✅ Lifespan management
✅ Production uvicorn config
```

---

## ⏳ Planned Features (After Migration)

### Complete RAG Pipeline

```python
# domain/entities/query.py
class Query:
    def validate(self) -> None: ...
    def to_embedding(self, service: IEmbeddingService) -> Embedding: ...

# application/use_cases/chat/process_query.py
class ProcessQueryUseCase:
    async def execute(self, query: str) -> RagResult:
        # 1. Validate query
        # 2. Embed query
        # 3. Vector search (top 20)
        # 4. Rerank (top 5)
        # 5. Generate response
        # 6. Safety check
        return result
```

### Document Management

```python
# application/use_cases/documents/upload_document.py
class UploadDocumentUseCase:
    async def execute(self, file: UploadFile) -> DocumentId:
        # 1. Validate file
        # 2. Load & chunk
        # 3. Embed chunks
        # 4. Store in Qdrant
        return document_id

# application/use_cases/documents/delete_document.py
class DeleteDocumentUseCase:
    async def execute(self, doc_id: DocumentId) -> bool: ...
```

### API Endpoints

```python
# api/routes/chat.py
@router.post("/chat/stream")
async def stream_chat(
    request: ChatRequest,
    use_case: ProcessQueryUseCase = Depends()
) -> StreamingResponse: ...

# api/routes/documents.py
@router.post("/documents/upload")
async def upload_document(
    file: UploadFile,
    use_case: UploadDocumentUseCase = Depends()
) -> DocumentUploadResponse: ...
```

### Provider Flexibility

Switch providers via configuration:

```bash
# .env
EMBEDDING_PROVIDER=fpt      # or openai, huggingface
LLM_PROVIDER=fpt            # or openai, anthropic
VECTOR_STORE=qdrant         # or pinecone
CHUNKING_STRATEGY=recursive # or semantic
```

No code changes required!

---

## 🧪 Testing

### Current Tests

```bash
# Embedding test script
python test_embeddings.py

# Tests:
✅ Query embedding
✅ Batch embedding
✅ Document chunking
✅ Error handling
```

### After Migration (Target: 90%+ Coverage)

```bash
# Unit tests (fast, no dependencies)
pytest tests/unit -v

# Integration tests (with real Qdrant)
pytest tests/integration -v --integration

# E2E tests (full API flow)
pytest tests/e2e -v --e2e

# All tests with coverage
pytest tests/ --cov=. --cov-report=html
```

**Test Structure:**

```
tests/
├── unit/
│   ├── domain/
│   │   ├── test_document.py
│   │   └── test_value_objects.py
│   └── application/
│       └── test_use_cases.py
│
├── integration/
│   ├── test_qdrant_repository.py
│   ├── test_embedding_adapter.py
│   └── test_rag_pipeline.py
│
└── e2e/
    ├── test_chat_api.py
    └── test_document_api.py
```

---

## 🐳 Docker

### Development Build

```bash
# Build image
docker build -t rag-backend:dev .

# Run container
docker run -d \
  -p 8000:8000 \
  -e FPT_API_KEY=your-key \
  -e QDRANT_HOST=host.docker.internal \
  --name rag-backend \
  rag-backend:dev

# View logs
docker logs -f rag-backend
```

### Production Build

Multi-stage Dockerfile optimized for size:

```dockerfile
# Builder stage
FROM python:3.10-slim as builder
# ... install dependencies

# Runtime stage
FROM python:3.10-slim
# ... copy only needed files
```

**Features:**
- Multi-stage build
- Minimal base image
- Non-root user
- Health check
- Optimized layers

---

## 🛠️ Development

### Code Style

```bash
# Install dev dependencies
pip install black isort mypy ruff

# Format code
black .
isort .

# Type checking
mypy .

# Linting
ruff check .
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Adding New Features (After Migration)

#### 1. Add Domain Entity

```python
# domain/entities/your_entity.py
from dataclasses import dataclass
from domain.value_objects import YourId

@dataclass
class YourEntity:
    id: YourId
    # ... fields

    def validate(self) -> None:
        # Business rules
        pass
```

#### 2. Create Use Case

```python
# application/use_cases/your_use_case.py
from domain.interfaces import IYourRepository

class YourUseCase:
    def __init__(self, repository: IYourRepository):
        self._repository = repository

    async def execute(self, request) -> response:
        # Business logic
        pass
```

#### 3. Add API Endpoint

```python
# api/routes/your_route.py
from api.dependencies import get_your_use_case

@router.post("/your-endpoint")
async def your_endpoint(
    use_case: YourUseCase = Depends(get_your_use_case)
):
    return await use_case.execute(...)
```

---

## 📊 Performance

### Current Status (v1.0)

- Health check: < 10ms
- Embedding (single query): ~200-500ms
- Embedding (10 documents): ~1-2s

### Target (v2.0)

- Health check: < 10ms
- Query processing: < 2s (full RAG pipeline)
- Document upload (10MB): < 10s
- Concurrent requests: 100+ req/s (with HPA)

### Optimization Strategies

1. **Caching**
   - Redis for frequently accessed embeddings
   - Query result caching

2. **Batch Processing**
   - Batch embed documents
   - Parallel chunk processing

3. **Connection Pooling**
   - Qdrant connection pool
   - HTTP client pooling

4. **Async Operations**
   - Full async/await
   - Non-blocking I/O

---

## 🔧 Configuration Reference

### Environment Variables

```bash
# FPT Cloud API
FPT_API_KEY=your-api-key                    # Required
FPT_API_BASE=https://api.fpt.ai/v1          # Optional

# Qdrant
QDRANT_HOST=localhost                       # Default
QDRANT_PORT=6333                            # Default
QDRANT_COLLECTION_NAME=documents            # Default

# Redis (Optional)
REDIS_HOST=localhost
REDIS_PORT=6379

# Application
LOG_LEVEL=INFO                              # DEBUG, INFO, WARNING, ERROR
MAX_UPLOAD_SIZE=52428800                    # 50MB
ALLOWED_ORIGINS=http://localhost:5173       # CORS

# RAG Configuration
CHUNK_SIZE=1000                             # Characters
CHUNK_OVERLAP=200                           # Characters
RETRIEVAL_TOP_K=20                          # Vector search results
RERANK_TOP_N=5                              # After reranking

# AI Models
EMBEDDING_MODEL=Vietnamese_Embedding
EMBEDDING_DIMENSIONS=1024
LLM_MODEL=GLM-4.5
LLM_TEMPERATURE=0.7
RERANKER_MODEL=bge-reranker-v2-m3
GUARD_MODEL=Llama-Guard-3-8B
```

### Complete example in `.env.example`

---

## 📚 API Documentation

### Current Endpoints

#### GET `/`
Root endpoint with API information

**Response:**
```json
{
  "name": "MODAS RAG API",
  "version": "1.0.0",
  "status": "running"
}
```

#### GET `/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "checks": {
    "api": "ok",
    "qdrant": "not_configured",
    "fpt_cloud": "not_configured"
  },
  "timestamp": "2025-11-15T..."
}
```

### Planned Endpoints (After Migration)

#### POST `/chat/simple`
Non-streaming chat

**Request:**
```json
{
  "message": "What is the document about?"
}
```

**Response:**
```json
{
  "response": "The document discusses...",
  "sources": [...],
  "metadata": {...}
}
```

#### POST `/chat/stream`
Streaming chat with SSE

**Response:** Server-Sent Events stream

#### POST `/documents/upload`
Upload document

**Request:** Multipart form data with file

**Response:**
```json
{
  "document_id": "uuid",
  "filename": "document.pdf",
  "status": "success",
  "metadata": {
    "chunk_count": 25,
    "size": 102400
  }
}
```

#### GET `/documents/`
List documents

#### DELETE `/documents/{document_id}`
Delete document

**Interactive docs:** http://localhost:8000/docs

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** FPT API key not working
```bash
# Check environment variable
echo $FPT_API_KEY

# Verify in .env file
cat .env | grep FPT_API_KEY

# Test API key
curl -H "Authorization: Bearer $FPT_API_KEY" https://api.fpt.ai/v1/models
```

**Issue:** Qdrant connection failed
```bash
# Check Qdrant is running
docker ps | grep qdrant

# Test connection
curl http://localhost:6333/collections

# Start Qdrant
docker run -d -p 6333:6333 qdrant/qdrant
```

**Issue:** Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check virtual environment
which python
# Should be: /path/to/backend/.venv/bin/python
```

**Issue:** Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn main:app --reload --port 8080
```

---

## 📖 Additional Resources

### Documentation

- [Main README](../README.md) - Project overview
- [Migration Plan](../docs/migration-plan.md) - Detailed refactoring plan
- [Clean Architecture Design](../docs/clean-architecture-design.md) - Architecture details
- [Current Analysis](../docs/analysis-current-architecture.md) - Technical assessment

### External Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

---

## 🎯 Next Steps

### For New Developers

1. **Read documentation:**
   - [`../docs/summary-refactoring-plan.md`](../docs/summary-refactoring-plan.md)
   - [`../docs/migration-plan.md`](../docs/migration-plan.md)

2. **Setup environment:**
   ```bash
   uv venv && source .venv/bin/activate
   uv pip install -r requirements.txt
   cp .env.example .env
   ```

3. **Run current code:**
   ```bash
   uvicorn main:app --reload
   curl http://localhost:8000/health
   ```

### For Migration Contributors

1. **Understand target architecture:**
   - Read [`../docs/clean-architecture-design.md`](../docs/clean-architecture-design.md)

2. **Start Phase 1:**
   - Create domain layer (value objects, entities)
   - Follow [`../docs/migration-plan.md#phase-1`](../docs/migration-plan.md)

3. **Write tests:**
   - Unit tests for all domain logic
   - 100% coverage for domain layer

---

**Status:** 🚀 Ready for Clean Architecture Migration

**Current:** v1.0 (Functional, ~30% complete)

**Target:** v2.0 (Clean Architecture, production-ready)

**Timeline:** 2.5 weeks

**Questions?** See [migration docs](../docs/migration-plan.md) or open an issue
