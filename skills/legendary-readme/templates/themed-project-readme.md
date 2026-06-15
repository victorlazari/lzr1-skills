# Themed Project README Template

> A fully worked example of the **Theme Engine** in action.
> This sample uses the **Guardian Fortress** kit for a fictional backup tool called **VaultKeeper**.
> Study how EVERY element — banner, colors, mascot 🛡️ "Sir Backsalot", section names, GIFs, and catchphrase — points back to one concept: *"Your files have a guardian."*
> To reuse: swap the theme kit, replace `[bracketed]` values, and keep the structure.

---

<!-- ════════════ THEME KIT (keep as a comment for future editors) ════════════
Concept:     "Your files have a guardian"
Archetype:   Guardian Fortress
Mascot:      🛡️ Sir Backsalot
Catchphrase: "Sleep well. The Guardian is watching."
Palette:     #1E3A8A · #64748B · #F59E0B · BG #0F172A · Text #F1F5F9
Gradient:    0:1E3A8A,100:F59E0B
═══════════════════════════════════════════════════════════════════════════ -->

<!-- COPY BELOW THIS LINE -->

<!-- BANNER: themed colors + animation -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=slice&color=0:1E3A8A,100:F59E0B&height=210&section=header&text=VaultKeeper&fontSize=54&fontColor=FFFFFF&animation=fadeIn&fontAlignY=38&desc=Your%20files%20have%20a%20guardian&descAlignY=58&descColor=F1F5F9" width="100%" alt="VaultKeeper — Your files have a guardian" />
</p>

<!-- TYPING TAGLINE: the catchphrase, in a themed font -->
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Cinzel&weight=600&size=20&pause=1200&color=F59E0B&center=true&vCenter=true&width=600&lines=Sleep+well.+The+Guardian+is+watching.;Back+up+once.+Worry+never." alt="Tagline" />
</p>

<!-- BADGES: only palette colors (navy, steel, gold) -->
<p align="center">
  <img src="https://img.shields.io/github/v/release/acme/vaultkeeper?style=flat-square&color=1E3A8A&label=version" alt="Version" />
  <img src="https://img.shields.io/github/actions/workflow/status/acme/vaultkeeper/ci.yml?style=flat-square&color=F59E0B&label=build" alt="Build" />
  <img src="https://img.shields.io/github/license/acme/vaultkeeper?style=flat-square&color=64748B" alt="License" />
  <img src="https://img.shields.io/github/stars/acme/vaultkeeper?style=flat-square&color=F59E0B&label=stars" alt="Stars" />
</p>

<!-- HERO GIF: the mascot's domain — a vault/shield (themed, not random) -->
<p align="center">
  <img src="https://media.giphy.com/media/REPLACE_WITH_SHIELD_OR_VAULT_GIF/giphy.gif" width="320" alt="A vault door swinging shut and locking" />
  <br />
  <sub><em>🛡️ Sir Backsalot reporting for duty.</em></sub>
</p>

---

## 📜 The Oath  <!-- themed name for "Intro" -->

**VaultKeeper** automatically backs up your files so you never lose work again. It runs quietly in the background, copies your important folders to safe storage, and lets you roll back to any earlier version in one command.

Think of it as a **guardian angel for your files** 🛡️. You don't have to remember to back up — Sir Backsalot never sleeps, never forgets, and never complains.

**Why?** Because losing three days of work to a crashed laptop is a special kind of pain that nobody should feel twice.

```bash
# Summon the Guardian in 30 seconds
npm install -g vaultkeeper && vaultkeeper guard ./my-project
```

> **For everyone:** A "backup" is just a safe copy of your files kept somewhere else. If your computer breaks, your copy is still safe. That's all this does — automatically.

---

## 🗡️ The Arsenal  <!-- themed name for "Features" -->

<table>
  <tr>
    <td align="center" width="33%">
      <br /><img src="https://img.shields.io/badge/🛡️-1E3A8A?style=for-the-badge" /><br />
      <strong>Always Watching</strong><br />
      <sub>Backs up automatically, every change</sub><br /><br />
    </td>
    <td align="center" width="33%">
      <br /><img src="https://img.shields.io/badge/⏪-F59E0B?style=for-the-badge" /><br />
      <strong>Time Travel</strong><br />
      <sub>Roll back to any past version</sub><br /><br />
    </td>
    <td align="center" width="33%">
      <br /><img src="https://img.shields.io/badge/🔒-64748B?style=for-the-badge" /><br />
      <strong>Locked Tight</strong><br />
      <sub>End-to-end encrypted, always</sub><br /><br />
    </td>
  </tr>
</table>

---

## ⚔️ Summon the Guardian  <!-- themed name for "Install" -->

<table>
  <tr>
    <td>

**Step 1 — Recruit him**
```bash
npm install -g vaultkeeper
```

**Step 2 — Give him a post**
```bash
vaultkeeper guard ./important-folder
```

**Step 3 — Sleep well**
```bash
vaultkeeper status   # "All quiet. Watching 1,204 files."
```

    </td>
    <td width="40%" align="center">

```mermaid
graph TD
    A[Install] -->|10s| B[Point at a folder]
    B -->|instant| C[Guardian on watch]
    C -->|forever| D[🛡️ Files safe]
    style A fill:#1E3A8A,color:#fff
    style C fill:#F59E0B,color:#fff
    style D fill:#1E3A8A,color:#fff
```

    </td>
  </tr>
</table>

---

## 🏰 Standing Watch  <!-- themed name for "Usage" -->

Here's the Guardian protecting a folder, then restoring a file from yesterday:

<!-- DEMO GIF: the REAL product working — this one is non-negotiable -->
<p align="center">
  <img src="./docs/vaultkeeper-demo.gif" width="700" alt="Terminal showing VaultKeeper backing up files and restoring an earlier version" />
  <br />
  <sub><em>Restoring a file from yesterday — in one command.</em></sub>
</p>

```bash
# See every saved version of a file
vaultkeeper history report.pdf

# Bring back the version from 2 hours ago
vaultkeeper restore report.pdf --when "2 hours ago"
```

---

## 🤝 Join the Order  <!-- themed name for "Contributing" -->

The Order of the Guardian always welcomes new knights.

<table>
  <tr>
    <td align="center" width="25%"><strong>🐛</strong><br /><a href="#">Report a Breach</a></td>
    <td align="center" width="25%"><strong>💡</strong><br /><a href="#">Propose a Weapon</a></td>
    <td align="center" width="25%"><strong>📜</strong><br /><a href="CONTRIBUTING.md">Read the Code</a></td>
    <td align="center" width="25%"><strong>⭐</strong><br /><a href="#">Pledge a Star</a></td>
  </tr>
</table>

> **Sir Backsalot says:** "A single star powers my shield for a fortnight. Probably."

---

## 📖 The Decree  <!-- themed name for "License" -->

VaultKeeper is released under the MIT License — free to use, modify, and share. See [LICENSE](LICENSE) for the full decree.

---

<!-- FOOTER: mirrors the header, mascot says goodbye in theme voice -->
<p align="center">
  <img src="https://media.giphy.com/media/REPLACE_WITH_KNIGHT_WAVE_GIF/giphy.gif" width="160" alt="A knight waving goodbye" />
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=slice&color=0:F59E0B,100:1E3A8A&height=110&section=footer&text=Sleep%20well.%20The%20Guardian%20is%20watching.&fontSize=18&fontColor=FFFFFF" width="100%" />
</p>

<!-- Easter egg for source readers -->
<!--
   🛡️  You read the source. Sir Backsalot respects that.
   Secret command:  vaultkeeper --knight-mode
-->
