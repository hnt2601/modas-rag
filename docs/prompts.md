## Init Codebase
### Step 1
@docs/architecture.md @docs/cursor-prompt.md 

Hello! I'm ready to build the RAG system following the architecture documentation.

System Requirements:
- Frontend: React 18+ with TypeScript and Ant Design 5.x
- Backend: FastAPI with Python 3.10+
- AI Models: All from FPT Cloud (Vietnamese_Embedding, GLM-4.5, bge-reranker-v2-m3, Llama-Guard-3-8B)
- Vector DB: Qdrant
- Deployment: Kubernetes

Let's start with Phase 1.1 - Backend Structure Setup.
Please create all necessary files and folders:
- backend/ with proper structure
- Using astral uv install requirements.txt with all dependencies
- .env.example with FPT Cloud configuration
- main.py with FastAPI app and health check endpoint

Follow the specifications in @docs/architecture.md and ensure all code follows .cursorrules patterns.

### Step 2
docs/architecture.md Phase 1.1 complete and tested. 

Let's move to Phase 1.2 - Core Configuration (core/config.py).
Please implement:
- Pydantic BaseSettings class
- FPT_API_KEY from environment
- Qdrant and Redis configuration
- Support for .env files
- Type hints for all fields

Follow the patterns in @docs/cursor-prompt.md section 1.2.



## Build Backend Component
```
@docs/architecture.md 

Implement the Vietnamese Embedding service (section 6) in core/embeddings.py:
- Use langchain_openai.OpenAIEmbeddings
- Configure for FPT Cloud API (model: "Vietnamese_Embedding")
- 1024 dimensions (not 1536)
- Support async operations
- Document chunking with RecursiveCharacterTextSplitter
- Support PDF, DOCX, TXT, MD files
- Comprehensive error handling

Follow .cursorrules patterns for error handling and logging.
```

## Build Frontend Component
```
@docs/architecture.md 

Create the chat interface (section 1) with Ant Design:
- Use Layout, Card, Typography, Input.TextArea, Button components
- Support streaming messages via SSE
- Implement MessageList and MessageBubble sub-components
- Add loading states and error handling
- Follow theme configuration from theme/antd-theme.ts
- TypeScript strict mode with proper types
- Use useChat custom hook for state management

Ensure WCAG 2.0 accessibility compliance.
```

## Create K8s Manifests
```
@docs/architecture.md 

Create Kubernetes deployment for backend (section on K8s deployment):
- Deployment with 3-10 replicas
- HorizontalPodAutoscaler configuration
- ConfigMap for non-sensitive config
- Secrets for FPT_API_KEY
- Resource requests/limits
- Liveness and readiness probes at /health
- Rolling update strategy
- Proper labels and selectors

Include Service and HPA in the same file.
```

## Debug Issues
```
@docs/architecture.md @backend/core/rag.py

I'm getting this error when calling the RAG pipeline:
[paste error message]

Please help me debug while ensuring the implementation follows:
1. The RAG pipeline flow in architecture (Input Guard → Retrieval → Reranking → Generation → Output Guard)
2. The error handling patterns in .cursorrules
3. Proper async/await usage
4. FPT Cloud API configuration

What's wrong and how should I fix it?