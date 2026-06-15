# Specialist: 50-slack

## === FILE: 50-slack-advanced.md ===
# Slack Master Specialist — Advanced Patterns

## 1. Advanced Block Kit Composition

### Dynamic Block Generation

Building blocks programmatically based on data allows for complex, data-driven UIs:

```python
def build_deployment_dashboard(deployments):
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": ":rocket: Deployment Dashboard"}},
        {"type": "divider"}
    ]
    
    for deploy in deployments:
        status_emoji = {
            "running": ":large_blue_circle:",
            "success": ":white_check_mark:",
            "failed": ":x:",
            "pending": ":hourglass:"
        }.get(deploy["status"], ":grey_question:")
        
        blocks.append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"{status_emoji} *{deploy['service']}* `{deploy['version']}`\nEnvironment: `{deploy['env']}` | Duration: {deploy['duration']}s"},
            "accessory": {
                "type": "overflow",
                "action_id": f"deploy_actions_{deploy['id']}",
                "options": [
                    {"text": {"type": "plain_text", "text": ":arrow_right: View Logs"}, "value": f"logs_{deploy['id']}"},
                    {"text": {"type": "plain_text", "text": ":rewind: Rollback"}, "value": f"rollback_{deploy['id']}"},
                    {"text": {"type": "plain_text", "text": ":mag: Details"}, "value": f"details_{deploy['id']}"}
                ]
            }
        })
    
    # Add summary context
    total = len(deployments)
    success = sum(1 for d in deployments if d["status"] == "success")
    failed = sum(1 for d in deployments if d["status"] == "failed")
    
    blocks.append({"type": "divider"})
    blocks.append({
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": f"Total: {total} | :white_check_mark: {success} | :x: {failed} | Last updated: <!date^{int(time.time())}^{{date_short}} {{time}}|now>"}]
    })
    
    return blocks
```

### Multi-Step Modal Workflows

```python
# Step 1: Initial form
@app.command("/onboard")
def start_onboard(ack, command, client):
    ack()
    client.views_open(
        trigger_id=command["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "onboard_step1",
            "title": {"type": "plain_text", "text": "New Team Member"},
            "submit": {"type": "plain_text", "text": "Next"},
            "blocks": [
                {"type": "input", "block_id": "name", "label": {"type": "plain_text", "text": "Full Name"}, "element": {"type": "plain_text_input", "action_id": "name_input"}},
                {"type": "input", "block_id": "role", "label": {"type": "plain_text", "text": "Role"}, "element": {"type": "static_select", "action_id": "role_select", "options": [
                    {"text": {"type": "plain_text", "text": "Engineer"}, "value": "engineer"},
                    {"text": {"type": "plain_text", "text": "Designer"}, "value": "designer"},
                    {"text": {"type": "plain_text", "text": "Product Manager"}, "value": "pm"}
                ]}},
                {"type": "input", "block_id": "team", "label": {"type": "plain_text", "text": "Team"}, "element": {"type": "external_select", "action_id": "team_select", "min_query_length": 0}}
            ]
        }
    )

# Step 2: Additional details based on role
@app.view("onboard_step1")
def handle_step1(ack, body, client, view):
    values = view["state"]["values"]
    name = values["name"]["name_input"]["value"]
    role = values["role"]["role_select"]["selected_option"]["value"]
    
    # Build step 2 based on role
    role_blocks = []
    if role == "engineer":
        role_blocks = [
            {"type": "input", "block_id": "github", "label": {"type": "plain_text", "text": "GitHub Username"}, "element": {"type": "plain_text_input", "action_id": "github_input"}},
            {"type": "input", "block_id": "languages", "label": {"type": "plain_text", "text": "Languages"}, "element": {"type": "multi_static_select", "action_id": "lang_select", "options": [
                {"text": {"type": "plain_text", "text": "Go"}, "value": "go"},
                {"text": {"type": "plain_text", "text": "Python"}, "value": "python"},
                {"text": {"type": "plain_text", "text": "TypeScript"}, "value": "typescript"},
                {"text": {"type": "plain_text", "text": "Rust"}, "value": "rust"}
            ]}}
        ]
    
    ack(response_action="update", view={
        "type": "modal",
        "callback_id": "onboard_step2",
        "private_metadata": json.dumps({"name": name, "role": role}),
        "title": {"type": "plain_text", "text": "Details"},
        "submit": {"type": "plain_text", "text": "Complete"},
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": f"Setting up *{name}* as *{role}*"}},
            {"type": "divider"}
        ] + role_blocks
    })
```

### Conditional Block Rendering

```python
def build_alert_message(alert):
    blocks = [
        {"type": "section", "text": {"type": "mrkdwn", "text": f":warning: *Alert: {alert['title']}*\n{alert['description']}"}}
    ]
    
    # Add graph image if available
    if alert.get("graph_url"):
        blocks.append({"type": "image", "image_url": alert["graph_url"], "alt_text": f"Graph for {alert['title']}"})
    
    # Add runbook link if exists
    if alert.get("runbook_url"):
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": f":book: <{alert['runbook_url']}|View Runbook>"}})
    
    # Add action buttons based on alert type
    actions = []
    if alert["type"] == "infrastructure":
        actions.extend([
            {"type": "button", "text": {"type": "plain_text", "text": "Scale Up"}, "action_id": "scale_up", "value": alert["resource_id"]},
            {"type": "button", "text": {"type": "plain_text", "text": "Restart"}, "action_id": "restart", "style": "danger", "value": alert["resource_id"], "confirm": {
                "title": {"type": "plain_text", "text": "Confirm Restart"},
                "text": {"type": "mrkdwn", "text": f"Are you sure you want to restart `{alert['resource_id']}`?"},
                "confirm": {"type": "plain_text", "text": "Restart"},
                "deny": {"type": "plain_text", "text": "Cancel"}
            }}
        ])
    
    if actions:
        blocks.append({"type": "actions", "elements": actions})
    
    return blocks
```

## 2. App Home Tab

The App Home provides a personalized dashboard for each user:

```python
@app.event("app_home_opened")
def update_home_tab(client, event):
    user_id = event["user"]
    
    # Fetch user-specific data
    user_tasks = get_user_tasks(user_id)
    user_prs = get_user_open_prs(user_id)
    oncall_status = get_oncall_status(user_id)
    
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": ":house: Your Dashboard"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": f"Welcome back, <@{user_id}>! Here's your overview."}}
    ]
    
    # On-call status
    if oncall_status["is_oncall"]:
        blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": f":pager: *You are currently on-call*\nShift ends: <!date^{oncall_status['end_ts']}^{{date_long}} {{time}}|soon>"}})
    
    # Open PRs
    if user_prs:
        blocks.append({"type": "divider"})
        blocks.append({"type": "header", "text": {"type": "plain_text", "text": ":git-pull-request: Your Open PRs"}})
        for pr in user_prs[:5]:
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": f"<{pr['url']}|#{pr['number']} {pr['title']}> — {pr['reviews']} reviews, {pr['age']} days old"}})
    
    # Tasks
    if user_tasks:
        blocks.append({"type": "divider"})
        blocks.append({"type": "header", "text": {"type": "plain_text", "text": ":clipboard: Your Tasks"}})
        for task in user_tasks[:5]:
            checkbox = ":white_check_mark:" if task["done"] else ":white_large_square:"
            blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": f"{checkbox} {task['title']}"}})
    
    # Quick actions
    blocks.append({"type": "divider"})
    blocks.append({"type": "actions", "elements": [
        {"type": "button", "text": {"type": "plain_text", "text": ":heavy_plus_sign: New Task"}, "action_id": "new_task"},
        {"type": "button", "text": {"type": "plain_text", "text": ":calendar: Schedule Meeting"}, "action_id": "schedule_meeting"},
        {"type": "button", "text": {"type": "plain_text", "text": ":mag: Search Docs"}, "action_id": "search_docs"}
    ]})
    
    client.views_publish(user_id=user_id, view={"type": "home", "blocks": blocks})
```

## 3. Advanced Incoming Webhooks

### Webhook with Full Block Kit

```python
import requests

WEBHOOK_URL = "https://hooks.slack.com/services/YOUR_T/YOUR_B/YOUR_TOKEN"

def send_build_notification(build):
    status_map = {
        "success": (":white_check_mark:", "#36a64f"),
        "failure": (":x:", "#dc3545"),
        "running": (":arrows_counterclockwise:", "#ffc107")
    }
    emoji, color = status_map.get(build["status"], (":grey_question:", "#6c757d"))
    
    payload = {
        "blocks": [
            {"type": "header", "text": {"type": "plain_text", "text": f"{emoji} Build #{build['number']} — {build['status'].title()}"}},
            {"type": "section", "fields": [
                {"type": "mrkdwn", "text": f"*Repository:*\n`{build['repo']}`"},
                {"type": "mrkdwn", "text": f"*Branch:*\n`{build['branch']}`"},
                {"type": "mrkdwn", "text": f"*Commit:*\n`{build['commit'][:7]}`"},
                {"type": "mrkdwn", "text": f"*Duration:*\n{build['duration']}s"},
                {"type": "mrkdwn", "text": f"*Triggered by:*\n{build['author']}"},
                {"type": "mrkdwn", "text": f"*Tests:*\n{build['tests_passed']}/{build['tests_total']} passed"}
            ]},
            {"type": "context", "elements": [
                {"type": "mrkdwn", "text": f"Pipeline: {build['pipeline']} | Stage: {build['stage']}"}
            ]}
        ]
    }
    
    if build["status"] == "failure" and build.get("error_log"):
        payload["blocks"].append({
            "type": "section",
            "text": {"type": "mrkdwn", "text": f"*Error:*\n```{build['error_log'][:2000]}```"}
        })
    
    response = requests.post(WEBHOOK_URL, json=payload)
    return response.status_code == 200
```

## 4. Rate Limiting Strategy

### Tier-Based Rate Limits

| Tier | Rate | Methods |
|------|------|---------|
| Tier 1 | 1 req/min | `admin.*`, `migration.*` |
| Tier 2 | 20 req/min | `channels.list`, `users.list` |
| Tier 3 | 50 req/min | `chat.postMessage`, `reactions.add` |
| Tier 4 | 100 req/min | `auth.test`, `conversations.info` |
| Special | 1 req/sec/channel | `chat.postMessage` per channel |

### Token Bucket Implementation

```python
import time
import threading

class SlackRateLimiter:
    def __init__(self):
        self.locks = {}
        self.tokens = {}
        self.last_refill = {}
        self.tier_limits = {
            1: (1, 60),    # 1 token, refill every 60s
            2: (20, 60),   # 20 tokens, refill every 60s
            3: (50, 60),   # 50 tokens, refill every 60s
            4: (100, 60),  # 100 tokens, refill every 60s
        }
    
    def _get_tier(self, method):
        tier_map = {
            "chat.postMessage": 3,
            "chat.update": 3,
            "reactions.add": 3,
            "conversations.list": 2,
            "users.list": 2,
            "conversations.info": 4,
            "auth.test": 4,
        }
        return tier_map.get(method, 3)
    
    def acquire(self, method):
        tier = self._get_tier(method)
        max_tokens, refill_interval = self.tier_limits[tier]
        
        if method not in self.locks:
            self.locks[method] = threading.Lock()
            self.tokens[method] = max_tokens
            self.last_refill[method] = time.time()
        
        with self.locks[method]:
            # Refill tokens
            now = time.time()
            elapsed = now - self.last_refill[method]
            refill_amount = int(elapsed / refill_interval * max_tokens)
            if refill_amount > 0:
                self.tokens[method] = min(max_tokens, self.tokens[method] + refill_amount)
                self.last_refill[method] = now
            
            if self.tokens[method] > 0:
                self.tokens[method] -= 1
                return True
            else:
                # Calculate wait time
                wait = refill_interval / max_tokens
                time.sleep(wait)
                return True

rate_limiter = SlackRateLimiter()
```

## 5. Slash Command Response Patterns

### Ephemeral vs In-Channel Responses

```python
@app.command("/status")
def handle_status(ack, command, respond):
    ack()
    
    # Ephemeral (only visible to the user who triggered it)
    respond(
        response_type="ephemeral",
        text="Checking status...",
        replace_original=False
    )
    
    # Fetch actual status
    status = get_system_status()
    
    # In-channel (visible to everyone)
    respond(
        response_type="in_channel",
        replace_original=True,
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": f":green_circle: All systems operational\nLast check: <!date^{int(time.time())}^{{time}}|now>"}}
        ]
    )
```

### Delayed Responses (response_url)

The `response_url` is valid for 30 minutes and allows up to 5 responses:

```python
import requests

@app.command("/deploy")
def handle_deploy(ack, command, respond):
    ack()
    response_url = command["response_url"]
    
    # Immediate acknowledgment
    respond(response_type="ephemeral", text=":hourglass: Starting deployment...")
    
    # Start async deployment
    threading.Thread(target=run_deployment, args=(command, response_url)).start()

def run_deployment(command, response_url):
    # ... long-running deployment ...
    
    # Send delayed response
    requests.post(response_url, json={
        "response_type": "in_channel",
        "replace_original": True,
        "blocks": [
            {"type": "section", "text": {"type": "mrkdwn", "text": ":white_check_mark: Deployment complete!"}}
        ]
    })
```

## 6. External Data Sources for Select Menus

```python
@app.options("team_select")
def handle_team_options(ack, body):
    query = body.get("value", "")
    
    teams = fetch_teams_from_api(query)
    
    options = [
        {"text": {"type": "plain_text", "text": team["name"]}, "value": team["id"]}
        for team in teams
        if query.lower() in team["name"].lower()
    ][:100]  # Max 100 options
    
    ack(options=options)
```

## 7. Message Update Patterns

### Progressive Updates (Long-Running Operations)

```python
async def deploy_with_progress(client, channel, service, version):
    # Initial message
    msg = await client.chat_postMessage(
        channel=channel,
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": f":hourglass: *Deploying {service} {version}*\n\n:white_circle: Building image\n:white_circle: Pushing to registry\n:white_circle: Updating pods\n:white_circle: Health check"}}
        ]
    )
    ts = msg["ts"]
    
    steps = ["Building image", "Pushing to registry", "Updating pods", "Health check"]
    
    for i, step in enumerate(steps):
        await asyncio.sleep(5)  # Simulate work
        
        progress_lines = []
        for j, s in enumerate(steps):
            if j < i:
                progress_lines.append(f":white_check_mark: ~~{s}~~")
            elif j == i:
                progress_lines.append(f":arrows_counterclockwise: *{s}*")
            else:
                progress_lines.append(f":white_circle: {s}")
        
        await client.chat_update(
            channel=channel,
            ts=ts,
            blocks=[
                {"type": "section", "text": {"type": "mrkdwn", "text": f":rocket: *Deploying {service} {version}*\n\n" + "\n".join(progress_lines)}}
            ]
        )
    
    # Final success
    await client.chat_update(
        channel=channel,
        ts=ts,
        blocks=[
            {"type": "section", "text": {"type": "mrkdwn", "text": f":white_check_mark: *{service} {version} deployed successfully!*\n\n" + "\n".join([f":white_check_mark: ~~{s}~~" for s in steps])}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": f"Completed in 20s | <!date^{int(time.time())}^{{date_short}} {{time}}|now>"}]}
        ]
    )
```

## 8. Conversation Store Pattern

For apps that need to maintain state across interactions:

```python
import sqlite3
import json

class ConversationStore:
    def __init__(self, db_path="conversations.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                key TEXT PRIMARY KEY,
                data TEXT,
                expires_at REAL
            )
        """)
    
    def set(self, key, data, ttl=3600):
        expires_at = time.time() + ttl
        self.conn.execute(
            "INSERT OR REPLACE INTO conversations (key, data, expires_at) VALUES (?, ?, ?)",
            (key, json.dumps(data), expires_at)
        )
        self.conn.commit()
    
    def get(self, key):
        row = self.conn.execute(
            "SELECT data, expires_at FROM conversations WHERE key = ?", (key,)
        ).fetchone()
        if row and row[1] > time.time():
            return json.loads(row[0])
        return None
    
    def delete(self, key):
        self.conn.execute("DELETE FROM conversations WHERE key = ?", (key,))
        self.conn.commit()

store = ConversationStore()

# Usage: Track multi-step workflows
@app.action("start_deploy")
def handle_start(ack, body, client):
    ack()
    user_id = body["user"]["id"]
    store.set(f"deploy:{user_id}", {"step": 1, "service": None, "env": None}, ttl=600)
    # Open next step...
```

## 9. Scheduled Messages

```python
import datetime

# Schedule a message for a specific time
def schedule_reminder(client, channel, text, when):
    result = client.chat_scheduleMessage(
        channel=channel,
        text=text,
        post_at=int(when.timestamp())
    )
    return result["scheduled_message_id"]

# Schedule for tomorrow at 9 AM
tomorrow_9am = datetime.datetime.now().replace(hour=9, minute=0, second=0) + datetime.timedelta(days=1)
msg_id = schedule_reminder(client, "C012AB3CD", "Don't forget: sprint review today at 2 PM!", tomorrow_9am)

# List scheduled messages
scheduled = client.chat_scheduledMessages_list(channel="C012AB3CD")

# Delete a scheduled message
client.chat_deleteScheduledMessage(channel="C012AB3CD", scheduled_message_id=msg_id)
```

## 10. Rich Text Blocks

Rich text blocks provide structured formatting without mrkdwn parsing:

```json
{
  "type": "rich_text",
  "elements": [
    {
      "type": "rich_text_section",
      "elements": [
        {"type": "text", "text": "Important: ", "style": {"bold": true}},
        {"type": "text", "text": "Please review the following changes before merging."}
      ]
    },
    {
      "type": "rich_text_list",
      "style": "bullet",
      "elements": [
        {"type": "rich_text_section", "elements": [{"type": "text", "text": "Database migration added"}]},
        {"type": "rich_text_section", "elements": [{"type": "text", "text": "API endpoint deprecated"}]},
        {"type": "rich_text_section", "elements": [{"type": "text", "text": "New environment variable required: "}, {"type": "text", "text": "REDIS_URL", "style": {"code": true}}]}
      ]
    },
    {
      "type": "rich_text_preformatted",
      "elements": [
        {"type": "text", "text": "ALTER TABLE users ADD COLUMN preferences JSONB DEFAULT '{}';\nCREATE INDEX idx_users_preferences ON users USING GIN (preferences);"}
      ]
    }
  ]
}
```

This advanced guide covers the most sophisticated patterns for building production-grade Slack applications with proper state management, progressive UIs, and robust error handling.

## === FILE: 50-slack-cli-reference.md ===
# Slack Master Specialist — CLI and API Reference

## 1. Web API Methods (Complete Reference)

### chat.* Methods

```bash
# Post a message
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","text":"Hello","blocks":[...]}'

# Update a message
curl -X POST https://slack.com/api/chat.update \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","ts":"1234567890.123456","text":"Updated"}'

# Delete a message
curl -X POST https://slack.com/api/chat.delete \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","ts":"1234567890.123456"}'

# Schedule a message
curl -X POST https://slack.com/api/chat.scheduleMessage \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","text":"Reminder!","post_at":1716100000}'

# Post ephemeral message (visible only to one user)
curl -X POST https://slack.com/api/chat.postEphemeral \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","user":"U012AB3CD","text":"Only you can see this"}'

# Get message permalink
curl "https://slack.com/api/chat.getPermalink?channel=C012AB3CD&message_ts=1234567890.123456" \
  -H "Authorization: Bearer xoxb-TOKEN"

# Unfurl links in a message
curl -X POST https://slack.com/api/chat.unfurl \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","ts":"1234567890.123456","unfurls":{"https://example.com":{"blocks":[...]}}}'
```

### conversations.* Methods

```bash
# List channels
curl "https://slack.com/api/conversations.list?types=public_channel,private_channel&limit=200" \
  -H "Authorization: Bearer xoxb-TOKEN"

# Get channel info
curl "https://slack.com/api/conversations.info?channel=C012AB3CD&include_num_members=true" \
  -H "Authorization: Bearer xoxb-TOKEN"

# Create a channel
curl -X POST https://slack.com/api/conversations.create \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"proj-new-feature","is_private":false}'

# Join a channel
curl -X POST https://slack.com/api/conversations.join \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD"}'

# Invite users to a channel
curl -X POST https://slack.com/api/conversations.invite \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","users":"U001,U002,U003"}'

# Kick a user from a channel
curl -X POST https://slack.com/api/conversations.kick \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","user":"U012AB3CD"}'

# Get channel history
curl "https://slack.com/api/conversations.history?channel=C012AB3CD&limit=100&oldest=1716000000" \
  -H "Authorization: Bearer xoxb-TOKEN"

# Get thread replies
curl "https://slack.com/api/conversations.replies?channel=C012AB3CD&ts=1234567890.123456" \
  -H "Authorization: Bearer xoxb-TOKEN"

# Get channel members
curl "https://slack.com/api/conversations.members?channel=C012AB3CD&limit=200" \
  -H "Authorization: Bearer xoxb-TOKEN"

# Set channel topic
curl -X POST https://slack.com/api/conversations.setTopic \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","topic":"Sprint 42 | Ends June 1 | Board: https://jira.example.com"}'

# Set channel purpose
curl -X POST https://slack.com/api/conversations.setPurpose \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","purpose":"Team discussions for the platform team"}'

# Archive a channel
curl -X POST https://slack.com/api/conversations.archive \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD"}'

# Unarchive a channel
curl -X POST https://slack.com/api/conversations.unarchive \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD"}'

# Rename a channel
curl -X POST https://slack.com/api/conversations.rename \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","name":"new-channel-name"}'

# Open a DM
curl -X POST https://slack.com/api/conversations.open \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"users":"U001,U002"}'
```

