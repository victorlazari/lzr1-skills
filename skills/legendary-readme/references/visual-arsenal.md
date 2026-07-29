# Visual Arsenal

> "A README with no visuals is a cover letter. A README with the right visuals is a movie trailer."

This is the grab-bag toolkit for every README visual that **isn't** deep ASCII/terminal-animation
technique (that's [Char Art and Animation](char-art-and-animation.md)) and **isn't** deep
Mermaid/table technique (that's [Tables, Diagrams, and Workflows](tables-diagrams-workflows.md)).
Use it in **Step 6: Add Visual Firepower** to assemble badges, banners, GIFs, theme-aware images,
and hidden surprises.

Everything here still obeys the **Visual Budget Rule**: 1 banner + 1 badge row + 2-3 GIFs + 1-2
diagrams + 1 footer, max. This file gives you the recipes; the budget still applies once you use
them.

---

## 1. Badges

Badges are the fastest way to communicate project health at a glance. They all come from
[shields.io](https://shields.io) (or a service that mimics its API), and they all live in one
row, directly under the title/tagline.

### Static badges

For anything shields.io doesn't auto-detect from a registry — a fixed claim you control by hand.

```markdown
![Made with Love](https://img.shields.io/badge/Made%20with-Love-red)
![Status](https://img.shields.io/badge/status-active-success)
```

### Dynamic badges (pull live data)

| Badge | Markdown |
| :--- | :--- |
| npm version | `![npm](https://img.shields.io/npm/v/PACKAGE_NAME)` |
| Build status (GitHub Actions) | `![Build](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/ci.yml)` |
| License | `![License](https://img.shields.io/github/license/OWNER/REPO)` |
| Downloads (npm, monthly) | `![Downloads](https://img.shields.io/npm/dm/PACKAGE_NAME)` |
| Tech stack (single language) | `![Go](https://img.shields.io/badge/Go-1.22-00ADD8?logo=go&logoColor=white)` |

Copy-paste examples, ready to drop under the title:

```markdown
![Version](https://img.shields.io/npm/v/legendary-readme?style=flat-square&color=blueviolet)
![License](https://img.shields.io/github/license/lerianstudio/legendary-readme?style=flat-square)
![Build](https://img.shields.io/github/actions/workflow/status/lerianstudio/legendary-readme/ci.yml?style=flat-square)
![Downloads](https://img.shields.io/npm/dm/legendary-readme?style=flat-square&color=orange)
![Go Version](https://img.shields.io/badge/Go-1.22-00ADD8?style=flat-square&logo=go&logoColor=white)
```

### Styling params

Shields.io badges take a `style` query param that controls the visual weight of the whole row:

| `style=` | Look | Best for |
| :--- | :--- | :--- |
| `flat` | Default, slight gradient | General use, no strong opinion needed |
| `flat-square` | Flat, no gradient, sharp corners | Minimal/modern READMEs (most common choice) |
| `for-the-badge` | Bold, uppercase, chunky | Personality level 3+, hero-row emphasis |
| `plastic` | Glossy, rounded, 2013-era GitHub look | Retro/nostalgia themes only |
| `social` | Rounded with a counter bubble (stars/followers) | Social-proof badges (GitHub stars, Twitter follow) |

**Rule: never mix badge styles in one row.** A `for-the-badge` badge next to a `flat-square`
badge looks like two different projects stitched together. Pick one `style=` value and apply it
to every badge in the row — set it once as a shared query param, not per-badge by accident.

### Grouping into one consistent row

Put every badge on consecutive lines directly under the title (Markdown renders adjacent images
as an inline-wrapping row) — don't scatter badges through the body of the README.

```markdown
# ProjectName

![Version](https://img.shields.io/npm/v/project?style=flat-square)
![Build](https://img.shields.io/github/actions/workflow/status/owner/project/ci.yml?style=flat-square)
![License](https://img.shields.io/github/license/owner/project?style=flat-square)
![Downloads](https://img.shields.io/npm/dm/project?style=flat-square)
```

Cap the row at **5-7 badges**. Past that, it stops reading as "trust signals" and starts reading
as noise — fold anything extra (coverage %, code climate grade, sponsor count) into the body or a
`docs/badges.md` if the project truly needs more.

---

## 2. Banners

A banner is the visual anchor right below (or replacing) the `# ProjectName` heading. Pick exactly
one approach — don't stack a capsule-render banner AND an SVG typing headline AND an ASCII banner.

### capsule-render (dynamic SVG header)

**[capsule-render](https://github.com/kyechan99/capsule-render)** generates a hosted, parametrized
SVG banner — no image file to commit, tunable via URL query params.

```markdown
![Header](https://capsule-render.vercel.app/api?type=waving&color=0:6D28D9,100:06B6D4&height=180&section=header&text=ProjectName&fontSize=60&fontColor=ffffff&animation=fadeIn)
```

Key params:

| Param | Values | Effect |
| :--- | :--- | :--- |
| `type` | `waving`, `rect`, `rounded`, `venom`, `soft`, `slice`, `transparent` | Shape of the banner |
| `color` | hex, or gradient `0:HEX,100:HEX` | Fill color / gradient stops |
| `height` | integer (px) | Banner height — keep it under the budget below |
| `text` | URL-encoded string | Headline text rendered on the banner |
| `fontSize` / `fontColor` | integer / hex | Text styling |
| `animation` | `fadeIn`, `blink`, `twinkling` | Optional looping motion (still SVG, not a GIF) |
| `section` | `header`, `footer` | Flip curvature direction — use `footer` to mirror the header at the bottom of the README |

### svg-banners (alternative)

**[svg-banners](https://github.com/Akshay090/svg-banners)** covers a similar niche with a
different visual set (chisel, wave-2, hero). Same usage pattern: point an `![]()` at the generated
URL with your text/theme baked into the query string.

### No-tool fallback: plain centered heading

When you don't want a third-party SVG dependency at all (offline builds, air-gapped docs, or a
Corporate Geek tone that wants zero decoration risk), a centered `<h1>` + tagline is a perfectly
legitimate banner:

```markdown
<h1 align="center">ProjectName</h1>
<p align="center"><em>One line that says what this is, in plain English.</em></p>
```

**Rule: keep total banner height under ~200px.** A banner taller than that pushes the Big Three
(What/Why/How) below the fold on a laptop screen, which defeats the entire purpose of a banner —
it's supposed to earn attention, not consume the reader's 3-second budget.

---

## 3. ASCII Art (pointer)

For static ASCII/Unicode wordmarks, box-drawing architecture sketches, and hand-built mascots, see
[Char Art and Animation](char-art-and-animation.md) for the full toolkit, generation tools, and
accessibility rules — don't duplicate that logic here.

---

## 4. Mermaid Diagrams (pointer)

For Mermaid diagram syntax, captioning rules, and the decision of when to reach for Mermaid vs. D2
vs. plain box-drawing, see [Tables, Diagrams, and Workflows](tables-diagrams-workflows.md) — that
file owns diagram technique end to end.

---

## 5. GIFs

GIFs are the highest-impact and highest-risk visual in a README: they sell "this actually works"
better than prose, but a bloated or jarring one tanks load time and trust in the same breath.

### Sourcing

| Source | When to use | Trade-off |
| :--- | :--- | :---: |
| **Giphy embed** (`![](https://media.giphy.com/media/ID/giphy.gif)`) | A reaction/humor GIF, not project-specific | Depends on Giphy staying up; zero hosting cost |
| **Self-hosted** (`docs/assets/*.gif`, committed) | Anything project-specific — demos, screenshots, UI walkthroughs | You own uptime and size, but it survives if a third party disappears |
| **Terminal-recording GIF** (VHS/asciinema) | "Watch the CLI actually run" | Full technique — see [Char Art and Animation](char-art-and-animation.md) §2, don't duplicate here |

Default to self-hosted for anything that demonstrates the product; reserve Giphy embeds for pure
humor/personality beats where the exact GIF doesn't need to survive forever.

### Etiquette

- **One clear subject per GIF.** A GIF trying to show "install, then configure, then run, then
  the dashboard" in one loop teaches nothing — split it into separate GIFs per Big-Three step, or
  cut it down to the single most convincing moment.
- **Don't autoplay something jarring above the fold.** GitHub GIFs autoplay and loop with no user
  control — a flashing, fast-cut, or loud-color GIF as the very first thing a reader sees reads as
  hostile, not exciting. Save high-energy GIFs for deeper sections (Contributing, Easter Eggs)
  where the reader has already opted in to the vibe.
- **Size/host discipline** — same budget as the terminal-recording rule in
  [Char Art and Animation](char-art-and-animation.md): commit to `docs/assets/` (or
  `.github/assets/`), run through `gifsicle -O3 --lossy=80`, target under 2MB with a hard cap of
  5MB, and reference by relative path so forks keep working.

---

## 6. Responsive Images (Dark/Light Mode)

GitHub renders READMEs in whatever theme the viewer has set. A banner or diagram with light text
on a transparent background disappears in light mode; dark text on transparent disappears in dark
mode. The fix is the `<picture>` tag with `prefers-color-scheme` media queries — GitHub's markdown
sanitizer allows this pattern natively.

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/banner-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/banner-light.png">
  <img alt="ProjectName banner" src="docs/assets/banner-light.png">
</picture>
```

- The trailing `<img>` is mandatory — it's the fallback for renderers that don't parse `<picture>`
  (some markdown-to-PDF exporters, RSS readers, older clients), so it must point at whichever
  variant is legible on a plain white background.
- Always set a real `alt` on the fallback `<img>`, not on the `<source>` tags (`<source>` doesn't
  support `alt`).
- Works identically for diagrams: a Mermaid-rendered PNG export, a capsule-render banner with two
  color params, or a screenshot taken once in each OS theme.

**Rule: every banner or diagram with a real contrast issue in one theme needs an explicit dark AND
light variant — not a single image that happens to "look OK" in both.** A gray-on-transparent
logo that's merely readable in dark mode and washed-out-but-technically-visible in light mode is
not a fix; if you can articulate which theme looks worse, that's the signal to generate the second
variant, not ship the compromise.

---

## 7. Visual Easter Eggs

Small surprises reward the readers who actually explore the file — collapsible sections, jokes
hidden where only the curious will find them, and content reachable only via a link, not the
visible nav.

### Collapsible `<details>` surprise

```markdown
<details>
<summary>🎉 You found the secret changelog haiku</summary>

Code once broken now,
tests are green, deploy at dawn —
ship it, then go home.

</details>
```

### Joke in alt text

Nobody reads alt text except screen-reader users and the terminally curious who right-click →
"Inspect" — perfect low-stakes real estate for a one-liner that doesn't interfere with the visible
page:

```markdown
![A very serious architecture diagram, drawn by someone who is clearly having a great time](docs/assets/architecture.png)
```

### Hidden section reachable only via anchor link

A section that exists in the file but is deliberately left out of the visible Table of Contents —
discoverable only by a footnote, a comment in the code examples, or a link buried in the FAQ that
says "there's more here" without saying what.

```markdown
<!-- Not listed in the ToC above. If you're reading the raw source, hi. -->
## <a name="you-found-it"></a> The Room Behind the Bookshelf

If you made it this far by reading the markdown source instead of the rendered page, you're
exactly the kind of person this project was built for.
```

**Rule: Easter eggs never carry load-bearing information.** Anything a user actually needs to
succeed (a required flag, a breaking-change warning) must live in the visible, linear flow — eggs
are for delight, not documentation.

---

## Visual Arsenal Checklist

- [ ] Every badge in the top row shares one `style=` value — no mixing `flat-square` with
      `for-the-badge` in the same row
- [ ] Badge row is 5-7 badges max; anything beyond that is moved into the body or a dedicated file
- [ ] Banner height stays under ~200px so the Big Three stay above the fold
- [ ] Exactly one banner technique is used (capsule-render, svg-banners, or plain heading) — not
      stacked with an ASCII banner or typing SVG in the same header
- [ ] Any banner or diagram with a real contrast problem in one theme ships both a dark AND a
      light variant via `<picture>` — not a single "good enough" image
- [ ] Every `<picture>` block has a fallback `<img>` with a real `alt`, not a filename
- [ ] Every GIF has one clear subject; nothing jarring or autoplaying sits above the fold
- [ ] All committed GIFs live in `docs/assets/` (or `.github/assets/`), are under 5MB (ideally
      under 2MB), and were run through `gifsicle -O3`
- [ ] Terminal-recording GIFs and ASCII art follow [Char Art and Animation](char-art-and-animation.md)
      instead of being reinvented here
- [ ] Easter eggs (collapsible `<details>`, alt-text jokes, hidden anchors) carry zero load-bearing
      information — everything essential is also in the visible, linear flow
- [ ] Total visual count still respects the Visual Budget Rule: 1 banner + 1 badge row + 2-3 GIFs
      + 1-2 diagrams + 1 footer
