# RAG System Development Prompt for Cursor AI

## 🎯 Project Overview

I need you to help me build a production-ready RAG (Retrieval-Augmented Generation) system based on the architecture documentation in `@architecture.md`. The system must follow enterprise best practices and be ready for Kubernetes deployment.

## 📋 Tech Stack (Reference @architecture.md)

**Frontend:**
- React 18+ with TypeScript
- Ant Design 5.x (Design System - MUST follow strictly)
- TanStack Query for data fetching
- Zustand for state management
- Vite as build tool
- Axios for API calls

**Backend:**
- FastAPI with Python 3.10+
- Pydantic for data validation
- LangChain with OpenAI-compatible interface
- Async/await patterns throughout

**AI Models (FPT Cloud):**
- Vietnamese_Embedding (AITeamVN) - 1024 dimensions
- GLM-4.5 (Z.ai) - LLM
- bge-reranker-v2-m3 (BAAI) - Reranker
- Llama-Guard-3-8B (Meta) - Safety

**Infrastructure:**
- Qdrant (Vector Database)
- Redis (Caching)
- Kubernetes (Deployment)

## 🏗️ Build Order & Requirements

### Phase 1: Backend Core (Start Here)

#### 1.1 Setup Backend Structure
```
Please create the FastAPI backend with the following structure:

backend/
├── main.py                 # FastAPI app entry point
├── api/
│   ├── __init__.py
│   ├── chat.py            # Chat endpoints
│   └── documents.py       # Document management endpoints
├── core/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── embeddings.py      # Vietnamese Embedding integration
│   ├── retriever.py       # Qdrant retriever
│   ├── reranker.py        # BGE Reranker
│   ├── guard.py           # Llama Guard safety
│   └── rag.py             # Complete RAG pipeline
├── models/
│   ├── __init__.py
│   └── schemas.py         # Pydantic models
├── utils/
│   ├── __init__.py
│   └── logger.py          # Logging configuration
├── requirements.txt
├── Dockerfile
└── .env.example

Requirements:
- Use async/await throughout
- Follow FastAPI best practices
- Implement proper error handling
- Add comprehensive logging
- Include Pydantic models for all requests/responses
- Add CORS middleware
- Implement health check endpoint at /health
```

#### 1.2 Core Configuration (core/config.py)
```
Create a Pydantic BaseSettings configuration class with:
- FPT_API_KEY (from environment)
- QDRANT_HOST and QDRANT_PORT
- REDIS_HOST and REDIS_PORT
- LOG_LEVEL
- MAX_UPLOAD_SIZE
- CHUNK_SIZE and CHUNK_OVERLAP
- Support for .env files
```

#### 1.3 Vietnamese Embedding Service (core/embeddings.py)
```
Implement the Vietnamese Embedding service with:
- Use langchain_openai.OpenAIEmbeddings
- Configure for FPT Cloud API (model: "Vietnamese_Embedding")
- Return 1024-dimension vectors
- Support batch processing
- Handle document chunking with RecursiveCharacterTextSplitter
- Support PDF, DOCX, TXT, MD file formats
- Async implementation
```

#### 1.4 Qdrant Retriever (core/retriever.py)
```
Create QdrantRetriever class with:
- Initialize Qdrant client
- Create collection with 1024 dimensions, cosine distance
- Methods:
  - add_documents(texts, metadata) -> async
  - search(query, k=5, filter_dict=None) -> List[Document]
  - get_all_documents() -> List[dict]
  - delete_document(doc_id) -> async
- Proper error handling
- Return LangChain Document objects
```

#### 1.5 Reranker Service (core/reranker.py)
```
Create FPTReranker class with:
- Use FPT Cloud API for bge-reranker-v2-m3
- Method: rerank(query, documents, top_n=5)
- Return reranked documents with scores
- Handle API errors gracefully
- Use requests or httpx library
```

#### 1.6 Guard Service (core/guard.py)
```
Create LlamaGuard class with:
- Use langchain_openai.ChatOpenAI with Llama-Guard-3-8B model
- Methods:
  - check_input(user_query) -> bool
  - check_output(ai_response) -> bool
  - get_safety_report(text) -> dict
- Safety categories: Violence, Sexual, Criminal, Dangerous, Self-Harm
- Temperature: 0 (deterministic)
```

