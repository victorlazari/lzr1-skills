# Media Handling & Scrollytelling

This reference outlines how to handle user-provided images, local videos, and YouTube embeds within a premium landing page architecture, focusing on scroll-driven transitions.

---

## 1. Handling User-Provided Media

When building a page, the user may provide specific assets.

### Local Videos (up to 10s)
If the user provides a short MP4/WebM video, it is best used as a silent, autoplaying background or a scroll-triggered reveal.

**Implementation:**
```html
<div class="video-wrapper">
  <video 
    src="assets/user-video.mp4" 
    autoplay 
    loop 
    muted 
    playsinline 
    class="bg-video">
  </video>
</div>
```
*Note: `muted` and `playsinline` are strictly required for autoplay to work on iOS Safari.*

### YouTube Embeds
If the user provides a YouTube link, use an iframe, but wrap it in an aspect-ratio container to prevent CLS.

**Implementation:**
```html
<div class="youtube-wrapper">
  <iframe 
    src="https://www.youtube.com/embed/VIDEO_ID?autoplay=0&controls=1&rel=0" 
    frameborder="0" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen>
  </iframe>
</div>
```
```css
.youtube-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  overflow: hidden;
}
.youtube-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
```

---

## 2. Scroll-Driven Fade Transitions (Scrollytelling)

This is the core mechanic for Apple/DJI style product reveals. A tall track allows the user to scroll while content remains sticky in the viewport, fading in and out based on scroll progress.

### HTML Structure

```html
<!-- The Track: Determines how long the scroll lasts -->
<div class="scroll-track" style="height: 400vh;">
  
  <!-- The Viewport: Sticks to the screen -->
  <div class="sticky-viewport">
    
    <!-- Background Media -->
    <div class="media-layer" data-fade-in="0" data-fade-out="0.9">
      <img src="assets/product-bg.jpg" alt="Product">
    </div>

    <!-- Text Layer 1 -->
    <div class="text-layer" data-fade-in="0.1" data-fade-out="0.4">
      <h2>Precision Engineering</h2>
      <p>Every detail considered.</p>
    </div>

    <!-- Text Layer 2 -->
    <div class="text-layer" data-fade-in="0.5" data-fade-out="0.8">
      <h2>Unmatched Performance</h2>
      <p>The fastest chip ever built.</p>
    </div>

  </div>
</div>
```

### CSS Structure

```css
.scroll-track {
  position: relative;
  width: 100%;
  /* Height is set inline based on how long the sequence should be */
}

.sticky-viewport {
  position: sticky;
  top: 0;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  background-color: #000;
}

.media-layer, .text-layer {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0; /* Hidden by default */
  will-change: opacity, transform;
}

.media-layer img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

### JavaScript Controller (No external libraries required)

```javascript
class ScrollytellingFader {
  constructor() {
    this.tracks = document.querySelectorAll('.scroll-track');
    window.addEventListener('scroll', () => this.onScroll(), { passive: true });
    this.onScroll(); // Init
  }

  onScroll() {
    const viewH = window.innerHeight;

    this.tracks.forEach(track => {
      const rect = track.getBoundingClientRect();
      const trackH = track.offsetHeight;
      
      // Calculate progress from 0 to 1
      // 0 = top of track hits bottom of viewport
      // 1 = bottom of track hits top of viewport
      let progress = (-rect.top) / (trackH - viewH);
      progress = Math.max(0, Math.min(1, progress));

      const layers = track.querySelectorAll('[data-fade-in]');
      
      layers.forEach(layer => {
        const fadeInStart = parseFloat(layer.dataset.fadeIn);
        const fadeOutEnd = parseFloat(layer.dataset.fadeOut);
        
        // Define transition zones (e.g., 10% of the total duration to fade in)
        const transitionDuration = 0.1; 
        const fadeInEnd = fadeInStart + transitionDuration;
        const fadeOutStart = fadeOutEnd - transitionDuration;

        let opacity = 0;
        let translateY = 20; // Start slightly lower

        if (progress >= fadeInStart && progress <= fadeOutEnd) {
          if (progress < fadeInEnd) {
            // Fading in
            const localProgress = (progress - fadeInStart) / transitionDuration;
            opacity = localProgress;
            translateY = 20 * (1 - localProgress);
          } else if (progress > fadeOutStart) {
            // Fading out
            const localProgress = (progress - fadeOutStart) / transitionDuration;
            opacity = 1 - localProgress;
            translateY = -20 * localProgress; // Drift up as it fades out
          } else {
            // Fully visible
            opacity = 1;
            translateY = 0;
          }
        }

        layer.style.opacity = opacity;
        layer.style.transform = `translateY(${translateY}px)`;
      });
    });
  }
}

document.addEventListener('DOMContentLoaded', () => new ScrollytellingFader());
```
