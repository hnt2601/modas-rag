We just implemented the feature described in the attached plan.

Please do a thorough code review for the RAG System:

## Architecture Context
Review the code against our tech stack:
- **Frontend**: React 18+ with TypeScript, Ant Design 5.x
- **Backend**: FastAPI with Python 3.10+
- **Vector DB**: Qdrant
- **AI Models**: FPT Cloud (Vietnamese_Embedding, GLM-4.5, bge-reranker-v2-m3, Llama-Guard-3-8B)
- **Deployment**: Kubernetes with StatefulSets, ConfigMaps, Secrets

## Review Checklist

1. **Plan Implementation**
   - Verify the plan was correctly implemented
   - Check all specified files were modified
   - Ensure all phases/steps are complete

2. **Bugs & Issues**
   - Look for obvious bugs or logic errors
   - Check error handling and edge cases
   - Verify async/await usage in Python
   - Check Promise handling in TypeScript/React

3. **Data Alignment Issues**
   - Frontend/Backend contract: Check API request/response shapes
   - Pydantic models match TypeScript types
   - Snake_case (Python) vs camelCase (TypeScript) conversions
   - Qdrant metadata structure consistency
   - Environment variables in ConfigMaps match code expectations

4. **Architecture Compliance**
   - Frontend: Uses Ant Design components (not custom UI)
   - Backend: Follows FastAPI router patterns
   - AI calls: Use LangChain OpenAI-compatible classes with FPT Cloud
   - K8s: Proper labels, health checks, resource limits
   - Follow existing project structure (see architecture.md)

5. **Code Quality**
   - No over-engineering or premature abstractions
   - Files not too large (split if >500 lines)
   - Consistent style with existing codebase
   - Proper TypeScript types (no `any`)
   - Python type hints on public functions

6. **Production Readiness**
   - Kubernetes manifests have resource requests/limits
   - Health checks and readiness probes configured
   - Secrets not hardcoded (use ConfigMap/Secrets)
   - Error messages user-friendly in Vietnamese
   - Loading states and error boundaries in React

7. **Security**
   - FPT_API_KEY stored in Secrets, not ConfigMap
   - Input validation on user queries
   - File upload size limits enforced
   - CORS configured correctly

Document your findings in `docs/features/<N>_REVIEW.md` unless a different file name is specified.