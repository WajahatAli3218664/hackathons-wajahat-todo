#!/bin/bash

# Minikube Setup Script for Todo App
set -e

echo "🚀 Setting up Minikube for Todo App..."

# Check if Minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "❌ Minikube is not installed. Please install it first."
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl is not installed. Please install it first."
    exit 1
fi

# Start Minikube with sufficient resources
echo "🔧 Starting Minikube..."
minikube start --cpus=2 --memory=4096 --disk-size=20g --driver=docker

# Enable required addons
echo "🔧 Enabling Minikube addons..."
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

# Set kubectl context
echo "🔧 Setting kubectl context..."
kubectl config use-context minikube

# Create namespace
echo "🔧 Creating namespace..."
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# Build Docker images in Minikube environment
echo "🐳 Building Docker images..."
eval $(minikube docker-env)

# Build backend image
echo "Building backend image..."
docker build -f k8s/docker/backend/Dockerfile -t todo-backend:latest .

# Build frontend image
echo "Building frontend image..."
docker build -f k8s/docker/frontend/Dockerfile -t todo-frontend:latest .

echo "✅ Minikube setup complete!"
echo "📊 Access dashboard: minikube dashboard"
echo "🌐 Get service URL: minikube service frontend-service -n todo-app --url"