# Rendering Pipeline Configuration

**Verified against upstream:** 2026-08-07
**Primary Source:** https://docs.requarks.io/rendering

This guide covers customizing the rendering pipeline in Wiki.js, including KaTeX, MathJax, Mermaid, and PlantUML.

## Overview

Wiki.js supports various rendering engines to process specific content blocks (e.g., math formulas, diagrams) within pages. These can be configured in the **Administration > Rendering** section.

## Supported Engines

- **KaTeX / MathJax:** For rendering mathematical formulas. KaTeX is generally faster, while MathJax offers broader compatibility.
- **Mermaid:** For rendering diagrams and flowcharts from text definitions.
- **PlantUML:** For rendering UML diagrams. Requires a separate PlantUML server.

## Configuration Steps

1. Navigate to **Administration > Rendering**.
2. Enable the desired rendering engines.
3. Configure engine-specific settings (e.g., PlantUML server URL).
4. Apply changes. The rendering pipeline will automatically process relevant code blocks in pages.
