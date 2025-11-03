You are the developer who implemented a new feature for the RAG System that has its plan and review notes attached. You also have access to the newly implemented code. Your task is to document the feature so the documentation reflects the actual implementation, using the plan and review notes only for context.

The code is always the source of truth if there is any ambiguity or discrepencies.

## Documentation Areas to Update

1. **Primary Entry-Point Documentation (README.md)**
   - Brief high-level overview of the feature
   - User-facing instructions in Vietnamese if applicable
   - Link to detailed docs in `/docs`

2. **Code Comments**
   - **Frontend (TypeScript/React)**:
     - JSDoc comments for exported components, hooks, and utilities
     - Prop types should be self-documenting via TypeScript interfaces
     - Inline comments only where logic is non-obvious
   - **Backend (Python/FastAPI)**:
     - Docstrings for all public functions/classes (Google style)
     - Type hints on all function signatures
     - Inline comments for complex RAG pipeline logic
   - **Kubernetes (YAML)**:
     - Comments explaining non-standard configurations
     - Resource limit rationale if unusual

3. **Main Documentation Set (`/docs`)**
   - Update `docs/architecture.md` if new components/flows added
     - Add to relevant sections (UI Layer, Backend, RAG Pipeline, K8s Deployment)
     - Include code examples matching architecture style
     - Update system flow diagrams if applicable
   - Reflect changes, removals, and additions
   - Add clear, minimal examples
   - Show API request/response samples
   - Include Ant Design component usage if new UI patterns

4. **New Documentation Files**
   - Only when the feature is large enough to justify them
   - Place in `/docs` (NOT in `/docs/features` - that's for plans/reviews)
   - Examples: `docs/api.md`, `docs/deployment.md`, `docs/user-guide.md`

## RAG System Documentation Style

Match the existing style in `docs/architecture.md`:

- **Code Examples**: Show both backend (Python) and frontend (TypeScript/React)
- **API Endpoints**: Document request/response with types
- **Ant Design Components**: Show component usage with props
- **FPT Cloud Models**: Document model parameters and use cases
- **Kubernetes**: Show complete YAML manifests with annotations
- **Vietnamese Terms**: Use for user-facing features (e.g., "Tải lên tài liệu")
- **Formatting**: Use tables for specs, code blocks with language tags

## Rules

1. Always match the project's documentation style, format, verbosity and structure (see `docs/architecture.md`).
2. Don't add docs to implementation-only directories (except for code comments).
3. NEVER create new documentation files in the same directory as review or plan documents (`docs/features/` is for historical reference only).
4. Avoid redundancy unless it improves usability.
5. Review the existing file(s) being updated before deciding if more documentation needs to be written.
6. Don't document tests unless the user specifically instructs you to.
7. For architecture.md updates: Add to existing sections rather than creating new ones when possible.
8. Include deployment considerations (ConfigMaps, Secrets, resource requirements) for production features.

## Clarification

Ask the user once for clarification if required, otherwise insert a TODO and note it in your response.

## Output

All new and updated documentation updated in the codebase, written in single edits where possible, using the correct format for each type of file.
