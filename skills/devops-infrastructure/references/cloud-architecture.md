# Cloud Architecture

**Verified against upstream: 2026-08-07**

## Table of Contents
1. Multi-Cloud Strategy
2. AWS Architecture
3. GCP Architecture
4. Azure Architecture
5. Well-Architected Framework

---

## 1. Multi-Cloud Strategy

### When to Use Multi-Cloud

| Reason | Justification | Consideration |
|---|---|---|
| Avoid vendor lock-in | Business continuity | Adds operational complexity |
| Best-of-breed services | Use each cloud's strengths | Higher learning curve |
| Compliance/data sovereignty | Regional requirements | Network latency between clouds |
| Disaster recovery | Cross-cloud failover | Expensive to maintain |

## 2. AWS Architecture

- **Compute**: EC2, ECS, EKS, Lambda
- **Storage**: S3, EBS, EFS
- **Database**: RDS, DynamoDB, Aurora
- **Networking**: VPC, Route 53, CloudFront

## 3. GCP Architecture

- **Compute**: Compute Engine, GKE, Cloud Run
- **Storage**: Cloud Storage, Persistent Disk
- **Database**: Cloud SQL, Spanner, Bigtable
- **Networking**: VPC, Cloud DNS, Cloud CDN

## 4. Azure Architecture

- **Compute**: Virtual Machines, AKS, Azure Functions
- **Storage**: Blob Storage, Managed Disks
- **Database**: Azure SQL, Cosmos DB
- **Networking**: Virtual Network, Azure DNS, Front Door

## 5. Well-Architected Framework

- **Operational Excellence**: Run and monitor systems to deliver business value.
- **Security**: Protect information, systems, and assets.
- **Reliability**: Ensure a workload performs its intended function correctly and consistently.
- **Performance Efficiency**: Use computing resources efficiently to meet system requirements.
- **Cost Optimization**: Avoid unnecessary costs.
- **Sustainability**: Minimize the environmental impacts of running cloud workloads.
