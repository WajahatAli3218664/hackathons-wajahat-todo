#!/bin/bash

# Production-Ready Local Deployment
echo "🚀 Setting up Production-Ready Local Environment"

# Enable Minikube addons for production features
echo "📦 Enabling production addons..."
minikube addons enable ingress
minikube addons enable metrics-server
minikube addons enable dashboard

# Deploy monitoring stack
echo "📊 Deploying monitoring..."
kubectl apply -f k8s/manifests/monitoring.yaml

# Deploy Kafka
echo "☕ Deploying Kafka..."
kubectl apply -f k8s/manifests/kafka.yaml

# Wait for Kafka
echo "⏳ Waiting for Kafka..."
kubectl wait --for=condition=ready pod -l app=kafka -n kafka --timeout=300s

# Deploy microservices
echo "🔧 Deploying microservices..."
kubectl apply -f k8s/manifests/microservices.yaml

# Get URLs
echo "🌐 Production URLs:"
echo "Frontend: http://$(minikube ip):$(kubectl get service frontend-service -n todo-app -o jsonpath='{.spec.ports[0].nodePort}')"
echo "Backend: http://$(minikube ip):$(kubectl get service backend-service -n todo-app -o jsonpath='{.spec.ports[0].nodePort}')"
echo "Grafana: http://$(minikube ip):$(kubectl get service grafana -n monitoring -o jsonpath='{.spec.ports[0].nodePort}')"

echo "✅ Production-ready local deployment complete!"