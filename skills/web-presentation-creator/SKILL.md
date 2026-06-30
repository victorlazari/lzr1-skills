---
name: premium-landing-page-architect
description: "Design and build premium, high-performance landing pages. Use for: creating cinematic scrollytelling experiences, integrating GSAP animations (preloader, scramble text, fade transitions), handling complex media (images, HTML5 video, YouTube embeds), and generating complete HTML or ZIP packages with assets."
license: Complete terms in LICENSE.txt
---

# Premium Landing Page Architect Skill

This skill enables Manus to design, architect, and build premium landing pages inspired by industry leaders (Apple, DJI, ChainGPT Labs, The Outline, Glossier). It provides a complete workflow for generating production-ready HTML, CSS, and JavaScript, with a strong emphasis on scrollytelling, high-performance media handling, and complex animations.

---

## Core Capabilities & Workflows

When activated, this skill provides specialized workflows across three main domains:

1.  **Cinematic Scrollytelling**: Building scroll-driven sequences where the user's scroll position controls video playback, canvas image sequences, or opacity fades.
2.  **Advanced Animation & Preloaders**: Implementing GSAP-powered loading sequences (like pixel dissolves), text scramble reveals, and hardware-accelerated transitions.
3.  **Media & Asset Management**: Handling user-provided images, local videos (up to 10s), and YouTube embeds, and packaging everything into a deliverable ZIP file.

---

## Step-by-Step Implementation Guide

Follow this systematic workflow when a user requests a premium landing page:

### Step 1: Requirements Gathering & Media Assessment
Before writing any code, determine the scope and media requirements.
*   **Action**: Ask the user if they have specific images (PNG/JPG/GIF) or videos (MP4/WebM, up to 10s) they want to include.
*   **Action**: Ask if they want to embed any YouTube links.
*   **Action**: Determine the preferred aesthetic (e.g., Apple's dark cinematic, Glossier's bright editorial, ChainGPT's tech/Web3).
*   **Reference**: See [references/style-presets.md](references/style-presets.md) for available aesthetic themes.

### Step 2: Establish the Architectural Model
Set up the HTML/CSS foundation for high performance.
*   **Action**: Use semantic HTML5 with a modern CSS Grid/Flexbox layout.
*   **Action**: Implement `content-visibility: auto` and `contain-intrinsic-size` on off-screen sections.
*   **Action**: Ensure all media wrappers have an explicit `aspect-ratio` to eliminate Cumulative Layout Shift (CLS).
*   **Reference**: See [references/responsive-rules.md](references/responsive-rules.md) for desktop-to-mobile scaling and breakpoints.

### Step 3: Implement the Animation Engine (GSAP)
Integrate GreenSock Animation Platform (GSAP) for all complex timelines.
*   **Action**: Include GSAP core, ScrollTrigger, and Lenis (for smooth scrolling).
*   **Action**: If requested, implement the "Pixel Dissolve" preloader (ChainGPT style) or "Scramble Text" reveal.
*   **Reference**: See [references/animation-library.md](references/animation-library.md) for the exact JavaScript implementations of these effects.

### Step 4: Build Scrollytelling & Media Transitions
Create immersive scroll-driven sequences.
*   **Action**: Build tall vertical track containers (`height: calc(...)`) holding sticky viewport wrappers (`position: sticky; top: 0; height: 100vh`).
*   **Action**: Implement scroll-driven opacity fades for text and images.
*   **Reference**: See [references/media-handling.md](references/media-handling.md) for handling local video, YouTube embeds, and image layers.

### Step 5: Package and Deliver
Deliver the final product in the correct format.
*   **Action**: If the project uses *only* external URLs or inline SVGs, deliver a single self-contained `index.html` file.
*   **Action**: If the user provided local images or videos, or if the project requires a complex folder structure, create a directory, move all assets into it, and deliver a `.zip` file containing the complete project (HTML, CSS, JS, and `/assets`).
*   **Action**: Use the `shell` tool to `zip -r project.zip project_folder/` and use the `message` tool to deliver it.

---

## Detailed References

For deep-dive technical and design patterns, consult the complementary reference guides bundled with this skill:

*   **Aesthetic Themes**: Refer to [references/style-presets.md](references/style-presets.md) for Apple, DJI, Glossier, Outline, and ChainGPT visual patterns.
*   **Animation & Preloaders**: Refer to [references/animation-library.md](references/animation-library.md) for GSAP implementations, Lenis smooth scroll, and text scrambling.
*   **Media & Scrollytelling**: Refer to [references/media-handling.md](references/media-handling.md) for video backgrounds, YouTube integration, and fade transitions.
*   **Responsive & Performance Rules**: Refer to [references/responsive-rules.md](references/responsive-rules.md) for mobile optimization and CLS prevention.

---

## Adversarial Verification Panel

For each significant design and implementation recommendation produced by the parallel sub-agents:

1. Spawn **3 independent Refuter Agents** per finding, each with:
   - The finding in full
   - Instruction: *"Assume this finding is wrong. Find the strongest argument against it."*
   - Default stance: `refuted=true` if evidence is insufficient or ambiguous
2. A finding is **confirmed** only if ≥2 refuters fail to refute it
3. A finding is **discarded** if ≥2 refuters succeed
4. When a confirmed finding had 1 successful refuter, include the dissenting argument in the output with a `CONTESTED` label

> This prevents plausible-but-wrong design and implementation recommendations from reaching the final output. The 3-vote panel eliminates single-point hallucination without requiring unanimity.

## Cross-System Consistency Validator

After all parallel agents (Cinematic Scrollytelling, Advanced Animation & Preloaders, Media & Asset Management) complete, but **before** synthesis:

Run one **Consistency Validator Agent** with all parallel outputs that:
- Flags any pair of recommendations that logically contradict each other
  *(example: the Advanced Animation & Preloaders agent recommends a GSAP pixel dissolve preloader with heavy JS timelines, while the Cinematic Scrollytelling agent recommends `content-visibility: auto` and minimal scripting for maximum scroll performance — these can conflict when both are applied simultaneously)*
- Notes where one agent's output is a prerequisite for another agent's recommendation
- Passes contradictions to the Synthesis Agent as `MUST_RESOLVE` items
- Passes missing prerequisites as `SEQUENCING_REQUIRED` items

## Synthesis Agent (Upgraded)

The synthesis step actively resolves rather than aggregates:

1. **`MUST_RESOLVE` contradictions**: Pick the better recommendation, annotate the reasoning, preserve the dissenting view as a footnote
2. **`SEQUENCING_REQUIRED` items**: Re-order the unified packaged `index.html` or `.zip` project so prerequisites appear before the steps that depend on them
3. **Confidence calibration**: Label each finding `HIGH` / `MEDIUM` / `LOW` confidence based on refuter panel outcomes
4. **Gap analysis**: Note any analysis dimension not covered by any of the parallel agents — these are blind spots, not confirmed negatives
