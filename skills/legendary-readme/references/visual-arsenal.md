# Visual Arsenal

This reference dictates how to use dynamic media effectively in GitHub READMEs.

## 1. Light and Dark Mode Safe Images

GitHub supports specifying different images for light and dark themes using URL fragments.
Always provide both versions for critical assets like logos and architecture diagrams.

**Syntax:**
```markdown
![Logo Light Mode](https://example.com/logo-light.png#gh-light-mode-only)
![Logo Dark Mode](https://example.com/logo-dark.png#gh-dark-mode-only)
```

## 2. Dynamic Media (GIFs and Videos)

- **GIFs:** Use GIFs to demonstrate CLI tools, UI interactions, or brief workflows. Keep them under 5MB. Place them immediately after the "Quick Start" or "Features" section.
- **Videos:** GitHub supports MP4 and WebM video uploads. Use them for longer tutorials.

## 3. Charts and Diagrams

- Use Mermaid.js for architecture, sequence, and state diagrams. It renders natively in GitHub Markdown.
- If static charts (PNG/SVG) are required, ensure they have transparent or theme-adaptive backgrounds.

## 4. PDFs and Extended Documentation

- Do not embed PDFs directly in the README.
- Link to PDFs using clear, descriptive text (e.g., "Read the full Whitepaper (PDF)").

## 5. Badges

- Use Shields.io for standard badges.
- Group badges logically (e.g., Build Status, Versioning, License).
- For pyOpenSci packages, badges MUST include: CI/test coverage, docs building, Python versions, current package version, and the pyOpenSci peer-review badge.
