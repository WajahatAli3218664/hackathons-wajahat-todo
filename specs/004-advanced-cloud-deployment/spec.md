# Phase V: Advanced Cloud Deployment Specification

## Overview
Implement advanced features with event-driven architecture using Kafka and Dapr, then deploy to production cloud (AKS/GKE/OKE).

## Objectives
- Add Advanced Level features (Recurring Tasks, Due Dates & Reminders)
- Add Intermediate Level features (Priorities, Tags, Search, Filter, Sort)
- Implement event-driven architecture with Kafka
- Deploy Dapr for distributed application runtime
- Deploy locally on Minikube then to cloud (AKS/GKE/OKE)

## Technology Stack
- **Event Streaming**: Kafka (Redpanda Cloud/Self-hosted)
- **Distributed Runtime**: Dapr (Pub/Sub, State, Bindings, Secrets, Service Invocation)
- **Cloud Platform**: Oracle Cloud (OKE) - Always Free
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

## Part A: Advanced Features

### A1: Advanced Level Features
- **Recurring Tasks**: Daily, Weekly, Monthly patterns
- **Due Dates**: Date/time picker with timezone support
- **Reminders**: Email/Push notifications before due date

### A2: Intermediate Level Features
- **Priorities**: High, Medium, Low with color coding
- **Tags**: Custom labels for task categorization
- **Search**: Full-text search across title and description
- **Filter**: By status, priority, tags, due date
- **Sort**: By created date, due date, priority, alphabetical

### A3: Event-Driven Architecture
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Chat API       │────▶│  Kafka Topics   │────▶│  Microservices  │
│  (Producer)     │     │  - task-events  │     │  - Notification │
│                 │     │  - reminders    │     │  - Recurring    │
│                 │     │  - task-updates │     │  - Audit        │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Part B: Local Deployment (Minikube)

### B1: Kafka Setup
- Deploy Redpanda on Minikube
- Create topics: task-events, reminders, task-updates
- Configure Kafka clients in services

### B2: Dapr Integration
- Install Dapr on Minikube
- Configure Pub/Sub component (Kafka)
- Configure State component (Redis)
- Configure Bindings component (Cron)
- Configure Secrets component (Kubernetes)
- Configure Service Invocation

### B3: Microservices Architecture
- **Chat API**: Main service with MCP tools
- **Notification Service**: Handles reminders and alerts
- **Recurring Task Service**: Manages recurring task creation
- **Audit Service**: Logs all task operations

## Part C: Cloud Deployment

### C1: Oracle Cloud (OKE) Setup
- Create OKE cluster (Always Free: 4 OCPUs, 24GB RAM)
- Configure kubectl for OKE
- Deploy Dapr on OKE
- Use Redpanda Cloud for managed Kafka

### C2: CI/CD Pipeline
- GitHub Actions workflow
- Automated testing
- Docker image builds
- Helm chart deployment
- Environment promotion (dev → staging → prod)

### C3: Monitoring & Observability
- Prometheus for metrics
- Grafana for dashboards
- Jaeger for distributed tracing
- ELK stack for logging

## Success Criteria
- [ ] All advanced features implemented and working
- [ ] Event-driven architecture with Kafka operational
- [ ] Dapr components configured and functional
- [ ] Local deployment on Minikube successful
- [ ] Cloud deployment on OKE successful
- [ ] CI/CD pipeline automated
- [ ] Monitoring and logging operational
- [ ] Performance and scalability tested