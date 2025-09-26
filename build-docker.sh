#!/bin/bash

# Simple Docker build script
set -e

# Configuration
IMAGE_NAME="okaru413/clappia-mcp"
VERSION=${1:-"1.0.0"}

echo "Building Docker image: $IMAGE_NAME:$VERSION"
docker build -t $IMAGE_NAME:$VERSION .
docker build -t $IMAGE_NAME:latest .

echo "✅ Docker image built successfully"
echo "Use 'make docker-push DOCKER_HUB_USERNAME=yourusername' to push to registry"
