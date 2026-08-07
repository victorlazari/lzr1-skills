# Slack Web API Reference

Verified against upstream: 2026-08-07

This reference covers essential Slack Web API methods for building applications.

## chat.* Methods

- `chat.postMessage`: Sends a message to a channel.
- `chat.update`: Updates a message.
- `chat.delete`: Deletes a message.
- `chat.scheduleMessage`: Schedules a message to be sent to a channel.
- `chat.postEphemeral`: Sends an ephemeral message to a user in a channel.

## conversations.* Methods

- `conversations.list`: Lists all channels in a Slack team.
- `conversations.info`: Retrieves information about a conversation.
- `conversations.create`: Initiates a public or private channel-based conversation.
- `conversations.join`: Joins an existing conversation.
- `conversations.invite`: Invites users to a channel.
- `conversations.history`: Fetches a conversation's history of messages and events.

## users.* Methods

- `users.info`: Gets information about a user.
- `users.list`: Lists all users in a Slack team.
- `users.lookupByEmail`: Find a user with an email address.

## views.* Methods

- `views.open`: Open a view for a user.
- `views.update`: Update an existing view.
- `views.publish`: Publish a static view for a User.

## files.* Methods

- `files.getUploadURLExternal`: Get a URL for an external file upload.
- `files.completeUploadExternal`: Complete an external file upload.
- `files.list`: List for a team, in a channel, or from a user with applied filters.
