# Visual Arsenal: Badges, Banners, ASCII Art, and Diagrams

> "A picture is worth a thousand words. A well-placed GIF is worth a thousand stars."

This reference covers every visual technique available for making your README a visual masterpiece that works on GitHub, GitLab, and other platforms.

---

## Table of Contents

- [Header Banners](#header-banners)
- [Badges and Shields](#badges-and-shields)
- [ASCII Art](#ascii-art)
- [Mermaid.js Diagrams](#mermaidjs-diagrams)
- [GIFs and Screenshots](#gifs-and-screenshots)
- [Dark/Light Mode Support](#darklight-mode-support)
- [Custom HTML Layouts](#custom-html-layouts)
- [Visual Easter Eggs](#visual-easter-eggs)

---

## Header Banners

### Capsule Render (Dynamic SVG — No Hosting Required)

Base URL: `https://capsule-render.vercel.app/api`

| Parameter | Options | Description |
| :--- | :--- | :--- |
| `type` | `waving`, `egg`, `shark`, `slice`, `rect`, `soft`, `rounded`, `cylinder`, `venom`, `transparent` | Banner shape |
| `color` | `auto`, `gradient`, `timeAuto`, hex code, `0:COLOR1,100:COLOR2` | Color scheme |
| `height` | Number (px) | Banner height |
| `text` | URL-encoded string | Display text |
| `fontSize` | Number | Text size |
| `fontColor` | Hex code (no #) | Text color |
| `animation` | `fadeIn`, `scaleIn`, `blink`, `blinking`, `twinkling` | Text animation |
| `section` | `header`, `footer` | Position |
| `desc` | URL-encoded string | Subtitle text |

**Popular Combinations:**

```markdown
<!-- Waving gradient with animation -->
![Header](https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=ProjectName&fontSize=50&fontColor=fff&animation=twinkling)

<!-- Minimal transparent with color accent -->
![Header](https://capsule-render.vercel.app/api?type=transparent&color=auto&height=120&text=ProjectName&fontSize=40&fontAlignY=50)

<!-- Venom style (dramatic) -->
![Header](https://capsule-render.vercel.app/api?type=venom&color=0:8B5CF6,100:EC4899&height=200&text=ProjectName&fontSize=50&fontColor=fff)

<!-- Footer wave -->
![Footer](https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer)
```

### Typing Effect (Animated Taglines)

```markdown
<p align="center">
  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=6366F1&center=true&vCenter=true&random=false&width=600&lines=Build+Legendary+READMEs;Make+Documentation+Fun+Again;Write+Once%2C+Impress+Forever" alt="Typing SVG" />
  </a>
</p>
```

Parameters: `font`, `weight`, `size`, `pause` (ms between lines), `color`, `center`, `vCenter`, `width`, `lines` (separated by `;`).

---

## Badges and Shields

### Badge Anatomy

URL pattern: `https://img.shields.io/badge/LABEL-MESSAGE-COLOR?style=STYLE&logo=LOGO&logoColor=LOGOCOLOR`

### Style Options

| Style | Look | Best For |
| :--- | :--- | :--- |
| `flat` | Default, clean | General use |
| `flat-square` | No rounded corners | Modern, minimal |
| `for-the-badge` | Large, bold | Headers, CTAs |
| `plastic` | Glossy, 3D | Retro feel |
| `social` | GitHub-style | Social metrics |

### Essential Badge Categories

**Project Health:**
```markdown
![Build](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml?style=flat-square&label=build)
![Coverage](https://img.shields.io/codecov/c/github/user/repo?style=flat-square)
![Version](https://img.shields.io/github/v/release/user/repo?style=flat-square)
![Downloads](https://img.shields.io/npm/dm/package-name?style=flat-square)
```

**Tech Stack:**
```markdown
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=node.js&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
```

**Fun/Personality Badges:**
```markdown
![Powered by Coffee](https://img.shields.io/badge/Powered_by-Coffee-brown?style=flat-square&logo=buymeacoffee&logoColor=white)
![Works on My Machine](https://img.shields.io/badge/Works_on-My_Machine-green?style=flat-square)
![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square)
![Made with Love](https://img.shields.io/badge/Made_with-❤️-red?style=flat-square)
![Mass of Bugs](https://img.shields.io/badge/Bugs-Features-blue?style=flat-square)
![Sleep Deprived](https://img.shields.io/badge/Built_at-3AM-purple?style=flat-square)
```

**Social/Community:**
```markdown
![Stars](https://img.shields.io/github/stars/user/repo?style=social)
![Forks](https://img.shields.io/github/forks/user/repo?style=social)
![Discord](https://img.shields.io/discord/SERVER_ID?style=flat-square&logo=discord&logoColor=white&label=Discord)
![Twitter Follow](https://img.shields.io/twitter/follow/username?style=social)
```

### Custom Badge Builder

For any custom badge: `https://img.shields.io/badge/LABEL-MESSAGE-COLOR`

- Replace spaces with `_` or `%20`
- Replace `-` with `--` (double dash)
- Colors: named (`green`, `blue`) or hex (`FF6B6B`)

---

## ASCII Art

### When to Use ASCII Art

- Terminal-focused projects (CLI tools, shell scripts)
- Retro/hacker aesthetic (personality level 4-5)
- Project logos when no image is available
- Section dividers for dramatic effect

### ASCII Art Generators

Use these tools, then paste the output in a code block:

- **figlet** — Classic block letters: `figlet -f slant "ProjectName"`
- **toilet** — Colored ASCII: `toilet -f mono12 "ProjectName"`
- **boxes** — Decorative borders: `echo "text" | boxes -d stone`

### Pre-Made Patterns

**Simple divider:**
```
═══════════════════════════════════════════════════════
```

**Retro computer:**
```
┌──────────────────────────────────────────────────┐
│  ██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗│
│  ██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝│
│  ██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║   │
│  ██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║   │
│  ██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║   │
│  ╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝   │
└──────────────────────────────────────────────────┘
```

**Minimal box:**
```
╔═══════════════════════════════╗
║   ProjectName v2.0            ║
║   "Making things less broken" ║
╚═══════════════════════════════╝
```

---

## Mermaid.js Diagrams

GitHub renders Mermaid natively. No images needed. Always prefer Mermaid over static diagrams.

### Flowchart (Decision/Process)

````markdown
```mermaid
graph TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Don't touch it]
    B -->|No| D{Did you change something?}
    D -->|Yes| E[Undo it]
    D -->|No| F[It's DNS]
    E --> B
    F --> B
```
````

### Sequence Diagram (API Flows)

````markdown
```mermaid
sequenceDiagram
    actor User
    participant App
    participant API
    participant DB

    User->>App: Click "Save"
    App->>API: POST /data
    API->>DB: INSERT INTO...
    DB-->>API: OK (id: 42)
    API-->>App: 201 Created
    App-->>User: "Saved! ✓"
```
````

### State Diagram (Lifecycle)

````markdown
```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Review : Submit
    Review --> Approved : Accept
    Review --> Draft : Request Changes
    Approved --> Published : Deploy
    Published --> Archived : Deprecate
    Archived --> [*]
```
````

### Git Graph (Branching Strategy)

````markdown
```mermaid
gitGraph
    commit id: "init"
    commit id: "feat: core"
    branch develop
    checkout develop
    commit id: "feat: api"
    commit id: "feat: auth"
    checkout main
    merge develop id: "v1.0.0" tag: "v1.0.0"
    branch hotfix
    commit id: "fix: security"
    checkout main
    merge hotfix id: "v1.0.1" tag: "v1.0.1"
```
````

### Pie Chart (Distribution)

````markdown
```mermaid
pie title Language Distribution
    "TypeScript" : 65
    "Rust" : 20
    "Python" : 10
    "Shell" : 5
```
````

### Timeline (Project History)

````markdown
```mermaid
timeline
    title Project History
    2022 : Initial concept
         : First prototype
    2023 : v1.0 release
         : 1000 stars
    2024 : v2.0 rewrite
         : Enterprise features
         : 10K users
```
````

---

## GIFs and Screenshots

### Best Practices

| Aspect | Recommendation |
| :--- | :--- |
| Format | GIF for short demos (<30s), MP4/WebM for longer |
| Width | 600-800px (fits most screens without scrolling) |
| Duration | 5-15 seconds ideal, loop if possible |
| File size | Under 5MB (GitHub has a 10MB limit) |
| Content | Show the "wow moment" — the thing that makes people want to use it |

### Recording Tools

- **Terminal**: [asciinema](https://asciinema.org/) (records as text, tiny files)
- **Screen**: [Kap](https://getkap.co/) (macOS), [Peek](https://github.com/phw/peek) (Linux), [ScreenToGif](https://www.screentogif.com/) (Windows)
- **Browser**: Chrome DevTools → Performance → Screenshot

### Embedding Patterns

```markdown
<!-- Centered GIF with caption -->
<p align="center">
  <img src="./docs/demo.gif" alt="Demo showing the main workflow" width="700" />
  <br />
  <em>Creating a new project in under 10 seconds</em>
</p>

<!-- Side-by-side comparison -->
<table>
  <tr>
    <td align="center"><strong>Before</strong></td>
    <td align="center"><strong>After</strong></td>
  </tr>
  <tr>
    <td><img src="./docs/before.png" width="400" alt="Before: messy output" /></td>
    <td><img src="./docs/after.png" width="400" alt="After: clean output" /></td>
  </tr>
</table>
```

---

## Dark/Light Mode Support

GitHub supports theme-aware images using the `<picture>` element.

### Pattern: Swap Entire Images

```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./docs/logo-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./docs/logo-light.svg">
  <img alt="ProjectName Logo" src="./docs/logo-light.svg" width="300">
</picture>
```

### Pattern: Theme-Aware Diagrams

```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./docs/architecture-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="./docs/architecture-light.png">
  <img alt="System architecture diagram" src="./docs/architecture-light.png" width="100%">
</picture>
```

### Tip: Mermaid Auto-Adapts

Mermaid.js diagrams automatically adapt to GitHub's dark/light mode. This is another reason to prefer Mermaid over static images.

---

## Custom HTML Layouts

GitHub Markdown supports a subset of HTML for advanced layouts.

### Centered Content Block

```html
<div align="center">

  **ProjectName** — Your tagline here

  [Website](https://example.com) · [Docs](https://docs.example.com) · [Discord](https://discord.gg/xxx)

</div>
```

### Two-Column Layout

```html
<table>
  <tr>
    <td width="50%" valign="top">

### 🎯 For Users

- Easy installation
- Zero configuration
- Works out of the box

    </td>
    <td width="50%" valign="top">

### 🔧 For Developers

- Extensible plugin API
- Full TypeScript support
- Comprehensive test suite

    </td>
  </tr>
</table>
```

### Feature Showcase Cards

```html
<table>
  <tr>
    <td align="center" width="33%">
      <img src="./docs/icon-speed.png" width="60" alt="Speed" /><br />
      <strong>Fast</strong><br />
      <sub>Sub-ms latency</sub>
    </td>
    <td align="center" width="33%">
      <img src="./docs/icon-secure.png" width="60" alt="Secure" /><br />
      <strong>Secure</strong><br />
      <sub>Zero-trust by default</sub>
    </td>
    <td align="center" width="33%">
      <img src="./docs/icon-simple.png" width="60" alt="Simple" /><br />
      <strong>Simple</strong><br />
      <sub>3 lines to start</sub>
    </td>
  </tr>
</table>
```

---

## Visual Easter Eggs

### The Hidden Image

```markdown
<!-- This comment contains a secret message for source-code readers:
     ___
    /   \
   | o o |
    \_^_/
   You found Blobby! The unofficial mascot.
   Blobby says: "Star this repo and good things will happen."
-->
```

### The Expandable Art Gallery

```markdown
<details>
<summary>🎨 Click for unnecessary but delightful art</summary>

```
    /\_/\
   ( o.o )
    > ^ <   "I helped write this README"
   /|   |\
  (_|   |_)
```

</details>
```

### The Progress Bar (Fake but Fun)

```markdown
**Project Completion:**

```
██████████████████████░░░░░ 84% — Almost there!
```

**Documentation Quality:**

```
████████████████████████████ 100% — You're reading proof
```
```

### Star History Chart

```markdown
## ⭐ Star History

<a href="https://star-history.com/#user/repo&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=user/repo&type=Date&theme=dark" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=user/repo&type=Date" />
    <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=user/repo&type=Date" width="600" />
  </picture>
</a>
```
