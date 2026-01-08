# Oracle Cloud Manual Setup Guide

## 🔥 QUICK START (5 Minutes)

### Step 1: Create Oracle Account
1. **Go to**: https://www.oracle.com/cloud/free/
2. **Sign up** with email (no credit card needed for Always Free)
3. **Verify** email and complete setup

### Step 2: Create OKE Cluster
1. **Login** to Oracle Cloud Console
2. **Navigate**: ☰ Menu → Developer Services → Kubernetes Clusters (OKE)
3. **Click**: "Create Cluster"
4. **Choose**: "Quick Create" 
5. **Select**: 
   - Name: `todo-app-cluster`
   - Shape: `VM.Standard.A1.Flex` (Always Free)
   - OCPUs: 1-4 (Always Free limit)
   - Memory: 6-24 GB
6. **Click**: "Create Cluster"
7. **Wait**: 10-15 minutes for creation

### Step 3: Get Cluster Access
1. **Go to**: Your cluster details page
2. **Click**: "Access Cluster" 
3. **Copy**: The `oci ce cluster create-kubeconfig` command
4. **Run**: The command in your terminal

### Step 4: Deploy Todo App
```bash
# Run our deployment script
./scripts/deploy-oracle.sh
```

## 📋 What You Need
- Oracle Cloud account (free)
- OCI CLI installed
- kubectl installed  
- Cluster OCID (from console)
- Tenancy OCID (from console)

## 💰 Cost
**$0** - Everything uses Always Free tier:
- 4 OCPUs ARM Ampere A1
- 24 GB Memory
- 200 GB Storage
- Load Balancer
- Container Registry

## 🎯 Expected Result
After deployment:
- Frontend: `http://<load-balancer-ip>:3000`
- Backend API: `http://<load-balancer-ip>:8000`
- All microservices running
- Monitoring dashboard available

## 🚨 Common Issues
1. **"Insufficient capacity"**: Try different availability domain
2. **"Service limit exceeded"**: Use Always Free shapes only
3. **"Authentication failed"**: Check OCI CLI config

Ready to start? Create Oracle account first! 🚀