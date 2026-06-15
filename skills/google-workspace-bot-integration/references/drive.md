# Google Drive Integration Reference

The Google Drive API allows the bot to manage files, folders, permissions, and file metadata. This integration acts as the central nervous system for organizing the workspace's digital assets.

## Core Capabilities

The bot facilitates file transfers by uploading new files to Drive or downloading file contents. It organizes the workspace by creating folders, moving files between directories, and copying existing files. The bot executes complex searches for files or folders based on names, types, owners, or content keywords. Crucially, it manages permissions by sharing files or folders with specific users or groups, setting access levels (viewer, commenter, editor), and revoking access when necessary. It also updates file metadata, such as names and descriptions, and manages the trash bin.

## Action Categories and Examples

| Action Category | Description | Example Bot Command |
| :--- | :--- | :--- |
| **Organization & Storage** | Create folders, move files, and upload assets. | *"Create a new folder in Drive called 'Client Y Deliverables' and move the three attached PDFs into it."* |
| **Access Management** | Share files and configure user permissions. | *"Share the 'Q3 Financials' spreadsheet with @finance_team and give them editor access."* |
| **Search & Metadata** | Locate files and update file names or descriptions. | *"Find all documents owned by me containing the word 'Confidential' and list them."* <br><br> *"Copy the 'Standard Contract' file, rename it to 'Contract - Acme Corp', and share it with @legal."* |

## Official Documentation

* [Google Drive API Reference](https://developers.google.com/workspace/drive/api/reference/rest/v3)
