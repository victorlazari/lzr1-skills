# Google Slides Integration Reference

The Google Slides API provides the ability to create and modify presentations, slides, and page elements. This integration streamlines the generation of reports, pitch decks, and recurring meeting materials.

## Core Capabilities

The bot can generate entirely new, blank presentations or manage slides within an existing deck by adding, duplicating, or deleting them. It manipulates text by inserting, deleting, or globally replacing specific text strings, which is particularly useful for populating presentation templates with dynamic data. The bot also manages visual elements by inserting, resizing, moving, or cropping images and shapes. Finally, it can update text formatting, shape background colors, and interact with table elements on the slides.

## Action Categories and Examples

| Action Category | Description | Example Bot Command |
| :--- | :--- | :--- |
| **Template Population** | Replace variables with dynamic text across presentations. | *"Create a new presentation from the 'Monthly Review' template and replace the {{Month}} variable with 'August'."* |
| **Content Insertion** | Add new slides, text blocks, and images to decks. | *"Add a new slide to the end of the 'Pitch Deck' presentation and insert the summary text from this channel."* <br><br> *"Insert the generated chart image into slide 3 of the 'Metrics Report'."* |
| **Slide Modification** | Update existing slide titles and formatting. | *"Update the title slide of the 'Team All-Hands' presentation to say 'Q4 Kickoff'."* |

## Official Documentation

* [Google Slides API Reference](https://developers.google.com/workspace/slides/api/reference/rest)
