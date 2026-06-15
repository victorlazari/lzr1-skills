# OpenClaw Security Audit Procedures

## 1. Introduction to OpenClaw Security Architecture

OpenClaw, also widely known in the community as ZeroClaw, is an advanced open-source AI agent runtime designed for highly scalable, multi-channel, and multi-agent deployments. With native support for over 30 Large Language Model (LLM) providers and seamless integration across 14 distinct messaging channels, OpenClaw presents a uniquely complex attack surface that requires rigorous security auditing and continuous monitoring.

The core configuration for any OpenClaw deployment resides in the `openclaw.json` file. This file acts as the central nervous system for the runtime, dictating everything from API keys and provider preferences to channel routing rules and memory management settings. Because of its critical nature, securing `openclaw.json` and the surrounding architecture is the primary objective of any OpenClaw security audit.

This document outlines the comprehensive security audit procedures required to maintain a hardened OpenClaw environment. It is specifically tailored for production operations, focusing on worst-case scenarios, technical support workflows, and the mitigation of advanced persistent threats against the agent runtime. The procedures detailed herein cover channel policies, cross-context messaging controls, credential directory protection, workspace file safety, and the intricacies of multi-agent orchestration.

## 2. Channel Security Policies and Controls

OpenClaw's ability to interface with 14 different messaging channels is one of its most powerful features, but it also introduces significant risk. Each channel operates under different protocols and security paradigms. The primary channels include WhatsApp (utilizing the Baileys library), Signal (via signal-cli), and Telegram (using long polling mechanisms).

### 2.1 Channel Policy Configurations

Security auditors must verify that each active channel is configured with an appropriate access policy. OpenClaw supports four distinct channel policies:

*   **Open:** The channel accepts incoming messages from any user or number. This policy should strictly be limited to public-facing customer support bots and must be accompanied by aggressive rate limiting and input sanitization.
*   **Allowlist:** The channel only processes messages from explicitly approved identifiers (e.g., specific phone numbers or user IDs). This is the recommended policy for internal enterprise deployments.
*   **Pairing:** The channel requires a cryptographic handshake or a one-time password (OTP) exchange before a session is established. This is crucial for high-security environments where identity verification is paramount.
*   **Disabled:** The channel is completely deactivated at the runtime level, ignoring all incoming traffic.

### 2.2 Auditing Channel Implementations

When auditing specific channels, the following checks are mandatory:

*   **WhatsApp (Baileys):** Ensure that the Baileys session state is stored securely and encrypted at rest. The audit must verify that multi-device synchronization does not leak session keys to unauthorized nodes.
*   **Signal (signal-cli):** Verify that the `signal-cli` daemon is running with the principle of least privilege. The daemon should not run as root, and its UNIX socket permissions must be strictly controlled to prevent local privilege escalation.
*   **Telegram (Polling):** Confirm that the polling mechanism uses HTTPS exclusively and that the bot token is never hardcoded in scripts, but rather injected via secure environment variables or a secrets manager.

## 3. Cross-Context Messaging Controls

In a multi-agent environment, agents often need to communicate with one another or share context across different user sessions. This cross-context messaging introduces the risk of data leakage, where sensitive information from one user's session might inadvertently be exposed to another user or an unauthorized agent.

### 3.1 Enforcing Isolation

The security audit must rigorously test the boundaries of cross-context messaging. OpenClaw utilizes a strict context isolation protocol by default, but misconfigurations in `openclaw.json` can inadvertently bridge contexts.

Auditors must simulate scenarios where an agent attempts to access memory or session data outside its designated scope. The expected behavior is a hard denial, typically logged as a `cross-context messaging denied` error. If this error is not triggered during the simulation, the isolation controls are failing, and immediate remediation is required.

### 3.2 Validating Message Routing

All inter-agent communication must be routed through the central OpenClaw message broker. The audit must verify that:

1.  Messages contain cryptographic signatures verifying the sender agent's identity.
2.  The receiving agent explicitly authorizes the incoming message based on its configured trust matrix.
3.  Payloads are sanitized to prevent prompt injection attacks from one agent to another.

## 4. Credential Directory Protection

The credential directory is the most sensitive component of the OpenClaw filesystem. It houses API keys for the 30+ LLM providers, cryptographic keys for channel sessions (like the WhatsApp Baileys state), and database credentials.

### 4.1 Filesystem Permissions

The audit must confirm that the credential directory is locked down at the operating system level.