### users.* Methods

```bash
# Get user info
curl "https://slack.com/api/users.info?user=U012AB3CD" \
  -H "Authorization: Bearer xoxb-TOKEN"

# List all users
curl "https://slack.com/api/users.list?limit=200" \
  -H "Authorization: Bearer xoxb-TOKEN"

# Lookup user by email
curl "https://slack.com/api/users.lookupByEmail?email=user@example.com" \
  -H "Authorization: Bearer xoxb-TOKEN"

# Get user presence
curl "https://slack.com/api/users.getPresence?user=U012AB3CD" \
  -H "Authorization: Bearer xoxb-TOKEN"

# Set user profile (requires user token)
curl -X POST https://slack.com/api/users.profile.set \
  -H "Authorization: Bearer xoxp-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"profile":{"status_text":"In a meeting","status_emoji":":calendar:","status_expiration":1716100000}}'
```

### reactions.* Methods

```bash
# Add a reaction
curl -X POST https://slack.com/api/reactions.add \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","timestamp":"1234567890.123456","name":"thumbsup"}'

# Remove a reaction
curl -X POST https://slack.com/api/reactions.remove \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","timestamp":"1234567890.123456","name":"thumbsup"}'

# Get reactions on a message
curl "https://slack.com/api/reactions.get?channel=C012AB3CD&timestamp=1234567890.123456" \
  -H "Authorization: Bearer xoxb-TOKEN"

# List items a user reacted to
curl "https://slack.com/api/reactions.list?user=U012AB3CD&limit=100" \
  -H "Authorization: Bearer xoxb-TOKEN"
```

### views.* Methods

```bash
# Open a modal
curl -X POST https://slack.com/api/views.open \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"trigger_id":"12345.98765","view":{"type":"modal","callback_id":"my_modal","title":{"type":"plain_text","text":"My Modal"},"blocks":[...]}}'

# Update a modal
curl -X POST https://slack.com/api/views.update \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"view_id":"V012AB3CD","view":{"type":"modal","callback_id":"my_modal","title":{"type":"plain_text","text":"Updated"},"blocks":[...]}}'

# Push a new view onto the modal stack
curl -X POST https://slack.com/api/views.push \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"trigger_id":"12345.98765","view":{"type":"modal","callback_id":"step2","title":{"type":"plain_text","text":"Step 2"},"blocks":[...]}}'

# Publish App Home tab
curl -X POST https://slack.com/api/views.publish \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"U012AB3CD","view":{"type":"home","blocks":[...]}}'
```

### files.* Methods

```bash
# Upload a file (v2 - modern)
# Step 1: Get upload URL
curl -X POST https://slack.com/api/files.getUploadURLExternal \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filename":"report.pdf","length":1048576}'

# Step 2: Upload to returned URL
curl -X POST "$UPLOAD_URL" -F "file=@report.pdf"

# Step 3: Complete upload
curl -X POST https://slack.com/api/files.completeUploadExternal \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"files":[{"id":"F012AB3CD","title":"Report"}],"channel_id":"C012AB3CD"}'

# List files
curl "https://slack.com/api/files.list?channel=C012AB3CD&types=pdfs,images&count=50" \
  -H "Authorization: Bearer xoxb-TOKEN"

# Delete a file
curl -X POST https://slack.com/api/files.delete \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"file":"F012AB3CD"}'

# Get file info
curl "https://slack.com/api/files.info?file=F012AB3CD" \
  -H "Authorization: Bearer xoxb-TOKEN"
```

### pins.* Methods

```bash
# Pin a message
curl -X POST https://slack.com/api/pins.add \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","timestamp":"1234567890.123456"}'

# Unpin a message
curl -X POST https://slack.com/api/pins.remove \
  -H "Authorization: Bearer xoxb-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","timestamp":"1234567890.123456"}'

# List pinned items
curl "https://slack.com/api/pins.list?channel=C012AB3CD" \
  -H "Authorization: Bearer xoxb-TOKEN"
```

## 2. Slack CLI (slack-cli) Commands

```bash
# Authentication
slack login                    # Login to Slack
slack logout                   # Logout
slack auth list                # List authenticated workspaces

# App Management
slack create my-app            # Create new app from template
slack create my-app --template https://github.com/slack-samples/deno-starter-template
slack run                      # Run app locally with hot reload
slack deploy                   # Deploy to Slack infrastructure
slack delete                   # Delete deployed app

# Triggers
slack trigger create --trigger-def triggers/shortcut.ts
slack trigger list             # List all triggers
slack trigger info --trigger-id Ft012AB3CD
slack trigger delete --trigger-id Ft012AB3CD
slack trigger update --trigger-id Ft012AB3CD --trigger-def triggers/updated.ts

# Activity & Debugging
slack activity                 # View app activity
slack activity --tail          # Stream activity in real-time
slack activity --source functions  # Filter by source

# Datastore (for next-gen apps)
slack datastore put '{"datastore":"tasks","item":{"id":"1","title":"Test"}}'
slack datastore get '{"datastore":"tasks","id":"1"}'
slack datastore query '{"datastore":"tasks","expression":"#status = :s","expression_attributes":{"#status":"status"},"expression_values":{":s":"open"}}'
slack datastore delete '{"datastore":"tasks","id":"1"}'

# Environment Variables
slack env add MY_SECRET --value "secret123"
slack env list
slack env remove MY_SECRET

# Manifest
slack manifest info            # View current manifest
slack manifest validate        # Validate manifest
```

## 3. Python SDK Quick Reference

```python
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token="xoxb-TOKEN")

# Post message
client.chat_postMessage(channel="C012AB3CD", text="Hello", blocks=[...])

# Post to thread
client.chat_postMessage(channel="C012AB3CD", thread_ts="1234567890.123456", text="Reply")

# Update message
client.chat_update(channel="C012AB3CD", ts="1234567890.123456", text="Updated")

# Delete message
client.chat_delete(channel="C012AB3CD", ts="1234567890.123456")

# Open modal
client.views_open(trigger_id="12345.98765", view={...})

# Upload file
client.files_upload_v2(channel="C012AB3CD", file="./report.pdf", title="Report")

# Add reaction
client.reactions_add(channel="C012AB3CD", timestamp="1234567890.123456", name="thumbsup")

# Get user info
client.users_info(user="U012AB3CD")

# List channels with pagination
channels = []
cursor = None
while True:
    result = client.conversations_list(types="public_channel", limit=200, cursor=cursor)
    channels.extend(result["channels"])
    cursor = result.get("response_metadata", {}).get("next_cursor")
    if not cursor:
        break
```

## 4. Node.js SDK Quick Reference

```javascript
const { WebClient } = require('@slack/web-api');
const client = new WebClient(process.env.SLACK_BOT_TOKEN);

// Post message
await client.chat.postMessage({ channel: 'C012AB3CD', text: 'Hello', blocks: [...] });

// Post to thread
await client.chat.postMessage({ channel: 'C012AB3CD', thread_ts: '1234567890.123456', text: 'Reply' });

// Update message
await client.chat.update({ channel: 'C012AB3CD', ts: '1234567890.123456', text: 'Updated' });

// Open modal
await client.views.open({ trigger_id: '12345.98765', view: {...} });

// Upload file
await client.filesUploadV2({ channel_id: 'C012AB3CD', file: './report.pdf', filename: 'report.pdf' });

// Paginate through channels
let cursor;
const channels = [];
do {
  const result = await client.conversations.list({ types: 'public_channel', limit: 200, cursor });
  channels.push(...result.channels);
  cursor = result.response_metadata?.next_cursor;
} while (cursor);
```

## 5. Webhook One-Liners

```bash
# Simple text message
curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d '{"text":"Hello from CLI"}'

# Message with emoji
curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d '{"text":":rocket: Deployment started"}'

# Message with mention
curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d '{"text":"<!here> Server alert!"}'

# Message with blocks
curl -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d '{
  "blocks":[{"type":"section","text":{"type":"mrkdwn","text":"*Build #42* passed :white_check_mark:"}}]
}'

# From a shell script (CI/CD)
SLACK_MSG=":white_check_mark: Build \`${BUILD_NUMBER}\` passed for \`${REPO_NAME}\` on branch \`${BRANCH}\`"
curl -s -X POST "$SLACK_WEBHOOK" -H "Content-Type: application/json" -d "{\"text\":\"$SLACK_MSG\"}"
```

## 6. Common jq Patterns for Slack API Responses

```bash
# Extract channel IDs and names
curl -s "https://slack.com/api/conversations.list?types=public_channel" \
  -H "Authorization: Bearer xoxb-TOKEN" | jq -r '.channels[] | "\(.id)\t\(.name)"'

# Find channels with no messages in 30 days
curl -s "https://slack.com/api/conversations.list?types=public_channel" \
  -H "Authorization: Bearer xoxb-TOKEN" | jq -r '.channels[] | select(.updated < (now - 2592000)) | .name'

# Get user emails
curl -s "https://slack.com/api/users.list" \
  -H "Authorization: Bearer xoxb-TOKEN" | jq -r '.members[] | select(.deleted == false) | "\(.real_name)\t\(.profile.email)"'

# Count members per channel
curl -s "https://slack.com/api/conversations.list?types=public_channel" \
  -H "Authorization: Bearer xoxb-TOKEN" | jq -r '.channels[] | "\(.name)\t\(.num_members)"' | sort -t$'\t' -k2 -rn

# Extract message text from history
curl -s "https://slack.com/api/conversations.history?channel=C012AB3CD&limit=50" \
  -H "Authorization: Bearer xoxb-TOKEN" | jq -r '.messages[] | "\(.user // "bot"): \(.text)"'
```

## 7. Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SLACK_BOT_TOKEN` | Bot user OAuth token | `xoxb-123-456-abc` |
| `SLACK_APP_TOKEN` | App-level token (Socket Mode) | `xapp-1-A01-123-abc` |
| `SLACK_SIGNING_SECRET` | Request verification secret | `abc123def456` |
| `SLACK_CLIENT_ID` | OAuth client ID | `123456.789012` |
| `SLACK_CLIENT_SECRET` | OAuth client secret | `abcdef123456` |
| `SLACK_WEBHOOK_URL` | Incoming webhook URL | `https://hooks.slack.com/services/YOUR_T/YOUR_B/TOKEN` |
| `SLACK_LOG_LEVEL` | SDK log level | `DEBUG`, `INFO`, `WARN`, `ERROR` |

This reference covers all major Slack API methods, CLI commands, SDK patterns, and one-liners needed for production Slack app development and operations.

## === FILE: 50-slack-config-schemas.md ===
# Slack Master Specialist — Configuration Schemas Reference

## 1. App Manifest (manifest.yaml)

The complete schema for defining a Slack app declaratively:

```yaml
_metadata:
  major_version: 2
  minor_version: 0

display_information:
  name: "App Name"                    # Required, max 35 chars
  description: "Short description"    # Max 140 chars
  long_description: "Detailed..."     # Max 4000 chars
  background_color: "#2c2d30"         # Hex color for app icon background
  app_home:
    home_tab_enabled: true
    messages_tab_enabled: true
    messages_tab_read_only_enabled: false

features:
  bot_user:
    display_name: "BotName"           # Required, max 80 chars
    always_online: true               # Show bot as always online
  
  slash_commands:
    - command: /deploy
      url: https://app.example.com/slack/commands
      description: "Trigger a deployment"    # Max 2000 chars
      usage_hint: "[env] [service] [version]"  # Max 1000 chars
      should_escape: false
    - command: /status
      url: https://app.example.com/slack/commands
      description: "Check system status"
      usage_hint: "[service]"
      should_escape: false
  
  shortcuts:
    - name: "Create Incident"
      type: global                    # global or message
      callback_id: create_incident
      description: "Create a new incident report"
    - name: "Create Ticket"
      type: message
      callback_id: create_ticket_from_msg
      description: "Create ticket from this message"
  
  unfurl_domains:
    - "jira.example.com"
    - "confluence.example.com"
    - "github.com"
  
  workflow_steps:
    - name: "Create Ticket"
      callback_id: create_ticket_step

oauth_config:
  redirect_urls:
    - https://app.example.com/slack/oauth/callback
  scopes:
    user:
      - search:read
      - users.profile:write
    bot:
      - app_mentions:read
      - channels:history
      - channels:read
      - chat:write
      - chat:write.public
      - commands
      - files:read
      - files:write
      - groups:history
      - groups:read
      - im:history
      - im:read
      - im:write
      - mpim:history
      - reactions:read
      - reactions:write
      - users:read
      - users:read.email

settings:
  event_subscriptions:
    request_url: https://app.example.com/slack/events
    bot_events:
      - app_home_opened
      - app_mention
      - message.channels
      - message.groups
      - message.im
      - member_joined_channel
      - reaction_added
      - link_shared
    user_events:
      - message.channels
  
  interactivity:
    is_enabled: true
    request_url: https://app.example.com/slack/interactions
    message_menu_options_url: https://app.example.com/slack/options
  
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
  
  allowed_ip_address_ranges:
    - "203.0.113.0/24"
    - "198.51.100.0/24"
```

## 2. Block Kit Schemas

### All Block Types

```json
// Header Block
{"type": "header", "text": {"type": "plain_text", "text": "Title", "emoji": true}, "block_id": "optional_id"}

// Section Block
{
  "type": "section",
  "text": {"type": "mrkdwn", "text": "*Bold* and _italic_"},
  "block_id": "section_1",
  "fields": [
    {"type": "mrkdwn", "text": "*Field 1*\nValue"},
    {"type": "mrkdwn", "text": "*Field 2*\nValue"}
  ],
  "accessory": {/* element */}
}

// Divider Block
{"type": "divider", "block_id": "divider_1"}

// Image Block
{
  "type": "image",
  "image_url": "https://example.com/image.png",
  "alt_text": "Description of image",
  "title": {"type": "plain_text", "text": "Image Title"},
  "block_id": "image_1"
}

// Actions Block
{
  "type": "actions",
  "block_id": "actions_1",
  "elements": [/* up to 25 interactive elements */]
}

// Context Block
{
  "type": "context",
  "block_id": "context_1",
  "elements": [/* up to 10 image or text elements */]
}

// Input Block (modals and App Home only)
{
  "type": "input",
  "block_id": "input_1",
  "label": {"type": "plain_text", "text": "Label"},
  "element": {/* input element */},
  "hint": {"type": "plain_text", "text": "Helper text"},
  "optional": false,
  "dispatch_action": false
}

// Video Block
{
  "type": "video",
  "title": {"type": "plain_text", "text": "Video Title"},
  "video_url": "https://www.youtube.com/embed/VIDEO_ID",
  "thumbnail_url": "https://example.com/thumb.png",
  "alt_text": "Video description",
  "author_name": "Author",
  "provider_name": "YouTube",
  "provider_icon_url": "https://example.com/icon.png"
}

// Rich Text Block
{
  "type": "rich_text",
  "elements": [
    {"type": "rich_text_section", "elements": [{"type": "text", "text": "Hello", "style": {"bold": true}}]},
    {"type": "rich_text_list", "style": "bullet", "elements": [
      {"type": "rich_text_section", "elements": [{"type": "text", "text": "Item 1"}]}
    ]},
    {"type": "rich_text_preformatted", "elements": [{"type": "text", "text": "code here"}]},
    {"type": "rich_text_quote", "elements": [{"type": "text", "text": "quoted text"}]}
  ]
}
```

### Interactive Elements

```json
// Button
{
  "type": "button",
  "text": {"type": "plain_text", "text": "Click Me"},
  "action_id": "button_click",
  "value": "button_value",
  "style": "primary",  // "primary" (green), "danger" (red), or omit (default)
  "url": "https://example.com",  // Opens URL instead of sending action
  "confirm": {
    "title": {"type": "plain_text", "text": "Are you sure?"},
    "text": {"type": "mrkdwn", "text": "This action cannot be undone."},
    "confirm": {"type": "plain_text", "text": "Yes"},
    "deny": {"type": "plain_text", "text": "Cancel"},
    "style": "danger"
  }
}

// Static Select
{
  "type": "static_select",
  "action_id": "select_action",
  "placeholder": {"type": "plain_text", "text": "Choose an option"},
  "options": [
    {"text": {"type": "plain_text", "text": "Option 1"}, "value": "opt1"},
    {"text": {"type": "plain_text", "text": "Option 2"}, "value": "opt2"}
  ],
  "option_groups": [
    {"label": {"type": "plain_text", "text": "Group 1"}, "options": [...]}
  ],
  "initial_option": {"text": {"type": "plain_text", "text": "Option 1"}, "value": "opt1"}
}

// External Select (dynamic options)
{
  "type": "external_select",
  "action_id": "external_select",
  "placeholder": {"type": "plain_text", "text": "Search..."},
  "min_query_length": 3
}

// Multi-Static Select
{
  "type": "multi_static_select",
  "action_id": "multi_select",
  "placeholder": {"type": "plain_text", "text": "Select options"},
  "options": [...],
  "max_selected_items": 5
}

// Users Select
{"type": "users_select", "action_id": "user_pick", "placeholder": {"type": "plain_text", "text": "Pick a user"}}

// Conversations Select
{"type": "conversations_select", "action_id": "channel_pick", "placeholder": {"type": "plain_text", "text": "Pick a channel"}, "filter": {"include": ["public", "private"], "exclude_bot_users": true}}

// Date Picker
{
  "type": "datepicker",
  "action_id": "date_pick",
  "placeholder": {"type": "plain_text", "text": "Select a date"},
  "initial_date": "2025-06-01"
}

// Time Picker
{
  "type": "timepicker",
  "action_id": "time_pick",
  "placeholder": {"type": "plain_text", "text": "Select time"},
  "initial_time": "14:30"
}

// Date-Time Picker
{
  "type": "datetimepicker",
  "action_id": "datetime_pick",
  "initial_date_time": 1716100000
}

// Overflow Menu
{
  "type": "overflow",
  "action_id": "overflow_menu",
  "options": [
    {"text": {"type": "plain_text", "text": "Edit"}, "value": "edit"},
    {"text": {"type": "plain_text", "text": "Delete"}, "value": "delete"}
  ]
}

// Radio Buttons
{
  "type": "radio_buttons",
  "action_id": "radio_pick",
  "options": [
    {"text": {"type": "mrkdwn", "text": "*Option A*\nDescription"}, "value": "a"},
    {"text": {"type": "mrkdwn", "text": "*Option B*\nDescription"}, "value": "b"}
  ]
}

// Checkboxes
{
  "type": "checkboxes",
  "action_id": "checkbox_pick",
  "options": [
    {"text": {"type": "mrkdwn", "text": "Option 1"}, "value": "1"},
    {"text": {"type": "mrkdwn", "text": "Option 2"}, "value": "2"}
  ],
  "initial_options": [{"text": {"type": "mrkdwn", "text": "Option 1"}, "value": "1"}]
}

// Plain Text Input
{
  "type": "plain_text_input",
  "action_id": "text_input",
  "placeholder": {"type": "plain_text", "text": "Enter text"},
  "initial_value": "Default",
  "multiline": false,
  "min_length": 1,
  "max_length": 500,
  "dispatch_action_config": {"trigger_actions_on": ["on_enter_pressed"]}
}

// URL Input
{"type": "url_text_input", "action_id": "url_input", "placeholder": {"type": "plain_text", "text": "https://..."}}

// Email Input
{"type": "email_text_input", "action_id": "email_input", "placeholder": {"type": "plain_text", "text": "user@example.com"}}

// Number Input
{"type": "number_input", "action_id": "number_input", "is_decimal_allowed": true, "min_value": "0", "max_value": "100"}
```

## 3. Modal View Schema

```json
{
  "type": "modal",
  "callback_id": "modal_callback",
  "title": {"type": "plain_text", "text": "Modal Title", "emoji": true},
  "submit": {"type": "plain_text", "text": "Submit"},
  "close": {"type": "plain_text", "text": "Cancel"},
  "private_metadata": "{\"key\":\"value\"}",
  "clear_on_close": false,
  "notify_on_close": false,
  "external_id": "unique_external_id",
  "blocks": [
    // Input blocks for forms
    // Section blocks for display
    // Divider blocks for separation
  ]
}
```

## 4. App Home View Schema

```json
{
  "type": "home",
  "blocks": [
    // Any block type except input
    // Header, section, divider, image, actions, context, rich_text, video
  ],
  "private_metadata": "",
  "external_id": ""
}
```

## 5. Message Payload Schema

```json
{
  "channel": "C012AB3CD",
  "text": "Fallback text (required with blocks)",
  "blocks": [...],
  "thread_ts": "1234567890.123456",
  "reply_broadcast": false,
  "unfurl_links": true,
  "unfurl_media": true,
  "mrkdwn": true,
  "metadata": {
    "event_type": "custom_event",
    "event_payload": {"key": "value"}
  }
}
```

## 6. Bolt Configuration (Python)

