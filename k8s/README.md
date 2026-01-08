# Phase IV: Kubernetes Deployment Guide

## Prerequisites

### Required Software
- Docker Desktop 4.53+ (for Gordon AI)
- Minikube
- kubectl
- Helm 3.x
- kubectl-ai
- kagent

### Installation Commands
```bash
# Install Minikube (Linux)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install kubectl-ai
curl -Lo kubectl-ai https://github.com/sozercan/kubectl-ai/releases/latest/download/kubectl-ai-linux-amd64
chmod +x kubectl-ai && sudo mv kubectl-ai /usr/local/bin/

# Install kagent
pip install kagent
```

## Quick Start

### 1. Setup Environment
```bash
# Make scripts executable
chmod +x k8s/scripts/*.sh

# Setup Minikube
./k8s/scripts/setup-minikube.sh
```

### 2. Configure Secrets
Edit the base64 encoded values in `k8s/helm/todo-app/values.yaml`:
```bash
# Encode your actual values
echo -n "your-database-url" | base64
echo -n "your-auth-secret" | base64
echo -n "your-openai-api-key" | base64
```

### 3. Deploy Application
```bash
# Deploy using Helm
./k8s/scripts/deploy.sh
```

### 4. Access Application
```bash
# Get frontend URL
minikube service todo-app-frontend -n todo-app --url

# Access via browser
open $(minikube service todo-app-frontend -n todo-app --url)
```

## Manual Deployment Steps

### 1. Build Docker Images
```bash
# Set Minikube Docker environment
eval $(minikube docker-env)

# Build backend
docker build -f k8s/docker/backend/Dockerfile -t todo-backend:latest .

# Build frontend
docker build -f k8s/docker/frontend/Dockerfile -t todo-frontend:latest .
```

### 2. Deploy with Kubernetes Manifests
```bash
# Apply all manifests
kubectl apply -f k8s/manifests/

# Check deployment status
kubectl get pods -n todo-app
kubectl get services -n todo-app
```

### 3. Deploy with Helm
```bash
# Install/upgrade with Helm
helm upgrade --install todo-app ./k8s/helm/todo-app \
    --namespace todo-app \
    --create-namespace
```

## AI-Assisted Operations

### Using Gordon (Docker AI)
```bash
# Enable Gordon in Docker Desktop Settings > Beta features

# Build with AI assistance
docker ai "Build production images for my todo app"

# Optimize containers
docker ai "Help me reduce image sizes and improve security"
```

### Using kubectl-ai
```bash
# Deploy with AI
kubectl-ai "deploy todo app with high availability"

# Scale based on load
kubectl-ai "scale backend to handle 1000 concurrent users"

# Troubleshoot issues
kubectl-ai "why are my pods crashing?"
```

### Using kagent
```bash
# Analyze cluster health
kagent "analyze todo-app namespace performance"

# Optimize resources
kagent "suggest resource optimizations for cost reduction"

# Security audit
kagent "perform security assessment of my deployment"
```

## Monitoring and Troubleshooting

### Health Checks
```bash
# Check pod status
kubectl get pods -n todo-app

# View logs
kubectl logs -f deployment/todo-app-backend -n todo-app
kubectl logs -f deployment/todo-app-frontend -n todo-app

# Check services
kubectl get services -n todo-app
```

### Common Issues

#### Pods Not Starting
```bash
# Check events
kubectl describe pod <pod-name> -n todo-app

# Check resource limits
kubectl top pods -n todo-app
```

#### Image Pull Errors
```bash
# Verify images exist in Minikube
docker images | grep todo

# Rebuild if necessary
eval $(minikube docker-env)
docker build -f k8s/docker/backend/Dockerfile -t todo-backend:latest .
```

#### Service Not Accessible
```bash
# Check service endpoints
kubectl get endpoints -n todo-app

# Port forward for testing
kubectl port-forward service/todo-app-frontend 3000:3000 -n todo-app
```

## Scaling and Performance

### Manual Scaling
```bash
# Scale deployments
kubectl scale deployment todo-app-backend --replicas=3 -n todo-app
kubectl scale deployment todo-app-frontend --replicas=3 -n todo-app
```

### Auto-scaling (Optional)
```bash
# Enable HPA
kubectl autoscale deployment todo-app-backend --cpu-percent=70 --min=2 --max=10 -n todo-app
```

### Resource Monitoring
```bash
# View resource usage
kubectl top pods -n todo-app
kubectl top nodes

# Minikube dashboard
minikube dashboard
```

## Cleanup

### Remove Application
```bash
# Uninstall Helm release
helm uninstall todo-app -n todo-app

# Delete namespace
kubectl delete namespace todo-app
```

### Stop Minikube
```bash
# Stop cluster
minikube stop

# Delete cluster
minikube delete
```

## Production Considerations

### Security
- Use proper secrets management (not base64 in values.yaml)
- Enable RBAC
- Use network policies
- Scan images for vulnerabilities

### Performance
- Set appropriate resource limits
- Use persistent volumes for data
- Configure ingress with SSL
- Enable monitoring and logging

### High Availability
- Use multiple replicas
- Configure pod disruption budgets
- Use node affinity rules
- Set up health checks

## Next Steps

1. **Monitoring**: Add Prometheus and Grafana
2. **Logging**: Implement centralized logging with ELK stack
3. **CI/CD**: Set up automated deployments
4. **Security**: Implement security scanning and policies
5. **Backup**: Configure database backups
6. **SSL**: Add TLS certificates for production