#### 1.7 Complete RAG Pipeline (core/rag.py)
```
Create RAGPipeline class that orchestrates:
1. Input Guard (Llama Guard)
2. Retrieval (Qdrant with Vietnamese Embedding) - top 20
3. Reranking (BGE Reranker) - top 5
4. Generation (GLM-4.5)
5. Output Guard (Llama Guard)

Methods:
- __init__(): Initialize all components
- get_response(query: str) -> str: Full pipeline
- stream_response(query: str) -> AsyncGenerator: Streaming version

Use langchain_openai.ChatOpenAI for GLM-4.5
Include Vietnamese prompt template
```

#### 1.8 API Endpoints (api/chat.py & api/documents.py)
```
api/chat.py - Create endpoints:
- POST /chat/simple: Non-streaming chat
- POST /chat/stream: Server-Sent Events streaming
- Include proper error responses

api/documents.py - Create endpoints:
- POST /documents/upload: File upload with validation
- GET /documents/list: List all documents
- DELETE /documents/{doc_id}: Delete document
- Use FastAPI's UploadFile
- Save files temporarily, process async
- Return proper status codes
```

#### 1.9 Main Application (main.py)
```
Create FastAPI application with:
- CORS middleware (allow all origins for dev)
- Include routers from api/
- Health check endpoint: GET /health
- Exception handlers
- Startup/shutdown events
- API documentation at /docs
- Proper logging setup
```

### Phase 2: Frontend with Ant Design (After Backend is Working)

#### 2.1 Setup Frontend Structure
```
Create React + TypeScript + Ant Design application:

frontend/
├── src/
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   └── MessageInput.tsx
│   │   ├── documents/
│   │   │   ├── DocumentUpload.tsx
│   │   │   ├── DocumentList.tsx
│   │   │   └── DocumentCard.tsx
│   │   ├── layout/
│   │   │   ├── AppLayout.tsx
│   │   │   ├── Header.tsx
│   │   │   └── Sidebar.tsx
│   │   └── common/
│   │       ├── Loading.tsx
│   │       ├── ErrorBoundary.tsx
│   │       └── EmptyState.tsx
│   ├── pages/
│   │   ├── ChatPage.tsx
│   │   ├── DocumentsPage.tsx
│   │   └── SettingsPage.tsx
│   ├── hooks/
│   │   ├── useChat.ts
│   │   ├── useDocuments.ts
│   │   └── useWebSocket.ts
│   ├── services/
│   │   └── api.ts
│   ├── store/
│   │   └── chatStore.ts
│   ├── theme/
│   │   └── antd-theme.ts
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   └── main.tsx
├── public/
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .env.example

Use pnpm as package manager.
```

#### 2.2 Ant Design Theme Configuration
```
Configure Ant Design theme in src/theme/antd-theme.ts:
- Set primary color
- Configure component styles
- Ensure WCAG 2.0 accessibility
- Export ThemeConfig object
```

#### 2.3 API Service Layer (src/services/api.ts)
```
Create Axios-based API service with:
- Base configuration (baseURL from env)
- Request/response interceptors
- Error handling
- Methods for:
  - chatAPI.sendMessage(message)
  - chatAPI.streamMessage(message) - SSE generator
  - documentsAPI.upload(file)
  - documentsAPI.list()
  - documentsAPI.delete(id)
```

#### 2.4 Custom Hooks
```
Create React Query hooks in src/hooks/:

useChat.ts:
- useMutation for sending messages
- State management for message history
- SSE streaming support

useDocuments.ts:
- useQuery for listing documents
- useMutation for upload/delete
- Optimistic updates
```

#### 2.5 Chat Interface Components
```
Build chat components using Ant Design:

ChatInterface.tsx:
- Main container with Layout
- Message list (scrollable)
- Input area with TextArea + Button
- Loading states
- Error handling

MessageBubble.tsx:
- User/assistant message styling
- Markdown rendering for AI responses
- Timestamp display
- Copy button for messages
```