```python
from slack_bolt import App

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    # OR for Socket Mode:
    # token=os.environ["SLACK_BOT_TOKEN"],
    # For OAuth:
    # client_id=os.environ["SLACK_CLIENT_ID"],
    # client_secret=os.environ["SLACK_CLIENT_SECRET"],
    # scopes=["chat:write", "commands"],
    # installation_store=FileInstallationStore(),
    # oauth_state_store=FileOAuthStateStore(expiration_seconds=600),
)

# Middleware configuration
app.use(lambda next, event, logger: (logger.info(f"Event: {event}"), next()))

# Error handler
@app.error
def handle_error(error, body, logger):
    logger.exception(f"Error: {error}")
    logger.info(f"Request body: {body}")
```

## 7. Bolt Configuration (JavaScript)

```javascript
const { App, LogLevel } = require('@slack/bolt');

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
  socketMode: true,
  appToken: process.env.SLACK_APP_TOKEN,
  logLevel: LogLevel.DEBUG,
  
  // Custom receiver (for Express integration)
  // receiver: new ExpressReceiver({ signingSecret, endpoints: '/slack/events' }),
  
  // OAuth configuration
  // clientId: process.env.SLACK_CLIENT_ID,
  // clientSecret: process.env.SLACK_CLIENT_SECRET,
  // stateSecret: 'my-state-secret',
  // scopes: ['chat:write', 'commands'],
  // installationStore: new FileInstallationStore(),
});

// Global middleware
app.use(async ({ next, body, logger }) => {
  logger.info(`Incoming: ${body.type}`);
  await next();
});

// Error handler
app.error(async (error) => {
  console.error(`Error: ${error.message}`, error.original || error);
});
```

## 8. Next-Gen Platform Configuration (Deno)

### manifest.ts

```typescript
import { Manifest } from "deno-slack-sdk/mod.ts";
import { CreateTicketWorkflow } from "./workflows/create_ticket.ts";

export default Manifest({
  name: "DeployBot",
  description: "Deployment automation",
  icon: "assets/icon.png",
  workflows: [CreateTicketWorkflow],
  outgoingDomains: ["api.example.com"],
  datastores: [],
  botScopes: ["commands", "chat:write", "channels:read"],
});
```

### slack.json

```json
{
  "hooks": {
    "get-hooks": "deno run -q --allow-read --allow-net https://deno.land/x/deno_slack_hooks/mod.ts"
  }
}
```

## 9. Webhook Payload Schemas

### Incoming Webhook

```json
{
  "text": "Fallback text",
  "blocks": [...],
  "response_type": "in_channel",
  "replace_original": false,
  "delete_original": false,
  "unfurl_links": false,
  "unfurl_media": false
}
```

### Interaction Payload (block_actions)

```json
{
  "type": "block_actions",
  "user": {"id": "U012AB3CD", "username": "user", "name": "User Name", "team_id": "T012AB3CD"},
  "api_app_id": "A012AB3CD",
  "token": "verification_token",
  "trigger_id": "12345.98765.abcdef",
  "team": {"id": "T012AB3CD", "domain": "team"},
  "enterprise": null,
  "is_enterprise_install": false,
  "channel": {"id": "C012AB3CD", "name": "general"},
  "message": {"type": "message", "ts": "1234567890.123456", "text": "Original"},
  "response_url": "https://hooks.slack.com/actions/T012/B012/xxxx",
  "actions": [
    {
      "type": "button",
      "action_id": "action_id",
      "block_id": "block_id",
      "text": {"type": "plain_text", "text": "Button Text"},
      "value": "button_value",
      "action_ts": "1234567890.123456"
    }
  ]
}
```

### View Submission Payload

```json
{
  "type": "view_submission",
  "team": {"id": "T012AB3CD"},
  "user": {"id": "U012AB3CD"},
  "view": {
    "id": "V012AB3CD",
    "type": "modal",
    "callback_id": "modal_id",
    "title": {"type": "plain_text", "text": "Title"},
    "state": {
      "values": {
        "block_id": {
          "action_id": {
            "type": "plain_text_input",
            "value": "user entered text"
          }
        }
      }
    },
    "private_metadata": "{\"key\":\"value\"}"
  }
}
```

## 10. Date Formatting Tokens

```
{date_num}         → 2025-05-29
{date}             → May 29, 2025
{date_short}       → May 29, 2025
{date_long}        → Thursday, May 29, 2025
{date_pretty}      → May 29, 2025 (or "yesterday", "today", "tomorrow")
{date_short_pretty} → May 29 (or "yesterday")
{date_long_pretty} → Thursday, May 29, 2025 (or "yesterday")
{time}             → 2:30 PM
{time_secs}        → 2:30:45 PM

// Usage in mrkdwn:
<!date^1716988200^{date_short} at {time}|May 29, 2025 at 2:30 PM>
```

This configuration schemas reference provides the complete structure for all Slack app configurations, Block Kit elements, and payload formats needed for building any Slack integration.

## === FILE: 50-slack-deep-dive.md ===
# Slack Master Specialist — Deep Dive: Architecture and Internals

## 1. Slack Platform Architecture

### Message Flow

```
User types message
    → Slack Client (desktop/mobile/web)
    → Slack Gateway (WebSocket connection)
    → Message Service (validation, storage)
    → Channel Service (membership, permissions)
    → Search Index (Elasticsearch)
    → Event Dispatch (fan-out to subscribers)
    → App Event Delivery (HTTP POST or WebSocket)
    → Your App Server
```

### Real-Time Messaging (RTM) vs Events API vs Socket Mode

| Feature | RTM (deprecated) | Events API | Socket Mode |
|---------|-----------------|------------|-------------|
| Connection | WebSocket | HTTP POST | WebSocket |
| Public URL needed | No | Yes | No |
| Scalability | Limited (1 conn/workspace) | High | Medium |
| Event types | All | Subscribed only | Subscribed only |
| Recommended | No | Production | Development/Internal |

### Event Delivery Guarantees

- Events are delivered **at least once** (not exactly once)
- Slack retries up to 3 times with exponential backoff
- Retry intervals: ~1 min, ~5 min, ~30 min
- After 3 failures, the event is dropped and a warning appears in app dashboard
- Your app must handle duplicates (use `event_id` for deduplication)

## 2. Block Kit Rendering Engine

### How Blocks Are Rendered

```
Block Kit JSON
    → Server-side validation (schema check)
    → Client receives block array
    → React component tree (desktop/web)
    → Native component tree (mobile)
    → Layout engine (flexbox-like)
    → Rendered UI
```

### Block Limits

| Constraint | Limit |
|-----------|-------|
| Blocks per message | 50 |
| Blocks per modal | 100 |
| Blocks per App Home | 100 |
| Actions per actions block | 25 |
| Elements per context block | 10 |
| Fields per section block | 10 |
| Options per select menu | 100 |
| Option groups per select | 100 |
| Characters in mrkdwn text | 3,000 |
| Characters in plain_text | 3,000 |
| Characters in header | 150 |
| Characters in button text | 75 |
| Characters in option text | 75 |
| Characters in placeholder | 150 |
| Total message size | 40,000 chars |

### Text Object Types

| Type | Parsing | Use Case |
|------|---------|----------|
| `plain_text` | No formatting | Buttons, headers, labels, placeholders |
| `mrkdwn` | Slack markdown | Section text, context, fields |

mrkdwn supports: `*bold*`, `_italic_`, `~strike~`, `` `code` ``, ` ```code block``` `, `> quote`, `>>> block quote`, `<url|text>`, `<@user>`, `<#channel>`, `<!date^ts^format|fallback>`

## 3. OAuth 2.0 Implementation Details

### Token Types Deep Dive

**Bot Tokens (xoxb-)**
- Represent the app's bot user
- Persist across user sessions
- Limited to bot scopes
- One per workspace installation
- Cannot access user-specific data (search, profile write)

**User Tokens (xoxp-)**
- Represent a specific user
- Can access user-specific APIs (search, profile)
- Required for admin APIs
- One per user who authorizes
- Higher security risk

**App-Level Tokens (xapp-)**
- Used exclusively for Socket Mode connections
- Cannot call Web API methods
- One per app (not per workspace)
- Long-lived, rarely rotated

### Token Lifecycle

```
App Installation
    → OAuth flow initiated
    → User authorizes scopes
    → Slack issues access_token (+ refresh_token if rotation enabled)
    → Token stored by your app
    → Token used for API calls
    → [If rotation enabled] Token expires after 12 hours
    → Refresh token used to get new access_token
    → [If app uninstalled] Token revoked, tokens.revoked event sent
```

## 4. Interaction Payload Flow

### Complete Interaction Lifecycle

```
User clicks button/submits form
    → Slack sends interaction payload to Request URL
    → Your app receives payload (must respond in 3s)
    → Acknowledge with HTTP 200
    → [Optional] Return updated message/view in response body
    → [Optional] Use response_url for follow-up (within 30 min, max 5)
    → [Optional] Use trigger_id to open modal (within 3s)
    → [Optional] Call Web API for additional actions
```

### trigger_id Expiration

The `trigger_id` is valid for exactly 3 seconds from when the interaction occurred. This means:
- You must open modals immediately in your request handler
- You cannot fetch data from external APIs before opening a modal
- Pattern: Open modal with loading state, then update it with data

```python
@app.action("open_details")
def handle(ack, body, client):
    ack()
    
    # Open modal immediately with loading state
    result = client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "details_modal",
            "title": {"type": "plain_text", "text": "Loading..."},
            "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": ":hourglass: Loading details..."}}]
        }
    )
    
    # Now fetch data (can take as long as needed)
    data = fetch_details_from_api(body["actions"][0]["value"])
    
    # Update the modal with real data
    client.views_update(
        view_id=result["view"]["id"],
        view={
            "type": "modal",
            "callback_id": "details_modal",
            "title": {"type": "plain_text", "text": "Details"},
            "blocks": build_detail_blocks(data)
        }
    )
```

## 5. Message Storage and Retrieval

### Message Timestamps (ts)

The `ts` field is the unique identifier for messages within a channel:
- Format: `"1234567890.123456"` (Unix timestamp with microseconds)
- Used as message ID for updates, deletions, reactions, threading
- Thread parent `ts` becomes the `thread_ts` for replies
- Timestamps are unique within a channel but not globally

### Message History Pagination

```
conversations.history
    → Returns messages in reverse chronological order
    → Default limit: 100 messages
    → Max limit: 1000 messages
    → Use cursor-based pagination for more
    → oldest/latest parameters for time-based filtering
    → inclusive parameter to include boundary messages
```

### Message Subtypes

| Subtype | Meaning |
|---------|---------|
| `null` | Regular user message |
| `bot_message` | Posted by a bot (legacy) |
| `message_changed` | Message was edited |
| `message_deleted` | Message was deleted |
| `channel_join` | User joined channel |
| `channel_leave` | User left channel |
| `channel_topic` | Topic was changed |
| `channel_purpose` | Purpose was changed |
| `channel_name` | Channel was renamed |
| `file_share` | File was shared |
| `thread_broadcast` | Thread reply broadcast to channel |
| `tombstone` | DLP-deleted message placeholder |

## 6. File System

### File Upload Flow (V2)

```
1. Client requests upload URL
   POST files.getUploadURLExternal
   → Returns: upload_url, file_id

2. Client uploads file content
   POST {upload_url}
   → Binary file data uploaded directly

3. Client completes upload
   POST files.completeUploadExternal
   → File associated with channel/thread
   → Thumbnails generated
   → Search indexed
   → Virus scanned
```

### File Types and Processing

| Category | Types | Processing |
|----------|-------|-----------|
| Images | png, jpg, gif, svg, webp | Thumbnails, preview |
| Documents | pdf, doc, docx, ppt, pptx | Preview, text extraction |
| Code | py, js, ts, go, rb, etc. | Syntax highlighting |
| Archives | zip, tar, gz | File listing |
| Audio | mp3, wav, m4a | Playback, transcription |
| Video | mp4, webm, mov | Playback, thumbnails |

## 7. Search Architecture

### How Slack Search Works

- Uses Elasticsearch under the hood
- Indexes: messages, files, channels, users
- Real-time indexing (messages searchable within seconds)
- Supports: exact match, phrase, boolean operators
- Filters: from, in, during, has, before, after
- Ranking: relevance + recency + user affinity

### Search Modifiers

```
from:@username        → Messages from specific user
in:#channel           → Messages in specific channel
has:link              → Messages containing URLs
has:reaction          → Messages with reactions
has::emoji:           → Messages with specific reaction
before:2025-01-01    → Messages before date
after:2025-01-01     → Messages after date
during:january       → Messages during month
on:2025-05-29        → Messages on specific date
is:thread            → Messages that are thread replies
```

## 8. Workspace Data Model

### Entity Relationships

```
Enterprise (org)
  └── Workspaces (teams)
       ├── Users (members)
       │    ├── Profile
       │    ├── Status
       │    └── Preferences
       ├── Channels (conversations)
       │    ├── Public channels
       │    ├── Private channels
       │    ├── DMs (im)
       │    ├── Group DMs (mpim)
       │    └── Shared channels (Slack Connect)
       ├── User Groups
       ├── Apps (installed)
       │    ├── Bot User
       │    ├── Tokens
       │    └── Permissions
       └── Files
            ├── Uploads
            ├── Snippets
            └── Posts
```

### Channel Types

| Type | API Type | Properties |
|------|----------|-----------|
| Public | `public_channel` | Anyone can join, searchable |
| Private | `private_channel` | Invite only, not searchable by non-members |
| DM | `im` | 1:1 conversation |
| Group DM | `mpim` | Multi-party DM (up to 9 people) |
| Shared | `public_channel` + `is_shared` | Cross-organization |

## 9. Rate Limiting Internals

### How Rate Limits Are Calculated

Slack uses a token bucket algorithm per app per workspace:
- Each tier has a bucket size (burst capacity)
- Tokens refill at a steady rate
- When bucket is empty, requests get 429 response
- `Retry-After` header tells you when to retry

### Special Rate Limits

| Scenario | Limit | Notes |
|----------|-------|-------|
| `chat.postMessage` per channel | 1/sec | Prevents channel flooding |
| Incoming webhooks | 1/sec | Per webhook URL |
| Web API overall | Varies by tier | Per app per workspace |
| Events API delivery | No limit from Slack | But your server must handle |
| Socket Mode | 30,000 events/hour | Per app |

### Handling Burst Traffic

```python
import asyncio
from collections import defaultdict

class ChannelRateLimiter:
    """Ensures max 1 message per second per channel"""
    
    def __init__(self):
        self.last_post = defaultdict(float)
        self.lock = asyncio.Lock()
    
    async def wait_for_channel(self, channel_id):
        async with self.lock:
            now = asyncio.get_event_loop().time()
            elapsed = now - self.last_post[channel_id]
            if elapsed < 1.0:
                await asyncio.sleep(1.0 - elapsed)
            self.last_post[channel_id] = asyncio.get_event_loop().time()
```

## 10. Enterprise Grid Architecture

### Multi-Workspace Model

```
Organization (Enterprise Grid)
├── Org-level settings
│    ├── App management policies
│    ├── Information barriers
│    ├── DLP policies
│    └── Audit logs
├── Workspace A
│    ├── Local channels
│    ├── Local apps
│    └── Local users
├── Workspace B
│    ├── Local channels
│    ├── Local apps
│    └── Local users
└── Org-wide channels
     └── Available across all workspaces
```

### Org-Level vs Workspace-Level

| Feature | Org-Level | Workspace-Level |
|---------|-----------|-----------------|
| App approval | Org admin controls | Workspace admin installs |
| User management | Provisioned centrally | Workspace membership |
| Channels | Org-wide channels | Local channels |
| Policies | DLP, retention | Channel-specific |
| Audit logs | All workspaces | Single workspace |
| SSO/SAML | Configured once | Inherited |

## 11. Slack Connect Internals

### How Shared Channels Work

```
Workspace A                    Workspace B
    │                              │
    ├── Channel #shared-proj       │
    │       │                      │
    │       └── Shared via ────────┤
    │           Slack Connect      │
    │                              ├── Same channel appears
    │                              │   in Workspace B
    │                              │
    Messages are stored in both workspaces
    Each workspace applies its own:
    - Retention policies
    - DLP rules
    - Compliance exports
    - App access rules
```

### Security Boundaries

- Each org controls its own data retention
- Files can be restricted from external sharing
- Apps in one workspace cannot access the other's data
- User profiles show limited info to external users
- Admin controls for who can create shared channels

## 12. Performance Characteristics

### API Response Times (Typical)

| Method | p50 | p95 | p99 |
|--------|-----|-----|-----|
| `auth.test` | 50ms | 150ms | 500ms |
| `chat.postMessage` | 100ms | 300ms | 1000ms |
| `conversations.list` | 200ms | 500ms | 2000ms |
| `users.list` | 300ms | 800ms | 3000ms |
| `views.open` | 150ms | 400ms | 1500ms |
| `files.upload` | 500ms | 2000ms | 5000ms |

### Optimizing API Usage

1. **Cache aggressively**: User info, channel info rarely change
2. **Batch operations**: Use `conversations.list` instead of individual `info` calls
3. **Paginate efficiently**: Use max `limit` to reduce round trips
4. **Use Socket Mode**: Eliminates HTTP overhead for events
5. **Minimize blocks**: Fewer blocks = faster rendering
6. **Lazy load**: Don't fetch data until user requests it

## 13. Message Delivery Semantics

### Ordering Guarantees

- Messages within a channel are ordered by `ts`
- Events may arrive out of order (use `event_ts` for ordering)
- Thread replies are ordered within the thread
- Edited messages keep their original `ts` (position)

### Consistency Model

- Messages are eventually consistent across clients
- Real-time delivery is best-effort (WebSocket may drop)
- API reads are strongly consistent (always see latest)
- Search index has slight delay (seconds to minutes)

## 14. Slack's Technology Stack (Public Knowledge)

Based on publicly available information:
- **Backend**: PHP (legacy), Java, Go (newer services)
- **Frontend**: React (web), Electron (desktop)
- **Mobile**: React Native + native modules
- **Database**: MySQL (sharded), Vitess
- **Cache**: Memcached, Redis
- **Search**: Elasticsearch
- **Queue**: Kafka
- **Storage**: S3-compatible
- **CDN**: CloudFront
- **Real-time**: Custom WebSocket infrastructure

## 15. Future Platform Direction

### Next-Gen Platform (Deno-based)

- Functions run on Slack's infrastructure (no server needed)
- Deno runtime for TypeScript/JavaScript
- Built-in datastores (key-value)
- Triggers replace traditional event subscriptions
- Workflows compose functions visually
- Automatic scaling and zero-ops deployment

### Deprecation Timeline

| Feature | Status | Replacement |
|---------|--------|-------------|
| RTM API | Deprecated | Events API + Socket Mode |
| Legacy attachments | Deprecated | Block Kit |
| Classic apps | Deprecated | New Slack apps |
| Workflow Steps from Apps | Deprecated | Platform Functions |
| `files.upload` (v1) | Deprecated | `files.uploadV2` |

This deep dive provides the architectural understanding needed to build robust, performant Slack integrations that work with the platform rather than against it.

## === FILE: 50-slack-security-audit.md ===
# Slack Master Specialist — Security Audit Guide

## 1. Token Security

### Token Types and Risk Levels

| Token | Prefix | Risk | Exposure Impact |
|-------|--------|------|-----------------|
| Bot Token | `xoxb-` | High | Full bot access to workspace |
| User Token | `xoxp-` | Critical | Full user access, can impersonate |
| App Token | `xapp-` | Medium | Socket Mode connection only |
| Webhook URL | `https://hooks...` | Medium | Can post to specific channel |
| Signing Secret | 32-char hex | High | Can forge requests to your app |

### Token Storage Best Practices

```python
# NEVER do this
BOT_TOKEN = "xoxb-123-456-abc"  # Hardcoded in source

# CORRECT: Use environment variables
import os
BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# CORRECT: Use secrets manager
from aws_secretsmanager import get_secret
BOT_TOKEN = get_secret("slack/bot-token")
```

### Token Rotation

```python
# Check if token rotation is enabled
# When enabled, tokens expire and must be refreshed

def refresh_token(client_id, client_secret, refresh_token):
    response = requests.post("https://slack.com/api/oauth.v2.access", data={
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    })
    data = response.json()
    if data["ok"]:
        return {
            "access_token": data["access_token"],
            "refresh_token": data["refresh_token"],
            "expires_in": data["expires_in"]
        }
    raise Exception(f"Token refresh failed: {data['error']}")
```

## 2. Request Verification

### Signing Secret Verification (Required)

Every incoming request from Slack must be verified:

```python
import hashlib
import hmac
import time

def verify_slack_request(signing_secret, body, timestamp, signature):
    # Prevent replay attacks (reject requests older than 5 minutes)
    if abs(time.time() - int(timestamp)) > 300:
        return False
    
    # Compute expected signature
    sig_basestring = f"v0:{timestamp}:{body}"
    expected_signature = "v0=" + hmac.new(
        signing_secret.encode("utf-8"),
        sig_basestring.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    
    # Constant-time comparison to prevent timing attacks
    return hmac.compare_digest(expected_signature, signature)
```

### Middleware Implementation

```python
from flask import Flask, request, abort
from functools import wraps

def require_slack_verification(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
        signature = request.headers.get("X-Slack-Signature", "")
        body = request.get_data(as_text=True)
        
        if not verify_slack_request(SIGNING_SECRET, body, timestamp, signature):
            abort(401)
        
        return f(*args, **kwargs)
    return decorated
```

