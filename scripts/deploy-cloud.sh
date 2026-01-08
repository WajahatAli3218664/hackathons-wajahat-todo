#!/bin/bash

# Cloud Deployment Script for Todo App Phase V
set -e

echo "🚀 Starting Todo App Cloud Deployment..."

# Configuration
NAMESPACE="todo-app"
REGISTRY="${OCI_REGION}.ocir.io"
TENANCY="${OCI_TENANCY}"
IMAGE_TAG="${GITHUB_SHA:-latest}"

echo "📋 Configuration:"
echo "  Namespace: $NAMESPACE"
echo "  Registry: $REGISTRY"
echo "  Image Tag: $IMAGE_TAG"

# Create namespace
echo "📦 Creating namespace..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Deploy monitoring stack
echo "📊 Deploying monitoring..."
kubectl apply -f k8s/manifests/monitoring.yaml

# Deploy main application
echo "🎯 Deploying Todo App..."
helm upgrade --install todo-app k8s/helm/todo-app/ \
  --namespace $NAMESPACE \
  --set backend.image.repository=$REGISTRY/$TENANCY/todo-backend \
  --set backend.image.tag=$IMAGE_TAG \
  --set frontend.image.repository=$REGISTRY/$TENANCY/todo-frontend \
  --set frontend.image.tag=$IMAGE_TAG \
  --wait --timeout=600s

# Deploy microservices
echo "🔧 Deploying microservices..."
kubectl apply -f k8s/manifests/microservices.yaml

echo "✅ Deployment completed successfully!"