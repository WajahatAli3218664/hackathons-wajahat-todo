# Phase V: Advanced Cloud Deployment Plan

## Architecture Overview

### Event-Driven Microservices
```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                              KUBERNETES CLUSTER                                       │
│                                                                                       │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────────────────────────────────────┐ │
│  │  Frontend   │   │  Chat API   │   │              KAFKA CLUSTER                  │ │
│  │  Service    │──▶│  + MCP      │──▶│  ┌─────────────┐  ┌─────────────────────┐  │ │
│  └─────────────┘   │  Tools      │   │  │ task-events │  │ reminders           │  │ │
│                    └──────┬──────┘   │  └─────────────┘  └─────────────────────┘  │ │
│                           │          └──────────┬────────────────────┬────────────┘ │
│                           │                     │                    │              │
│                           ▼                     ▼                    ▼              │
│                    ┌─────────────┐   ┌─────────────────┐   ┌─────────────────┐     │
│                    │   Neon DB   │   │ Recurring Task  │   │  Notification   │     │
│                    │  (External) │   │    Service      │   │    Service      │     │
│                    └─────────────┘   └─────────────────┘   └─────────────────┘     │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

## Implementation Phases

### Phase A: Advanced Features Implementation
1. **Database Schema Updates**
   - Add priority, tags, due_date, recurring fields to tasks table
   - Create tags table for many-to-many relationship
   - Add indexes for search and filtering

2. **Backend API Enhancements**
   - Extend Task model with new fields
   - Add search, filter, sort endpoints
   - Implement recurring task logic
   - Add due date validation

3. **Frontend UI Updates**
   - Priority selector component
   - Tag management interface
   - Date/time picker for due dates
   - Search and filter controls
   - Recurring task configuration

### Phase B: Event-Driven Architecture
1. **Kafka Integration**
   - Deploy Redpanda on Minikube
   - Create Kafka topics
   - Add Kafka producer to Chat API
   - Implement event schemas

2. **Microservices Development**
   - Notification Service (FastAPI)
   - Recurring Task Service (FastAPI)
   - Audit Service (FastAPI)
   - Event consumers with Kafka

3. **Dapr Configuration**
   - Pub/Sub component for Kafka
   - State component for Redis
   - Bindings for cron jobs
   - Service-to-service invocation

### Phase C: Cloud Deployment
1. **Oracle Cloud Setup**
   - Create OKE cluster
   - Configure networking and security
   - Set up Redpanda Cloud

2. **CI/CD Pipeline**
   - GitHub Actions workflows
   - Docker image registry
   - Helm chart deployment
   - Environment management

3. **Monitoring Stack**
   - Prometheus deployment
   - Grafana dashboards
   - Alerting rules
   - Log aggregation

## Technology Decisions

### Kafka vs Alternatives
- **Choice**: Redpanda (Kafka-compatible)
- **Reasons**: No Zookeeper, faster, easier setup, free tier

### Cloud Provider
- **Choice**: Oracle Cloud (OKE)
- **Reasons**: Always free tier, no time limits, 4 OCPUs + 24GB RAM

### Dapr Components
- **Pub/Sub**: Kafka (Redpanda)
- **State**: Redis
- **Bindings**: Cron (for scheduled tasks)
- **Secrets**: Kubernetes secrets
- **Service Invocation**: HTTP

## Event Flows

### Task Creation with Recurring
```
1. User creates recurring task via Chat API
2. Chat API saves task to database
3. Chat API publishes "task-created" event to Kafka
4. Recurring Task Service consumes event
5. If recurring, schedules next occurrence
```

### Reminder System
```
1. Task with due date created
2. Chat API publishes "reminder-scheduled" event
3. Notification Service consumes event
4. Service schedules reminder job
5. At reminder time, sends notification
```

### Real-time Updates
```
1. Task updated in any client
2. Chat API publishes "task-updated" event
3. WebSocket Service consumes event
4. Broadcasts update to all connected clients
```

## Development Workflow
1. Write detailed specifications
2. Generate implementation plan
3. Break into atomic tasks
4. Implement via Claude Code assistance
5. Test locally on Minikube
6. Deploy to Oracle Cloud
7. Monitor and optimize