## 3. OAuth Security

### Secure OAuth Flow

```python
import secrets

# Generate state parameter to prevent CSRF
def generate_oauth_state():
    state = secrets.token_urlsafe(32)
    # Store in session/database with expiry
    store_state(state, expires_in=600)
    return state

# Verify state on callback
def handle_oauth_callback(request):
    state = request.args.get("state")
    if not verify_state(state):
        abort(403, "Invalid state parameter - possible CSRF attack")
    
    code = request.args.get("code")
    # Exchange code for token...
```

### Scope Minimization

Only request the scopes your app actually needs:

```yaml
# BAD: Over-permissioned
oauth_config:
  scopes:
    bot:
      - admin
      - channels:manage
      - chat:write
      - users:read
      - files:read
      - files:write

# GOOD: Minimal permissions
oauth_config:
  scopes:
    bot:
      - chat:write          # Only if posting messages
      - channels:read       # Only if reading channel info
      - app_mentions:read   # Only if responding to mentions
```

## 4. Data Protection

### Sensitive Data in Messages

```python
# NEVER include sensitive data in messages
# BAD
client.chat_postMessage(channel=channel, text=f"API Key: {api_key}")

# GOOD: Use ephemeral messages for sensitive info
client.chat_postEphemeral(
    channel=channel,
    user=user_id,
    text="Your temporary access code has been sent to your email."
)
```

### Message Retention and Deletion

```python
# Delete sensitive messages after a timeout
import threading

def post_and_auto_delete(client, channel, text, delete_after_seconds=300):
    result = client.chat_postMessage(channel=channel, text=text)
    ts = result["ts"]
    
    def delete_later():
        time.sleep(delete_after_seconds)
        try:
            client.chat_delete(channel=channel, ts=ts)
        except Exception:
            pass
    
    threading.Thread(target=delete_later, daemon=True).start()
    return result
```

### Input Sanitization

```python
def sanitize_user_input(text, max_length=3000):
    # Remove potential mrkdwn injection
    sanitized = text.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")
    
    # Prevent @channel/@here abuse
    sanitized = sanitized.replace("<!channel>", "[channel]")
    sanitized = sanitized.replace("<!here>", "[here]")
    sanitized = sanitized.replace("<!everyone>", "[everyone]")
    
    # Truncate to prevent oversized messages
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length - 3] + "..."
    
    return sanitized
```

## 5. App Installation Security

### Restricting App Installation

For Enterprise Grid, restrict which workspaces can install your app:

```python
def handle_oauth_callback(request):
    code = request.args.get("code")
    result = client.oauth_v2_access(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code=code
    )
    
    team_id = result["team"]["id"]
    enterprise_id = result.get("enterprise", {}).get("id")
    
    # Verify the installing workspace is allowed
    allowed_teams = get_allowed_teams()
    if team_id not in allowed_teams:
        return "Installation not permitted for this workspace", 403
    
    # Store token securely
    store_token_encrypted(team_id, result["access_token"])
```

## 6. Webhook Security

### Webhook URL Protection

- Never expose webhook URLs in client-side code
- Rotate webhook URLs periodically
- Use IP allowlisting if possible
- Monitor webhook usage for anomalies

### Outgoing Webhook Verification

```python
def verify_outgoing_webhook(token, expected_token):
    """Verify the token in outgoing webhook payloads"""
    return hmac.compare_digest(token, expected_token)
```

## 7. Network Security

### HTTPS Requirements

- All Slack API communication must use HTTPS
- Request URLs must have valid SSL certificates
- Self-signed certificates are not accepted
- TLS 1.2+ is required

### IP Allowlisting

Slack does not publish a fixed IP range for outgoing requests. Instead:
- Use request signature verification (signing secret)
- Implement proper authentication on all endpoints
- Use Socket Mode to avoid exposing public endpoints

## 8. Audit Logging

### App Activity Logging

```python
import logging
import json
from datetime import datetime

audit_logger = logging.getLogger("slack_audit")
audit_logger.setLevel(logging.INFO)
handler = logging.FileHandler("slack_audit.log")
audit_logger.addHandler(handler)

def log_action(action, user_id, channel=None, details=None):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "user_id": user_id,
        "channel": channel,
        "details": details
    }
    audit_logger.info(json.dumps(entry))

# Usage
log_action("message_posted", user_id="U012AB3CD", channel="C012AB3CD", details={"text_length": 150})
log_action("modal_submitted", user_id="U012AB3CD", details={"callback_id": "create_ticket"})
log_action("file_uploaded", user_id="U012AB3CD", channel="C012AB3CD", details={"file_type": "pdf", "size_bytes": 1048576})
```

### Enterprise Grid Audit Logs

```bash
# Query audit logs
curl "https://api.slack.com/audit/v1/logs?action=user_login&oldest=1716000000" \
  -H "Authorization: Bearer xoxp-org-admin-token"

# Monitor app installations
curl "https://api.slack.com/audit/v1/logs?action=app_installed" \
  -H "Authorization: Bearer xoxp-org-admin-token"

# Track file downloads
curl "https://api.slack.com/audit/v1/logs?action=file_downloaded&actor=U012AB3CD" \
  -H "Authorization: Bearer xoxp-org-admin-token"
```

## 9. Security Checklist

### Development Phase

- [ ] Signing secret stored in environment variable, not code
- [ ] All tokens stored in secrets manager
- [ ] Request signature verification on all endpoints
- [ ] OAuth state parameter implemented (CSRF protection)
- [ ] Minimal scopes requested
- [ ] Input sanitization on all user-provided data
- [ ] No sensitive data logged or stored in messages
- [ ] Error messages don't leak internal details

### Deployment Phase

- [ ] HTTPS with valid certificate on all endpoints
- [ ] Token rotation enabled (if supported)
- [ ] Rate limiting implemented
- [ ] Audit logging enabled
- [ ] Monitoring for unusual API usage patterns
- [ ] Webhook URLs not exposed in public repositories
- [ ] Environment variables not in Docker images
- [ ] Secrets not in CI/CD logs

### Operations Phase

- [ ] Regular token rotation schedule
- [ ] Unused app permissions removed
- [ ] Inactive apps uninstalled
- [ ] Audit logs reviewed weekly
- [ ] Incident response plan for token compromise
- [ ] Backup authentication method available
- [ ] DLP policies configured (Enterprise)
- [ ] Information barriers set (Enterprise Grid)

## 10. Incident Response for Token Compromise

### Immediate Actions

1. Revoke the compromised token immediately
2. Check audit logs for unauthorized activity
3. Regenerate all related secrets (signing secret, client secret)
4. Re-install the app to generate new tokens
5. Notify affected workspace admins
6. Review and rotate any other secrets that may have been exposed

### Prevention

```python
# Implement token usage monitoring
def monitor_token_usage(method, response):
    # Alert on unusual patterns
    if method in ["admin.users.remove", "conversations.delete"]:
        alert_security_team(f"Sensitive API call: {method}")
    
    # Track usage patterns
    record_api_usage(method, response.get("ok"), time.time())
```

This security audit guide ensures your Slack applications follow enterprise-grade security practices and are resilient against common attack vectors.

## === FILE: 50-slack-specialist.md ===
# Slack Master Specialist

## 1. Role Definition and Expertise

The Slack Master Specialist possesses comprehensive knowledge of the Slack platform, covering message formatting with mrkdwn syntax, Block Kit UI framework, emoji and reactions systems, Web API methods, app development patterns, workflow automation, and enterprise administration. This specialist helps teams communicate effectively by crafting well-formatted messages, building interactive Block Kit layouts, developing Slack apps, troubleshooting integration issues, and optimizing workspace configurations for maximum productivity.

## 2. Slack Architecture Overview

Slack operates as a channel-based messaging platform built on a real-time event-driven architecture. The platform consists of workspaces (formerly teams), which contain channels (public and private), direct messages, and group messages. Each workspace has its own set of users, custom emoji, installed apps, and configuration settings.

### Core Concepts

| Concept | Description | ID Format |
|---------|-------------|-----------|
| Workspace | Top-level organizational unit | T followed by alphanumeric (T012AB3CD) |
| Channel | Conversation space (public or private) | C followed by alphanumeric (C012AB3CD) |
| User | Individual workspace member | U followed by alphanumeric (U012AB3CD) |
| Bot User | App-controlled user | B followed by alphanumeric (B012AB3CD) |
| Message | Individual post in a channel | Timestamp-based (1234567890.123456) |
| Thread | Reply chain under a parent message | Uses parent message ts |
| File | Uploaded or shared file | F followed by alphanumeric |
| App | Integration or bot application | A followed by alphanumeric |

### Message Addressing

Every message in Slack is uniquely identified by the combination of its channel ID and timestamp (ts). The timestamp serves as both a unique identifier and a chronological marker. Thread replies reference the parent message's ts as thread_ts.

### Enterprise Grid

Enterprise Grid connects multiple workspaces under a single organization. It provides centralized administration, shared channels across workspaces, organization-wide search, and unified compliance controls. Grid organizations have an org-level ID (E prefix) and manage multiple workspace-level teams.

## 3. Message Formatting with mrkdwn

Slack uses its own markup language called mrkdwn (not standard Markdown). Understanding the differences is critical for proper message formatting.

### Text Formatting

```
*bold text*          → bold text
_italic text_        → italic text
~strikethrough~      → strikethrough text
`inline code`        → inline code
```code block```     → code block (multi-line)
> blockquote         → indented quote (single line)
>>> blockquote all   → quotes everything after this marker
```

### Important mrkdwn vs Markdown Differences

| Feature | Markdown | Slack mrkdwn |
|---------|----------|--------------|
| Bold | `**text**` | `*text*` |
| Italic | `*text*` | `_text_` |
| Strikethrough | `~~text~~` | `~text~` |
| Headers | `# Header` | Not supported |
| Bullet lists | `- item` | Use bullet character or emoji |
| Numbered lists | `1. item` | Manual numbering |
| Tables | Pipe syntax | Not supported in mrkdwn |
| Images | `![alt](url)` | Not supported (use blocks) |
| Horizontal rule | `---` | Not supported |

### Links and References

```
<https://example.com|Display Text>              → Hyperlink with custom text
<mailto:user@example.com|Email Link>            → Email link
<#C012AB3CD>                                     → Channel reference (auto-resolves name)
<#C012AB3CD|general>                            → Channel with fallback text
<@U012AB3CD>                                     → User mention (triggers notification)
<!subteam^S012AB3CD|@team-name>                 → User group mention
<!here>                                          → Notify active channel members
<!channel>                                       → Notify all channel members
<!everyone>                                      → Notify everyone in #general
```

### Date Formatting

Slack provides locale-aware date formatting using a special syntax that renders dates in each user's local timezone:

```
<!date^1392734382^{date_num} at {time}|February 18th, 2014 at 6:39 AM PST>
```

Available date tokens:

| Token | Example Output |
|-------|---------------|
| `{date_num}` | 2014-02-18 |
| `{date}` | February 18th, 2014 |
| `{date_short}` | Feb 18, 2014 |
| `{date_long}` | Tuesday, February 18th, 2014 |
| `{date_pretty}` | yesterday, today, tomorrow (or falls back to {date}) |
| `{date_short_pretty}` | yesterday, today, tomorrow (or falls back to {date_short}) |
| `{date_long_pretty}` | yesterday, today, tomorrow (or falls back to {date_long}) |
| `{time}` | 6:39 AM |
| `{time_secs}` | 6:39:42 AM |

The syntax is: `<!date^UNIX_TIMESTAMP^TOKEN_STRING^OPTIONAL_LINK|FALLBACK_TEXT>`

### Special Characters and Escaping

Three characters must be escaped in mrkdwn:

```
& → &amp;
< → &lt;
> → &gt;
```

## 4. Block Kit Complete Reference

Block Kit is Slack's UI framework for building rich, interactive message layouts. It uses a JSON-based structure where blocks are stacked vertically to create complex layouts.

### Limits

- Messages: maximum 50 blocks
- Modals and Home tabs: maximum 100 blocks
- Text fields within blocks: maximum 3,000 characters (some fields allow less)

### 4.1 Section Block

The most versatile block type. Displays text with an optional accessory element and up to 10 fields.

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": "*Project Update*\nThe deployment completed successfully."
  },
  "accessory": {
    "type": "button",
    "text": { "type": "plain_text", "text": "View Details" },
    "action_id": "view_details_btn",
    "url": "https://deploy.example.com/run/123"
  },
  "fields": [
    { "type": "mrkdwn", "text": "*Environment:*\nProduction" },
    { "type": "mrkdwn", "text": "*Duration:*\n3m 42s" }
  ]
}
```

### 4.2 Header Block

Displays large, bold text. Plain text only, max 150 characters.

```json
{
  "type": "header",
  "text": { "type": "plain_text", "text": "Weekly Status Report", "emoji": true }
}
```

### 4.3 Divider Block

A simple horizontal line separator.

```json
{ "type": "divider" }
```

### 4.4 Image Block

Displays a standalone image with optional title.

```json
{
  "type": "image",
  "image_url": "https://example.com/chart.png",
  "alt_text": "Monthly revenue chart",
  "title": { "type": "plain_text", "text": "Revenue Q1 2025" }
}
```

### 4.5 Actions Block

Holds up to 25 interactive elements.

```json
{
  "type": "actions",
  "elements": [
    {
      "type": "button",
      "text": { "type": "plain_text", "text": "Approve" },
      "style": "primary",
      "action_id": "approve_request",
      "value": "req_001"
    },
    {
      "type": "button",
      "text": { "type": "plain_text", "text": "Deny" },
      "style": "danger",
      "action_id": "deny_request",
      "value": "req_001"
    },
    {
      "type": "static_select",
      "placeholder": { "type": "plain_text", "text": "Assign to..." },
      "action_id": "assign_user",
      "options": [
        { "text": { "type": "plain_text", "text": "Alice" }, "value": "U001" },
        { "text": { "type": "plain_text", "text": "Bob" }, "value": "U002" }
      ]
    }
  ]
}
```

### 4.6 Context Block

Displays small contextual information (max 10 elements of images and text).

```json
{
  "type": "context",
  "elements": [
    { "type": "image", "image_url": "https://example.com/avatar.png", "alt_text": "avatar" },
    { "type": "mrkdwn", "text": "Submitted by <@U012AB3CD> on <!date^1716000000^{date_short}|May 18>" }
  ]
}
```

### 4.7 Input Block

Collects user input. Works in modals, Home tabs, and messages with dispatch_action.

```json
{
  "type": "input",
  "block_id": "title_input",
  "label": { "type": "plain_text", "text": "Issue Title" },
  "element": {
    "type": "plain_text_input",
    "action_id": "title_value",
    "placeholder": { "type": "plain_text", "text": "Enter a descriptive title" },
    "max_length": 150
  },
  "hint": { "type": "plain_text", "text": "Keep it concise but descriptive" },
  "optional": false
}
```

### 4.8 Rich Text Block

Provides structured rich text with formatting preserved.

```json
{
  "type": "rich_text",
  "elements": [
    {
      "type": "rich_text_section",
      "elements": [
        { "type": "text", "text": "Important: ", "style": { "bold": true } },
        { "type": "text", "text": "Review changes before merging." }
      ]
    },
    {
      "type": "rich_text_list",
      "style": "bullet",
      "elements": [
        { "type": "rich_text_section", "elements": [{ "type": "text", "text": "Updated schema" }] },
        { "type": "rich_text_section", "elements": [{ "type": "text", "text": "Added endpoints" }] }
      ]
    }
  ]
}
```

### 4.9 Video Block

```json
{
  "type": "video",
  "title": { "type": "plain_text", "text": "Product Demo" },
  "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
  "thumbnail_url": "https://example.com/thumb.png",
  "alt_text": "Product demonstration video"
}
```

### 4.10 Alert Block (Modals only)

```json
{
  "type": "alert",
  "text": { "type": "plain_text", "text": "This action cannot be undone." },
  "variant": "warning"
}
```

Variants: `info`, `warning`, `danger`, `success`.

### 4.11 Card Block

```json
{
  "type": "card",
  "title": { "type": "plain_text", "text": "Sprint Task" },
  "description": { "type": "mrkdwn", "text": "Implement user auth flow" },
  "thumbnail": { "image_url": "https://example.com/icon.png", "alt_text": "icon" }
}
```

### 4.12 Carousel Block

Horizontally-scrolling container of card blocks.

```json
{
  "type": "carousel",
  "elements": [
    { "type": "card", "title": { "type": "plain_text", "text": "Card 1" } },
    { "type": "card", "title": { "type": "plain_text", "text": "Card 2" } }
  ]
}
```

### 4.13 Data Table Block

```json
{
  "type": "data_table",
  "columns": [
    { "id": "name", "name": "Service", "type": "text" },
    { "id": "status", "name": "Status", "type": "text" }
  ],
  "rows": [
    { "cells": { "name": "API Gateway", "status": "Healthy" } },
    { "cells": { "name": "Payment API", "status": "Degraded" } }
  ]
}
```

### 4.14 Table Block

```json
{
  "type": "table",
  "rows": [
    { "cells": [{ "type": "plain_text", "text": "Service" }, { "type": "plain_text", "text": "Status" }] },
    { "cells": [{ "type": "mrkdwn", "text": "API" }, { "type": "mrkdwn", "text": ":white_check_mark:" }] }
  ]
}
```

### 4.15 File Block (Messages only)

```json
{ "type": "file", "external_id": "ABCDE12345", "source": "remote" }
```

### 4.16 Markdown Block (Messages only)

```json
{ "type": "markdown", "text": "## Heading\n\nThis supports *full* markdown." }
```

### 4.17 Context Actions Block (Messages only)

```json
{
  "type": "context_actions",
  "elements": [
    { "type": "button", "text": { "type": "plain_text", "text": "Helpful" }, "action_id": "helpful" },
    { "type": "button", "text": { "type": "plain_text", "text": "Not Helpful" }, "action_id": "not_helpful" }
  ]
}
```

### 4.18 Plan Block (Messages only)

```json
{
  "type": "plan",
  "title": { "type": "plain_text", "text": "Release Checklist" },
  "sections": [
    {
      "title": { "type": "plain_text", "text": "Pre-release" },
      "items": [
        { "title": { "type": "plain_text", "text": "Run test suite" }, "checked": true },
        { "title": { "type": "plain_text", "text": "Update changelog" }, "checked": false }
      ]
    }
  ]
}
```

### 4.19 Task Card Block (Messages only)

```json
{
  "type": "task_card",
  "title": { "type": "plain_text", "text": "Review PR #423" },
  "description": { "type": "mrkdwn", "text": "Add rate limiting" },
  "status": { "label": { "type": "plain_text", "text": "In Progress" } }
}
```

## 5. Block Kit Elements (Interactive Components)

### 5.1 Button

```json
{
  "type": "button",
  "text": { "type": "plain_text", "text": "Click Me", "emoji": true },
  "action_id": "button_click",
  "value": "click_value",
  "style": "primary",
  "url": "https://example.com",
  "confirm": {
    "title": { "type": "plain_text", "text": "Are you sure?" },
    "text": { "type": "mrkdwn", "text": "This will trigger the deployment." },
    "confirm": { "type": "plain_text", "text": "Yes, deploy" },
    "deny": { "type": "plain_text", "text": "Cancel" }
  }
}
```

Styles: `primary` (green), `danger` (red), or omit for default (grey).

### 5.2 Select Menus

Types: `static_select`, `external_select`, `users_select`, `conversations_select`, `channels_select`.

```json
{
  "type": "static_select",
  "placeholder": { "type": "plain_text", "text": "Choose an option" },
  "action_id": "select_action",
  "options": [
    { "text": { "type": "plain_text", "text": "Option 1" }, "value": "opt_1" },
    { "text": { "type": "plain_text", "text": "Option 2" }, "value": "opt_2" }
  ]
}
```

### 5.3 Multi-Select Menus

Types: `multi_static_select`, `multi_external_select`, `multi_users_select`, `multi_conversations_select`, `multi_channels_select`.

```json
{
  "type": "multi_static_select",
  "placeholder": { "type": "plain_text", "text": "Select labels" },
  "action_id": "label_select",
  "max_selected_items": 5,
  "options": [
    { "text": { "type": "plain_text", "text": "Bug" }, "value": "bug" },
    { "text": { "type": "plain_text", "text": "Feature" }, "value": "feature" }
  ]
}
```

### 5.4 Date Picker

```json
{
  "type": "datepicker",
  "action_id": "date_select",
  "initial_date": "2025-05-29",
  "placeholder": { "type": "plain_text", "text": "Select a date" }
}
```

### 5.5 Time Picker

```json
{
  "type": "timepicker",
  "action_id": "time_select",
  "initial_time": "14:30",
  "placeholder": { "type": "plain_text", "text": "Select time" }
}
```

### 5.6 Datetime Picker

```json
{ "type": "datetimepicker", "action_id": "datetime_select", "initial_date_time": 1716000000 }
```

### 5.7 Overflow Menu

```json
{
  "type": "overflow",
  "action_id": "overflow_menu",
  "options": [
    { "text": { "type": "plain_text", "text": "Edit" }, "value": "edit" },
    { "text": { "type": "plain_text", "text": "Delete" }, "value": "delete" }
  ]
}
```

### 5.8 Radio Buttons

```json
{
  "type": "radio_buttons",
  "action_id": "priority_select",
  "options": [
    { "text": { "type": "plain_text", "text": "Low" }, "value": "low" },
    { "text": { "type": "plain_text", "text": "High" }, "value": "high" }
  ]
}
```

### 5.9 Checkboxes

```json
{
  "type": "checkboxes",
  "action_id": "checklist",
  "options": [
    { "text": { "type": "mrkdwn", "text": "*Code review* completed" }, "value": "review" },
    { "text": { "type": "mrkdwn", "text": "*Tests* passing" }, "value": "tests" }
  ]
}
```

### 5.10 Plain Text Input

```json
{
  "type": "plain_text_input",
  "action_id": "text_input",
  "multiline": true,
  "min_length": 10,
  "max_length": 3000,
  "placeholder": { "type": "plain_text", "text": "Describe the issue..." }
}
```

### 5.11 URL, Email, and Number Inputs

```json
{ "type": "url_text_input", "action_id": "url_input" }
{ "type": "email_text_input", "action_id": "email_input" }
{ "type": "number_input", "action_id": "num_input", "is_decimal_allowed": true, "min_value": "0", "max_value": "100" }
```

### 5.12 Rich Text Input

```json
{ "type": "rich_text_input", "action_id": "rich_text", "placeholder": { "type": "plain_text", "text": "Write here..." } }
```

### 5.13 File Input

```json
{ "type": "file_input", "action_id": "file_upload", "max_files": 5 }
```

## 6. Composition Objects

### Text Object

```json
{ "type": "mrkdwn", "text": "*bold* and _italic_" }
{ "type": "plain_text", "text": "No formatting", "emoji": true }
```

### Confirmation Dialog

```json
{
  "title": { "type": "plain_text", "text": "Confirm Action" },
  "text": { "type": "mrkdwn", "text": "Are you sure you want to proceed?" },
  "confirm": { "type": "plain_text", "text": "Yes" },
  "deny": { "type": "plain_text", "text": "No" },
  "style": "danger"
}
```

### Option Object

```json
{
  "text": { "type": "plain_text", "text": "Option Label" },
  "value": "option_value",
  "description": { "type": "plain_text", "text": "Additional context" }
}
```

### Option Group

```json
{
  "label": { "type": "plain_text", "text": "Group Name" },
  "options": [
    { "text": { "type": "plain_text", "text": "Item 1" }, "value": "item_1" }
  ]
}
```

### Filter Object (for conversation lists)

```json
{
  "include": ["public", "private", "mpim"],
  "exclude_bot_users": true,
  "exclude_external_shared_channels": true
}
```

## 7. Emoji and Reactions System

### Standard Emoji for Technical Communication

| Category | Emoji | Code | Use Case |
|----------|-------|------|----------|
| Status | ✅ | `:white_check_mark:` | Complete, approved |
| Status | ❌ | `:x:` | Failed, rejected |
| Status | ⚠️ | `:warning:` | Caution needed |
| Status | 🚨 | `:rotating_light:` | Critical alert |
| Status | ⏳ | `:hourglass:` | In progress |
| Priority | 🔥 | `:fire:` | Urgent |
| Priority | 🚀 | `:rocket:` | Launch, deploy |
| Feedback | 👍 | `:thumbsup:` | Agreement |
| Feedback | 👀 | `:eyes:` | Reviewing |
| Feedback | 🙌 | `:raised_hands:` | Celebration |
| Process | 📝 | `:memo:` | Documentation |
| Process | ⚙️ | `:gear:` | Configuration |
| Process | 🔒 | `:lock:` | Security |
| Process | 💡 | `:bulb:` | Idea |

### Reactions API

```bash
# Add a reaction
curl -X POST https://slack.com/api/reactions.add \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","timestamp":"1234567890.123456","name":"thumbsup"}'

