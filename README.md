# C201 Simplified

A simplified version of the C201 discipleship course, rewritten for non-English-proficient audiences at **IELTS Level 3 (A2)**.

**Live site:** https://samuelscho92.github.io/c201-simplified/

---

## About

The original C201 course materials were written for American adults at approximately IELTS 6–7 level. This project simplifies all 17 sessions across 4 chapters while preserving the full theological content.

**Simplification standards:**
- IELTS Level 3 English (short sentences, common words, one idea per sentence)
- All Bible verses converted to NLT
- Quotes simplified or summarized where needed
- Definition tables added for difficult words
- Concrete examples added for abstract concepts

---

## Contents

### Chapter 1 — Holiness of God
- 1A: Seeing God
- 1B: Seeing Myself
- 1C: The Cross
- 1D: Self-Reflection

### Chapter 2 — Repentance
- 2A: We Need Repentance
- 2B: Dreadful Repentance
- 2C: We Don't Understand Repentance
- 2D: Confession and Repentance Loop

### Chapter 3 — Heaven and Hell
- 3A: What Is Real?
- 3B: Reality of Heaven and Hell
- 3C: Heaven and Hell
- 3D: Worship
- 3E: Evangelism: Habits to Form

### Chapter 4 — Spiritual Battle
- 4A: Know Your Enemy
- 4B: Spiritual Battle
- 4C: Two Crucial Weapons
- 4D: Habits to Form: Praying Like Jesus

---

## How to Update

1. Add or edit `.md` files in `C201_FM_Simplified/`
2. Run the build and deploy script:

```bash
python3 rebuild_preview.py
```

This rebuilds `index.html` and pushes to GitHub Pages automatically.

To build locally without deploying:

```bash
python3 rebuild_preview.py --no-push
open index.html
```

---

## Using the `/simplify` Skill

When working in Claude Code from this folder, type:

```
/simplify 2A
```

Claude will find the source PDF, write the simplified markdown, and deploy.
