# Kubernetes Custom Domain Setup

## Step 1: Install Docker Desktop
1. Download: https://www.docker.com/products/docker-desktop
2. Install and restart computer
3. Start Docker Desktop

## Step 2: Start Minikube with Ingress
```bash
minikube start --driver=docker
minikube addons enable ingress
```

## Step 3: Create Custom Domain Ingress
```yaml
# k8s/manifests/custom-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-app-ingress
  namespace: todo-app
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: todo-frontend.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 3000
  - host: todo-backend.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
```

## Step 4: Update Windows Hosts File
```bash
# Add to C:\Windows\System32\drivers\etc\hosts
192.168.49.2 todo-frontend.local
192.168.49.2 todo-backend.local
```

## Step 5: Deploy
```bash
kubectl apply -f k8s/manifests/custom-ingress.yaml
```

## Result URLs:
- Frontend: http://todo-frontend.local
- Backend: http://todo-backend.local