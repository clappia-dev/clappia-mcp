#!/bin/bash

# Minimal Google Cloud Project Setup for Clappia MCP Server

set -e

echo "🚀 Minimal Google Cloud Project Setup"
echo "====================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Please login: gcloud auth login"
    exit 1
fi

# Get project details
read -p "Enter project ID: " PROJECT_ID
read -p "Enter project name: " PROJECT_NAME

# Create project
echo "Creating project..."
gcloud projects create $PROJECT_ID --name="$PROJECT_NAME"
gcloud config set project $PROJECT_ID

# Enable APIs
echo "Enabling APIs..."
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

# Create repository
echo "Creating repository..."
gcloud artifacts repositories create clappia-mcp-servers \
    --repository-format=docker \
    --location=us-central1

echo "✅ Setup complete!"
echo "Project ID: $PROJECT_ID"
echo ""
echo "Next steps:"
echo "1. Set billing: gcloud billing accounts list"
echo "2. Deploy: ./deploy-cloud-run.sh"
