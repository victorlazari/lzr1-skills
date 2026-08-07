# OpenClaw and ZeroClaw Complete Reference Guide

**Verified against upstream:** 2026-08-07

This document serves as the definitive reference for OpenClaw (Node.js) and ZeroClaw (Rust) architectures, operations, and troubleshooting. It distinguishes between the two runtimes, which have fundamentally different designs and configuration models.

## 1. OpenClaw (Node.js) Architecture & Configuration

OpenClaw is a TypeScript/Node.js-based AI assistant runtime that connects models, tools, and messaging channels through a Gateway.

### 1.1 Workspace Bootstrap Files

OpenClaw relies on a workspace directory containing specific Markdown files that define the agent's persona, topology, and initialization parameters. These files are treated as code and should be version-controlled.

-   **`AGENTS.md`**: Defines the topology of the multi-agent network and communication protocols.
-   **`SOUL.md`**: Core ethical boundaries, immutable directives, and fundamental purpose.
-   **`IDENTITY.md`**: Persona, tone of voice, and background story.
-   **`USER.md`**: Persistent user preferences and historical context.
-   **`BOOTSTRAP.md`**: Initialization instructions and startup parameters.
-   **`MEMORY.md`**: Scratchpad for short-term memory consolidation.

### 1.2 Session State (SQLite)

OpenClaw stores active session state and historical interactions in a local SQLite database, typically located at `~/.openclaw/state/openclaw.sqlite`.

-   **Integrity:** The database must be maintained to prevent corruption.
-   **Validation:** Use the SQLite CLI to verify integrity: `sqlite3 ~/.openclaw/state/openclaw.sqlite "PRAGMA integrity_check;"`

### 1.3 Validation Command

-   **`openclaw setup`**: Validates the workspace initialization and ensures all required bootstrap files are present and correctly formatted.

## 2. ZeroClaw (Rust) Architecture & Configuration

ZeroClaw is a separate, lightweight Rust-based alternative runtime. It employs a trait-based architecture and is designed for high performance and minimal resource overhead.

### 2.1 Configuration (`config.toml`)

ZeroClaw uses a single TOML configuration file (`config.toml`) to manage all settings, including LLM providers, routing, and system parameters.

-   **Format:** TOML (Tom's Obvious, Minimal Language).
-   **Management:** Ensure strict syntax adherence when modifying this file.

### 2.2 Validation Command

-   **`zeroclaw doctor`**: A built-in diagnostic tool that validates the `config.toml` file, checks dependencies, and reports on the overall health of the ZeroClaw environment.

## 3. Troubleshooting and Operations

### 3.1 OpenClaw Troubleshooting

-   **Workspace Errors:** If `openclaw setup` fails, verify that all required `.md` files exist in the workspace directory and contain valid Markdown.
-   **State Corruption:** If the SQLite integrity check fails, the database may be corrupted. Attempt to restore from a known good backup. Avoid manual editing of the SQLite database unless strictly necessary.

### 3.2 ZeroClaw Troubleshooting

-   **Configuration Errors:** If `zeroclaw doctor` reports errors, carefully review `config.toml` for syntax mistakes or invalid values. Use a TOML linter if available.
-   **Dependency Issues:** Ensure all required system libraries for the Rust runtime are installed.

## 4. Authoritative Sources

Always consult the official documentation for the most current information regarding supported versions, configuration schemas, and CLI flags.

-   **OpenClaw GitHub Repository:** https://github.com/openclaw/openclaw
-   **OpenClaw Agent Runtime Documentation:** https://docs.openclaw.ai/concepts/agent
-   **ZeroClaw GitHub Repository:** https://github.com/zeroclaw-labs/zeroclaw
-   **ZeroClaw Official Website:** https://zeroclaw.net/
