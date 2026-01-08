#!/bin/bash

# Deployment Script for Todo App
set -e

echo "🚀 Deploying Todo App to Kubernetes..."

# Check if Helm is installed
if ! command -v helm &> /dev/null; then
    echo "❌ Helm is not installed. Please install it first."
    exit 1
fi

# Set kubectl context to minikube
kubectl config use-context minikube

# Deploy using Helm
echo "📦 Deploying with Helm..."
helm upgrade --install todo-app ./k8s/helm/todo-app \
    --namespace todo-app \
    --create-namespace \
    --wait \
    --timeout=300s

# Wait for deployments to be ready
echo "⏳ Waiting for deployments to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/todo-app-backend -n todo-app
kubectl wait --for=condition=available --timeout=300s deployment/todo-app-frontend -n todo-app

# Get service URLs
echo "🌐 Getting service URLs..."
echo "Frontend URL: $(minikube service todo-app-frontend -n todo-app --url)"
echo "Backend URL: $(minikube service todo-app-backend -n todo-app --url)"

# Show pod status
echo "📊 Pod Status:"
kubectl get pods -n todo-app

echo "✅ Deployment complete!"
echo "🎯 Access your app at: $(minikube service todo-app-frontend -n todo-app --url)"