#### 2.6 Document Upload Component
```
Create DocumentUpload.tsx with:
- Ant Design Upload.Dragger
- File type validation (.pdf, .txt, .docx, .md)
- Progress indicator
- Success/error notifications
- Preview uploaded files
```

#### 2.7 Main App Setup
```
Configure App.tsx with:
- ConfigProvider for Ant Design theme
- QueryClientProvider for React Query
- Router setup with react-router-dom
- Vietnamese locale (viVN)
- Error boundary
```

### Phase 3: Kubernetes Configuration

#### 3.1 Create K8s Manifests
```
Create Kubernetes manifests in k8s/:

1. namespace.yaml - Create "rag-system" namespace
2. configmap.yaml - Non-sensitive configuration
3. secrets.yaml - FPT_API_KEY and other secrets
4. backend-deployment.yaml:
   - 3 replicas minimum
   - Resource requests/limits
   - Liveness/readiness probes
   - Environment variables from ConfigMap/Secrets
   - HorizontalPodAutoscaler (3-10 replicas)
5. frontend-deployment.yaml:
   - 2 replicas minimum
   - Nginx to serve static files
6. qdrant-statefulset.yaml:
   - 2 replicas
   - 50Gi PVC per pod
   - Proper health checks
7. redis-deployment.yaml:
   - Single replica
   - 256Mi-512Mi resources
8. ingress.yaml:
   - /api → backend-service
   - / → frontend-service
   - TLS configuration
9. pvc.yaml - Persistent volume claims
```

#### 3.2 Create Helm Chart (Optional)
```
Create Helm chart structure in rag-system-chart/:
- Chart.yaml
- values.yaml with all configurations
- templates/ with all K8s resources
- Make everything configurable
```

#### 3.3 Deployment Scripts
```
Create deployment scripts in scripts/:

deploy.sh:
- Build and push Docker images
- Apply K8s manifests in order
- Wait for pods to be ready
- Verify deployment
- Show access URLs

Make script executable and add error handling
```

### Phase 4: Docker & CI/CD

#### 4.1 Dockerfiles
```
Create production-ready Dockerfiles:

backend/Dockerfile:
- Multi-stage build
- Python 3.11-slim base
- Install dependencies
- Copy application code
- Non-root user
- Health check
- CMD: uvicorn with proper workers

frontend/Dockerfile:
- Multi-stage build (build + runtime)
- Node 18+ for building
- Nginx alpine for serving
- Copy built assets
- Nginx configuration for SPA
```

#### 4.2 GitHub Actions Workflow
```
Create .github/workflows/deploy.yaml:
- Trigger on push to main
- Jobs:
  1. Build backend image
  2. Build frontend image
  3. Push to container registry
  4. Deploy to Kubernetes
  5. Verify deployment
- Use GitHub Container Registry
- Include proper versioning (git SHA or tags)
```

#### 4.3 Docker Compose (Local Dev)
```
Create docker-compose.yml for local development:
- Backend service
- Frontend service
- Qdrant service
- Redis service
- Proper networking
- Volume mounts for development
- Environment variables
```

## ✅ Code Quality Requirements

**MUST Follow:**
1. **TypeScript**: Strict mode, proper typing, no `any`
2. **Ant Design**: Use components from library only, follow design system
3. **Error Handling**: Try-catch blocks, proper error messages, user-friendly errors
4. **Async/Await**: Use throughout, handle promises correctly
5. **Logging**: Structured logging with appropriate levels
6. **Comments**: Clear docstrings and inline comments for complex logic
7. **Environment Variables**: Never hardcode secrets
8. **Validation**: Pydantic for backend, Zod/TypeScript for frontend
9. **Testing**: Write unit tests for critical functions
10. **Security**: Input validation, rate limiting, CORS properly configured

