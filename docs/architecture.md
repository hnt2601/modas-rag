# RAG System Architecture

## Overview

This document defines the complete architecture of our production-ready RAG (Retrieval-Augmented Generation) system. The system is built with enterprise-grade components following industry best practices.

### Key Features

**🎨 Design System Compliant**
- React 18+ with TypeScript
- Ant Design 5.x (Enterprise UI framework)
- WCAG 2.0 accessibility standards
- Fully responsive and themeable
- Professional component library

**☸️ Kubernetes Native**
- Container orchestration with K8s
- Auto-scaling (HPA)
- Zero-downtime deployments
- StatefulSets for data persistence
- Helm chart support
- CI/CD with GitHub Actions

**🇻🇳 Vietnamese-Optimized AI**
- Vietnamese_Embedding (FPT Cloud)
- GLM-4.5 LLM
- BGE Reranker v2-m3
- Llama Guard 3 for safety
- All models via unified FPT Cloud API

**🏗️ Production-Ready**
- Microservices architecture
- High availability (HA)
- Monitoring & observability
- Persistent storage
- Load balancing
- TLS/HTTPS support

Use this as reference when developing features, debugging, or planning improvements. Tag `@architecture.md` in Cursor to provide AI assistants with full system context.

---

## Tech Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **UI** | React + Ant Design | Design system compliant interface |
| **Backend** | FastAPI | REST API & business logic |
| **Vector DB** | Qdrant | Vector search & storage |
| **Embedding** | Vietnamese_Embedding (FPT) | Text → Vectors (Vietnamese) |
| **Reranker** | bge-reranker-v2-m3 (FPT) | Reorder search results |
| **LLM** | GLM-4.5 (FPT) | Response generation |
| **Guard** | Llama-Guard-3-8B (FPT) | Content safety |
| **Deployment** | Kubernetes (K8s) | Container orchestration |
| **CI/CD** | GitHub Actions | Automated deployment |

**All AI models are accessed via FPT Cloud Marketplace with OpenAI-compatible API.**

---

## Architecture Layers

### 1. UI Layer - React + Ant Design

**Purpose:** Professional, design system compliant web interface

**Why React + Ant Design:**
- Enterprise-grade design system
- Comprehensive component library
- Accessibility (WCAG 2.0)
- Responsive by default
- Customizable theming
- TypeScript support

**Tech Stack:**
- React 18+ with TypeScript
- Ant Design 5.x (Design System)
- TanStack Query (data fetching)
- Zustand (state management)
- Axios (API calls)
- Vite (build tool)

**Project Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   └── MessageBubble.tsx
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
│   └── App.tsx
├── package.json
├── tsconfig.json
└── vite.config.ts
```

**Core Components:**

**1. Chat Interface (`components/chat/ChatInterface.tsx`):**
```tsx
import React, { useState } from 'react';
import { Layout, Input, Button, Space, Typography, Card } from 'antd';
import { SendOutlined, LoadingOutlined } from '@ant-design/icons';
import { useChat } from '@/hooks/useChat';
import MessageList from './MessageList';

const { Content } = Layout;
const { TextArea } = Input;
const { Title } = Typography;

export const ChatInterface: React.FC = () => {
  const [message, setMessage] = useState('');
  const { messages, sendMessage, isLoading } = useChat();

  const handleSend = async () => {
    if (!message.trim()) return;
    
    await sendMessage(message);
    setMessage('');
  };

  return (
    <Layout style={{ height: '100vh' }}>
      <Content style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
        <Card 
          style={{ flex: 1, display: 'flex', flexDirection: 'column' }}
          bodyStyle={{ flex: 1, display: 'flex', flexDirection: 'column' }}
        >
          <Title level={3}>RAG Chat Assistant</Title>
          
          {/* Message List */}
          <MessageList messages={messages} style={{ flex: 1, overflow: 'auto' }} />
          
          {/* Input Area */}
          <Space.Compact style={{ width: '100%', marginTop: '16px' }}>
            <TextArea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Nhập câu hỏi của bạn..."
              autoSize={{ minRows: 2, maxRows: 6 }}
              onPressEnter={(e) => {
                if (e.shiftKey) return;
                e.preventDefault();
                handleSend();
              }}
            />
            <Button
              type="primary"
              size="large"
              icon={isLoading ? <LoadingOutlined /> : <SendOutlined />}
              onClick={handleSend}
              disabled={isLoading || !message.trim()}
            >
              Gửi
            </Button>
          </Space.Compact>
        </Card>
      </Content>
    </Layout>
  );
};
```

**2. Document Upload (`components/documents/DocumentUpload.tsx`):**
```tsx
import React from 'react';
import { Upload, Button, message, Card, Typography } from 'antd';
import { UploadOutlined, FileTextOutlined } from '@ant-design/icons';
import type { UploadProps } from 'antd';
import { useDocuments } from '@/hooks/useDocuments';

const { Title, Text } = Typography;

export const DocumentUpload: React.FC = () => {
  const { uploadDocument } = useDocuments();

  const props: UploadProps = {
    name: 'file',
    multiple: false,
    accept: '.pdf,.txt,.docx,.md',
    customRequest: async ({ file, onSuccess, onError }) => {
      try {
        await uploadDocument(file as File);
        message.success(`${(file as File).name} uploaded successfully`);
        onSuccess?.('ok');
      } catch (error) {
        message.error(`${(file as File).name} upload failed`);
        onError?.(error as Error);
      }
    },
  };

  return (
    <Card>
      <Title level={4}>Tải lên tài liệu</Title>
      <Upload.Dragger {...props}>
        <p className="ant-upload-drag-icon">
          <FileTextOutlined style={{ fontSize: '48px', color: '#1890ff' }} />
        </p>
        <p className="ant-upload-text">Click hoặc kéo thả file vào đây</p>
        <p className="ant-upload-hint">
          Hỗ trợ: PDF, TXT, DOCX, MD
        </p>
      </Upload.Dragger>
    </Card>
  );
};
```

**3. API Service (`services/api.ts`):**
```typescript
import axios from 'axios';

