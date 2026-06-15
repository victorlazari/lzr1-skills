# NemoClaw Specialist Guide

> **Role:** NVIDIA NemoClaw Platform Specialist
> **Domain:** Sandboxed AI agent runtime, security-hardened OpenClaw deployment, NVIDIA OpenShell, inference routing
> **Official Documentation:** [docs.nvidia.com/nemoclaw](https://docs.nvidia.com/nemoclaw/latest/) | [GitHub](https://github.com/NVIDIA/NemoClaw)
> **License:** Apache-2.0

---

## 1. Executive Summary and Core Philosophy

NVIDIA NemoClaw is an open-source reference stack that simplifies running OpenClaw always-on assistants more safely. It installs the NVIDIA OpenShell runtime (part of NVIDIA Agent Toolkit) which provides additional security layers for running autonomous agents. NemoClaw wraps OpenClaw inside a hardened, containerized sandbox with network policies, filesystem restrictions, process isolation, and routed inference — ensuring that the AI agent operates within strictly defined boundaries [1] [2].

The project was released as an **alpha / early preview** on March 16, 2026, and has rapidly gained traction with 19.9k GitHub stars, 2.5k forks, and 116 contributors. The codebase is primarily TypeScript (72.5%), Shell (23.9%), and Python (2.0%), with 1,018 commits across 507 branches and 30 tags. NemoClaw is licensed under Apache-2.0 [1].

The fundamental philosophy of NemoClaw centers on the principle that **autonomous AI agents must be contained by default**. Unlike a bare OpenClaw installation where the agent has broad access to the host system, NemoClaw enforces a layered security model where no access is granted by default, and every capability must be explicitly approved by the operator. This "deny-all, approve-selectively" approach is critical for production deployments where agents run autonomously for extended periods [2].

### 1.1 Key Capabilities

| Capability | Description |
|-----------|-------------|
| **Sandbox OpenClaw** | Creates an OpenShell sandbox pre-configured for OpenClaw, with filesystem and network policies applied from first boot |
| **Route Inference** | Configures OpenShell inference routing (NVIDIA Endpoints, OpenAI, Anthropic, Gemini, Ollama, etc.). Agent uses `inference.local` inside sandbox; credentials stay on host |
| **Manage the Lifecycle** | Handles blueprint versioning, digest verification, and sandbox setup |

### 1.2 Key Features

| Feature | Description |
|---------|-------------|
| **Guided Onboarding** | Validates credentials, selects providers, creates working sandbox in one command |
| **Hardened Blueprint** | Security-first Dockerfile with capability drops, least-privilege network rules, declarative policy |
| **State Management** | Safe migration of agent state across machines with credential stripping and integrity verification |
| **Channel Messaging** | OpenShell-managed processes connect Telegram, Discord, Slack to sandboxed agent |
| **Routed Inference** | Provider-routed model calls through OpenShell gateway, transparent to agent |
| **Layered Protection** | Network, filesystem, process, and inference controls that can be hot-reloaded or locked at creation |

---

## 2. Architecture and How It Works

### 2.1 Deployment Topology

NemoClaw's architecture consists of four primary components that work together to provide a secure agent runtime [1]:

**Sandbox** is an isolated container running the OpenClaw agent. The sandbox is created from a hardened blueprint that includes capability drops, filesystem restrictions, and network policies. The agent inside the sandbox cannot directly access the host system or the internet — all communication is mediated through the Gateway.

**Gateway** manages communication between the sandbox and external services. It handles channel connections (Telegram, Discord, Slack), webhook callbacks, and API requests. The Gateway runs on the host system and bridges the isolated sandbox to the outside world.

**Policy Engine** enforces security policies that control what the sandbox can and cannot do. Policies cover network access (which hosts the agent can reach), filesystem access (which paths the agent can read/write), process capabilities (which system calls are allowed), and inference routing (which model providers are available).

**Inference Router** routes model requests from the sandbox to configured providers. The agent inside the sandbox talks to `inference.local`, and the router transparently forwards requests to the actual provider (NVIDIA Endpoints, OpenAI, Anthropic, Gemini, Ollama). This design ensures that provider credentials never enter the sandbox [2].

### 2.2 Integration Layers

NemoClaw operates through four integration layers, each with a specific role in the system [3]:

| Layer | Role |
|-------|------|
| **Onboarding** | `nemoclaw onboard` validates credentials, selects providers, drives blueprint execution |
| **Blueprint** | Supplies hardened image definition, default policies, capability posture, orchestration steps |
| **State Management** | Migrates agent state across machines with credential stripping and integrity checks |
| **Channel Messaging** | OpenShell-managed processes connect Telegram, Discord, Slack to agent |

### 2.3 Plugin and Blueprint Architecture

NemoClaw uses a two-component architecture that separates the lightweight plugin from the heavyweight blueprint [3]:

**Plugin** is a TypeScript package that registers the inference provider and `/nemoclaw` slash command inside the sandbox. The plugin is small and focused — it serves as the interface between the agent and the NemoClaw system.

**Blueprint** is a versioned Python artifact that contains all logic for creating sandboxes, applying policies, configuring inference, and managing the lifecycle. The blueprint is immutable, versioned, and digest-verified to ensure supply chain safety.

The relationship between plugin and blueprint follows a strict protocol: the plugin downloads the blueprint artifact, checks the version, verifies the SHA-256 digest, and then executes the blueprint as a subprocess. The blueprint determines which OpenShell resources to create or update (gateway, inference, sandbox, policy) and calls OpenShell CLI commands to create the sandbox and configure resources [3].

### 2.4 Sandbox Creation Flow

The sandbox creation follows a precise sequence [3]:

1. Plugin downloads blueprint artifact, checks version, verifies digest
2. Blueprint determines which OpenShell resources to create/update (gateway, inference, sandbox, policy)
3. Blueprint calls OpenShell CLI commands to create sandbox and configure resources
4. Agent runs inside sandbox with all controls in place

### 2.5 Design Principles

NemoClaw follows five core design principles that guide all architectural decisions [3]:

1. **Thin plugin, versioned blueprint** — The plugin stays small; all orchestration logic lives in the blueprint
2. **Respect CLI boundaries** — The `nemoclaw` CLI is the primary interface; avoid using `openshell` commands directly
3. **Supply chain safety** — All artifacts are immutable, versioned, and digest-verified
4. **OpenShell-backed lifecycle** — `nemoclaw onboard` is the supported entry point for all operations
5. **Reproducible setup** — Running setup again recreates from the same blueprint/policy, ensuring consistency

---

## 3. Security Model

### 3.1 Protection Layers

NemoClaw implements four distinct protection layers, each addressing a different aspect of security [3]:

| Layer | What It Protects | When It Applies | Mutability |
|-------|-----------------|-----------------|------------|
| **Network** | Blocks unauthorized outbound connections | Hot-reloadable at runtime | Can be updated without restart |
| **Filesystem** | Prevents reads/writes outside `/sandbox` and `/tmp` | Locked at sandbox creation | Immutable after creation |
| **Process** | Blocks privilege escalation and dangerous syscalls | Locked at sandbox creation | Immutable after creation |
| **Inference** | Reroutes model API calls to controlled backends | Hot-reloadable at runtime | Can be updated without restart |

### 3.2 Network Policy

The network policy is one of NemoClaw's most critical security features. By default, the sandbox has **no network access** — all outbound connections are blocked. When the agent attempts to reach an unlisted host, OpenShell blocks the connection and surfaces it in the TUI (Terminal User Interface) for operator approval. This creates a human-in-the-loop security model where the operator must explicitly approve each new network destination [2] [3].

The network policy is declarative and YAML-based, defining egress rules that specify which hosts and ports the sandbox can reach. The policy can be customized to pre-approve known-safe destinations (such as model provider APIs) while blocking everything else.

### 3.3 Filesystem Isolation

Filesystem isolation is enforced through Landlock, a Linux security module that restricts filesystem access at the kernel level. The sandbox can only read and write within `/sandbox` and `/tmp` — all other paths are blocked. This prevents the agent from accessing sensitive host files, modifying system configuration, or exfiltrating data through the filesystem [2].

### 3.4 Process Isolation

Process isolation is enforced through seccomp (secure computing mode), which filters system calls at the kernel level. The seccomp profile blocks dangerous system calls that could be used for privilege escalation, container escape, or other security violations. Additionally, the sandbox runs with dropped capabilities, meaning it cannot perform privileged operations even if a vulnerability is exploited [2].

### 3.5 Inference Routing Security

The inference routing layer ensures that provider credentials never enter the sandbox. The agent inside the sandbox makes inference requests to `inference.local`, which is intercepted by the OpenShell gateway and forwarded to the actual provider with the correct credentials. This design means that even if the sandbox is compromised, the attacker cannot extract API keys or access model providers directly [2] [3].

### 3.6 Additional Security Features

| Feature | Description |
|---------|-------------|
| **SHA-256 integrity verification** | All blueprint artifacts and k8s installer downloads are verified |
| **L4 tunnel for WebSocket hosts** | Secure tunneling for WebSocket connections |
| **GIT_SSL_CAINFO** | Support for proxy CA trust in corporate environments |
| **.dockerignore** | Sensitive file patterns excluded from container builds |
| **Gateway process isolation** | Gateway process runs separately from sandbox agent |
| **Credential stripping** | State migration removes credentials before transfer |

---

## 4. Installation and Prerequisites

### 4.1 Hardware Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 4 vCPU | 4+ vCPU |
| RAM | 8 GB | 16 GB |
| Disk | 20 GB free | 40 GB free |

The sandbox image is approximately 2.4 GB compressed. Systems with less than 8 GB RAM should configure swap to avoid OOM (Out of Memory) kills [1].

### 4.2 Software Requirements

| Software | Version | Notes |
|----------|---------|-------|
| Node.js | 22.16+ | Required for NemoClaw CLI |
| npm | 10+ | Package management |
| Docker | Latest stable | Primary container runtime |
| Colima | Latest | Alternative for macOS |
| Docker Desktop | Latest | Alternative for macOS/Windows |

### 4.3 Supported Platforms

| OS | Container Runtime | Status |
|----|-------------------|--------|
| **Linux** | Docker | Tested (primary) |
| **macOS (Apple Silicon)** | Colima, Docker Desktop | Tested with limitations |
| **DGX Spark** | Docker | Tested |
| **Windows WSL2** | Docker Desktop (WSL backend) | Tested with limitations |

### 4.4 Installation

NemoClaw is installed via a single command that runs as a normal user (no sudo/root required). The installer sets up Node.js via nvm and NemoClaw via npm [1]:

```bash
curl -fsSL https://raw.githubusercontent.com/NVIDIA/NemoClaw/main/install.sh | bash
```

After installation, the guided onboarding process creates the sandbox:

```bash
nemoclaw onboard
```

### 4.5 Key CLI Commands

| Command | Purpose |
|---------|---------|
| `nemoclaw onboard` | Create/recreate OpenShell gateway or sandbox |
| `nemoclaw status` | Check system status |

> **Important:** Avoid using `openshell self-update` or `openshell gateway start --recreate` directly. Always use the `nemoclaw` CLI as the primary interface [1].

---

## 5. Inference Configuration

### 5.1 Supported Inference Providers

NemoClaw supports multiple inference providers, all routed transparently through the OpenShell gateway [2]:

| Provider | Type | Notes |
|----------|------|-------|
| **NVIDIA Endpoints** | Cloud | NVIDIA's hosted inference service |
| **OpenAI** | Cloud | GPT-4, GPT-4o, etc. |
| **Anthropic** | Cloud | Claude models |
| **Google Gemini** | Cloud | Gemini models |
| **Ollama** | Local | Self-hosted open-source models |
| **Compatible Endpoints** | Any | Any OpenAI-compatible API |

### 5.2 Inference Routing Mechanism

The inference routing is completely transparent to the agent. Inside the sandbox, the agent makes API calls to `inference.local`, which is a virtual endpoint managed by OpenShell. The OpenShell gateway intercepts these calls and routes them to the configured provider with the correct credentials. The agent never sees the actual provider URL or API key [3].

This architecture provides several benefits. First, provider switching can be done without modifying the agent's code or configuration. Second, credentials are never exposed to the sandbox, even if the agent is compromised. Third, the operator can monitor and audit all inference requests at the gateway level. Fourth, failover between providers can be configured at the routing level [3].

### 5.3 Local Inference with Ollama

For privacy-sensitive deployments or offline operation, NemoClaw supports local inference through Ollama. When configured for local inference, all model requests are processed on the host machine without any data leaving the network. This is particularly useful for air-gapped environments or when processing sensitive data [2].

### 5.4 Switching Inference Providers

Switching between inference providers is a hot-reloadable operation — it can be done at runtime without restarting the sandbox. The operator updates the inference configuration, and the OpenShell gateway begins routing requests to the new provider immediately [2].

---

## 6. Network Policy Management

### 6.1 Default Network Policy

By default, NemoClaw blocks all outbound network connections from the sandbox. This "deny-all" default ensures that the agent cannot communicate with any external service unless explicitly approved. When the agent attempts to reach an unlisted host, the connection is blocked and the host is surfaced in the operator's TUI for review [2] [3].

### 6.2 Approving Network Requests

When the agent needs to access a new network destination, the operator sees a notification in the TUI showing the requested host, port, and the context of the request. The operator can then approve or deny the request. Approved hosts are added to the network policy, and subsequent requests to the same host are allowed automatically [2].

### 6.3 Customizing the Network Policy

For production deployments, operators can pre-configure the network policy to approve known-safe destinations:

```yaml
# Example network policy
egress:
  - host: "api.openai.com"
    port: 443
    protocol: tcp
    description: "OpenAI API"
  - host: "api.anthropic.com"
    port: 443
    protocol: tcp
    description: "Anthropic API"
  - host: "*.githubusercontent.com"
    port: 443
    protocol: tcp
    description: "GitHub raw content"
```

---

## 7. Channel Messaging

### 7.1 Supported Channels

NemoClaw supports connecting the sandboxed agent to messaging platforms through OpenShell-managed channel processes [2]:

| Channel | Status | Notes |
|---------|--------|-------|
| **Telegram** | Supported | Bot API integration |
| **Discord** | Supported | Bot API + Gateway |
| **Slack** | Supported | Bolt SDK integration |

### 7.2 Channel Architecture

Channel messaging in NemoClaw follows a specific architecture where the channel process runs on the host (outside the sandbox) and communicates with the sandboxed agent through the OpenShell gateway. This design ensures that channel credentials (bot tokens, API keys) never enter the sandbox [2].

---

## 8. State Management and Migration

### 8.1 State Migration

NemoClaw provides safe migration of agent state across machines. The state management system handles credential stripping (removing sensitive data before transfer), integrity verification (ensuring state has not been tampered with), and version compatibility (ensuring the target machine can accept the state format) [2] [3].

### 8.2 Blueprint Versioning

Blueprints are versioned artifacts that define the complete sandbox configuration. Each blueprint version is immutable and digest-verified, ensuring that the same blueprint always produces the same sandbox configuration. This reproducibility is critical for production deployments where consistency across environments is required [3].

---

## 9. Repository Structure

The NemoClaw repository is organized into the following directories [1]:

| Directory | Purpose |
|-----------|---------|
| `.agents/skills` | Agent skills |
| `.claude` | Claude-specific docs-as-skills |
| `agents/` | Agent configurations |
| `bin/` | CLI binaries and policy tools |
| `ci/` | CI/CD configurations |
| `docs/` | Documentation |
| `nemoclaw-blueprint/` | Hardened blueprint configurations |
| `nemoclaw/` | Core NemoClaw module |
| `schemas/` | JSON schemas for policy and configuration |
| `scripts/` | Installation and utility scripts |
| `src/` | TypeScript source code |
| `test/` | Test suites (uses Vitest) |

---

## 10. Documentation Structure

The official NVIDIA documentation for NemoClaw is organized into the following sections [2]:

| Section | Topics |
|---------|--------|
| **About NemoClaw** | Overview, How It Works, Ecosystem, Release Notes |
| **Get Started** | Prerequisites, Quickstart |
| **Inference** | Inference Options, Use Local Inference, Switch Inference Providers |
| **Network Policy** | Approve or Deny Network Requests, Customize the Network Policy |
| **Security** | Security Best Practices, Credential Storage, OpenClaw Controls |
| **Deployment** | Deploy to Remote GPU Instance, Set Up Telegram, Sandbox Hardening |
| **Workspace** | Workspace files section |

---

## References

[1]: [NVIDIA NemoClaw GitHub Repository](https://github.com/NVIDIA/NemoClaw)
[2]: [NVIDIA NemoClaw Official Documentation - Overview](https://docs.nvidia.com/nemoclaw/latest/about/overview.html)
[3]: [NVIDIA NemoClaw - How It Works](https://docs.nvidia.com/nemoclaw/latest/about/how-it-works.html)
