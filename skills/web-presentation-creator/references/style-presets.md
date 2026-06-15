# Aesthetic Style Presets

This reference documents five distinct aesthetic presets inspired by industry leaders. Use these presets to establish the color palette, typography, and core visual identity of the landing page.

---

## 1. Cinematic Dark (Inspired by Apple / DJI)

This style is designed to make consumer hardware and high-res photography pop. It relies on pure black backgrounds, high-contrast typography, and cinematic lighting.

### Core Tokens
*   **Background:** `#000000` (Pure Black) or `#1a1a1a` (Near Black)
*   **Card Backgrounds:** `#1d1d1f` (Dark Gray with subtle border/glow)
*   **Text (Primary):** `#f5f5f7` (Off-White)
*   **Text (Secondary):** `#86868b` (Medium Gray)
*   **Accent (Performance):** `#30d158` (Apple Green) or `#FF4500` (DJI Red)
*   **Accent (CTA):** `#0071e3` (Apple Blue)

### Typography
*   **Headlines:** SF Pro Display (or Inter/Roboto fallback), extremely bold, tight letter-spacing (`-0.02em`).
*   **Body:** SF Pro Text (or Inter/Roboto fallback), light to regular weight, relaxed line-height (`1.5`).
*   **Gradient Text:** Use for hero headlines to create a metallic or glowing effect:
    ```css
    .gradient-text {
      background: linear-gradient(135deg, #fff, #86868b);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    ```

### Signature Elements
*   **Bento Grids:** Asymmetric grids (e.g., 2x3) with rounded corners (`border-radius: 18px`).
*   **Scrollytelling:** Heavy reliance on scroll-driven product reveals and large number count-ups.

---

## 2. Bright Editorial (Inspired by Glossier)

This style is clean, friendly, and e-commerce focused. It uses white space heavily, lifestyle photography, and conversational microcopy.

### Core Tokens
*   **Background:** `#ffffff` (Pure White)
*   **Text (Primary):** `#000000` (Pure Black)
*   **Text (Secondary):** `#4a4a4a` (Dark Gray)
*   **Accent (Sale/Urgency):** `#FF4500` (Bright Orange/Red)
*   **Accent (Brand):** `#FCE4EC` (Soft Pink)

### Typography
*   **Headlines:** Bold sans-serif, often all-caps for promotional banners (`letter-spacing: 0.05em`).
*   **Body:** Clean sans-serif, medium weight.
*   **Monospace:** Used for labels, badges, or "SALE" text to create a utilitarian feel.

### Signature Elements
*   **Frictionless Commerce:** Inline color swatches on product cards.
*   **Badge System:** Circular, stamp-like badges for "Top Picks" or "Best Sellers."
*   **Minimal Chrome:** Let the lifestyle photography do the heavy lifting; avoid complex backgrounds.

---

## 3. Web3 Tech (Inspired by ChainGPT Labs)

This style is futuristic, technical, and highly interactive. It features light backgrounds with striking neon accents and complex loading sequences.

### Core Tokens
*   **Background:** `#f5f5f5` (Light Gray) or `#ffffff` (White)
*   **Text (Primary):** `#000000` (Pure Black)
*   **Accent (Brand):** `#FF6B00` (Vibrant Orange)
*   **Card Backgrounds:** `#ffffff` with subtle borders (`border: 1px solid #e0e0e0`).

### Typography
*   **Headlines:** Custom monospace or blocky, geometric sans-serif (e.g., Space Grotesk, Syne).
*   **Body:** Clean sans-serif.

### Signature Elements
*   **Pixel Dissolve Preloader:** A complex loading sequence involving counters and dissolving grid elements.
*   **Scramble Text:** Text that flickers and scrambles through random characters before revealing the actual content.
*   **Infinite Marquees:** Horizontal scrolling bands for partner logos or tech stacks.

---

## 4. Brutalist Editorial (Inspired by The Outline)

This style rejects traditional grids and embraces vibrant, clashing colors, duotone photography, and unconventional layouts.

### Core Tokens
*   **Background (Animated):** A continuous morphing gradient or "lava lamp" effect using Coral (`#FF6B6B`), Hot Pink (`#FF1493`), Orange (`#FF4500`), and Purple (`#8B5CF6`).
*   **Card Backgrounds:** `#1a2332` (Dark Navy/Teal).
*   **Card Borders:** Neon Coral or Salmon (`border: 2px solid #FF6B6B`).
*   **Text (On Dark):** `#ffffff` (White).

### Typography
*   **Headlines:** A character-rich display serif (e.g., Playfair Display, spectral).
*   **Category Labels:** All-caps sans-serif, small size.
*   **Body:** Serif for excerpts to maintain an editorial feel.

### Signature Elements
*   **Duotone Filters:** Apply CSS filters or blend modes to all photography to unify diverse images.
*   **Emoji/Sticker Illustrations:** Use floating, asymmetric emoji or simple illustrations instead of complex vector graphics.
*   **Path-Based Scrolling:** Unconventional scroll mechanics (often requiring custom JS/Web Components).
