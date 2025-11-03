# 📚 RAG System Documentation Package

Complete documentation and prompts for building a production-ready RAG (Retrieval-Augmented Generation) system with Vietnamese AI models, React + Ant Design UI, and Kubernetes deployment.

## 📦 What's Included

This package contains everything you need to build the RAG system in Cursor AI:

### 1. **architecture.md** (Main Reference)
- 📖 **Purpose:** Complete system architecture and technical specifications
- 🎯 **Use:** Reference throughout development for all architectural decisions
- 📝 **Contains:**
  - Complete tech stack (React + Ant Design, FastAPI, Qdrant, K8s)
  - All FPT Cloud AI models configuration
  - Full component specifications
  - Kubernetes deployment manifests
  - CI/CD pipeline setup
  - Code examples for every component

### 2. **.cursorrules** (Auto-Loaded Rules)
- 📖 **Purpose:** Automatic rules that Cursor AI follows during development
- 🎯 **Use:** Place in project root - Cursor loads automatically
- 📝 **Contains:**
  - Code quality standards
  - Architectural compliance rules
  - Common patterns and anti-patterns
  - Error handling templates
  - Security requirements
  - Testing requirements

### 3. **cursor-prompt.md** (Development Guide)
- 📖 **Purpose:** Step-by-step prompt for building the entire system
- 🎯 **Use:** Follow phase by phase in Cursor chat
- 📝 **Contains:**
  - 4 development phases
  - Detailed component specifications
  - Code templates
  - Testing strategies
  - Quality requirements
  - Complete checklist

### 4. **QUICKSTART.md** (This File)
- 📖 **Purpose:** Quick start guide for using the documentation
- 🎯 **Use:** First-time setup and reference
- 📝 **Contains:**
  - Setup instructions
  - Usage examples
  - Troubleshooting guide
  - Pro tips

## 🚀 Quick Start (3 Steps)

### Step 1: Setup Project

```bash
# Create and initialize project
mkdir rag-system && cd rag-system
git init

# Copy documentation files
cp /path/to/architecture.md ./docs/architecture.md
cp /path/to/.cursorrules ./.cursorrules
cp /path/to/cursor-prompt.md ./docs/cursor-prompt.md
cp /path/to/QUICKSTART.md ./docs/QUICKSTART.md
```

### Step 2: Open in Cursor

```bash
# Open project in Cursor
cursor .
```

### Step 3: Start Building

Open Cursor AI Chat (Cmd+L / Ctrl+L) and paste:

```
@docs/architecture.md @docs/cursor-prompt.md 

Hello! I'm ready to build the RAG system following the architecture.
Let's start with Phase 1.1 - Backend Structure Setup.
Please create all necessary files and folders as specified.
```

## 📖 How to Use Each File

### Using architecture.md

**Reference for every decision:**
```
Cursor Chat:
→ @docs/architecture.md What's the correct way to configure Vietnamese Embedding?
→ @docs/architecture.md Show me the RAG pipeline implementation
→ @docs/architecture.md How should I structure the React components?
```

**Multi-file context:**
```
Cursor Chat:
→ @docs/architecture.md @backend/core/rag.py
→ Is this implementation following the architecture specifications?
```

### Using .cursorrules

**Automatic:** Place in project root, Cursor loads it automatically

**Manual reference:**
```
Cursor Chat:
→ @.cursorrules Review my code for compliance
→ @.cursorrules What's the error handling pattern I should use?
→ @.cursorrules Check if I'm following the security rules
```

### Using cursor-prompt.md

**Phase-by-phase development:**
```
Cursor Chat:
→ @docs/cursor-prompt.md I'm ready for Phase 1.2
→ @docs/cursor-prompt.md What are the requirements for Phase 2.3?
→ @docs/cursor-prompt.md Show me the testing strategy
```

**Combined with architecture:**
```
Cursor Chat:
→ @docs/architecture.md @docs/cursor-prompt.md
→ Let's implement Phase 1.7 (RAG Pipeline) following the architecture specs
```

## 🎯 Development Workflow

### Recommended Flow

```
Phase 1: Backend Core
├─ 1.1 Project Structure
├─ 1.2 Configuration
├─ 1.3 Vietnamese Embedding
├─ 1.4 Qdrant Retriever
├─ 1.5 Reranker
├─ 1.6 Llama Guard
├─ 1.7 RAG Pipeline
├─ 1.8 API Endpoints
└─ 1.9 Main App
    └─→ Test thoroughly before Phase 2

Phase 2: Frontend
├─ 2.1 React + TS + Ant Design Setup
├─ 2.2 Theme Configuration
├─ 2.3 API Service Layer
├─ 2.4 Custom Hooks
├─ 2.5 Chat Components
├─ 2.6 Document Upload
└─ 2.7 Main App Integration
    └─→ Test integration with backend

Phase 3: Kubernetes
├─ 3.1 K8s Manifests
├─ 3.2 Helm Chart
└─ 3.3 Deployment Scripts
    └─→ Test in K8s cluster

Phase 4: CI/CD
├─ 4.1 Dockerfiles
├─ 4.2 GitHub Actions
└─ 4.3 Production Deployment
    └─→ Final production testing
```

