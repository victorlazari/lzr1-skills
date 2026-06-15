# Networking

## Table of Contents
1. Network Architecture
2. Load Balancing
3. DNS
4. Security
5. Troubleshooting

---

## 1. Network Architecture

### Network Layers (OSI Model - Relevant Layers)

| Layer | Protocol | DevOps Relevance |
|---|---|---|
| L7 (Application) | HTTP, gRPC, DNS | API gateways, WAF, routing |
| L4 (Transport) | TCP, UDP | Load balancers, firewalls |
| L3 (Network) | IP, ICMP | Routing, VPNs, subnets |
| L2 (Data Link) | Ethernet, ARP | VLANs, switches |

### Cloud Network Design

```
Internet → WAF → CDN → Load Balancer → Application (Private Subnet) → Database (Isolated Subnet)
                                              ↓
                                     NAT Gateway → Internet (outbound only)
```

### VPN and Connectivity

| Solution | Use Case | Bandwidth |
|---|---|---|
| Site-to-Site VPN | Office to cloud | Up to 1.25 Gbps |
| Client VPN | Remote access | Variable |
| Direct Connect / ExpressRoute | High-bandwidth, low-latency | 1-100 Gbps |
| Transit Gateway | Multi-VPC connectivity | Scalable |
| VPC Peering | VPC-to-VPC | No bandwidth limit |

---

## 2. Load Balancing

### Load Balancer Types

| Type | Layer | Features | Use Case |
|---|---|---|---|
| Application LB (ALB) | L7 | Path routing, host routing, WebSocket | Web applications |
| Network LB (NLB) | L4 | Ultra-low latency, static IP, TCP/UDP | High-performance |
| Gateway LB | L3 | Transparent network gateway | Security appliances |
| Global LB | L7 | Multi-region, anycast | Global applications |

### Load Balancing Algorithms

| Algorithm | Description | Best For |
|---|---|---|
| Round Robin | Sequential distribution | Equal-capacity servers |
| Least Connections | Route to least busy | Variable request duration |
| Weighted | Proportional distribution | Mixed-capacity servers |
| IP Hash | Consistent per-client routing | Session affinity |
| Random | Random selection | Simple, stateless |

### Health Checks

```yaml
# Kubernetes-style health checks
livenessProbe:      # Is the container alive? (restart if fails)
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:     # Is the container ready for traffic? (remove from LB if fails)
  httpGet:
    path: /ready
    port: 8080
  periodSeconds: 5
  failureThreshold: 2

startupProbe:       # Has the container started? (don't check liveness until started)
  httpGet:
    path: /healthz
    port: 8080
  failureThreshold: 30
  periodSeconds: 10
```

---

## 3. DNS

### DNS Record Types

| Type | Purpose | Example |
|---|---|---|
| A | IPv4 address | `api.example.com → 1.2.3.4` |
| AAAA | IPv6 address | `api.example.com → 2001:db8::1` |
| CNAME | Alias to another name | `www → example.com` |
| MX | Mail server | `example.com → mail.example.com` |
| TXT | Verification, SPF, DKIM | `v=spf1 include:...` |
| SRV | Service discovery | `_http._tcp.example.com` |
| CAA | Certificate authority authorization | `example.com CAA 0 issue "letsencrypt.org"` |

### DNS Strategies

| Strategy | Purpose | Implementation |
|---|---|---|
| Weighted routing | Traffic distribution | 80% primary, 20% secondary |
| Latency-based | Performance | Route to nearest region |
| Failover | High availability | Health-checked primary/secondary |
| Geolocation | Compliance, performance | Route by user location |

---

## 4. Security

### Network Security Layers

| Layer | Control | Purpose |
|---|---|---|
| Edge | WAF, DDoS protection | Block attacks at the perimeter |
| Network | Security groups, NACLs | Control traffic flow |
| Transport | TLS/mTLS | Encrypt in transit |
| Application | API gateway, auth | Application-level security |
| Data | Encryption at rest | Protect stored data |

### Firewall Rules (Security Groups)

```
# Principle: Default deny, explicit allow
Inbound:
  - Allow HTTPS (443) from 0.0.0.0/0 (public-facing)
  - Allow HTTP (80) from 0.0.0.0/0 (redirect to HTTPS)
  - Allow app port from load balancer SG only
  - Allow SSH (22) from bastion SG only

Outbound:
  - Allow HTTPS (443) to 0.0.0.0/0 (API calls)
  - Allow database port to database SG only
  - Allow DNS (53) to VPC DNS
```

### Zero Trust Networking

- Never trust, always verify (even internal traffic)
- Authenticate and authorize every request
- Use mTLS for service-to-service communication
- Implement micro-segmentation (network policies)
- Log and monitor all network traffic
- Use identity-based access (not IP-based)

---

## 5. Troubleshooting

### Network Troubleshooting Tools

| Tool | Purpose | Example |
|---|---|---|
| ping | Connectivity test | `ping -c 4 host` |
| traceroute | Path discovery | `traceroute host` |
| dig/nslookup | DNS resolution | `dig +short example.com` |
| curl | HTTP testing | `curl -v https://api.example.com` |
| netstat/ss | Connection state | `ss -tlnp` |
| tcpdump | Packet capture | `tcpdump -i eth0 port 443` |
| mtr | Combined ping + traceroute | `mtr host` |
| nmap | Port scanning | `nmap -sT host` |
| openssl | TLS debugging | `openssl s_client -connect host:443` |

### Common Issues and Resolution

| Symptom | Likely Cause | Investigation |
|---|---|---|
| Connection timeout | Firewall/SG blocking | Check security groups, NACLs |
| Connection refused | Service not listening | Check service status, port binding |
| DNS resolution failure | DNS misconfiguration | Check Route 53, resolv.conf |
| Intermittent failures | Network instability | Check packet loss, MTU issues |
| SSL/TLS errors | Certificate issues | Check expiry, chain, SANs |
| High latency | Network congestion or routing | Check traceroute, bandwidth |
