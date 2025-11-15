# Current Architecture Analysis

> Generated: 2025-11-15
>
> Status: RAG Application ~30% Complete

## Executive Summary

The MODAS RAG application is a well-architected system with strong foundations but incomplete implementation. Current code shows production-ready patterns (health checks, type safety, logging) but lacks core RAG functionality (retrieval, reranking, generation).

### Current State
- ✅ **Frontend**: 100% Complete - Production-ready React app with streaming
- ⚠️ **Backend**: 30% Complete - Foundation ready, core logic missing
- ✅ **K8s**: 100% Complete - Production manifests with HA
- ⚠️ **Overall Maturity**: ~30% Complete

---

## 1. Current Architecture Pattern

### Overall Pattern: **Functional Service-Oriented**

```
┌─────────────────────────────────────────────────────────┐
│                     CURRENT STRUCTURE                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐                                       │
│  │   main.py    │  ← Entry point (FastAPI app)          │
│  └──────┬───────┘                                       │
│         │                                                │
│         ├─→ core/config.py       (Settings)             │
│         ├─→ core/embeddings.py   (Functions)            │
│         ├─→ models/schemas.py    (Pydantic models)      │
│         └─→ utils/logger.py      (Logger)               │
│                                                          │
│  ┌──────────────┐                                       │
│  │  api/ (EMPTY)│  ← TODO: Routes not implemented       │
│  └──────────────┘                                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Issues with Current Architecture

1. **No Layer Separation**
   - Business logic mixed with infrastructure (embeddings.py)
   - No clear boundaries between layers
   - Direct dependencies on external services

2. **Functional Programming Only**
   - No OOP abstractions
   - No interfaces/protocols
   - Hard to test and swap implementations

3. **No Dependency Injection**
   - Global settings import
   - Tight coupling to FPT Cloud
   - Can't easily switch providers

4. **No Repository Pattern**
   - Direct database access (when implemented)
   - No abstraction for data persistence

5. **Incomplete Implementation**
   - Core RAG logic missing
   - API endpoints not implemented
   - No integration between components

---

## 2. Component Categorization

### A. Business Logic (Domain/Use Cases)

**Currently Mixed/Not Separated:**

```python
# embeddings.py - INFRASTRUCTURE masquerading as business logic
async def process_document(file_path: str):
    """Should be a Use Case, not an infrastructure function"""
    docs = load_document(file_path)        # Infrastructure
    chunks = split_documents(docs)         # Domain/Use Case
    embeddings = await embed_documents()   # Infrastructure
    return result
```

**Actual Business Logic (Implicit):**
- Document validation rules (schemas.py)
- Text chunking strategy (embeddings.py)
- RAG pipeline orchestration (TODO)
- Query processing (TODO)

**Should Be Domain Entities:**
- `Document` - With content, metadata, chunks
- `Query` - With text, filters, context
- `ChatMessage` - With role, content, sources
- `Embedding` - Value object for vectors
- `SearchResult` - With score, document, metadata

**Should Be Use Cases:**
- `UploadDocumentUseCase` - Validates, processes, stores
- `ProcessQueryUseCase` - Embeds, searches, ranks, generates
- `DeleteDocumentUseCase` - Removes from vector store
- `ListDocumentsUseCase` - Retrieves document list

### B. Infrastructure Code

**Currently Implemented:**
```python
# core/embeddings.py
- get_embeddings()           # FPT Cloud client
- embed_query()              # API call
- embed_documents()          # Batch API call
- load_document()            # File I/O
- split_documents()          # Text processing

# core/config.py
- Settings class             # Environment config
- Pydantic validation        # Config validation
```

**Should Be Infrastructure:**
- `FptEmbeddingProvider` - Implements `IEmbeddingProvider`
- `QdrantVectorStore` - Implements `IVectorStore`
- `GlmLlmProvider` - Implements `ILlmProvider`
- `BgeReranker` - Implements `IReranker`
- `LlamaGuard` - Implements `IGuard`
- `DocumentFileRepository` - Implements `IDocumentRepository`

### C. API Schemas vs Domain Models

**Current Issue: Only API Schemas Exist**

```python
# models/schemas.py - Pydantic models
class ChatRequest(BaseModel):
    """This is an API schema, NOT a domain model"""
    message: str = Field(..., min_length=1, max_length=2000)

class DocumentInfo(BaseModel):
    """This is a data transfer object, NOT a domain entity"""
    document_id: str
    filename: str
```

**Should Be Separated:**

```python
# domain/entities.py - Domain models
class Document:
    """Rich domain entity with behavior"""
    def __init__(self, id: DocumentId, content: str, ...):
        self.id = id
        self.validate_content()

    def split_into_chunks(self, strategy: ChunkingStrategy) -> List[Chunk]:
        """Domain logic belongs here"""

# api/schemas.py - DTOs for API layer
class DocumentUploadRequest(BaseModel):
    """Thin API contract"""
    file: UploadFile

class DocumentResponse(BaseModel):
    """Serialization for API"""
    @classmethod
    def from_entity(cls, doc: Document):
        """Map from domain to DTO"""
```

---

## 3. Current Dependencies Map

### Dependency Direction (Current)

```
main.py
   ↓ (imports)
core/config.py ←────┐
core/embeddings.py  │ (circular risk)
   ↓                │
models/schemas.py ──┘
```

**Problems:**
- No dependency inversion
- Concrete implementations at top level
- Can't swap providers without code changes
- Hard to test (no mocking points)

### External Dependencies

```
Backend Code
   ↓
LangChain → OpenAI API Protocol → FPT Cloud
   ↓
Qdrant Client → Qdrant Server
   ↓
