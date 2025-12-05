#!/bin/bash
# test_consolidated.sh

echo "🧪 Testing LLM Council Enhanced Edition"

# Test 1: Backend starts
echo "Test 1: Backend startup..."
cd /Users/mreza/Documents/My-Projects/LLM-Coucil/LLM_Council_ApplimentAI
uv run python -c "from backend import main; print('✅ Backend imports OK')" || exit 1

# Test 2: Config loads
echo "Test 2: Configuration..."
uv run python -c "from backend.config import get_database_config; print(f'✅ Config OK: {get_database_config()}')" || exit 1

# Test 3: Database module
echo "Test 3: Database module..."
uv run python -c "from backend.storage.json_storage import create_conversation; print('✅ Storage OK')" || exit 1

# Test 4: Tools (if integrated)
if [ -d "backend/tools" ]; then
    echo "Test 4: Tools module..."
    uv run python -c "from backend.tools import calculator_tool; print('✅ Tools OK')" || exit 1
fi

# Test 5: Frontend builds
echo "Test 5: Frontend build..."
cd frontend
npm run build > /dev/null 2>&1 && echo "✅ Frontend OK" || exit 1

echo ""
echo "✅ All automated tests passed!"
echo "Manual testing required for:"
echo "  - API integrations"
echo "  - UI functionality"
echo "  - Multi-provider features"
