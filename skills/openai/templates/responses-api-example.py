#!/usr/bin/env python3
"""
Responses API Example

This script demonstrates the Responses API tool calling loop, including
Structured Outputs (`strict: True`).

Usage:
    python3 responses-api-example.py
"""

import os
import json
import sys

# Ensure OPENAI_API_KEY is set
if "OPENAI_API_KEY" not in os.environ:
    print("Error: OPENAI_API_KEY environment variable not set.", file=sys.stderr)
    sys.exit(1)

# Mock implementation for demonstration purposes
# In a real scenario, this would use the official openai python package
def mock_responses_create(model, messages, tools):
    print(f"Calling API with model: {model}")
    print(f"Messages: {json.dumps(messages, indent=2)}")
    print(f"Tools: {json.dumps(tools, indent=2)}")

    # Simulate a tool call response
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": None,
                    "tool_calls": [
                        {
                            "id": "call_123",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": '{"location": "San Francisco, CA"}'
                            }
                        }
                    ]
                }
            }
        ]
    }

def main():
    tools = [
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
                        }
                    },
                    "required": ["location"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    ]

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather like in San Francisco?"}
    ]

    print("Initiating Responses API call...")
    response = mock_responses_create(
        model="gpt-5.6",
        messages=messages,
        tools=tools
    )

    message = response["choices"][0]["message"]

    if message.get("tool_calls"):
        print("\nModel requested tool calls:")
        for tool_call in message["tool_calls"]:
            print(f"  Tool: {tool_call['function']['name']}")
            print(f"  Arguments: {tool_call['function']['arguments']}")

            # Here you would execute the tool and append the result to messages
            # messages.append(message)
            # messages.append({
            #     "role": "tool",
            #     "tool_call_id": tool_call["id"],
            #     "content": '{"temperature": 72, "condition": "Sunny"}'
            # })
            # Then call the API again
    else:
        print("\nModel response:")
        print(message.get("content"))

if __name__ == "__main__":
    main()
