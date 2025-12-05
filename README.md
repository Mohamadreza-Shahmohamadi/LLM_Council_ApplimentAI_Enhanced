---
title: LLM Council
emoji: 🏛️
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# LLM Council - AI Deliberation Platform

Multiple AI models discuss and vote on responses to your questions.

# LLM Council - Enhanced Edition

A consolidated fork combining the best features from multiple community contributions to [karpathy/llm-council](https://github.com/karpathy/llm-council).

## Features

### Core Features (from jacob-bd/llm-council-plus)
- ✅ Multi-provider LLM support (OpenRouter, Groq, OpenAI, Anthropic, Google, Mistral, DeepSeek)
- ✅ Web search integration (DuckDuckGo, Tavily, Brave)
- ✅ Execution modes (Chat Only, Chat+Ranking, Full Deliberation)
- ✅ Temperature controls for all 3 stages
- ✅ Council sizing (2-8 members)
- ✅ Advanced settings UI
- ✅ Conversation history with local storage

### Enhanced Features (consolidated from community forks)

#### Stage 0: Message Classification (NEW)
- ✅ **Intelligent Routing**: Automatically classifies queries before deliberation
- ✅ **Direct Answers**: Simple questions get instant responses (saves time & API costs)
- ✅ **Full Deliberation**: Complex questions go through complete council process
- ✅ **Confidence Scoring**: Adjustable threshold for classification confidence
- ✅ **Visual Indicators**: Blue badge for direct answers, green for deliberation

#### Multi-Strategy Deliberation (NEW)
- ✅ **Simple Strategy**: Fast, single-round deliberation (default)
- ✅ **Multi-Round Strategy**: Iterative refinement for complex questions
- ✅ **Auto-Select**: AI recommends best strategy based on query type
- ✅ **Configurable Rounds**: Set number of refinement iterations (default: 2)
- ✅ **Progress Tracking**: See improvement across rounds

#### Robust Connectivity (NEW)
- ✅ **Automatic Retry**: Exponential backoff for failed API calls (3 attempts)
- ✅ **Circuit Breaker**: Temporarily blocks providers after repeated failures
- ✅ **Rate Limit Handling**: Smart backoff when hitting API limits (429 errors)
- ✅ **Error Recovery**: Graceful degradation for network/server issues
- ✅ **Health Monitoring**: Check provider status via `/api/health` endpoint

#### Database Backend (from Reeteshrajesh/llm-council)
- ✅ PostgreSQL support
- ✅ MySQL support
- ✅ JSON storage (default, no setup required)
- ✅ Easy switching via environment variable

#### AI Tools (from Reeteshrajesh/llm-council)
- ✅ Calculator for mathematical computations
- ✅ Wikipedia for knowledge lookup
- ✅ ArXiv for research paper search
- ✅ Yahoo Finance for market data

#### Document Upload (from ianpcook/llm-council)
- ✅ Upload documents for context-aware conversations
- ✅ Support for .txt, .md, .pdf, .docx, .pptx files

## Installation

### Quick Start

```bash
# Clone and enter directory
git clone <repo-url>
cd LLM_Council_ApplimentAI

# Install dependencies
uv sync
cd frontend && npm install && cd ..

# Configure
cp .env.example .env
# Edit .env: Add OPENROUTER_API_KEY=sk-or-...

# Run
./start.sh
```

### Advanced Setup (with PostgreSQL & Tools)

```bash
# Install all dependencies
uv sync

# Configure
cp .env.example .env

# Edit .env and set:
DB_TYPE=postgresql
DATABASE_URL=postgresql://user:pass@localhost/llm_council
ENABLE_TOOLS=true
AVAILABLE_TOOLS=calculator,wikipedia,arxiv,finance

# Run
./start.sh
```

## Configuration

### Environment Variables

```bash
# Required
OPENROUTER_API_KEY=sk-or-...

# Optional - Additional LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
GROQ_API_KEY=gsk_...

# Optional - Database (default: JSON)
DB_TYPE=json  # json | postgresql | mysql
DATABASE_URL=postgresql://...  # if using PostgreSQL/MySQL

# Optional - Tools (enabled by default)
ENABLE_TOOLS=true
AVAILABLE_TOOLS=calculator,wikipedia,arxiv,finance

# Optional - Stage 0 Classification
ENABLE_CLASSIFICATION=true
CLASSIFICATION_CONFIDENCE=0.7

# Optional - Deliberation Strategy
DEFAULT_STRATEGY=simple  # simple | multi_round
MULTI_ROUND_ROUNDS=2

# Optional - Search
TAVILY_API_KEY=tvly-...  # if using Tavily
BRAVE_API_KEY=...  # if using Brave
```

## Architecture

```
LLM_Council_ApplimentAI/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── council.py              # Core council logic
│   ├── providers/              # LLM providers
│   ├── search/                 # Web search
│   ├── storage/                # Database backends
│   │   ├── json_storage.py     # JSON file storage
│   │   ├── sql_storage.py      # PostgreSQL/MySQL
│   │   ├── models.py           # SQLAlchemy models
│   │   └── database.py         # DB connection
│   ├── tools/                  # AI tools
│   │   └── __init__.py         # Calculator, Wikipedia, etc.
│   └── documents/              # Document handling
│       ├── parser.py           # Text extraction
│       └── manager.py          # Document management
├── frontend/                   # React UI
├── data/                       # JSON storage (default)
├── .env.example
├── pyproject.toml
└── README.md
```

## Usage

### Basic Council Conversation

1. Open http://localhost:5173
2. Enter your question: "What are the implications of quantum computing?"
3. Select 4-6 models
4. Choose execution mode: Full Deliberation
5. Watch the council debate!

### Stage 0 Classification (Auto-Routing)

**Enable in .env**: `ENABLE_CLASSIFICATION=true`

```
Simple question: "What is 2+2?"
→ ⚡ Direct Answer (fast, chairman only, ~2-3 seconds)

Complex question: "Compare quantum computing paradigms"
→ 🏛️ Council Deliberation (full process, ~30-60 seconds)
```

Classification runs automatically - no UI changes needed!

### Multi-Round Strategy

**Enable in .env**: `DEFAULT_STRATEGY=multi_round`

```
Round 1: Initial responses from all models
Round 2: Models see peer responses and refine
→ Measurably better answers for complex topics
```

Use for:
- Complex analysis questions
- Topics requiring deep thought
- When quality >> speed

### With Tools Enabled

```bash
# Set in .env
ENABLE_TOOLS=true

# Ask: "Calculate the compound interest on $10,000 at 5% for 10 years"
# Council will use Calculator tool automatically
```

### With Document Upload

1. Upload a document (.pdf, .docx, .txt, etc.)
2. Ask questions about the document
3. Council will reference the uploaded content in responses

## Credits

This enhanced version consolidates features from:

- **Base:** [jacob-bd/llm-council-plus](https://github.com/jacob-bd/llm-council-plus) - Multi-provider support, web search, advanced UI
- **Database & Tools:** [Reeteshrajesh/llm-council](https://github.com/Reeteshrajesh/llm-council) - PostgreSQL/MySQL, AI tools
- **Document Upload:** [ianpcook/llm-council](https://github.com/ianpcook/llm-council) - File context injection
- **Original:** [karpathy/llm-council](https://github.com/karpathy/llm-council) - Core concept

## Development

```bash
# Run backend in dev mode
cd backend
uv run uvicorn main:app --reload

# Run frontend in dev mode
cd frontend
npm run dev
```

## Deployment

See [DEPLOY_HF.md](DEPLOY_HF.md) for instructions on deploying to Hugging Face Spaces (Free Tier).

## License

MIT License (consistent with all source forks)

## Maintained by

ApplimentAI - [https://github.com/Mohamadreza-Shahmohamadi/LLM_Council_ApplimentAI_Enhanced](https://github.com/Mohamadreza-Shahmohamadi/LLM_Council_ApplimentAI_Enhanced)
