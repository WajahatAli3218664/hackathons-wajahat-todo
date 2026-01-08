# AI DevOps Commands for Todo App

## Docker AI (Gordon) Commands

### Basic Gordon Usage
```bash
# Check Gordon capabilities
docker ai "What can you do?"

# Build images with AI assistance
docker ai "Build a production-ready image for my FastAPI backend"
docker ai "Create an optimized Next.js frontend container"

# Container management
docker ai "Show me running containers and their resource usage"
docker ai "Help me debug why my container is failing"
docker ai "Optimize my Docker image size"

# Security scanning
docker ai "Scan my images for vulnerabilities"
docker ai "Check for security best practices in my Dockerfile"
```

### Specific Todo App Commands
```bash
# Build backend
docker ai "Build backend image from k8s/docker/backend/Dockerfile with tag todo-backend:latest"

# Build frontend
docker ai "Build frontend image from k8s/docker/frontend/Dockerfile with tag todo-frontend:latest"

# Test containers
docker ai "Run todo-backend container with environment variables for testing"
docker ai "Check health of todo-frontend container"
```

## kubectl-ai Commands

### Deployment Management
```bash
# Deploy applications
kubectl-ai "deploy the todo frontend with 2 replicas"
kubectl-ai "deploy the todo backend with health checks"

# Scaling operations
kubectl-ai "scale the backend to handle more load"
kubectl-ai "scale frontend deployment to 3 replicas"

# Service management
kubectl-ai "create a service for the frontend deployment"
kubectl-ai "expose backend deployment on port 8000"
```

### Troubleshooting
```bash
# Debug issues
kubectl-ai "check why the pods are failing"
kubectl-ai "show me logs for failed backend pods"
kubectl-ai "diagnose networking issues between frontend and backend"

# Resource monitoring
kubectl-ai "show resource usage for todo-app namespace"
kubectl-ai "check if pods have enough memory"
kubectl-ai "find pods that are consuming too much CPU"
```

### Configuration Management
```bash
# ConfigMaps and Secrets
kubectl-ai "create configmap for todo app environment variables"
kubectl-ai "create secret for database credentials"
kubectl-ai "update configmap with new API endpoint"

# Ingress and networking
kubectl-ai "create ingress for todo app with SSL"
kubectl-ai "configure load balancer for frontend service"
```

## kagent Commands

### Cluster Analysis
```bash
# Health monitoring
kagent "analyze the cluster health"
kagent "check for any security vulnerabilities in the cluster"
kagent "identify performance bottlenecks"

# Resource optimization
kagent "optimize resource allocation for todo-app namespace"
kagent "suggest cost optimization strategies"
kagent "analyze pod resource utilization patterns"
```

### Advanced Operations
```bash
# Capacity planning
kagent "predict resource needs for scaling to 100 users"
kagent "analyze storage requirements for the database"

# Security analysis
kagent "audit security configurations for todo-app"
kagent "check for compliance with security best practices"

# Performance tuning
kagent "optimize network policies for better performance"
kagent "suggest improvements for pod startup times"
```

## Combined Workflow Examples

### Complete Deployment Workflow
```bash
# 1. Build images with Gordon
docker ai "Build optimized images for todo app frontend and backend"

# 2. Deploy with kubectl-ai
kubectl-ai "deploy todo app with 2 replicas each for frontend and backend"

# 3. Monitor with kagent
kagent "analyze the deployment health and suggest optimizations"

# 4. Scale based on analysis
kubectl-ai "scale deployments based on kagent recommendations"
```

### Troubleshooting Workflow
```bash
# 1. Identify issues
kagent "analyze why todo app is responding slowly"

# 2. Debug specific components
kubectl-ai "check backend pod logs for errors"

# 3. Fix container issues
docker ai "help me fix the container startup issues"

# 4. Verify fixes
kagent "confirm that performance issues are resolved"
```

### Security Workflow
```bash
# 1. Scan images
docker ai "scan todo app images for security vulnerabilities"

# 2. Audit cluster
kagent "perform security audit of todo-app namespace"

# 3. Apply fixes
kubectl-ai "apply security patches and update configurations"

# 4. Verify security posture
kagent "verify that security recommendations have been implemented"
```

## Installation Requirements

### Docker AI (Gordon)
- Docker Desktop 4.53+
- Enable in Settings > Beta features

### kubectl-ai
```bash
# Install kubectl-ai
curl -Lo kubectl-ai https://github.com/sozercan/kubectl-ai/releases/latest/download/kubectl-ai-linux-amd64
chmod +x kubectl-ai
sudo mv kubectl-ai /usr/local/bin/
```

### kagent
```bash
# Install kagent
pip install kagent
# or
brew install kagent
```

## Best Practices

1. **Start Simple**: Begin with kubectl-ai for basic operations
2. **Layer Complexity**: Add kagent for advanced analysis
3. **Combine Tools**: Use all three tools together for comprehensive management
4. **Monitor Continuously**: Regular health checks with kagent
5. **Automate Common Tasks**: Create scripts combining AI commands
6. **Learn from AI**: Ask tools to explain their recommendations