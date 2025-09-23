#!/bin/bash
set -e

# Phase 2: Redeploy with discovered URL
# This updates server.py to use the actual deployed URL

# Configuration
PROJECT_ID="fluent-radar-471616-n9"
SERVICE_NAME="my-fullstack-agent"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Check if BASE_URL is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide the BASE_URL from Phase 1 deployment"
    echo "Usage: ./deploy-phase2.sh <BASE_URL>"
    echo "Example: ./deploy-phase2.sh https://my-fullstack-agent-123456789.us-central1.run.app"
    exit 1
fi

BASE_URL="$1"
echo "🚀 Phase 2: Redeploying ${SERVICE_NAME} with BASE_URL=${BASE_URL}..."

# Ensure Docker is running
echo "🐳 Checking Docker..."
if ! docker ps >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Create backup of original server.py
echo "💾 Creating backup of server.py..."
cp financial_advisor/server.py financial_advisor/server.py.backup

# Update server.py to use the deployed URL
echo "📝 Updating server.py with BASE_URL=${BASE_URL}..."

# Replace hardcoded localhost URLs with environment variable fallback
sed -i.tmp 's|"http://localhost:8000/run"|f"{os.getenv('"'"'BASE_URL'"'"', '"'"'http://localhost:8000'"'"')}/run"|g' financial_advisor/server.py
sed -i.tmp 's|base_url = os.getenv("BASE_URL", "http://localhost:8000")|base_url = os.getenv("BASE_URL", "'"${BASE_URL}"'")|g' financial_advisor/server.py

# Clean up temporary files
rm -f financial_advisor/server.py.tmp

echo "✅ Updated server.py to use BASE_URL environment variable"

# Build new image
echo "📦 Building updated Docker image..."
docker build --platform linux/amd64 -t ${IMAGE_NAME} .

# Push updated image
echo "⬆️ Pushing updated image to Container Registry..."
docker push ${IMAGE_NAME}

# Deploy with BASE_URL environment variable
echo "🌐 Deploying to Cloud Run (Phase 2)..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --set-env-vars BASE_URL=${BASE_URL} \
  --memory 2Gi \
  --timeout 3600 \
  --cpu 2 \
  --max-instances 10

# Get the final URL (should be the same)
FINAL_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format="value(status.url)")

echo "✅ Phase 2 deployment complete!"
echo "🔗 Final Service URL: ${FINAL_URL}"
echo "🔧 BASE_URL environment variable set to: ${BASE_URL}"
echo ""
echo "🧪 Test the service:"
echo "   curl -X POST ${FINAL_URL}/extract_financial_output \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"query\": \"test\"}'"

# Restore original server.py for development
echo "🔄 Restoring original server.py for local development..."
mv financial_advisor/server.py.backup financial_advisor/server.py

echo "📝 Note: server.py has been restored to original state for local development"
echo "The deployed version uses BASE_URL=${BASE_URL} via environment variable"