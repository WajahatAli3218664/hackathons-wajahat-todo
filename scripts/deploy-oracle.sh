#!/bin/bash

# Oracle Cloud OKE Deployment - Step by Step
echo "🚀 Oracle Cloud OKE Deployment Started"

# Step 1: Check prerequisites
echo "📋 Checking prerequisites..."
command -v oci >/dev/null 2>&1 || { 
    echo "❌ OCI CLI not found. Installing..."
    bash -c "$(curl -L https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh)"
}

command -v kubectl >/dev/null 2>&1 || { 
    echo "❌ kubectl required but not installed"; exit 1; 
}

command -v helm >/dev/null 2>&1 || { 
    echo "❌ helm required but not installed"; exit 1; 
}

# Step 2: Configure OCI CLI (if not already done)
if [ ! -f ~/.oci/config ]; then
    echo "🔧 Configuring OCI CLI..."
    echo "Please run: oci setup config"
    echo "You'll need:"
    echo "  - User OCID (from Oracle Cloud Console)"
    echo "  - Tenancy OCID"
    echo "  - Region (e.g., us-ashburn-1)"
    echo "  - API Key (generate from console)"
    exit 1
fi

# Step 3: Set variables (update these)
COMPARTMENT_ID="ocid1.compartment.oc1..your-compartment-id"
CLUSTER_NAME="todo-app-cluster"
REGION="us-ashburn-1"
TENANCY_NAMESPACE="your-tenancy-namespace"

echo "📝 Configuration:"
echo "  Compartment: $COMPARTMENT_ID"
echo "  Cluster: $CLUSTER_NAME"
echo "  Region: $REGION"

# Step 4: Create OKE cluster (if not exists)
echo "🏗️ Creating OKE cluster..."
CLUSTER_ID=$(oci ce cluster list --compartment-id $COMPARTMENT_ID --name $CLUSTER_NAME --query 'data[0].id' --raw-output 2>/dev/null)

if [ "$CLUSTER_ID" == "null" ] || [ -z "$CLUSTER_ID" ]; then
    echo "Creating new OKE cluster..."
    # This would create cluster - but requires VCN setup first
    echo "⚠️  Please create OKE cluster manually from Oracle Cloud Console"
    echo "   Go to: Developer Services → Kubernetes Clusters (OKE)"
    echo "   Click: Create Cluster → Quick Create"
    echo "   Choose: Always Free eligible shapes"
    exit 1
else
    echo "✅ Using existing cluster: $CLUSTER_ID"
fi

# Step 5: Configure kubectl
echo "🔧 Configuring kubectl..."
oci ce cluster create-kubeconfig \
    --cluster-id $CLUSTER_ID \
    --file ~/.kube/config \
    --region $REGION \
    --token-version 2.0.0 \
    --kube-endpoint PUBLIC_ENDPOINT

# Test connection
echo "🧪 Testing connection..."
kubectl get nodes

# Step 6: Deploy application
echo "🚀 Deploying Todo App to OKE..."

# Create namespace
kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -

# Deploy using Helm
helm upgrade --install todo-app k8s/helm/todo-app/ \
    --namespace todo-app \
    --set backend.image.repository=$REGION.ocir.io/$TENANCY_NAMESPACE/todo-backend \
    --set frontend.image.repository=$REGION.ocir.io/$TENANCY_NAMESPACE/todo-frontend \
    --set backend.image.tag=latest \
    --set frontend.image.tag=latest \
    --wait --timeout=600s

# Get service URLs
echo "🌐 Getting service URLs..."
kubectl get services -n todo-app

echo "✅ Deployment completed!"
echo ""
echo "📱 Access your application:"
FRONTEND_IP=$(kubectl get service frontend-service -n todo-app -o jsonpath='{.status.loadBalancer.ingress[0].ip}' 2>/dev/null)
if [ ! -z "$FRONTEND_IP" ]; then
    echo "  Frontend: http://$FRONTEND_IP:3000"
else
    echo "  Frontend: $(kubectl get service frontend-service -n todo-app)"
fi