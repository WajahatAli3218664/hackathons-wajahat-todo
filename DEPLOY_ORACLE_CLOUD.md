# Quick Oracle Cloud Deployment

## Step 1: Create Oracle Account
1. Go to https://www.oracle.com/cloud/free/
2. Sign up (Always Free - no credit card after trial)
3. Get $300 credits + Always Free resources

## Step 2: Create OKE Cluster
1. Login to Oracle Cloud Console
2. Go to Developer Services → Kubernetes Clusters (OKE)
3. Create Cluster → Quick Create
4. Choose "Always Free" shape (Ampere A1)
5. Wait 10-15 minutes for cluster creation

## Step 3: Connect kubectl
```bash
# Install OCI CLI
bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"

# Configure OCI CLI (need API key from console)
oci setup config

# Get kubeconfig for your cluster
oci ce cluster create-kubeconfig --cluster-id <your-cluster-ocid> --file ~/.kube/config --region <region>

# Test connection
kubectl get nodes
```

## Step 4: Deploy Todo App
```bash
# Use our existing deployment
./scripts/deploy-cloud.sh
```

## Always Free Resources (Forever)
- 4 OCPUs ARM Ampere A1
- 24 GB Memory  
- 200 GB Block Storage
- Load Balancer
- Container Registry

**Total Cost: $0 (Always Free)**