const API_BASE = process.env.VITE_API_BASE || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Chat API
export const chatAPI = {
  sendMessage: (message: string) => 
    api.post('/chat', { message }),
  
  streamMessage: async function* (message: string) {
    const response = await fetch(`${API_BASE}/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    });
    
    const reader = response.body?.getReader();
    const decoder = new TextDecoder();
    
    while (reader) {
      const { done, value } = await reader.read();
      if (done) break;
      
      const chunk = decoder.decode(value);
      const lines = chunk.split('\n');
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = JSON.parse(line.slice(6));
          yield data.text;
        }
      }
    }
  },
};

// Documents API
export const documentsAPI = {
  upload: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  list: () => api.get('/documents/list'),
  
  delete: (id: string) => api.delete(`/documents/${id}`),
};
```

**4. Custom Hook (`hooks/useChat.ts`):**
```typescript
import { useState, useCallback } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { chatAPI } from '@/services/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const queryClient = useQueryClient();

  const { mutateAsync: sendMessage, isLoading } = useMutation({
    mutationFn: async (message: string) => {
      // Add user message
      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: message,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, userMessage]);

      // Stream assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '',
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, assistantMessage]);

      for await (const chunk of chatAPI.streamMessage(message)) {
        setMessages((prev) => {
          const updated = [...prev];
          const lastMsg = updated[updated.length - 1];
          lastMsg.content += chunk;
          return updated;
        });
      }
    },
  });

  return { messages, sendMessage, isLoading };
};
```

**Design System Configuration (`theme/antd-theme.ts`):**
```typescript
import type { ThemeConfig } from 'antd';

export const theme: ThemeConfig = {
  token: {
    colorPrimary: '#1890ff',
    colorSuccess: '#52c41a',
    colorWarning: '#faad14',
    colorError: '#ff4d4f',
    colorInfo: '#1890ff',
    
    fontSize: 14,
    borderRadius: 6,
    
    // Spacing
    marginXS: 8,
    marginSM: 12,
    margin: 16,
    marginMD: 20,
    marginLG: 24,
    marginXL: 32,
  },
  components: {
    Button: {
      controlHeight: 40,
      fontSize: 14,
    },
    Input: {
      controlHeight: 40,
      fontSize: 14,
    },
    Card: {
      borderRadius: 8,
    },
  },
};
```

**Main App (`App.tsx`):**
```tsx
import React from 'react';
import { ConfigProvider, App as AntApp } from 'antd';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import viVN from 'antd/locale/vi_VN';
import { theme } from '@/theme/antd-theme';
import { AppLayout } from '@/components/layout/AppLayout';
import { ChatPage } from '@/pages/ChatPage';
import { DocumentsPage } from '@/pages/DocumentsPage';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider theme={theme} locale={viVN}>
        <AntApp>
          <BrowserRouter>
            <AppLayout>
              <Routes>
                <Route path="/" element={<ChatPage />} />
                <Route path="/documents" element={<DocumentsPage />} />
              </Routes>
            </AppLayout>
          </BrowserRouter>
        </AntApp>
      </ConfigProvider>
    </QueryClientProvider>
  );
}

export default App;
```

**Package Configuration (`package.json`):**
```json
{
  "name": "rag-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "antd": "^5.12.0",
    "@ant-design/icons": "^5.2.6",
    "react-router-dom": "^6.20.0",
    "@tanstack/react-query": "^5.12.0",
    "axios": "^1.6.2",
    "zustand": "^4.4.7"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.2.2",
    "vite": "^5.0.8",
    "eslint": "^8.55.0"
  }
}
```

---

### 2. FPT Cloud AI Models

**Purpose:** All AI capabilities via unified FPT Cloud API

**Why FPT Cloud:**
- Vietnamese-optimized models
- Low latency in Vietnam
- Competitive pricing
- OpenAI-compatible API (easy integration with LangChain)
- All models in one platform

**API Configuration:**
```python
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Base configuration for all FPT models
FPT_CONFIG = {
    "openai_api_key": os.getenv("FPT_API_KEY"),
    "openai_api_base": "https://api.fpt.ai/v1"
}

# Embedding model
embeddings = OpenAIEmbeddings(
    model="Vietnamese_Embedding",
    **FPT_CONFIG
)

# LLM model
llm = ChatOpenAI(
    model="GLM-4.5",
    temperature=0.7,
    **FPT_CONFIG
)

# Guard model
guard = ChatOpenAI(
    model="Llama-Guard-3-8B",
    temperature=0,
    **FPT_CONFIG
)
```

**Available Models:**
```python
FPT_MODELS = {
    # Embedding
    "Vietnamese_Embedding": {
        "type": "embedding",
        "provider": "AITeamVN",
        "dimensions": 1024,
        "languages": ["vi", "en"]
    },
    
    # LLM
    "GLM-4.5": {
        "type": "chat",
        "provider": "Z.ai",
        "context_window": 128000,
        "languages": ["vi", "en", "zh"]
    },
    
    # Reranker
    "bge-reranker-v2-m3": {
        "type": "reranker",
        "provider": "BAAI",
        "max_input": 512,
        "languages": ["multilingual"]
    },
    
    # Safety
    "Llama-Guard-3-8B": {
        "type": "safety",
        "provider": "Meta",
        "categories": ["violence", "sexual", "criminal", "dangerous"]
    }
}
```

**Authentication:**
1. Register at https://marketplace.fptcloud.com
2. Create API Key
3. Set environment variable: `FPT_API_KEY=your-key`
4. Use with any LangChain OpenAI-compatible class

---

### 3. Backend - FastAPI

**Purpose:** Core business logic and API endpoints

**Project Structure:**
```
backend/
├── main.py              # FastAPI app entry
├── api/
│   ├── chat.py          # Chat endpoints
│   ├── documents.py     # Document management
│   └── knowledge_base.py
├── core/
│   ├── rag.py           # RAG pipeline
│   ├── embeddings.py    # Embedding generation
│   └── retriever.py     # Document retrieval
├── models/
│   ├── schemas.py       # Pydantic models
│   └── database.py      # SQLite models
└── requirements.txt
```

**Main Application (`main.py`):**
```python
from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
import uvicorn

app = FastAPI(title="RAG API")

# Import routers
from api import chat, documents

app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

**Chat Endpoint (`api/chat.py`):**
```python
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from core.rag import RAGPipeline
import json

router = APIRouter()
rag = RAGPipeline()

@router.post("/")
async def chat(message: str):
    async def generate():
        async for chunk in rag.stream_response(message):
            yield f"data: {json.dumps({'text': chunk})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")

@router.post("/simple")
async def chat_simple(message: str):
    response = await rag.get_response(message)
    return {"answer": response}
```

**Document Upload (`api/documents.py`):**
```python
from fastapi import APIRouter, UploadFile, File
import shutil
from core.embeddings import process_document

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Save file
    file_path = f"./uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process document (async)
    await process_document(file_path)
    
    return {"filename": file.filename, "status": "processing"}

@router.get("/list")
async def list_documents():
    # Return list of documents from Qdrant metadata
    from core.retriever import get_all_documents
    documents = get_all_documents()
    return {"documents": documents}
```

---

### 4. RAG Pipeline - Core Logic

**Purpose:** The brain of the system - retrieval + reranking + generation with safety

**Enhanced RAG Pipeline (`core/rag.py`):**
```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from core.retriever import QdrantRetriever
from core.reranker import FPTReranker
from core.guard import LlamaGuard
from core.embeddings import get_embeddings
import os

class RAGPipeline:
    def __init__(self):
        self.retriever = QdrantRetriever()
        self.reranker = FPTReranker()
        self.guard = LlamaGuard()
        self.embeddings = get_embeddings()
        
        # GLM-4.5 LLM from FPT Cloud
        self.llm = ChatOpenAI(
            model="GLM-4.5",
            openai_api_key=os.getenv("FPT_API_KEY"),
            openai_api_base="https://api.fpt.ai/v1",
            temperature=0.7,
            max_tokens=2000
        )
        
        # Prompt template optimized for Vietnamese
        self.prompt = PromptTemplate(
            template="""Bạn là trợ lý AI thông minh. Sử dụng ngữ cảnh dưới đây để trả lời câu hỏi.
            Nếu không biết câu trả lời, hãy nói "Tôi không biết."
            
            Ngữ cảnh: {context}
            
            Câu hỏi: {question}
            
            Trả lời:""",
            input_variables=["context", "question"]
        )
    
    async def get_response(self, query: str) -> str:
        """
        Complete RAG pipeline with safety checks
        
        Flow:
        1. Input Guard - Check if query is safe
        2. Retrieve - Get top-20 candidates from Qdrant
        3. Rerank - Reorder and keep top-5
        4. Generate - Create response with GLM-4.5
        5. Output Guard - Check if response is safe
        """
        # Step 1: Input Guard
        is_safe_input = await self.guard.check_input(query)
        if not is_safe_input:
            return "Xin lỗi, câu hỏi của bạn chứa nội dung không phù hợp. Vui lòng thử lại."
        
        # Step 2: Retrieve candidates (top-20)
        candidates = await self.retriever.search(query, k=20)
        
        # Step 3: Rerank to top-5
        docs = await self.reranker.rerank(query, candidates, top_n=5)
        
        # Step 4: Build context and generate
        context = "\n\n".join([
            f"[Nguồn {i+1}]: {doc.page_content}" 
            for i, doc in enumerate(docs)
        ])
        
        prompt = self.prompt.format(context=context, question=query)
        
        response = await self.llm.apredict(prompt)
        
        # Step 5: Output Guard
        is_safe_output = await self.guard.check_output(response)
        if not is_safe_output:
            return "Xin lỗi, tôi không thể cung cấp câu trả lời này. Vui lòng thử câu hỏi khác."
        
        return response
    
    async def stream_response(self, query: str):
        """
        Stream response with safety checks
        """
        # Input guard
        is_safe_input = await self.guard.check_input(query)
        if not is_safe_input:
            yield "Xin lỗi, câu hỏi của bạn chứa nội dung không phù hợp."
            return
        
        # Retrieve and rerank
        candidates = await self.retriever.search(query, k=20)
        docs = await self.reranker.rerank(query, candidates, top_n=5)
        
        # Build context
        context = "\n\n".join([doc.page_content for doc in docs])
        prompt = self.prompt.format(context=context, question=query)
        
        # Stream response
        full_response = ""
        async for chunk in self.llm.astream(prompt):
            if chunk.content:
                full_response += chunk.content
                yield chunk.content
        
        # Output guard (after full response)
        is_safe_output = await self.guard.check_output(full_response)
        if not is_safe_output:
            yield "\n\n[Cảnh báo: Phản hồi có thể chứa nội dung không phù hợp]"
```

**LLM Configuration - GLM-4.5:**
```python
# GLM-4.5 from Z.ai on FPT Cloud
llm = ChatOpenAI(
    model="GLM-4.5",
    openai_api_key=os.getenv("FPT_API_KEY"),
    openai_api_base="https://api.fpt.ai/v1",
    temperature=0.7,  # Creativity level
    max_tokens=2000,  # Max response length
    streaming=True    # Enable streaming
)
```

**Model Specifications:**
| Component | Model | Provider | Purpose |
|-----------|-------|----------|---------|
| Embedding | Vietnamese_Embedding | AITeamVN | Text → Vectors |
| Reranker | bge-reranker-v2-m3 | BAAI | Reorder results |
| LLM | GLM-4.5 | Z.ai | Generate response |
| Guard | Llama-Guard-3-8B | Meta | Safety check |

---

### 5. Vector Search - Qdrant

**Purpose:** Fast, scalable vector similarity search

**Why Qdrant:**
- Production-ready vector database
- High performance (written in Rust)
- Rich filtering capabilities
- Easy Python integration
- Local or cloud deployment

**Setup:**
```bash
# Option 1: Docker
docker run -p 6333:6333 qdrant/qdrant

# Option 2: Local install
pip install qdrant-client
```

**Qdrant Retriever (`core/retriever.py`):**
```python
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain.schema import Document
from core.embeddings import get_embeddings
import uuid

class QdrantRetriever:
    def __init__(self):
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = "documents"
        self.embeddings = get_embeddings()
        
        # Create collection if not exists
        self._create_collection_if_not_exists()
    
    def _create_collection_if_not_exists(self):
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)
        
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1536,  # OpenAI embedding dimension
                    distance=Distance.COSINE
                )
            )
    
    async def add_documents(self, texts: list[str], metadata: list[dict]):
        """Add documents to Qdrant"""
        # Generate embeddings
        embeddings = self.embeddings.embed_documents(texts)
        
        # Create points
        points = []
        for i, (text, embedding, meta) in enumerate(zip(texts, embeddings, metadata)):
            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": text,
                    "metadata": meta
                }
            )
            points.append(point)
        
        # Upload to Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
    
    async def search(self, query: str, k: int = 5, filter_dict: dict = None):
        """Search for relevant documents"""
        # Generate query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # Search in Qdrant
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=k,
            query_filter=filter_dict  # Optional metadata filtering
        )
        
        # Convert to LangChain documents
        documents = []
        for result in results:
            doc = Document(
                page_content=result.payload["text"],
                metadata={
                    **result.payload["metadata"],
                    "score": result.score
                }
            )
            documents.append(doc)
        
        return documents
    
    def get_all_documents(self):
        """List all documents"""
        # Scroll through all points
        offset = None
        all_docs = []
        
        while True:
            results, offset = self.client.scroll(
                collection_name=self.collection_name,
                limit=100,
                offset=offset
            )
            
            if not results:
                break
            
            for point in results:
                all_docs.append({
                    "id": point.id,
                    "metadata": point.payload["metadata"]
                })
        
        return all_docs
