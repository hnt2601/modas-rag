# Migration Plan: Clean Architecture Refactoring

> Version: 1.0
> Date: 2025-11-15
> Estimated Duration: 2.5 weeks (12 working days)
> Risk Level: LOW (no breaking changes, API not yet implemented)

## Table of Contents
1. [Migration Overview](#migration-overview)
2. [Phase-by-Phase Plan](#phase-by-phase-plan)
3. [Risk Assessment](#risk-assessment)
4. [Rollback Strategy](#rollback-strategy)
5. [Success Criteria](#success-criteria)
6. [Timeline](#timeline)

---

## Migration Overview

### Strategy: **Incremental Strangler Fig Pattern**

We'll build the new architecture alongside the existing code, gradually migrating components:

```
Current State          Migration           Target State
┌─────────────┐       ┌─────────────┐      ┌─────────────┐
│   Old Code  │  -->  │   New Code  │  --> │   New Code  │
│  (Partial)  │       │ + Old Code  │      │  (Complete) │
└─────────────┘       └─────────────┘      └─────────────┘
```

### Key Principles

1. **No Breaking Changes**: API not yet public, so we're free to refactor
2. **Incremental**: Build layer by layer, test at each step
3. **Backward Compatible**: Keep old code working until migration complete
4. **Test-Driven**: Write tests for each new component
5. **Documentation**: Update docs as we go

### Migration Approach

```
Phase 1: Foundation (Domain Layer)
   ↓
Phase 2: Contracts (Interfaces)
   ↓
Phase 3: Infrastructure (Adapters & Repositories)
   ↓
Phase 4: Business Logic (Use Cases)
   ↓
Phase 5: Dependency Injection (Container)
   ↓
Phase 6: API Layer (Routes)
   ↓
Phase 7: Testing & Cleanup
```

---

## Phase-by-Phase Plan

### Phase 1: Domain Layer Foundation (2 days)

**Goal:** Create pure domain entities and value objects with no dependencies

**Why First:** Domain has no external dependencies, safest to build first

#### Tasks

##### 1.1 Create Domain Structure (2 hours)
```bash
# Create folder structure
mkdir -p backend/domain/{entities,value_objects,interfaces,events,exceptions}
touch backend/domain/__init__.py
touch backend/domain/{entities,value_objects,interfaces,events,exceptions}/__init__.py
```

##### 1.2 Implement Value Objects (3 hours)
- `domain/value_objects/document_id.py` - UUID wrapper
- `domain/value_objects/content.py` - Text content
- `domain/value_objects/metadata.py` - Document metadata
- `domain/value_objects/embedding.py` - Vector wrapper
- `domain/value_objects/query_text.py` - Query text
- `domain/value_objects/score.py` - Relevance score

**Example:**
```python
# domain/value_objects/document_id.py
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True)
class DocumentId:
    value: UUID

    @classmethod
    def generate(cls) -> 'DocumentId':
        return cls(value=uuid4())

    @classmethod
    def from_string(cls, id_str: str) -> 'DocumentId':
        return cls(value=UUID(id_str))

    def __str__(self) -> str:
        return str(self.value)
```

**Tests:**
```python
# tests/unit/domain/value_objects/test_document_id.py
def test_document_id_generation():
    doc_id = DocumentId.generate()
    assert isinstance(doc_id.value, UUID)

def test_document_id_from_string():
    uuid_str = "123e4567-e89b-12d3-a456-426614174000"
    doc_id = DocumentId.from_string(uuid_str)
    assert str(doc_id) == uuid_str
```

##### 1.3 Implement Domain Exceptions (1 hour)
- `domain/exceptions/document_errors.py`
- `domain/exceptions/query_errors.py`
- `domain/exceptions/validation_errors.py`

```python
# domain/exceptions/document_errors.py
class DocumentError(Exception):
    """Base exception for document errors"""
    pass

class InvalidDocumentError(DocumentError):
    """Document validation failed"""
    pass

class DocumentNotFoundError(DocumentError):
    """Document not found"""
    pass
```

##### 1.4 Implement Entities (5 hours)
- `domain/entities/document.py` - Document entity with business logic
- `domain/entities/chunk.py` - Chunk value object
- `domain/entities/query.py` - Query entity
- `domain/entities/chat_message.py` - Chat message entity
- `domain/entities/search_result.py` - Search result

**Example:**
```python
# domain/entities/document.py
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

from domain.value_objects import DocumentId, Content, Metadata
from domain.exceptions import InvalidDocumentError

@dataclass
class Document:
    id: DocumentId
    content: Content
    metadata: Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    chunks: Optional[List['Chunk']] = None

    @classmethod
    def create(cls, content_text: str, metadata_dict: dict) -> 'Document':
        doc_id = DocumentId.generate()
        content = Content(content_text)
        metadata = Metadata.from_dict(metadata_dict)

        document = cls(id=doc_id, content=content, metadata=metadata)
        document.validate()
        return document

    def validate(self) -> None:
        if len(self.content.text) < 10:
            raise InvalidDocumentError("Document too short")
        if len(self.content.text) > 10_000_000:
            raise InvalidDocumentError("Document too large")

    def split_into_chunks(self, strategy: 'IChunkingStrategy') -> List['Chunk']:
        if self.chunks is not None:
            return self.chunks
        self.chunks = strategy.split(self.content, self.metadata)
        return self.chunks
```

**Tests:**
```python
# tests/unit/domain/entities/test_document.py
def test_document_creation():
    doc = Document.create("Valid content here", {"filename": "test.txt"})
    assert isinstance(doc.id, DocumentId)
    assert doc.content.text == "Valid content here"

def test_document_validation_too_short():
    with pytest.raises(InvalidDocumentError):
        Document.create("Short", {"filename": "test.txt"})

def test_document_validation_no_filename():
    with pytest.raises(InvalidDocumentError):
        Document.create("Valid content", {})
```

##### 1.5 Domain Events (1 hour)
- `domain/events/document_uploaded.py`
- `domain/events/query_processed.py`

```python
# domain/events/document_uploaded.py
from dataclasses import dataclass
from datetime import datetime
from domain.value_objects import DocumentId

@dataclass
class DocumentUploaded:
    document_id: DocumentId
    filename: str
    chunk_count: int
    occurred_at: datetime = field(default_factory=datetime.utcnow)
```

**Deliverables:**
- ✅ All value objects implemented with tests
- ✅ All entities implemented with tests
- ✅ Domain exceptions defined
- ✅ Domain events defined
- ✅ 100% test coverage for domain layer
- ✅ No external dependencies (pure Python)

**Acceptance Criteria:**
- [ ] All unit tests pass
- [ ] No imports from FastAPI, LangChain, or other frameworks
- [ ] Type hints on all public methods
- [ ] Docstrings on all classes and methods

---

### Phase 2: Domain Interfaces (1 day)

**Goal:** Define contracts (interfaces) for repositories and services

**Why Second:** Interfaces have no implementation, depend only on domain models

#### Tasks

##### 2.1 Repository Interfaces (2 hours)
- `domain/interfaces/repositories/document_repository.py`
- `domain/interfaces/repositories/vector_repository.py`

```python
# domain/interfaces/repositories/document_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities import Document
from domain.value_objects import DocumentId

class IDocumentRepository(ABC):
    @abstractmethod
    async def save(self, document: Document) -> DocumentId:
        pass

    @abstractmethod
    async def find_by_id(self, doc_id: DocumentId) -> Optional[Document]:
        pass

    @abstractmethod
    async def delete(self, doc_id: DocumentId) -> bool:
        pass

    @abstractmethod
    async def list_all(self, limit: int = 100) -> List[Document]:
        pass

    @abstractmethod
    async def search(self, query: str, top_k: int = 20) -> List[Document]:
        pass
```

##### 2.2 Service Interfaces (3 hours)
- `domain/interfaces/services/embedding_service.py`
- `domain/interfaces/services/llm_service.py`
- `domain/interfaces/services/reranker_service.py`
- `domain/interfaces/services/guard_service.py`
- `domain/interfaces/services/chunking_strategy.py`

```python
# domain/interfaces/services/embedding_service.py
from abc import ABC, abstractmethod
from typing import List

from domain.value_objects import Embedding

class IEmbeddingService(ABC):
    @abstractmethod
    async def embed_query(self, text: str) -> Embedding:
        """Generate embedding for a single query"""
        pass

    @abstractmethod
    async def embed_documents(self, texts: List[str]) -> List[Embedding]:
        """Generate embeddings for multiple documents"""
        pass

    @abstractmethod
    def get_dimensions(self) -> int:
        """Get embedding dimensions"""
        pass
```

```python
# domain/interfaces/services/llm_service.py
from abc import ABC, abstractmethod
from typing import AsyncIterator

class ILlmService(ABC):
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Generate a response"""
        pass

    @abstractmethod
    async def stream(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> AsyncIterator[str]:
        """Stream a response"""
        pass
```

##### 2.3 Strategy Interfaces (2 hours)
- `domain/interfaces/services/chunking_strategy.py`

```python
# domain/interfaces/services/chunking_strategy.py
from abc import ABC, abstractmethod
from typing import List

from domain.value_objects import Content, Metadata
from domain.entities import Chunk

class IChunkingStrategy(ABC):
    @abstractmethod
    def split(self, content: Content, metadata: Metadata) -> List[Chunk]:
        """Split content into chunks"""
        pass

    @abstractmethod
    def get_chunk_size(self) -> int:
        """Get configured chunk size"""
        pass

    @abstractmethod
    def get_overlap(self) -> int:
        """Get configured overlap"""
        pass
```

**Deliverables:**
- ✅ All repository interfaces defined
- ✅ All service interfaces defined
- ✅ Strategy interfaces defined
- ✅ Type hints using domain models only

**Acceptance Criteria:**
- [ ] All interfaces are abstract (ABC)
- [ ] All methods have clear docstrings
- [ ] No concrete implementations yet
- [ ] Type hints reference domain models only

---

### Phase 3: Infrastructure Layer (3 days)

**Goal:** Implement domain interfaces with external services

**Why Third:** Now we have contracts to implement against

#### Tasks

##### 3.1 Configuration Module (2 hours)
Refactor existing `core/config.py` into modular configs:

```python
# infrastructure/config/settings.py
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class AIConfig(BaseModel):
    fpt_api_key: str
    fpt_api_base: str = "https://api.fpt.ai/v1"
    embedding_model: str = "Vietnamese_Embedding"
    embedding_dimensions: int = 1024
    embedding_provider: str = "fpt"
    llm_model: str = "GLM-4.5"
    llm_temperature: float = 0.7
    llm_provider: str = "fpt"

class QdrantConfig(BaseModel):
    host: str = "localhost"
    port: int = 6333
    collection_name: str = "documents"
    grpc_port: int = 6334

class ChunkingConfig(BaseModel):
    chunk_size: int = 1000
    chunk_overlap: int = 200
    strategy: str = "recursive"

class FeatureFlags(BaseModel):
    enable_reranking: bool = True
    enable_guard: bool = True
    enable_caching: bool = False

class Settings(BaseSettings):
    ai: AIConfig
    qdrant: QdrantConfig
    chunking: ChunkingConfig
    features: FeatureFlags
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
```

##### 3.2 Embedding Adapters (4 hours)
Refactor `core/embeddings.py` into proper adapters:

```python
# infrastructure/ai/embeddings/fpt_embedding_adapter.py
from typing import List
from langchain_openai import OpenAIEmbeddings

from domain.interfaces import IEmbeddingService
from domain.value_objects import Embedding
from infrastructure.config import AIConfig
from shared.logger import get_logger

logger = get_logger(__name__)

class FptEmbeddingAdapter(IEmbeddingService):
    """FPT Cloud embedding service adapter"""

    def __init__(self, config: AIConfig):
        self._config = config
        self._client = OpenAIEmbeddings(
            api_key=config.fpt_api_key,
            base_url=config.fpt_api_base,
            model=config.embedding_model,
        )
        logger.info(f"Initialized FPT embedding adapter: {config.embedding_model}")

    async def embed_query(self, text: str) -> Embedding:
        try:
            vector = await self._client.aembed_query(text)
            return Embedding(vector)
        except Exception as e:
            logger.error(f"Failed to embed query: {e}")
            raise

    async def embed_documents(self, texts: List[str]) -> List[Embedding]:
        try:
            vectors = await self._client.aembed_documents(texts)
            return [Embedding(vector) for vector in vectors]
        except Exception as e:
            logger.error(f"Failed to embed documents: {e}")
            raise

    def get_dimensions(self) -> int:
        return self._config.embedding_dimensions
```

```python
# infrastructure/ai/embeddings/embedding_factory.py
from domain.interfaces import IEmbeddingService
from infrastructure.config import Settings
from infrastructure.ai.embeddings import FptEmbeddingAdapter

class EmbeddingFactory:
    @staticmethod
    def create(settings: Settings) -> IEmbeddingService:
        provider = settings.ai.embedding_provider

        if provider == "fpt":
            return FptEmbeddingAdapter(settings.ai)
        else:
            raise ValueError(f"Unknown embedding provider: {provider}")
```

##### 3.3 Chunking Strategy Implementation (3 hours)
```python
# infrastructure/document/recursive_chunking_strategy.py
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter

from domain.interfaces import IChunkingStrategy
from domain.value_objects import Content, Metadata, DocumentId
from domain.entities import Chunk
from infrastructure.config import ChunkingConfig

class RecursiveChunkingStrategy(IChunkingStrategy):
    def __init__(self, config: ChunkingConfig):
        self._config = config
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""],
        )

    def split(self, content: Content, metadata: Metadata) -> List[Chunk]:
        texts = self._splitter.split_text(content.text)

        chunks = []
        for idx, text in enumerate(texts):
            chunk_metadata = Metadata.from_dict({
                **metadata.to_dict(),
                "chunk_index": idx,
                "total_chunks": len(texts),
            })
            chunk = Chunk(
                text=text,
                metadata=chunk_metadata,
                chunk_index=idx,
                parent_document_id=metadata.document_id,
            )
            chunks.append(chunk)

        return chunks

    def get_chunk_size(self) -> int:
        return self._config.chunk_size

    def get_overlap(self) -> int:
        return self._config.chunk_overlap
```

##### 3.4 Vector Store Repository (5 hours)
```python
# infrastructure/persistence/vector_stores/qdrant_repository.py
from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from domain.interfaces import IDocumentRepository
from domain.entities import Document, Chunk
from domain.value_objects import DocumentId, Embedding
from infrastructure.config import QdrantConfig

class QdrantDocumentRepository(IDocumentRepository):
    def __init__(self, config: QdrantConfig):
        self._config = config
        self._client = QdrantClient(host=config.host, port=config.port)
        self._ensure_collection()

    def _ensure_collection(self):
        """Create collection if not exists"""
        collections = self._client.get_collections().collections
        if config.collection_name not in [c.name for c in collections]:
            self._client.create_collection(
                collection_name=config.collection_name,
                vectors_config=VectorParams(
                    size=1024,
                    distance=Distance.COSINE,
                ),
            )

    async def save(self, document: Document) -> DocumentId:
        """Save document with chunks to Qdrant"""
        if not document.chunks:
            raise ValueError("Document must have chunks before saving")

        points = []
        for chunk in document.chunks:
            if not hasattr(chunk, 'embedding'):
                raise ValueError("Chunk must have embedding before saving")

            point = PointStruct(
                id=str(uuid4()),
                vector=chunk.embedding.vector,
                payload={
                    "document_id": str(document.id),
                    "chunk_index": chunk.chunk_index,
                    "text": chunk.text,
                    "metadata": chunk.metadata.to_dict(),
                }
            )
            points.append(point)

        self._client.upsert(
            collection_name=self._config.collection_name,
            points=points,
        )

        return document.id

    async def find_by_id(self, doc_id: DocumentId) -> Optional[Document]:
        """Find document by ID"""
        # Query Qdrant for all chunks with this document_id
        results = self._client.scroll(
            collection_name=self._config.collection_name,
            scroll_filter={
                "must": [
                    {"key": "document_id", "match": {"value": str(doc_id)}}
                ]
            },
        )

        if not results[0]:
            return None

        # Reconstruct document from chunks
        # ... implementation details
```

##### 3.5 LLM Adapters (4 hours)
- `infrastructure/ai/llm/fpt_llm_adapter.py`
- `infrastructure/ai/llm/llm_factory.py`

##### 3.6 File System (2 hours)
- `infrastructure/file_system/document_loader.py` (refactor from embeddings.py)
- `infrastructure/file_system/file_validator.py`

**Deliverables:**
- ✅ All domain interfaces implemented
- ✅ Configuration refactored into modules
- ✅ Embedding service migrated from old code
- ✅ Chunking strategy implemented
- ✅ Qdrant repository implemented
- ✅ LLM adapters implemented
- ✅ Integration tests for all adapters

**Acceptance Criteria:**
- [ ] All adapters implement domain interfaces
- [ ] Integration tests pass with real Qdrant
- [ ] Configuration can switch providers
- [ ] Old `core/embeddings.py` code deprecated

---

### Phase 4: Application Layer (Use Cases) (2 days)

**Goal:** Implement business logic orchestration

#### Tasks

##### 4.1 Upload Document Use Case (4 hours)
```python
# application/use_cases/documents/upload_document.py
from dataclasses import dataclass
from typing import Optional

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
    content: str
    filename: str
    file_type: str
    user_id: Optional[str] = None

@dataclass
class UploadDocumentResponse:
    document_id: DocumentId
    chunk_count: int
    status: str

class UploadDocumentUseCase:
    def __init__(
        self,
        document_repository: IDocumentRepository,
        embedding_service: IEmbeddingService,
        chunking_strategy: IChunkingStrategy,
    ):
        self._repository = document_repository
        self._embedding_service = embedding_service
        self._chunking_strategy = chunking_strategy

    async def execute(self, request: UploadDocumentRequest) -> UploadDocumentResponse:
        # 1. Create domain entity
        metadata = {
            "filename": request.filename,
            "file_type": request.file_type,
            "user_id": request.user_id,
        }
        document = Document.create(request.content, metadata)

        # 2. Validate
        document.validate()

        # 3. Chunk
        chunks = document.split_into_chunks(self._chunking_strategy)

        # 4. Embed
        chunk_texts = [chunk.text for chunk in chunks]
        embeddings = await self._embedding_service.embed_documents(chunk_texts)

        # 5. Attach embeddings
        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = embedding

        # 6. Save
        doc_id = await self._repository.save(document)

        # 7. Return
        return UploadDocumentResponse(
            document_id=doc_id,
            chunk_count=len(chunks),
            status="success",
        )
```

**Tests:**
```python
# tests/unit/application/use_cases/test_upload_document.py
@pytest.mark.asyncio
async def test_upload_document_success(
    mock_repository,
    mock_embedding_service,
    mock_chunking_strategy,
):
    use_case = UploadDocumentUseCase(
        mock_repository,
        mock_embedding_service,
        mock_chunking_strategy,
    )

    request = UploadDocumentRequest(
        content="Valid content here",
        filename="test.pdf",
        file_type="application/pdf",
    )

    result = await use_case.execute(request)

    assert result.status == "success"
    assert result.chunk_count > 0
    mock_repository.save.assert_called_once()
```

##### 4.2 Process Query Use Case (6 hours)
- `application/use_cases/chat/process_query.py`
- Implement full RAG pipeline

##### 4.3 Other Use Cases (4 hours)
- `application/use_cases/documents/delete_document.py`
- `application/use_cases/documents/list_documents.py`

**Deliverables:**
- ✅ All use cases implemented
- ✅ Unit tests for all use cases with mocks
- ✅ Clear separation from infrastructure

**Acceptance Criteria:**
- [ ] Use cases only depend on domain interfaces
- [ ] All unit tests pass (100% coverage)
- [ ] No direct infrastructure dependencies

---

### Phase 5: Dependency Injection (1 day)

**Goal:** Setup DI container for automatic dependency wiring

#### Tasks

##### 5.1 Install DI Library (15 minutes)
```bash
# Add to requirements.txt
dependency-injector==4.41.0
```

##### 5.2 Create Container (3 hours)
```python
# api/dependencies/container.py
from dependency_injector import containers, providers

from infrastructure.config import Settings
from infrastructure.ai.embeddings import EmbeddingFactory
from infrastructure.ai.llm import LlmFactory
from infrastructure.persistence.vector_stores import VectorStoreFactory
from infrastructure.document import ChunkingStrategyFactory
from application.use_cases import (
    UploadDocumentUseCase,
    ProcessQueryUseCase,
    DeleteDocumentUseCase,
    ListDocumentsUseCase,
)

class Container(containers.DeclarativeContainer):
    # Config
    config = providers.Singleton(Settings)

    # Infrastructure - AI Services
    embedding_service = providers.Singleton(
        EmbeddingFactory.create,
        settings=config,
    )

    llm_service = providers.Singleton(
        LlmFactory.create,
        settings=config,
    )

    # Infrastructure - Repositories
    document_repository = providers.Singleton(
        VectorStoreFactory.create_document_repository,
        settings=config,
    )

    # Infrastructure - Strategies
    chunking_strategy = providers.Singleton(
        ChunkingStrategyFactory.create,
        settings=config,
    )

    # Use Cases
    upload_document_use_case = providers.Factory(
        UploadDocumentUseCase,
        document_repository=document_repository,
        embedding_service=embedding_service,
        chunking_strategy=chunking_strategy,
    )

    process_query_use_case = providers.Factory(
        ProcessQueryUseCase,
        document_repository=document_repository,
        embedding_service=embedding_service,
        llm_service=llm_service,
    )

    delete_document_use_case = providers.Factory(
        DeleteDocumentUseCase,
        document_repository=document_repository,
    )

    list_documents_use_case = providers.Factory(
        ListDocumentsUseCase,
        document_repository=document_repository,
    )
```

##### 5.3 FastAPI Integration (2 hours)
```python
# api/dependencies/use_case_providers.py
from fastapi import Depends
from api.dependencies.container import Container

# Global container
container = Container()

# Dependency providers
def get_upload_use_case():
    return container.upload_document_use_case()

def get_process_query_use_case():
    return container.process_query_use_case()

def get_delete_document_use_case():
    return container.delete_document_use_case()

def get_list_documents_use_case():
    return container.list_documents_use_case()
```

##### 5.4 Update main.py (1 hour)
```python
# main.py
from fastapi import FastAPI
from api.dependencies.container import Container

def create_app() -> FastAPI:
    # Initialize container
    container = Container()
    container.wire(modules=["api.routes.chat", "api.routes.documents"])

    app = FastAPI(title="MODAS RAG API")

    # Include routers
    from api.routes import chat, documents, health
    app.include_router(chat.router)
    app.include_router(documents.router)
    app.include_router(health.router)

    return app

app = create_app()
```

**Deliverables:**
- ✅ DI container configured
- ✅ All dependencies wired automatically
- ✅ Provider switching via configuration

**Acceptance Criteria:**
- [ ] Container can create all use cases
- [ ] Configuration can switch providers
- [ ] No manual dependency instantiation in routes

---

### Phase 6: API Layer (2 days)

**Goal:** Implement FastAPI routes using new architecture

#### Tasks

##### 6.1 API Schemas (2 hours)
Refactor `models/schemas.py` into API-specific DTOs:

```python
# api/schemas/document_schemas.py
from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime

class DocumentUploadRequest(BaseModel):
    # Handled by FastAPI UploadFile
    pass

class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    metadata: Dict[str, Any]

    @classmethod
    def from_use_case_response(cls, response, filename: str):
        return cls(
            document_id=str(response.document_id),
            filename=filename,
            status=response.status,
            metadata={"chunk_count": response.chunk_count},
        )

class DocumentInfo(BaseModel):
    document_id: str
    filename: str
    created_at: str
    chunk_count: int

class DocumentListResponse(BaseModel):
    documents: List[DocumentInfo]
    total: int
```

##### 6.2 Mappers (2 hours)
```python
# api/mappers/document_mapper.py
from domain.entities import Document
from api.schemas import DocumentInfo

class DocumentMapper:
    @staticmethod
    def to_api(document: Document) -> DocumentInfo:
        return DocumentInfo(
            document_id=str(document.id),
            filename=document.metadata.filename,
            created_at=document.created_at.isoformat(),
            chunk_count=document.get_chunk_count(),
        )
```

##### 6.3 Document Routes (4 hours)
```python
# api/routes/documents.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List

from api.schemas import DocumentUploadResponse, DocumentListResponse
from api.dependencies import (
    get_upload_use_case,
    get_list_use_case,
    get_delete_use_case,
)
from api.mappers import DocumentMapper
from application.use_cases import (
    UploadDocumentUseCase,
    UploadDocumentRequest,
    ListDocumentsUseCase,
    DeleteDocumentUseCase,
)

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    use_case: UploadDocumentUseCase = Depends(get_upload_use_case),
):
    # Validate file
    if file.size > 50 * 1024 * 1024:
        raise HTTPException(400, "File too large (max 50MB)")

    # Read content
    content = await file.read()
    content_text = content.decode('utf-8')

    # Execute use case
    request = UploadDocumentRequest(
        content=content_text,
        filename=file.filename,
        file_type=file.content_type,
    )

    result = await use_case.execute(request)

    # Map to response
    return DocumentUploadResponse.from_use_case_response(result, file.filename)

@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    use_case: ListDocumentsUseCase = Depends(get_list_use_case),
):
    documents = await use_case.execute()
    return DocumentListResponse(
        documents=[DocumentMapper.to_api(doc) for doc in documents],
        total=len(documents),
    )

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    use_case: DeleteDocumentUseCase = Depends(get_delete_use_case),
):
    from domain.value_objects import DocumentId
    doc_id = DocumentId.from_string(document_id)
    success = await use_case.execute(doc_id)

    if not success:
        raise HTTPException(404, "Document not found")

    return {"status": "deleted"}
```

##### 6.4 Chat Routes (6 hours)
- `api/routes/chat.py` - Implement streaming chat endpoint

##### 6.5 Middleware (2 hours)
- `api/middleware/error_handler.py` - Global error handling
- `api/middleware/logging.py` - Request/response logging

**Deliverables:**
- ✅ All API endpoints implemented
- ✅ Thin controllers (no business logic)
- ✅ Proper error handling
- ✅ Request/response logging

**Acceptance Criteria:**
- [ ] All endpoints use dependency injection
- [ ] Controllers delegate to use cases
- [ ] API schemas map to/from domain models
- [ ] Error handling with proper status codes

---

### Phase 7: Testing & Documentation (2 days)

**Goal:** Comprehensive testing and documentation

#### Tasks

##### 7.1 Unit Tests (4 hours)
- Ensure 100% coverage for domain and application layers
- Add missing test cases

##### 7.2 Integration Tests (4 hours)
```python
# tests/integration/test_qdrant_repository.py
@pytest.mark.integration
async def test_document_save_and_retrieve(qdrant_client):
    config = QdrantConfig(host="localhost", port=6333)
    repo = QdrantDocumentRepository(config)

    # Create document
    doc = Document.create("Test content", {"filename": "test.txt"})
    chunks = doc.split_into_chunks(RecursiveChunkingStrategy(...))

    # Embed
    embeddings = [Embedding([0.1] * 1024) for _ in chunks]
    for chunk, emb in zip(chunks, embeddings):
        chunk.embedding = emb

    # Save
    doc_id = await repo.save(doc)

    # Retrieve
    retrieved = await repo.find_by_id(doc_id)
    assert retrieved.content.text == "Test content"
```

##### 7.3 E2E Tests (4 hours)
```python
# tests/e2e/test_document_api.py
@pytest.mark.e2e
async def test_upload_document_flow(client):
    # Upload
    with open("test.pdf", "rb") as f:
        response = await client.post(
            "/documents/upload",
            files={"file": ("test.pdf", f, "application/pdf")}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    doc_id = data["document_id"]

    # List
    response = await client.get("/documents/")
    assert doc_id in [doc["document_id"] for doc in response.json()["documents"]]

    # Delete
    response = await client.delete(f"/documents/{doc_id}")
    assert response.status_code == 200
```

##### 7.4 Architecture Decision Records (2 hours)
- `docs/adr/001-clean-architecture.md`
- `docs/adr/002-dependency-injection.md`
- `docs/adr/003-repository-pattern.md`

##### 7.5 API Documentation (2 hours)
- Update OpenAPI docs
- Add examples and descriptions
- Document error responses

##### 7.6 Developer Guide (2 hours)
- `docs/developer-guide.md` - How to add new features
- `docs/testing-guide.md` - How to write tests
- `docs/deployment-guide.md` - How to deploy

**Deliverables:**
- ✅ 90%+ test coverage
- ✅ All integration tests pass
- ✅ E2E tests for critical paths
- ✅ Complete documentation

**Acceptance Criteria:**
- [ ] All tests pass in CI
- [ ] Coverage >= 90%
- [ ] ADRs document key decisions
- [ ] Developer guide complete

---

## Risk Assessment

### Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Performance degradation | Low | Medium | Benchmark after each phase |
| Integration issues with Qdrant | Medium | High | Integration tests early |
| DI container complexity | Low | Medium | Start simple, iterate |
| Breaking existing frontend | Very Low | High | API contracts maintained |
| Over-engineering | Medium | Low | YAGNI principle, iterate |

### Schedule Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Scope creep | Medium | High | Stick to plan, defer nice-to-haves |
| Underestimated complexity | Medium | Medium | 20% buffer in estimates |
| Blockers on infrastructure | Low | High | Test infrastructure early |

### Migration Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Lost work (no backup) | Very Low | Critical | Git branches, frequent commits |
| Incomplete migration | Low | High | Phase-by-phase validation |
| Technical debt increases | Medium | Medium | Code reviews, refactor as we go |

---

## Rollback Strategy

### Per-Phase Rollback

Each phase is isolated, so rollback is simple:

1. **Domain Layer**: No dependencies, safe to remove
2. **Interfaces**: Just definitions, safe to remove
3. **Infrastructure**: Keep old code until fully migrated
4. **Use Cases**: Can coexist with old code
5. **DI Container**: Optional, can use manual wiring
6. **API Layer**: Can revert to direct infrastructure calls

### Git Strategy

```bash
# Main branch: stable
main

# Feature branch for migration
feature/clean-architecture-migration
  ├─ phase-1-domain
  ├─ phase-2-interfaces
  ├─ phase-3-infrastructure
  ├─ phase-4-use-cases
  ├─ phase-5-di
  ├─ phase-6-api
  └─ phase-7-testing

# Merge strategy: squash merge each phase after validation
```

### Validation Checklist (Per Phase)

- [ ] All tests pass
- [ ] No regressions in existing functionality
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Performance benchmarks acceptable

---

## Success Criteria

### Technical Success Metrics

1. **Code Quality**
   - [ ] Test coverage >= 90%
   - [ ] No circular dependencies
   - [ ] Type hints on all public APIs
   - [ ] Linting passes (Ruff, MyPy)

2. **Architecture**
   - [ ] Clear layer separation
   - [ ] Dependencies point inward
   - [ ] All interfaces implemented
   - [ ] No framework dependencies in domain

3. **Functionality**
   - [ ] All existing features work
   - [ ] New features (chat, documents) implemented
   - [ ] API endpoints functional
   - [ ] Streaming works

4. **Performance**
   - [ ] Response time < 2s for queries
   - [ ] Document upload < 10s for 10MB file
   - [ ] No memory leaks

5. **Flexibility**
   - [ ] Can switch LLM providers via config
   - [ ] Can switch vector stores via config
   - [ ] Can add new chunking strategies easily

### Business Success Metrics

1. **Development Velocity**
   - [ ] New features take < 50% of pre-refactor time
   - [ ] Bugs reduced by 30%

2. **Maintainability**
   - [ ] Onboarding time for new devs < 2 days
   - [ ] Code review time < 1 hour per PR

3. **Reliability**
   - [ ] Zero production incidents related to architecture
   - [ ] 99.9% uptime

---

## Timeline

### Gantt Chart

```
Week 1
├─ Mon-Tue: Phase 1 (Domain Layer)
├─ Wed: Phase 2 (Interfaces)
└─ Thu-Fri: Phase 3 Start (Infrastructure)

Week 2
├─ Mon: Phase 3 Finish (Infrastructure)
├─ Tue-Wed: Phase 4 (Use Cases)
├─ Thu: Phase 5 (DI)
└─ Fri: Phase 6 Start (API)

Week 3
├─ Mon: Phase 6 Finish (API)
├─ Tue-Wed: Phase 7 (Testing)
├─ Thu: Documentation & Cleanup
└─ Fri: Buffer & Final Review
```

### Detailed Schedule

| Day | Phase | Tasks | Hours |
|-----|-------|-------|-------|
| **Day 1** | Phase 1 | Value objects, exceptions | 8h |
| **Day 2** | Phase 1 | Entities, events, tests | 8h |
| **Day 3** | Phase 2 | All interfaces | 7h |
| **Day 4** | Phase 3 | Config, embedding adapters | 8h |
| **Day 5** | Phase 3 | Chunking, vector store | 8h |
| **Day 6** | Phase 3 | LLM adapters, file system | 6h |
| **Day 7** | Phase 4 | Upload use case | 4h |
| **Day 8** | Phase 4 | Query use case, others | 10h |
| **Day 9** | Phase 5 | DI container setup | 6h |
| **Day 10** | Phase 6 | API schemas, routes | 8h |
| **Day 11** | Phase 6 | Chat routes, middleware | 8h |
| **Day 12** | Phase 7 | Testing (all levels) | 8h |
| **Day 13** | Phase 7 | Documentation & ADRs | 6h |
| **Day 14** | Buffer | Cleanup, final review | 4h |

**Total Estimated Hours:** 99 hours (~12.5 working days)

**Buffer:** 20% (2.5 days built into 14-day timeline)

---

## Post-Migration Checklist

### Code Cleanup

- [ ] Remove old `core/embeddings.py`
- [ ] Remove old `models/schemas.py`
- [ ] Remove old `core/config.py`
- [ ] Remove unused imports
- [ ] Run linter and fix all warnings

### Documentation

- [ ] Update README.md with new architecture
- [ ] Update PROGRESS.md
- [ ] Create architecture diagram
- [ ] Document all ADRs
- [ ] Update API documentation

### Testing

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass
- [ ] Performance benchmarks documented
- [ ] Load testing completed

### Deployment

- [ ] Update Dockerfile if needed
- [ ] Update K8s manifests if needed
- [ ] Test deployment to staging
- [ ] Create deployment runbook

### Knowledge Transfer

- [ ] Team walkthrough of new architecture
- [ ] Developer guide reviewed
- [ ] Q&A session
- [ ] Code review checklist updated

---

## Next Steps

1. **Review and Approve Plan** ✓
2. **Setup Git Branch** - `feature/clean-architecture-migration`
3. **Begin Phase 1** - Domain layer implementation
4. **Daily Stand-ups** - Track progress, address blockers
5. **Phase Reviews** - Validate before moving to next phase

**Ready to start implementation?**

Once approved, we'll begin with Phase 1: Domain Layer Foundation.
