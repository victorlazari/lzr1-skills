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