```

**Advanced Filtering:**
```python
from qdrant_client.models import Filter, FieldCondition, MatchValue

# Search with metadata filter
filter_dict = Filter(
    must=[
        FieldCondition(
            key="metadata.category",
            match=MatchValue(value="technical")
        ),
        FieldCondition(
            key="metadata.year",
            match=MatchValue(value=2024)
        )
    ]
)

results = await retriever.search(
    query="What is RAG?",
    k=5,
    filter_dict=filter_dict
)
```

---

### 6. Embeddings - Vietnamese Embedding Model

**Purpose:** Convert text into numerical vectors for Vietnamese language

**Why Vietnamese Embedding from FPT Cloud:**
- Fine-tuned from BGE-M3 specifically for Vietnamese language
- Trained on 300,000+ Vietnamese query-document pairs
- Better retrieval quality for Vietnamese content
- Hosted on FPT Cloud (low latency in Vietnam)

**Embeddings Implementation (`core/embeddings.py`):**
```python
from langchain_openai import OpenAIEmbeddings
import os

def get_embeddings():
    """Get Vietnamese Embedding model from FPT Cloud"""
    return OpenAIEmbeddings(
        model="Vietnamese_Embedding",  # Model name from FPT Cloud
        openai_api_key=os.getenv("FPT_API_KEY"),
        openai_api_base="https://api.fpt.ai/v1",  # FPT Cloud endpoint
        dimensions=1024  # Vietnamese Embedding dimensions
    )

# For batch processing
async def embed_documents(texts: list[str]):
    """Embed multiple documents"""
    embeddings_model = get_embeddings()
    return await embeddings_model.aembed_documents(texts)

async def embed_query(text: str):
    """Embed a single query"""
    embeddings_model = get_embeddings()
    return await embeddings_model.aembed_query(text)
```

**Model Specifications:**
- **Model**: Vietnamese_Embedding (AITeamVN)
- **Base Model**: BGE-M3
- **Dimensions**: 1024
- **Max Input**: 512 tokens
- **Language**: Optimized for Vietnamese
- **Use Cases**: Semantic search, RAG, text clustering

**Configuration in Qdrant:**
```python
from qdrant_client.models import Distance, VectorParams

# Update collection config for Vietnamese Embedding
self.client.create_collection(
    collection_name=self.collection_name,
    vectors_config=VectorParams(
        size=1024,  # Vietnamese Embedding dimension
        distance=Distance.COSINE
    )
)
```

---

### 7. Reranking - BGE Reranker v2-m3

**Purpose:** Improve retrieval quality by reordering search results

**Why Use Reranking:**
- Vector search retrieves candidates based on embedding similarity
- Reranker uses cross-attention to deeply compare query and documents
- Can significantly improve top-K accuracy (especially top-1 to top-5)
- Reduces false positives from initial retrieval

**Reranker Implementation (`core/reranker.py`):**
```python
from langchain_openai import OpenAI
import os
import requests
from typing import List
from langchain.schema import Document

class FPTReranker:
    def __init__(self):
        self.api_key = os.getenv("FPT_API_KEY")
        self.api_base = "https://api.fpt.ai/v1"
        self.model = "bge-reranker-v2-m3"
    
    async def rerank(
        self, 
        query: str, 
        documents: List[Document], 
        top_n: int = 5
    ) -> List[Document]:
        """
        Rerank documents using BGE Reranker v2-m3
        
        Args:
            query: User query
            documents: List of candidate documents
            top_n: Number of top documents to return
        
        Returns:
            Reranked list of documents
        """
        # Prepare documents for reranking
        texts = [doc.page_content for doc in documents]
        
        # Call FPT Cloud Reranker API
        response = requests.post(
            f"{self.api_base}/rerank",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "query": query,
                "documents": texts,
                "top_n": top_n
            }
        )
        
        results = response.json()
        
        # Reorder documents based on reranking scores
        reranked_docs = []
        for result in results["results"]:
            idx = result["index"]
            score = result["relevance_score"]
            doc = documents[idx]
            doc.metadata["rerank_score"] = score
            reranked_docs.append(doc)
        
        return reranked_docs[:top_n]

