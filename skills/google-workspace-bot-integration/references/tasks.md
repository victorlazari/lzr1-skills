# Google Tasks Integration Reference

The Google Tasks API lets the bot manage user tasks and task lists. This integration turns the bot into a personal productivity assistant, managing to-dos directly from conversational interfaces.

## Core Capabilities

The bot creates new tasks, assigning titles, detailed notes, and specific due dates. It manages the lifecycle of these tasks by updating details, marking them as completed, or deleting them entirely. The bot also organizes the broader structure by creating new task lists, renaming them, or removing them. It retrieves and lists tasks within specific lists, optionally filtering the results by completion status or upcoming due dates. Finally, the bot can move tasks between different lists or reorder their position within a single list.

## Action Categories and Examples

| Action Category | Description | Example Bot Command |
| :--- | :--- | :--- |
| **Task Creation & Tracking** | Add new tasks and list pending items. | *"Add a task to my 'Work' list to 'Review the API documentation' due tomorrow."* <br><br> *"List all my pending tasks due this week."* |
| **Task Lifecycle** | Mark tasks as complete or update their details. | *"Mark the task 'Send weekly report' as completed."* |
| **List Management** | Create task lists and move tasks between them. | *"Create a new task list called 'Project Launch Checklist'."* <br><br> *"Move the task 'Call vendor' from the 'Backlog' list to the 'Today' list."* |

## Official Documentation

* [Google Tasks API Reference](https://developers.google.com/workspace/tasks/reference/rest)