**Best Practices:**
- Follow PEP 8 for Python
- Follow Airbnb style guide for TypeScript/React
- Use meaningful variable names
- Keep functions small and focused
- DRY principle (Don't Repeat Yourself)
- SOLID principles where applicable
- Proper dependency injection
- Configuration over code

## 🚀 Development Workflow

**Step-by-Step Approach:**
1. ✅ Start with backend core (Phase 1)
2. ✅ Test each component individually
3. ✅ Test complete RAG pipeline locally
4. ✅ Build frontend (Phase 2)
5. ✅ Test frontend-backend integration
6. ✅ Create Docker images (Phase 4)
7. ✅ Test with Docker Compose
8. ✅ Create K8s manifests (Phase 3)
9. ✅ Deploy to K8s cluster
10. ✅ Setup CI/CD (Phase 4)

## 📝 Testing Strategy

**Backend Testing:**
```python
# Create tests/test_rag.py
def test_vietnamese_embedding():
    # Test embedding generation
    
def test_qdrant_retriever():
    # Test document storage and retrieval
    
def test_reranker():
    # Test reranking logic
    
def test_guard():
    # Test safety checks
    
def test_complete_pipeline():
    # Test end-to-end RAG pipeline
```

**Frontend Testing:**
```typescript
// Create tests with Vitest + React Testing Library
describe('ChatInterface', () => {
  it('should send message', () => {})
  it('should display response', () => {})
  it('should handle errors', () => {})
})
```

## 🎯 Deliverables Checklist

After completing all phases, I should have:

- [ ] ✅ Backend API running on http://localhost:8000
- [ ] ✅ Frontend UI running on http://localhost:5173
- [ ] ✅ Qdrant accessible on http://localhost:6333
- [ ] ✅ Complete RAG pipeline working (upload doc → chat)
- [ ] ✅ All API endpoints functional (/health, /chat, /documents)
- [ ] ✅ Streaming chat working
- [ ] ✅ Document upload working
- [ ] ✅ Safety guards active (Llama Guard)
- [ ] ✅ Ant Design components properly implemented
- [ ] ✅ Docker images built successfully
- [ ] ✅ Docker Compose working
- [ ] ✅ K8s manifests created
- [ ] ✅ Deployment script working
- [ ] ✅ CI/CD pipeline configured
- [ ] ✅ Documentation complete

## 💡 Important Notes

1. **FPT Cloud API**: All AI models use OpenAI-compatible interface
   ```python
   # Configuration pattern for all FPT models
   openai_api_base="https://api.fpt.ai/v1"
   openai_api_key=os.getenv("FPT_API_KEY")
   ```

2. **Vietnamese Embedding**: 1024 dimensions (not 1536 like OpenAI)
   ```python
   VectorParams(size=1024, distance=Distance.COSINE)
   ```

3. **Ant Design**: MUST use components from library
   - Don't create custom buttons/inputs
   - Use Layout, Card, Typography, etc.
   - Follow theme configuration

4. **Error Messages**: Vietnamese for user-facing, English for logs
   ```python
   return "Xin lỗi, câu hỏi của bạn chứa nội dung không phù hợp."
   logger.error("Unsafe input detected: {query}")
   ```

5. **CORS**: Configure properly for development and production
   ```python
   # Development
   app.add_middleware(CORSMiddleware, allow_origins=["*"])
   # Production - specific origins only
   ```

## 🆘 If You Need Help

When asking for help, provide:
- Which phase/step you're on
- Error messages (full traceback)
- Code snippet causing the issue
- What you've already tried
- Reference the architecture.md section

## 📚 Reference Documentation

Throughout development, constantly reference:
- `@architecture.md` - Complete system architecture
- FPT Cloud API documentation
- Ant Design component documentation
- LangChain documentation
- FastAPI documentation
- Kubernetes documentation

---

## 🏁 Let's Start!

**First Command:**
```
I'm ready to start Phase 1.1. Please create the backend structure with all the 
necessary files and folders as specified above. Start with the basic project 
structure, requirements.txt, .env.example, and main.py with a simple FastAPI 
app and health check endpoint.
```

After each component is complete and tested, we'll move to the next one systematically.

---

**Remember:** 
- Follow the architecture.md strictly
- Test each component before moving forward
- Use Ant Design components exclusively for UI
- Keep code clean, documented, and production-ready
- Ask if anything is unclear!

Let's build this amazing RAG system! 🚀