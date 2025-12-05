# Changelog

## [2.1.0] - 2025-12-05

### Added
- [Tools] Tool execution integrated into Stage 1 (`run_tools_for_query()`)
- [Classification] Two-tier classification: fast heuristic + LLM fallback
- [Personalities] 5 seed expert personas (Systems Architect, Value Investor, etc.)
- [Personalities] REST API for CRUD operations
- [Query Classifier] Rule-based query categorization

### Changed
- Tools enabled by default (`ENABLE_TOOLS=true`)
- Docs moved to `/docs` folder for cleaner root

---

## [2.0.0-consolidated] - 2025-12-05

### Base
- Forked from jacob-bd/llm-council-plus
- Multi-provider LLM support (9 providers)
- Web search integration (DuckDuckGo, Tavily, Brave)
- Execution modes, temperature controls, council sizing

### Added
- [Database] PostgreSQL/MySQL support (from Reeteshrajesh)
- [Tools] Calculator, Wikipedia, ArXiv, Yahoo Finance
- [Documents] File upload (.txt, .md, .pdf, .docx)
- [Core] Stage 0 Classification, Multi-Round Strategy, Retry Logic

### Removed
- Local LLM support (Ollama, LM Studio)

