# Google Calendar Integration Reference

The Google Calendar API enables the bot to create, modify, and manage events and settings. This allows for seamless scheduling and time management through natural language commands.

## Core Capabilities

Through this integration, the bot can create new single or recurring events and modify existing ones by updating times, locations, or descriptions. It manages guests by adding or removing attendees and sending RSVP requests. The bot can also query schedules by checking free/busy information across multiple users to find optimal meeting times. Additionally, it handles broader calendar management tasks, such as creating secondary calendars, updating calendar metadata, clearing events, and setting up or modifying event reminders.

## Action Categories and Examples

| Action Category | Description | Example Bot Command |
| :--- | :--- | :--- |
| **Event Management** | Create, update, reschedule, or delete calendar events. | *"Add to the calendar a meeting for tomorrow at 10am with @user1, @user2 and @user3."* <br><br> *"Reschedule my 2 PM meeting with the marketing team to Thursday at 11 AM."* |
| **Schedule Coordination** | Query free/busy times and manage event attendees. | *"Find a 30-minute slot where both @sarah and I are free this afternoon and schedule a sync."* |
| **Calendar Operations** | Manage overall calendar views and daily schedules. | *"Cancel all my afternoon meetings for today."* <br><br> *"What is my schedule looking like for next Tuesday?"* |

## Official Documentation

* [Google Calendar API Reference](https://developers.google.com/workspace/calendar/api/v3/reference)