# Usage
reranker = FPTReranker()
```

**Integration with Retrieval Pipeline:**
```python
async def retrieve_and_rerank(
    query: str, 
    k_initial: int = 20, 
    k_final: int = 5
):
    """
    Two-stage retrieval: Vector search + Reranking
    
    1. Retrieve top-K candidates from Qdrant (k=20)
    2. Rerank candidates and keep top-N (n=5)
    """
    # Stage 1: Vector search
    retriever = QdrantRetriever()
    candidates = await retriever.search(query, k=k_initial)
    
    # Stage 2: Rerank
    reranker = FPTReranker()
    final_docs = await reranker.rerank(query, candidates, top_n=k_final)
    
    return final_docs
```

**Model Specifications:**
- **Model**: bge-reranker-v2-m3 (BAAI)
- **Type**: Cross-encoder reranker
- **Languages**: Multilingual (including Vietnamese)
- **Max Input**: Query + Document up to 512 tokens
- **Output**: Relevance score between 0-1

**Performance Gains:**
- Typical improvement: 5-15% in top-5 accuracy
- Best for: Long documents, ambiguous queries
- Trade-off: Additional API call (~100-200ms latency)

---

### 8. Content Safety - Llama Guard 3

**Purpose:** Filter harmful content in user queries and AI responses

**Why Use Llama Guard:**
- Detect harmful, toxic, or inappropriate content
- Support Vietnamese language
- Protect users from unsafe AI outputs
- Comply with content safety regulations

**Guard Implementation (`core/guard.py`):**
```python
from langchain_openai import ChatOpenAI
import os

class LlamaGuard:
    def __init__(self):
        self.guard_model = ChatOpenAI(
            model="Llama-Guard-3-8B",
            openai_api_key=os.getenv("FPT_API_KEY"),
            openai_api_base="https://api.fpt.ai/v1",
            temperature=0  # Deterministic for safety checks
        )
        
        # Safety categories (customizable)
        self.categories = [
            "Violence & Hate Speech",
            "Sexual Content",
            "Criminal Planning",
            "Dangerous Content",
            "Self-Harm"
        ]
    
    async def check_input(self, user_query: str) -> bool:
        """
        Check if user query is safe
        
        Returns:
            True if safe, False if harmful
        """
        prompt = f"""Task: Check if the following user query violates any safety policies.

Safety Categories:
{chr(10).join(f'- {cat}' for cat in self.categories)}

User Query: {user_query}

Is this query safe? Answer only 'safe' or 'unsafe' with the violated category."""

        response = await self.guard_model.apredict(prompt)
        
        return "safe" in response.lower()
    
    async def check_output(self, ai_response: str) -> bool:
        """
        Check if AI response is safe
        
        Returns:
            True if safe, False if harmful
        """
        prompt = f"""Task: Check if the following AI response violates any safety policies.

Safety Categories:
{chr(10).join(f'- {cat}' for cat in self.categories)}

AI Response: {ai_response}

Is this response safe? Answer only 'safe' or 'unsafe' with the violated category."""

        response = await self.guard_model.apredict(prompt)
        
        return "safe" in response.lower()
    
    async def get_safety_report(self, text: str) -> dict:
        """
        Get detailed safety analysis
        
        Returns:
            {
                "is_safe": bool,
                "violated_categories": list[str],
                "confidence": float
            }
        """
        prompt = f"""Analyze the safety of this text:

Text: {text}

Provide analysis in JSON format:
{{
    "is_safe": true/false,
    "violated_categories": ["category1", "category2"],
    "confidence": 0.95
}}"""

        response = await self.guard_model.apredict(prompt)
        import json
        return json.loads(response)

# Usage
guard = LlamaGuard()
```

**Integration Patterns:**

**1. Pre-generation Check (Input Guard):**
```python
async def chat_with_guard(query: str):
    # Check user input
    is_safe = await guard.check_input(query)
    
    if not is_safe:
        return "Xin lỗi, câu hỏi của bạn chứa nội dung không phù hợp."
    
    # Continue with RAG pipeline
    response = await rag_pipeline.get_response(query)
    return response
```

**2. Post-generation Check (Output Guard):**
```python
async def generate_safe_response(query: str):
    # Generate response
    response = await rag_pipeline.get_response(query)
    
    # Check output safety
    is_safe = await guard.check_output(response)
    
    if not is_safe:
        return "Tôi không thể cung cấp câu trả lời này."
    
    return response
```

**3. Bidirectional Guard (Both):**
```python
async def safe_chat_pipeline(query: str):
    # Input guard
    if not await guard.check_input(query):
        return {"error": "Unsafe input"}
    
    # Generate
    response = await rag_pipeline.get_response(query)
    
    # Output guard
    if not await guard.check_output(response):
        return {"error": "Unsafe output"}
    
    return {"response": response}
```

**Model Specifications:**
- **Model**: Llama-Guard-3-8B (Meta)
- **Type**: Safety classifier
- **Languages**: Multilingual (including Vietnamese)
- **Categories**: Violence, Sexual, Criminal, Dangerous, Self-Harm
- **Output**: Safe/Unsafe + Category

**Performance Considerations:**
- Latency: ~200-500ms per check
- Accuracy: 90%+ for common safety violations
- Trade-off: Better safety vs. slower response time

**Best Practices:**
- Use input guard for all user queries
- Use output guard for high-risk applications
- Cache results for repeated queries
- Monitor false positives and adjust categories

---

### 9. Document Processing

**Purpose:** Extract text from various file formats and prepare for indexing

**Document Processor (`core/embeddings.py` continued):**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader
)
import os

async def process_document(file_path: str):
    """Process uploaded document and add to vector store"""
    # 1. Load document based on file type
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.pdf':
        loader = PyPDFLoader(file_path)
    elif file_ext == '.txt':
        loader = TextLoader(file_path)
    elif file_ext in ['.doc', '.docx']:
        loader = UnstructuredWordDocumentLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")
    
    documents = loader.load()
    
    # 2. Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # 3. Extract text and metadata
    texts = [chunk.page_content for chunk in chunks]
    metadata = [
        {
            "source": file_path,
            "filename": os.path.basename(file_path),
            "chunk_index": i,
            "file_type": file_ext
        }
        for i, chunk in enumerate(chunks)
    ]
    
    # 4. Add to Qdrant
    from core.retriever import QdrantRetriever
    retriever = QdrantRetriever()
    await retriever.add_documents(texts, metadata)
    
    return len(chunks)
```

**Supported File Types:**
- PDF (`.pdf`)
- Text (`.txt`)
- Word (`.doc`, `.docx`)
- Markdown (`.md`)

**Chunking Strategy:**
- Chunk size: 1000 characters
- Overlap: 200 characters (preserves context)
- Smart splitting on paragraphs → sentences → words

**Installation Requirements:**
```bash
pip install pypdf unstructured python-docx langchain
```

---

## Complete System Flow

### Document Ingestion Flow
```
1. User uploads file via Gradio
   ↓
2. Gradio sends file to FastAPI /documents/upload
   ↓
3. FastAPI saves file to ./uploads/
   ↓
4. process_document() extracts text
   ↓
5. Split text into chunks (1000 chars, 200 overlap)
   ↓
6. Generate embeddings via OpenAI
   ↓
7. Store in Qdrant with metadata
   ↓
8. Return success to Gradio
```

### Chat Query Flow
```
1. User sends message via Gradio
   ↓
2. Gradio calls FastAPI /chat
   ↓
3. RAGPipeline.get_response(message):
   a. Embed query → Search Qdrant (top-5 docs)
   b. Build prompt with context
   c. Call LiteLLM → LLM generates response
   ↓
4. Stream response back to Gradio
   ↓
5. Display to user
```

---

## Quick Start Deployment

## Quick Start Deployment

### Prerequisites

