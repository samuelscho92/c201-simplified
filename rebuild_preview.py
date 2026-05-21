#!/usr/bin/env python3
"""
Rebuilds index.html from all .md files in C201_FM_Simplified/,
then commits and pushes to GitHub Pages.

Usage:
    python3 rebuild_preview.py           # build + commit + push
    python3 rebuild_preview.py --no-push # build only, no git
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path

BASE = Path(__file__).parent
MD_DIR = BASE / "C201_FM_Simplified"
OUT = BASE / "index.html"
PUSH = "--no-push" not in sys.argv


def get_title(content: str, filename: str) -> str:
    """Extract first H1 from markdown, fall back to filename."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return filename.replace("_", " ").replace(".md", "")


def get_subtitle(content: str) -> str:
    """Extract first bold line after H1 (e.g. 'Course 201 · Chapter 1')."""
    match = re.search(r'^\*\*(.+?)\*\*', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


def get_chapter(filename: str) -> str:
    """Extract chapter label from filename like C201_1A_... → Chapter 1."""
    match = re.search(r'C201_(\d)', filename)
    if match:
        return f"Chapter {match.group(1)}"
    return "Other"


files = sorted(MD_DIR.glob("*.md"))
if not files:
    print(f"No .md files found in {MD_DIR}")
    exit(1)

sessions = []
for path in files:
    content = path.read_text(encoding="utf-8")
    sessions.append({
        "id": path.stem,
        "filename": path.name,
        "chapter": get_chapter(path.name),
        "title": get_title(content, path.stem),
        "subtitle": get_subtitle(content),
        "content": content,
    })

sessions_json = json.dumps(sessions, ensure_ascii=False, indent=2)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>C201 Simplified — Preview</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 15px;
      line-height: 1.75;
      color: #1a1a1a;
      background: #eef0ee;
      display: flex;
      height: 100vh;
      overflow: hidden;
    }}

    /* ── Sidebar ── */
    #sidebar {{
      width: 260px;
      min-width: 260px;
      background: #1c2b3a;
      color: #c8d8e8;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      flex-shrink: 0;
    }}

    #sidebar-header {{
      padding: 20px 18px 14px;
      border-bottom: 1px solid #2e4257;
    }}
    #sidebar-header h1 {{
      font-size: 0.95em;
      font-weight: 700;
      color: #fff;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }}
    #sidebar-header p {{
      font-size: 0.75em;
      color: #7a9bb5;
      margin-top: 2px;
    }}

    .chapter-group {{ margin-top: 8px; }}
    .chapter-label {{
      font-size: 0.68em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: #5a7a96;
      padding: 10px 18px 4px;
    }}

    .session-btn {{
      display: block;
      width: 100%;
      text-align: left;
      background: none;
      border: none;
      cursor: pointer;
      padding: 7px 18px;
      color: #b0c8dc;
      font-size: 0.82em;
      line-height: 1.4;
      transition: background 0.15s;
    }}
    .session-btn:hover {{ background: #243546; color: #fff; }}
    .session-btn.active {{
      background: #2d4a62;
      color: #fff;
      border-left: 3px solid #c9a84c;
      padding-left: 15px;
    }}
    .session-btn .session-id {{
      font-weight: 700;
      font-size: 0.9em;
      color: #c9a84c;
      display: block;
    }}

    /* ── Content ── */
    #content-wrap {{
      flex: 1;
      overflow-y: auto;
      padding: 40px 48px;
    }}

    #content {{
      max-width: 780px;
      margin: 0 auto;
      background: #fff;
      padding: 56px 64px;
      border-radius: 4px;
      box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    }}

    /* ── Typography ── */
    #content h1 {{
      font-size: 2em;
      font-weight: 700;
      line-height: 1.2;
      margin-bottom: 4px;
      color: #111;
    }}
    #content h2 {{
      font-size: 1em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #1a5276;
      margin-top: 40px;
      margin-bottom: 12px;
      padding-bottom: 6px;
      border-bottom: 2px solid #d4e6f1;
    }}
    #content h3 {{
      font-size: 1em;
      font-weight: 600;
      margin-top: 20px;
      margin-bottom: 6px;
    }}
    #content p {{ margin-bottom: 10px; }}
    #content hr {{
      border: none;
      border-top: 1px solid #eaeaea;
      margin: 28px 0;
    }}
    #content strong {{ font-weight: 600; }}
    #content em {{ font-style: italic; }}

    /* Bible verses / block quotes */
    #content blockquote {{
      margin: 14px 0;
      padding: 14px 20px;
      background: #fdf8ee;
      border-left: 4px solid #c9a84c;
      border-radius: 0 4px 4px 0;
      font-size: 0.96em;
      color: #333;
    }}
    #content blockquote p {{ margin-bottom: 6px; }}
    #content blockquote p:last-child {{ margin-bottom: 0; }}

    /* Definition tables */
    #content table {{
      width: 100%;
      border-collapse: collapse;
      margin: 8px 0 18px;
      font-size: 0.88em;
    }}
    #content th {{
      background: #1a5276;
      color: #fff;
      text-align: left;
      padding: 7px 12px;
      font-weight: 600;
    }}
    #content td {{
      padding: 6px 12px;
      border-bottom: 1px solid #eaeaea;
      vertical-align: top;
    }}
    #content tr:nth-child(even) td {{ background: #f5f8fc; }}
    #content tr:last-child td {{ border-bottom: none; }}

    /* First table (Key Words) — slightly different header */
    #content h2:first-of-type + p + table th {{ background: #154360; }}

    /* Lists */
    #content ul, #content ol {{
      padding-left: 24px;
      margin-bottom: 10px;
    }}
    #content li {{ margin-bottom: 3px; }}

    /* Sidebar italic labels ("Definitions:") */
    #content p > em:only-child {{
      font-size: 0.8em;
      color: #999;
    }}

    /* Empty state */
    #empty {{
      display: flex;
      align-items: center;
      justify-content: center;
      height: 100%;
      color: #aaa;
      font-size: 1em;
    }}

    /* Print */
    @media print {{
      #sidebar {{ display: none; }}
      body {{ display: block; overflow: visible; }}
      #content-wrap {{ padding: 0; overflow: visible; }}
      #content {{ box-shadow: none; padding: 40px; max-width: 100%; }}
    }}
  </style>
