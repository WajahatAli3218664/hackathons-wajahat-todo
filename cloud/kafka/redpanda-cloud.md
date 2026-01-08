# Redpanda Cloud Setup for Production Kafka

## Step 1: Create Redpanda Cloud Account
1. Go to https://redpanda.com/cloud
2. Sign up for free Serverless tier
3. Create cluster in same region as OKE

## Step 2: Create Topics
```bash
rpk topic create task-events --partitions 3 --replicas 3
rpk topic create reminders --partitions 3 --replicas 3  
rpk topic create task-updates --partitions 3 --replicas 3
```

## Step 3: Update Kubernetes Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: kafka-config
  namespace: todo-app
type: Opaque
stringData:
  bootstrap-servers: "seed-123abc.cloud.redpanda.com:9092"
  sasl-username: "todo-app-user"
  sasl-password: "your-password"
  security-protocol: "SASL_SSL"
  sasl-mechanism: "SCRAM-SHA-256"
```