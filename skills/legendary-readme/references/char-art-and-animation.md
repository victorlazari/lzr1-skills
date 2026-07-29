# Char Art and Animation

> "Real hackers don't need a design team. They need a monospace font and a grudge."

This is the toolkit for making a README look like it was *typed*, not designed — ASCII/Unicode
art, fake terminal sessions that actually play, SVG text that animates without a GIF file, and
retro-CRT/Matrix flourishes. Use it inside **Step 6: Add Visual Firepower** whenever the theme or
personality level (3+, Playful Hacker and up) calls for a geeky, hand-built visual instead of a
stock badge or screenshot.

Everything here obeys the **Visual Budget Rule** from the main skill: these elements compete for
the same 2-3 GIF / 1-2 diagram slots as anything else. Pick the ONE technique that fits the
theme, don't stack all four.

---

## Decision Table: Which Technique Fits?

| You want... | Use | Renders natively on GitHub? | File to host? |
| :--- | :--- | :---: | :---: |
| A logo/mascot that never moves | Static ASCII/Unicode art | ✅ (in a code fence) | No |
| A tiny architecture sketch made of boxes and arrows | Box-drawing diagram | ✅ (in a code fence) | No |
| "Watch me actually run this command" | Terminal-recording GIF (VHS/asciinema) | ✅ (as `<img>`) | Yes |
| A typing headline under the project name | SVG typing/wave banner | ✅ (as `<img>`) | No (hosted by a service, or self-generated once and committed) |
| Full nerd-mode chaos (Matrix rain, glitch, CRT) | Composited GIF or animated SVG | ✅ (as `<img>`) | Usually yes |

Rule of thumb: **if it doesn't need to move, don't make it move.** A static ASCII banner in a
code fence loads instantly, is copy-pasteable, greppable, and never breaks — an animated GIF is
none of those things. Reach for motion only when the motion itself is the joke or the demo.

---

## 1. Static ASCII / Unicode Art

The cheapest, most durable geek flex in the toolkit. No hosting, no dependencies, renders
everywhere including `cat README.md` in a raw terminal.

### Banner text (figlet-style wordmarks)

Generate block-letter project names with any of these, then paste the output straight into a
fenced code block:

