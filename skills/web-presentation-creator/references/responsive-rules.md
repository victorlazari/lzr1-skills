# Responsive & Performance Rules

Premium landing pages must feel like native applications across all devices. This requires strict adherence to responsive design principles and Core Web Vitals optimization.

---

## 1. Responsive Layout Rules

Do not rely solely on arbitrary breakpoints. Use fluid typography and CSS Grid/Flexbox to ensure the layout adapts continuously.

### Fluid Typography
Use `clamp()` for responsive typography to avoid abrupt jumps at media queries.

```css
:root {
  /* Scales smoothly from 2.5rem on mobile to 5rem on desktop */
  --font-size-hero: clamp(2.5rem, 5vw + 1rem, 5rem);
  
  /* Scales from 1rem to 1.25rem */
  --font-size-body: clamp(1rem, 1vw + 0.75rem, 1.25rem);
}

h1 {
  font-size: var(--font-size-hero);
}
```

### Grid Adaptation
For Bento grids (like DJI/Apple feature cards), shift from multi-column to single-column on mobile.

```css
.bento-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

/* Specific overrides for complex asymmetric grids */
@media (max-width: 768px) {
  .bento-grid.asymmetric {
    grid-template-columns: 1fr; /* Stack everything on mobile */
  }
}
```

### Touch Targets
Ensure all interactive elements (tabs, buttons, links) have a minimum touch target size of 44x44px for mobile users.

```css
.scenario-tab, .cta-button {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 24px; /* Ensure padding makes up the size */
}
```

---

## 2. Performance & CLS Prevention

Cumulative Layout Shift (CLS) destroys the premium feel. The page must not jump as assets load.

### Aspect Ratio Locking
Every image and video container MUST have an explicit aspect ratio.

```css
.media-wrapper {
  width: 100%;
  aspect-ratio: 16 / 9; /* Or 4/3, 1/1 depending on the asset */
  background-color: #1a1a1a; /* Placeholder color while loading */
  overflow: hidden;
}

.media-wrapper img, 
.media-wrapper video, 
.media-wrapper iframe {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

### Content Visibility
For extremely long scrollytelling pages (like Apple/DJI), tell the browser to skip rendering off-screen sections until they are needed.

```css
.scroll-section {
  content-visibility: auto;
  contain-intrinsic-size: 1000px; /* Estimate of the section's height */
}
```

### Hardware Acceleration
Force the browser to use the GPU for elements that will be animated (like scrollytelling layers).

```css
.animated-layer {
  will-change: transform, opacity;
  transform: translateZ(0); /* Legacy GPU trigger, still useful */
}
```

---

## 3. Media Queries & Breakpoints

Standardize breakpoints across the project.

```css
/* Mobile First Approach */

/* Tablet (Portrait) */
@media (min-width: 768px) {
  .hero-content {
    width: 80%;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .hero-content {
    width: 60%;
  }
}

/* Ultra-Wide */
@media (min-width: 1440px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
}

/* Reduced Motion Preference */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
