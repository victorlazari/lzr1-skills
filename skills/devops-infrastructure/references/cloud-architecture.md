# Cloud Architecture

## Table of Contents
1. Multi-Cloud Strategy
2. AWS Architecture
3. GCP Architecture
4. Azure Architecture
5. Cost Optimization
6. Well-Architected Framework

---

## 1. Multi-Cloud Strategy

### When to Use Multi-Cloud

| Reason | Justification | Consideration |
|---|---|---|
| Avoid vendor lock-in | Business continuity | Adds operational complexity |
| Best-of-breed services | Use each cloud's strengths | Higher learning curve |
| Compliance/data sovereignty | Regional requirements | Network latency between clouds |
| Disaster recovery | Cross-cloud failover | Expensive to maintain active-active |
| Acquisitions | Inherited infrastructure | Consolidation path needed |

### Abstraction Layers

- **Kubernetes**: Portable workload orchestration across clouds
- **Terraform**: Multi-cloud IaC with provider abstraction
- **Service mesh (Istio)**: Cross-cloud service communication
- **Object storage APIs**: S3-compatible interfaces (MinIO)
- **Managed databases**: CockroachDB, PlanetScale for portability

---

## 2. AWS Architecture

### Core Services by Category

| Category | Service | Purpose |
|---|---|---|
| Compute | EC2, ECS, EKS, Lambda, Fargate | Run workloads |
| Storage | S3, EBS, EFS, FSx | Data storage |
| Database | RDS, Aurora, DynamoDB, ElastiCache | Data persistence |
| Networking | VPC, ALB/NLB, Route 53, CloudFront | Network and CDN |
| Security | IAM, KMS, Secrets Manager, GuardDuty | Security controls |
| Observability | CloudWatch, X-Ray, CloudTrail | Monitoring and audit |
| Messaging | SQS, SNS, EventBridge, Kinesis | Async communication |

### AWS Well-Architected Pillars

1. **Operational Excellence**: Automate operations, learn from failures
2. **Security**: Protect data, manage access, detect events
3. **Reliability**: Recover from failures, meet demand
4. **Performance Efficiency**: Use resources efficiently
5. **Cost Optimization**: Avoid unnecessary costs
6. **Sustainability**: Minimize environmental impact

### VPC Design Pattern

```
Region
├── VPC (10.0.0.0/16)
│   ├── Public Subnets (3 AZs)
│   │   ├── NAT Gateways
│   │   ├── Load Balancers
│   │   └── Bastion hosts
│   ├── Private Subnets (3 AZs)
│   │   ├── Application servers
│   │   ├── EKS worker nodes
│   │   └── Internal services
│   └── Data Subnets (3 AZs)
│       ├── RDS instances
│       ├── ElastiCache
│       └── Elasticsearch
```

---

## 3. GCP Architecture

### Core Services

| Category | Service | Purpose |
|---|---|---|
| Compute | GCE, GKE, Cloud Run, Cloud Functions | Run workloads |
| Storage | Cloud Storage, Persistent Disk, Filestore | Data storage |
| Database | Cloud SQL, Spanner, Firestore, Bigtable | Data persistence |
| Networking | VPC, Cloud Load Balancing, Cloud DNS, CDN | Network and CDN |
| Security | IAM, KMS, Secret Manager, Security Command Center | Security |
| Observability | Cloud Monitoring, Cloud Logging, Cloud Trace | Monitoring |
| Messaging | Pub/Sub, Cloud Tasks, Eventarc | Async communication |

### GCP Differentiators

- **Spanner**: Globally distributed, strongly consistent database
- **BigQuery**: Serverless data warehouse with ML built-in
- **GKE Autopilot**: Fully managed Kubernetes (no node management)
- **Cloud Run**: Serverless containers with scale-to-zero
- **Anthos**: Hybrid/multi-cloud Kubernetes management

---

## 4. Azure Architecture

### Core Services

| Category | Service | Purpose |
|---|---|---|
| Compute | VMs, AKS, App Service, Functions, Container Apps | Run workloads |
| Storage | Blob Storage, Managed Disks, Azure Files | Data storage |
| Database | Azure SQL, Cosmos DB, Cache for Redis | Data persistence |
| Networking | VNet, Load Balancer, Front Door, DNS | Network and CDN |
| Security | Entra ID, Key Vault, Defender, Sentinel | Security |
| Observability | Monitor, Log Analytics, Application Insights | Monitoring |
| Messaging | Service Bus, Event Grid, Event Hubs | Async communication |

### Azure Differentiators

- **Entra ID (Azure AD)**: Enterprise identity and access management
- **Cosmos DB**: Multi-model, globally distributed database
- **Azure DevOps**: Integrated CI/CD and project management
- **Azure Arc**: Manage on-premises and multi-cloud resources
- **Power Platform**: Low-code integration with Azure services

---

## 5. Cost Optimization

### Cost Reduction Strategies

| Strategy | Savings | Effort | Risk |
|---|---|---|---|
| Reserved Instances (1-3 yr) | 30-72% | Low | Commitment |
| Spot/Preemptible instances | 60-90% | Medium | Interruption |
| Right-sizing | 20-40% | Medium | Performance impact |
| Auto-scaling | Variable | Medium | Configuration |
| Storage tiering | 30-60% | Low | Access latency |
| Serverless migration | Variable | High | Architecture change |

### FinOps Practices

- Tag all resources for cost allocation (team, environment, project)
- Set budgets and alerts per team/project
- Review costs weekly; optimize monthly
- Use spot instances for stateless, fault-tolerant workloads
- Implement auto-scaling with appropriate min/max
- Delete unused resources (snapshots, unattached volumes, idle LBs)
- Use savings plans for predictable baseline compute
- Implement data lifecycle policies (S3 Glacier, archive tiers)

---

## 6. Well-Architected Framework

### Design Principles (Universal)

- Design for failure: assume everything fails
- Decouple components: reduce blast radius
- Implement elasticity: scale with demand
- Think parallel: distribute workloads
- Automate everything: reduce human error
- Use managed services: reduce operational burden
- Implement security at every layer: defense in depth
- Optimize costs continuously: right-size and review
