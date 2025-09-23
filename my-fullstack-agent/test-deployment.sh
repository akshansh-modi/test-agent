#!/bin/bash

# Test script for the deployed financial advisor service

if [ -z "$1" ]; then
    echo "❌ Error: Please provide the service URL"
    echo "Usage: ./test-deployment.sh <SERVICE_URL>"
    echo "Example: ./test-deployment.sh https://my-fullstack-agent-123456789.us-central1.run.app"
    exit 1
fi

SERVICE_URL="$1"

echo "🧪 Testing deployed service at: ${SERVICE_URL}"
echo ""

# Test 1: Health check (if exists)
echo "1️⃣ Testing basic connectivity..."
if curl -s "${SERVICE_URL}" > /dev/null; then
    echo "✅ Service is reachable"
else
    echo "❌ Service is not reachable"
    exit 1
fi

# Test 2: Test /extract_financial_output endpoint
echo ""
echo "2️⃣ Testing /extract_financial_output endpoint..."
curl -X POST "${SERVICE_URL}/extract_financial_output" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the current market outlook?"}' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | head -20

echo ""
echo "3️⃣ Testing /run_with_extraction endpoint..."
curl -X POST "${SERVICE_URL}/run_with_extraction" \
  -H "Content-Type: application/json" \
  -d '{"query": "Analyze AAPL stock"}' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | head -20

echo ""
echo "4️⃣ Testing /extract_all_outputs endpoint..."
curl -X POST "${SERVICE_URL}/extract_all_outputs" \
  -H "Content-Type: application/json" \
  -d '{"query": "Market summary for tech stocks"}' \
  -w "\nHTTP Status: %{http_code}\n" \
  -s | head -20

echo ""
echo "✅ Testing complete!"