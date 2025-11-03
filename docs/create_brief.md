Please create a product brief based on the description that the user provides. Your goal is to capture the business and functional requirements of the product and to provide solid context for others working on the RAG System.

## Brief Template

Include the following sections:

1. **Project Overview / Description**
   - What problem does this solve in the RAG System?
   - How does it fit into the overall architecture?

2. **Target Audience**
   - Who will use this feature? (End users, admins, developers?)
   - Vietnamese market context if relevant

3. **Primary Benefits / Features**
   - Key capabilities and value proposition
   - How it improves the RAG pipeline or user experience

4. **High-Level Tech/Architecture**
   - Which layer(s) affected: UI (React/Ant Design), Backend (FastAPI), Vector DB (Qdrant), AI Models (FPT Cloud)?
   - Integration points with existing components
   - Any new dependencies or services

5. **Relation to Existing System**
   - Reference relevant sections in `docs/architecture.md`
   - How this extends/modifies current capabilities
   - Example: "Extends RAG Pipeline (Section 4) with new retrieval strategy"

## Style Guidelines

- Keep the brief very concise and to the point
- Use Vietnamese terms for user-facing features
- Reference our tech stack: React + Ant Design, FastAPI, Qdrant, FPT Cloud AI models
- Mention K8s deployment implications if relevant
- Link to architecture.md sections when applicable

Write the document into `docs/PRODUCT_BRIEF.md` (unless a different file name is specified)