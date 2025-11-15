# Prompt: Refactor RAG Project theo Clean Architecture + DDD

Hãy phân tích repo RAG hiện tại của tôi và refactor theo cấu trúc Clean Architecture kết hợp Domain-Driven Design với các yêu cầu sau:

## Mục tiêu Refactoring

### 1. Backend Structure (Clean Architecture)
- **API Layer** (Presentation): Định nghĩa routes, schemas, middleware
- **Core Layer** (Business Logic):
  - Domain: Entities, Value Objects, Domain Events
  - Use Cases: Business rules cụ thể (ProcessQuery, UploadDocument, etc.)
  - Interfaces: Abstract classes cho repositories, services
- **Infrastructure Layer**: 
  - AI implementations (embeddings, LLM, RAG pipeline)
  - Database repositories
  - Vector store integrations
  - External services
- **Services Layer**: Application services orchestrating use cases

### 2. Separation of Concerns
- Tách riêng AI/ML logic vào module độc lập
- Database models tách khỏi business entities
- API schemas tách khỏi domain models

### 3. Dependency Injection
- Sử dụng DI container (dependency-injector hoặc tương tự)
- Inject dependencies qua constructors
- Config-based switching giữa các providers (OpenAI/Anthropic, Pinecone/Qdrant)

### 4. Design Patterns
- **Repository Pattern**: Tất cả database access qua repositories
- **Strategy Pattern**: Cho LLM providers, embedding models, vector stores
- **Factory Pattern**: Tạo instances của AI services
- **Adapter Pattern**: Wrap external APIs

### 5. Testing Structure
- Unit tests cho use cases
- Integration tests cho infrastructure
- E2E tests cho API endpoints

## Yêu cầu cụ thể

1. **Phân tích codebase hiện tại**:
   - Xác định các components chính
   - Identify business logic vs infrastructure code
   - Map các dependencies hiện tại

2. **Đề xuất migration plan**:
   - Thứ tự refactor (ưu tiên critical paths)
   - Identify breaking changes
   - Backward compatibility strategy

3. **Tạo file structure mới**:
   - Detailed folder structure theo Clean Architecture
   - File placement cho từng component
   - Import path organization

4. **Refactor code**:
   - Di chuyển code vào đúng layers
   - Implement interfaces và abstractions
   - Setup dependency injection
   - Viết tests cho từng layer

5. **Configuration Management**:
   - Environment-based configs
   - Feature flags
   - Multi-provider support

6. **Documentation**:
   - Architecture decision records (ADRs)
   - API documentation
   - Developer guide

## Constraints
- Maintain existing API contracts (hoặc liệt kê breaking changes)
- Preserve current features
- Migration phải incremental, không break production
- Performance không được giảm

## Output mong muốn
1. Detailed migration plan với timeline
2. Refactored code structure
3. Updated documentation
4. Migration scripts nếu cần
5. Example implementations cho key patterns

Hãy bắt đầu với việc phân tích repo và đề xuất migration plan chi tiết.

# Prompt: Refactor RAG Project theo các tính năng
Hãy phân tích repo RAG hiện tại của tôi và refactor gồm những tính năng và techstack sau:
- Data Ingestion: https://docs.langchain.com/oss/python/integrations/document_loaders
- Search and Retrieval
    - Multi-collection searchability
    - Hybrid search with dense and sparse search
- Evaluation: Evaluation with https://docs.ragas.io/en/stable/
- Operations:
    - Observability with https://langfuse.com
    - OpenAI-compatible APIs
Hãy bắt đầu với việc phân tích repo và đề xuất migration plan chi tiết.
