# Google Contacts (People API) Integration Reference

The Google People API provides programmatic access to Google Contacts data, allowing interaction with profiles, contacts, and contact groups. This integration ensures the bot can manage and utilize the organization's address book.

## Core Capabilities

The bot creates new contacts, populating fields such as names, email addresses, phone numbers, and organizational affiliations. It modifies existing contact details or deletes outdated contacts. The bot searches for contacts by name or email to retrieve necessary information. It also manages contact groups (labels) by creating new groups, modifying group names, and adding or removing members. If authorized, the bot can access the broader Google Workspace directory to retrieve domain profiles and organizational contacts.

## Action Categories and Examples

| Action Category | Description | Example Bot Command |
| :--- | :--- | :--- |
| **Contact Management** | Create, update, or delete individual contacts. | *"Add a new contact for 'Alice Walker' with email 'alice@partner.com' and phone '555-0192'."* <br><br> *"Update the company name for 'Charlie Davis' to 'Globex Corporation'."* |
| **Information Retrieval** | Search the address book for contact details. | *"Find the phone number for 'Bob' in my contacts."* |
| **Group Organization** | Create and manage contact groups/labels. | *"Create a new contact group called 'VIP Clients' and add @client1 and @client2 to it."* |

## Official Documentation

* [Google People API Reference](https://developers.google.com/people/api/rest)
