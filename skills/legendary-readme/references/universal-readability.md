# Universal Readability

> "If your grandmother and a 15-year-old can't both follow it, it's not clear. It's just familiar to you."

This is the toolkit for **Step 5: Make It Universally Readable** — the mechanics, vocabulary
rules, and structural habits that let a README work for a teenager discovering code for the
first time and an 80-year-old engineer who has debugged mainframes. Plain language is not
dumbed-down language. It's efficient language: every sentence spends the reader's attention on
the idea, not on decoding the sentence itself.

This file governs *how sentences and paragraphs are built*. For humor and personality layered on
top of that plain-language base, see [Tone and Voice](tone-and-voice.md). For which sections a
README needs in the first place, see [Sections Encyclopedia](sections-encyclopedia.md).

---

## 1. Sentence and Paragraph Mechanics

| Rule | Target | Why |
| :--- | :--- | :--- |
| Sentence length | ~20 words average, hard cap ~30 | Beyond that, working memory drops the subject before it reaches the verb |
| Paragraph length | 3-4 sentences max | A wall of text signals "skip me" before it signals "read me" |
| Ideas per sentence | One | Two ideas joined by "which" or "and" means the reader has to hold both in the air |
| Voice | Active over passive | Active names *who does what* — passive hides the actor and adds words |
| Nouns | Concrete over abstract | "The server" beats "the underlying infrastructure component" |

**Active vs. passive, in practice:**

- Passive: "The configuration file is read by the application on startup."
- Active: "The app reads the config file on startup."

The active version is shorter, names the actor first, and matches how someone would say it out
loud — which is the real test. If it sounds like a memo, rewrite it like a sentence you'd say to
a friend.

### Before/after: de-jargoning a real sentence

> **Before:** "Upon instantiation, the middleware layer performs idempotent validation of the
> incoming payload prior to delegating execution to the downstream handler, thereby mitigating
> the risk of duplicate side effects in the event of client-side retry logic."
>
> **After:** "Before handling a request, the middleware checks it once. If the same request
> comes in twice — say, because the client retried after a timeout — the second one is ignored.
> This stops the same action from happening twice by accident."

What changed and why it matters:

- **One idea per sentence.** The before-sentence packs four ideas (timing, validation,
  delegation, risk mitigation) into one 40-word clause. The after-version gives each idea its
  own sentence.
- **Concrete nouns replace abstractions.** "The middleware layer" → "the middleware." "The
  incoming payload" → "a request." "Downstream handler" is dropped entirely — it wasn't load-
  bearing for the reader's understanding.
- **The technical term (idempotent) is explained, not deleted.** Plain language doesn't mean
  removing precision — it means earning the right to use the term by explaining it first (see
  Section 2).
- **Active voice throughout.** "Is performed by," "is mitigated" → "checks," "is ignored,"
  "stops."

---

## 2. Vocabulary Tiers

Every technical word is a trade: it's precise and fast for someone who already knows it, and a
wall for someone who doesn't. The fix isn't to avoid technical words — it's to pay the definition
cost exactly once.

**The rule:** define a technical term in plain language the *first* time it appears, then use it
freely for the rest of the document. Don't re-explain it every time (that insults the reader who
got it the first time) and don't use it cold (that loses the reader who didn't).

### The glossary-inline pattern

Define the term inline, right where it first appears, in this format — bold the term, em-dash,
one plain-language sentence:

```markdown
The API is **idempotent** — running it twice does the same thing as running it once.
```

More examples of the same pattern:

```markdown
This runs as a **daemon** — a background process that keeps running after you close the terminal.

Requests go through a **rate limiter** — a bouncer that only lets a certain number of requests
through per minute, so one user can't accidentally take down the whole system.

State is stored in a **key-value store** — think of it like a giant dictionary: you give it a
word (the key) and it gives you back the definition (the value).
```

**Rules:**
- Define on **first use only**. If "idempotent" appears again in the Configuration section, just
  use it — the reader already has the definition, and repeating it reads as condescending.
- Keep the definition to **one sentence**. If it needs two, the term probably deserves its own
  subsection instead of an inline aside.
- Prefer a **common word over a technical word** whenever they mean the same thing to the reader
  who matters. "Use" beats "utilize." "Start" beats "instantiate." "Delete" beats "deprecate and
  remove." Save the technical word for when it's genuinely more precise, not when it just sounds
  more impressive.
- If a term is used more than 3-4 times across a long README, consider a short glossary section
  or table near the top instead of hunting for its first-use location.

---

## 3. The Analogy Toolkit

A good technical analogy borrows understanding the reader already has and lends it to a concept
they don't. A bad one tries to explain the whole system at once and collapses under its own
weight.

**How to build one:**

1. **Pick an everyday object or experience** the reader has almost certainly touched — a
   restaurant, a mailbox, a bouncer at a club, a library, traffic. Avoid anything niche to one
   culture, age group, or hobby (see Section 8).
2. **Map exactly ONE property at a time.** Say what the everyday thing and the technical thing
   share, and stop there before moving to the next mapped property.
