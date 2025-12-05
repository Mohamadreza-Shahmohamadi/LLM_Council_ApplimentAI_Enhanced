# TEST_PLAN.md

## Core Functionality Tests

### Test 1: Basic Council (jacob-bd base)
- [ ] Start backend and frontend
- [ ] Select 3 models from OpenRouter
- [ ] Run Chat Only mode
- [ ] Verify 3 responses appear
- [ ] Run Full Deliberation mode
- [ ] Verify all 3 stages complete
- [ ] Check final consolidated response

### Test 2: Multi-Provider Support (jacob-bd)
- [ ] Test OpenRouter API
- [ ] Test Groq API (if key provided)
- [ ] Test direct OpenAI API (if key provided)
- [ ] Verify all providers work
- [ ] Check error handling for missing keys

### Test 3: Web Search (jacob-bd)
- [ ] Enable web search
- [ ] Ask time-sensitive question
- [ ] Verify search results appear in context
- [ ] Test DuckDuckGo (default)
- [ ] Test Tavily (if key provided)

### Test 4: Database Backend (Reeteshrajesh) - IF INTEGRATED
- [ ] Test JSON storage (default)
- [ ] Switch to PostgreSQL
- [ ] Verify conversation saves to DB
- [ ] Switch to MySQL
- [ ] Verify conversation saves to DB
- [ ] Test conversation retrieval
- [ ] Test conversation deletion

### Test 5: AI Tools (Reeteshrajesh) - IF INTEGRATED
- [ ] Enable tools
- [ ] Test Calculator: "What is 1234 * 5678?"
- [ ] Test Wikipedia: "Who is Alan Turing?"
- [ ] Test ArXiv: "Papers on transformer architecture"
- [ ] Test Yahoo Finance: "What is Apple's stock price?"
- [ ] Verify tools activate automatically
- [ ] Check tool results appear in council discussion

### Test 6: Document Upload (ianpcook) - IF INTEGRATED
- [ ] Upload .txt file
- [ ] Verify content injected into context
- [ ] Ask question about document
- [ ] Verify council references document
- [ ] Test .pdf upload
- [ ] Test .md upload

## Integration Tests

### Test 7: Combined Features
- [ ] Enable database + tools + search
- [ ] Upload document
- [ ] Ask complex question requiring tools and search
- [ ] Verify all features work together
- [ ] Check no conflicts between features

## Performance Tests

### Test 8: Load & Responsiveness
- [ ] Create 50+ conversations
- [ ] Check UI remains responsive
- [ ] Test database query performance
- [ ] Check memory usage
- [ ] Test with 8 council members (max)

## Error Handling Tests

### Test 9: Failure Scenarios
- [ ] Invalid API key
- [ ] Database connection failure
- [ ] Rate limit exceeded
- [ ] Tool execution failure
- [ ] Search API timeout
- [ ] Verify graceful degradation

## Regression Tests

### Test 10: Original Features Still Work
- [ ] Basic 3-stage process (original Karpathy)
- [ ] Temperature controls (jacob-bd)
- [ ] Settings persistence (jacob-bd)
- [ ] Conversation history (jacob-bd)
