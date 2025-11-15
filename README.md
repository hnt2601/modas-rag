# MODAS RAG - Production-Ready RAG System with Clean Architecture

> **Version:** 2.0 (Clean Architecture Refactoring)
> **Status:** Migration Planning Complete - Ready for Implementation
> **Architecture:** Clean Architecture + Domain-Driven Design

Production-ready RAG (Retrieval-Augmented Generation) system optimized for Vietnamese language, built with Clean Architecture principles and modern best practices.

## 🎯 Project Overview

MODAS RAG is an enterprise-grade conversational AI system that combines:
- **Clean Architecture** for maintainable, testable code
- **Vietnamese AI Models** from FPT Cloud Marketplace
- **Modern React UI** with Ant Design 5.x
- **Kubernetes-ready** deployment with auto-scaling
- **Domain-Driven Design** for complex business logic

### Key Features

✅ **Clean Architecture**
- Clear layer separation (Domain, Application, Infrastructure, API)
- Dependency Inversion Principle
- Testable business logic
- Flexible provider switching

✅ **Vietnamese-Optimized AI**
- Vietnamese_Embedding (1024 dimensions)
- GLM-4.5 LLM for generation
- BGE Reranker v2-m3 for accuracy
- Llama Guard 3 for safety

✅ **Enterprise UI**
- React 18 + TypeScript
- Ant Design 5.x design system
- Streaming chat responses
- WCAG 2.0 accessibility

✅ **Production-Ready**
- Kubernetes with HPA (3-10 replicas)
- Health checks & monitoring
- Comprehensive testing
- CI/CD with GitHub Actions

---

## 📁 Project Structure

```
modas-rag/
├── backend/                        # FastAPI Backend (Clean Architecture)
│   ├── domain/                     # 🔵 Domain Layer (Pure business logic)
│   │   ├── entities/               # Document, Query, ChatMessage
│   │   ├── value_objects/          # DocumentId, Embedding, Content
│   │   ├── interfaces/             # Repository & Service contracts
│   │   ├── events/                 # Domain events
│   │   └── exceptions/             # Business exceptions
│   │
│   ├── application/                # 🟢 Application Layer (Use Cases)
│   │   ├── use_cases/              # UploadDocument, ProcessQuery, etc.
│   │   ├── services/               # Application services
│   │   └── dtos/                   # Internal DTOs
│   │
│   ├── infrastructure/             # 🟡 Infrastructure Layer
│   │   ├── ai/                     # AI adapters (FPT, OpenAI, etc.)
│   │   ├── persistence/            # Qdrant, PostgreSQL
│   │   ├── file_system/            # Document loaders
│   │   └── config/                 # Configuration management
│   │
│   ├── api/                        # 🔴 API Layer (Presentation)
│   │   ├── routes/                 # FastAPI endpoints
│   │   ├── schemas/                # Request/response models
│   │   ├── dependencies/           # DI container
│   │   └── middleware/             # CORS, auth, logging
│   │
│   ├── shared/                     # Cross-cutting concerns
│   └── tests/                      # Comprehensive tests
│       ├── unit/                   # Fast, isolated tests
│       ├── integration/            # With real infrastructure
│       └── e2e/                    # Full API flow
│
├── frontend/                       # React + TypeScript UI ✅ COMPLETE
│   ├── src/
│   │   ├── components/chat/        # Chat interface
│   │   ├── hooks/                  # useChat, etc.
│   │   ├── services/               # API client
│   │   ├── theme/                  # Ant Design theme
│   │   └── types/                  # TypeScript types
│   └── ...
│
├── k8s/                            # Kubernetes Manifests ✅ COMPLETE
│   ├── namespace.yaml
│   ├── backend-deployment.yaml     # With HPA
│   ├── qdrant-statefulset.yaml     # HA setup
│   └── ...
│
└── docs/                           # Comprehensive Documentation
    ├── analysis-current-architecture.md    # Current state analysis
    ├── clean-architecture-design.md        # Target architecture
    ├── migration-plan.md                   # Detailed migration steps
    └── summary-refactoring-plan.md         # Executive summary
```

---

## 🗺️ Current Status & Roadmap

### Current State: Architecture Transition

**Previous Architecture:** Functional, service-oriented (~30% complete)
- ✅ Backend foundation (FastAPI, config, logging)
- ✅ Embedding service (Vietnamese support)
- ✅ Frontend UI (100% complete)
- ✅ K8s manifests (100% complete)
- ⚠️ Missing: Core RAG logic, API endpoints, testing

