# Theme Engine

> "A theme isn't decoration. It's a promise that every part of this document was made by the same person, on purpose."

This is the system for turning a project's purpose into **one cohesive identity** — a matching
palette, an animated banner, a mascot, a voice, themed section names, fitting GIFs, and a
recurring catchphrase — instead of a README that bolts on a random badge here and a random meme
there. Use it before **Step 6: Add Visual Firepower** in the main workflow, whenever the user
wants a README that feels designed, fun, and memorable rather than merely correct.

A theme is a filter, not a costume. Every choice below still has to answer the Big Three (What/
Why/How) — see the main [SKILL.md](../SKILL.md) — the theme just decides *how* those answers look
and sound. If a joke, color, or GIF doesn't serve the metaphor, it doesn't go in.

The process is 5 steps:

1. **Extract the project DNA** — answer a short set of questions before touching a color
2. **Pick a theme archetype** — one of 8 named kits, chosen by fit, not by taste
3. **Generate the Theme Kit** — palette, banner, voice, mascot, section names, GIFs, catchphrase
4. **Choose funny GIFs that fit the theme** — humor rules so jokes stay diegetic
5. **Assemble and audit** — a consistency pass before shipping

For the palette-to-badge-to-diagram mechanics once a theme is chosen, see
[Visual Style System](visual-style-system.md). For how the theme's voice should actually read
sentence-by-sentence, see [Tone and Voice](tone-and-voice.md). For the char-art and animated-
banner techniques referenced throughout the kits below, see
[Char Art and Animation](char-art-and-animation.md). For a complete README built end-to-end from
the Guardian Fortress kit, see the template
[Themed Project Readme](../templates/themed-project-readme.md).

---

## Step 1: Extract the Project DNA

Answer these before picking an archetype. Skipping this step is how you end up with a Space
Mission theme bolted onto a boring internal CRUD tool because rockets are cool — fit beats taste
every time.

| Question | Why it matters | Example answer |
| :--- | :--- | :--- |
| **What does it do, in one verb?** | The theme has to visually *act out* this verb. | "Backs up." "Deploys." "Watches." "Reconciles." |
| **Who's it for?** | A theme for solo indie-hacker CLIs reads differently than one for an enterprise platform team. | "Solo devs running side projects." |
| **What's the best everyday metaphor for what it does?** | This is the seed of everything downstream — mascot, voice, section names all grow from it. | A guardian, a rocket ship, a workshop, a lab, a garden. |
| **What emotional register fits?** | Serious infra tools tolerate less silliness than playful dev tools; get this wrong and the theme reads as unserious about a serious job. | "Confident and protective, not goofy." |
| **Is there a natural mascot already implied by the name/domain?** | A project literally named `sentinel` or `owl-logger` has already half-picked its mascot — don't fight a gift. | "Name is `vaultkeeper` → the mascot is obviously already a keeper/guardian." |

Write down one-line answers to all five before moving to Step 2. If two archetypes both seem
plausible, the **emotional register** answer is usually the tiebreaker — it separates, e.g.,
Guardian Fortress (serious protection) from Neon Hacker (edgy, offense-flavored security).

---

## Step 2: Pick a Theme Archetype

Eight archetypes, chosen by what the project *does* and how it should *feel* — not by which one is
most fun to draw. Each maps to a recognizable category of project.

| Archetype | Fits when the project is... | Feels like |
| :--- | :--- | :--- |
| **Guardian Fortress** | Security, backup, auth, secrets management, disaster recovery | "Your files/secrets have a protector." Calm, sturdy, watchful. |
| **Space Mission** | Deployment, CI/CD, orchestration, release tooling | "Launch your code." Countdown energy, mission control precision. |
| **Retro Arcade** | Fun dev tools, CLIs, games, playful utilities | High score energy, pixel joy, "insert coin to continue." |
| **Cozy Workshop** | Maker tools, CLIs, local-first apps, hand-built utilities | Warm, tactile, "built at a workbench, not a boardroom." |
| **Mad Science Lab** | Experimental tools, research code, ML/AI projects | Chaotic-but-brilliant, bubbling beakers, "it's alive!" |
| **Nature Zen** | Observability, monitoring, minimalist/calm tools | Quiet confidence, growth metaphors, low-stimulation calm. |
| **Neon Hacker** | Security/pentest tools, hacker-flavored CLIs, offensive-security kits | Cyberpunk edge, terminal-green, "we're the ones who find the holes." |
| **Premium Studio** | Design systems, component libraries, paid SaaS SDKs | Polished, restrained, "we sweat the details so you don't have to." |

