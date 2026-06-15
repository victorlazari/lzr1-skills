# Kubernetes

## Table of Contents
1. Architecture and Components
2. Workload Management
3. Networking
4. Storage
5. Security
6. Operations and Troubleshooting

---

## 1. Architecture and Components

### Control Plane

| Component | Purpose | Failure Impact |
|---|---|---|
| kube-apiserver | API gateway, authentication, admission | Cluster unmanageable |
| etcd | Distributed key-value store (cluster state) | Total cluster failure |
| kube-scheduler | Assigns pods to nodes | New pods won't schedule |
| kube-controller-manager | Runs controllers (ReplicaSet, Deployment) | No reconciliation |
| cloud-controller-manager | Cloud provider integration | Cloud resources stale |

### Node Components

| Component | Purpose | Configuration |
|---|---|---|
| kubelet | Pod lifecycle management | Node-level agent |
| kube-proxy | Network rules (iptables/IPVS) | Service networking |
| Container runtime | Run containers (containerd, CRI-O) | OCI-compliant |

### Resource Hierarchy

```
Cluster → Namespace → Deployment → ReplicaSet → Pod → Container
```

---

## 2. Workload Management

### Workload Types

| Resource | Use Case | Scaling |
|---|---|---|
| Deployment | Stateless applications | HPA, replicas |
| StatefulSet | Databases, stateful apps | Ordered scaling |
| DaemonSet | Node-level agents (logging, monitoring) | One per node |
| Job | One-time tasks | Completions |
| CronJob | Scheduled tasks | Schedule-based |

### Deployment Strategies

| Strategy | Downtime | Rollback | Resource Usage |
|---|---|---|---|
| Rolling Update | Zero | Automatic | 1.25-1.5x normal |
| Blue-Green | Zero | Instant (switch) | 2x normal |
| Canary | Zero | Fast (route change) | 1.1x normal |
| Recreate | Yes | Redeploy | 1x normal |

### Resource Management

```yaml
resources:
  requests:    # Scheduling guarantee (minimum)
    cpu: 100m       # 0.1 CPU cores
    memory: 128Mi   # 128 MiB
  limits:      # Hard ceiling (maximum)
    cpu: 500m       # 0.5 CPU cores
    memory: 512Mi   # 512 MiB (OOMKilled if exceeded)
```

**Best Practices**:
- Always set requests (scheduling) and memory limits (OOM protection)
- CPU limits are controversial: can cause throttling; consider omitting
- Use LimitRange for namespace defaults
- Use ResourceQuota to prevent resource exhaustion per namespace
- Right-size based on actual usage (VPA recommendations)

### Horizontal Pod Autoscaler (HPA)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 3
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Prevent flapping
```

---

## 3. Networking

### Service Types

| Type | Access | Use Case |
|---|---|---|
| ClusterIP | Internal only | Service-to-service |
| NodePort | External via node IP:port | Development, testing |
| LoadBalancer | External via cloud LB | Production external access |
| ExternalName | DNS CNAME | External service alias |

### Ingress Controllers

| Controller | Features | Best For |
|---|---|---|
| NGINX Ingress | Widely used, stable, flexible | General purpose |
| Traefik | Auto-discovery, middleware | Dynamic environments |
| Istio Gateway | Service mesh integration | Istio users |
| AWS ALB Ingress | AWS-native, WAF integration | AWS environments |
| Envoy Gateway | K8s Gateway API native | Modern deployments |

### Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend-to-backend
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - port: 8080
```

### Service Mesh (Istio/Linkerd)

- **mTLS**: Automatic encryption between services
- **Traffic management**: Canary, A/B testing, fault injection
- **Observability**: Automatic metrics, traces, access logs
- **Resilience**: Retries, timeouts, circuit breakers
- **Authorization**: Fine-grained access policies

---

## 4. Storage

### Storage Classes

| Type | Speed | Persistence | Use Case |
|---|---|---|---|
| emptyDir | Fast (node disk) | Pod lifetime | Temp files, caches |
| hostPath | Fast (node disk) | Node lifetime | Development only |
| PersistentVolume (block) | Fast | Persistent | Databases |
| PersistentVolume (file) | Medium | Persistent | Shared storage |
| CSI drivers | Variable | Persistent | Cloud-specific |

### StatefulSet Storage Pattern

```yaml
volumeClaimTemplates:
- metadata:
    name: data
  spec:
    accessModes: ["ReadWriteOnce"]
    storageClassName: gp3
    resources:
      requests:
        storage: 100Gi
```

---

## 5. Security

### Pod Security Standards

| Level | Description | Use Case |
|---|---|---|
| Privileged | Unrestricted | System-level pods |
| Baseline | Minimal restrictions | General workloads |
| Restricted | Hardened | Security-sensitive |

### Security Best Practices

- Run containers as non-root (`runAsNonRoot: true`)
- Use read-only root filesystem (`readOnlyRootFilesystem: true`)
- Drop all capabilities, add only needed ones
- Use network policies to restrict pod-to-pod communication
- Scan images for vulnerabilities (Trivy, Snyk)
- Use admission controllers (OPA Gatekeeper, Kyverno)
- Rotate secrets regularly (External Secrets Operator)
- Enable audit logging for API server
- Use RBAC with least privilege principle
- Sign and verify container images (cosign, Notary)

### RBAC Pattern

```yaml
# Role: defines permissions within a namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "watch"]
---
# RoleBinding: assigns role to user/group/service account
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: production
  name: read-pods
subjects:
- kind: ServiceAccount
  name: monitoring-sa
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

---

## 6. Operations and Troubleshooting

### Troubleshooting Workflow

```
Pod not running?
├── Pending → Check scheduling (resources, node selector, taints)
├── CrashLoopBackOff → Check logs (kubectl logs), liveness probe
├── ImagePullBackOff → Check image name, registry auth, network
├── OOMKilled → Increase memory limits or fix memory leak
└── Evicted → Node under pressure, check resource usage
```

### Essential Commands

```bash
# Debugging pods
kubectl describe pod <name> -n <ns>     # Events, conditions
kubectl logs <pod> -n <ns> --previous   # Previous container logs
kubectl exec -it <pod> -- /bin/sh       # Shell into container
kubectl top pods -n <ns>                # Resource usage

# Debugging nodes
kubectl describe node <name>            # Conditions, capacity
kubectl top nodes                       # Node resource usage
kubectl drain <node> --ignore-daemonsets # Evacuate node

# Debugging networking
kubectl run debug --image=nicolaka/netshoot -it --rm -- /bin/bash
nslookup <service>.<namespace>.svc.cluster.local
curl -v http://<service>:<port>/health
```

### Helm Best Practices

- Use `helm diff` before upgrading to preview changes
- Pin chart versions in production (never use `latest`)
- Use values files per environment (values-prod.yaml, values-staging.yaml)
- Implement proper hooks for migrations (pre-upgrade, post-upgrade)
- Use `helm test` for release validation
- Store Helm values in version control (GitOps)