# Remove a reaction
curl -X POST https://slack.com/api/reactions.remove \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","timestamp":"1234567890.123456","name":"thumbsup"}'

# Get reactions on a message
curl "https://slack.com/api/reactions.get?channel=C012AB3CD&timestamp=1234567890.123456" \
  -H "Authorization: Bearer xoxb-your-token"
```

Note: The `name` field uses the emoji shortcode WITHOUT colons.

### Custom Emoji

Custom emoji can be uploaded by workspace admins:
- Static images (PNG, GIF, JPG) up to 128KB
- Animated GIFs up to 256KB (paid plans)
- Recommended size: 128x128 pixels
- Aliases: multiple names pointing to the same image

Admin API for custom emoji:
```bash
# List all custom emoji
curl "https://slack.com/api/emoji.list" -H "Authorization: Bearer xoxb-your-token"

# Add custom emoji (admin token required)
curl -X POST https://slack.com/api/admin.emoji.add \
  -H "Authorization: Bearer xoxp-admin-token" \
  -F "name=custom_emoji" \
  -F "url=https://example.com/emoji.png"
```

## 8. Web API Essential Methods

### 8.1 Chat Methods

| Method | Description | Rate Tier |
|--------|-------------|-----------|
| `chat.postMessage` | Post a message to a channel | Tier 4 (1/sec per channel) |
| `chat.update` | Update an existing message | Tier 3 |
| `chat.delete` | Delete a message | Tier 3 |
| `chat.postEphemeral` | Post ephemeral message | Tier 4 |
| `chat.scheduleMessage` | Schedule a message | Tier 3 |
| `chat.unfurl` | Provide custom unfurl | Tier 3 |
| `chat.getPermalink` | Get message permalink | Tier 3 |
| `chat.meMessage` | Send /me message | Tier 3 |

### 8.2 Conversations Methods

| Method | Description | Rate Tier |
|--------|-------------|-----------|
| `conversations.list` | List channels | Tier 2 |
| `conversations.info` | Get channel info | Tier 3 |
| `conversations.create` | Create a channel | Tier 2 |
| `conversations.archive` | Archive a channel | Tier 2 |
| `conversations.invite` | Invite users to channel | Tier 3 |
| `conversations.kick` | Remove user from channel | Tier 3 |
| `conversations.join` | Join a channel | Tier 3 |
| `conversations.leave` | Leave a channel | Tier 3 |
| `conversations.members` | List channel members | Tier 3 |
| `conversations.history` | Fetch message history | Tier 3 |
| `conversations.replies` | Fetch thread replies | Tier 3 |
| `conversations.setPurpose` | Set channel purpose | Tier 2 |
| `conversations.setTopic` | Set channel topic | Tier 2 |

### 8.3 Users Methods

| Method | Description | Rate Tier |
|--------|-------------|-----------|
| `users.list` | List all users | Tier 2 |
| `users.info` | Get user info | Tier 4 |
| `users.lookupByEmail` | Find user by email | Tier 3 |
| `users.setPresence` | Set user presence | Tier 2 |
| `users.getPresence` | Get user presence | Tier 3 |
| `users.profile.get` | Get user profile | Tier 4 |
| `users.profile.set` | Set user profile | Tier 3 |

### 8.4 Files Methods

| Method | Description | Rate Tier |
|--------|-------------|-----------|
| `files.upload` | Upload a file | Tier 2 |
| `files.uploadV2` | Upload file (new method) | Tier 2 |
| `files.list` | List files | Tier 3 |
| `files.info` | Get file info | Tier 4 |
| `files.delete` | Delete a file | Tier 3 |
| `files.sharedPublicURL` | Share file publicly | Tier 3 |

### 8.5 Views Methods (Modals)

| Method | Description | Rate Tier |
|--------|-------------|-----------|
| `views.open` | Open a modal | Tier 4 |
| `views.update` | Update a modal | Tier 4 |
| `views.push` | Push a new view onto stack | Tier 4 |
| `views.publish` | Publish Home tab | Tier 4 |

## 9. Posting Messages - Complete Examples

### Basic Message with Blocks

```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C012AB3CD",
    "text": "Deployment complete - api-gateway v2.5.0 to production",
    "blocks": [
      {
        "type": "header",
        "text": { "type": "plain_text", "text": "Deployment Complete :rocket:" }
      },
      {
        "type": "section",
        "fields": [
          { "type": "mrkdwn", "text": "*Service:*\n`api-gateway`" },
          { "type": "mrkdwn", "text": "*Environment:*\nProduction" },
          { "type": "mrkdwn", "text": "*Version:*\nv2.4.1 → v2.5.0" },
          { "type": "mrkdwn", "text": "*Duration:*\n3m 42s" }
        ]
      },
      {
        "type": "context",
        "elements": [
          { "type": "mrkdwn", "text": "Triggered by <@U012AB3CD> via GitHub Actions | <https://github.com/org/repo/actions/runs/123|View Run>" }
        ]
      }
    ],
    "unfurl_links": false,
    "unfurl_media": false
  }'
```

### Ephemeral Message

```bash
curl -X POST https://slack.com/api/chat.postEphemeral \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C012AB3CD",
    "user": "U012AB3CD",
    "text": "Only you can see this message"
  }'
```

### Threaded Reply

```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C012AB3CD",
    "thread_ts": "1234567890.123456",
    "text": "This is a threaded reply",
    "reply_broadcast": false
  }'
```

### Scheduled Message

```bash
curl -X POST https://slack.com/api/chat.scheduleMessage \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C012AB3CD",
    "text": "Good morning! Daily standup in 15 minutes.",
    "post_at": 1716800000
  }'
```

## 10. Modals

### Opening a Modal

```bash
curl -X POST https://slack.com/api/views.open \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "trigger_id": "12345.98765.abcd2358fdea",
    "view": {
      "type": "modal",
      "callback_id": "create_ticket",
      "title": { "type": "plain_text", "text": "Create Ticket" },
      "submit": { "type": "plain_text", "text": "Submit" },
      "close": { "type": "plain_text", "text": "Cancel" },
      "blocks": [
        {
          "type": "input",
          "block_id": "title_block",
          "label": { "type": "plain_text", "text": "Title" },
          "element": { "type": "plain_text_input", "action_id": "title_input" }
        },
        {
          "type": "input",
          "block_id": "priority_block",
          "label": { "type": "plain_text", "text": "Priority" },
          "element": {
            "type": "static_select",
            "action_id": "priority_select",
            "options": [
              { "text": { "type": "plain_text", "text": "Low" }, "value": "low" },
              { "text": { "type": "plain_text", "text": "Medium" }, "value": "medium" },
              { "text": { "type": "plain_text", "text": "High" }, "value": "high" }
            ]
          }
        },
        {
          "type": "input",
          "block_id": "desc_block",
          "label": { "type": "plain_text", "text": "Description" },
          "element": { "type": "plain_text_input", "action_id": "desc_input", "multiline": true },
          "optional": true
        }
      ]
    }
  }'
```

### Handling Modal Submission

When a user submits a modal, Slack sends a `view_submission` payload. Your app must respond within 3 seconds with one of:

```json
{"response_action": "clear"}
```

```json
{"response_action": "update", "view": { "type": "modal", "title": {...}, "blocks": [...] }}
```

```json
{"response_action": "push", "view": { "type": "modal", "title": {...}, "blocks": [...] }}
```

```json
{"response_action": "errors", "errors": {"title_block": "Title is required"}}
```

## 11. Home Tab

```bash
curl -X POST https://slack.com/api/views.publish \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "U012AB3CD",
    "view": {
      "type": "home",
      "blocks": [
        { "type": "header", "text": { "type": "plain_text", "text": "Welcome to AppBot" } },
        { "type": "section", "text": { "type": "mrkdwn", "text": "Your active tasks:" } },
        { "type": "divider" },
        {
          "type": "section",
          "text": { "type": "mrkdwn", "text": ":memo: *Review PR #423*\nDue: Today" },
          "accessory": {
            "type": "button",
            "text": { "type": "plain_text", "text": "Open" },
            "url": "https://github.com/org/repo/pull/423",
            "action_id": "open_pr"
          }
        }
      ]
    }
  }'
```

## 12. Slash Commands

### Incoming Payload

When a user types `/deploy production api-gateway v2.5.0`, Slack sends:

```json
{
  "token": "verification_token",
  "team_id": "T012AB3CD",
  "channel_id": "C012AB3CD",
  "user_id": "U012AB3CD",
  "command": "/deploy",
  "text": "production api-gateway v2.5.0",
  "response_url": "https://hooks.slack.com/commands/T012/123/abc",
  "trigger_id": "12345.98765.abcd"
}
```

### Response Types

- `in_channel` — visible to everyone
- `ephemeral` — visible only to the invoking user

For operations taking longer than 3 seconds, acknowledge immediately with HTTP 200 and use the `response_url` to send up to 5 follow-up messages within 30 minutes.

## 13. Incoming Webhooks

```bash
curl -X POST https://hooks.slack.com/services/TXXXXX/BXXXXX/your-webhook-token \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Alert: CPU usage exceeded 90%",
    "blocks": [
      {
        "type": "section",
        "text": { "type": "mrkdwn", "text": ":rotating_light: *CPU Alert*\nServer `prod-web-03` at *94%* for 5 minutes." }
      },
      {
        "type": "actions",
        "elements": [
          { "type": "button", "text": { "type": "plain_text", "text": "View Dashboard" }, "url": "https://grafana.example.com/d/cpu", "action_id": "view_dashboard" }
        ]
      }
    ]
  }'
```

## 14. Rate Limits

| Tier | Rate | Common Methods |
|------|------|----------------|
| Tier 1 | 1 request/min | admin.*, some legacy |
| Tier 2 | 20 requests/min | files.upload, conversations.create |
| Tier 3 | 50 requests/min | conversations.list, users.list |
| Tier 4 | 100+ requests/min | chat.postMessage, reactions.add |
| Special | 1 request/sec | chat.postMessage per channel |

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 98
X-RateLimit-Reset: 1716000060
Retry-After: 30  (only on 429 responses)
```

## 15. Production Message Templates

### Incident Alert

```json
{
  "blocks": [
    { "type": "header", "text": { "type": "plain_text", "text": ":rotating_light: Incident Detected" } },
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": "*Severity:* P1 - Critical\n*Service:* Payment Processing\n*Impact:* Users unable to complete checkout" }
    },
    {
      "type": "actions",
      "elements": [
        { "type": "button", "text": { "type": "plain_text", "text": "Acknowledge" }, "style": "primary", "action_id": "ack_incident" },
        { "type": "button", "text": { "type": "plain_text", "text": "Escalate" }, "style": "danger", "action_id": "escalate" }
      ]
    }
  ]
}
```

### PR Review Request

```json
{
  "blocks": [
    {
      "type": "section",
      "text": { "type": "mrkdwn", "text": ":mag: *Code Review Requested*\n<https://github.com/org/repo/pull/423|#423 - Add rate limiting>\n_+342 / -28 lines across 5 files_" }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Author:*\n<@U012AB3CD>" },
        { "type": "mrkdwn", "text": "*CI:*\n:white_check_mark: Passing" }
      ]
    }
  ]
}
```

### Daily Standup

```json
{
  "blocks": [
    { "type": "header", "text": { "type": "plain_text", "text": ":calendar: Daily Standup - May 29, 2025" } },
    { "type": "divider" },
    { "type": "section", "text": { "type": "mrkdwn", "text": "*<@U001> Alice*\n• _Yesterday:_ Completed rate limiting PR\n• _Today:_ Database migration\n• _Blockers:_ None" } },
    { "type": "section", "text": { "type": "mrkdwn", "text": "*<@U002> Bob*\n• _Yesterday:_ Fixed webhook timeout\n• _Today:_ Load testing\n• _Blockers:_ Need staging Redis access" } }
  ]
}
```

## 16. Accessibility Best Practices

When posting messages with blocks, screen readers default to reading the top-level `text` field. To ensure accessibility:

1. Always include a meaningful `text` field alongside `blocks`
2. Provide descriptive `alt_text` for all images
3. Use `plain_text` for critical information
4. Avoid conveying meaning through color or emoji alone
5. Structure blocks in a logical reading order

## 17. Token Types

| Token Type | Prefix | Use Case |
|-----------|--------|----------|
| Bot token | `xoxb-` | App actions on behalf of the bot |
| User token | `xoxp-` | Actions on behalf of a user |
| App-level token | `xapp-` | Socket Mode, connections |
| Webhook URL | `https://hooks.slack.com/...` | Simple message posting |
| Signing secret | (hex string) | Request verification |

## 18. Request Verification

Verify incoming requests using the signing secret:

```python
import hashlib
import hmac
import time

def verify_slack_request(signing_secret, timestamp, body, signature):
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False  # Request too old
    sig_basestring = f"v0:{timestamp}:{body}"
    my_signature = "v0=" + hmac.new(
        signing_secret.encode(), sig_basestring.encode(), hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(my_signature, signature)
```

Headers to check: `X-Slack-Request-Timestamp` and `X-Slack-Signature`.

## 19. Events API

The Events API allows your app to receive real-time notifications about events in Slack workspaces. Events are delivered via HTTP POST to your configured Request URL.

### Event Subscription Types

| Event | Description | Scope Required |
|-------|-------------|----------------|
| `message.channels` | Message posted to public channel | `channels:history` |
| `message.groups` | Message posted to private channel | `groups:history` |
| `message.im` | Message posted in DM | `im:history` |
| `message.mpim` | Message posted in group DM | `mpim:history` |
| `app_mention` | App mentioned in a message | `app_mentions:read` |
| `member_joined_channel` | User joined a channel | `channels:read` |
| `member_left_channel` | User left a channel | `channels:read` |
| `channel_created` | New channel created | `channels:read` |
| `reaction_added` | Reaction added to message | `reactions:read` |
| `reaction_removed` | Reaction removed from message | `reactions:read` |
| `app_home_opened` | User opened app Home tab | None |
| `file_shared` | File shared in channel | `files:read` |
| `team_join` | New user joined workspace | `users:read` |
| `user_change` | User profile updated | `users:read` |
| `workflow_step_execute` | Workflow step triggered | `workflow.steps:execute` |

### Event Envelope Structure

```json
{
  "token": "verification_token",
  "team_id": "T012AB3CD",
  "api_app_id": "A012AB3CD",
  "event": {
    "type": "message",
    "subtype": null,
    "channel": "C012AB3CD",
    "user": "U012AB3CD",
    "text": "Hello world",
    "ts": "1234567890.123456",
    "event_ts": "1234567890.123456",
    "channel_type": "channel"
  },
  "type": "event_callback",
  "event_id": "Ev012AB3CD",
  "event_time": 1234567890,
  "authorizations": [
    {
      "enterprise_id": "E012AB3CD",
      "team_id": "T012AB3CD",
      "user_id": "U012AB3CD",
      "is_bot": true,
      "is_enterprise_install": false
    }
  ]
}
```

### URL Verification Challenge

When you first configure your Request URL, Slack sends a challenge:

```json
{ "token": "verification_token", "challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P", "type": "url_verification" }
```

Your app must respond with: `{"challenge": "3eZbrw1aBm2rZgRNFdxV2595E9CY3gmdALWMmHkvFXO7tYXAYM8P"}`

### Best Practices for Events

1. Respond with HTTP 200 within 3 seconds (acknowledge receipt)
2. Process events asynchronously (queue for processing)
3. Handle duplicate events (use `event_id` for deduplication)
4. Implement retry logic (Slack retries after failures with `X-Slack-Retry-Num` header)
5. Filter by `subtype` to ignore bot messages and avoid loops

## 20. Socket Mode

Socket Mode allows your app to receive events over a WebSocket connection instead of HTTP, eliminating the need for a public URL.

### Setup

```bash
# Install the Slack SDK
pip install slack-sdk

# Or for Node.js
npm install @slack/socket-mode @slack/bolt
```

### Python Example

```python
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.web import WebClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse

client = SocketModeClient(
    app_token="xapp-1-A012AB3CD-1234567890-abcdef",
    web_client=WebClient(token="xoxb-your-bot-token")
)

def handle_events(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        event = req.payload["event"]
        if event["type"] == "app_mention":
            client.web_client.chat_postMessage(
                channel=event["channel"],
                thread_ts=event["ts"],
                text=f"Hello <@{event['user']}>! How can I help?"
            )
    client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))

client.socket_mode_request_listeners.append(handle_events)
client.connect()

import time
while True:
    time.sleep(1)
```

### Node.js Bolt Example

```javascript
const { App } = require('@slack/bolt');

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  appToken: process.env.SLACK_APP_TOKEN,
  socketMode: true,
});

app.event('app_mention', async ({ event, say }) => {
  await say({
    thread_ts: event.ts,
    text: `Hello <@${event.user}>! How can I help?`
  });
});

app.command('/deploy', async ({ command, ack, respond }) => {
  await ack();
  const [env, service, version] = command.text.split(' ');
  await respond({
    response_type: 'in_channel',
    text: `Deploying ${service} ${version} to ${env}...`
  });
});

(async () => { await app.start(); console.log('App running'); })();
```

## 21. Workflow Builder and Automation

### Workflow Steps from Apps (Legacy)

Apps can contribute custom steps to Workflow Builder:

```python
@app.step("create_ticket")
def handle_step(ack, step, configure, update, fail):
    ack()
    # Step configuration
    inputs = step["inputs"]
    title = inputs["title"]["value"]
    priority = inputs["priority"]["value"]
    # Process the step
    try:
        ticket_id = create_jira_ticket(title, priority)
        update(outputs=[{"name": "ticket_id", "value": ticket_id}])
    except Exception as e:
        fail(error={"message": str(e)})
```

### New Platform Functions (Next-Gen)