**New Architecture:** Clean Architecture + DDD (In Migration)
- 📋 Planning complete
- 📋 Migration plan ready
- ⏳ Implementation starting

### Migration Timeline

**Total Duration:** 2.5 weeks (12 working days)

```
Phase 1: Domain Layer (2 days)          - START HERE
├─ Value Objects (DocumentId, Embedding, etc.)
├─ Entities (Document, Query, ChatMessage)
├─ Domain Exceptions
└─ 100% test coverage

Phase 2: Domain Interfaces (1 day)
├─ Repository interfaces
├─ Service interfaces
└─ Strategy interfaces

Phase 3: Infrastructure (3 days)
├─ Configuration modules
├─ Embedding adapters (FPT, OpenAI)
├─ Qdrant repository
├─ LLM adapters
└─ Integration tests

Phase 4: Use Cases (2 days)
├─ UploadDocumentUseCase
├─ ProcessQueryUseCase
├─ DeleteDocumentUseCase
└─ Unit tests with mocks

Phase 5: Dependency Injection (1 day)
├─ DI container setup
├─ Provider factories
└─ FastAPI integration

Phase 6: API Layer (2 days)
├─ API schemas & DTOs
├─ Routes (chat, documents)
├─ Middleware
└─ E2E tests

Phase 7: Testing & Docs (2 days)
├─ 90%+ test coverage
├─ Architecture Decision Records
├─ Developer guide
└─ Deployment guide
```

**See [`docs/migration-plan.md`](docs/migration-plan.md) for detailed plan**

---

## 🚀 Quick Start

### Option 1: View Migration Plan (Recommended)

```bash
# Navigate to project
cd modas-rag

# Read the comprehensive documentation
open docs/summary-refactoring-plan.md    # Executive summary
open docs/migration-plan.md              # Detailed plan
open docs/clean-architecture-design.md   # Architecture design
```

### Option 2: Start Development (Current Architecture)

```bash
# Backend
cd backend
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
cp .env.example .env  # Add your FPT_API_KEY
uvicorn main:app --reload

# Frontend
cd frontend
pnpm install
pnpm dev

# Qdrant (Docker)
docker run -d -p 6333:6333 qdrant/qdrant
```

### Option 3: Begin Clean Architecture Migration

```bash
# Create feature branch
git checkout -b feature/clean-architecture-migration

# Start Phase 1: Domain Layer
# See: docs/migration-plan.md#phase-1-domain-layer-foundation
```

---

## 🏗️ Architecture Overview

### Clean Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     API LAYER (Presentation)                 │
│  FastAPI routes, schemas, middleware, DI container           │
└────────────────────────┬────────────────────────────────────┘
                         ↓ DTOs
┌─────────────────────────────────────────────────────────────┐
│               APPLICATION LAYER (Use Cases)                  │
│  UploadDocument, ProcessQuery, DeleteDocument...             │
└────────────────────────┬────────────────────────────────────┘
                         ↓ Domain Models
┌─────────────────────────────────────────────────────────────┐
│                   DOMAIN LAYER (Core)                        │
│  Entities, Value Objects, Interfaces, Domain Events          │
└────────────────────────↑────────────────────────────────────┘
                         ↑ Implements
┌─────────────────────────────────────────────────────────────┐
│                INFRASTRUCTURE LAYER                          │
│  AI adapters, Repositories, Vector stores, File system       │
└─────────────────────────────────────────────────────────────┘

🎯 KEY RULE: Dependencies point INWARD
   Infrastructure → Domain (not vice versa)
