# NemoClaw Complete Reference

Verified against upstream: 2026-08-07

## 1. Supported Environments

NemoClaw can be deployed on the following environments:
- DGX Spark
- DGX Station
- Windows WSL
- Linux/macOS

## 2. Supported Agents

NemoClaw supports the following agents:
- OpenClaw
- Hermes
- LangChain Deep Agents Code

## 3. Supported Inference Providers

NemoClaw supports the following inference providers:
- vLLM
- Ollama
- NVIDIA Endpoints
- OpenRouter
- OpenAI
- Anthropic
- Gemini

## 4. Guided Onboarding

The guided onboarding process uses an interactive terminal installer to configure the sandbox, select the agent, and set up the inference provider.

## 5. Secure Credential Handling

Credentials must be handled securely using the local helper script and form. They should never be exposed in configuration files.

### 5.1 Local Credential Helper Script
The `local-credential-helper.mts` script provides a secure mechanism for managing credentials locally.

### 5.2 Local Credential Form
The `local-credential-form.html` provides a user interface for securely inputting credentials.