Slack's next-generation platform uses Deno-based functions:

```typescript
import { DefineFunction, Schema, SlackFunction } from "deno-slack-sdk/mod.ts";

export const CreateTicketFunction = DefineFunction({
  callback_id: "create_ticket",
  title: "Create Ticket",
  source_file: "functions/create_ticket.ts",
  input_parameters: {
    properties: {
      title: { type: Schema.types.string, description: "Ticket title" },
      priority: { type: Schema.types.string, enum: ["low", "medium", "high"] },
      reporter: { type: Schema.slack.types.user_id }
    },
    required: ["title", "priority", "reporter"]
  },
  output_parameters: {
    properties: {
      ticket_id: { type: Schema.types.string },
      ticket_url: { type: Schema.types.string }
    },
    required: ["ticket_id"]
  }
});

export default SlackFunction(CreateTicketFunction, async ({ inputs, client }) => {
  const { title, priority, reporter } = inputs;
  const ticketId = `TICK-${Date.now()}`;
  
  await client.chat.postMessage({
    channel: reporter,
    text: `Ticket ${ticketId} created: ${title} (${priority})`
  });
  
  return { outputs: { ticket_id: ticketId, ticket_url: `https://tickets.example.com/${ticketId}` } };
});
```

## 22. Slack Connect (Cross-Organization Channels)

Slack Connect allows organizations to communicate in shared channels. Key considerations:

- Shared channels have a `is_shared` flag set to true
- External users have `is_stranger` flag in user objects
- Messages from external users include `team` field with their workspace ID
- File sharing can be restricted across organizations
- Apps need `channels:read` scope to see shared channel membership
- DLP and compliance policies apply per-organization

### Identifying External Users

```python
def is_external_user(user_info, my_team_id):
    return user_info.get("team_id") != my_team_id

# Check in message events
if event.get("team") and event["team"] != MY_TEAM_ID:
    # Message from external user
    pass
```

## 23. File Uploads

### Modern Upload (files.uploadV2)

```bash
# Step 1: Get upload URL
curl -X POST https://slack.com/api/files.getUploadURLExternal \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{"filename":"report.pdf","length":1048576}'

# Step 2: Upload to the returned URL
curl -X POST "https://files.slack.com/upload/v1/..." \
  -F "file=@report.pdf"

# Step 3: Complete upload
curl -X POST https://slack.com/api/files.completeUploadExternal \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "files": [{"id":"F012AB3CD","title":"Monthly Report"}],
    "channel_id": "C012AB3CD",
    "initial_comment": "Here is the monthly report :memo:"
  }'
```

### File Sharing Snippet (Code)

```bash
curl -X POST https://slack.com/api/files.upload \
  -H "Authorization: Bearer xoxb-your-token" \
  -F "channels=C012AB3CD" \
  -F "content=def hello():\n    print('Hello, World!')" \
  -F "filename=hello.py" \
  -F "filetype=python" \
  -F "title=Hello World Script" \
  -F "initial_comment=Here's the code snippet you requested"
```

## 24. Interactivity Payloads

When users interact with Block Kit elements, Slack sends interaction payloads to your configured Interactivity Request URL.

### Payload Types

| Type | Trigger |
|------|---------|
| `block_actions` | User clicks button, selects option, etc. |
| `view_submission` | User submits a modal |
| `view_closed` | User closes a modal |
| `shortcut` | User triggers a global or message shortcut |
| `message_action` | User triggers a message action (legacy) |

### block_actions Payload

```json
{
  "type": "block_actions",
  "user": { "id": "U012AB3CD", "username": "johndoe", "name": "John Doe" },
  "trigger_id": "12345.98765.abcd",
  "channel": { "id": "C012AB3CD", "name": "general" },
  "message": { "ts": "1234567890.123456", "text": "Original message" },
  "actions": [
    {
      "type": "button",
      "action_id": "approve_request",
      "block_id": "actions_block",
      "text": { "type": "plain_text", "text": "Approve" },
      "value": "req_001",
      "action_ts": "1234567890.123456"
    }
  ]
}
```

### Responding to Interactions

1. Acknowledge with HTTP 200 within 3 seconds
2. Use `response_url` for follow-up messages (up to 5 within 30 min)
3. Use `trigger_id` to open modals (valid for 3 seconds)
4. Update the original message by returning a new message payload

## 25. App Distribution and OAuth

### OAuth 2.0 Flow

```
1. User clicks "Add to Slack" button
2. Redirect to: https://slack.com/oauth/v2/authorize?client_id=CLIENT_ID&scope=SCOPES&redirect_uri=REDIRECT_URI
3. User authorizes the app
4. Slack redirects to your redirect_uri with a code parameter
5. Exchange code for token:
   POST https://slack.com/api/oauth.v2.access
   client_id=CLIENT_ID&client_secret=CLIENT_SECRET&code=CODE&redirect_uri=REDIRECT_URI
6. Store the returned access_token (xoxb-...) and team info
```

### Bot Token Scopes (Common)

| Scope | Grants |
|-------|--------|
| `chat:write` | Post messages as the bot |
| `chat:write.public` | Post to channels without joining |
| `channels:read` | View public channel info |
| `channels:history` | Read public channel messages |
| `groups:read` | View private channel info |
| `im:read` | View DM info |
| `im:write` | Send DMs |
| `users:read` | View user info |
| `users:read.email` | View user email addresses |
| `reactions:read` | View reactions |
| `reactions:write` | Add/remove reactions |
| `files:read` | View files |
| `files:write` | Upload/modify files |
| `commands` | Add slash commands |
| `app_mentions:read` | Receive app_mention events |

## 26. Bolt Framework Patterns

### Python Bolt

```python
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Listen for messages containing "hello"
@app.message("hello")
def handle_hello(message, say):
    say(f"Hey there <@{message['user']}>!")

# Listen for slash command
@app.command("/ticket")
def handle_ticket(ack, command, client):
    ack()
    client.views_open(
        trigger_id=command["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "ticket_modal",
            "title": {"type": "plain_text", "text": "New Ticket"},
            "submit": {"type": "plain_text", "text": "Create"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "title_block",
                    "label": {"type": "plain_text", "text": "Title"},
                    "element": {"type": "plain_text_input", "action_id": "title_input"}
                }
            ]
        }
    )

# Handle modal submission
@app.view("ticket_modal")
def handle_submission(ack, body, client, view):
    title = view["state"]["values"]["title_block"]["title_input"]["value"]
    user = body["user"]["id"]
    ack()
    client.chat_postMessage(
        channel=user,
        text=f"Ticket created: {title}"
    )

# Handle button click
@app.action("approve_request")
def handle_approve(ack, body, client):
    ack()
    client.chat_update(
        channel=body["channel"]["id"],
        ts=body["message"]["ts"],
        text="Request approved!",
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": ":white_check_mark: *Approved* by <@" + body["user"]["id"] + ">"}
            }
        ]
    )

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
```

### JavaScript Bolt

```javascript
const { App } = require('@slack/bolt');

const app = new App({
  token: process.env.SLACK_BOT_TOKEN,
  signingSecret: process.env.SLACK_SIGNING_SECRET,
});

// Respond to app_mention
app.event('app_mention', async ({ event, client }) => {
  await client.chat.postMessage({
    channel: event.channel,
    thread_ts: event.ts,
    blocks: [
      {
        type: 'section',
        text: { type: 'mrkdwn', text: `Hi <@${event.user}>! What can I help with?` },
        accessory: {
          type: 'button',
          text: { type: 'plain_text', text: 'Open Help' },
          action_id: 'open_help'
        }
      }
    ]
  });
});

// Handle overflow menu selection
app.action('task_overflow', async ({ ack, action, body, client }) => {
  await ack();
  const selectedValue = action.selected_option.value;
  if (selectedValue === 'delete') {
    await client.chat.delete({
      channel: body.channel.id,
      ts: body.message.ts
    });
  }
});

(async () => { await app.start(3000); })();
```

## 27. Admin API (Enterprise Grid)

### User Management

```bash
# Invite a user to workspace
curl -X POST https://slack.com/api/admin.users.invite \
  -H "Authorization: Bearer xoxp-admin-token" \
  -H "Content-Type: application/json" \
  -d '{"team_id":"T012AB3CD","email":"new.user@company.com","channel_ids":"C012AB3CD,C034EF5GH"}'

# Deactivate a user
curl -X POST https://slack.com/api/admin.users.remove \
  -H "Authorization: Bearer xoxp-admin-token" \
  -H "Content-Type: application/json" \
  -d '{"team_id":"T012AB3CD","user_id":"U012AB3CD"}'

# Set user to admin
curl -X POST https://slack.com/api/admin.users.setAdmin \
  -H "Authorization: Bearer xoxp-admin-token" \
  -H "Content-Type: application/json" \
  -d '{"team_id":"T012AB3CD","user_id":"U012AB3CD"}'
```

### Channel Management

```bash
# Archive a channel
curl -X POST https://slack.com/api/admin.conversations.archive \
  -H "Authorization: Bearer xoxp-admin-token" \
  -H "Content-Type: application/json" \
  -d '{"channel_id":"C012AB3CD"}'

# Set channel retention
curl -X POST https://slack.com/api/admin.conversations.setCustomRetention \
  -H "Authorization: Bearer xoxp-admin-token" \
  -H "Content-Type: application/json" \
  -d '{"channel_id":"C012AB3CD","duration_days":90}'
```

## 28. Slack App Manifest

Define your entire app configuration in YAML:

```yaml
display_information:
  name: DeployBot
  description: Automated deployment notifications and controls
  background_color: "#2c2d30"
  long_description: "DeployBot provides real-time deployment notifications, rollback controls, and environment status monitoring for your engineering team."

features:
  bot_user:
    display_name: DeployBot
    always_online: true
  slash_commands:
    - command: /deploy
      url: https://your-app.example.com/slack/commands
      description: Trigger a deployment
      usage_hint: "[environment] [service] [version]"
      should_escape: false
    - command: /rollback
      url: https://your-app.example.com/slack/commands
      description: Rollback a deployment
      usage_hint: "[service] [version]"
  shortcuts:
    - name: Create Incident
      type: global
      callback_id: create_incident
      description: Create a new incident report

oauth_config:
  scopes:
    bot:
      - chat:write
      - chat:write.public
      - commands
      - channels:read
      - channels:history
      - reactions:write
      - users:read
      - app_mentions:read
      - files:write

settings:
  event_subscriptions:
    request_url: https://your-app.example.com/slack/events
    bot_events:
      - app_mention
      - message.channels
      - reaction_added
  interactivity:
    is_enabled: true
    request_url: https://your-app.example.com/slack/interactions
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```

## 29. Message Unfurling

When URLs are posted in Slack, apps can provide custom unfurls:

```python
@app.event("link_shared")
def handle_link_shared(event, client):
    links = event["links"]
    unfurls = {}
    
    for link in links:
        url = link["url"]
        if "jira.example.com" in url:
            ticket = fetch_jira_ticket(url)
            unfurls[url] = {
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*{ticket['key']}*: {ticket['summary']}\nStatus: {ticket['status']} | Priority: {ticket['priority']}"
                        }
                    }
                ]
            }
    
    client.chat_unfurl(
        channel=event["channel"],
        ts=event["message_ts"],
        unfurls=unfurls
    )
```

## 30. Search API

```bash
# Search messages
curl "https://slack.com/api/search.messages?query=deployment+failed&sort=timestamp&sort_dir=desc&count=20" \
  -H "Authorization: Bearer xoxp-user-token"

# Search files
curl "https://slack.com/api/search.files?query=report+Q1+2025&types=pdf,xlsx" \
  -H "Authorization: Bearer xoxp-user-token"
```

Note: Search requires a user token (xoxp-), not a bot token.

## 31. User Groups (Teams/Handles)

```bash
# Create a user group
curl -X POST https://slack.com/api/usergroups.create \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{"name":"On-Call Engineers","handle":"oncall","description":"Current on-call rotation"}'

# Update members
curl -X POST https://slack.com/api/usergroups.users.update \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{"usergroup":"S012AB3CD","users":"U001,U002,U003"}'

# List user groups
curl "https://slack.com/api/usergroups.list?include_users=true" \
  -H "Authorization: Bearer xoxb-your-token"
```

## 32. Bookmarks API

```bash
# Add a bookmark to a channel
curl -X POST https://slack.com/api/bookmarks.add \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_id": "C012AB3CD",
    "title": "Runbook",
    "type": "link",
    "link": "https://wiki.example.com/runbook",
    "emoji": ":book:"
  }'
```

## 33. Reminders API

```bash
# Set a reminder
curl -X POST https://slack.com/api/reminders.add \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Review the PR before end of day",
    "time": "in 2 hours",
    "user": "U012AB3CD"
  }'

# List reminders
curl "https://slack.com/api/reminders.list" \
  -H "Authorization: Bearer xoxb-your-token"
```

## 34. Pins and Stars

```bash
# Pin a message
curl -X POST https://slack.com/api/pins.add \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{"channel":"C012AB3CD","timestamp":"1234567890.123456"}'

# List pinned items
curl "https://slack.com/api/pins.list?channel=C012AB3CD" \
  -H "Authorization: Bearer xoxb-your-token"
```

## 35. Best Practices Summary

| Area | Best Practice |
|------|--------------|
| Formatting | Use mrkdwn sparingly; prefer clarity over decoration |
| Blocks | Always include fallback `text` field with blocks |
| Buttons | Limit to 5 buttons per actions block for usability |
| Modals | Keep to 3-5 input fields; use multi-step for complex forms |
| Rate limits | Implement exponential backoff; respect Retry-After header |
| Threads | Use threads for detailed discussions; keep channels clean |
| Emoji | Use reactions for quick feedback instead of reply messages |
| Webhooks | Validate webhook URLs; never expose in client-side code |
| Tokens | Use bot tokens (xoxb-) for app actions; never expose in logs |
| Error handling | Always check `ok` field in API responses |
| Events | Acknowledge within 3 seconds; process asynchronously |
| Socket Mode | Use for development and apps without public URLs |
| Unfurls | Cache external data to avoid rate limits |
| Accessibility | Always provide alt_text and fallback text |
| Security | Verify request signatures on all incoming payloads |

## 36. Conversation Canvas

Canvases are collaborative documents embedded within channels. They support rich formatting, checklists, code blocks, and embedded Slack content.

### Creating a Canvas

```bash
curl -X POST https://slack.com/api/canvases.create \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sprint Planning - Week 22",
    "document_content": {
      "type": "markdown",
      "markdown": "# Sprint Planning\n\n## Goals\n- [ ] Complete API rate limiting\n- [ ] Deploy monitoring stack\n- [ ] Review security audit findings\n\n## Notes\nPlease add your items below."
    }
  }'
```

### Canvas Sections API

```bash
# Edit canvas sections
curl -X POST https://slack.com/api/canvases.sections.lookup \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{"canvas_id":"F012AB3CD","criteria":{"section_types":["any_header"],"contains_text":"Goals"}}'
```

## 37. Status and Presence

### Setting User Status

```bash
curl -X POST https://slack.com/api/users.profile.set \
  -H "Authorization: Bearer xoxp-user-token" \
  -H "Content-Type: application/json" \
  -d '{
    "profile": {
      "status_text": "In a meeting",
      "status_emoji": ":calendar:",
      "status_expiration": 1716003600
    }
  }'
```

### Common Status Patterns for Engineering Teams

| Status | Emoji | Text | Duration |
|--------|-------|------|----------|
| Focus time | `:headphones:` | "Deep work - no interruptions" | 2 hours |
| In meeting | `:calendar:` | "In a meeting" | Until meeting ends |
| On call | `:pager:` | "On-call rotation" | 24 hours |
| Deploying | `:rocket:` | "Deploying to production" | 30 minutes |
| Lunch | `:hamburger:` | "Lunch break" | 1 hour |
| PTO | `:palm_tree:` | "Out of office" | Days |
| Sick | `:face_with_thermometer:` | "Out sick" | Days |
| Commuting | `:bus:` | "Commuting" | 1 hour |

### Do Not Disturb

```bash
# Set DND for 2 hours
curl -X POST https://slack.com/api/dnd.setSnooze \
  -H "Authorization: Bearer xoxp-user-token" \
  -H "Content-Type: application/json" \
  -d '{"num_minutes":120}'

# End DND
curl -X POST https://slack.com/api/dnd.endSnooze \
  -H "Authorization: Bearer xoxp-user-token"

# Check DND status
curl "https://slack.com/api/dnd.info?user=U012AB3CD" \
  -H "Authorization: Bearer xoxb-your-token"
```

## 38. Channel Management Patterns

### Naming Conventions

| Pattern | Example | Use Case |
|---------|---------|----------|
| `#team-{name}` | `#team-platform` | Team channels |
| `#proj-{name}` | `#proj-migration` | Project channels |
| `#inc-{id}` | `#inc-2025-0042` | Incident channels |
| `#help-{topic}` | `#help-kubernetes` | Support channels |
| `#announce-{scope}` | `#announce-engineering` | Announcements (restricted posting) |
| `#ext-{company}` | `#ext-acme-corp` | Slack Connect channels |
| `#bot-{name}` | `#bot-alerts` | Bot notification channels |
| `#tmp-{purpose}` | `#tmp-hackathon-2025` | Temporary channels |

### Automated Channel Creation for Incidents

```python
async def create_incident_channel(client, incident_id, severity, title):
    channel_name = f"inc-{incident_id}"
    
    # Create the channel
    result = await client.conversations_create(name=channel_name, is_private=False)
    channel_id = result["channel"]["id"]
    
    # Set topic
    await client.conversations_setTopic(
        channel=channel_id,
        topic=f"P{severity} | {title} | Status: Investigating"
    )
    
    # Set purpose
    await client.conversations_setPurpose(
        channel=channel_id,
        purpose=f"Incident {incident_id}: {title}. See pinned message for details."
    )
    
    # Invite on-call team
    oncall_users = get_oncall_users()
    await client.conversations_invite(channel=channel_id, users=",".join(oncall_users))
    
    # Post initial message and pin it
    msg = await client.chat_postMessage(
        channel=channel_id,
        blocks=[
            {"type": "header", "text": {"type": "plain_text", "text": f":rotating_light: Incident {incident_id}"}},
            {"type": "section", "fields": [
                {"type": "mrkdwn", "text": f"*Severity:* P{severity}"},
                {"type": "mrkdwn", "text": f"*Title:* {title}"},
                {"type": "mrkdwn", "text": f"*Status:* Investigating"},
                {"type": "mrkdwn", "text": f"*Commander:* TBD"}
            ]},
            {"type": "actions", "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": "Claim Commander"}, "style": "primary", "action_id": "claim_commander"},
                {"type": "button", "text": {"type": "plain_text", "text": "Update Status"}, "action_id": "update_status"},
                {"type": "button", "text": {"type": "plain_text", "text": "Resolve"}, "style": "danger", "action_id": "resolve_incident"}
            ]}
        ]
    )
    
    await client.pins_add(channel=channel_id, timestamp=msg["ts"])
    return channel_id
```

## 39. Message Metadata

Attach structured metadata to messages for programmatic handling:

```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer xoxb-your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "C012AB3CD",
    "text": "Deployment started for api-gateway",
    "metadata": {
      "event_type": "deployment_started",
      "event_payload": {
        "service": "api-gateway",
        "version": "v2.5.0",
        "environment": "production",
        "triggered_by": "U012AB3CD",
        "commit_sha": "abc123def456"
      }
    }
  }'
```

Subscribe to metadata events:
```json
{
  "type": "event_callback",
  "event": {
    "type": "message_metadata_posted",
    "metadata": {
      "event_type": "deployment_started",
      "event_payload": { "service": "api-gateway", "version": "v2.5.0" }
    }
  }
}
```

## 40. Pagination

All list methods use cursor-based pagination:

```python
def get_all_channels(client):
    channels = []
    cursor = None
    
    while True:
        result = client.conversations_list(
            types="public_channel,private_channel",
            limit=200,
            cursor=cursor
        )
        channels.extend(result["channels"])
        
        cursor = result.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
    
    return channels
```

Key pagination parameters:
- `limit`: Number of items per page (max varies by method, typically 100-1000)
- `cursor`: Opaque string for the next page
- Response includes `response_metadata.next_cursor` (empty string means no more pages)

## 41. Error Handling

### Common Error Codes

| Error | Meaning | Resolution |
|-------|---------|------------|
| `not_authed` | No token provided | Include Authorization header |
| `invalid_auth` | Token is invalid | Regenerate token |
| `token_revoked` | Token was revoked | Re-authorize the app |
| `channel_not_found` | Channel doesn't exist or bot not in it | Join channel or check ID |
| `not_in_channel` | Bot not a member | Invite bot to channel |
| `is_archived` | Channel is archived | Unarchive or use different channel |
| `msg_too_long` | Message exceeds 40,000 chars | Split into multiple messages |
| `too_many_attachments` | More than 50 blocks | Reduce block count |
| `rate_limited` | Hit rate limit | Wait for Retry-After seconds |
| `missing_scope` | Token lacks required scope | Add scope and re-authorize |
| `user_not_found` | Invalid user ID | Verify user ID exists |
| `invalid_blocks` | Block Kit JSON is malformed | Validate with Block Kit Builder |
| `no_text` | Message has no text or blocks | Include text or blocks field |
| `ekm_access_denied` | EKM key not available | Contact workspace admin |

### Robust Error Handling Pattern