*   **Ownership:** The directory and all its contents must be owned by the specific user account running the OpenClaw daemon.
*   **Permissions:** Directory permissions must be set to `0700` (read, write, and execute only by the owner). File permissions within the directory must be set to `0600` (read and write only by the owner).

### 4.2 Encryption at Rest

Storing credentials in plaintext, even with strict filesystem permissions, is unacceptable in production environments. The audit must verify that OpenClaw is configured to use encryption at rest for the credential directory. This typically involves integrating with a Key Management Service (KMS) or utilizing a local hardware security module (HSM) to encrypt the `openclaw.json` secrets and session state files.

## 5. Workspace File Safety and Integrity

OpenClaw relies heavily on a set of standardized workspace files to define agent behavior, personality, and operational parameters. These files are parsed dynamically by the runtime, making them prime targets for manipulation.

### 5.1 The Core Workspace Files

The audit must cover the following critical workspace files:

*   **SOUL.md:** Defines the core ethical boundaries and immutable directives of the agent.
*   **IDENTITY.md:** Establishes the persona, tone, and background of the agent.
*   **USER.md:** Contains specific instructions or preferences related to the human user interacting with the agent.
*   **AGENTS.md:** Defines the topology and roles of other agents in a multi-agent setup.
*   **BOOT.md:** Contains initialization scripts and startup sequences.
*   **HEARTBEAT.md:** Defines recurring tasks, cron jobs, and background monitoring activities.
*   **MEMORY.md:** Outlines the rules for what information should be retained or discarded.
*   **TOOLS.md:** Lists the authorized extensions and skills the agent can invoke.

### 5.2 Integrity Monitoring

Because these files dictate the agent's behavior, unauthorized modifications can lead to catastrophic security breaches, such as an attacker altering `SOUL.md` to bypass safety filters or modifying `TOOLS.md` to execute malicious code.

The security audit must ensure that a File Integrity Monitoring (FIM) system is in place. The FIM must continuously hash the workspace files and alert administrators immediately if any unauthorized changes are detected. Furthermore, in high-security deployments, OpenClaw should be configured to refuse startup if the cryptographic signatures of the workspace files do not match the expected values.

## 6. Memory and Session Security

OpenClaw employs a sophisticated 3-layer memory architecture to maintain context and provide intelligent responses. Securing this memory stack is critical to protecting user privacy and preventing data exfiltration.

### 6.1 The 3-Layer Memory Architecture

1.  **Context Window:** The immediate, ephemeral memory held in RAM and sent to the LLM provider.
2.  **Workspace Files:** The persistent, behavioral memory defined in files like `MEMORY.md`.
3.  **Vector Database:** The long-term semantic memory, typically implemented using SQLite combined with Gemini embeddings for fast retrieval.

### 6.2 Auditing Memory Security

*   **Vector DB Protection:** The SQLite database file must be subjected to the same strict filesystem permissions as the credential directory. The audit must verify that SQL injection vulnerabilities are mitigated by ensuring OpenClaw uses parameterized queries exclusively when interacting with the database.
*   **Session Storage:** User sessions are stored as JSONL (JSON Lines) files. These files contain the raw transcripts of conversations. The audit must confirm that these JSONL files are encrypted at rest and that a strict data retention policy is enforced, automatically purging sessions older than a specified threshold.
*   **Embedding Security:** When using Gemini embeddings, the audit must verify that the API communication is secure and that sensitive PII (Personally Identifiable Information) is redacted *before* being sent to the embedding model, preventing accidental leakage to the LLM provider.

## 7. Extension and Skill Marketplace Security

OpenClaw's functionality can be expanded through custom TypeScript plugins (Extensions) and pre-packaged capabilities downloaded from the ClawdHub marketplace (Skills). This extensibility introduces significant supply chain risks.

### 7.1 Extension Sandboxing

Custom TypeScript extensions execute code directly within the OpenClaw runtime environment. The audit must verify that extensions are executed within a secure sandbox, such as a V8 isolate or a restricted Node.js `vm` module.

The sandbox must enforce strict limitations:
*   No access to the host filesystem outside of designated temporary directories.
*   No ability to spawn child processes.
*   Network access restricted to explicitly approved domains.

### 7.2 ClawdHub Skill Verification

Skills downloaded from the ClawdHub marketplace must be treated as untrusted third-party code. The audit procedure must include:

1.  **Signature Verification:** Ensuring that OpenClaw only installs skills that are cryptographically signed by trusted developers.
2.  **Static Analysis:** Running automated static analysis tools against the skill's source code to detect known vulnerabilities, hardcoded credentials, or malicious patterns before deployment.
3.  **Dependency Auditing:** Checking the skill's `package.json` for vulnerable dependencies using tools like `npm audit`.

