# Clean Architecture Design for MODAS RAG

> Version: 1.0
> Date: 2025-11-15
> Status: Design Document

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Layer Definitions](#layer-definitions)
3. [Folder Structure](#folder-structure)
4. [Component Design](#component-design)
5. [Design Patterns](#design-patterns)
6. [Dependencies Flow](#dependencies-flow)
7. [Testing Strategy](#testing-strategy)

---

## 1. Architecture Overview

### Clean Architecture Principles

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLEAN ARCHITECTURE                        │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                    API LAYER                            │    │
│  │  (FastAPI routes, schemas, middleware, dependencies)    │    │
│  └────────────────────┬───────────────────────────────────┘    │
│                       │                                          │
│                       ↓ DTOs                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              APPLICATION LAYER                          │    │
│  │         (Use Cases, Application Services)               │    │
│  └────────────────────┬───────────────────────────────────┘    │
│                       │                                          │
│                       ↓ Domain Models                            │
│  ┌────────────────────────────────────────────────────────┐    │
│  │                  DOMAIN LAYER                           │    │
│  │    (Entities, Value Objects, Interfaces, Events)        │    │
│  └────────────────────┬───────────────────────────────────┘    │
│                       ↑                                          │
│                       │ Implements                               │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              INFRASTRUCTURE LAYER                       │    │
│  │  (AI providers, Databases, Vector stores, Adapters)     │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘

KEY RULE: Dependencies point INWARD
- Infrastructure depends on Domain (not vice versa)
- Use Cases depend on Domain interfaces
- API depends on Use Cases
```

### Core Design Principles

1. **Dependency Inversion Principle (DIP)**
   - High-level modules don't depend on low-level modules
   - Both depend on abstractions (interfaces/protocols)

2. **Single Responsibility Principle (SRP)**
   - Each class/module has one reason to change
   - Separate concerns into distinct layers

3. **Interface Segregation Principle (ISP)**
   - Clients shouldn't depend on interfaces they don't use
   - Many small interfaces > one large interface

4. **Open/Closed Principle (OCP)**
   - Open for extension, closed for modification
   - Use strategies and factories for new providers

5. **Separation of Concerns**
   - Business logic isolated from infrastructure
   - API schemas separate from domain models
   - Configuration separate from implementation

---

## 2. Layer Definitions

### Layer 1: Domain Layer (Core)

**Purpose:** Pure business logic, no external dependencies

**Contains:**
- **Entities:** Core business objects with identity
- **Value Objects:** Immutable objects without identity
- **Domain Events:** Events that occur in the domain
- **Repository Interfaces:** Contracts for data access
- **Service Interfaces:** Contracts for external services
- **Domain Exceptions:** Business rule violations

**Rules:**
- ✅ No framework dependencies (no FastAPI, LangChain, etc.)
- ✅ No infrastructure code (no database, no API calls)
- ✅ Only Python standard library + type hints
- ✅ Rich behavior in entities
- ✅ Immutable value objects

**Example:**
```python
# domain/entities/document.py
from dataclasses import dataclass
from typing import List
from domain.value_objects import DocumentId, Content, Metadata
from domain.interfaces import IChunkingStrategy

@dataclass
class Document:
    """Rich domain entity with behavior"""
    id: DocumentId
    content: Content
    metadata: Metadata

    def split_into_chunks(self, strategy: IChunkingStrategy) -> List['Chunk']:
        """Business logic: how to chunk a document"""
        return strategy.split(self.content)

    def validate(self) -> None:
        """Business rule: document must be valid"""
        if len(self.content.text) < 10:
            raise InvalidDocumentError("Content too short")
```

### Layer 2: Application Layer (Use Cases)

**Purpose:** Orchestrate domain logic, implement use cases

**Contains:**
- **Use Cases:** Single application operations
- **Application Services:** Coordinate multiple use cases
- **DTOs:** Data transfer objects (internal)
- **Application Exceptions:** Application-level errors

**Rules:**
- ✅ Depends on domain layer only
- ✅ No framework dependencies (pure Python)
- ✅ Orchestrates domain entities
- ✅ Uses repository/service interfaces (from domain)
- ✅ No direct infrastructure access

**Example:**
```python
# application/use_cases/upload_document.py
from domain.entities import Document
from domain.interfaces import IDocumentRepository, IEmbeddingService
from domain.value_objects import DocumentId

class UploadDocumentUseCase:
    """Pure business logic orchestration"""

    def __init__(
        self,
        repository: IDocumentRepository,
        embedding_service: IEmbeddingService,
    ):
        self.repository = repository
        self.embedding_service = embedding_service

    async def execute(self, content: str, metadata: dict) -> DocumentId:
        # Create domain entity
        document = Document.create(content, metadata)

        # Business rule validation
        document.validate()

        # Chunk document (domain logic)
        chunks = document.split_into_chunks()

        # Generate embeddings (infrastructure)
        embeddings = await self.embedding_service.embed(chunks)

        # Persist (infrastructure)
        doc_id = await self.repository.save(document, embeddings)

        return doc_id
```

### Layer 3: Infrastructure Layer

**Purpose:** Implement domain interfaces, integrate external services

**Contains:**
- **Repository Implementations:** Qdrant, PostgreSQL, etc.
- **Service Adapters:** LLM providers, embedding APIs
- **External API Clients:** FPT Cloud, OpenAI wrappers
- **File System:** Document loaders, file storage
- **Factories:** Create service instances
- **Configurations:** Provider-specific configs

**Rules:**
- ✅ Implements domain interfaces
- ✅ Can use any framework/library
- ✅ Adapts external APIs to domain interfaces
- ✅ No business logic (just translation)

**Example:**
```python
# infrastructure/embedding/fpt_embedding_adapter.py
from langchain_openai import OpenAIEmbeddings
from domain.interfaces import IEmbeddingService
from domain.value_objects import Embedding

class FptEmbeddingAdapter(IEmbeddingService):
    """Adapts FPT Cloud API to domain interface"""

    def __init__(self, api_key: str, api_base: str):
        self._client = OpenAIEmbeddings(
            api_key=api_key,
            base_url=api_base,
            model="Vietnamese_Embedding"
        )

    async def embed(self, texts: List[str]) -> List[Embedding]:
        """Translate from LangChain to domain model"""
        vectors = await self._client.aembed_documents(texts)
        return [Embedding(vector) for vector in vectors]
```

### Layer 4: API Layer (Presentation)

**Purpose:** HTTP interface, request/response handling

**Contains:**
- **Routes:** FastAPI endpoints
- **API Schemas:** Pydantic request/response models
- **Middleware:** CORS, auth, error handling
- **Dependencies:** Dependency injection for routes
- **Validators:** Request validation
- **Mappers:** API schemas ↔ domain models

**Rules:**
- ✅ Thin layer (no business logic)
- ✅ Depends on application layer
- ✅ Translates HTTP → Use Cases → HTTP
- ✅ Handles serialization/deserialization

**Example:**
```python
# api/routes/documents.py
from fastapi import APIRouter, UploadFile, Depends
from api.schemas import DocumentUploadResponse
from api.dependencies import get_upload_use_case
from application.use_cases import UploadDocumentUseCase

router = APIRouter(prefix="/documents")

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile,
    use_case: UploadDocumentUseCase = Depends(get_upload_use_case),
):
    """Thin controller - delegates to use case"""
    content = await file.read()
    doc_id = await use_case.execute(content, metadata={...})
    return DocumentUploadResponse.from_domain(doc_id)
```

---

## 3. Folder Structure

### Complete Backend Structure

```
backend/
├── main.py                          # FastAPI app factory
├── requirements.txt                 # Dependencies
├── pyproject.toml                   # Poetry/setuptools config
├── pytest.ini                       # Test configuration
├── .env.example                     # Environment template
│
├── domain/                          # 🔵 DOMAIN LAYER (Pure Python)
│   ├── __init__.py
│   │
│   ├── entities/                    # Business entities
│   │   ├── __init__.py
│   │   ├── document.py              # Document entity
│   │   ├── query.py                 # Query entity
│   │   ├── chat_message.py          # ChatMessage entity
│   │   └── search_result.py         # SearchResult entity
│   │
│   ├── value_objects/               # Immutable values
│   │   ├── __init__.py
│   │   ├── document_id.py           # UUID wrapper
│   │   ├── embedding.py             # Vector wrapper
│   │   ├── content.py               # Text content
│   │   ├── metadata.py              # Document metadata
│   │   └── score.py                 # Relevance score
│   │
│   ├── interfaces/                  # Abstract contracts
│   │   ├── __init__.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── document_repository.py
│   │   │   └── vector_repository.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── embedding_service.py
│   │       ├── llm_service.py
│   │       ├── reranker_service.py
│   │       ├── guard_service.py
│   │       └── chunking_strategy.py
│   │
│   ├── events/                      # Domain events
│   │   ├── __init__.py
│   │   ├── document_uploaded.py
│   │   ├── query_processed.py
│   │   └── document_deleted.py
│   │
│   └── exceptions/                  # Domain exceptions
│       ├── __init__.py
│       ├── document_errors.py
│       ├── query_errors.py
│       └── validation_errors.py
│
├── application/                     # 🟢 APPLICATION LAYER
│   ├── __init__.py
│   │
│   ├── use_cases/                   # Single-purpose operations
│   │   ├── __init__.py
│   │   ├── documents/
│   │   │   ├── __init__.py
│   │   │   ├── upload_document.py
│   │   │   ├── delete_document.py
│   │   │   └── list_documents.py
│   │   │
│   │   └── chat/
│   │       ├── __init__.py
│   │       ├── process_query.py
│   │       └── stream_response.py
│   │
│   ├── services/                    # Application services
│   │   ├── __init__.py
│   │   ├── rag_service.py           # Orchestrates RAG pipeline
│   │   └── document_service.py      # Document operations
│   │
│   ├── dtos/                        # Internal DTOs
│   │   ├── __init__.py
│   │   ├── query_request.py
│   │   └── rag_result.py
│   │
│   └── exceptions/                  # Application exceptions
│       ├── __init__.py
│       └── application_errors.py
│
├── infrastructure/                  # 🟡 INFRASTRUCTURE LAYER
│   ├── __init__.py
│   │
│   ├── ai/                          # AI service adapters
│   │   ├── __init__.py
│   │   │
│   │   ├── embeddings/
│   │   │   ├── __init__.py
│   │   │   ├── fpt_embedding_adapter.py
│   │   │   ├── openai_embedding_adapter.py
│   │   │   └── embedding_factory.py
│   │   │
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── fpt_llm_adapter.py
│   │   │   ├── openai_llm_adapter.py
│   │   │   ├── anthropic_llm_adapter.py
│   │   │   └── llm_factory.py
│   │   │
│   │   ├── reranking/
│   │   │   ├── __init__.py
│   │   │   ├── bge_reranker_adapter.py
│   │   │   └── reranker_factory.py
│   │   │
│   │   └── guard/
│   │       ├── __init__.py
│   │       ├── llama_guard_adapter.py
│   │       └── guard_factory.py
│   │
│   ├── persistence/                 # Data persistence
│   │   ├── __init__.py
│   │   │
│   │   ├── vector_stores/
│   │   │   ├── __init__.py
│   │   │   ├── qdrant_repository.py
│   │   │   ├── pinecone_repository.py
│   │   │   └── vector_store_factory.py
│   │   │
│   │   └── database/
│   │       ├── __init__.py
│   │       ├── postgresql_repository.py
│   │       └── models.py            # SQLAlchemy models
│   │
│   ├── file_system/                 # File handling
│   │   ├── __init__.py
│   │   ├── document_loader.py       # PDF, DOCX, TXT loader
│   │   └── file_validator.py        # File validation
│   │
│   ├── external/                    # External service clients
│   │   ├── __init__.py
│   │   ├── fpt_cloud_client.py
│   │   └── health_checker.py
│   │
│   └── config/                      # Infrastructure configs
│       ├── __init__.py
│       ├── settings.py              # Pydantic settings
│       ├── ai_config.py             # AI provider configs
│       ├── database_config.py       # DB configs
│       └── feature_flags.py         # Feature toggles
│
├── api/                             # 🔴 API LAYER (Presentation)
│   ├── __init__.py
│   │
│   ├── routes/                      # FastAPI routes
│   │   ├── __init__.py
│   │   ├── chat.py                  # Chat endpoints
│   │   ├── documents.py             # Document endpoints
│   │   └── health.py                # Health check
│   │
│   ├── schemas/                     # Pydantic API models
│   │   ├── __init__.py
│   │   ├── chat_schemas.py
│   │   ├── document_schemas.py
│   │   ├── health_schemas.py
│   │   └── error_schemas.py
│   │
│   ├── dependencies/                # FastAPI dependencies
│   │   ├── __init__.py
│   │   ├── container.py             # DI container
│   │   ├── auth.py                  # Auth dependencies
│   │   └── use_case_providers.py   # Use case injection
│   │
│   ├── middleware/                  # FastAPI middleware
│   │   ├── __init__.py
│   │   ├── cors.py
│   │   ├── error_handler.py
│   │   └── logging.py
│   │
│   └── mappers/                     # DTO ↔ Domain mappers
│       ├── __init__.py
│       ├── document_mapper.py
│       └── chat_mapper.py
│
├── shared/                          # 🔵 SHARED (Cross-cutting)
│   ├── __init__.py
│   ├── logger.py                    # Logging utility
│   ├── utils.py                     # Common utilities
│   └── constants.py                 # Application constants
│
└── tests/                           # 🧪 TESTS
    ├── __init__.py
    ├── conftest.py                  # Pytest fixtures
    │
    ├── unit/                        # Unit tests (fast)
    │   ├── domain/
    │   │   ├── test_document.py
    │   │   └── test_value_objects.py
    │   │
    │   └── application/
    │       └── test_use_cases.py
    │
    ├── integration/                 # Integration tests
    │   ├── test_repositories.py
    │   ├── test_ai_services.py
    │   └── test_rag_pipeline.py
    │
    └── e2e/                         # End-to-end tests
        ├── test_chat_api.py
        └── test_document_api.py
```

### Import Path Organization

```python
# ✅ Allowed imports (follows Clean Architecture)
# Domain layer
from domain.entities import Document
from domain.value_objects import DocumentId
from domain.interfaces import IEmbeddingService

# Application layer
from application.use_cases import UploadDocumentUseCase
from domain.entities import Document  # ✓ Can import domain

# Infrastructure layer
from infrastructure.ai.embeddings import FptEmbeddingAdapter
from domain.interfaces import IEmbeddingService  # ✓ Implements interface

# API layer
from api.routes import chat_router
from application.use_cases import ProcessQueryUseCase  # ✓ Uses use cases

# ❌ Forbidden imports (violates Clean Architecture)
# Domain layer
from infrastructure.ai import FptEmbeddingAdapter  # ✗ NO infrastructure
from fastapi import FastAPI  # ✗ NO framework dependencies

# Application layer
from infrastructure.persistence import QdrantRepository  # ✗ NO concrete infra
from api.schemas import ChatRequest  # ✗ NO API schemas
```

---

## 4. Component Design

### A. Domain Entities

#### Document Entity

```python
# domain/entities/document.py
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from domain.value_objects import DocumentId, Content, Metadata
from domain.interfaces import IChunkingStrategy
from domain.exceptions import InvalidDocumentError

@dataclass
class Document:
    """Core business entity: A document in the RAG system"""

    id: DocumentId
    content: Content
    metadata: Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    chunks: Optional[List['Chunk']] = None

    @classmethod
    def create(cls, content_text: str, metadata_dict: dict) -> 'Document':
        """Factory method to create a valid document"""
        doc_id = DocumentId.generate()
        content = Content(content_text)
        metadata = Metadata.from_dict(metadata_dict)

        document = cls(id=doc_id, content=content, metadata=metadata)
        document.validate()
        return document

    def validate(self) -> None:
        """Business rule: document must meet quality criteria"""
        if len(self.content.text) < 10:
            raise InvalidDocumentError("Document too short (min 10 chars)")

        if len(self.content.text) > 10_000_000:  # 10MB
            raise InvalidDocumentError("Document too large (max 10MB)")

        if not self.metadata.filename:
            raise InvalidDocumentError("Filename required")

    def split_into_chunks(self, strategy: IChunkingStrategy) -> List['Chunk']:
        """Business logic: split document using strategy pattern"""
        if self.chunks is not None:
            return self.chunks

        self.chunks = strategy.split(self.content, self.metadata)
        return self.chunks

    def get_chunk_count(self) -> int:
        """Business query: how many chunks?"""
        return len(self.chunks) if self.chunks else 0


@dataclass
class Chunk:
    """Value object: A chunk of a document"""

    text: str
    metadata: Metadata
    chunk_index: int
    parent_document_id: DocumentId

    def __post_init__(self):
        if not self.text or len(self.text) < 10:
            raise InvalidDocumentError("Chunk too short")
```

#### Query Entity

```python
# domain/entities/query.py
from dataclasses import dataclass
from typing import Optional, Dict, Any

from domain.value_objects import QueryText
from domain.exceptions import InvalidQueryError

@dataclass
class Query:
    """Core business entity: A user query"""

    text: QueryText
    filters: Optional[Dict[str, Any]] = None
    max_results: int = 5

    @classmethod
    def create(cls, text: str, **kwargs) -> 'Query':
        """Factory method"""
        query_text = QueryText(text)
        query = cls(text=query_text, **kwargs)
        query.validate()
        return query

    def validate(self) -> None:
        """Business rules for queries"""
        if len(self.text.value) < 3:
            raise InvalidQueryError("Query too short (min 3 chars)")

        if len(self.text.value) > 2000:
            raise InvalidQueryError("Query too long (max 2000 chars)")

        if self.max_results < 1 or self.max_results > 20:
            raise InvalidQueryError("max_results must be 1-20")
```

### B. Value Objects

```python
# domain/value_objects/document_id.py
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True)
class DocumentId:
    """Value object: Unique document identifier"""

    value: UUID

    @classmethod
    def generate(cls) -> 'DocumentId':
        """Generate new ID"""
        return cls(value=uuid4())

    @classmethod
    def from_string(cls, id_str: str) -> 'DocumentId':
        """Parse from string"""
        return cls(value=UUID(id_str))

    def __str__(self) -> str:
        return str(self.value)


# domain/value_objects/embedding.py
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Embedding:
    """Value object: Vector embedding"""

    vector: List[float]

    def __post_init__(self):
        if len(self.vector) != 1024:
            raise ValueError("Embedding must be 1024 dimensions")

    def dimension(self) -> int:
        return len(self.vector)
```

### C. Domain Interfaces

```python
# domain/interfaces/services/embedding_service.py
from abc import ABC, abstractmethod
from typing import List

from domain.value_objects import Embedding

class IEmbeddingService(ABC):
    """Contract for embedding generation"""

    @abstractmethod
    async def embed_query(self, text: str) -> Embedding:
        """Embed a single query"""
        pass

    @abstractmethod
    async def embed_documents(self, texts: List[str]) -> List[Embedding]:
        """Embed multiple documents"""
        pass


# domain/interfaces/repositories/document_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities import Document
from domain.value_objects import DocumentId

class IDocumentRepository(ABC):
    """Contract for document persistence"""

    @abstractmethod
    async def save(self, document: Document) -> DocumentId:
        """Persist a document"""
        pass

    @abstractmethod
    async def find_by_id(self, doc_id: DocumentId) -> Optional[Document]:
        """Retrieve by ID"""
        pass

    @abstractmethod
    async def delete(self, doc_id: DocumentId) -> bool:
        """Delete a document"""
        pass

    @abstractmethod
    async def list_all(self) -> List[Document]:
        """List all documents"""
        pass
```

### D. Use Cases

```python
# application/use_cases/documents/upload_document.py
from dataclasses import dataclass

from domain.entities import Document
from domain.interfaces import (
    IDocumentRepository,
    IEmbeddingService,
    IChunkingStrategy,
)
from domain.value_objects import DocumentId
from application.exceptions import DocumentProcessingError

@dataclass
class UploadDocumentRequest:
    """Use case input DTO"""
    content: str
    filename: str
    file_type: str
    user_id: Optional[str] = None

@dataclass
class UploadDocumentResponse:
    """Use case output DTO"""
    document_id: DocumentId
    chunk_count: int
    status: str


class UploadDocumentUseCase:
    """
    Use Case: Upload and process a document

    Business Rules:
    1. Document must be valid (min/max size, format)
    2. Content must be chunked using configured strategy
    3. Chunks must be embedded before storage
    4. All chunks stored together in vector store
    """

    def __init__(
        self,
        document_repository: IDocumentRepository,
        embedding_service: IEmbeddingService,
        chunking_strategy: IChunkingStrategy,
    ):
        """Inject dependencies (all are interfaces)"""
        self._repository = document_repository
        self._embedding_service = embedding_service
        self._chunking_strategy = chunking_strategy

    async def execute(
        self,
        request: UploadDocumentRequest
    ) -> UploadDocumentResponse:
        """Execute the use case"""

        # 1. Create domain entity
        metadata = {
            "filename": request.filename,
            "file_type": request.file_type,
            "user_id": request.user_id,
        }
        document = Document.create(request.content, metadata)

        # 2. Validate (business rules)
        document.validate()

        # 3. Chunk document (domain logic)
        chunks = document.split_into_chunks(self._chunking_strategy)

        # 4. Generate embeddings (infrastructure via interface)
        chunk_texts = [chunk.text for chunk in chunks]
        embeddings = await self._embedding_service.embed_documents(chunk_texts)

        # 5. Attach embeddings to chunks
        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding

        # 6. Persist document with chunks (infrastructure via interface)
        try:
            doc_id = await self._repository.save(document)
        except Exception as e:
            raise DocumentProcessingError(f"Failed to save document: {e}")

        # 7. Return result
        return UploadDocumentResponse(
            document_id=doc_id,
            chunk_count=len(chunks),
            status="success"
        )
```

### E. Infrastructure Adapters

```python
# infrastructure/ai/embeddings/fpt_embedding_adapter.py
from typing import List
from langchain_openai import OpenAIEmbeddings

from domain.interfaces import IEmbeddingService
from domain.value_objects import Embedding
from infrastructure.config import AIConfig

class FptEmbeddingAdapter(IEmbeddingService):
    """
    Adapter: Translates FPT Cloud API to domain interface

    This is pure infrastructure - no business logic
    """

    def __init__(self, config: AIConfig):
        """Initialize with config (not domain dependency)"""
        self._client = OpenAIEmbeddings(
            api_key=config.fpt_api_key,
            base_url=config.fpt_api_base,
            model=config.embedding_model,
        )
        self._dimensions = config.embedding_dimensions

    async def embed_query(self, text: str) -> Embedding:
        """Implement interface method"""
        vector = await self._client.aembed_query(text)
        return Embedding(vector)

    async def embed_documents(self, texts: List[str]) -> List[Embedding]:
        """Implement interface method"""
        vectors = await self._client.aembed_documents(texts)
        return [Embedding(vector) for vector in vectors]


# infrastructure/ai/embeddings/embedding_factory.py
from domain.interfaces import IEmbeddingService
from infrastructure.config import Settings
from infrastructure.ai.embeddings import (
    FptEmbeddingAdapter,
    OpenAIEmbeddingAdapter,
)

class EmbeddingFactory:
    """Factory pattern: Create embedding service based on config"""

    @staticmethod
    def create(settings: Settings) -> IEmbeddingService:
        """Factory method"""
        provider = settings.ai.embedding_provider

        if provider == "fpt":
            return FptEmbeddingAdapter(settings.ai)
        elif provider == "openai":
            return OpenAIEmbeddingAdapter(settings.ai)
        else:
            raise ValueError(f"Unknown embedding provider: {provider}")
```

### F. API Layer

```python
# api/routes/documents.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List

from api.schemas import DocumentUploadResponse, DocumentInfo
from api.dependencies import get_upload_use_case, get_list_use_case
from application.use_cases import (
    UploadDocumentUseCase,
    UploadDocumentRequest,
    ListDocumentsUseCase,
)

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    use_case: UploadDocumentUseCase = Depends(get_upload_use_case),
):
    """
    Upload and process a document

    This is a thin controller:
    1. Extract data from HTTP request
    2. Map to use case request DTO
    3. Execute use case
    4. Map result to API response
    5. Return HTTP response

    NO business logic here!
    """

    # 1. Validate file
    if file.size > 50 * 1024 * 1024:  # 50MB
        raise HTTPException(400, "File too large")

    # 2. Read content
    content = await file.read()
    content_text = content.decode('utf-8')

    # 3. Create use case request
    request = UploadDocumentRequest(
        content=content_text,
        filename=file.filename,
        file_type=file.content_type,
    )

    # 4. Execute use case (business logic)
    try:
        result = await use_case.execute(request)
    except Exception as e:
        raise HTTPException(500, f"Processing failed: {e}")

    # 5. Map to API response schema
    return DocumentUploadResponse(
        document_id=str(result.document_id),
        filename=request.filename,
        status=result.status,
        metadata={"chunk_count": result.chunk_count},
    )


@router.get("/", response_model=List[DocumentInfo])
async def list_documents(
    use_case: ListDocumentsUseCase = Depends(get_list_use_case),
):
    """List all documents (thin controller)"""
    documents = await use_case.execute()
    return [DocumentInfo.from_domain(doc) for doc in documents]


# api/schemas/document_schemas.py
from pydantic import BaseModel, Field
from typing import Dict, Any
from domain.entities import Document

class DocumentUploadResponse(BaseModel):
    """API response schema (not domain model)"""
    document_id: str
    filename: str
    status: str
    metadata: Dict[str, Any]

class DocumentInfo(BaseModel):
    """API response schema"""
    document_id: str
    filename: str
    created_at: str
    chunk_count: int

    @classmethod
    def from_domain(cls, document: Document) -> 'DocumentInfo':
        """Map from domain entity to API schema"""
        return cls(
            document_id=str(document.id),
            filename=document.metadata.filename,
            created_at=document.created_at.isoformat(),
            chunk_count=document.get_chunk_count(),
        )
```

---

## 5. Design Patterns

### Pattern 1: Repository Pattern

**Purpose:** Abstract data access

```python
# Domain defines the contract
class IDocumentRepository(ABC):
    @abstractmethod
    async def save(self, doc: Document) -> DocumentId: pass

# Infrastructure implements it
class QdrantDocumentRepository(IDocumentRepository):
    async def save(self, doc: Document) -> DocumentId:
        # Qdrant-specific implementation
        pass

# Use case uses the interface
class UploadDocumentUseCase:
    def __init__(self, repo: IDocumentRepository):
        self._repo = repo  # Depends on interface, not implementation
```

**Benefits:**
- Swap Qdrant for Pinecone without changing use cases
- Easy to mock for testing
- Business logic independent of database

### Pattern 2: Strategy Pattern

**Purpose:** Interchangeable algorithms

```python
# Domain defines strategy interface
class IChunkingStrategy(ABC):
    @abstractmethod
    def split(self, content: Content) -> List[Chunk]: pass

# Infrastructure provides implementations
class RecursiveChunkingStrategy(IChunkingStrategy):
    def split(self, content: Content) -> List[Chunk]:
        # RecursiveCharacterTextSplitter logic
        pass

class SemanticChunkingStrategy(IChunkingStrategy):
    def split(self, content: Content) -> List[Chunk]:
        # Semantic chunking logic
        pass

# Use at runtime
document.split_into_chunks(strategy=RecursiveChunkingStrategy())
```

**Benefits:**
- Multiple chunking strategies
- Config-based selection
- Easy to add new strategies

### Pattern 3: Factory Pattern

**Purpose:** Create complex objects

```python
class EmbeddingFactory:
    @staticmethod
    def create(settings: Settings) -> IEmbeddingService:
        match settings.ai.embedding_provider:
            case "fpt":
                return FptEmbeddingAdapter(settings.ai)
            case "openai":
                return OpenAIEmbeddingAdapter(settings.ai)
            case "huggingface":
                return HuggingFaceEmbeddingAdapter(settings.ai)

# Usage
embedding_service = EmbeddingFactory.create(settings)
```

**Benefits:**
- Centralized object creation
- Config-based provider selection
- Easy to extend

### Pattern 4: Adapter Pattern

**Purpose:** Translate external APIs to domain interfaces

```python
# External API (LangChain)
class OpenAIEmbeddings:
    def embed_documents(self, texts: List[str]) -> List[List[float]]: pass

# Domain interface
class IEmbeddingService(ABC):
    async def embed_documents(self, texts: List[str]) -> List[Embedding]: pass

# Adapter
class FptEmbeddingAdapter(IEmbeddingService):
    def __init__(self):
        self._langchain_client = OpenAIEmbeddings(...)

    async def embed_documents(self, texts: List[str]) -> List[Embedding]:
        # Adapt: List[List[float]] → List[Embedding]
        vectors = await self._langchain_client.aembed_documents(texts)
        return [Embedding(vector) for vector in vectors]
```

**Benefits:**
- Isolate external dependencies
- Domain doesn't know about LangChain
- Easy to replace LangChain

### Pattern 5: Dependency Injection

**Purpose:** Invert dependencies, improve testability

```python
# Without DI (bad)
class UploadDocumentUseCase:
    def __init__(self):
        self._repo = QdrantRepository()  # Hard-coded dependency

# With DI (good)
class UploadDocumentUseCase:
    def __init__(self, repo: IDocumentRepository):
        self._repo = repo  # Injected dependency

# DI Container
class Container:
    def __init__(self, settings: Settings):
        # Infrastructure
        self.embedding_service = EmbeddingFactory.create(settings)
        self.document_repository = QdrantRepository(settings.qdrant)
        self.chunking_strategy = RecursiveChunkingStrategy(settings.chunking)

        # Use cases
        self.upload_use_case = UploadDocumentUseCase(
            document_repository=self.document_repository,
            embedding_service=self.embedding_service,
            chunking_strategy=self.chunking_strategy,
        )

# FastAPI dependency
def get_upload_use_case(container: Container = Depends(get_container)):
    return container.upload_use_case
```

**Benefits:**
- Easy to test (inject mocks)
- Loose coupling
- Runtime flexibility

### Pattern 6: Unit of Work

**Purpose:** Transaction management

```python
class IUnitOfWork(ABC):
    @abstractmethod
    async def __aenter__(self): pass

    @abstractmethod
    async def __aexit__(self, *args): pass

    @abstractmethod
    async def commit(self): pass

    @abstractmethod
    async def rollback(self): pass

# Use case with transaction
async def execute(self, request):
    async with self._unit_of_work:
        # Multiple repository operations
        doc_id = await self._doc_repo.save(document)
        await self._vector_repo.save_embeddings(embeddings)

        # Commit all or rollback all
        await self._unit_of_work.commit()
```

---

## 6. Dependencies Flow

### Dependency Rules

```
┌─────────────────────────────────────────────────────────────┐
│                     DEPENDENCY FLOW                          │
│                                                              │
│  API Layer                                                   │
│     ↓ depends on                                             │
│  Application Layer (Use Cases)                               │
│     ↓ depends on                                             │
│  Domain Layer (Entities, Interfaces)                         │
│     ↑ implemented by                                         │
│  Infrastructure Layer (Adapters, Repositories)               │
│                                                              │
│  KEY RULE: Dependencies point INWARD                         │
│  - Infrastructure implements domain interfaces               │
│  - Domain has NO dependencies on outer layers                │
└─────────────────────────────────────────────────────────────┘
```

### Dependency Injection Flow

```python
# 1. Bootstrap (main.py)
settings = Settings()  # Load config

# 2. Build Infrastructure (factories)
embedding_service = EmbeddingFactory.create(settings)
llm_service = LlmFactory.create(settings)
vector_store = VectorStoreFactory.create(settings)

# 3. Build Repositories (infrastructure)
document_repo = QdrantDocumentRepository(vector_store)

# 4. Build Use Cases (application)
upload_use_case = UploadDocumentUseCase(
    document_repository=document_repo,
    embedding_service=embedding_service,
)

# 5. Inject into API (presentation)
@app.post("/documents/upload")
async def upload(use_case: UploadDocumentUseCase = Depends()):
    return await use_case.execute(...)
```

### Configuration-Based Provider Selection

```python
# .env
EMBEDDING_PROVIDER=fpt
LLM_PROVIDER=openai
VECTOR_STORE=qdrant

# Factory selects implementation
embedding_service = EmbeddingFactory.create(settings)
# Returns: FptEmbeddingAdapter (implements IEmbeddingService)

llm_service = LlmFactory.create(settings)
# Returns: OpenAILlmAdapter (implements ILlmService)

# Use cases receive interfaces (don't know concrete implementation)
use_case = ProcessQueryUseCase(
    embedding_service=embedding_service,  # Could be FPT or OpenAI
    llm_service=llm_service,              # Could be OpenAI or Anthropic
)
```

---

## 7. Testing Strategy

### Test Pyramid

```
       ┌─────────────┐
       │   E2E (5%)  │  ← Slow, expensive, few tests
       ├─────────────┤
       │Integration  │  ← Medium speed, moderate quantity
       │    (20%)    │
       ├─────────────┤
       │    Unit     │  ← Fast, cheap, many tests
       │    (75%)    │
       └─────────────┘
```

### Unit Tests (Fast, No Dependencies)

```python
# tests/unit/domain/test_document.py
def test_document_creation():
    """Test domain entity creation"""
    # No dependencies - pure Python
    doc = Document.create("Some content", {"filename": "test.txt"})
    assert doc.content.text == "Some content"

def test_document_validation():
    """Test business rules"""
    with pytest.raises(InvalidDocumentError):
        Document.create("Short", {})  # Too short

# tests/unit/application/test_upload_use_case.py
async def test_upload_document_success():
    """Test use case with mocks"""
    # Mock infrastructure
    mock_repo = Mock(IDocumentRepository)
    mock_embedding = Mock(IEmbeddingService)

    use_case = UploadDocumentUseCase(mock_repo, mock_embedding)

    # Execute
    result = await use_case.execute(request)

    # Assert
    mock_repo.save.assert_called_once()
    assert result.status == "success"
```

### Integration Tests (With Real Infrastructure)

```python
# tests/integration/test_qdrant_repository.py
@pytest.mark.integration
async def test_save_and_retrieve_document(qdrant_client):
    """Test with real Qdrant instance"""
    # Use real infrastructure
    repo = QdrantDocumentRepository(qdrant_client)

    # Create document
    doc = Document.create("Test content", {"filename": "test.txt"})

    # Save
    doc_id = await repo.save(doc)

    # Retrieve
    retrieved = await repo.find_by_id(doc_id)

    assert retrieved.content.text == "Test content"
```

### E2E Tests (Full HTTP Flow)

```python
# tests/e2e/test_chat_api.py
@pytest.mark.e2e
async def test_chat_streaming(client, uploaded_document):
    """Test full streaming chat flow"""
    # Real HTTP request
    async with client.stream(
        "POST",
        "/chat/stream",
        json={"message": "What is the document about?"}
    ) as response:
        chunks = []
        async for chunk in response.aiter_text():
            chunks.append(chunk)

    assert len(chunks) > 0
    assert "document" in "".join(chunks).lower()
```

### Test Fixtures

```python
# tests/conftest.py
@pytest.fixture
def mock_embedding_service():
    """Mock embedding service for tests"""
    service = Mock(IEmbeddingService)
    service.embed_documents.return_value = [
        Embedding([0.1] * 1024) for _ in range(5)
    ]
    return service

@pytest.fixture
async def qdrant_client():
    """Real Qdrant client for integration tests"""
    client = QdrantClient(":memory:")  # In-memory for tests
    yield client
    await client.close()

@pytest.fixture
def test_settings():
    """Test configuration"""
    return Settings(
        fpt_api_key="test-key",
        qdrant_host="localhost",
        embedding_provider="fpt",
    )
```

---

## Summary

This Clean Architecture design provides:

1. **Clear Separation of Concerns**
   - Domain: Pure business logic
   - Application: Use case orchestration
   - Infrastructure: External integrations
   - API: HTTP interface

2. **Testability**
   - Mock infrastructure in unit tests
   - Test domain logic in isolation
   - Integration tests with real services

3. **Flexibility**
   - Swap providers via configuration
   - Add new providers easily
   - Extend without modifying existing code

4. **Maintainability**
   - Each component has single responsibility
   - Dependencies point inward
   - Business logic independent of frameworks

5. **Scalability**
   - Modular architecture
   - Easy to add new features
   - Support multiple deployment scenarios

**Next Steps:** Create detailed migration plan to transform current codebase to this architecture.
