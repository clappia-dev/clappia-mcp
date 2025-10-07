#!/bin/bash

# Clappia MCP Server - Cloud Run Deployment Script
# This script deploys the Clappia MCP server to Google Cloud Run

set -e

# Configuration
PROJECT_ID=${PROJECT_ID:-"your-project-id"}
REGION=${REGION:-"us-central1"}
SERVICE_NAME=${SERVICE_NAME:-"clappia-mcp-server"}
REPOSITORY_NAME=${REPOSITORY_NAME:-"clappia-mcp-servers"}

echo "🚀 Deploying Clappia MCP Server to Cloud Run"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"

# Check if PROJECT_ID is set
if [ "$PROJECT_ID" = "your-project-id" ]; then
    echo "❌ Please set PROJECT_ID environment variable"
    echo "   export PROJECT_ID=your-actual-project-id"
    exit 1
fi

# Set the project
gcloud config set project $PROJECT_ID

# Create Artifact Registry repository if it doesn't exist
echo "📦 Creating Artifact Registry repository..."
gcloud artifacts repositories create $REPOSITORY_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Repository for Clappia MCP servers" \
    --project=$PROJECT_ID \
    2>/dev/null || echo "Repository already exists"

# Build and push the container image using the cloud-specific Dockerfile
echo "🔨 Building and pushing container image..."
gcloud builds submit \
    --region=$REGION \
    --tag $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/$SERVICE_NAME:latest \
    --file=Dockerfile.cloud

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/$SERVICE_NAME:latest \
    --region=$REGION \
    --no-allow-unauthenticated \
    --set-env-vars="PYTHONUNBUFFERED=1" \
    --memory=512Mi \
    --cpu=1 \
    --min-instances=0 \
    --max-instances=10 \
    --timeout=300 \
    --concurrency=100

echo "✅ Deployment complete!"
echo ""
echo "🔐 To access the server, use the Cloud Run proxy:"
echo "   gcloud run services proxy $SERVICE_NAME --region=$REGION"
echo ""
echo "📝 The server will be available at: http://localhost:8080/mcp"
echo "   (when using the proxy)"
echo ""
echo "🔑 Make sure to set CLAPPIA_API_KEY environment variable in Cloud Run:"
echo "   gcloud run services update $SERVICE_NAME --region=$REGION --set-env-vars=CLAPPIA_API_KEY=your-api-key"
