# Speedtest (Ookla) Complete Reference

This document consolidates advanced technical knowledge, architectural details, CLI command references, configuration schemas, troubleshooting guides, and security audit checklists for Speedtest (Ookla).

## 1. Core Measurement Methodology & Architecture

Speedtest.net measures the **full throughput capacity** of a network connection using a **foreground testing** paradigm. It actively floods the network interface to determine the realistic maximum Quality of Service (QoS).

### 1.1 TCP Test Components
- **Latency/Jitter**: Measured via bidirectional round-trip time (RTT) of small packets. Multiple pings are sent, and the lowest RTT is selected. Jitter is the variance.
- **Download Phase**: Establishes multiple concurrent TCP connections (port 8080). Dynamically adjusts chunk size and TCP buffer window to maximize utilization. Spawns additional threads if throughput exceeds thresholds (e.g., 4 Mbps) to overcome TCP slow start.
- **Upload Phase**: Mirrors download but in reverse. Server measures incoming data streams to handle asymmetric paths and high latency.

### 1.2 Multi-Stage Latency Measurement
Speedtest measures ping at three stages to assess bufferbloat and responsiveness:
1. **Idle Ping**: Baseline latency before data transfer.
2. **Download Ping**: Latency during downlink saturation.
3. **Upload Ping**: Latency during uplink saturation.

*Gaming Latency Guidelines:*
- 0-59 ms: Winning
- 60-129 ms: In the game
- 130-199 ms: Struggling
- 200+ ms: Unplayable

### 1.3 Result Calculation Algorithm
To ensure statistical robustness:
1. Sort all throughput samples descending.
2. Remove the top 2 fastest samples (anomalous spikes).
3. Remove the bottom 25% (transient slowdowns).
4. Average the remaining middle 72-73% of samples.

### 1.4 5G, Fiber, and Super-Fast Connections
Traditional small-file tests fail on 5G/Fiber due to TCP slow start and carrier aggregation requirements. Speedtest solves this via **Dynamic Connection Scaling** (spawning 4+ threads) and sustained data transfers with adaptive chunk sizes, saturating links up to 10 Gbps.

---

## 2. Speedtest CLI Command Reference

The `speedtest` CLI is a native Linux binary for automated testing and observability integration.

### 2.1 Global Flags
- `-h, --help`: Display help.
- `-V, --version`: Print version.
- `-L, --servers`: List nearby test servers.
- `--selection-details`: Show server selection latency details.

### 2.2 Output Formatting
- `-f, --format <FORMAT>`: `human-readable` (default), `csv`, `tsv`, `json`, `jsonl`, `json-pretty`.
- `--output-header`: Include headers for CSV/TSV.
- `-p, --progress <yes|no>`: Toggle interactive progress bar (disable for scripts).

### 2.3 Server & Network Selection
- `-s, --server-id <ID>`: Force specific server ID.
- `-o, --host <HOSTNAME>`: Specify custom server hostname/IP.
- `-i, --interface <INTERFACE>`: Bind to specific local interface (e.g., `eth0`).
- `-I, --ip <IP_ADDRESS>`: Bind to specific local IP.

### 2.4 Automated Monitoring Example
```bash
#!/bin/bash
LOG_FILE="/var/log/speedtest/speedtest_$(date +%Y%m%d).jsonl"
/usr/local/bin/speedtest --format json --progress no >> $LOG_FILE 2>&1
echo "" >> $LOG_FILE
```

---

## 3. Configuration Schemas

Speedtest tools often use YAML/JSON configuration files.

### 3.1 `speedtest.yaml` (Global)
```yaml
global:
  test_duration: 10 # seconds
  retries: 3
  timeout: 30
  enable_logging: true
  log_level: "INFO"
```

### 3.2 `servers.yaml` (Server Selection)
```yaml
servers:
  preferred:
    - id: 1234
  fallback:
    - id: 5678
  auto_select: true
```

### 3.3 `network.yaml` (Network & Proxy)
```yaml
network:
  interface: "eth0"
  proxy:
    enabled: false
    host: "proxy.example.com"
    port: 8080
```

### 3.4 `advanced.yaml` (Tuning)
```yaml
advanced:
  max_threads: 4
  buffer_size: 65536
  randomize_data: true
```

---

## 4. Troubleshooting & Diagnostics

### 4.1 Common Error Codes
- **100 (Network Unreachable)**: Client cannot reach server. Check connectivity, DNS, firewall.
- **101 (Server Unavailable)**: Server is down. Verify server status.
- **102 (Timeout Error)**: Test didn't complete. Increase timeout, check congestion.
- **103 (Protocol Mismatch)**: Update client/server software.

### 4.2 Diagnostic Tools
- **ping / traceroute**: Check latency and network path.
- **netstat / Wireshark**: Analyze active connections and packet drops.
- **iperf3**: Independent throughput testing.

### 4.3 Advanced Tuning
- **MTU Adjustment**: `ping -f -l 1472 google.com`
- **TCP Window Scaling**: `echo 1 > /proc/sys/net/ipv4/tcp_window_scaling`
- **NIC Settings**: `ethtool -s eth0 speed 1000 duplex full autoneg on`

---

## 5. Security Audit Checklist

When deploying custom OoklaServer instances or enterprise Speedtest infrastructure, follow this checklist:

### 5.1 Architecture & Network Security
- [ ] Encrypt all client-server traffic (TLS 1.2+).
- [ ] Isolate test nodes from internal corporate networks.
- [ ] Restrict administrative interfaces to trusted IPs.
- [ ] Implement DDoS protection (rate limiting, Anycast routing).

### 5.2 Server-Side Hardening
- [ ] Apply OS security patches promptly.
- [ ] Disable unnecessary services/ports.
- [ ] Secure SSH access (key-based, disable root login).
- [ ] Implement HIDS and File Integrity Monitoring (FIM).

### 5.3 API & Client Security
- [ ] Enforce strong authentication (OAuth 2.0, API keys) for APIs.
- [ ] Validate/sanitize all API inputs to prevent injection.
- [ ] Protect web clients against XSS/CSRF.
- [ ] Implement Content Security Policy (CSP).

### 5.4 Data Privacy & Compliance
- [ ] Comply with GDPR/CCPA for IP and location data collection.
- [ ] Implement data anonymization/pseudonymization.
- [ ] Establish data retention and deletion policies.
- [ ] Maintain an Incident Response Plan and conduct regular penetration testing.