```python
import time
from slack_sdk.errors import SlackApiError

def post_message_with_retry(client, channel, text, blocks=None, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = client.chat_postMessage(
                channel=channel,
                text=text,
                blocks=blocks
            )
            if result["ok"]:
                return result
        except SlackApiError as e:
            error = e.response["error"]
            
            if error == "rate_limited":
                retry_after = int(e.response.headers.get("Retry-After", 30))
                time.sleep(retry_after)
                continue
            elif error == "not_in_channel":
                client.conversations_join(channel=channel)
                continue
            elif error == "channel_not_found":
                raise ValueError(f"Channel {channel} not found")
            elif error in ("token_revoked", "invalid_auth"):
                raise AuthenticationError("Token invalid, re-auth required")
            else:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise
    
    raise RuntimeError(f"Failed after {max_retries} attempts")
```

## 42. Unfurl Domains

Register domains your app can unfurl:

```yaml
# In app manifest
features:
  unfurl_domains:
    - "jira.example.com"
    - "confluence.example.com"
    - "github.com"
```

When a URL matching your registered domain is posted, Slack sends a `link_shared` event. Your app has 30 minutes to provide an unfurl.

## 43. Message Scheduling Patterns

### Recurring Messages (Using External Scheduler)

```python
import schedule
import time

def post_standup_reminder():
    client.chat_postMessage(
        channel="C012AB3CD",
        text="Time for standup! Please post your update.",
        blocks=[
            {"type": "header", "text": {"type": "plain_text", "text": ":calendar: Daily Standup"}},
            {"type": "section", "text": {"type": "mrkdwn", "text": "Please share:\n• What you did yesterday\n• What you're doing today\n• Any blockers"}},
            {"type": "actions", "elements": [
                {"type": "button", "text": {"type": "plain_text", "text": "Post Update"}, "action_id": "post_standup", "style": "primary"}
            ]}
        ]
    )

schedule.every().monday.at("09:00").do(post_standup_reminder)
schedule.every().tuesday.at("09:00").do(post_standup_reminder)
schedule.every().wednesday.at("09:00").do(post_standup_reminder)
schedule.every().thursday.at("09:00").do(post_standup_reminder)
schedule.every().friday.at("09:00").do(post_standup_reminder)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 44. Channel Topic and Purpose Automation

```python
async def update_oncall_topic(client, channel_id, primary, secondary):
    topic = f":pager: On-call: <@{primary}> (primary) | <@{secondary}> (backup) | Escalation: #inc-response"
    await client.conversations_setTopic(channel=channel_id, topic=topic)

async def update_sprint_purpose(client, channel_id, sprint_num, end_date):
    purpose = f"Sprint {sprint_num} | Ends {end_date} | Board: https://jira.example.com/board/42"
    await client.conversations_setPurpose(channel=channel_id, purpose=purpose)
```

## 45. Keyboard Shortcuts

### Global Shortcuts

Triggered from anywhere in Slack (the lightning bolt menu or keyboard shortcut):

```python
@app.shortcut("create_incident")
def handle_shortcut(ack, shortcut, client):
    ack()
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "incident_form",
            "title": {"type": "plain_text", "text": "New Incident"},
            "blocks": [...]
        }
    )
```

### Message Shortcuts

Triggered from the context menu on a specific message:

```python
@app.shortcut("create_ticket_from_message")
def handle_message_shortcut(ack, shortcut, client):
    ack()
    message_text = shortcut["message"]["text"]
    client.views_open(
        trigger_id=shortcut["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "ticket_from_message",
            "title": {"type": "plain_text", "text": "Create Ticket"},
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"Creating ticket from:\n> {message_text}"}
                },
                {
                    "type": "input",
                    "block_id": "title_block",
                    "label": {"type": "plain_text", "text": "Ticket Title"},
                    "element": {"type": "plain_text_input", "action_id": "title", "initial_value": message_text[:100]}
                }
            ]
        }
    )
```

## 46. Data Loss Prevention (DLP) and Compliance

### Discovery API (Enterprise Grid)

```bash
# Search for messages containing sensitive data
curl -X POST https://slack.com/api/admin.conversations.search \
  -H "Authorization: Bearer xoxp-admin-token" \
  -H "Content-Type: application/json" \
  -d '{"query":"credit card","sort":"timestamp","sort_dir":"desc"}'
```

### Message Tombstoning

When a message is deleted by DLP, it leaves a tombstone:
```json
{
  "type": "message",
  "subtype": "tombstone",
  "text": "This message was deleted.",
  "hidden": true
}
```

### Audit Logs API (Enterprise Grid)

```bash
curl "https://api.slack.com/audit/v1/logs?action=user_login&oldest=1716000000&limit=100" \
  -H "Authorization: Bearer xoxp-admin-token"
```

Available audit actions: `user_login`, `user_logout`, `file_downloaded`, `file_uploaded`, `channel_created`, `app_installed`, `message_deleted`, `workspace_settings_changed`.

## 47. Tips for Effective Slack Communication

### Message Structure Guidelines

1. Lead with the most important information (inverted pyramid)
2. Use bold for key terms and action items
3. Use code formatting for technical references (commands, file paths, error codes)
4. Use threads for follow-up discussions
5. Use reactions instead of "thanks" or "+1" messages
6. Pin important messages for reference
7. Use scheduled messages for time-sensitive announcements across time zones
8. Include context blocks for metadata (who, when, links)

### Channel Hygiene

1. Archive inactive channels (no messages in 90+ days)
2. Use channel descriptions and topics actively
3. Set posting permissions on announcement channels
4. Use bookmarks for frequently referenced links
5. Create a channel naming convention and enforce it
6. Use default channels wisely (limit to essential ones)

### Notification Management

1. Configure channel-specific notification preferences
2. Use `<!here>` instead of `<!channel>` when possible
3. Schedule messages for recipients' working hours
4. Use threads to reduce notification noise
5. Set keywords for important topics across all channels

## 48. Advanced Integrations

### GitHub Integration Pattern

```python
from flask import Flask, request
import hmac
import hashlib

app = Flask(__name__)

@app.route("/github/webhook", methods=["POST"])
def github_webhook():
    # Verify GitHub signature
    signature = request.headers.get("X-Hub-Signature-256")
    payload = request.get_data()
    expected = "sha256=" + hmac.new(GITHUB_SECRET.encode(), payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return "Invalid signature", 401
    
    event = request.headers.get("X-GitHub-Event")
    data = request.json
    
    if event == "pull_request":
        action = data["action"]
        pr = data["pull_request"]
        
        if action == "opened":
            slack_client.chat_postMessage(
                channel="#code-reviews",
                blocks=[
                    {"type": "section", "text": {"type": "mrkdwn", "text": f":git-pull-request: *New PR Opened*\n<{pr['html_url']}|#{pr['number']} - {pr['title']}>\n\n_{pr['body'][:200]}..._"}},
                    {"type": "section", "fields": [
                        {"type": "mrkdwn", "text": f"*Author:*\n{pr['user']['login']}"},
                        {"type": "mrkdwn", "text": f"*Branch:*\n`{pr['head']['ref']}` → `{pr['base']['ref']}`"},
                        {"type": "mrkdwn", "text": f"*Changes:*\n+{pr['additions']} / -{pr['deletions']}"},
                        {"type": "mrkdwn", "text": f"*Files:*\n{pr['changed_files']} files"}
                    ]},
                    {"type": "actions", "elements": [
                        {"type": "button", "text": {"type": "plain_text", "text": "Review"}, "url": pr["html_url"], "action_id": "review_pr"},
                        {"type": "button", "text": {"type": "plain_text", "text": "Approve"}, "style": "primary", "action_id": "approve_pr", "value": str(pr["number"])}
                    ]}
                ]
            )
        elif action == "merged":
            slack_client.chat_postMessage(
                channel="#deployments",
                text=f":merged: PR #{pr['number']} merged: {pr['title']}"
            )
    
    elif event == "push":
        ref = data["ref"]
        if ref == "refs/heads/main":
            commits = data["commits"]
            commit_list = "\n".join([f"• `{c['id'][:7]}` {c['message'].split(chr(10))[0]}" for c in commits[:5]])
            slack_client.chat_postMessage(
                channel="#deployments",
                blocks=[
                    {"type": "section", "text": {"type": "mrkdwn", "text": f":arrow_up: *Push to main*\n{len(commits)} commit(s) by {data['pusher']['name']}\n\n{commit_list}"}}
                ]
            )
    
    return "OK", 200
```

### PagerDuty Integration Pattern

```python
def handle_pagerduty_webhook(payload):
    event = payload["event"]
    incident = event["data"]
    
    if event["event_type"] == "incident.triggered":
        slack_client.chat_postMessage(
            channel="#incidents",
            blocks=[
                {"type": "header", "text": {"type": "plain_text", "text": ":rotating_light: PagerDuty Incident Triggered"}},
                {"type": "section", "fields": [
                    {"type": "mrkdwn", "text": f"*Title:*\n{incident['title']}"},
                    {"type": "mrkdwn", "text": f"*Urgency:*\n{incident['urgency'].upper()}"},
                    {"type": "mrkdwn", "text": f"*Service:*\n{incident['service']['summary']}"},
                    {"type": "mrkdwn", "text": f"*Assigned:*\n{', '.join([a['summary'] for a in incident.get('assignments', [])])}"}
                ]},
                {"type": "actions", "elements": [
                    {"type": "button", "text": {"type": "plain_text", "text": "Acknowledge"}, "style": "primary", "action_id": "pd_ack", "value": incident["id"]},
                    {"type": "button", "text": {"type": "plain_text", "text": "Resolve"}, "style": "danger", "action_id": "pd_resolve", "value": incident["id"]},
                    {"type": "button", "text": {"type": "plain_text", "text": "View in PD"}, "url": incident["html_url"], "action_id": "pd_view"}
                ]}
            ]
        )
    
    elif event["event_type"] == "incident.resolved":
        slack_client.chat_postMessage(
            channel="#incidents",
            text=f":white_check_mark: Incident resolved: {incident['title']}"
        )
```

### Jira Integration Pattern

```python
def format_jira_issue(issue):
    status_emoji = {
        "To Do": ":white_circle:",
        "In Progress": ":large_blue_circle:",
        "In Review": ":mag:",
        "Done": ":white_check_mark:",
        "Blocked": ":no_entry:"
    }
    
    priority_emoji = {
        "Highest": ":fire:",
        "High": ":red_circle:",
        "Medium": ":large_orange_circle:",
        "Low": ":large_green_circle:",
        "Lowest": ":white_circle:"
    }
    
    emoji = status_emoji.get(issue["status"], ":grey_question:")
    p_emoji = priority_emoji.get(issue["priority"], "")
    
    return {
        "blocks": [
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"{emoji} *<{issue['url']}|{issue['key']}>* - {issue['summary']}\n{p_emoji} Priority: {issue['priority']} | Assignee: {issue.get('assignee', 'Unassigned')}"}
            },
            {
                "type": "context",
                "elements": [
                    {"type": "mrkdwn", "text": f"Type: {issue['type']} | Sprint: {issue.get('sprint', 'Backlog')} | Story Points: {issue.get('points', '-')}"}
                ]
            }
        ]
    }
```

## 49. Slack CLI (slack-cli)

The Slack CLI enables local development and deployment of next-gen Slack apps:

```bash
# Install
curl -fsSL https://downloads.slack-edge.com/slack-cli/install.sh | bash

# Login
slack login

# Create a new app
slack create my-app --template https://github.com/slack-samples/deno-starter-template

# Run locally (with hot reload)
slack run

# Deploy to Slack infrastructure
slack deploy

# List triggers
slack trigger list

# Create a trigger
slack trigger create --trigger-def triggers/shortcut.ts

# View activity logs
slack activity --tail

# List installed apps
slack app list

# Delete an app
slack app delete
```

### Trigger Types

| Type | Description | Example |
|------|-------------|---------|
| Link trigger | Clickable URL in channel | Share in channel bookmark |
| Shortcut trigger | Global or message shortcut | Lightning bolt menu |
| Event trigger | Fires on Slack event | reaction_added, message_posted |
| Scheduled trigger | Fires on schedule | Daily at 9 AM |
| Webhook trigger | External HTTP call | CI/CD pipeline callback |

## 50. Testing Slack Apps

### Block Kit Builder

Use https://app.slack.com/block-kit-builder to visually design and test Block Kit layouts before implementing them in code.

### Mocking the Slack API

```python
from unittest.mock import MagicMock, patch

def test_deploy_notification():
    mock_client = MagicMock()
    mock_client.chat_postMessage.return_value = {"ok": True, "ts": "1234567890.123456"}
    
    result = send_deploy_notification(
        client=mock_client,
        channel="C012AB3CD",
        service="api-gateway",
        version="v2.5.0",
        environment="production"
    )
    
    mock_client.chat_postMessage.assert_called_once()
    call_args = mock_client.chat_postMessage.call_args
    assert call_args.kwargs["channel"] == "C012AB3CD"
    assert "api-gateway" in call_args.kwargs["text"]
    assert any("v2.5.0" in str(block) for block in call_args.kwargs.get("blocks", []))
```

### Integration Testing with Slack Sandbox

```python
import os
import pytest
from slack_sdk import WebClient

@pytest.fixture
def slack_client():
    return WebClient(token=os.environ["SLACK_TEST_BOT_TOKEN"])

@pytest.fixture
def test_channel():
    return os.environ["SLACK_TEST_CHANNEL"]

def test_post_and_update_message(slack_client, test_channel):
    # Post
    result = slack_client.chat_postMessage(channel=test_channel, text="Test message")
    assert result["ok"]
    ts = result["ts"]
    
    # Update
    result = slack_client.chat_update(channel=test_channel, ts=ts, text="Updated message")
    assert result["ok"]
    
    # Delete (cleanup)
    slack_client.chat_delete(channel=test_channel, ts=ts)
```

## 51. Performance Optimization

### Batch Operations

When you need to perform many operations, batch them efficiently:

```python
import asyncio
from slack_sdk.web.async_client import AsyncWebClient

async def post_to_multiple_channels(channels, message, blocks):
    client = AsyncWebClient(token=BOT_TOKEN)
    
    # Respect rate limits: 1 message per channel per second
    tasks = []
    for i, channel in enumerate(channels):
        # Stagger requests to avoid rate limits
        await asyncio.sleep(1.1)
        task = client.chat_postMessage(channel=channel, text=message, blocks=blocks)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successes = [r for r in results if not isinstance(r, Exception) and r.get("ok")]
    failures = [r for r in results if isinstance(r, Exception) or not r.get("ok")]
    
    return {"sent": len(successes), "failed": len(failures)}
```

### Caching User and Channel Data

```python
from functools import lru_cache
import time

class SlackCache:
    def __init__(self, client, ttl=300):
        self.client = client
        self.ttl = ttl
        self._user_cache = {}
        self._channel_cache = {}
    
    def get_user(self, user_id):
        cached = self._user_cache.get(user_id)
        if cached and time.time() - cached["fetched_at"] < self.ttl:
            return cached["data"]
        
        result = self.client.users_info(user=user_id)
        if result["ok"]:
            self._user_cache[user_id] = {"data": result["user"], "fetched_at": time.time()}
            return result["user"]
        return None
    
    def get_channel(self, channel_id):
        cached = self._channel_cache.get(channel_id)
        if cached and time.time() - cached["fetched_at"] < self.ttl:
            return cached["data"]
        
        result = self.client.conversations_info(channel=channel_id)
        if result["ok"]:
            self._channel_cache[channel_id] = {"data": result["channel"], "fetched_at": time.time()}
            return result["channel"]
        return None
```

## 52. Slack Connect Best Practices

When working with external organizations via Slack Connect:

1. Use separate channels for each external partner (prefix with `#ext-`)
2. Be aware that external users can see channel history from when they joined
3. File sharing policies may differ between organizations
4. Apps installed in your workspace can see messages from external users
5. Custom emoji from other workspaces may not render
6. User groups cannot span across organizations
7. Workflows triggered in shared channels execute in the workspace that owns the workflow
8. Message retention policies are enforced by each organization independently

## 53. Accessibility and Internationalization

### Screen Reader Compatibility

- Always provide `alt_text` for images (descriptive, not decorative)
- Use the `text` fallback field in messages with blocks
- Avoid using only emoji to convey meaning
- Structure content with clear hierarchy (header → section → context)
- Use plain_text for critical actionable content

### Multi-Language Support

```python
def get_localized_message(user_locale, key):
    messages = {
        "en-US": {"greeting": "Hello!", "deploy_success": "Deployment successful"},
        "pt-BR": {"greeting": "Olá!", "deploy_success": "Deploy realizado com sucesso"},
        "es-ES": {"greeting": "¡Hola!", "deploy_success": "Despliegue exitoso"},
        "fr-FR": {"greeting": "Bonjour!", "deploy_success": "Déploiement réussi"}
    }
    locale_messages = messages.get(user_locale, messages["en-US"])
    return locale_messages.get(key, messages["en-US"][key])

# Get user locale
user_info = client.users_info(user=user_id)
locale = user_info["user"].get("locale", "en-US")
message = get_localized_message(locale, "deploy_success")
```

## 54. Migration from Legacy Attachments to Block Kit

Legacy attachments (the `attachments` field) are deprecated in favor of Block Kit. Here's how to migrate:

### Before (Legacy Attachment)

```json
{
  "attachments": [
    {
      "color": "#36a64f",
      "title": "Deployment Complete",
      "title_link": "https://deploy.example.com",
      "fields": [
        {"title": "Service", "value": "api-gateway", "short": true},
        {"title": "Version", "value": "v2.5.0", "short": true}
      ],
      "footer": "DeployBot",
      "ts": 1716000000
    }
  ]
}
```

### After (Block Kit)

```json
{
  "blocks": [
    {
      "type": "header",
      "text": {"type": "plain_text", "text": "Deployment Complete"}
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*Service:*\n`api-gateway`"},
        {"type": "mrkdwn", "text": "*Version:*\nv2.5.0"}
      ]
    },
    {
      "type": "context",
      "elements": [
        {"type": "mrkdwn", "text": "DeployBot | <!date^1716000000^{date_short} {time}|May 18, 2025>"}
      ]
    }
  ]
}
```

### Key Differences

| Feature | Legacy Attachments | Block Kit |
|---------|-------------------|-----------|
| Color bar | `color` field | Not available (use emoji/text) |
| Author | `author_name`, `author_icon` | Context block with image |
| Title link | `title_link` | Section with mrkdwn link |
| Fields | `fields` array | Section `fields` array |
| Footer | `footer`, `footer_icon` | Context block |
| Timestamp | `ts` field | Date formatting syntax |
| Actions | `actions` in attachment | Actions block |
| Interactivity | Limited | Full (buttons, selects, modals) |

## 55. Webhook Security

### Verifying Incoming Requests

```python
import hashlib
import hmac
import time

def verify_slack_signature(signing_secret, request_body, timestamp, signature):
    # Reject requests older than 5 minutes
    if abs(time.time() - int(timestamp)) > 300:
        return False
    
    # Compute expected signature
    sig_basestring = f"v0:{timestamp}:{request_body}"
    computed = "v0=" + hmac.new(
        signing_secret.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(computed, signature)

# In your request handler
@app.before_request
def verify_request():
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")
    body = request.get_data(as_text=True)
    
    if not verify_slack_signature(SIGNING_SECRET, body, timestamp, signature):
        abort(401)
```

### Webhook URL Rotation

If a webhook URL is compromised:
1. Regenerate the webhook URL in app settings
2. Update all systems using the old URL
3. Monitor the old URL for unauthorized usage
4. Consider using signed webhooks with verification

## 56. Complete Emoji Skin Tone Reference

Slack supports skin tone modifiers for people emoji:

```
:thumbsup::skin-tone-2:  → 👍🏻 (light)
:thumbsup::skin-tone-3:  → 👍🏼 (medium-light)
:thumbsup::skin-tone-4:  → 👍🏽 (medium)
:thumbsup::skin-tone-5:  → 👍🏾 (medium-dark)
:thumbsup::skin-tone-6:  → 👍🏿 (dark)
```

### Reacji (Reaction-Based Automation)

Use reactions as triggers for automated workflows:

```python
@app.event("reaction_added")
def handle_reaction(event, client):
    reaction = event["reaction"]
    channel = event["item"]["channel"]
    ts = event["item"]["ts"]
    
    if reaction == "ticket":
        # Fetch the message
        result = client.conversations_history(channel=channel, latest=ts, limit=1, inclusive=True)
        message = result["messages"][0]
        
        # Create a Jira ticket from the message
        ticket = create_jira_ticket(
            title=message["text"][:100],
            description=message["text"],
            reporter=event["user"]
        )
        
        # Reply in thread
        client.chat_postMessage(
            channel=channel,
            thread_ts=ts,
            text=f":ticket: Ticket created: <{ticket['url']}|{ticket['key']}>"
        )
    
    elif reaction == "eyes":
        # Acknowledge that someone is looking into it
        client.chat_postMessage(
            channel=channel,
            thread_ts=ts,
            text=f"<@{event['user']}> is looking into this :eyes:"
        )
    
    elif reaction == "pushpin":
        # Auto-pin the message
        try:
            client.pins_add(channel=channel, timestamp=ts)
        except Exception:
            pass  # Already pinned or no permission
```

## 57. Appendix: Quick Reference Card

