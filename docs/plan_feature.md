The user will provide a feature description for the RAG System. Your job is to:

1. Create a technical plan that concisely describes the feature the user wants to build.
2. Research the files and functions that need to be changed to implement the feature
3. Avoid any product manager style sections (no success criteria, timeline, migration, etc)
4. Avoid writing any actual code in the plan.
5. Include specific and verbatim details from the user's prompt to ensure the plan is accurate.

## Technical Requirements Document Structure

This is strictly a technical requirements document that should:

1. **Context** (brief description at top)
   - What is being built and why
   - Which architecture layer(s) are affected (see `docs/architecture.md`)

2. **Files to Modify/Create**
   - **Frontend** (`frontend/src/`): React components, hooks, services, types
   - **Backend** (`backend/`): FastAPI routers, core logic, models/schemas
   - **Kubernetes** (`k8s/`): Deployments, services, configmaps if needed
   - **Documentation** (`docs/`): Updates to architecture.md or other docs

3. **Technical Details**
   - API contracts (request/response shapes)
   - Data models (Pydantic for backend, TypeScript interfaces for frontend)
   - Qdrant collection schema changes if needed
   - FPT Cloud AI model integration points
   - State management approach (Zustand/TanStack Query)
   - Ant Design components to use

4. **Algorithms/Logic** (if applicable)
   - Step-by-step explanation of complex logic
   - RAG pipeline modifications (retrieval → reranking → generation → guard)

5. **Phasing** (only for REALLY big features)
   - **Phase 1 - Data Layer**: Types, schemas, Qdrant changes, API contracts
   - **Phase 2A - UI**: React components with Ant Design
   - **Phase 2B - Backend**: FastAPI endpoints and core logic
   - **Phase 3 - Deployment**: K8s manifests, ConfigMaps, environment variables

## Architecture Reference

When planning, consider:
- **Frontend**: React 18+ with TypeScript, Ant Design 5.x, TanStack Query, Zustand
- **Backend**: FastAPI, Pydantic models, async/await
- **Vector DB**: Qdrant client, collections, metadata filtering
- **AI Models**: LangChain with FPT Cloud (Vietnamese_Embedding, GLM-4.5, bge-reranker, Llama-Guard)
- **Deployment**: Kubernetes StatefulSets, ConfigMaps, Secrets, HPA
- **Project Structure**: See `docs/architecture.md` Section "Project Structure"

## Clarifying Questions

If the user's requirements are unclear, especially after researching the relevant files, you may ask up to 5 clarifying questions before writing the plan. If you do so, incorporate the user's answers into the plan.

## Output

Prioritize being concise and precise. Make the plan as tight as possible without losing any of the critical details from the user's requirements.

Write the plan into `docs/features/<N>_PLAN.md` file with the next available feature number (starting with 0001)