3. **Cap it at 2-3 mapped properties total.** Past that, the analogy has to bend to cover edge
   cases it was never built for, and the reader spends more effort reconciling the metaphor than
   they would have spent just reading the technical explanation directly. When you notice
   yourself writing "but unlike a real X, this Y actually..." — stop. That's the collapse point.

### Ready analogies for common concepts

| Concept | Analogy | Mapped properties (stop here) |
| :--- | :--- | :--- |
| **Caching** | "A cache is like keeping snacks in your desk drawer instead of walking to the kitchen every time you're hungry. Faster, but the snacks can go stale." | (1) faster access, (2) can become outdated |
| **Rate limiting** | "A rate limiter is a bouncer at a club door — only lets a certain number of people in per minute, no matter how big the crowd outside gets." | (1) caps throughput, (2) protects what's behind it |
| **Webhooks** | "A webhook is like giving a restaurant your phone number instead of sitting by the door waiting for your table — they call you the moment it's ready." | (1) event-driven, (2) no need to keep checking |
| **Message queues** | "A message queue is like a to-do list on a sticky note pad — tasks pile up in order, and a worker peels one off at a time instead of everything happening at once." | (1) ordering, (2) decouples sender from processor |
| **Idempotency** | "Idempotent is like pressing an elevator button that's already lit — pressing it again doesn't call two elevators." | (1) repeat-safe, (2) same result every time |
| **Eventual consistency** | "Eventual consistency is like a group text — everyone gets the message, but not at exactly the same second. Give it a moment and everyone's screen matches." | (1) temporary disagreement, (2) converges over time |

Use these as starting points, not copy-paste text — the best analogy is tuned to the specific
project's theme or domain (see [Theme Engine](theme-engine.md) if the README has one). A backup
tool might reach for "insurance," a queue-based system might reach for "a deli counter number."

---

## 4. Reading Level Targets

You don't need a Flesch-Kincaid calculator to hit a good reading level — three habits get you
there without any tooling:

- **Short words over long ones.** "Use" not "utilize," "help" not "facilitate," "show" not
  "demonstrate." If a shorter word means the same thing, it's not less professional — it's more
  efficient.
