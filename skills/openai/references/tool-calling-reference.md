# Tool Calling Reference

**Verified against upstream: 2026-08-07**

## Introduction

Tool calling (formerly function calling) allows language models to interact dynamically with external systems and APIs. This reference covers the implementation of tool calling using the Responses API, focusing on Structured Outputs and `tool_search`.

## Structured Outputs (`strict: true`)

To ensure reliable and predictable model responses, use the `strict: true` parameter in your function schemas. This enforces the model to output data that strictly adheres to the defined JSON schema.

### Example Schema

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g. San Francisco, CA"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"],
      "additionalProperties": false
    },
    "strict": true
  }
}
```

## Handling Large Schemas (`tool_search`)

When dealing with a large number of tools, use the `tool_search` feature to allow the model to efficiently find and select the appropriate tool based on the user's query.

## Implementation Flow

1. **Define Tools**: Create JSON schemas for your tools, ensuring `strict: true` is set for structured outputs.
2. **Invoke API**: Call `client.responses.create` with the `tools` parameter.
3. **Handle Response**: Check if the model returned a `tool_calls` array.
4. **Execute Tools**: Execute the requested tools locally.
5. **Submit Results**: Append the tool results to the conversation history and call the API again to get the final response.

## References

- [OpenAI API Documentation: Function Calling](https://developers.openai.com/api/docs/guides/function-calling)
