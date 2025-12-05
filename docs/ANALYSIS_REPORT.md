# ANALYSIS_REPORT.md

## Fork: jacob-bd/llm-council-plus (BASE)
### Key Features:
- **Multi-Provider Support**: Robust integration with OpenRouter, Groq, OpenAI, Anthropic, Google, Mistral, and DeepSeek.
- **Web Search**: Integrated DuckDuckGo search with context injection.
- **Execution Modes**: Chat Only, Chat+Ranking, and Full Deliberation workflows.
- **Architecture**: Clean FastAPI backend + React frontend. Separation of concerns is good.
- **UI**: Polished settings interface for API keys and model selection.

### File Structure:
- Standard FastAPI structure (`backend/main.py`, `backend/council.py`).
- Frontend is a standard Vite/React app.

### Code Quality:
- **High**. Type hinting is used consistently.
- Async patterns are well-implemented for API calls.

---

## Fork: Reeteshrajesh/llm-council
### Features NOT in jacob-bd:
- **Database Backend**: Support for PostgreSQL and MySQL via SQLAlchemy.
- **AI Tools**: Integration of Calculator, Wikipedia, ArXiv, and Yahoo Finance.
- **Memory System**: ChromaDB-based vector memory (Excluded for simplicity).

### Code Extracted:
- `backend/storage/`: Database abstraction and implementations.
- `backend/tools/`: Tool implementations (Calculator, Wikipedia, etc.).

### Features EXCLUDED:
- **Local LLM Integrations**: Removed to keep the project cloud-API focused and lightweight.
- **Memory System**: Excluded to avoid heavy dependencies (ChromaDB) for a hobby project.

---

## Fork: ianpcook/llm-council
### Features NOT in jacob-bd or Reeteshrajesh:
- **Document Upload**: Ability to upload files (.txt, .md, .pdf) and inject them into the context.

### Code Extracted:
- `backend/documents/`: File parsing and context management logic.

---

## Fork: RamaswamyGCP/llm-council
### Unique architectural improvements:
- **LangGraph**: Advanced orchestration.

### Decision:
- **SKIP**. The current `council.py` orchestration in `jacob-bd` is sufficient for the 3-stage process. Migrating to LangGraph would be a major refactor with high complexity and marginal immediate benefit for this specific use case.

---

## Fork: Indubitable-Industries/llm-context-arena
### RAG system analysis:
- **RAG**: Local code indexing.

### Decision:
- **SKIP**. Similar to the memory system, a full RAG pipeline adds significant complexity. The Document Upload feature from `ianpcook` provides a lighter-weight alternative for specific context injection.
