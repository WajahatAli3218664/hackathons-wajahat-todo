# Oracle Cloud (OKE) Setup Guide

## Step 1: Create Oracle Cloud Account
1. Go to https://www.oracle.com/cloud/free/
2. Sign up for Always Free account
3. Complete verification (no credit card required after trial)

## Step 2: Create OKE Cluster
```bash
# Install OCI CLI
curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh | bash

# Configure OCI CLI
oci setup config

# Create OKE cluster
oci ce cluster create \
  --compartment-id <compartment-ocid> \
  --name todo-app-cluster \
  --vcn-id <vcn-ocid> \
  --kubernetes-version v1.28.2 \
  --service-lb-subnet-ids '["<subnet-ocid>"]'
```

## Step 3: Configure kubectl
```bash
# Get kubeconfig
oci ce cluster create-kubeconfig \
  --cluster-id <cluster-ocid> \
  --file ~/.kube/config \
  --region <region> \
  --token-version 2.0.0

# Test connection
kubectl get nodes
```

## Always Free Resources
- 4 OCPUs ARM Ampere A1 Compute
- 24 GB Memory
- 200 GB Block Storage
- Load Balancer
- Container Registry