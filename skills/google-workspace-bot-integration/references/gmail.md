# Gmail Integration Reference

The Gmail API allows the bot to view and manage Gmail mailbox data, including threads, messages, drafts, and labels. This integration empowers the bot to handle communication workflows directly from chat interfaces or automated triggers.

## Core Capabilities

The bot can compose and send emails directly or as replies to existing threads. It manages drafts by creating, reading, updating, or deleting unsent messages. For message retrieval, the bot can search for, read, or list messages and threads based on specific criteria. Label management allows the bot to apply or remove labels such as INBOX, UNREAD, STARRED, or custom user-defined labels. Furthermore, the bot can move messages to the trash, permanently delete them, handle attachments for both incoming and outgoing emails, and update settings like auto-forwarding rules or out-of-office vacation responders.

## Action Categories and Examples

| Action Category | Description | Example Bot Command |
| :--- | :--- | :--- |
| **Sending & Drafting** | Compose new emails, reply to threads, and manage drafts. | *"Send an email with all the users in the slack thread copied with the summary and bullet points."* <br><br> *"Draft a response to the latest email from John Smith saying I will review the proposal by Friday."* |
| **Retrieval & Organization** | Search messages, read threads, and apply or remove labels. | *"Find all unread emails from 'billing@example.com' and apply the label 'Invoices'."* <br><br> *"Summarize the last 5 emails in the 'Project Alpha' thread."* |
| **Settings Management** | Configure auto-forwarding and vacation responders. | *"Turn on my out-of-office responder starting tomorrow until next Monday."* |

## Official Documentation

* [Gmail API Reference](https://developers.google.com/workspace/gmail/api/reference/rest)