## 8. Multi-Agent Orchestration Security

OpenClaw excels at multi-agent orchestration, utilizing background workers like Codex, Claude Code, and Pi to handle complex, asynchronous tasks. This distributed architecture requires robust security controls to prevent rogue agents from compromising the system.

### 8.1 Worker Authentication and Authorization

The audit must verify that background workers authenticate securely with the main OpenClaw orchestrator. This should involve mutual TLS (mTLS) or robust JWT-based authentication.

Furthermore, authorization must be strictly enforced. A worker agent designed for data analysis (e.g., using Claude Code) should not have the authorization to send messages via the WhatsApp channel. The audit must review the `AGENTS.md` file and the corresponding runtime configurations to ensure the principle of least privilege is applied to all background workers.

### 8.2 Orchestration Monitoring

The orchestrator must maintain a comprehensive audit log of all tasks assigned to and completed by background workers. The security audit should verify that these logs are immutable and forwarded to a centralized SIEM (Security Information and Event Management) system for real-time anomaly detection.

## 9. Known Security Errors and Troubleshooting

Technical support and security operations teams must be intimately familiar with OpenClaw's known error states, as these often indicate underlying security issues or active attacks.

### 9.1 Common Error States and Remediation

| Error Code / Message | Typical Cause | Security Implication | Remediation Steps |
| :--- | :--- | :--- | :--- |
| **WhatsApp 408 Timeouts** | Network instability or Baileys session corruption. | Potential denial of service or session hijacking attempt. | Force a session reset, rotate Baileys cryptographic keys, and verify network integrity. |
| **Signal RPC Failures** | `signal-cli` daemon crashed or socket permissions altered. | Loss of secure communication channel; potential local privilege escalation. | Restart daemon, audit UNIX socket permissions, check system logs for unauthorized access attempts. |
| **Cross-Context Messaging Denied** | Agent attempted to access unauthorized memory or session data. | Active attempt at data exfiltration or misconfiguration in `openclaw.json`. | Immediately isolate the offending agent, review `AGENTS.md` trust matrix, and audit recent configuration changes. |
| **Telegram getUpdates Timeout** | Telegram API rate limiting or network blocking. | Denial of service; potential indicator of a volumetric attack against the bot. | Implement exponential backoff, verify bot token hasn't been leaked, and check firewall rules. |

## 10. Worst-Case Scenarios and Incident Response

A comprehensive security audit must prepare the organization for worst-case scenarios. The following incident response protocols must be documented and tested regularly.

### 10.1 Scenario: `openclaw.json` Compromise

If the central configuration file is compromised, the attacker gains full control over the runtime, including all API keys and channel sessions.

**Response Protocol:**
1.  **Immediate Isolation:** Disconnect the OpenClaw server from the network immediately.
2.  **Credential Revocation:** Revoke all 30+ LLM provider API keys and channel bot tokens simultaneously.
3.  **Session Termination:** Force-close all active user sessions across all 14 channels.
4.  **Forensic Analysis:** Image the server for forensic analysis to determine the vector of compromise.
5.  **Rebuild and Restore:** Rebuild the server from a known good state, generate new credentials, and restore configurations from secure backups.

### 10.2 Scenario: Malicious Skill Execution

If a malicious skill bypasses ClawdHub verification and is executed within the runtime, it could attempt to exfiltrate data or establish a reverse shell.

**Response Protocol:**
1.  **Skill Deactivation:** Immediately disable the offending skill via the OpenClaw CLI or by modifying `TOOLS.md`.
2.  **Sandbox Review:** Analyze the sandbox logs to determine the extent of the skill's activities. Did it attempt network connections? Did it try to access the filesystem?
3.  **Memory Purge:** If the skill interacted with the vector database or session JSONL files, those data stores must be considered compromised and potentially rolled back to a previous snapshot.
4.  **Vulnerability Disclosure:** Report the malicious skill to the ClawdHub maintainers immediately to protect the wider community.

## 11. Conclusion

Securing an OpenClaw deployment is an ongoing process that requires vigilance, deep technical understanding of the architecture, and a proactive approach to threat modeling. By rigorously adhering to the audit procedures outlined in this document—focusing on channel policies, cross-context isolation, workspace integrity, and multi-agent orchestration—organizations can harness the immense power of ZeroClaw while mitigating the substantial risks associated with advanced AI agent runtimes. Regular audits, coupled with automated monitoring and robust incident response plans, are the cornerstone of a secure OpenClaw ecosystem.
