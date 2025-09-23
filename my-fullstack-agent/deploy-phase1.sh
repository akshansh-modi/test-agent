#!/bin/bash
set -e

# Phase 1: Initial Deployment (before we know the URL)
# This deploys with hardcoded localhost URLs in server.py

# Configuration
PROJECT_ID="fluent-radar-471616-n9"
SERVICE_NAME="my-fullstack-agent"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Phase 1: Initial deployment for ${SERVICE_NAME}..."

# Ensure Docker is running
echo "🐳 Checking Docker..."
if ! docker ps >/dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Build
echo "📦 Building Docker image..."
docker build --platform linux/amd64 -t ${IMAGE_NAME} .

# Push
echo "⬆️ Pushing to Container Registry..."
docker push ${IMAGE_NAME}

# Deploy with initial configuration
echo "🌐 Deploying to Cloud Run (Phase 1)..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 2Gi \
  --timeout 3600 \
  --cpu 2 \
  --max-instances 10

# Get the deployed URL
DEPLOYED_URL=$(gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format="value(status.url)")

echo "✅ Phase 1 deployment complete!"
echo "🔗 Service URL: ${DEPLOYED_URL}"
echo ""
echo "📝 IMPORTANT: Save this URL for Phase 2 deployment:"
echo "   BASE_URL=${DEPLOYED_URL}"
echo ""
echo "🔄 Next Steps:"
echo "   1. Test the service at: ${DEPLOYED_URL}"
echo "   2. Run deploy-phase2.sh with the discovered URL"
echo "   3. This will update server.py to use the correct BASE_URL"