## 💡 Pro Tips

### 1. Always Reference Architecture
```
❌ Bad: "Create a chat API"
✅ Good: "@docs/architecture.md Create chat API following section 3.3"
```

### 2. Use Multi-File Context
```
@docs/architecture.md @backend/core/rag.py @docs/cursor-prompt.md
Refactor this RAG pipeline to match the architecture specifications in Phase 1.7
```

### 3. Leverage Cursor Composer
```
Cmd+I (or Ctrl+I):
Following @docs/architecture.md, implement the complete backend Phase 1
with all files: config.py, embeddings.py, retriever.py, reranker.py, 
guard.py, and rag.py. Ensure all follow .cursorrules patterns.
```

### 4. Generate Tests Automatically
```
@backend/core/embeddings.py @.cursorrules
Generate comprehensive unit tests following the testing requirements
```

### 5. Get Architecture Explanations
```
@docs/architecture.md
Explain the RAG pipeline flow step by step.
Why do we use 1024 dimensions for Vietnamese Embedding?
```

## 🏗️ Architecture Highlights

### Tech Stack
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Frontend** | React + Ant Design | Enterprise UI with design system |
| **Backend** | FastAPI | High-performance async API |
| **Embedding** | Vietnamese_Embedding (FPT) | 1024-dim Vietnamese vectors |
| **Reranker** | bge-reranker-v2-m3 (FPT) | Improve retrieval accuracy |
| **LLM** | GLM-4.5 (FPT) | Response generation |
| **Guard** | Llama-Guard-3-8B (FPT) | Content safety |
| **Vector DB** | Qdrant | Vector storage & search |
| **Deploy** | Kubernetes | Container orchestration |

### Key Features
- ✅ Vietnamese-optimized AI models
- ✅ Design system compliance (Ant Design)
- ✅ Production-ready Kubernetes deployment
- ✅ Auto-scaling with HPA
- ✅ Content safety with Llama Guard
- ✅ Two-stage retrieval (vector search + reranking)
- ✅ Streaming chat responses
- ✅ CI/CD with GitHub Actions

## 📝 Example Prompts

### Starting from Scratch
```
@docs/architecture.md @docs/cursor-prompt.md

Hi! I want to build the complete RAG system from scratch.
Let's start with Phase 1.1 - Backend Structure.
Create the project with:
- Proper folder structure
- requirements.txt
- .env.example
- main.py with health check
```

### Implementing Specific Component
```
@docs/architecture.md

I need to implement the Vietnamese Embedding service (section 6).
Create core/embeddings.py with:
- FPT Cloud integration
- 1024 dimensions
- Document chunking
- Async support
- Error handling
Follow .cursorrules patterns.
```

### Frontend Component
```
@docs/architecture.md

Create the chat interface (section 1) with Ant Design:
- Use Layout, Card, Input, Button
- Support streaming messages
- Follow the theme configuration
- Implement useChat hook
TypeScript strict mode.
```

### Kubernetes Deployment
```
@docs/architecture.md

Create Kubernetes manifests for backend deployment:
- 3-10 replicas with HPA
- ConfigMap and Secrets
- Resource limits
- Health checks
- Rolling update strategy
Follow section on K8s deployment.
```

### Debugging
```
@docs/architecture.md @backend/core/rag.py

I'm getting this error when running the RAG pipeline:
[paste error]

Please help fix while following architecture specs.
What am I doing wrong?
```

### Code Review
```
@docs/architecture.md @.cursorrules @backend/api/chat.py

Review this code:
[paste code]

Check:
1. Follows architecture?
2. Follows .cursorrules?
3. Error handling correct?
4. Security issues?
5. Improvements needed?
```

## 🐛 Common Issues & Solutions

### Issue 1: FPT Cloud API Not Working
```
Problem: API calls failing
Solution:
1. Check FPT_API_KEY in .env
2. Verify endpoint: https://api.fpt.ai/v1
3. Confirm model names are exact:
   - Vietnamese_Embedding (not vietnamese_embedding)
   - GLM-4.5 (not glm-4.5)
4. Check API key has access to these models
```