- **[patorjk.com/software/taag](http://patorjk.com/software/taag/)** — the web figlet generator; hundreds of fonts, copy-paste output directly
- **`figlet`** (CLI, `brew install figlet` / `apt install figlet`) — `figlet -f slant "MyProject"`
- **`toilet`** (`figlet`'s louder cousin) — adds color/filters for terminal use, but for README purposes just take the plain output
- **`cfonts`** (npm) — good defaults for camelCase project names, run once and paste the output, don't ship it as a runtime dependency

```
    __  ____     ______           _           __
   /  |/  (_)___/ / __ /___  ____(_)___  _____/ /_
  / /|_/ / / __  / / / __ \/ __/ / __ \/ ___/ __/
 / /  / / / /_/ / /_/ / /_/ / /  / /_/ / /__/ /_
/_/  /_/_/\__,_/\____/\____/_/  /_/ .___/\___/\__/
                                 /_/
```

**Rules:**
- Wrap in a fenced code block (\`\`\`text or plain triple backticks) — never an `<img>` for text
  art. This keeps it selectable, screen-reader-skippable via the code semantics, and immune to
  GitHub's markdown line-wrapping.
- Cap width at **80 columns**. Anything wider truncates or wraps ugly on mobile GitHub and in
  narrow terminals; test by resizing your browser to ~600px.
- Pick a font where every character renders in monospace without lookalike collisions (avoid
  fonts that lean on `_`/`-` baseline tricks that shift under different monospace fonts —
  GitHub, VS Code, and a raw terminal don't all use the same one).
- One banner per README, at the very top, immediately after or instead of the `# ProjectName`
  heading. A second ASCII banner deeper in the doc reads as clutter, not charm.

### Box-drawing diagrams

Unicode box-drawing characters (`─│┌┐└┘├┤┬┴┼╔╗╚╝║═`) let you sketch a tiny architecture or data-
flow diagram that renders identically everywhere, with zero external tooling. Use this for a
2-4 node sketch; for anything bigger, use a real Mermaid diagram (see
[Tables, Diagrams, and Workflows](tables-diagrams-workflows.md)) instead — box art gets unreadable
past about 5 boxes.

```
┌─────────┐      ┌─────────┐      ┌─────────┐
│  Client │─────▶│   API   │─────▶│   DB    │
└─────────┘      └────┬────┘      └─────────┘
                       │
                       ▼
                 ┌─────────┐
                 │  Cache  │
                 └─────────┘
```

**Rules:**
- Draw it in a monospace editor with a fixed grid (or generate it with a tool like
  [asciiflow.com](https://asciiflow.com) or `graph-easy`) — hand-aligning box corners in a
  proportional font guarantees drift once someone edits a label.
- Every box needs a label short enough to fit without wrapping the box.
- Caption it in plain English immediately below (see **Accessibility**, below) — box art alone
  fails anyone using a screen reader or a font where alignment breaks.

### Mascot / pixel art

A small (≤20 lines tall, ≤40 cols wide) ASCII/Unicode mascot reinforces a theme (see
[Theme Engine](theme-engine.md)) without needing an artist. Keep it recognizable at a glance —
silhouette over detail. Block elements (`█▓▒░`) read better than punctuation art at small sizes
for anything meant to look "pixel," while punctuation art (`/\|_-.()`) reads better for line-based
mascots (ghosts, robots, animals).

---

## 2. Terminal-Style Animated GIFs

For "watch this actually run" demos — installing the CLI, running the one command from the Big
Three, a REPL session. This is the highest-value animated element in a dev-tool README because it
answers "does this really work?" better than any prose.

### Recommended toolchain: script it, don't screen-record it

Never freehand a screen recording for this — timing is inconsistent, mistakes are baked in, and
re-recording after a typo means starting over. Script the exact keystrokes and let a tool play
them back deterministically.

| Tool | What it does | Output |
| :--- | :--- | :--- |
| **[VHS](https://github.com/charmbracelet/vhs)** (Charm) | Write a `.tape` script (`Type`, `Sleep`, `Enter`, `Screenshot`) → renders a real terminal | GIF, MP4, or WebM |
| **[asciinema](https://asciinema.org/) + [agg](https://github.com/asciinema/agg)** | Record a real terminal session as text (tiny file), convert to GIF with `agg` | GIF (or keep as `.cast` + embed player) |
| **[termtosvg](https://github.com/nbedos/termtosvg)** | Records a session straight to animated SVG | SVG (scalable, tiny file size) |
| **[terminalizer](https://github.com/faressoft/terminalizer)** | Record + theme + render to GIF | GIF |

**Default recommendation: VHS.** It's declarative, diffable, and re-runnable in CI — check the
`.tape` file into the repo (e.g. `docs/demo.tape`) so the GIF can be regenerated whenever the CLI
output changes, instead of going stale.

Example `docs/demo.tape`:

```
Output docs/demo.gif

Set Theme "Dracula"
Set FontSize 18
Set Width 900
Set Height 500

Type "npx create-awesome-thing my-project"
Sleep 500ms
Enter
Sleep 3s
Type "cd my-project && npm run dev"
Enter
Sleep 2s
Screenshot docs/demo-final.png
```

### File size and embedding discipline

- **Target under 2 MB, hard cap 5 MB.** GitHub renders large GIFs by lazily loading them, which
  reads as "broken image" on a slow connection — the opposite of the effect you want.
- Run every GIF through **`gifsicle -O3 --lossy=80`** before committing. This alone typically cuts
  size 50-70% with no visible quality loss for a terminal recording (flat colors, little motion).
- Width **800-900px max**. A terminal GIF doesn't need retina resolution to be readable — cap
  `Set Width`/`Set Height` in the VHS script rather than downscaling after the fact.
- Keep clips **short (8-15 seconds)**. Loop a short, punchy demo rather than recording a 40-second
  saga — README GIFs autoplay and loop, so viewers will see it more than once anyway.
- Commit GIFs to `docs/assets/` or `.github/assets/` (both are git-tracked, not `.gitignored`, and
  don't trigger GitHub's "large file" warnings the way root-level binaries sometimes do) and
  reference with a relative path, not an absolute URL — this keeps demos working in forks.

---

## 3. SVG-Based Text/Typing Animations

These animate **without shipping a GIF file at all** — the browser's SVG/CSS engine does the
animation, so the asset is a few KB of markup instead of a few MB of raster frames, and it's
crisp at any zoom level and in both light/dark mode.

### Typing headline (most common use)

**[readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg)** generates a hosted SVG
that types out a rotating list of lines, no build step:

```markdown
[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=00FF9C&center=true&vCenter=true&width=600&lines=Ship+faster.;Break+less.;Sleep+more.)](https://git.io/typing-svg)
```

Tune `color` to match the project's [Visual Style](visual-style-system.md) palette, and keep the
`lines` list to 3-4 short phrases — more than that and the animation never finishes a loop before
the reader scrolls past.

### Animated banner (wave/rect/venom types)

**[capsule-render](https://github.com/kyechan99/capsule-render)** covers the animated-header case
already referenced in [Visual Arsenal](visual-arsenal.md); the animated types (`waving`,
`venom`, `rect` with `animation=fadeIn`) are the geek-relevant ones here — they render as looping
SVG, not GIF, so they stay sharp and small.

### Hand-rolled: a blinking cursor with zero dependencies

For full control (exact theme colors, exact font, no third-party hosting dependency), a typing
cursor is trivial to hand-roll as raw SVG using **SMIL** (`<animate>`), which GitHub's markdown
sanitizer allows even though it strips `<script>`:

```xml
<svg width="340" height="40" xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="28" font-family="monospace" font-size="22" fill="#39ff14">
    $ npm install legendary-readme
  </text>
  <rect x="326" y="8" width="10" height="24" fill="#39ff14">
    <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
  </rect>
</svg>
```

Save as `docs/assets/cursor.svg` and embed with `![](docs/assets/cursor.svg)`. Because it's
self-hosted, it has no third-party dependency to go down, unlike services like readme-typing-svg.

**Rule:** commit self-hosted SVGs to the repo rather than pointing at a personal CDN/gist — a
README's visuals should survive the original author disappearing.

---

## 4. Matrix / Glitch / Retro-CRT Effects

Reserve these for **personality level 4-5 (Full Nerd Mode / Chaotic Genius)** projects or a theme
that explicitly calls for them (Neon Hacker, Retro Arcade — see
[Theme Engine](theme-engine.md)). On a Corporate Geek or Friendly Nerd README these read as noise,
not charm.

### Matrix rain

Simplest path: a short (5-8s) looped GIF of green falling characters, generated once with a
terminal Matrix-rain script (`cmatrix`, or any of the countless "matrix rain" CodePens) recorded
via VHS/`agg` exactly like a terminal demo, then treated with the same size budget as
Section 2. Use it **only** as a header/footer background flourish, never as the sole way to
convey the Big Three — motion should never be the only channel carrying information.

### Glitch text

Light glitch effects (a CSS `text-shadow` split-RGB animation, delivered as SVG/GIF) work for a
single headline; avoid Unicode "Zalgo" combining-character glitch text
(`T̸͎̊h̷͈͌i̶̡͐s̶̈́`) in running prose — it breaks screen readers, breaks search/grep, and often
renders as mangled boxes on older systems. If you want the Zalgo look, confine it to a single
decorative word inside an image/SVG, never in live selectable text.

### CRT / scanline border

A subtle scanline overlay (repeating semi-transparent horizontal lines + a slight vignette) on a
banner image sells "retro terminal" cheaply. Apply it as a CSS `background-image` gradient baked
into the banner SVG/PNG itself — don't rely on inline `<style>` blocks in the README, since
GitHub's markdown sanitizer strips `<style>` tags and most inline styles.

---

## Accessibility and Fallback Rules

These apply across all four sections above — carried over from
[Universal Readability](universal-readability.md), specialized for char-art/motion:

1. **Always caption decorative art in plain text.** A screen reader announces alt text for
   `<img>`-embedded GIFs/SVGs (write a real `alt`, not a filename), but reads a code-fenced ASCII
   banner character-by-character or symbol-by-symbol — genuinely painful. Immediately follow any
   ASCII banner or box diagram with one plain sentence stating what it shows, so a screen-reader
   user isn't stuck parsing `┌─┐│└┘`.
2. **Never encode unique information only in ASCII/motion.** If the box diagram is the only place
   a data flow is documented, someone using a reader — or someone who just skimmed past the
   animation — misses it entirely. Say it in prose too.
3. **Respect motion sensitivity.** GitHub's markdown doesn't support `prefers-reduced-motion`
   media queries on `<img>` GIFs, so the practical mitigation is: keep animated GIFs **short,
   low-contrast in motion (avoid strobing/flashing), and non-essential** — the README must be
   fully usable with every GIF mentally replaced by a still frame.
4. **Provide a static fallback for load failures.** For hosted SVG services (readme-typing-svg,
   capsule-render), if the service is unreachable the `<img>` just breaks — always keep the plain
   `# ProjectName` heading and tagline as real text above/below it, never inside the animated
   asset only.

---

## Quality Checklist for This Content Type

Add these to Step 7's validation pass whenever char-art/animation is used:

- [ ] Every ASCII/Unicode art block is in a fenced code block, ≤80 columns wide
- [ ] Every ASCII banner/diagram has a one-sentence plain-text caption immediately after it
- [ ] No information exists ONLY in ASCII art or ONLY in a GIF — it's also stated in prose
- [ ] All committed GIFs are under 5MB (ideally under 2MB) and were run through `gifsicle -O3`
- [ ] Terminal-recording GIFs have a checked-in source script (`.tape`/`.cast`), not a one-off
      screen recording — so they're regenerable when output changes
- [ ] SVG animations use SMIL/CSS only — no `<script>` (GitHub strips it silently)
- [ ] Glitch/Matrix/CRT effects are confined to decorative headers/footers, never load-bearing text
- [ ] Total motion budget respected: this counts against the same 2-3 GIF slots as any other
      animated element in the Visual Budget Rule — don't stack ASCII art + terminal GIF +
      typing SVG + Matrix rain all in one README
