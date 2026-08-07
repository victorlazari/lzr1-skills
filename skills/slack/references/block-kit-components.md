# Block Kit Components for Agent Experiences

Verified against upstream: 2026-08-07

This reference covers the new Block Kit components designed to transform agent responses from static text into structured, interactive interfaces.

## 1. Card Block

The Card block provides structured, scannable context with optional icons, titles, hero images, and action buttons.

```json
{
  "type": "card",
  "title": {
    "type": "plain_text",
    "text": "Project Status Update"
  },
  "text": {
    "type": "mrkdwn",
    "text": "The latest deployment was successful."
  },
  "image_url": "https://example.com/hero.png",
  "alt_text": "Hero image",
  "actions": [
    {
      "type": "button",
      "text": {
        "type": "plain_text",
        "text": "View Details"
      },
      "value": "view_details"
    }
  ]
}
```

## 2. Alert Block

The Alert block introduces visual severity (Default, Info, Success, Warning, Error) to communicate urgency clearly.

```json
{
  "type": "alert",
  "style": "error",
  "title": {
    "type": "plain_text",
    "text": "Critical System Failure"
  },
  "text": {
    "type": "mrkdwn",
    "text": "The database connection has been lost."
  }
}
```

## 3. Carousel Block

The Carousel block allows grouping up to 10 Cards into a horizontal, scrollable layout.

```json
{
  "type": "carousel",
  "elements": [
    {
      "type": "card",
      "title": {
        "type": "plain_text",
        "text": "Card 1"
      },
      "text": {
        "type": "mrkdwn",
        "text": "Content for card 1."
      }
    },
    {
      "type": "card",
      "title": {
        "type": "plain_text",
        "text": "Card 2"
      },
      "text": {
        "type": "mrkdwn",
        "text": "Content for card 2."
      }
    }
  ]
}
```

## 4. Data Table Block

The Data Table block enables rendering structured, tabular data directly in Slack.

```json
{
  "type": "data_table",
  "headers": [
    {"type": "plain_text", "text": "Name"},
    {"type": "plain_text", "text": "Role"}
  ],
  "rows": [
    [
      {"type": "plain_text", "text": "Alice"},
      {"type": "plain_text", "text": "Engineer"}
    ],
    [
      {"type": "plain_text", "text": "Bob"},
      {"type": "plain_text", "text": "Designer"}
    ]
  ]
}
```

## 5. Work Object Block

The Work Object block is used to represent a specific entity or task within a workflow.

```json
{
  "type": "work_object",
  "title": {
    "type": "plain_text",
    "text": "Task-1234"
  },
  "status": "In Progress",
  "assignee": "U12345678"
}
```

## 6. Code Block

The Code block is used to display code snippets with syntax highlighting.

```json
{
  "type": "code",
  "language": "python",
  "code": "def hello_world():\n    print('Hello, World!')"
}
```