### Issue 2: Qdrant Dimensions Mismatch
```
Problem: Vector dimension error
Solution:
- Vietnamese Embedding uses 1024 dimensions (not 1536)
- Configure Qdrant collection with size=1024
- Don't use OpenAI's default 1536
```

### Issue 3: Ant Design Not Rendering
```
Problem: Components not displaying
Solution:
1. Ensure ConfigProvider wraps app:
   <ConfigProvider theme={theme} locale={viVN}>
2. Import CSS: import 'antd/dist/reset.css'
3. Check theme configuration in theme/antd-theme.ts
```

### Issue 4: Cursor Not Loading .cursorrules
```
Problem: Rules not being followed
Solution:
1. Ensure .cursorrules is in project root
2. Restart Cursor (File → Reload Window)
3. Check file permissions
4. Manually reference: @.cursorrules
```

### Issue 5: Docker Build Failing
```
Problem: Image build errors
Solution:
1. Check Dockerfile follows multi-stage pattern
2. Verify requirements.txt has correct versions
3. Ensure .dockerignore excludes node_modules, venv
4. Build with: docker build --no-cache
```

## 📊 Quality Checklist

Before considering phase complete:

### Backend
- [ ] All imports work
- [ ] No syntax errors
- [ ] Type hints present
- [ ] Docstrings complete
- [ ] Error handling comprehensive
- [ ] Logging configured
- [ ] Environment variables used
- [ ] Tests written and passing
- [ ] API endpoints functional
- [ ] Health check working

### Frontend
- [ ] TypeScript strict mode
- [ ] No 'any' types
- [ ] Ant Design components only
- [ ] Proper error boundaries
- [ ] Loading states implemented
- [ ] API integration working
- [ ] Responsive design
- [ ] Theme applied correctly
- [ ] Tests passing
- [ ] Build successful

### Infrastructure
- [ ] Dockerfiles optimized
- [ ] K8s manifests valid
- [ ] Resources limits set
- [ ] Health checks configured
- [ ] Secrets not committed
- [ ] ConfigMaps used correctly
- [ ] Ingress configured
- [ ] HPA working
- [ ] CI/CD pipeline functional
- [ ] Deployment successful

## 🎓 Learning Resources

### Understand the Architecture
```
@docs/architecture.md

Can you explain:
1. Why do we use two-stage retrieval?
2. How does the RAG pipeline flow work?
3. What's the purpose of Llama Guard?
4. Why Ant Design over other UI frameworks?
```

### Best Practices
```
@.cursorrules

Show me:
1. The correct error handling pattern
2. How to structure async functions
3. Security best practices
4. Testing requirements
```

### Implementation Details
```
@docs/cursor-prompt.md

Explain:
1. Phase 1.7 RAG Pipeline requirements
2. Phase 2.5 Chat component specifications
3. Phase 3.1 K8s manifest structure
```

## 🚀 Next Steps

1. **Read This README** ✅ (You're here!)

2. **Setup Project:**
   ```bash
   mkdir rag-system && cd rag-system
   # Copy files as shown in Quick Start
   cursor .
   ```

3. **Start Building:**
   ```
   Open Cursor Chat → Cmd+L
   Reference @docs/architecture.md and @docs/cursor-prompt.md
   Start with Phase 1.1
   ```

4. **Follow Phases:**
   - Complete each phase fully
   - Test after each component
   - Use checklist to track progress

5. **Deploy:**
   ```bash
   # When ready
   ./scripts/deploy.sh v1.0.0
   ```

## 📞 Support

### In Cursor Chat
```
For help, always reference the docs:
@docs/architecture.md @.cursorrules @docs/cursor-prompt.md

[Your question here]
```

### Documentation Structure
```
rag-system/
├── docs/
│   ├── architecture.md      ← Main reference
│   ├── cursor-prompt.md     ← Development guide
│   ├── QUICKSTART.md        ← This file
│   └── README.md            ← Package overview
├── .cursorrules             ← Auto-loaded rules
└── [your code here]
```

## 🎉 Ready to Build!

You have everything needed to build a production-ready RAG system:
- ✅ Complete architecture
- ✅ Automatic rules
- ✅ Step-by-step guide
- ✅ All code patterns
- ✅ K8s deployment
- ✅ CI/CD setup

**Start now:**
```bash
cursor .
# Press Cmd+L
# Paste the quick start prompt
# Start building! 🚀
```

---

**Remember:**
- Reference @docs/architecture.md frequently
- Let .cursorrules guide your code
- Follow @docs/cursor-prompt.md phases
- Test as you go
- Keep it production-ready!

Good luck building your RAG system! 🎊