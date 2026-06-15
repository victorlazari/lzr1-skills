# Google Sheets Integration Reference

The Google Sheets API allows the bot to read, write, and format data within spreadsheets. This capability is essential for automating data entry, reporting, and dashboard management.

## Core Capabilities

The bot retrieves values from specific cells, ranges, or entire sheets for analysis. It can write or update data by appending new rows or modifying specific cells using batch update requests. Formatting capabilities include applying text styles, colors, borders, and conditional formatting rules to highlight key metrics. The bot also manages the structure of the spreadsheet by adding, deleting, renaming, or copying individual sheets (tabs). Furthermore, it can interact with embedded charts and apply data filters or sorting rules to organize information.

## Action Categories and Examples

| Action Category | Description | Example Bot Command |
| :--- | :--- | :--- |
| **Data Entry & Updates** | Append rows and modify specific cell values. | *"Append the weekly sales metrics from this slack thread into the 'Q3 Sales' Google Sheet."* <br><br> *"Find the row for 'Client X' in the CRM sheet and update their status to 'Onboarded'."* |
| **Data Retrieval** | Read values and extract information based on criteria. | *"Read the status column in the 'Project Tracker' sheet and list all tasks marked as 'Blocked'."* |
| **Formatting & Structure** | Create tabs and apply visual formatting rules. | *"Create a new tab in the 'Financials' spreadsheet named 'October Expenses'."* <br><br> *"Format the header row of the 'Inventory' sheet to be bold with a blue background."* |

## Official Documentation

* [Google Sheets API Reference](https://developers.google.com/workspace/sheets/api/reference/rest)