</head>
<body>

<nav id="sidebar">
  <div id="sidebar-header">
    <h1>C201 Simplified</h1>
    <p>IELTS 3 Edition</p>
  </div>
  <div id="session-list"></div>
</nav>

<main id="content-wrap">
  <div id="content"><div id="empty">← Select a session</div></div>
</main>

<script>
const SESSIONS = {sessions_json};

// Build sidebar
const listEl = document.getElementById('session-list');
const chapters = {{}};
SESSIONS.forEach(s => {{
  if (!chapters[s.chapter]) chapters[s.chapter] = [];
  chapters[s.chapter].push(s);
}});

Object.entries(chapters).forEach(([chap, sessions]) => {{
  const group = document.createElement('div');
  group.className = 'chapter-group';
  const label = document.createElement('div');
  label.className = 'chapter-label';
  label.textContent = chap;
  group.appendChild(label);
  sessions.forEach(s => {{
    const btn = document.createElement('button');
    btn.className = 'session-btn';
    const idMatch = s.id.match(/C201_(\\d[A-Z])/);
    const idLabel = idMatch ? idMatch[1] : s.id;
    btn.innerHTML = `<span class="session-id">${{idLabel}}</span>${{s.title}}`;
    btn.dataset.id = s.id;
    btn.addEventListener('click', () => loadSession(s, btn));
    group.appendChild(btn);
  }});
  listEl.appendChild(group);
}});

// Load session
function loadSession(session, btn) {{
  document.querySelectorAll('.session-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('content').innerHTML = marked.parse(session.content);
  document.getElementById('content-wrap').scrollTop = 0;
}}

// Auto-load first session
const firstBtn = document.querySelector('.session-btn');
if (firstBtn) {{
  const firstId = firstBtn.dataset.id;
  const firstSession = SESSIONS.find(s => s.id === firstId);
  loadSession(firstSession, firstBtn);
}}
</script>
</body>
</html>"""

OUT.write_text(HTML, encoding="utf-8")
print(f"Built {OUT} with {len(sessions)} session(s):")
for s in sessions:
    print(f"  [{s['chapter']}] {s['id']} — {s['title']}")

if PUSH:
    def run(cmd):
        result = subprocess.run(cmd, cwd=BASE, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ✗ {' '.join(cmd)}\n{result.stderr.strip()}")
            return False
        return True

    session_names = ", ".join(s["id"] for s in sessions)
    msg = f"Rebuild: {len(sessions)} session(s) — {session_names}"

    print("\nDeploying to GitHub Pages...")
    ok = (
        run(["git", "add", "index.html", "C201_FM_Simplified"]) and
        run(["git", "diff", "--cached", "--quiet"]) or
        (run(["git", "commit", "-m", msg]) and run(["git", "push"]))
    )
    if ok:
        print("  ✓ Pushed — https://samuelscho92.github.io/c201-simplified/")
else:
    print("\n(Skipped git push — run without --no-push to deploy)")