**Decision rule:** if the project's core verb is *protect/back up/secure-at-rest* → Guardian
Fortress. If it's *ship/deploy/launch* → Space Mission. If it's *explore/experiment/train* → Mad
Science Lab. If it's *observe/measure/stay calm under load* → Nature Zen. If it's *break in/find
weaknesses* → Neon Hacker. If it's *build/tinker/assemble locally* → Cozy Workshop. If it's *play/
delight* → Retro Arcade. If it's *sell/license/integrate as infrastructure for other people's
products* → Premium Studio.

If a project genuinely straddles two (e.g., a CLI that's both a security tool AND playful) — pick
the archetype that matches what happens when the tool **fails**, not when it succeeds. A security
tool that fails quietly and catastrophically wants Guardian Fortress's gravity, not Retro Arcade's
whimsy, even if the CLI has fun flourishes day-to-day.

---

## Step 3: Generate the Theme Kit

Each kit below is complete and ready to copy: palette, animated banner concept, font/voice,
mascot, at least 6 remapped section names, GIF concepts, and a catchphrase. Guardian Fortress is
worked in the most detail — it's the canonical example referenced elsewhere in this skill, and the
template README is built directly from it.

### Guardian Fortress

*Fits: security tools, backup systems, auth/secrets management, disaster recovery, anything where
the promise is "this protects something you can't afford to lose."*

**Palette**

| Role | Color | Hex |
| :--- | :--- | :--- |
| Primary | Fortress Stone | `#2B2D42` |
| Accent | Beacon Gold | `#FFD60A` |
| Secondary accent | Shield Blue | `#3A86FF` |
| Background (dark mode) | Midnight Rampart | `#14151F` |
| Background (light mode) | Parchment | `#F4F1EA` |

Beacon Gold is the "alert/highlight" color — use it exactly like a torch or watchtower light: for
CTAs, badges, and the one thing you want the eye to land on. Don't let it become a body-text
color, or the fortress loses its one bright point.

**Animated banner concept**

A dark stone-textured or deep-navy banner with the project name rendered in a solid, blocky,
slightly-serif or slab typeface — the visual opposite of "flimsy." Use
[capsule-render](https://github.com/kyechan99/capsule-render)'s `rect` type with
`color=2B2D42` and a subtle `animation=fadeIn`, or a hand-rolled SVG per
[Char Art and Animation](char-art-and-animation.md) with a single Beacon Gold accent line (like a
torch glow) animating with SMIL along the top edge. Avoid bouncy/waving banner types (`waving`,
`venom`) — motion should read as **watchful**, not playful. A slow pulse (2-3s cycle) on the
accent line is the ceiling for how much motion this theme wants.

**Font/voice**

Monospace or a blocky slab-serif for headings — something that reads as carved stone, not
handwriting. Voice: **calm, declarative, protective, quietly confident** — short sentences that
sound like a briefing from someone who has done this before and isn't worried. Never frantic,
never cutesy. Humor here is dry understatement ("the walls held"), not slapstick.

**Mascot**

A **stone gargoyle** (or, softer alternative, a **owl in a sentry post**) — visual trait: always
shown facing outward/on watch, never asleep, never looking at the reader. If the project name
already implies an animal (owl, hawk, hound), use that instead of the generic gargoyle — a named
mascot beats a generic one every time.

**Themed section names**

| Standard section | Themed name |
| :--- | :--- |
| Installation | Raising the Walls (Installation) |
| Quick Start | Manning the Gates (Quick Start) |
| Features | The Armory (Features) |
| Configuration | Fortifications (Configuration) |
| Contributing | Join the Garrison (Contributing) |
| FAQ / Troubleshooting | When the Alarm Sounds (Troubleshooting) |
| Roadmap | The Watch Ahead (Roadmap) |
| Credits/Contributors | The Round Table (Credits) |

**GIF concepts**

1. A drawbridge/gate slamming shut, timed to a successful `npm install` or setup command — "access
   granted, gate secured."
2. A castle torch/beacon flaring brighter, used right where the README shows a security scan or
   audit passing — reinforces "the watchtower saw something and it's fine."
3. A stone golem or gargoyle giving a slow nod, used as the closing GIF right before the license/
   footer — a silent "we've got this."

**Catchphrase**

> "Your files have a guardian."

---

### Space Mission

*Fits: deployment tools, CI/CD, orchestration, release/rollout tooling — anything whose job is to
get code from here to production.*

**Palette**

| Role | Color | Hex |
| :--- | :--- | :--- |
| Primary | Launchpad Black | `#0B0C10` |
| Accent | Ignition Orange | `#FF6B35` |
| Secondary accent | Mission Blue | `#1B98E0` |
| Background (dark) | Deep Space | `#05060A` |
| Background (light) | Cloud Deck | `#EAF2F8` |

**Animated banner concept**

Dark banner with a countdown or star-field feel — use capsule-render's `rect` with a starfield-
suggestive dark background and Ignition Orange text, or the `waving` type turned upside-down
(rocket exhaust trail) at the footer instead of the header. A typing-SVG headline (see
[Char Art and Animation](char-art-and-animation.md)) that types out `T-10... T-9... LAUNCH` before
settling on the tagline works well here — motion should feel like a countdown, not idle decoration.

**Font/voice**

Monospace, NASA-console feel. Voice: **precise, procedural, confident under pressure** — mission-
control phrasing ("all systems nominal," "go for launch"). Short imperative sentences. Humor is
dry radio-chatter understatement, not slapstick.

**Mascot**

A **small rocket ship** or **astronaut** figure, visual trait: always mid-launch or floating with
a tether, never grounded/static — motion implied even in a still mascot.

**Themed section names**

| Standard section | Themed name |
| :--- | :--- |
| Installation | Pre-Flight Checklist (Installation) |
| Quick Start | Countdown (Quick Start) |
| Features | Payload (Features) |
| Configuration | Flight Plan (Configuration) |
| Contributing | Join Mission Control (Contributing) |
| FAQ / Troubleshooting | Houston, We Have a Problem (Troubleshooting) |
| Roadmap | Next Launch Window (Roadmap) |
| Credits/Contributors | The Crew (Credits) |

**GIF concepts**

1. A small rocket lifting off, timed right after the install/deploy command block — "liftoff"
   right where the tool actually launches something.
2. Mission-control operators clapping/high-fiving, used right after a successful deploy example —
   diegetic celebration, not a random reaction GIF.
3. A retro countdown clock ticking to zero, used as a loading/progress motif near CI status
   badges.

**Catchphrase**

> "Ship it like it's going to orbit."

---

### Retro Arcade

*Fits: fun dev tools, CLIs, games, playful utilities — projects where delight is a feature, not a
liability.*

**Palette**

| Role | Color | Hex |
| :--- | :--- | :--- |
| Primary | Cabinet Purple | `#6C1BA2` |
| Accent | High-Score Yellow | `#FFD500` |
| Secondary accent | Player-One Cyan | `#00E5FF` |
| Background (dark) | Arcade Black | `#0D0221` |
| Background (light) | Marquee White | `#FFF7EE` |

**Animated banner concept**

Pixel-font wordmark on a dark background with a scanline/CRT texture (see the CRT technique in
[Char Art and Animation](char-art-and-animation.md)) — or capsule-render's `rect` with a bold
pixel-adjacent font and High-Score Yellow text. A blinking "INSERT COIN" or "PRESS START" line
underneath, animated with a simple opacity blink SMIL animation, sells the arcade cabinet feeling
cheaply.

**Font/voice**

A pixel/8-bit display font for headings, monospace for body/code. Voice: **playful, competitive,
score-obsessed** — frame milestones as high scores, frame errors as "game over, try again." Puns
are welcome here more than in any other archetype.

**Mascot**

A small **8-bit pixel-art critter** (a ghost, a coin, a blocky robot) — visual trait: it should
have an idle "bounce" even as a static image (drawn mid-hop, not standing flat).

**Themed section names**

| Standard section | Themed name |
| :--- | :--- |
| Installation | Insert Coin (Installation) |
| Quick Start | Press Start (Quick Start) |
| Features | Power-Ups (Features) |
| Configuration | Settings Menu (Configuration) |
| Contributing | Join the High-Score Table (Contributing) |
| FAQ / Troubleshooting | Game Over? Continue? (Troubleshooting) |
| Roadmap | Next Level (Roadmap) |
| Credits/Contributors | Credits (roll the actual arcade credits) |

**GIF concepts**

1. A pixel-art "LEVEL UP" flash, timed right after a feature that unlocks new capability (e.g. a
   plugin system) — level-up as literal feature-unlock.
2. A coin-flip/coin-collect animation next to the star/sponsor button — "insert a star to
   continue."
3. A "GAME OVER — CONTINUE? 9...8...7" countdown used playfully in the Troubleshooting section
   right before a fix, then a "CONTINUE" flash once resolved.

**Catchphrase**

> "High score: zero bugs. Beat it."

---

### Cozy Workshop

*Fits: maker tools, CLIs, local-first apps, hand-built utilities — projects that feel like they
came off someone's workbench, not a corporate roadmap.*

**Palette**

| Role | Color | Hex |
| :--- | :--- | :--- |
| Primary | Workbench Brown | `#6F4E37` |
| Accent | Warm Amber | `#E8A33D` |
| Secondary accent | Sawdust Cream | `#F1E4C3` |
| Background (dark) | Old Oak | `#2B211A` |
| Background (light) | Linen | `#FBF6EE` |

**Animated banner concept**

A warm, low-contrast banner — think string-lights-in-a-garage-workshop, not neon. A hand-drawn-
style wordmark (rounded, slightly imperfect font) works better than a crisp geometric one.
capsule-render's `rect` type with a soft `animation=fadeIn` and Warm Amber text is enough motion —
this theme should feel unhurried, so avoid fast/looping motion entirely.

**Font/voice**

Rounded, slightly hand-lettered feel for headings; monospace for code. Voice: **warm, unhurried,
first-person, a little self-deprecating** — like a maker explaining a project over coffee, not a
product team pitching a roadmap. Contractions and asides are welcome.

**Mascot**

A **wood-carved fox or owl figurine**, or a simple **toolbox with a face**, visual trait: slightly
worn/imperfect edges (this theme actively wants "handmade," not "polished").

**Themed section names**

| Standard section | Themed name |
| :--- | :--- |
| Installation | Setting Up the Bench (Installation) |
| Quick Start | First Cut (Quick Start) |
| Features | What's on the Shelf (Features) |
| Configuration | Adjusting the Tools (Configuration) |
| Contributing | Pull Up a Stool (Contributing) |
| FAQ / Troubleshooting | Splinters and Fixes (Troubleshooting) |
| Roadmap | Next Project on the Bench (Roadmap) |
| Credits/Contributors | Who Built This (Credits) |

**GIF concepts**

1. A stop-motion-style clip of hands assembling small wooden blocks, used near the "Features"
   section to imply "built piece by piece."
2. A kettle/mug of coffee steaming, used as a small aside near a long-running command ("this'll
   take a minute, go make tea").
3. A single string-light bulb flickering on, used right at the "Quick Start" section as a soft
   "and... we're on."

**Catchphrase**

> "Handmade, but it scales."

---

### Guardian Fortress vs. Mad Science Lab — a note on tone drift

Before continuing to the remaining four kits: Guardian Fortress and Mad Science Lab are the two
easiest to blur if the DNA extraction in Step 1 was rushed. A security-research tool that *finds*
vulnerabilities (offense) is Neon Hacker or Mad Science Lab; a tool that *prevents* or *contains*
them (defense) is Guardian Fortress. Re-check the DNA answers if a kit feels like it's fighting
the project.

### Mad Science Lab

*Fits: experimental tools, research code, ML/AI projects — anything where "it might explode, but
it's exciting" is an honest description.*

**Palette**

| Role | Color | Hex |
| :--- | :--- | :--- |
| Primary | Lab Coat White | `#F5F5F0` |
| Accent | Bubbling Green | `#39FF14` |
| Secondary accent | Beaker Purple | `#8338EC` |
| Background (dark) | Chalkboard Slate | `#1A1F1C` |
| Background (light) | Clipboard White | `#FAFAF7` |

**Animated banner concept**

A dark banner with a bubbling-liquid or spark-of-electricity motif — a simple animated SVG dot
rising through a "beaker" shape works (SMIL `<animate>` on `cy`, see
[Char Art and Animation](char-art-and-animation.md)), or capsule-render's `rect` with
Bubbling Green text and `animation=fadeIn`. A crackling-electricity glitch flicker on the project
name (used sparingly, one flicker on load, not looping) sells "it's alive" without becoming noisy.

**Font/voice**

Monospace with occasional "handwritten note in the margin" asides (small, italicized). Voice:
**excitable, curious, a little unhinged, but rigorous underneath** — lots of "what if we tried..."
energy, footnotes that read like lab notebook margin scrawl. Self-aware humor about things
breaking is on-theme here more than almost anywhere else.

**Mascot**

A **frazzled scientist figure** or a **small blob/creature mid-mutation**, visual trait: one eye
bigger than the other, or hair mid-explosion — controlled chaos, not tidy.

**Themed section names**

| Standard section | Themed name |
| :--- | :--- |
| Installation | Stocking the Lab (Installation) |
| Quick Start | First Experiment (Quick Start) |
| Features | What's Bubbling (Features) |
| Configuration | Calibration (Configuration) |
| Contributing | Join the Research Team (Contributing) |
| FAQ / Troubleshooting | When the Beaker Cracks (Troubleshooting) |
| Roadmap | Hypotheses Under Test (Roadmap) |
| Credits/Contributors | Lab Notebook Credits (Credits) |

**GIF concepts**

1. A beaker bubbling over, timed right at a benchmark/results table — "results are in, and they're
   good" played as a controlled overflow rather than a disaster.
2. A lightning-bolt "IT'S ALIVE" flash, used right after the first working example runs
   successfully.
3. A scientist scribbling furiously on a clipboard, used near the Roadmap/experimental-features
   section — "we're still testing this."

**Catchphrase**

> "Every bug is just data we didn't expect yet."

---

### Nature Zen

*Fits: observability, monitoring, minimalist tools — anything whose value proposition is calm,
clarity, and not being paged at 3am.*

**Palette**

| Role | Color | Hex |
| :--- | :--- | :--- |
| Primary | Moss Green | `#3F6B4F` |
| Accent | Morning Sun | `#F2C14E` |
| Secondary accent | River Blue | `#7BA7BC` |
| Background (dark) | Deep Forest | `#0F1B14` |
| Background (light) | Fog White | `#F6F5F0` |

**Animated banner concept**

Low-contrast, minimal-motion banner — a slow gradient fade (dawn-to-day color sweep) is the most
motion this theme should ever use. capsule-render's `rect` with `animation=fadeIn` and a long
duration reads as "breathing," not "loading." Avoid anything that pulses fast, blinks, or loops
under 3 seconds — the entire point of this theme is that nothing feels urgent.

**Font/voice**

Clean, rounded sans-serif feel for headings (even rendered in monospace in markdown, keep line
lengths short and airy); generous whitespace. Voice: **quiet, precise, reassuring** — short
declarative sentences, almost haiku-like restraint. Humor is a single wry aside, never a bit.

**Mascot**

A **small bird** (owl for night-watch/monitoring, sparrow for lightweight tools) perched, visual
trait: still and observant, never mid-action — stillness IS the trait.

**Themed section names**

| Standard section | Themed name |
| :--- | :--- |
| Installation | Planting the Seed (Installation) |
| Quick Start | First Bloom (Quick Start) |
| Features | What Grows Here (Features) |
| Configuration | Tending the Garden (Configuration) |
| Contributing | Join the Grove (Contributing) |
| FAQ / Troubleshooting | When a Leaf Wilts (Troubleshooting) |
| Roadmap | Next Season (Roadmap) |
| Credits/Contributors | Who Tends This Garden (Credits) |

**GIF concepts**

1. A time-lapse of a plant sprouting, used right at the "Quick Start" section as literal "watch
   it grow" for a first successful run.
2. A single leaf falling and landing gently, used in the Troubleshooting section for a resolved,
   low-severity issue — nothing dramatic, just "handled."
3. A slow sunrise gradient loop, used as a section-divider motif rather than a standalone gag —
   this theme prefers ambient over comedic GIFs.

**Catchphrase**

> "Calm is a feature."

---

### Neon Hacker

*Fits: security/pentest tools, offensive-security kits, hacker-flavored CLIs — projects with an
edge, built by and for people who find the holes.*

**Palette**

| Role | Color | Hex |
| :--- | :--- | :--- |
| Primary | Terminal Black | `#0A0A0A` |
| Accent | Matrix Green | `#00FF41` |
| Secondary accent | Hot Magenta | `#FF00C8` |
| Background (dark) | Void | `#000000` |
| Background (light) | (this theme has no real light mode — see note below) | `#101014` |

**Animated banner concept**

Terminal-green monospace wordmark on black, with a scanline/glitch flicker per
[Char Art and Animation](char-art-and-animation.md)'s Matrix/glitch section — a short (5-8s)
Matrix-rain GIF behind or above the header is the signature move here, or a typing-SVG headline
that types out a fake `whoami`/`nmap`-style command before resolving to the tagline. This is one
of the few themes where a genuinely animated, motion-forward banner is the *correct* choice, not
excess — but still cap it at one banner, per the Visual Budget Rule.

**Font/voice**

Monospace, terminal-green-on-black, no exceptions. Voice: **confident, terse, slightly
conspiratorial** — short lines, imperative mood, occasional 1337-speak used ironically rather than
sincerely. Never actually condescending to the reader — the edge is aesthetic, not gatekeeping.

**Mascot**

A **hooded silhouette** or a **glitching skull/circuit-board icon**, visual trait: rendered as
negative space/silhouette rather than a detailed illustration — the theme wants suggestion, not
detail.

**Themed section names**

| Standard section | Themed name |
| :--- | :--- |
| Installation | Gaining Access (Installation) |
| Quick Start | Root in 60 Seconds (Quick Start) |
| Features | Exploits Included (Features) |
| Configuration | Payload Config (Configuration) |
| Contributing | Join the Crew (Contributing) |
| FAQ / Troubleshooting | Debug or Die (Troubleshooting) |
| Roadmap | Next Target (Roadmap) |
| Credits/Contributors | Shoutouts (Credits) |

**GIF concepts**

1. A fast-scrolling terminal log (green text on black) that suddenly stops on `ACCESS GRANTED`,
   timed right after the install/auth example — diegetic payoff, not decoration.
2. A short Matrix-rain loop used once as a header/footer flourish (see banner concept above) —
   don't repeat it a second time elsewhere, one use is confident, two is a gimmick.
3. A glitch-flicker on a single word (e.g. "SECURE" flickering to "SECURED") right where a scan
   result turns green.

**Catchphrase**

> "We found the hole before they did."

*Note on light mode:* Neon Hacker is the one archetype that can legitimately skip a true light
palette — the aesthetic depends on black. If light-mode support is required, use a dark-gray
(`#101014`) background rather than a genuinely light one, and keep Matrix Green/Hot Magenta as the
only bright colors so the theme doesn't collapse into generic "dark UI."

---

### Premium Studio

*Fits: design systems, component libraries, paid SaaS SDKs — infrastructure sold or licensed to
other engineering teams, where trust and polish matter more than personality.*

**Palette**

| Role | Color | Hex |
| :--- | :--- | :--- |
| Primary | Studio Black | `#111113` |
| Accent | Signal Indigo | `#5B5BF5` |
| Secondary accent | Warm Graphite | `#8A8A93` |
| Background (dark) | Obsidian | `#08080A` |
| Background (light) | Studio White | `#FFFFFF` |

**Animated banner concept**

Restrained: a clean wordmark in a single accent color on a solid or very subtle gradient
background, with **one** understated motion — a slow fade-in or a thin accent line drawing itself
left-to-right (SMIL `<animate>` on a `<line>`'s `stroke-dashoffset`) is the ceiling. No bounce, no
particle effects, no glitch. capsule-render's `rect` type with `animation=fadeIn` and a slow
duration is the safe default. This theme signals quality through restraint — more motion reads as
less premium, not more.

**Font/voice**

Clean geometric sans feel for headings (again, rendered as clean monospace/plain text within
markdown constraints — the *impression* of a geometric sans, achieved via spacing and brevity
rather than an actual font swap); tight, confident, benefit-first copy. Voice: **precise,
respectful of the reader's time, zero filler** — every sentence earns its place. Humor is a single
dry aside at most per section, never a bit, never an emoji flourish.

**Mascot**

Often **no literal creature mascot** — if one is wanted, use an abstract geometric monogram/icon
(a single shape derived from the logo) rather than an animal or character. Visual trait: it should
work as a single-color silhouette at 16px (favicon-sized), since this theme's mascot usually
doubles as a brand mark.

**Themed section names**

| Standard section | Themed name |
| :--- | :--- |
| Installation | Setup (kept close to standard — see note below) |
| Quick Start | Get Started in Minutes |
| Features | What You Get |
| Configuration | Customization |
| Contributing | Building With Us |
| FAQ / Troubleshooting | Common Questions |
| Roadmap | What's Next |
| Credits/Contributors | Built By |

**GIF concepts**

1. A single UI component smoothly transitioning between two states (e.g., light/dark toggle, or a
   button's hover-to-pressed animation), sourced from the actual product — this theme's "GIF"
   budget is best spent on real product motion, not illustrated humor.
2. A terminal install command completing with a clean checkmark animation, no flourish beyond the
   checkmark itself.
3. If humor is wanted at all, keep it to one dry visual pun in the footer (e.g., a subtly
   perfect pixel-alignment joke) — this is the one theme where "no joke" is an entirely valid
   choice.

**Catchphrase**

> "Built like it's already in production."

*Note on section names:* Premium Studio is the one archetype that deliberately under-themes
section names — the audience (engineering teams evaluating a paid dependency) values fast
scanning over cleverness. Lean toward the standard word with light polish rather than a full
metaphor remap; "Setup" over "Raising the Walls"-style renames.

---

## Step 4: Choose Funny GIFs That Fit the Theme

**Rule: GIF humor must be diegetic to the theme.** A joke earns its place only if it makes sense
*inside the metaphor* — a Guardian Fortress README jokes about walls, gates, and watchtowers, not
about cats. A random meme dropped in "because it's funny" breaks the illusion that one person
designed this document on purpose, and it's the single fastest way a README goes from "legendary"
to "trying too hard."

**Rule: the GIF has to reinforce something the reader is actually doing at that point in the
doc.** Placement matters as much as content — a themed GIF next to unrelated content is still a
non-sequitur, just a prettier one.

| Project | GOOD themed choice | BAD random choice |
| :--- | :--- | :--- |
| A backup tool (Guardian Fortress) | A castle gate slamming shut, placed right after the "your backup completed" example — the gate closing = the vault sealing. | A generic "This is fine" dog-in-burning-room meme — funny in isolation, has nothing to do with backups or guardianship. |
| A CI/CD tool (Space Mission) | A rocket launch clip placed right after the deploy command succeeds — liftoff = deploy. | A random "distracted boyfriend" meme captioned with framework names — off-theme and also overused to the point of cliché. |

If a GIF idea can be described without mentioning the project's metaphor at all ("it's just a
funny cat gif"), it fails this test — cut it or replace it with a themed alternative from the
kit's GIF concepts list above.

---

## Step 5: Assemble and Audit

Once the kit is chosen and applied, run the **Theme Consistency Audit** before shipping. This
folds into the main skill's Step 7 validation pass whenever a theme is in play.

- [ ] **Shared palette** — banner, badges, mascot artwork, and any diagrams all pull from the same
      hex values in the kit's palette table (not "close enough" colors picked by eye)
- [ ] **Catchphrase appears at least twice** — once near the top (right after the banner/tagline)
      and once at the close (footer, final section, or right above the license) — a catchphrase
      used only once is a tagline, not a motif
- [ ] **Themed section names stay discoverable** — every remapped heading keeps the standard word
      in parentheses (e.g. `## Raising the Walls (Installation)`), so Ctrl+F, a generated Table of
      Contents, and screen readers can still resolve it to the section a reader is actually
      looking for
- [ ] **No section drops the theme** — scan every heading in order; if one section reverts to a
      bare, unthemed name while its neighbors are themed, that's a tell the README was finished in
      a hurry — either theme it or, for Premium Studio-style light theming, confirm the
      under-theming was a deliberate choice per that kit's own rule, not an oversight
- [ ] **Mascot appears at least once, ideally twice** — once near the top (banner or intro) and
      once at the close (footer) — a mascot introduced and never seen again reads as unfinished
- [ ] **GIFs pass the diegetic test from Step 4** — every GIF's humor is explainable using only the
      project's metaphor, with no "it's just funny" exceptions
- [ ] **Voice stays consistent** — spot-check 3-4 sections; if one reads noticeably more formal or
      more chaotic than the others, the [Tone and Voice](tone-and-voice.md) guide's voice
      description for this kit wasn't applied consistently
- [ ] **Light/dark mode both honor the palette** — check the kit's light-mode background actually
      gets used somewhere (badges, `<picture>` fallback images), not just the dark one
- [ ] **The Big Three still survive the theme** — What/Why/How are still answerable in the first
      viewport even with themed language; if a reader has to decode the metaphor before
      understanding what the project does, the theme has overridden clarity — clarity always wins