FastAPI → Uvicorn → HTTP
```

**Issues:**
- Direct coupling to LangChain
- Hard-coded to OpenAI protocol
- No abstraction layer for external services

---

## 4. Data Flow Analysis

### Current Data Flow (Partial)

```
┌──────────────┐
│   Frontend   │
│  (Complete)  │
└───────┬──────┘
        │ HTTP POST /chat/stream (TODO endpoint)
        ↓
┌──────────────┐
│   main.py    │ ← Entry point
│   (Partial)  │
└───────┬──────┘
        │
        ├─→ Validate with schemas.py ✓
        │
        ├─→ api/chat.py (MISSING)
        │        │
        │        ↓
        │   core/embeddings.py ✓
        │        │
        │        ↓
        │   core/retriever.py (TODO)
        │        │
        │        ↓
        │   core/reranker.py (TODO)
        │        │
        │        ↓
        │   core/rag.py (TODO)
        │        │
        │        ↓
        │   Stream response (TODO)
        │
        ✗ Endpoint not implemented
```

### Ideal Data Flow (Clean Architecture)

```
API Layer (Presentation)
   ↓ (DTO)
Application Layer (Use Cases)
   ↓ (Domain Models)
Domain Layer (Entities, Interfaces)
   ↑ (Implements)
Infrastructure Layer (AI, DB, Vector Stores)
```

**Key Difference:**
- Current: Direct calls from API → Infrastructure
- Ideal: API → Use Case → Domain ← Infrastructure (inverted)

---

## 5. Testing Gaps

### Current Test Coverage: ~5%

**Existing:**
- `test_embeddings.py` - Basic embedding tests

**Missing:**
1. **Unit Tests**
   - No domain logic tests (entities don't exist)
   - No use case tests (use cases don't exist)
   - No validation tests

2. **Integration Tests**
   - No API endpoint tests (endpoints don't exist)
   - No database integration tests
   - No vector store tests

3. **E2E Tests**
   - No full RAG pipeline tests
   - No streaming tests
   - No error handling tests

4. **Test Infrastructure**
   - No pytest fixtures
   - No mocking utilities
   - No test configuration

---

## 6. Configuration Management Analysis

### Current Approach: **Centralized Pydantic Settings**

**Strengths:**
- Type-safe configuration
- Validation at startup
- Environment variable support
- Single source of truth

**Weaknesses:**
- Monolithic settings class (120 lines)
- No feature flags support
- No multi-provider switching
- No runtime reconfiguration

**Current Structure:**
```python
# core/config.py
class Settings(BaseSettings):
    # All configs in one class
    fpt_api_key: str
    qdrant_host: str
    chunk_size: int
    # ... 30+ fields
```

**Should Be:**
```python
# Multiple specialized configs
class FptConfig(BaseModel): ...
class QdrantConfig(BaseModel): ...
class RagConfig(BaseModel): ...

# Feature flags
class FeatureFlags(BaseModel):
    enable_reranking: bool = True
    enable_guard: bool = True

# Provider selection
class ProviderConfig(BaseModel):
    llm_provider: Literal["fpt", "openai", "anthropic"]
    vector_store: Literal["qdrant", "pinecone"]
```

---

## 7. Key Findings Summary

### Strengths
1. ✅ Solid foundation (FastAPI, Pydantic, type safety)
2. ✅ Production-ready patterns (health checks, logging, error handling)
3. ✅ Modern stack and tooling
4. ✅ Kubernetes-ready with HA configuration
5. ✅ Vietnamese language optimization

### Critical Gaps
1. ❌ No layer separation (Clean Architecture)
2. ❌ No domain models (DDD)
3. ❌ No dependency injection
4. ❌ No repository pattern
5. ❌ No strategy pattern for providers
6. ❌ No testing structure
7. ❌ Core RAG logic missing (~70% of functionality)

### Technical Debt
1. Functional programming limits scalability
2. Hard-coded dependencies
3. No abstraction for external services
4. Configuration not modular enough
5. No CI/CD pipeline

### Business Logic vs Infrastructure
**Current Split:** ~80% Infrastructure, 20% Business Logic
**Ideal Split:** 60% Business Logic, 40% Infrastructure

**Current Location of Business Logic:**
- Scattered in `embeddings.py` (should be Use Cases)
- Mixed with infrastructure concerns
- No rich domain models

---

## 8. Migration Complexity Assessment

### Low Complexity (Safe Refactor)
- ✅ Extract configuration into modules
- ✅ Create domain entities from schemas
- ✅ Add interfaces/protocols

### Medium Complexity
- ⚠️ Implement repository pattern
- ⚠️ Add dependency injection
- ⚠️ Create use cases layer
- ⚠️ Implement strategy pattern

### High Complexity
- 🔴 Refactor embeddings.py into proper layers
- 🔴 Build complete RAG pipeline with new architecture
- 🔴 Migrate all future API endpoints to use new structure

### Risk Assessment

**Breaking Changes:**
- None (API endpoints not yet implemented)
- No existing users or data

**Migration Risk:** **LOW**
- Can refactor without breaking anything
- No backward compatibility needed
- Green field for API implementation

**Timeline Estimate:**
- Planning & Design: 1 day
- Core Domain Layer: 2 days
- Infrastructure Layer: 3 days
- Use Cases Layer: 2 days
- API Layer: 2 days
- Testing Setup: 2 days
- **Total: ~12 working days** (2.5 weeks)

---

## Next Steps

1. Design Clean Architecture structure
2. Create detailed migration plan with phases
3. Implement core domain layer
4. Refactor infrastructure layer
5. Build use cases
6. Setup DI container
7. Implement API endpoints with new architecture
8. Add comprehensive testing

**Priority:** Start with domain layer (entities, value objects, interfaces) as this has no dependencies on existing code.
