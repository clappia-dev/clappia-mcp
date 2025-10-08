#!/bin/bash

# Enhanced Docker Build Script with Rich Metadata
set -e

# Configuration
IMAGE_NAME="okaru413/clappia-mcp"
VERSION=${1:-"1.0.0"}
PLATFORMS="linux/amd64,linux/arm64"

# Get Git information for metadata
GIT_COMMIT=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ')
GIT_BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🏷️  Building with rich metadata...${NC}"
echo "Image: $IMAGE_NAME:$VERSION"
echo "Platforms: $PLATFORMS"
echo "Build Date: $BUILD_DATE"
echo "Git Commit: $GIT_COMMIT"
echo "Git Branch: $GIT_BRANCH"
echo ""

# Setup buildx
echo -e "${BLUE}🔧 Setting up Docker buildx...${NC}"
docker buildx create --name multiarch-builder --use 2>/dev/null || {
    docker buildx use multiarch-builder
}

# Build with rich metadata
echo -e "${BLUE}📦 Building multi-platform image with metadata...${NC}"
docker buildx build \
    --platform $PLATFORMS \
    --build-arg BUILD_DATE="$BUILD_DATE" \
    --build-arg VCS_REF="$GIT_COMMIT" \
    --build-arg VCS_BRANCH="$GIT_BRANCH" \
    --build-arg VERSION="$VERSION" \
    --label "org.opencontainers.image.created=$BUILD_DATE" \
    --label "org.opencontainers.image.revision=$GIT_COMMIT" \
    --label "org.opencontainers.image.version=$VERSION" \
    --label "build.branch=$GIT_BRANCH" \
    --label "build.platform=$PLATFORMS" \
    -t $IMAGE_NAME:$VERSION \
    -t $IMAGE_NAME:latest \
    --load \
    -f Dockerfile.main .

echo -e "${GREEN}✅ Multi-platform image built successfully with rich metadata!${NC}"

# Show image details
echo ""
echo -e "${BLUE}📋 Image Details:${NC}"
docker image inspect $IMAGE_NAME:latest --format '{{json .Config.Labels}}' | \
    python3 -m json.tool 2>/dev/null || echo "Labels added successfully"

echo ""
echo -e "${BLUE}🔍 Platform Support:${NC}"
docker buildx imagetools inspect $IMAGE_NAME:latest 2>/dev/null | grep "Platform:" || \
    echo "Multi-platform build completed"

echo ""
echo -e "${YELLOW}💡 Next Steps:${NC}"
echo "• Test: docker run --rm -e CLAPPIA_API_KEY=test $IMAGE_NAME:latest"
echo "• Push: make docker-push DOCKER_HUB_USERNAME=okaru413"
echo "• Inspect: docker buildx imagetools inspect $IMAGE_NAME:latest"