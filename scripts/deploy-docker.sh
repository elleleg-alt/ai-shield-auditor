#!/bin/bash
# Deploy using Docker
# Supports local deployment and cloud registries

set -e

echo "🐳 Docker Deployment Script"
echo "============================"

# Configuration
APP_NAME="ai-shield-auditor"
VERSION=${VERSION:-"latest"}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Install from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Menu
echo ""
echo "Select deployment option:"
echo "1) Build and run locally"
echo "2) Build and push to Docker Hub"
echo "3) Build and push to AWS ECR"
echo "4) Build and push to Google Container Registry"
echo "5) Run with docker-compose"
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo "🔨 Building Docker image..."
        docker build -t $APP_NAME:$VERSION .

        echo "🚀 Starting container..."
        docker run -d \
            --name $APP_NAME \
            -p 8501:8501 \
            -e OPENAI_API_KEY="${OPENAI_API_KEY}" \
            -e ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" \
            -e LLM_PROVIDER="${LLM_PROVIDER:-none}" \
            -v $(pwd)/reports:/app/reports \
            $APP_NAME:$VERSION

        echo "✅ Container started!"
        echo "Access at: http://localhost:8501"
        echo ""
        echo "Useful commands:"
        echo "  docker logs -f $APP_NAME     # View logs"
        echo "  docker stop $APP_NAME        # Stop container"
        echo "  docker rm $APP_NAME          # Remove container"
        ;;

    2)
        read -p "Docker Hub username: " DOCKER_USER
        read -p "Image name [$APP_NAME]: " IMAGE_NAME
        IMAGE_NAME=${IMAGE_NAME:-$APP_NAME}

        echo "🔨 Building image..."
        docker build -t $DOCKER_USER/$IMAGE_NAME:$VERSION .

        echo "📤 Pushing to Docker Hub..."
        docker login
        docker push $DOCKER_USER/$IMAGE_NAME:$VERSION

        echo "✅ Pushed to Docker Hub!"
        echo "Pull with: docker pull $DOCKER_USER/$IMAGE_NAME:$VERSION"
        ;;

    3)
        read -p "AWS Account ID: " AWS_ACCOUNT_ID
        read -p "AWS Region [us-east-1]: " AWS_REGION
        AWS_REGION=${AWS_REGION:-us-east-1}

        ECR_REPO="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$APP_NAME"

        echo "🔐 Logging into ECR..."
        aws ecr get-login-password --region $AWS_REGION | \
            docker login --username AWS --password-stdin $ECR_REPO

        echo "📦 Creating repository (if not exists)..."
        aws ecr create-repository --repository-name $APP_NAME --region $AWS_REGION 2>/dev/null || true

        echo "🔨 Building image..."
        docker build -t $APP_NAME:$VERSION .
        docker tag $APP_NAME:$VERSION $ECR_REPO:$VERSION

        echo "📤 Pushing to ECR..."
        docker push $ECR_REPO:$VERSION

        echo "✅ Pushed to ECR!"
        echo "Image URI: $ECR_REPO:$VERSION"
        ;;

    4)
        read -p "GCP Project ID: " GCP_PROJECT
        read -p "GCP Region [us-central1]: " GCP_REGION
        GCP_REGION=${GCP_REGION:-us-central1}

        GCR_REPO="gcr.io/$GCP_PROJECT/$APP_NAME"

        echo "🔐 Configuring Docker for GCR..."
        gcloud auth configure-docker

        echo "🔨 Building image..."
        docker build -t $APP_NAME:$VERSION .
        docker tag $APP_NAME:$VERSION $GCR_REPO:$VERSION

        echo "📤 Pushing to GCR..."
        docker push $GCR_REPO:$VERSION

        echo "✅ Pushed to GCR!"
        echo "Image URI: $GCR_REPO:$VERSION"

        echo ""
        read -p "Deploy to Cloud Run? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            gcloud run deploy $APP_NAME \
                --image $GCR_REPO:$VERSION \
                --platform managed \
                --region $GCP_REGION \
                --allow-unauthenticated \
                --memory 2Gi \
                --cpu 2
        fi
        ;;

    5)
        echo "🐳 Starting with docker-compose..."

        if [ ! -f .env ]; then
            echo "⚠️  No .env file found, creating from example..."
            cp .env.example .env
            echo "📝 Please edit .env with your API keys"
            exit 1
        fi

        docker-compose up -d

        echo "✅ Services started!"
        echo "Access at: http://localhost:8501"
        echo ""
        echo "Useful commands:"
        echo "  docker-compose logs -f       # View logs"
        echo "  docker-compose ps            # List services"
        echo "  docker-compose down          # Stop services"
        ;;

    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac
