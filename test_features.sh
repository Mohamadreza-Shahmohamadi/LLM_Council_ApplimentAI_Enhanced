#!/bin/bash
# Quick test script for new features

echo "=== Testing LLM Council Enhanced Features ==="
echo

# Check Python imports
echo "✓ Testing imports..."
cd /Users/mreza/Documents/My-Projects/LLM-Coucil/LLM_Council_ApplimentAI
python3 -c "
from backend.classification import classify_message
from backend.connectivity import robust_client, RobustHTTPClient, CircuitBreaker
from backend.multi_round import run_multi_round
from backend.config import get_classification_config, get_strategy_config
from backend import documents, tools, storage
print('✅ All imports successful')
"

if [ $? -eq 0 ]; then
    echo "✅ All module imports work!"
else
    echo "❌ Import errors detected"
    exit 1
fi

echo
echo "✓ Checking configuration..."
python3 -c "
from backend.config import get_classification_config, get_strategy_config, get_tool_config, get_document_config, get_database_config
print('Classification config:', get_classification_config())
print('Strategy config:', get_strategy_config())
print('Tool config:', get_tool_config())
print('Document config:', get_document_config())
print('Database config:', get_database_config())
"

echo
echo "=== All Core Tests Passed ===" echo "Next steps:"
echo "1. Set API keys in .env"
echo "2. Run: ./start.sh"
echo "3. Test Stage 0: Ask 'What is 2+2?'"
echo "4. Test Multi-round: Set DEFAULT_STRATEGY=multi_round, ask complex question"
echo "5. Monitor /api/health for connectivity status"