### mrkdwn Cheat Sheet

```
*bold*  _italic_  ~strike~  `code`  ```block```
> quote  >>> quote all
<url|text>  <@user>  <#channel>  <!here>  <!channel>
<!date^ts^{token}|fallback>
:emoji:  :emoji::skin-tone-2:
```

### Block Types Quick Reference

```
header     → Large bold text (plain_text, 150 chars)
section    → Text + optional accessory + fields
divider    → Horizontal line
image      → Standalone image
actions    → Interactive elements (max 25)
context    → Small metadata (max 10 elements)
input      → Form input (modals/home)
rich_text  → Structured formatted text
video      → Embedded video
file       → File reference
```

### Token Prefixes

```
xoxb-  → Bot token
xoxp-  → User token
xapp-  → App-level token
xoxe-  → Enterprise token
```

### HTTP Response Codes

```
200 → Success (check "ok" field)
429 → Rate limited (check Retry-After header)
500 → Server error (retry with backoff)
```

## 58. Slack Notifications Best Practices for Bots

### Notification Priority Matrix

| Priority | Channel | Format | Mention | Example |
|----------|---------|--------|---------|---------|
| P1 Critical | #incidents + DM | Full blocks + emoji | `<!channel>` | Production down |
| P2 High | #alerts | Blocks with actions | `<!here>` | Error rate spike |
| P3 Medium | #monitoring | Simple block | None | Deployment complete |
| P4 Low | #bot-logs | Plain text | None | Scheduled job ran |
| Info | Thread reply | Context block | None | Status update |

### Notification Throttling

```python
import time
from collections import defaultdict

class NotificationThrottler:
    def __init__(self, min_interval_seconds=60):
        self.min_interval = min_interval_seconds
        self.last_sent = defaultdict(float)
    
    def should_send(self, key):
        now = time.time()
        if now - self.last_sent[key] >= self.min_interval:
            self.last_sent[key] = now
            return True
        return False
    
    def send_or_batch(self, key, message):
        if self.should_send(key):
            return self._send_immediately(key, message)
        else:
            return self._add_to_batch(key, message)

throttler = NotificationThrottler(min_interval_seconds=300)

def alert_handler(alert):
    key = f"{alert['service']}:{alert['type']}"
    if throttler.should_send(key):
        post_alert_to_slack(alert)
    else:
        # Batch similar alerts and send summary later
        batch_alert(key, alert)
```

### Smart Notification Routing

```python
def route_notification(event_type, severity, service):
    routing = {
        "deployment": {
            "channel": "#deployments",
            "mention": None,
            "thread": False
        },
        "incident": {
            "channel": "#incidents",
            "mention": "<!channel>" if severity <= 2 else "<!here>",
            "thread": False
        },
        "alert": {
            "channel": f"#alerts-{service}",
            "mention": "<!here>" if severity == 1 else None,
            "thread": True
        },
        "ci_failure": {
            "channel": "#ci-cd",
            "mention": None,
            "thread": True
        }
    }
    return routing.get(event_type, {"channel": "#bot-logs", "mention": None, "thread": False})
```

## 59. Enterprise Grid Administration

### Organization-Level Operations

```bash
# List all workspaces in the org
curl "https://slack.com/api/admin.teams.list?limit=100" \
  -H "Authorization: Bearer xoxp-org-admin-token"

# Create a new workspace
curl -X POST https://slack.com/api/admin.teams.create \
  -H "Authorization: Bearer xoxp-org-admin-token" \
  -H "Content-Type: application/json" \
  -d '{"team_domain":"new-team","team_name":"New Team","team_description":"A new workspace"}'

# Set organization-wide app policies
curl -X POST https://slack.com/api/admin.apps.restrict \
  -H "Authorization: Bearer xoxp-org-admin-token" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"A012AB3CD","team_id":"T012AB3CD"}'
```

### Information Barriers

Enterprise Grid supports information barriers to prevent communication between specific groups:

```bash
# Create an information barrier
curl -X POST https://slack.com/api/admin.barriers.create \
  -H "Authorization: Bearer xoxp-org-admin-token" \
  -H "Content-Type: application/json" \
  -d '{
    "barriered_from_usergroup_ids": ["S001", "S002"],
    "primary_usergroup_id": "S003",
    "restricted_subjects": ["im", "mpim", "call"]
  }'
```

## 60. Monitoring Your Slack App

### Health Check Endpoint

```python
from flask import Flask, jsonify
import time

app = Flask(__name__)
last_event_time = time.time()

@app.route("/health")
def health():
    # Check if we've received events recently
    seconds_since_last_event = time.time() - last_event_time
    
    status = {
        "status": "healthy" if seconds_since_last_event < 300 else "degraded",
        "last_event_seconds_ago": int(seconds_since_last_event),
        "uptime_seconds": int(time.time() - app_start_time),
        "version": APP_VERSION,
        "slack_api_reachable": check_slack_api()
    }
    
    code = 200 if status["status"] == "healthy" else 503
    return jsonify(status), code

def check_slack_api():
    try:
        result = slack_client.auth_test()
        return result["ok"]
    except Exception:
        return False
```

### Metrics to Track

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `slack_api_calls_total` | Total API calls made | Rate > 80% of limit |
| `slack_api_errors_total` | Failed API calls | Error rate > 5% |
| `slack_api_latency_ms` | API response time | p99 > 5000ms |
| `slack_events_received_total` | Events received | Drop to 0 for 5 min |
| `slack_events_processed_total` | Events processed | Lag > 100 events |
| `slack_rate_limits_hit` | 429 responses received | Any occurrence |
| `slack_message_send_duration_ms` | Time to send message | p95 > 3000ms |

### Logging Best Practices

```python
import logging
import json

logger = logging.getLogger("slack_app")

def log_api_call(method, channel=None, user=None, success=True, error=None, duration_ms=None):
    log_data = {
        "type": "slack_api_call",
        "method": method,
        "channel": channel,
        "user": user,
        "success": success,
        "error": error,
        "duration_ms": duration_ms,
        "timestamp": time.time()
    }
    
    if success:
        logger.info(json.dumps(log_data))
    else:
        logger.error(json.dumps(log_data))
```

This concludes the comprehensive Slack Master Specialist reference covering all aspects of the Slack platform from basic message formatting through enterprise administration, app development, and production operations.

## === FILE: 50-slack-troubleshooting.md ===
# Slack Master Specialist — Troubleshooting Guide

## 1. Message Delivery Issues

### Messages Not Appearing

| Symptom | Cause | Fix |
|---------|-------|-----|
| Message not posted | Bot not in channel | `conversations.join` or invite bot |
| Message not visible | Posted as ephemeral | Use `chat.postMessage` instead of `chat.postEphemeral` |
| Message delayed | Rate limited | Check for 429 response, implement backoff |
| Message in wrong channel | Channel ID mismatch | Verify channel ID with `conversations.info` |
| Blocks not rendering | Invalid block JSON | Validate in Block Kit Builder |
| Formatting broken | Wrong text type | Use `mrkdwn` type for formatting, `plain_text` for no parsing |

### Debugging Message Failures

```python
try:
    result = client.chat_postMessage(channel=channel, text=text, blocks=blocks)
    if not result["ok"]:
        print(f"API returned ok=false: {result.get('error')}")
except SlackApiError as e:
    print(f"Error: {e.response['error']}")
    print(f"Response: {e.response.data}")
    
    # Common fixes
    if e.response["error"] == "not_in_channel":
        client.conversations_join(channel=channel)
        # Retry
    elif e.response["error"] == "channel_not_found":
        # Channel may be private or deleted
        pass
    elif e.response["error"] == "invalid_blocks":
        # Validate blocks at https://app.slack.com/block-kit-builder
        print(f"Invalid blocks: {json.dumps(blocks, indent=2)}")
```

## 2. Rate Limiting Issues

### Identifying Rate Limits

```python
import time

def handle_rate_limit(response):
    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 30))
        print(f"Rate limited. Retry after {retry_after} seconds")
        time.sleep(retry_after)
        return True
    return False
```

### Rate Limit Tiers

| Tier | Limit | Methods | Strategy |
|------|-------|---------|----------|
| Tier 1 | 1/min | `admin.*` | Queue with 60s delay |
| Tier 2 | 20/min | `conversations.list`, `users.list` | Cache results, paginate efficiently |
| Tier 3 | 50/min | `chat.postMessage`, `reactions.add` | Batch operations, use queues |
| Tier 4 | 100/min | `auth.test`, `conversations.info` | Generally safe |
| Special | 1/sec/channel | `chat.postMessage` per channel | Distribute across channels |

### Burst Protection Pattern

```python
from collections import deque
import time

class BurstProtector:
    def __init__(self, max_per_minute=50):
        self.max_per_minute = max_per_minute
        self.timestamps = deque()
    
    def wait_if_needed(self):
        now = time.time()
        # Remove timestamps older than 60 seconds
        while self.timestamps and self.timestamps[0] < now - 60:
            self.timestamps.popleft()
        
        if len(self.timestamps) >= self.max_per_minute:
            wait_time = 60 - (now - self.timestamps[0])
            if wait_time > 0:
                time.sleep(wait_time)
        
        self.timestamps.append(time.time())
```

## 3. Authentication Issues

### Token Problems

| Error | Cause | Fix |
|-------|-------|-----|
| `not_authed` | Missing token | Add `Authorization: Bearer xoxb-...` header |
| `invalid_auth` | Malformed token | Check token format (xoxb- prefix) |
| `token_revoked` | App uninstalled or token rotated | Re-authorize the app |
| `missing_scope` | Token lacks permission | Add scope in app settings, re-install |
| `account_inactive` | User deactivated | Use a different user's token |
| `org_login_required` | SSO required | User must re-authenticate via SSO |
| `ekm_access_denied` | Enterprise key management | Contact workspace admin |

### Verifying Your Token

```bash
# Quick token check
curl "https://slack.com/api/auth.test" -H "Authorization: Bearer xoxb-YOUR-TOKEN"

# Expected response
# {"ok":true,"url":"https://team.slack.com/","team":"Team Name","user":"bot_name","team_id":"T012AB3CD","user_id":"U012AB3CD","bot_id":"B012AB3CD"}
```

### Scope Debugging

```bash
# Check what scopes your token has
curl "https://slack.com/api/auth.test" -H "Authorization: Bearer xoxb-TOKEN" -v 2>&1 | grep "x-oauth-scopes"
```

## 4. Block Kit Issues

### Common Block Kit Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `invalid_blocks` | Malformed JSON | Validate at Block Kit Builder |
| `too_many_blocks` | More than 50 blocks | Split into multiple messages |
| `invalid_blocks_format` | Wrong block structure | Check required fields |
| Text too long | Section text > 3000 chars | Truncate or split |
| Action ID collision | Duplicate action_id | Use unique action_ids |

### Block Validation Checklist

```python
def validate_blocks(blocks):
    errors = []
    
    if len(blocks) > 50:
        errors.append(f"Too many blocks: {len(blocks)} (max 50)")
    
    for i, block in enumerate(blocks):
        if "type" not in block:
            errors.append(f"Block {i}: missing 'type' field")
        
        if block.get("type") == "section":
            text = block.get("text", {})
            if text.get("type") == "mrkdwn" and len(text.get("text", "")) > 3000:
                errors.append(f"Block {i}: mrkdwn text exceeds 3000 chars")
            if text.get("type") == "plain_text" and len(text.get("text", "")) > 3000:
                errors.append(f"Block {i}: plain_text exceeds 3000 chars")
            
            fields = block.get("fields", [])
            if len(fields) > 10:
                errors.append(f"Block {i}: too many fields ({len(fields)}, max 10)")
        
        if block.get("type") == "actions":
            elements = block.get("elements", [])
            if len(elements) > 25:
                errors.append(f"Block {i}: too many action elements ({len(elements)}, max 25)")
        
        if block.get("type") == "context":
            elements = block.get("elements", [])
            if len(elements) > 10:
                errors.append(f"Block {i}: too many context elements ({len(elements)}, max 10)")
        
        if block.get("type") == "header":
            text = block.get("text", {}).get("text", "")
            if len(text) > 150:
                errors.append(f"Block {i}: header text exceeds 150 chars")
    
    return errors
```

## 5. Events API Issues

### Events Not Being Received

| Symptom | Cause | Fix |
|---------|-------|-----|
| No events at all | URL not verified | Complete URL verification challenge |
| Events stop arriving | Server returning non-200 | Fix server to respond 200 within 3s |
| Duplicate events | Not deduplicating | Track `event_id` to skip duplicates |
| Missing specific events | Not subscribed | Add event type in app settings |
| Events from wrong workspace | Multi-workspace app | Check `team_id` in payload |

### Event Debugging

```python
import logging

logging.basicConfig(level=logging.DEBUG)

@app.event("message")
def handle_all_messages(event, logger):
    logger.debug(f"Received event: {json.dumps(event, indent=2)}")
    
    # Check for subtypes that should be ignored
    if event.get("subtype") in ["bot_message", "message_changed", "message_deleted"]:
        logger.debug(f"Ignoring subtype: {event['subtype']}")
        return
    
    # Check for bot messages to avoid loops
    if event.get("bot_id"):
        logger.debug("Ignoring bot message")
        return
```

### Retry Headers

When Slack retries an event delivery, it includes:

```
X-Slack-Retry-Num: 1        # Retry attempt number (1, 2, or 3)
X-Slack-Retry-Reason: http_timeout  # Why it's retrying
```

Handle retries:
```python
@app.before_request
def handle_retries():
    retry_num = request.headers.get("X-Slack-Retry-Num")
    if retry_num:
        # Already processed this event, just acknowledge
        return make_response("", 200)
```

## 6. Socket Mode Issues

### Connection Problems

| Symptom | Cause | Fix |
|---------|-------|-----|
| Connection refused | Wrong app token | Use `xapp-` token, not `xoxb-` |
| Immediate disconnect | Socket Mode not enabled | Enable in app settings |
| Intermittent drops | Network instability | Implement reconnection logic |
| Events not received | Wrong event subscriptions | Check app event subscriptions |

### Socket Mode Reconnection

```python
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.listeners import SocketModeRequestListener
import time

def create_resilient_client():
    client = SocketModeClient(
        app_token="xapp-TOKEN",
        web_client=WebClient(token="xoxb-TOKEN"),
        auto_reconnect_enabled=True,
        trace_enabled=True
    )
    
    # Monitor connection health
    def on_disconnect():
        print("Disconnected! Auto-reconnect will handle this.")
    
    def on_connect():
        print("Connected to Slack!")
    
    return client
```

## 7. Modal and Interactivity Issues

### Modal Not Opening

| Symptom | Cause | Fix |
|---------|-------|-----|
| `expired_trigger_id` | trigger_id expired (3s) | Open modal immediately in ack handler |
| `invalid_trigger_id` | Wrong trigger_id format | Use trigger_id from the interaction payload |
| Modal opens blank | Empty blocks array | Add at least one block |
| Submit not working | Missing callback_id | Add `callback_id` to view |

### View Submission Errors

```python
@app.view("my_form")
def handle_submission(ack, body, view):
    values = view["state"]["values"]
    errors = {}
    
    # Validate inputs
    email = values["email_block"]["email_input"]["value"]
    if not email or "@" not in email:
        errors["email_block"] = "Please enter a valid email"
    
    name = values["name_block"]["name_input"]["value"]
    if not name or len(name) < 2:
        errors["name_block"] = "Name must be at least 2 characters"
    
    if errors:
        # Return validation errors (modal stays open)
        ack(response_action="errors", errors=errors)
    else:
        # Success - close modal
        ack()
        # Process the submission...
```

## 8. File Upload Issues

### Common Upload Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `file_not_found` | Invalid file path | Verify file exists locally |
| `too_large` | File exceeds limit | Compress or split file (max varies by plan) |
| `invalid_channel` | Bot not in channel | Join channel first |
| `not_allowed_token_type` | Using wrong token type | Use bot token with `files:write` scope |

### File Size Limits

| Plan | Max File Size |
|------|--------------|
| Free | 5 GB total workspace storage |
| Pro | 10 GB per member |
| Business+ | 20 GB per member |
| Enterprise Grid | 1 TB per member |

Individual file upload limit: 1 GB regardless of plan.

## 9. Webhook Issues

### Incoming Webhook Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| 404 response | Webhook URL invalid | Regenerate webhook in app settings |
| 410 response | Webhook revoked | App was uninstalled, re-install |
| 500 response | Slack server error | Retry with exponential backoff |
| No message appears | Invalid JSON payload | Validate JSON structure |
| Formatting not working | Wrong content type | Set `Content-Type: application/json` |

### Webhook Debugging

```bash
# Test webhook with verbose output
curl -v -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"text":"test"}'

# Check if webhook URL is reachable
curl -s -o /dev/null -w "%{http_code}" -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{"text":"ping"}'
```

## 10. Slash Command Issues

### Command Not Responding

| Symptom | Cause | Fix |
|---------|-------|-----|
| "This command didn't work" | No response within 3s | Acknowledge immediately with `ack()` |
| "dispatch_failed" | Request URL unreachable | Check server is running and URL is correct |
| Command not found | Not installed in workspace | Re-install app or check command config |
| Wrong response format | Invalid response_type | Use "ephemeral" or "in_channel" |

### Proper Command Handling

```python
# WRONG - processing before ack causes timeout
@app.command("/deploy")
def bad_handler(ack, command):
    result = run_long_deployment()  # Takes 30 seconds
    ack(text=f"Done: {result}")  # TOO LATE - already timed out

# CORRECT - ack immediately, process async
@app.command("/deploy")
def good_handler(ack, command, respond):
    ack()  # Acknowledge within 3 seconds
    
    # Process asynchronously
    result = run_long_deployment()
    
    # Use respond() to send follow-up (uses response_url)
    respond(text=f"Done: {result}", response_type="in_channel")
```

## 11. Formatting Issues

### mrkdwn Not Rendering

| Issue | Cause | Fix |
|-------|-------|-----|
| `*bold*` shows literally | Using `plain_text` type | Change to `"type": "mrkdwn"` |
| Links not clickable | Wrong link format | Use `<url|text>` format |
| Newlines ignored | Using `\n` in plain_text | Use actual newlines or switch to mrkdwn |
| Code block broken | Unescaped backticks | Escape with backslash or use rich_text |
| Mentions not working | Wrong format | Use `<@U012AB3CD>` not `@username` |
| Channel links broken | Using # prefix | Use `<#C012AB3CD>` format |

### Special Characters That Need Escaping

In mrkdwn text, these characters have special meaning:
- `&` → `&amp;`
- `<` → `&lt;`
- `>` → `&gt;`

```python
def escape_mrkdwn(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# Use when including user-generated content in mrkdwn
user_input = "Check if x < 5 && y > 3"
safe_text = f"User said: {escape_mrkdwn(user_input)}"
```

## 12. Performance Issues

### Slow API Responses

```python
import time

def measure_api_call(method, **kwargs):
    start = time.time()
    try:
        result = getattr(client, method)(**kwargs)
        duration = (time.time() - start) * 1000
        print(f"{method} took {duration:.0f}ms")
        return result
    except SlackApiError as e:
        duration = (time.time() - start) * 1000
        print(f"{method} FAILED after {duration:.0f}ms: {e.response['error']}")
        raise
```

### Memory Issues with Large Workspaces

```python
# BAD: Loading all users into memory
all_users = client.users_list()["members"]  # Could be 10,000+ users

# GOOD: Stream with pagination
def process_users_streaming(client, callback):
    cursor = None
    while True:
        result = client.users_list(limit=200, cursor=cursor)
        for user in result["members"]:
            callback(user)  # Process one at a time
        cursor = result.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
```

## 13. Common Integration Pitfalls

### Bot Message Loops

```python
# DANGER: This creates an infinite loop
@app.event("message")
def echo_message(event, say):
    say(event["text"])  # Bot responds to its own messages!

# SAFE: Filter out bot messages
@app.event("message")
def echo_message(event, say):
    if event.get("bot_id") or event.get("subtype"):
        return  # Ignore bot messages and subtypes
    say(f"You said: {event['text']}")
```

### Thread vs Channel Confusion

```python
# Post to thread (reply)
client.chat_postMessage(
    channel="C012AB3CD",
    thread_ts="1234567890.123456",  # Parent message timestamp
    text="This is a thread reply"
)

# Post to thread AND broadcast to channel
client.chat_postMessage(
    channel="C012AB3CD",
    thread_ts="1234567890.123456",
    reply_broadcast=True,  # Also shows in channel
    text="Important thread reply"
)
```

## 14. Diagnostic Commands

```bash
# Check API status
curl -s "https://status.slack.com/api/v2.0.0/current" | jq .

# Verify bot permissions
curl -s "https://slack.com/api/auth.test" -H "Authorization: Bearer $SLACK_BOT_TOKEN" | jq .

# Check if bot is in a channel
curl -s "https://slack.com/api/conversations.info?channel=C012AB3CD" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" | jq '.channel.is_member'

# List bot's channels
curl -s "https://slack.com/api/users.conversations?types=public_channel,private_channel" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" | jq '.channels[].name'

# Check rate limit headers in response
curl -v "https://slack.com/api/auth.test" -H "Authorization: Bearer $SLACK_BOT_TOKEN" 2>&1 | grep -i "retry\|x-ratelimit"
```

This troubleshooting guide covers all common issues encountered when developing and operating Slack applications in production environments.

