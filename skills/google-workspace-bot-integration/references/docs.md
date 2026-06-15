# Google Docs Integration Reference

The Google Docs API allows the bot to read document content and make structured edits via batch updates. This integration is vital for automated document generation, contract drafting, and note-taking.

## Core Capabilities

The bot creates new, blank documents and reads existing content, extracting full text along with structural elements like paragraphs, tables, and lists. It modifies documents by inserting new text at specific indexes or deleting content ranges. Similar to Slides, the bot performs global find-and-replace operations to populate document templates. It also applies formatting styles, such as bolding, italics, and heading levels, and inserts structural elements like tables, lists, or images directly into the document flow.

## Action Categories and Examples

| Action Category | Description | Example Bot Command |
| :--- | :--- | :--- |
| **Document Generation** | Create new docs and append content. | *"Create a new Google Doc with the transcript of this meeting and share the link."* <br><br> *"Append the incident post-mortem summary to the bottom of the 'Q2 Outages' document."* |
| **Template Management** | Execute find-and-replace for dynamic document drafting. | *"Take the 'Offer Letter' template, replace {{Candidate_Name}} with 'Jane Doe', and replace {{Salary}} with '$100,000'."* |
| **Content Extraction** | Read and extract specific sections of a document. | *"Read the 'Project Requirements' doc and extract all the bullet points under the 'Phase 1' heading."* |

## Official Documentation

* [Google Docs API Reference](https://developers.google.com/workspace/docs/api/reference/rest)
