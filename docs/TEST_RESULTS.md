# Test Results

**Date:** 2025-12-05
**Version:** 2.0.0-consolidated

## Automated Testing

Run via `test_consolidated.sh`.

| Test Case | Status | Notes |
|-----------|--------|-------|
| **1. Backend Startup** | ✅ PASS | Imports `backend.main` successfully. |
| **2. Configuration** | ✅ PASS | Loads `config.py` and defaults to JSON storage. |
| **3. Database Module** | ✅ PASS | `create_conversation` works in JSON mode. |
| **4. Tools Module** | ✅ PASS | `calculator_tool` loads correctly. |
| **5. Frontend Build** | ✅ PASS | Vite build completes successfully. |

## Manual Verification Required

The following features require manual testing in the browser:
1.  **API Integration**: Verify that actual calls to OpenRouter/OpenAI work with valid keys.
2.  **UI Interaction**:
    -   Check that the Settings page saves correctly.
    -   Verify the "Chat", "Chat + Ranking", and "Full Deliberation" modes.
3.  **Database Switching**:
    -   If using Postgres/MySQL, verify data persistence.
4.  **Tool Execution**:
    -   Ask a math question to trigger the Calculator.
    -   Ask a stock price question to trigger Yahoo Finance.

## Known Issues / Notes
-   **Search Dependency**: `duckduckgo_search` package name was fixed in `backend/search.py`.
-   **Frontend Dependencies**: `npm install` is required before the first build (handled in setup).