**1. Development Tools:**
```bash
# Node.js 18+ & pnpm
node --version  # v18+
pnpm --version  # 8+

# Python 3.10+
python --version  # 3.10+
```

**2. Kubernetes Cluster:**
```bash
# kubectl
kubectl version --client

# Helm (optional)
helm version

# Access to K8s cluster
kubectl cluster-info
```

**3. Container Registry:**
- Docker Hub, GitHub Container Registry, or private registry
- Credentials configured

### Local Development

**1. Clone Repository:**
```bash
git clone https://github.com/your-org/rag-system.git
cd rag-system
```

**2. Setup Backend:**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env and add FPT_API_KEY

# Run locally
uvicorn main:app --reload --port 8000
```

**3. Setup Frontend:**
```bash
cd frontend

# Install dependencies
pnpm install

# Create .env file
cp .env.example .env
# Edit .env: VITE_API_BASE=http://localhost:8000

# Run dev server
pnpm dev
```

**4. Setup Qdrant (Docker):**
```bash
docker run -d -p 6333:6333 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant
```

### Production Deployment (Kubernetes)

**1. Build Images:**
```bash
# Backend
docker build -t your-registry/rag-backend:v1.0.0 ./backend
docker push your-registry/rag-backend:v1.0.0

# Frontend
docker build -t your-registry/rag-frontend:v1.0.0 ./frontend
docker push your-registry/rag-frontend:v1.0.0
```

**2. Update K8s Manifests:**
```bash
# Edit image references in k8s/*.yaml
sed -i 's|your-registry|your-actual-registry|g' k8s/*.yaml
```

**3. Create Secrets:**
```bash
kubectl create namespace rag-system

kubectl create secret generic rag-secrets \
  --from-literal=FPT_API_KEY=your-api-key \
  -n rag-system
```

**4. Deploy:**
```bash
# Option 1: Using kubectl
./deploy.sh v1.0.0

# Option 2: Using Helm
helm install rag-system ./rag-system-chart \
  -n rag-system \
  --create-namespace \
  --set secrets.fptApiKey=your-api-key
```

**5. Verify:**
```bash
# Check pods
kubectl get pods -n rag-system

# Check services
kubectl get svc -n rag-system

# Get Ingress URL
kubectl get ingress -n rag-system
```

### Environment Variables

**Backend (`.env`):**
```bash
# FPT Cloud API
FPT_API_KEY=your-fpt-api-key-here

# Qdrant
QDRANT_HOST=localhost  # or qdrant-service in K8s
QDRANT_PORT=6333

# Redis (optional for caching)
REDIS_HOST=localhost  # or redis-service in K8s
REDIS_PORT=6379

# App Config
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE=52428800  # 50MB
```

**Frontend (`.env`):**
```bash
VITE_API_BASE=http://localhost:8000  # Dev
# VITE_API_BASE=/api  # Production (via Ingress)
```

### Complete System Flow

### Document Ingestion Flow
```
1. User uploads file via React UI (Ant Design Upload)
   ↓
2. React sends file to FastAPI /documents/upload
   ↓
3. FastAPI saves file to Persistent Volume
   ↓
4. process_document() extracts text
   ↓
5. Split text into chunks (1000 chars, 200 overlap)
   ↓
6. Generate embeddings via Vietnamese_Embedding (FPT Cloud)
   ↓
7. Store in Qdrant (1024-dim vectors)
   ↓
8. Return success to React UI
```

### Chat Query Flow (with Safety)
```
1. User sends message via React Chat Interface
   ↓
2. React calls FastAPI /chat (via Axios)
   ↓
3. RAGPipeline.get_response(message):
   
   a. Input Guard (Llama-Guard-3-8B)
      → Check if query is safe
      → If unsafe, return warning
   
   b. Retrieval (Vietnamese_Embedding + Qdrant)
      → Embed query (1024-dim vector)
      → Search top-20 candidates
   
   c. Reranking (bge-reranker-v2-m3)
      → Reorder candidates
      → Keep top-5 most relevant
   
   d. Generation (GLM-4.5)
      → Build context from top-5 docs
      → Generate response
   
   e. Output Guard (Llama-Guard-3-8B)
      → Check if response is safe
      → If unsafe, return filtered message
   ↓
4. Stream response back via SSE
   ↓
5. React displays streaming message in chat UI
```

### Kubernetes Request Flow
```
User Browser
   ↓ HTTPS
Ingress Controller (NGINX)
   ↓ /api/* → Backend Service
   ↓ /* → Frontend Service
   │
   ├─→ Frontend Pod (React)
   │   └─→ Serve static files
   │
   └─→ Backend Pod (FastAPI)
       ├─→ Qdrant Service (StatefulSet)
       │   └─→ Vector search
       │
       ├─→ Redis Service (Cache)
       │   └─→ Response caching
       │
       └─→ FPT Cloud API (External)
           ├─→ Vietnamese_Embedding
           ├─→ bge-reranker-v2-m3
           ├─→ GLM-4.5
           └─→ Llama-Guard-3-8B
```

---

## Kubernetes Deployment

### Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Kubernetes Cluster                   │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │              Ingress Controller                 │    │
│  │          (NGINX/Traefik/Istio)                 │    │
│  └─────────────────┬──────────────────────────────┘    │
│                    │                                     │
│       ┌────────────┴────────────┐                      │
│       │                         │                       │
│  ┌────▼─────┐            ┌─────▼─────┐                │
│  │          │            │           │                 │
│  │ Frontend │            │  Backend  │                 │
│  │ Service  │            │  Service  │                 │
│  │          │            │           │                 │
│  │ ┌──────┐ │            │ ┌───────┐ │                │
│  │ │ Pod  │ │            │ │  Pod  │ │                │
│  │ │React │ │            │ │FastAPI│ │                │
│  │ └──────┘ │            │ └───────┘ │                │
│  │ Replicas:│            │ Replicas: │                 │
│  │    2-5   │            │    3-10   │                 │
│  └──────────┘            └─────┬─────┘                 │
│                                │                        │
│                     ┌──────────┴─────────┐             │
│                     │                    │             │
│              ┌──────▼──────┐      ┌─────▼──────┐      │
│              │             │      │            │      │
│              │   Qdrant    │      │  Redis     │      │
│              │  StatefulSet│      │  (Cache)   │      │
│              │             │      │            │      │
│              │  ┌────────┐ │      │  ┌───────┐ │      │
│              │  │  Pod-0 │ │      │  │  Pod  │ │      │
│              │  └────────┘ │      │  └───────┘ │      │
│              │  ┌────────┐ │      │            │      │
│              │  │  Pod-1 │ │      │            │      │
│              │  └────────┘ │      │            │      │
│              │             │      │            │      │
│              │  PVC: 50Gi  │      │            │      │
│              └─────────────┘      └────────────┘      │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Namespace Configuration

**Create Namespace (`k8s/namespace.yaml`):**
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: rag-system
  labels:
    name: rag-system
    environment: production
```

---

### 1. ConfigMap & Secrets

**ConfigMap (`k8s/configmap.yaml`):**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: rag-config
  namespace: rag-system
data:
  # API URLs
  BACKEND_URL: "http://backend-service:8000"
  QDRANT_HOST: "qdrant-service"
  QDRANT_PORT: "6333"
  REDIS_HOST: "redis-service"
  REDIS_PORT: "6379"
  
  # App Config
  LOG_LEVEL: "INFO"
  MAX_UPLOAD_SIZE: "52428800"  # 50MB
  CHUNK_SIZE: "1000"
  CHUNK_OVERLAP: "200"
```

**Secrets (`k8s/secrets.yaml`):**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: rag-secrets
  namespace: rag-system
type: Opaque
stringData:
  FPT_API_KEY: "your-fpt-api-key-here"
  # Add other secrets as needed
```

**Create secret from command line:**
```bash
kubectl create secret generic rag-secrets \
  --from-literal=FPT_API_KEY=your-api-key \
  -n rag-system
```

---

### 2. Backend Deployment

**Backend Deployment (`k8s/backend-deployment.yaml`):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: rag-system
  labels:
    app: backend
    version: v1
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
        version: v1
    spec:
      containers:
      - name: backend
        image: your-registry/rag-backend:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: FPT_API_KEY
          valueFrom:
            secretKeyRef:
              name: rag-secrets
              key: FPT_API_KEY
        - name: QDRANT_HOST
          valueFrom:
            configMapKeyRef:
              name: rag-config
              key: QDRANT_HOST
        - name: QDRANT_PORT
          valueFrom:
            configMapKeyRef:
              name: rag-config
              key: QDRANT_PORT
        - name: REDIS_HOST
          valueFrom:
            configMapKeyRef:
              name: rag-config
              key: REDIS_HOST
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        volumeMounts:
        - name: uploads
          mountPath: /app/uploads
      volumes:
      - name: uploads
        persistentVolumeClaim:
          claimName: uploads-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: rag-system
  labels:
    app: backend
spec:
  type: ClusterIP
  ports:
  - port: 8000
    targetPort: 8000
    protocol: TCP
    name: http
  selector:
    app: backend
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: rag-system
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

### 3. Frontend Deployment

**Frontend Deployment (`k8s/frontend-deployment.yaml`):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: rag-system
  labels:
    app: frontend
    version: v1
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
        version: v1
    spec:
      containers:
      - name: frontend
        image: your-registry/rag-frontend:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 80
          name: http
        env:
        - name: VITE_API_BASE
          valueFrom:
            configMapKeyRef:
              name: rag-config
              key: BACKEND_URL
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 80
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: rag-system
  labels:
    app: frontend
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
  selector:
    app: frontend
```

---

### 4. Qdrant StatefulSet

**Qdrant Deployment (`k8s/qdrant-statefulset.yaml`):**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: qdrant-service
  namespace: rag-system
  labels:
    app: qdrant
spec:
  clusterIP: None
  ports:
  - port: 6333
    targetPort: 6333
    name: http
  - port: 6334
    targetPort: 6334
    name: grpc
  selector:
    app: qdrant
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: qdrant
  namespace: rag-system
  labels:
    app: qdrant
spec:
  serviceName: qdrant-service
  replicas: 2
  selector:
    matchLabels:
      app: qdrant
  template:
    metadata:
      labels:
        app: qdrant
    spec:
      containers:
      - name: qdrant
        image: qdrant/qdrant:latest
        ports:
        - containerPort: 6333
          name: http
        - containerPort: 6334
          name: grpc
        env:
        - name: QDRANT__SERVICE__GRPC_PORT
          value: "6334"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        volumeMounts:
        - name: qdrant-storage
          mountPath: /qdrant/storage
        livenessProbe:
          httpGet:
            path: /
            port: 6333
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /readyz
            port: 6333
          initialDelaySeconds: 10
          periodSeconds: 5
  volumeClaimTemplates:
  - metadata:
      name: qdrant-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 50Gi
```

---

### 5. Redis Deployment (Caching)

**Redis Deployment (`k8s/redis-deployment.yaml`):**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: rag-system
  labels:
    app: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
          name: redis
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
        volumeMounts:
        - name: redis-data
          mountPath: /data
      volumes:
      - name: redis-data
        emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: rag-system
  labels:
    app: redis
spec:
  type: ClusterIP
  ports:
  - port: 6379
    targetPort: 6379
    name: redis
  selector:
    app: redis
```

---

### 6. Ingress Configuration

**Ingress (`k8s/ingress.yaml`):**
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rag-ingress
  namespace: rag-system
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
spec:
  tls:
  - hosts:
    - rag.yourdomain.com
    secretName: rag-tls
  rules:
  - host: rag.yourdomain.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
```

---

### 7. Persistent Volume Claims

**PVC for Uploads (`k8s/pvc.yaml`):**
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: uploads-pvc
  namespace: rag-system
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Gi
  storageClassName: standard
```

---

### 8. Deployment Script

**Deploy Script (`deploy.sh`):**
```bash
#!/bin/bash

set -e

NAMESPACE="rag-system"
REGISTRY="your-registry"
VERSION=${1:-latest}

echo "🚀 Deploying RAG System v${VERSION} to Kubernetes..."

# Create namespace
kubectl apply -f k8s/namespace.yaml

# Apply ConfigMap and Secrets
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml

# Apply PVCs
kubectl apply -f k8s/pvc.yaml

# Deploy Redis
echo "📦 Deploying Redis..."
kubectl apply -f k8s/redis-deployment.yaml

# Deploy Qdrant
echo "📦 Deploying Qdrant..."
kubectl apply -f k8s/qdrant-statefulset.yaml

# Wait for Qdrant to be ready
echo "⏳ Waiting for Qdrant..."
kubectl wait --for=condition=ready pod -l app=qdrant -n ${NAMESPACE} --timeout=300s

# Deploy Backend
echo "📦 Deploying Backend..."
kubectl apply -f k8s/backend-deployment.yaml

# Wait for Backend to be ready
echo "⏳ Waiting for Backend..."
kubectl wait --for=condition=ready pod -l app=backend -n ${NAMESPACE} --timeout=300s

# Deploy Frontend
echo "📦 Deploying Frontend..."
kubectl apply -f k8s/frontend-deployment.yaml

# Deploy Ingress
echo "📦 Deploying Ingress..."
kubectl apply -f k8s/ingress.yaml

echo "✅ Deployment complete!"
echo ""
echo "📊 Check status:"
echo "  kubectl get pods -n ${NAMESPACE}"
echo ""
echo "🔍 View logs:"
echo "  kubectl logs -f deployment/backend -n ${NAMESPACE}"
echo ""
echo "🌐 Access application:"
echo "  https://rag.yourdomain.com"
```

**Make executable:**
```bash
chmod +x deploy.sh
```

**Run deployment:**
```bash
./deploy.sh v1.0.0
```

---

### 9. Helm Chart (Alternative)

**Helm Chart Structure:**
```
rag-system-chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── qdrant-statefulset.yaml
│   ├── redis-deployment.yaml
│   ├── services.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   └── pvc.yaml
└── README.md
```

**Chart.yaml:**
```yaml
apiVersion: v2
name: rag-system
description: RAG System with Vietnamese AI Models
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - rag
  - ai
  - chatbot
maintainers:
  - name: Your Team
    email: team@example.com
```

**values.yaml:**
```yaml
namespace: rag-system

backend:
  replicas: 3
  image:
    repository: your-registry/rag-backend
    tag: latest
    pullPolicy: Always
  resources:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "2000m"
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

frontend:
  replicas: 2
  image:
    repository: your-registry/rag-frontend
    tag: latest
    pullPolicy: Always
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"

qdrant:
  replicas: 2
  storage: 50Gi
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "4Gi"
      cpu: "2000m"

redis:
  enabled: true
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"

ingress:
  enabled: true
  host: rag.yourdomain.com
  tls:
    enabled: true
    secretName: rag-tls

secrets:
  fptApiKey: "your-fpt-api-key"
```

**Install with Helm:**
```bash
# Install
helm install rag-system ./rag-system-chart -n rag-system --create-namespace

# Upgrade
helm upgrade rag-system ./rag-system-chart -n rag-system

# Uninstall
helm uninstall rag-system -n rag-system
```

---

### 10. CI/CD Pipeline (GitHub Actions)

**GitHub Actions Workflow (`.github/workflows/deploy.yaml`):**
```yaml
name: Build and Deploy to K8s

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME_BACKEND: ${{ github.repository }}/backend
  IMAGE_NAME_FRONTEND: ${{ github.repository }}/frontend

jobs:
  build-backend:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_BACKEND }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push Backend
        uses: docker/build-push-action@v4
        with:
          context: ./backend
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

  build-frontend:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME_FRONTEND }}

      - name: Build and push Frontend
        uses: docker/build-push-action@v4
        with:
          context: ./frontend
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

  deploy:
    runs-on: ubuntu-latest
    needs: [build-backend, build-frontend]
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Set up kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'latest'

      - name: Configure kubectl
        run: |
          mkdir -p $HOME/.kube
          echo "${{ secrets.KUBECONFIG }}" | base64 -d > $HOME/.kube/config

      - name: Deploy to Kubernetes
        run: |
          ./deploy.sh ${{ github.sha }}

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/backend -n rag-system
          kubectl rollout status deployment/frontend -n rag-system
```

---

### 11. Monitoring & Observability

**Prometheus ServiceMonitor (`k8s/monitoring/servicemonitor.yaml`):**
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: rag-backend-monitor
  namespace: rag-system
  labels:
    app: backend
spec:
  selector:
    matchLabels:
      app: backend
  endpoints:
  - port: http
    path: /metrics
    interval: 30s
```

**Grafana Dashboard ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: rag-dashboard
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  rag-metrics.json: |
    {
      "dashboard": {
        "title": "RAG System Metrics",
        "panels": [
          {
            "title": "Request Rate",
            "targets": [
              {
                "expr": "rate(http_requests_total[5m])"
              }
            ]
          },
          {
            "title": "Response Time",
            "targets": [
              {
                "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
              }
            ]
          }
        ]
      }
    }
```

---

### 12. Useful Commands

**View Resources:**
```bash
# All resources
kubectl get all -n rag-system

# Pods
kubectl get pods -n rag-system -o wide

# Services
kubectl get svc -n rag-system

# Ingress
kubectl get ingress -n rag-system
```

**Logs:**
```bash
# Backend logs
kubectl logs -f deployment/backend -n rag-system

# Frontend logs
kubectl logs -f deployment/frontend -n rag-system

# Qdrant logs
kubectl logs -f statefulset/qdrant -n rag-system
```

**Debugging:**
```bash
# Describe pod
kubectl describe pod <pod-name> -n rag-system

# Execute command in pod
kubectl exec -it <pod-name> -n rag-system -- /bin/bash

# Port forward for local testing
kubectl port-forward svc/backend-service 8000:8000 -n rag-system
kubectl port-forward svc/frontend-service 8080:80 -n rag-system
```

**Scaling:**
```bash
# Manual scaling
kubectl scale deployment backend --replicas=5 -n rag-system

# Check HPA status
kubectl get hpa -n rag-system
```

**Updates:**
```bash
# Rolling update
kubectl set image deployment/backend backend=new-image:tag -n rag-system

# Rollback
kubectl rollout undo deployment/backend -n rag-system

# Check rollout status
kubectl rollout status deployment/backend -n rag-system
```

### Docker Compose (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  # Vector Database
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage
    restart: unless-stopped

  # FastAPI Backend
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - FPT_API_KEY=${FPT_API_KEY}
      - QDRANT_HOST=qdrant
      - QDRANT_PORT=6333
    depends_on:
      - qdrant
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped

  # Gradio UI
  gradio:
    build: ./frontend
    ports:
      - "7860:7860"
    environment:
      - API_BASE=http://backend:8000
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  qdrant_data:
```

### Backend Dockerfile (`backend/Dockerfile`)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Requirements (`backend/requirements.txt`)

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
langchain==0.1.0
langchain-openai==0.0.2
qdrant-client==1.7.0
pypdf==3.17.1
python-docx==1.1.0
python-multipart==0.0.6
requests==2.31.0
```

### Gradio Dockerfile (`frontend/Dockerfile`)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir gradio requests

# Copy application
COPY gradio_app.py .

# Expose port
EXPOSE 7860

# Run application
CMD ["python", "gradio_app.py"]
```

### Start Everything

```bash
# Create .env file with FPT API key
echo "FPT_API_KEY=your-fpt-api-key" > .env

# Start all services
docker-compose up -d

# Access Gradio UI at http://localhost:7860
```

---

## Monitoring & Debugging

### Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    """Check if all services are healthy"""
    checks = {
        "api": "ok",
        "qdrant": check_qdrant(),
        "fpt_cloud": check_fpt_cloud()
    }
    
    all_healthy = all(v == "ok" for v in checks.values())
    status_code = 200 if all_healthy else 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if all_healthy else "unhealthy",
            "checks": checks
        }
    )

def check_qdrant():
    try:
        from core.retriever import QdrantRetriever
        retriever = QdrantRetriever()
        retriever.client.get_collections()
        return "ok"
    except Exception as e:
        return f"error: {str(e)}"

def check_fpt_cloud():
    try:
        # Test FPT Cloud API connectivity
        import requests
        response = requests.get(
            "https://api.fpt.ai/v1/models",
            headers={"Authorization": f"Bearer {os.getenv('FPT_API_KEY')}"}
        )
        return "ok" if response.status_code == 200 else "error"
    except:
        return "error: cannot connect"
```
            "status": "healthy" if all_healthy else "unhealthy",
            "checks": checks
        }
    )

def check_qdrant():
    try:
        from core.retriever import QdrantRetriever
        retriever = QdrantRetriever()
        retriever.client.get_collections()
        return "ok"
    except Exception as e:
        return f"error: {str(e)}"

def check_litellm():
    try:
        response = requests.get("http://localhost:4000/health")
        return "ok" if response.status_code == 200 else "error"
    except:
        return "error: cannot connect"
```

### Logging

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Use in code
logger.info(f"Processing document: {filename}")
logger.error(f"Failed to upload to Qdrant: {e}")
```

---

## Project Structure

```
rag-system/
├── frontend/                    # React + Ant Design UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── chat/           # Chat interface components
│   │   │   ├── documents/      # Document management
│   │   │   ├── layout/         # Layout components
│   │   │   └── common/         # Shared components
│   │   ├── pages/              # Page components
│   │   ├── hooks/              # Custom React hooks
│   │   ├── services/           # API services
│   │   ├── store/              # State management
│   │   ├── theme/              # Ant Design theme
│   │   ├── types/              # TypeScript types
│   │   └── App.tsx
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   └── .env.example
│
├── backend/                     # FastAPI Backend
│   ├── main.py                 # FastAPI app entry
│   ├── api/
│   │   ├── chat.py             # Chat endpoints
│   │   └── documents.py        # Document endpoints
│   ├── core/
│   │   ├── rag.py              # RAG pipeline
│   │   ├── retriever.py        # Qdrant retriever
│   │   ├── reranker.py         # BGE Reranker
│   │   ├── guard.py            # Llama Guard
│   │   └── embeddings.py       # Document processing
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── k8s/                         # Kubernetes Manifests
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── secrets.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── qdrant-statefulset.yaml
│   ├── redis-deployment.yaml
│   ├── ingress.yaml
│   ├── pvc.yaml
│   └── monitoring/
│       ├── servicemonitor.yaml
│       └── grafana-dashboard.yaml
│
├── rag-system-chart/            # Helm Chart (Optional)
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── templates/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── ingress.yaml
│   │   └── ...
│   └── README.md
│
├── .github/
│   └── workflows/
│       └── deploy.yaml          # CI/CD Pipeline
│
├── scripts/
│   ├── deploy.sh                # K8s deployment script
│   ├── build.sh                 # Build Docker images
│   └── test.sh                  # Run tests
│
├── docs/
│   ├── architecture.md          # This file
│   ├── api.md                   # API documentation
│   └── deployment.md            # Deployment guide
│
├── docker-compose.yml           # Local development only
├── .gitignore
└── README.md
```

---

## Common Tasks

### Add New Document Type Support

```python
# In core/embeddings.py
elif file_ext == '.csv':
    from langchain.document_loaders import CSVLoader
    loader = CSVLoader(file_path)
elif file_ext == '.json':
    from langchain.document_loaders import JSONLoader
    loader = JSONLoader(file_path, jq_schema='.[]', text_content=False)
```

### Change LLM Model

```python
# In core/rag.py
self.llm = ChatOpenAI(
    model="GLM-4.5",  # or another FPT Cloud model
    openai_api_key=os.getenv("FPT_API_KEY"),
    openai_api_base="https://api.fpt.ai/v1",
    temperature=0.7
)
```

### Adjust Chunk Size

```python
# In core/embeddings.py
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,   # Smaller chunks for more precise retrieval
    chunk_overlap=100  # Adjust overlap
)
```

### Add Metadata Filtering

```python
# In core/retriever.py
from qdrant_client.models import Filter, FieldCondition, MatchValue

filter_dict = Filter(
    must=[
        FieldCondition(
            key="metadata.category",
            match=MatchValue(value="technical")
        )
    ]
)

results = await retriever.search(query, k=5, filter_dict=filter_dict)
```

### Scale Deployments in K8s

```bash
# Scale backend manually
kubectl scale deployment backend --replicas=5 -n rag-system

# Update HPA settings
kubectl patch hpa backend-hpa -n rag-system \
  --patch '{"spec":{"maxReplicas":20}}'

# Scale Qdrant StatefulSet
kubectl scale statefulset qdrant --replicas=3 -n rag-system
```

### Update Docker Images

```bash
# Build new version
docker build -t your-registry/rag-backend:v1.0.1 ./backend
docker push your-registry/rag-backend:v1.0.1

# Update K8s deployment
kubectl set image deployment/backend \
  backend=your-registry/rag-backend:v1.0.1 \
  -n rag-system

# Check rollout status
kubectl rollout status deployment/backend -n rag-system
```

### Add New UI Component

```tsx
// In frontend/src/components/chat/CustomComponent.tsx
import React from 'react';
import { Card, Typography } from 'antd';

const { Title, Text } = Typography;

export const CustomComponent: React.FC = () => {
  return (
    <Card>
      <Title level={4}>Custom Feature</Title>
      <Text>Your content here</Text>
    </Card>
  );
};
```

### Configure Custom Theme

```typescript
// In frontend/src/theme/antd-theme.ts
export const theme: ThemeConfig = {
  token: {
    colorPrimary: '#00b96b',  // Change primary color
    borderRadius: 8,
    // Add more customizations
  },
  components: {
    Button: {
      controlHeight: 44,  // Larger buttons
      primaryColor: '#00b96b',
    },
  },
};
```

---

## Performance Tips

1. **Use smaller embedding model** for faster processing:
   ```python
   embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
   ```

2. **Enable LiteLLM caching** to reduce API calls:
   ```yaml
   cache:
     type: redis
     host: localhost
   ```

3. **Batch document processing** for multiple files:
   ```python
   for file in files:
       await process_document(file)  # Process in parallel
   ```

4. **Optimize Qdrant** for production:
   ```python
   self.client.create_collection(
       collection_name=self.collection_name,
       vectors_config=VectorParams(
           size=1536,
           distance=Distance.COSINE,
           on_disk=True  # Use disk storage for large datasets
       )
   )
   ```

---

## Troubleshooting

### Qdrant Connection Error
```bash
# Check if Qdrant is running
curl http://localhost:6333/health

# Restart Qdrant
docker restart qdrant
```

### LiteLLM API Error
```bash
# Check LiteLLM logs
curl http://localhost:4000/health

# Verify API keys in config
```

### Slow Response Times
- Reduce `k` parameter (retrieve fewer documents)
- Use smaller embedding model
- Enable caching in LiteLLM
- Check network latency to LLM API

### Poor Retrieval Quality
- Increase chunk overlap (e.g., 300 chars)
- Adjust chunk size (try 500-1500)
- Add more documents to knowledge base
- Use better query phrasing

---

## Next Steps

### Features to Add
- [ ] User authentication
- [ ] Multiple knowledge bases per user
- [ ] Conversation history persistence
- [ ] Document deletion
- [ ] Search filters in UI
- [ ] Export chat history
- [ ] Metrics dashboard

### Improvements
- [ ] Add tests (pytest)
- [ ] CI/CD pipeline
- [ ] Production logging (Sentry)
- [ ] Rate limiting
- [ ] API documentation (Swagger)
- [ ] Performance monitoring

---

## References

- [Gradio Documentation](https://www.gradio.app/docs)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [LangChain Documentation](https://python.langchain.com/)

---

## Version History

- v1.0.0 (2025-11-02): Production-ready architecture
  - React + Ant Design (Design System)
  - Kubernetes deployment
  - FPT Cloud AI models (Vietnamese-optimized)
  - Complete RAG pipeline with safety guards
  - Auto-scaling and monitoring

---

## FPT Cloud Models Summary

All AI capabilities in this system are powered by FPT Cloud Marketplace models:

### Complete Model Stack

```python
# Configuration
FPT_API_BASE = "https://api.fpt.ai/v1"
FPT_API_KEY = os.getenv("FPT_API_KEY")

# 1. Vietnamese Embedding (AITeamVN)
embeddings = OpenAIEmbeddings(
    model="Vietnamese_Embedding",
    openai_api_base=FPT_API_BASE,
    openai_api_key=FPT_API_KEY,
    dimensions=1024
)

# 2. GLM-4.5 LLM (Z.ai)
llm = ChatOpenAI(
    model="GLM-4.5",
    openai_api_base=FPT_API_BASE,
    openai_api_key=FPT_API_KEY,
    temperature=0.7
)

# 3. BGE Reranker v2-m3 (BAAI) - via REST API
reranker_response = requests.post(
    f"{FPT_API_BASE}/rerank",
    headers={"Authorization": f"Bearer {FPT_API_KEY}"},
    json={
        "model": "bge-reranker-v2-m3",
        "query": query,
        "documents": documents
    }
)

# 4. Llama Guard 3-8B (Meta)
guard = ChatOpenAI(
    model="Llama-Guard-3-8B",
    openai_api_base=FPT_API_BASE,
    openai_api_key=FPT_API_KEY,
    temperature=0
)
```

### Why This Stack?

| Benefit | Description |
|---------|-------------|
| **Vietnamese Optimized** | All models support Vietnamese language natively |
| **Low Latency** | FPT Cloud servers in Vietnam reduce network delay |
| **Cost Effective** | Competitive pricing compared to international providers |
| **Single Platform** | One API key for all AI capabilities |
| **LangChain Compatible** | Easy integration via OpenAI-compatible interface |
| **Local Support** | Vietnamese documentation and customer service |

### Getting Started with FPT Cloud

1. **Register**: Visit https://marketplace.fptcloud.com
2. **Get Credits**: New users receive $1 free credit
3. **Create API Key**: Navigate to My Account → API Keys
4. **Select Models**: Enable the 4 models used in this system
5. **Copy Key**: Use in `.env` file as `FPT_API_KEY`

### Model Usage Tips

**Embedding Model:**
- Use for Vietnamese text (best performance)
- Max 512 tokens per input
- Returns 1024-dim vectors

**Reranker Model:**
- Use after initial retrieval (20 → 5 docs)
- Improves top-K accuracy by 5-15%
- ~100-200ms additional latency

**LLM Model:**
- GLM-4.5 supports 128K context window
- Good for Vietnamese + English + Chinese
- Stream responses for better UX

**Guard Model:**
- Check inputs AND outputs for safety
- Customizable safety categories
- ~200-500ms per check

### API Rate Limits (FPT Cloud)

Check current limits at: https://marketplace.fptcloud.com/pricing

Typical limits:
- Embedding: 1000 requests/min
- LLM: 60 requests/min
- Reranker: 500 requests/min
- Guard: 100 requests/min

---

## Additional Resources

### Design System & UI
- [Ant Design](https://ant.design/)
- [Ant Design Components](https://ant.design/components/overview/)
- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Vite Guide](https://vitejs.dev/guide/)

### AI & ML
- [FPT AI Marketplace](https://marketplace.fptcloud.com)
- [FPT Cloud Documentation](https://fptcloud.com/en)
- [LangChain OpenAI Integration](https://python.langchain.com/docs/integrations/platforms/openai)

### Infrastructure
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Charts](https://helm.sh/docs/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Redis Documentation](https://redis.io/docs/)

### Backend
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)
