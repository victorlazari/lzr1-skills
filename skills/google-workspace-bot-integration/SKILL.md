---
name: google-workspace-bot-integration
description: Comprehensive documentation for integrating a bot application with the Google Workspace stack. Use when designing, building, or documenting bot commands and workflows for Gmail, Calendar, Sheets, Slides, Docs, Drive, Forms, Contacts, and Tasks.
---

# Google Workspace Bot Integration

This skill provides comprehensive documentation and reference material for integrating a bot application with the Google Workspace stack. It outlines all possible actions and capabilities your bot can execute across 9 different Google applications.

## Overview

The integration empowers the bot to handle communication workflows, seamless scheduling, data entry, automated document generation, and asset organization directly from chat interfaces or automated triggers.

## Available Integrations

For detailed capabilities, actions, and bot command examples, refer to the specific reference file for the application you are integrating with:

* **Communication & Scheduling**
  * **Gmail**: Read [references/gmail.md](references/gmail.md) for email sending, drafting, and inbox organization.
  * **Calendar**: Read [references/calendar.md](references/calendar.md) for event management and schedule coordination.
  * **Contacts (People API)**: Read [references/contacts.md](references/contacts.md) for address book and group management.

* **Productivity & Documents**
  * **Docs**: Read [references/docs.md](references/docs.md) for document generation and template management.
  * **Sheets**: Read [references/sheets.md](references/sheets.md) for data entry, retrieval, and formatting.
  * **Slides**: Read [references/slides.md](references/slides.md) for presentation creation and template population.

* **Organization & Workflow**
  * **Drive**: Read [references/drive.md](references/drive.md) for file storage, organization, and access management.
  * **Forms**: Read [references/forms.md](references/forms.md) for survey creation and response analysis.
  * **Tasks**: Read [references/tasks.md](references/tasks.md) for to-do list management and tracking.

## Usage Guidelines

1. **Identify the Target Application**: Determine which Google Workspace application the bot needs to interact with.
2. **Consult the Reference**: Open the corresponding reference file to understand the available actions and API capabilities.
3. **Review Examples**: Use the provided bot command examples to design natural language triggers or automated workflows.
4. **Implementation**: Refer to the official Google API documentation linked in each reference file for technical implementation details.

---

## Adversarial Verification Panel

For each significant integration recommendation produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong integration recommendations from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Gmail Agent, Calendar Agent, Contacts Agent, Docs Agent, Sheets Agent, Slides Agent, Drive Agent, Forms Agent, and Tasks Agent) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Drive Agent recommends storing a generated document in a specific shared folder while the Docs Agent recommends creating it in the user's root Drive — contradicting the file organization strategy)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified integration workflow so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