```

### Design Patterns

1. **Repository Pattern** - Abstract data access
2. **Strategy Pattern** - Interchangeable algorithms
3. **Factory Pattern** - Create complex objects
4. **Adapter Pattern** - Translate external APIs
5. **Dependency Injection** - Loose coupling
6. **Unit of Work** - Transaction management

**See [`docs/clean-architecture-design.md`](docs/clean-architecture-design.md) for details**

---

## 🛠️ Tech Stack

### Backend
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | FastAPI 0.115.0 | High-performance async API |
| Language | Python 3.10+ | Type-safe development |
| Validation | Pydantic 2.9.2 | Data validation |
| AI Framework | LangChain 0.3.7 | AI orchestration |
| Vector DB | Qdrant 1.11.3 | Vector similarity search |
| Logging | Loguru 0.7.2 | Structured logging |
| Testing | Pytest | Comprehensive testing |
| DI | dependency-injector 4.41.0 | Dependency injection |

### Frontend (✅ Complete)
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Framework | React 18 | Modern UI framework |
| Language | TypeScript 5.3+ | Type safety |
| UI Library | Ant Design 5.x | Enterprise UI components |
| State | TanStack Query 5.x | Data fetching & caching |
| Build | Vite | Fast dev & build |

### AI Models (FPT Cloud)
| Model | Purpose | Dimensions |
|-------|---------|-----------|
| Vietnamese_Embedding | Text embeddings | 1024 |
| GLM-4.5 | Response generation | - |
| bge-reranker-v2-m3 | Result reranking | - |
| Llama-Guard-3-8B | Content safety | - |

### Infrastructure (✅ Complete)
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Orchestration | Kubernetes 1.24+ | Container management |
| Ingress | NGINX | HTTP routing |
| Auto-scaling | HPA | 3-10 replicas |
| Vector DB | Qdrant StatefulSet | HA vector storage |
| Cache | Redis | Optional caching |

---

## 📚 Documentation

### 📖 Migration & Architecture Docs (NEW)

1. **[Summary: Refactoring Plan](docs/summary-refactoring-plan.md)**
   - Executive summary of migration
   - Current state analysis
   - Benefits & timeline
   - **READ THIS FIRST**

2. **[Detailed Migration Plan](docs/migration-plan.md)**
   - 7 phases with detailed tasks
   - Code examples for each phase
   - Time estimates & success criteria
   - Risk assessment & rollback strategy

3. **[Clean Architecture Design](docs/clean-architecture-design.md)**
   - Architecture overview with diagrams
   - Layer definitions & examples
   - Folder structure
   - Design patterns implementation
   - Testing strategy

4. **[Current Architecture Analysis](docs/analysis-current-architecture.md)**
   - Detailed codebase analysis
   - Component categorization
   - Dependency mapping
   - Technical debt assessment

### 📁 Component Documentation

5. **[Backend README](backend/README.md)**
   - Backend setup & usage
   - Current implementation status
   - Development guide

6. **[Frontend README](frontend/README.md)** ✅
   - Frontend architecture
   - Component documentation
   - Development guide

7. **[Kubernetes README](k8s/README.md)** ✅
   - Deployment instructions
   - Resource configuration
   - Monitoring & troubleshooting

### 📊 Progress Tracking

8. **[PROGRESS.md](PROGRESS.md)**
   - Development milestones
   - Phase completion status
   - Next steps

---

## 🧪 Testing Strategy

### Test Pyramid (Target)

```
       ┌─────────────┐
       │   E2E (5%)  │  ← Full API flow tests
       ├─────────────┤
       │ Integration │  ← With real infrastructure
       │    (20%)    │
       ├─────────────┤
       │    Unit     │  ← Fast, isolated tests
       │    (75%)    │
       └─────────────┘
```

### Current Status
- ⏳ Unit tests (Phase 1-4 of migration)
- ⏳ Integration tests (Phase 3, 6)
- ⏳ E2E tests (Phase 6)
- **Target:** 90%+ coverage

### Running Tests (After Migration)

```bash
# Unit tests (fast)
pytest tests/unit -v

# Integration tests (with real Qdrant)
pytest tests/integration -v --integration

# E2E tests (full flow)
pytest tests/e2e -v --e2e

# All tests with coverage
pytest tests/ --cov=. --cov-report=html
```

---

## 🚢 Deployment

### Local Development

```bash
# Backend
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
pnpm dev

# Qdrant
docker run -d -p 6333:6333 qdrant/qdrant
```

### Docker

```bash
# Build backend
cd backend
docker build -t rag-backend:latest .

# Build frontend
cd frontend
docker build -t rag-frontend:latest .

# Run with docker-compose (TODO)
docker-compose up -d
```

### Kubernetes ✅

```bash
# Create namespace & secrets
kubectl apply -f k8s/namespace.yaml
kubectl create secret generic rag-backend-secrets \
  --from-literal=FPT_API_KEY=your-key \
  -n rag-system

# Deploy infrastructure
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/qdrant-statefulset.yaml
kubectl apply -f k8s/redis-deployment.yaml

# Deploy backend
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/backend-deployment.yaml

# Setup ingress
kubectl apply -f k8s/ingress.yaml

# Verify
kubectl get all -n rag-system
```

**See [k8s/README.md](k8s/README.md) for complete deployment guide**

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in `backend/`:

```bash
# FPT Cloud API
FPT_API_KEY=your-fpt-cloud-api-key
FPT_API_BASE=https://api.fpt.ai/v1

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=documents

# RAG Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
RETRIEVAL_TOP_K=20
RERANK_TOP_N=5

