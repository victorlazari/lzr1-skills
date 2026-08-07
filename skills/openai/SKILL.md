---
name: openai
description: Specialist in OpenAI API, Responses API, Realtime API, function calling, structured outputs, and current models (gpt-5.6, gpt-5.4).
---

# OpenAI Specialist Skill

## When to Use

Use this skill when you need to:
- Interact with the OpenAI API for text generation, summarization, or chat completions using current models (e.g., `gpt-5.6`, `gpt-5.4`).
- Build intelligent conversational agents using the new Responses API with persistent state and custom personas.
- Implement function calling (tool calling) to allow language models to interact dynamically with external systems and APIs.
- Enforce structured outputs (e.g., JSON) for reliable and predictable model responses using `strict: true`.
- Implement low-latency voice or audio sessions using the Realtime API.
- Manage large numbers of tools using the `tool_search` feature.
- Authenticate securely using workload identity federation for short-lived access tokens.

## Preconditions

- **API Key**: Ensure a valid OpenAI API key is available in the environment (`OPENAI_API_KEY`).
- **Model Version**: Verify the target model is current (e.g., `gpt-5.6`, `gpt-5.4`).
- **API Version**: Ensure the application uses the Responses API (`client.responses.create`) instead of the deprecated Assistants API (`client.beta.assistants`).

## Source Freshness

- **Volatile Facts**: Model versions, pricing, rate limits, and specific API endpoints may change.
- **Verification**: Always verify current details via the official OpenAI documentation URLs (e.g., https://developers.openai.com/api/reference/overview/) at runtime before applying destructive or production-impacting actions.
- **Verified Date**: The current package was verified against upstream on 2026-08-07.

## Workflow

1. **Requirement Analysis**: Determine the specific OpenAI capability needed (e.g., Responses API, Realtime API, standard completions).
2. **Model Selection**: Choose the appropriate current model (e.g., `gpt-5.6`, `gpt-5.4`) based on the task requirements.
3. **Implementation**: Use the Responses API for stateful interactions and tool use, ensuring `strict: true` is used for Structured Outputs.
4. **Validation**: Run syntax checks on any generated code and verify that no deprecated APIs (like Assistants API) are used.
5. **Execution**: Execute the API calls, handling any rate limits or errors gracefully. Require confirmation before executing scripts that incur API costs.
6. **Stop Condition**: The task is complete when the API returns the expected structured output or completion without errors.

## Safety

- **Read-Only Discovery**: Separate read-only discovery from mutations.
- **Confirmation Required**: Require confirmation for destructive, external, privileged, financial, legal, or production-impacting actions (e.g., executing scripts that incur API costs).
- **Untrusted Artifacts**: Do not download or execute untrusted artifacts.

## Validation

- **Syntax Checks**: Run safe local syntax checks on generated code (`bash -n`, Python compilation, JSON/YAML parsing).
- **API Checks**: Verify no usage of `client.beta.assistants` in any code or documentation. Ensure all tool calling examples use the `client.responses.create` endpoint. Validate that `strict: true` is included in function schemas where appropriate. Check that model names in examples reflect current versions (e.g., `gpt-5.6`).

## Failure Handling

- **Diagnosis**: Diagnose errors using API response codes and error messages.
- **Alternatives**: Choose alternative models or approaches if the primary method fails.
- **Rollback**: Roll back any partial changes if a multi-step process fails.
- **Avoid Repetition**: Do not repeat a failed action unchanged.

## Output Contract

- **Structure**: The result must be a structured output (e.g., JSON) conforming to the requested schema.
- **Evidence**: Include evidence of successful API calls or validation checks.
- **Actionable Next Steps**: Provide actionable next steps based on the API response.

## Resources

- [Responses API Guide](references/responses-api-guide.md): Detailed guide on using the new Responses API for stateful interactions and tool use.
- [Tool Calling Reference](references/tool-calling-reference.md): Focused reference on function calling, Structured Outputs (`strict: true`), and `tool_search`.
- [Realtime API Guide](references/realtime-api-guide.md): Guide on using the Realtime API for low-latency voice/audio sessions.
- [Responses API Example](templates/responses-api-example.py): Executable Python template demonstrating the Responses API tool calling loop.

## Orchestration

- **Parallel Work**: Use parallel work only for independent dimensions.
- **Synthesis**: Define inputs, schemas, conflict handling, synthesis, and termination conditions for parallel tasks.
