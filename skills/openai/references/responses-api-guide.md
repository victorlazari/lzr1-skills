# Responses API Guide

**Verified against upstream: 2026-08-07**

## Introduction

The Responses API is the primary method for stateful interactions, tool use, and multi-modal inputs in the OpenAI API. It replaces the deprecated Assistants API (which shuts down on August 26, 2026).

## Key Concepts

- **Stateful Interactions**: The Responses API maintains conversation history automatically, reducing client-side complexity.
- **Tool Use**: Seamlessly integrate function calling (tool calling) with structured outputs.
- **Multi-Modal Inputs**: Support for text, vision, and other modalities.

## Migration from Assistants API

- **Endpoint**: Replace `client.beta.assistants` with `client.responses.create`.
- **Models**: Update model references to a current model from the provider's model list (pick the tier that fits the task: flagship, balanced, or small and fast).
- **Authentication**: Utilize workload identity federation for short-lived access tokens where applicable.

## Basic Usage

```python
import os
import openai

# Pick from the provider's current model list; do not hard-code a stale id.
MODEL = os.environ.get("OPENAI_MODEL", "<set-a-current-model-id>")

client = openai.OpenAI()

response = client.responses.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

## Advanced Features

- **Structured Outputs**: Use `strict: true` in function schemas to enforce structured outputs.
- **Tool Search**: Use `tool_search` for handling large numbers of tools efficiently.

## References

- [OpenAI API Reference](https://developers.openai.com/api/reference/overview/)
