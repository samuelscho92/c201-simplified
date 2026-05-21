# C201 Simplified — Project Instructions

This project simplifies C201 course materials (originally written for American adults) into IELTS Level 3 English for non-English-proficient audiences. Simplified sessions are published at **https://samuelscho92.github.io/c201-simplified/**.

## Folder Structure

```
C201_Project/
├── C201_Ch1/          Original course PDFs (Ch1 sessions 1A–1D)
├── C201_Ch2/          Original course PDFs (Ch2 sessions 2A–2D)
├── C201_Ch3/          Original course PDFs (Ch3 sessions 3A–3E)
├── C201_Ch4/          Original course PDFs (Ch4 sessions 4A–4D)
├── C201_FM_Simplified/    Simplified IELTS 3 markdown files (source of truth)
├── rebuild_preview.py     Builds index.html from all .md files and pushes to GitHub
├── index.html             Auto-generated — do not edit directly
└── .claude/commands/      Project skills
```

## File Naming Convention

Simplified MD files go in `C201_FM_Simplified/` and follow this pattern:

```
C201_{chapter}{session}_{Title}.md
Examples:
  C201_1A_Seeing_God.md
  C201_2B_Dreadful_Repentance.md
```

## Deploy Workflow

After writing or updating any MD files:

```bash
python3 rebuild_preview.py
```

This builds `index.html`, commits, and pushes to GitHub Pages automatically.

---

## Simplification Requirements

### Reading Level
- Use IELTS Level 3 English (A2 level — basic, everyday vocabulary)
- Use common words only
- Keep sentences short — one idea per sentence, max ~12 words
- Avoid idioms, slang, and complex expressions
- Avoid phrasal verbs when possible
- Tone should be respectful, never childish

### Structure
- Each session should take about 1 hour to complete
- Start every session with a **Key Words** table (pre-teach theological vocabulary)
- Use clear numbered or named sections (Part 1, Part 2, etc.)
- Avoid unnecessary details
- Use a concrete example (marked with *Example:*) whenever an idea is abstract

### Bible Translation
- Always convert Bible verses to **NLT** (New Living Translation)

### Quotes
- Keep quotes when possible
- If a quote is too difficult for IELTS 3, simplify it and note *(Simplified from original)*
- If still too complex after simplifying, remove it

### Vocabulary Support (Definition Tables)
- For all words above IELTS 3 in Bible verses or quotes, add a definition table
- Place after the verse or quote it relates to
- Use matching superscripts (¹ ² ³…) to link difficult words to their definitions
- The final Word document will place these tables in the right 1/3 sidebar — note this in layout notes if needed

### Opening Hymns / Poetry
- Keep original text as-is (do not rewrite hymns)
- Add a **"What this means:"** plain-English summary directly below

### Consistent Terms
- Use the same word for the same concept throughout (e.g. always "sin," never alternating with "wrongdoing" or "transgression")

---

## Session File Template

````markdown
# SESSION {ID} — {TITLE}
**Course 201 · Chapter {N} · {Chapter Theme}**

---

## Key Words

| Word | Meaning |
|---|---|
| word | definition |

---

## Part 1: {Section Title}

[Content]

---

## Part 2: {Section Title}

[Content]

---

## Discussion Questions

1. Question
2. Question
````

---

## Source Materials by Chapter

| Chapter | Theme | Sessions |
|---|---|---|
| 1 | Holiness of God | 1A Seeing God, 1B Seeing Myself, 1C The Cross, 1D Self-Reflection |
| 2 | Repentance | 2A We Need Repentance, 2B Dreadful Repentance, 2C We Don't Understand Repentance, 2D Repentance Loop |
| 3 | Heaven & Hell, Worship, Evangelism | 3A–3C Heaven & Hell, 3D Worship & Pitfalls, 3E Evangelism |
| 4 | Spiritual Battle, Prayer | 4A Knowing the Enemy, 4B Spiritual Battle, 4C Two Crucial Weapons, 4D Prayer |

## Completed Sessions
- [x] C201_1A_Seeing_God.md
- [x] C201_1B_Seeing_Myself.md
- [x] C201_1C_The_Cross.md
- [x] C201_1D_Self_Reflection.md
- [x] C201_2A_We_Need_Repentance.md
- [x] C201_2B_Dreadful_Repentance.md
- [x] C201_2C_We_Dont_Understand_Repentance.md
- [x] C201_2D_Repentance_Loop.md
- [x] C201_3A_What_Is_Real.md
- [x] C201_3B_Reality_of_Heaven_and_Hell.md
- [x] C201_3C_Heaven_and_Hell.md
- [x] C201_3D_Worship.md
- [x] C201_3E_Evangelism.md
- [x] C201_4A_Know_Your_Enemy.md
- [x] C201_4B_Spiritual_Battle.md
- [x] C201_4C_Two_Crucial_Weapons.md
- [x] C201_4D_Praying_Like_Jesus.md
