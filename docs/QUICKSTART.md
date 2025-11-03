# 🚀 Quick Start Guide - Building RAG System in Cursor

## 📦 What You Have

You now have 3 essential files for building your RAG system:

1. **`architecture.md`** - Complete system architecture and technical specifications
2. **`cursor-prompt.md`** - Step-by-step development prompt
3. **`.cursorrules`** - Automatic rules for Cursor AI to follow

## 🎯 Setup Instructions

### Step 1: Prepare Your Project

```bash
# Create project directory
mkdir rag-system
cd rag-system

# Initialize git
git init

# Create .gitignore
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.env
.venv

# Node
node_modules/
dist/
.DS_Store
*.log
npm-debug.log*

# IDE
.vscode/
.idea/
*.swp
*.swo

# Docker
*.tar
*.gz

# Kubernetes
*.secret.yaml

# Uploads
uploads/
*.pdf
*.docx
EOF
```

### Step 2: Copy Documentation Files

```bash
# Copy all files to your project root
cp path/to/architecture.md ./docs/architecture.md
cp path/to/.cursorrules ./.cursorrules
cp path/to/cursor-prompt.md ./docs/cursor-prompt.md
```

### Step 3: Open in Cursor

```bash
# Open project in Cursor
cursor .
```

### Step 4: Verify Cursor Setup

1. **Check if `.cursorrules` is loaded:**
   - Cursor automatically loads `.cursorrules` from project root
   - You should see it referenced in Cursor's context

2. **Verify file access:**
   - Open Cursor AI chat (Cmd+L or Ctrl+L)
   - Type: `@architecture.md`
   - File should be accessible

## 💬 How to Use the Prompts

### Method 1: Start from Beginning (Recommended)

**Step 1: Open Cursor AI Chat**
- Press `Cmd+L` (Mac) or `Ctrl+L` (Windows/Linux)

**Step 2: Reference Architecture**
```
@architecture.md I want to build this RAG system. Let's follow the development plan in @docs/cursor-prompt.md. I'm ready to start Phase 1.1 - Backend Structure Setup. Please create all the necessary files and folders.
```

**Step 3: Continue Phase by Phase**
After each phase completion:
```
@architecture.md Phase 1.1 complete. Let's move to Phase 1.2 - Core Configuration (core/config.py). Please implement as specified in @docs/cursor-prompt.md.
```

### Method 2: Jump to Specific Component

If you want to build a specific component:

```
@architecture.md I need to implement the Vietnamese Embedding service as described in section 6. Please create core/embeddings.py following the specifications in the architecture document.
```

### Method 3: Debug/Fix Issues

When you encounter issues:

```
@architecture.md I'm getting this error in core/rag.py:
[paste error]

Please help me fix this while following the architecture specifications and .cursorrules.
```

## 🎨 Example Development Flow

### Backend Development Example

**1. Start Backend Core:**
```
Cursor Chat:
→ @architecture.md @docs/cursor-prompt.md
→ Let's start Phase 1. Create the backend structure with:
  - main.py (FastAPI app with health check)
  - requirements.txt (all dependencies)
  - .env.example (environment variables template)
  - Basic folder structure as per architecture
```

**2. Implement Vietnamese Embedding:**
```
Cursor Chat:
→ @architecture.md
→ Implement core/embeddings.py with Vietnamese Embedding from FPT Cloud.
  - Use langchain_openai.OpenAIEmbeddings
  - Configure for 1024 dimensions
  - Support async operations
  - Follow .cursorrules patterns
```

**3. Test Component:**
```
Cursor Chat:
→ Create a test file for Vietnamese Embedding service.
→ Test embedding generation with sample Vietnamese text.
```

### Frontend Development Example

**1. Setup Frontend:**
```
Cursor Chat:
→ @architecture.md @docs/cursor-prompt.md
→ Create frontend with React + TypeScript + Ant Design.
→ Follow the structure in Phase 2.1
→ Setup package.json, tsconfig.json, vite.config.ts
```

**2. Create Chat Interface:**
```
Cursor Chat:
→ @architecture.md
→ Create src/components/chat/ChatInterface.tsx using Ant Design.
→ Must use: Layout, Card, Input.TextArea, Button
→ Support streaming messages
→ Follow Ant Design theme from architecture
```

## 🔧 Advanced Usage Tips

### 1. Multi-File Context

```
Cursor Chat:
→ @architecture.md @backend/core/rag.py @backend/core/retriever.py
→ I need to integrate the retriever into the RAG pipeline. Please show me how.
```

### 2. Code Review

```
Cursor Chat:
→ @.cursorrules Review this code:
[paste code]
→ Check if it follows all the rules and architecture patterns.
```

### 3. Refactoring

```
Cursor Chat:
→ @architecture.md @backend/api/chat.py
→ Refactor this to follow the RAG pipeline flow described in architecture.
→ Ensure it uses all components: Guard, Retriever, Reranker, LLM
```

### 4. Adding New Features

```
Cursor Chat:
→ @architecture.md
→ I want to add support for CSV file uploads. 
→ Where should this be implemented?
→ Please update the necessary files while maintaining architecture compliance.
```

## 📋 Development Checklist

Use this checklist as you build:

