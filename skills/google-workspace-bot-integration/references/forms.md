# Google Forms Integration Reference

The Google Forms API provides programmatic access for managing forms and acting on responses. This integration is perfect for automating surveys, feedback collection, and internal request processes.

## Core Capabilities

The bot can create new forms and configure their overarching titles and descriptions. It manages the form's structure by adding, updating, or deleting specific questions, supporting various types like multiple choice, short text, and checkboxes. The bot updates form settings, such as converting a form into a quiz or restricting responses to a specific organization domain. Furthermore, it retrieves submitted responses for data analysis and can utilize watches or webhooks to trigger immediate bot actions whenever a new response is submitted.

## Action Categories and Examples

| Action Category | Description | Example Bot Command |
| :--- | :--- | :--- |
| **Form Creation & Editing** | Build forms and add or modify questions. | *"Create a new Google Form for 'Team Lunch Preferences' with a multiple-choice question for dietary restrictions."* <br><br> *"Add a new short-answer question to the 'Event Registration' form asking for 'Company Name'."* |
| **Response Analysis** | Retrieve and summarize form submissions. | *"Get the latest 10 responses from the 'Customer Feedback' form and summarize the main complaints."* |
| **Automated Triggers** | React to new submissions via webhooks. | *"When a new response is submitted to the 'IT Support Request' form, post a summary in the #it-helpdesk channel."* |

## Official Documentation

* [Google Forms API Reference](https://developers.google.com/workspace/forms/api/reference/rest)