- **Short sentences over long ones.** See Section 1's 20-word average.
- **No nested clauses.** A sentence with a clause inside a clause inside a clause ("the function,
  which is called by the handler that processes the request once it's been validated, returns...")
  forces the reader to hold three open brackets in their head at once. Break it into separate
  sentences in the order things actually happen.

**Rule of thumb:** if you'd need a comma to explain it to your parent out loud, split it into two
sentences on the page. Spoken explanations naturally chunk into short bursts with pauses between
them — written technical prose should mimic that rhythm instead of fighting it with semicolons and
subordinate clauses.

```markdown
❌ The migration, which runs automatically on deploy unless disabled via the SKIP_MIGRATION flag,
   will lock the users table for the duration of the schema change.

✅ Migrations run automatically on deploy. They lock the users table while the schema changes.
   Set SKIP_MIGRATION=true to skip this.
```

---

## 5. Structuring for Skimmers

Almost nobody reads a README top to bottom on the first pass — they scan for the part that
answers their question, then read that part closely. Structure for that behavior:

- **A header every 2-3 paragraphs.** If a section runs longer than that with no subheading, a
  skimmer has already scrolled past it looking for a landmark.
- **Bold key terms sparingly.** Bold the 1-2 words per paragraph a skimmer needs to catch the gist
  from a glance. Bolding every other phrase defeats the purpose — it all becomes visual noise
  again.
- **Bullets over prose for 3+ items.** "It supports X, Y, and Z, along with W" buries a list
  inside a sentence. A bulleted list lets the eye jump straight down the left edge.
- **Answer before explanation — the inverted pyramid.** State the conclusion or instruction
  first, then the reasoning. "Run `npm install` first — it pulls in the build tools the next step
  needs" beats "Because the next step needs certain build tools, you should first run
  `npm install`."
- **One code example beats three paragraphs of description.** If a config option, API call, or
  CLI flag can be shown, show it — then add one sentence of prose, not the reverse.

```markdown
❌ To start the development server, you'll first want to make sure your dependencies are
   installed, and then you can run the start command, which will launch the server on the
   default port unless you've configured a different one in your environment file.

✅ Start the dev server:

   ```bash
   npm install && npm run dev
   ```

   This runs on port 3000 by default — override it with `PORT=4000 npm run dev`.
```

For the deeper mechanics of tables, diagrams, and structured data blocks, see
[Tables, Diagrams, and Workflows](tables-diagrams-workflows.md).

---

## 6. Accessibility Rules

These are non-negotiable, not stylistic preferences — they determine whether a screen-reader
user, a colorblind user, or a mobile reader can use the README at all.

| Rule | Do | Don't |
| :--- | :--- | :--- |
| **Alt text** | Write a real description: `![CLI showing three green checkmarks after a successful install](demo.png)` | Leave it blank, or use the filename: `![](demo.png)` |
| **Color meaning** | Pair every color badge with a text label: `🟢 Passing` `🔴 3 failing` | Rely on red/green alone — colorblind readers (~8% of men) can't distinguish them |
| **Heading hierarchy** | Nest strictly: `#` → `##` → `###`, no skipping | Jump from `#` to `###` because it "looked right" visually |
| **Tables** | Always include a header row, even for a 2-column table | Use a table with no header row — screen readers can't announce column meaning without one |
| **Directional language** | "Click the **Save** button" | "Click the button on the right" — layout shifts on mobile, and screen readers don't convey position |

**Why heading hierarchy matters beyond looks:** screen readers let users jump section-to-section
by heading level. A skipped level (`#` straight to `###`) breaks that navigation even though it
renders fine visually — the strict nesting rule exists for a reader who can't see the visual size
difference at all.

For char-art, ASCII diagrams, and animated-GIF-specific accessibility rules (captions, motion
sensitivity, fallback text), see the dedicated accessibility section in
[Char Art and Animation](char-art-and-animation.md) — those rules build directly on this section.

---

## 7. Writing for the 15-to-80 Range

These two readers need almost opposite things, and a Legendary README gives both of them what
they need without either one noticing the accommodation made for the other:

| Reader | Needs | Fails if... |
| :--- | :--- | :--- |
| **15-year-old, first time seeing this kind of project** | The *why* spelled out, zero assumed prior knowledge, permission to not already know things | Jargon appears with no definition; steps skip a "so-obvious-nobody-said-it" prerequisite |
| **80-year-old veteran engineer** | To not feel talked down to; technical precision preserved; jokes that respect their intelligence | Explanations over-simplify to the point of being *wrong*; tone is cutesy instead of confident |

**The reconciliation:** plain language and technical precision are not opposites — treating them
as opposites is what causes README writers to either drown beginners in jargon or condescend to
experts with baby talk. The fix is to explain the *why* plainly (which serves the beginner) while
keeping every technical claim accurate and every term properly named once defined (which serves
the expert). "Idempotent" is a fine word to use — right after the first sentence has taught it in
one clause. A veteran skims past the definition in half a second and loses nothing; a newcomer
reads it and gains a word.

**A useful test:** read the sentence back and ask "would an expert roll their eyes at this?" and
separately "would a beginner be lost?" If either answer is yes, it's not a plain-language problem
— it's a *precision* problem. Fix the content, not just the vocabulary.

---

## 8. Internationalization Awareness

A README written in English is still read by people for whom English is a second, third, or
fourth language, and by machine translators. Write so both groups land on the same meaning as a
native speaker would.

- **Avoid idioms that don't translate.** "Knock it out of the park," "hit the ground running,"
  "the whole shebang" — sports metaphors and regional slang either translate literally into
  nonsense or require cultural context the reader doesn't have. Say the plain thing instead:
  "get started immediately," "everything included."
- **Never make culturally-specific humor the ONLY carrier of key information.** A joke that only
  lands for readers from one country or generation is fine as flavor *on top of* a plain
  statement — it's not fine as the sole sentence conveying a setup step or a warning. If removing
  the joke would remove the information, the joke is in the wrong place.
- **Prefer explicit over implied.** "Click **Save**" beats "hit that button" — "that button" only
  works if the reader is looking at the exact same screen, in the exact same language, at the
  exact same layout width the writer had open. Name the actual label, in bold, every time.
- **Watch for false-friend words.** Words that look like an easy cognate in another language but
  mean something else entirely ("actual" in Spanish/Portuguese means "current," not "real") cause
  quiet misreadings that a spell-checker will never catch. When in doubt, pick the less clever,
  more literal word.

---

## Readability Audit

Run this against any README section before shipping it:

- [ ] Average sentence length is roughly 20 words; no sentence runs past ~30
- [ ] No paragraph runs longer than 3-4 sentences
- [ ] Each sentence carries one idea — no "which... and... that..." chains
- [ ] Active voice is the default; passive only where the actor genuinely doesn't matter
- [ ] Concrete nouns replace abstract ones wherever possible
- [ ] Every technical term is defined in plain language on its first use, then used freely
- [ ] Any analogy maps 2-3 properties max and doesn't need a "but unlike a real X..." caveat
- [ ] Headers appear at least every 2-3 paragraphs
- [ ] Lists of 3+ items are bullets, not buried in a sentence
- [ ] The answer/instruction comes before the explanation, not after
- [ ] Every image/GIF has real, descriptive alt text — never a filename
- [ ] Every color-coded badge or status also has a text label
- [ ] Heading levels are strictly nested with no skipped levels
- [ ] Every table has a header row
- [ ] No instruction relies on screen position ("on the right," "below") alone
- [ ] A total beginner and a veteran engineer could both read this section without wincing
- [ ] No idiom, sports metaphor, or region-specific joke carries information found nowhere else
- [ ] Every button/action reference uses the actual label in bold, not a vague pointer
