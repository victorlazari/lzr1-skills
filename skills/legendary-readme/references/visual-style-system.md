# Visual Style System: GIFs, Banners, Images, and Design Recipes

> "Design is not just what it looks like. Design is how it works." — Steve Jobs
> (But also... it should look absolutely stunning.)

This reference is your complete toolkit for making README files visually gorgeous, stylish, and memorable. It covers curated GIF sources, banner generators, color palettes, design systems, and ready-to-paste visual recipes.

---

## Table of Contents

- [Design Philosophy](#design-philosophy)
- [The Style Selector](#the-style-selector)
- [Color Palettes and Gradient Systems](#color-palettes-and-gradient-systems)
- [Banner Recipes (Copy-Paste Ready)](#banner-recipes-copy-paste-ready)
- [GIF Libraries and Animated Assets](#gif-libraries-and-animated-assets)
- [Dynamic Widgets and Stats Cards](#dynamic-widgets-and-stats-cards)
- [Illustration and Icon Sources](#illustration-and-icon-sources)
- [Complete Visual Layout Recipes](#complete-visual-layout-recipes)
- [The Contribution Snake and Activity Animations](#the-contribution-snake-and-activity-animations)
- [Typography and Font Styling](#typography-and-font-styling)
- [Visual Consistency Rules](#visual-consistency-rules)

---

## Design Philosophy

A visually stunning README follows three principles:

1. **Cohesion** — Every visual element shares the same color palette, style, and energy
2. **Hierarchy** — The eye flows naturally from banner → badges → content → footer
3. **Restraint** — More visuals is not better; the RIGHT visuals are better

**The Visual Budget Rule:** A legendary README has at most:
- 1 banner/header
- 1 row of badges (max 6-8)
- 1-2 GIFs or screenshots
- 1-2 diagrams
- 1 footer

Anything beyond this becomes visual noise.

---

## The Style Selector

Choose ONE style for your entire README. Mixing styles looks chaotic.

| Style | Vibe | Colors | Best For |
| :--- | :--- | :--- | :--- |
| **Cyberpunk Neon** | Futuristic, edgy, hacker | Purple, pink, cyan on dark | CLI tools, security, AI |
| **Minimal Mono** | Clean, elegant, professional | Black, white, one accent | Libraries, SDKs, enterprise |
| **Sunset Gradient** | Warm, inviting, creative | Orange, pink, purple gradients | Creative tools, design |
| **Ocean Depth** | Calm, trustworthy, deep | Navy, teal, aqua | Infrastructure, databases |
| **Forest Tech** | Natural, sustainable, fresh | Green, emerald, lime | Open source, sustainability |
| **Retro Terminal** | Nostalgic, hacker, fun | Green on black, amber | CLI, terminal tools |
| **Candy Pop** | Fun, playful, energetic | Bright multi-color | Games, fun projects, bots |
| **Dark Luxe** | Premium, sophisticated | Gold, silver on dark | Premium tools, paid products |

---

## Color Palettes and Gradient Systems

### Pre-Built Palettes (Hex Codes Ready to Use)

#### Cyberpunk Neon
```
Primary:    #8B5CF6 (Purple)
Secondary:  #EC4899 (Pink)
Accent:     #06B6D4 (Cyan)
Background: #0F172A (Dark Navy)
Text:       #F8FAFC (Near White)

Gradient:   0:8B5CF6,100:EC4899
Badge color: 8B5CF6
```

#### Minimal Mono
```
Primary:    #1F2937 (Charcoal)
Secondary:  #6B7280 (Gray)
Accent:     #3B82F6 (Blue) or #10B981 (Emerald)
Background: #FFFFFF (White)
Text:       #111827 (Near Black)

Gradient:   0:1F2937,100:374151
Badge color: 1F2937
```

#### Sunset Gradient
```
Primary:    #F59E0B (Amber)
Secondary:  #EF4444 (Red)
Accent:     #8B5CF6 (Purple)
Background: #FFFBEB (Warm White)
Text:       #1C1917 (Dark Brown)

Gradient:   0:F59E0B,50:EF4444,100:8B5CF6
Badge color: F59E0B
```

#### Ocean Depth
```
Primary:    #0EA5E9 (Sky Blue)
Secondary:  #0D9488 (Teal)
Accent:     #06B6D4 (Cyan)
Background: #0C4A6E (Deep Navy)
Text:       #F0F9FF (Ice White)

Gradient:   0:0EA5E9,100:0D9488
Badge color: 0EA5E9
```

#### Forest Tech
```
Primary:    #10B981 (Emerald)
Secondary:  #059669 (Green)
Accent:     #84CC16 (Lime)
Background: #022C22 (Forest Dark)
Text:       #ECFDF5 (Mint White)

Gradient:   0:10B981,100:059669
Badge color: 10B981
```

#### Retro Terminal
```
Primary:    #22C55E (Terminal Green)
Secondary:  #16A34A (Dark Green)
Accent:     #FDE047 (Amber Warning)
Background: #000000 (Pure Black)
Text:       #22C55E (Green)

Gradient:   0:22C55E,100:16A34A
Badge color: 22C55E
```

#### Candy Pop
```
Primary:    #F472B6 (Pink)
Secondary:  #A78BFA (Lavender)
Accent:     #34D399 (Mint)
Background: #FDF4FF (Light Pink)
Text:       #1E1B4B (Deep Indigo)

Gradient:   0:F472B6,50:A78BFA,100:34D399
Badge color: F472B6
```

#### Dark Luxe
```
Primary:    #F59E0B (Gold)
Secondary:  #D4D4D8 (Silver)
Accent:     #FBBF24 (Bright Gold)
Background: #18181B (Rich Black)
Text:       #FAFAFA (White)

Gradient:   0:F59E0B,100:FBBF24
Badge color: F59E0B
```

### Capsule-Render customColorList Quick Reference

These are the `idx` values for the `customColorList` parameter:

| idx | Color Description | Best Styles |
| :---: | :--- | :--- |
| 0 | Warm sunset (orange → red) | Sunset Gradient |
| 2 | Cool ocean (blue → teal) | Ocean Depth |
| 3 | Purple dream (purple → pink) | Cyberpunk Neon |
| 5 | Forest (green → emerald) | Forest Tech |
| 6 | Deep space (indigo → violet) | Cyberpunk Neon, Dark Luxe |
| 11 | Coral reef (pink → orange) | Candy Pop, Sunset |
| 12 | Arctic (light blue → white) | Minimal Mono |
| 14 | Midnight (dark blue → purple) | Ocean Depth, Cyberpunk |
| 20 | Nebula (violet → magenta) | Cyberpunk Neon |
| 24 | Emerald city (green → cyan) | Forest Tech |
| 27 | Fire (red → orange → yellow) | Sunset Gradient |
| 30 | Ice (cyan → blue → purple) | Ocean Depth |

**Usage:** `&customColorList=6,11,20` (picks from these three randomly on each load)

### GitHub Color Swatch Feature

GitHub renders hex codes as colored dots in Markdown. Use this for visual color documentation:

```markdown
Here are our brand colors:

- `#8B5CF6` — Primary Purple
- `#EC4899` — Accent Pink
- `#06B6D4` — Highlight Cyan
```

---

## Banner Recipes (Copy-Paste Ready)

### Recipe 1: Cyberpunk Waving Header

```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:8B5CF6,100:EC4899&height=220&section=header&text=ProjectName&fontSize=55&fontColor=FFFFFF&animation=twinkling&fontAlignY=35&desc=Your%20awesome%20tagline%20here&descAlignY=55&descSize=16&descColor=E2E8F0" width="100%" alt="ProjectName" />
</p>
```

### Recipe 2: Minimal Transparent with Typing Effect

```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=transparent&height=150&text=ProjectName&fontSize=60&fontColor=1F2937&fontAlignY=50&animation=fadeIn" width="100%" alt="ProjectName" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Inter&weight=500&size=20&pause=1000&color=3B82F6&center=true&vCenter=true&width=500&lines=Clean+code.+Clear+docs.+Ship+fast." alt="Tagline" />
</p>
```

### Recipe 3: Venom Style (Dramatic Dark)

```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=venom&color=0:0EA5E9,100:8B5CF6&height=200&text=ProjectName&fontSize=50&fontColor=FFFFFF&animation=scaleIn" width="100%" alt="ProjectName" />
</p>
```

### Recipe 4: Shark Bite (Edgy)

```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=shark&color=gradient&customColorList=6,11,20&height=180&section=header&text=ProjectName&fontSize=45&fontColor=FFFFFF&fontAlignY=40" width="100%" alt="ProjectName" />
</p>
```

### Recipe 5: Soft Rounded (Friendly)

```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=soft&color=0:10B981,100:059669&height=150&text=ProjectName&fontSize=45&fontColor=FFFFFF&animation=fadeIn&fontAlignY=45" width="100%" alt="ProjectName" />
</p>
```

### Recipe 6: Cylinder (Retro/3D)

```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=cylinder&color=0:F59E0B,100:EF4444&height=150&text=ProjectName&fontSize=40&fontColor=FFFFFF&animation=blinking" width="100%" alt="ProjectName" />
</p>
```

### Recipe 7: SVG Banners (Self-Hosted Alternative)

From [Akshay090/svg-banners](https://github.com/Akshay090/svg-banners):

```markdown
<p align="center">
  <img src="https://svg-banners.vercel.app/api?type=luminance&text1=ProjectName&width=800&height=200" alt="ProjectName Banner" />
</p>
```

Types available: `luminance`, `typeWriter`, `glitch`, `origin`, `rainbow`, `wave`

### Recipe 8: Animated Sweet Banner

From [SystemVll/readme-animated-sweetbanner](https://github.com/SystemVll/readme-animated-sweetbanner):

Custom animated SVG banners with meteors, glowing effects, and particle animations. Use the web editor to generate your banner SVG, then host it in your repo.

### Footer Recipes

```markdown
<!-- Matching waving footer -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:8B5CF6,100:EC4899&height=120&section=footer" width="100%" />
</p>

<!-- Minimal line footer -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:8B5CF6,100:EC4899&height=2&section=footer" width="100%" />
</p>

<!-- Soft rounded footer -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=soft&color=gradient&customColorList=6,11,20&height=80&section=footer&text=Made%20with%20❤️&fontSize=16&fontColor=FFFFFF" width="100%" />
</p>
```

---

## GIF Libraries and Animated Assets

### Curated GIF Sources for READMEs

| Source | What It Has | URL |
| :--- | :--- | :--- |
| **Cool-GIFs-For-GitHub** | Animated logos, emojis, banners, work culture GIFs | [github.com/Anmol-Baranwal/Cool-GIFs-For-GitHub](https://github.com/Anmol-Baranwal/Cool-GIFs-For-GitHub) |
| **LottieFiles** | Professional animated illustrations (free tier) | [lottiefiles.com](https://lottiefiles.com) |
| **Icons8 Illustrations** | Animated illustrations in multiple styles | [icons8.com/illustrations](https://icons8.com/illustrations) |
| **DrawKit** | Hand-drawn animated illustrations | [drawkit.com](https://drawkit.com) |
| **unDraw** | Open-source SVG illustrations (customizable colors) | [undraw.co](https://undraw.co) |
| **Storyset** | Animated illustrations with customizable colors | [storyset.com](https://storyset.com) |
| **Giphy Developers** | Searchable GIF API for any topic | [giphy.com](https://giphy.com) |

### Animated Tech Logo GIFs (Direct Links)

These are commonly used animated tech logos from the Cool-GIFs-For-GitHub repository:

```markdown
<!-- Animated tech logos (40px height for inline use) -->
<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/212257454-16e3712e-945a-4ca2-b238-408ad0bf87e6.gif" width="40" alt="JavaScript" />
  <img src="https://user-images.githubusercontent.com/74038190/212257472-08e52665-c503-4bd9-aa20-f5a4dae769b5.gif" width="40" alt="TypeScript" />
  <img src="https://user-images.githubusercontent.com/74038190/212257468-1e9a91f1-b626-4baa-b15d-5c385dfa7ed2.gif" width="40" alt="CSS" />
  <img src="https://user-images.githubusercontent.com/74038190/212257465-7ce8d493-cac5-494e-982a-5a9deb852c4b.gif" width="40" alt="React" />
  <img src="https://user-images.githubusercontent.com/74038190/212257463-4d082cb4-7483-4eaf-bc25-6dde2628aabd.gif" width="40" alt="Git" />
  <img src="https://user-images.githubusercontent.com/74038190/212257460-738ff738-247f-4445-a718-cdd0ca76e2db.gif" width="40" alt="Java" />
  <img src="https://user-images.githubusercontent.com/74038190/212257467-871d32b7-e401-42e8-a166-fcfd7baa4c6b.gif" width="40" alt="Python" />
  <img src="https://user-images.githubusercontent.com/74038190/212281756-450d3ffa-9335-4b98-a965-db8a18fee927.gif" width="40" alt="Docker" />
  <img src="https://user-images.githubusercontent.com/74038190/212280805-9bcb336b-8c55-46a8-abf8-ff286ab55472.gif" width="40" alt="AWS" />
</p>
```

### Animated Social Media Icons

```markdown
<!-- Animated social icons (35px for clean inline display) -->
<p align="center">
  <a href="https://linkedin.com/in/USERNAME">
    <img src="https://user-images.githubusercontent.com/74038190/235294012-0a55e343-37ad-4b0f-924f-c8431d9d2483.gif" width="35" alt="LinkedIn" />
  </a>
  <a href="https://twitter.com/USERNAME">
    <img src="https://user-images.githubusercontent.com/74038190/235294011-b8074c31-9097-4a65-a594-4151b58743a8.gif" width="35" alt="Twitter" />
  </a>
  <a href="https://discord.gg/INVITE">
    <img src="https://user-images.githubusercontent.com/74038190/235294015-47144047-25ab-417c-af1b-6746820a20ff.gif" width="35" alt="Discord" />
  </a>
  <a href="https://youtube.com/@USERNAME">
    <img src="https://user-images.githubusercontent.com/74038190/235294007-de441046-823e-4eff-89bf-d4df52858b65.gif" width="35" alt="YouTube" />
  </a>
  <a href="mailto:email@example.com">
    <img src="https://user-images.githubusercontent.com/74038190/235294010-ec412ef5-e3da-4efa-b1d4-0ab4d4638755.gif" width="35" alt="Email" />
  </a>
</p>
```

### Animated Dividers and Decorations

```markdown
<!-- Rainbow line divider -->
<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%" alt="divider" />

<!-- Neon line divider -->
<img src="https://user-images.githubusercontent.com/74038190/212284115-f47cd8ff-2ffb-4b04-b5bf-4d1c14c0247f.gif" width="100%" alt="divider" />

<!-- Pac-Man divider (fun!) -->
<img src="https://user-images.githubusercontent.com/74038190/212284158-e840e285-664b-44d7-b79b-e264b5e54825.gif" width="400" alt="pacman" />
```

### Animated "Hello" / Greeting GIFs

```markdown
<!-- Waving hand -->
<img src="https://user-images.githubusercontent.com/74038190/214644152-52f47eb3-5e31-4f47-8758-05c9468b5596.gif" width="40" alt="wave" />

<!-- Developer at work -->
<img src="https://user-images.githubusercontent.com/74038190/229223263-cf2e4b07-2615-4f87-9c38-e37600f8381a.gif" width="400" alt="developer" />

<!-- Coding animation -->
<img src="https://user-images.githubusercontent.com/74038190/212749447-bfb7e725-6987-49d9-ae85-2015e3e7cc41.gif" width="400" alt="coding" />
```

### GIF Usage Best Practices

| Rule | Why |
| :--- | :--- |
| Max 2-3 GIFs per README | More causes visual overload and slow loading |
| Keep GIFs under 5MB each | GitHub has a 10MB file limit; large GIFs lag |
| Use `width` attribute always | Prevents layout shifts on different screens |
| Add meaningful `alt` text | Accessibility for screen readers |
| Place GIFs near relevant content | Don't use decorative GIFs in technical sections |
| Prefer SVG animations over GIFs | Smaller files, sharper rendering, scalable |

---

## Dynamic Widgets and Stats Cards

### GitHub Readme Stats

```markdown
<!-- Stats card with custom theme -->
<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=USERNAME&show_icons=true&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=8B5CF6&icon_color=EC4899&text_color=E2E8F0" alt="GitHub Stats" />
</p>

<!-- Top languages card -->
<p align="center">
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=USERNAME&layout=compact&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=8B5CF6&text_color=E2E8F0" alt="Top Languages" />
</p>

<!-- Repo card (for featuring specific repos) -->
<p align="center">
  <a href="https://github.com/USER/REPO">
    <img src="https://github-readme-stats.vercel.app/api/pin/?username=USER&repo=REPO&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=8B5CF6&icon_color=EC4899" alt="Repo Card" />
  </a>
</p>
```

**Available themes:** `default`, `dark`, `radical`, `merko`, `gruvbox`, `tokyonight`, `onedark`, `cobalt`, `synthwave`, `highcontrast`, `dracula`, `monokai`, `vue`, `vue-dark`, `shades-of-purple`, `nightowl`, `buefy`, `blue-green`, `algolia`, `great-gatsby`, `darcula`, `bear`, `solarized-dark`, `solarized-light`, `chartreuse-dark`, `nord`, `gotham`, `material-palenight`, `graywhite`, `vision-friendly-dark`, `aura-dark`, `jolly`, `noctis-minimus`, `github_dark`, `github_dark_dimmed`, `catppuccin_latte`, `catppuccin_mocha`

**Custom colors (override theme):**
```
&bg_color=HEX      Background
&title_color=HEX   Title text
&text_color=HEX    Body text
&icon_color=HEX    Icons
&border_color=HEX  Border (if show_border=true)
&ring_color=HEX    Progress ring
```

### GitHub Streak Stats

```markdown
<p align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user=USERNAME&theme=tokyonight&hide_border=true&background=0D1117&stroke=8B5CF6&ring=EC4899&fire=EC4899&currStreakLabel=8B5CF6" alt="GitHub Streak" />
</p>
```

### GitHub Profile Trophy

```markdown
<p align="center">
  <img src="https://github-profile-trophy.vercel.app/?username=USERNAME&theme=tokyonight&no-frame=true&no-bg=true&column=7&margin-w=10" alt="Trophies" />
</p>
```

### GitHub Activity Graph

```markdown
<p align="center">
  <img src="https://github-readme-activity-graph.vercel.app/graph?username=USERNAME&theme=tokyo-night&hide_border=true&bg_color=0D1117&color=8B5CF6&line=EC4899&point=06B6D4&area=true&area_color=8B5CF6" alt="Activity Graph" />
</p>
```

### Visitor Counter

```markdown
<!-- Profile views counter -->
<p align="center">
  <img src="https://komarev.com/ghpvc/?username=USERNAME&style=flat-square&color=8B5CF6&label=Profile+Views" alt="Profile Views" />
</p>

<!-- Hit counter for repos -->
<p align="center">
  <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FUSER%2FREPO&count_bg=%238B5CF6&title_bg=%231F2937&icon=github.svg&icon_color=%23E7E7E7&title=visits&edge_flat=true" alt="Hits" />
</p>
```

---

## Illustration and Icon Sources

### Free Illustration Libraries (for README Headers and Sections)

| Library | Style | License | Best For |
| :--- | :--- | :--- | :--- |
| [unDraw](https://undraw.co) | Flat, modern, customizable color | MIT | Tech projects, SaaS |
| [Storyset](https://storyset.com) | Animated, multiple styles | Free with attribution | Any project |
| [DrawKit](https://drawkit.com) | Hand-drawn, playful | Free tier available | Creative projects |
| [Open Peeps](https://openpeeps.com) | Hand-drawn people | CC0 | Community, social |
| [Humaaans](https://humaaans.com) | Mix-and-match people | Free | Team pages, about |
| [Blush](https://blush.design) | Multiple artist styles | Free tier | Diverse styles |
| [Illustrations.co](https://illlustrations.co) | Minimal, open source | MIT | Clean, minimal |
| [ManyPixels](https://manypixels.co/gallery) | Flat, isometric options | Free | Tech, business |
| [Pixeltrue](https://pixeltrue.com) | Animated SVGs | Free | Dynamic READMEs |

### Icon Sets for Feature Grids

```markdown
<!-- Using emoji as icons (universal, no hosting needed) -->
| | Feature | Description |
| :---: | :--- | :--- |
| 🚀 | **Performance** | Sub-millisecond response times |
| 🔒 | **Security** | Enterprise-grade encryption |
| 🧩 | **Extensible** | Plugin system for everything |

<!-- Using Devicon (tech-specific icons) -->
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" width="40" alt="React" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg" width="40" alt="TypeScript" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg" width="40" alt="Node.js" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" width="40" alt="Docker" />
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="40" alt="PostgreSQL" />

<!-- Using Skill Icons (beautiful grouped tech badges) -->
<p align="center">
  <img src="https://skillicons.dev/icons?i=react,ts,nodejs,docker,postgres,redis&theme=dark" alt="Tech Stack" />
</p>
```

### Skill Icons (skillicons.dev)

Beautiful, consistent tech stack badges in one line:

```markdown
<!-- Dark theme -->
<img src="https://skillicons.dev/icons?i=js,ts,react,nextjs,nodejs,python,rust,go&theme=dark" />

<!-- Light theme -->
<img src="https://skillicons.dev/icons?i=js,ts,react,nextjs,nodejs,python,rust,go&theme=light" />

<!-- With line breaks (perline parameter) -->
<img src="https://skillicons.dev/icons?i=js,ts,react,nextjs,nodejs,python,rust,go,docker,kubernetes,aws,gcp&perline=6&theme=dark" />
```

Available icons: `js`, `ts`, `react`, `nextjs`, `vue`, `nuxtjs`, `svelte`, `angular`, `nodejs`, `deno`, `bun`, `python`, `rust`, `go`, `java`, `kotlin`, `swift`, `cpp`, `cs`, `ruby`, `php`, `dart`, `flutter`, `docker`, `kubernetes`, `aws`, `gcp`, `azure`, `vercel`, `netlify`, `supabase`, `firebase`, `mongodb`, `postgres`, `mysql`, `redis`, `graphql`, `prisma`, `git`, `github`, `gitlab`, `linux`, `vim`, `vscode`, `figma`, `tailwind`, `sass`, `webpack`, `vite`, and many more.

---

## Complete Visual Layout Recipes

### Recipe A: Cyberpunk Neon Full Header

```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:8B5CF6,100:EC4899&height=200&section=header&text=ProjectName&fontSize=50&fontColor=FFFFFF&animation=twinkling&fontAlignY=35&desc=Tagline%20goes%20here&descAlignY=55&descSize=16&descColor=E2E8F0" width="100%" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=18&pause=1000&color=8B5CF6&center=true&vCenter=true&width=500&lines=First+rotating+message;Second+rotating+message;Third+rotating+message" alt="Typing" />
</p>

<p align="center">
  <a href="#quick-start"><img src="https://img.shields.io/badge/Get_Started-8B5CF6?style=for-the-badge&logoColor=white" alt="Get Started" /></a>
  <a href="#docs"><img src="https://img.shields.io/badge/Documentation-EC4899?style=for-the-badge&logoColor=white" alt="Docs" /></a>
  <a href="https://discord.gg/xxx"><img src="https://img.shields.io/badge/Discord-06B6D4?style=for-the-badge&logo=discord&logoColor=white" alt="Discord" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/USER/REPO?style=flat-square&color=8B5CF6" alt="Stars" />
  <img src="https://img.shields.io/github/license/USER/REPO?style=flat-square&color=EC4899" alt="License" />
  <img src="https://img.shields.io/github/actions/workflow/status/USER/REPO/ci.yml?style=flat-square&color=06B6D4&label=build" alt="Build" />
  <img src="https://img.shields.io/npm/v/PACKAGE?style=flat-square&color=8B5CF6" alt="Version" />
</p>

<!-- Animated divider -->
<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="100%" />
```

### Recipe B: Minimal Professional Header

```markdown
<div align="center">

# ProjectName

**One clear sentence describing what this does.**

[![Build](https://img.shields.io/github/actions/workflow/status/USER/REPO/ci.yml?style=flat-square&label=build)](https://github.com/USER/REPO/actions)
[![Version](https://img.shields.io/npm/v/PACKAGE?style=flat-square)](https://npmjs.com/package/PACKAGE)
[![License](https://img.shields.io/github/license/USER/REPO?style=flat-square)](LICENSE)
[![Downloads](https://img.shields.io/npm/dm/PACKAGE?style=flat-square)](https://npmjs.com/package/PACKAGE)

[Quick Start](#quick-start) · [Documentation](https://docs.example.com) · [Examples](./examples)

</div>

---
```

### Recipe C: Ocean Depth with Tech Stack

```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0EA5E9,100:0D9488&height=180&section=header&text=ProjectName&fontSize=45&fontColor=FFFFFF&animation=fadeIn&fontAlignY=38" width="100%" />
</p>

<p align="center">
  <strong>A brief, powerful description of what this project does.</strong>
</p>

<p align="center">
  <img src="https://skillicons.dev/icons?i=typescript,react,nodejs,postgres,docker,redis&theme=dark" alt="Tech Stack" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0.0-0EA5E9?style=flat-square" />
  <img src="https://img.shields.io/badge/tests-passing-0D9488?style=flat-square" />
  <img src="https://img.shields.io/badge/coverage-94%25-06B6D4?style=flat-square" />
  <img src="https://img.shields.io/badge/license-MIT-0EA5E9?style=flat-square" />
</p>
```

### Recipe D: Fun Candy Pop with GIFs

```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=egg&color=0:F472B6,100:A78BFA&height=200&text=ProjectName&fontSize=50&fontColor=FFFFFF&animation=blinking" width="100%" />
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/74038190/229223263-cf2e4b07-2615-4f87-9c38-e37600f8381a.gif" width="300" alt="Coding" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Fun_Level-Over_9000-F472B6?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Bugs-They're_Features-A78BFA?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Coffee_Consumed-∞-34D399?style=for-the-badge" />
</p>
```

### Recipe E: Dark Luxe Premium

```markdown
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=18181B&height=1&section=header" width="100%" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Playfair+Display&weight=700&size=36&pause=1000&color=F59E0B&center=true&vCenter=true&width=600&height=60&lines=ProjectName" alt="ProjectName" />
</p>

<p align="center">
  <sub>
    <img src="https://img.shields.io/badge/★★★★★-F59E0B?style=flat-square" />
    Premium developer tooling for teams that ship.
    <img src="https://img.shields.io/badge/★★★★★-F59E0B?style=flat-square" />
  </sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Enterprise_Ready-F59E0B?style=flat-square&logoColor=18181B" />
  <img src="https://img.shields.io/badge/SOC2_Compliant-D4D4D8?style=flat-square" />
  <img src="https://img.shields.io/badge/99.99%25_Uptime-FBBF24?style=flat-square" />
</p>
```

---

## The Contribution Snake and Activity Animations

### GitHub Contribution Snake

A snake animation that eats your contribution graph. Requires GitHub Actions:

```yaml
# .github/workflows/snake.yml
name: Generate Snake

on:
  schedule:
    - cron: "0 0 * * *"  # Every day at midnight
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: Platane/snk@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/github-snake.svg
            dist/github-snake-dark.svg?palette=github-dark

      - uses: crazy-max/ghaction-github-pages@v3
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

Then in your README:

```markdown
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/USER/USER/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/USER/USER/output/github-snake.svg" />
  <img alt="Snake animation" src="https://raw.githubusercontent.com/USER/USER/output/github-snake.svg" />
</picture>
```

---

## Typography and Font Styling

### Typing SVG Font Options

Popular fonts for `readme-typing-svg`:

| Font | Vibe | Best For |
| :--- | :--- | :--- |
| `Fira+Code` | Developer, monospace | Technical projects |
| `JetBrains+Mono` | Modern monospace | Code-heavy projects |
| `Inter` | Clean, professional | SaaS, enterprise |
| `Poppins` | Friendly, rounded | Creative projects |
| `Space+Mono` | Retro, space-age | Experimental projects |
| `Playfair+Display` | Elegant, serif | Premium/luxury |
| `Orbitron` | Futuristic, geometric | Sci-fi, gaming |
| `Press+Start+2P` | Pixel art, retro | Games, fun projects |
| `Permanent+Marker` | Handwritten, casual | Personal projects |

### Multi-Line Typing Effect

```markdown
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=8B5CF6&center=true&vCenter=true&multiline=true&repeat=false&width=600&height=100&lines=Welcome+to+ProjectName;The+future+of+%5Bthing%5D+is+here." alt="Welcome" />
</p>
```

---

## Visual Consistency Rules

### The Matching Rule

Every visual element in your README should share the same DNA:

| Element | Must Match |
| :--- | :--- |
| Banner gradient | Badge colors |
| Badge style | All badges same `style=` value |
| Icon theme | All from same source (Devicon OR Skill Icons, not mixed) |
| GIF style | All same art style (don't mix pixel art with 3D) |
| Diagram theme | Mermaid theme matches overall palette |
| Font choice | Typing SVG font matches project personality |

### The Color Consistency Checklist

Before shipping, verify:

- [ ] Banner uses colors from your chosen palette
- [ ] All custom badges use the same hex colors
- [ ] Stats cards use matching theme or custom colors
- [ ] Typing SVG color matches primary brand color
- [ ] Footer matches header (same gradient, same type)
- [ ] Any illustrations match the overall color scheme

### Badge Alignment Rules

```markdown
<!-- GOOD: All same style, consistent spacing -->
<p align="center">
  <img src="https://img.shields.io/badge/A-8B5CF6?style=flat-square" />
  <img src="https://img.shields.io/badge/B-EC4899?style=flat-square" />
  <img src="https://img.shields.io/badge/C-06B6D4?style=flat-square" />
</p>

<!-- BAD: Mixed styles, inconsistent -->
<p align="center">
  <img src="https://img.shields.io/badge/A-8B5CF6?style=for-the-badge" />
  <img src="https://img.shields.io/badge/B-green?style=flat" />
  <img src="https://img.shields.io/badge/C-blue?style=plastic" />
</p>
```

### Responsive Width Guidelines

| Element | Recommended Width | Why |
| :--- | :--- | :--- |
| Banner | `width="100%"` | Full bleed, responsive |
| GIFs/Screenshots | `width="600"` to `width="800"` | Fits most viewports |
| Logos/Icons | `width="40"` to `width="60"` | Inline-friendly |
| Dividers | `width="100%"` | Full bleed |
| Stats cards | No width (auto) or `width="450"` | Standard card size |
| Side-by-side images | `width="48%"` each | Leaves gap between |

### The "Squint Test"

Squint at your README (or zoom out to 25%). Can you still see:
1. A clear header area?
2. Distinct sections?
3. Visual breathing room between elements?
4. A clear footer/ending?

If YES → Your visual hierarchy works.
If NO → You need more whitespace, clearer section breaks, or fewer competing elements.