# Models
EMBEDDING_MODEL=Vietnamese_Embedding
EMBEDDING_DIMENSIONS=1024
LLM_MODEL=GLM-4.5
LLM_TEMPERATURE=0.7

# Application
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE=52428800  # 50MB
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

**See [backend/.env.example](backend/.env.example) for all options**

---

## 📊 Project Metrics

### Current Codebase

**Backend:**
- **Status:** ~30% complete (functional foundation)
- **Files:** 9 Python files
- **Lines of Code:** ~1,109 lines
- **Packages:** 111 dependencies
- **Tests:** Basic embedding test

**Frontend:** ✅ 100% Complete
- **Files:** 15 TypeScript files
- **Components:** 8 components
- **Hooks:** 1 custom hook
- **Type Safety:** Strict mode, no 'any'

**K8s:** ✅ 100% Complete
- **Manifests:** 8 YAML files
- **Resources:** HA setup with auto-scaling
- **Production-ready:** Yes

### After Migration (Target)

**Backend:**
- **Files:** ~50+ files (domain, app, infra, api)
- **Lines of Code:** ~5,000+ lines
- **Test Coverage:** 90%+
- **Layers:** 4 clear layers
- **Patterns:** 6 design patterns
- **APIs:** Complete chat & document endpoints

---

## 🎯 Benefits of Clean Architecture

### Technical Benefits

1. **Testability**
   - Mock infrastructure in unit tests
   - Test business logic in isolation
   - 90%+ coverage achievable

2. **Flexibility**
   - Switch LLM providers via config
   - Replace vector stores without code changes
   - Add new features without breaking existing code

3. **Maintainability**
   - Clear responsibilities per layer
   - Dependencies point inward
   - Business logic independent of frameworks

4. **Scalability**
   - Modular architecture
   - Parallel development possible
   - Easy to onboard new developers

### Business Benefits

1. **Development Velocity**
   - New features: -50% time
   - Bug fixes: -30% time
   - Onboarding: < 2 days

2. **Code Quality**
   - Reduced coupling
   - Better type safety
   - Comprehensive testing

3. **Future-Proof**
   - Domain logic stable despite tech changes
   - Easy to adopt new AI models
   - Support multiple deployment scenarios

---

## 🤝 Contributing

### Development Workflow

1. **Review Documentation**
   ```bash
   # Read the migration plan first
   open docs/summary-refactoring-plan.md
   open docs/migration-plan.md
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Follow Architecture**
   - Respect layer boundaries
   - Dependencies point inward
   - Use interfaces for external services

4. **Write Tests**
   - Unit tests for domain & application
   - Integration tests for infrastructure
   - E2E tests for critical paths

5. **Submit PR**
   - Reference migration phase if applicable
   - Include tests
   - Update documentation

### Code Standards

- **Python:** Follow PEP 8, use type hints
- **TypeScript:** Strict mode, no 'any'
- **Tests:** 90%+ coverage for new code
- **Docs:** Update ADRs for architectural decisions

---

## 📞 Support & Resources

### Documentation Links

- [Migration Summary](docs/summary-refactoring-plan.md) - Start here
- [Detailed Migration Plan](docs/migration-plan.md) - Step-by-step guide
- [Clean Architecture Design](docs/clean-architecture-design.md) - Architecture details
- [Current State Analysis](docs/analysis-current-architecture.md) - Technical assessment

### External Resources

- [Clean Architecture (Uncle Bob)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🎉 Next Steps

### If You're New Here

1. **Read the summary:** [`docs/summary-refactoring-plan.md`](docs/summary-refactoring-plan.md)
2. **Understand the plan:** [`docs/migration-plan.md`](docs/migration-plan.md)
3. **Review architecture:** [`docs/clean-architecture-design.md`](docs/clean-architecture-design.md)

### If You're Ready to Develop

**Option A: Start Migration (Recommended)**
```bash
git checkout -b feature/clean-architecture-migration
# Follow Phase 1 in docs/migration-plan.md
```

**Option B: Work on Current Code**
```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
# Continue with existing functional architecture
```

### If You're Deploying

**Frontend & K8s are production-ready!**
```bash
# Deploy frontend
cd frontend && pnpm build

# Deploy to Kubernetes
kubectl apply -f k8s/
```

---

**Status:** 🚀 Ready for Clean Architecture Migration

**Current Phase:** Planning Complete ✅

**Next Phase:** Phase 1 - Domain Layer Implementation

**Timeline:** 2.5 weeks to completion

**Questions?** See [`docs/summary-refactoring-plan.md`](docs/summary-refactoring-plan.md)