### Backend (Phase 1)
- [ ] ✅ Project structure created
- [ ] ✅ requirements.txt with all dependencies
- [ ] ✅ Config management (core/config.py)
- [ ] ✅ Logging setup (utils/logger.py)
- [ ] ✅ Vietnamese Embedding (core/embeddings.py)
- [ ] ✅ Qdrant Retriever (core/retriever.py)
- [ ] ✅ Reranker (core/reranker.py)
- [ ] ✅ Llama Guard (core/guard.py)
- [ ] ✅ RAG Pipeline (core/rag.py)
- [ ] ✅ Chat API (api/chat.py)
- [ ] ✅ Documents API (api/documents.py)
- [ ] ✅ Main app (main.py)
- [ ] ✅ Tests written
- [ ] ✅ Backend running locally

### Frontend (Phase 2)
- [ ] ✅ Project setup with Vite + React + TS
- [ ] ✅ Ant Design configuration
- [ ] ✅ API service layer
- [ ] ✅ Custom hooks (useChat, useDocuments)
- [ ] ✅ Chat interface components
- [ ] ✅ Document upload component
- [ ] ✅ Layout and routing
- [ ] ✅ Theme configuration
- [ ] ✅ Frontend running locally
- [ ] ✅ Integration with backend working

### Infrastructure (Phase 3 & 4)
- [ ] ✅ Dockerfiles (backend, frontend)
- [ ] ✅ Docker Compose for local dev
- [ ] ✅ K8s namespace
- [ ] ✅ ConfigMap and Secrets
- [ ] ✅ Backend deployment
- [ ] ✅ Frontend deployment
- [ ] ✅ Qdrant StatefulSet
- [ ] ✅ Redis deployment
- [ ] ✅ Ingress configuration
- [ ] ✅ HPA configuration
- [ ] ✅ Deployment script
- [ ] ✅ GitHub Actions CI/CD

## 🐛 Troubleshooting

### Cursor Not Reading .cursorrules
```bash
# Ensure file is in project root
ls -la .cursorrules

# Restart Cursor
# File → Reload Window
```

### Architecture.md Not Accessible
```bash
# Move to project root or docs folder
mv architecture.md ./docs/architecture.md

# Reference with correct path in Cursor
@docs/architecture.md
```

### FPT Cloud API Issues
```
Check:
1. FPT_API_KEY is set in .env
2. API endpoint is correct: https://api.fpt.ai/v1
3. Model names are exact:
   - Vietnamese_Embedding
   - GLM-4.5
   - bge-reranker-v2-m3
   - Llama-Guard-3-8B
```

### Ant Design Not Working
```typescript
// Ensure ConfigProvider is setup in App.tsx
import { ConfigProvider } from 'antd';
import { theme } from './theme/antd-theme';
import viVN from 'antd/locale/vi_VN';

<ConfigProvider theme={theme} locale={viVN}>
  {/* Your app */}
</ConfigProvider>
```

## 💡 Pro Tips

### 1. Use Composer for Complex Changes
```
Open Cursor Composer (Cmd+I):
→ "Following @architecture.md, refactor the entire RAG pipeline to add 
   conversation memory. Update all affected files: core/rag.py, 
   api/chat.py, and models/schemas.py"
```

### 2. Generate Tests Automatically
```
Cursor Chat:
→ @backend/core/rag.py
→ Generate comprehensive unit tests for this module.
→ Cover all edge cases and error scenarios.
```

### 3. Documentation Generation
```
Cursor Chat:
→ @architecture.md
→ Generate API documentation in OpenAPI format for all endpoints
→ in backend/api/
```

### 4. Code Explanation
```
Cursor Chat:
→ @backend/core/rag.py
→ Explain this RAG pipeline step by step.
→ How does it integrate with Qdrant and FPT Cloud models?
```

## 🚦 Next Steps

1. **Start Development:**
   ```
   Open Cursor → Press Cmd+L → Start with Phase 1.1
   ```

2. **Follow Phase Order:**
   - Complete each phase fully before moving to next
   - Test after each component
   - Keep checking architecture.md

3. **Commit Regularly:**
   ```bash
   git add .
   git commit -m "feat(backend): implement Vietnamese embedding service"
   ```

4. **Deploy When Ready:**
   ```bash
   ./scripts/deploy.sh v1.0.0
   ```

## 📚 Additional Resources

- **Architecture Reference:** `docs/architecture.md`
- **Development Plan:** `docs/cursor-prompt.md`
- **Cursor Rules:** `.cursorrules` (auto-loaded)
- **FPT Cloud:** https://marketplace.fptcloud.com
- **Ant Design:** https://ant.design/components/overview
- **FastAPI:** https://fastapi.tiangolo.com

## ❓ Need Help?

### In Cursor Chat:
```
@architecture.md @.cursorrules
I'm stuck on [specific issue]. 
What does the architecture say about this?
How should I implement it according to the rules?
```

### For Architecture Questions:
```
@architecture.md
Section [X] mentions [Y]. Can you explain this in more detail?
Show me the implementation pattern for this.
```

### For Best Practices:
```
@.cursorrules
What's the correct pattern for [specific task]?
Am I following the rules correctly in this code?
```

---

## 🎉 Ready to Build!

You're all set! Start building your production-ready RAG system with:

```
Cursor → Open Chat (Cmd+L) → Paste:

@architecture.md @docs/cursor-prompt.md 

Hi! I'm ready to build the RAG system. Let's start with Phase 1.1 - 
Backend Structure Setup. Please create the initial project structure 
with all necessary files and folders as specified.
```

**Remember:** 
- Reference @architecture.md frequently
- Follow .cursorrules automatically
- Build phase by phase
- Test as you go
- Keep it production-ready!

Good luck! 🚀