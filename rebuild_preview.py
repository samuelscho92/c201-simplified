#!/usr/bin/env python3
"""
Rebuilds sessions/*.html and index.html from all .md files in C201_FM_Simplified/,
then commits and pushes to GitHub Pages.

Usage:
    python3.11 rebuild_preview.py           # build + commit + push
    python3.11 rebuild_preview.py --no-push # build only, no git
"""

import re
import sys
import subprocess
from pathlib import Path

try:
    import markdown as mdlib
except ImportError:
    print("Missing dependency: pip3.11 install markdown")
    exit(1)

BASE = Path(__file__).parent
MD_DIR = BASE / "C201_FM_Simplified"
SESSIONS_DIR = BASE / "sessions"
OUT = BASE / "index.html"
PUSH = "--no-push" not in sys.argv


def render_md(text):
    return mdlib.markdown(text, extensions=["tables", "sane_lists"])


def get_title(content, filename):
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else filename.replace("_", " ").replace(".md", "")


def get_chapter(filename):
    match = re.search(r'C201_(\d)', filename)
    return f"Chapter {match.group(1)}" if match else "Other"


def get_pdf_path(session_id):
    m = re.search(r'C201_(\d)([A-Z])', session_id)
    if m:
        return f"../C201_Source_PDFs/Ch{m.group(1)}/C201_{m.group(1)}{m.group(2)}_Booklet.pdf"
    return ""


# ── Load sessions ──────────────────────────────────────────────────────────
files = sorted(MD_DIR.glob("*.md"))
if not files:
    print(f"No .md files found in {MD_DIR}")
    exit(1)

sessions = []
for path in files:
    content = path.read_text(encoding="utf-8")
    sid = path.stem
    sessions.append({
        "id": sid,
        "chapter": get_chapter(path.name),
        "title": get_title(content, sid),
        "html": render_md(content),
        "pdf": get_pdf_path(sid),
    })

SESSIONS_DIR.mkdir(exist_ok=True)


# ── Sidebar ────────────────────────────────────────────────────────────────
def build_sidebar(current_id):
    chapters = {}
    for s in sessions:
        chapters.setdefault(s["chapter"], []).append(s)

    out = ""
    for ch, items in chapters.items():
        out += f'<div class="chapter-group"><div class="chapter-label">{ch}</div>'
        for s in items:
            m = re.search(r'C201_(\d[A-Z])', s["id"])
            label = m.group(1) if m else s["id"]
            cls = "session-btn active" if s["id"] == current_id else "session-btn"
            out += (
                f'<a href="{s["id"]}.html" class="{cls}">'
                f'<span class="session-id">{label}</span>{s["title"]}</a>'
            )
        out += "</div>"
    return out


# ── Page template ──────────────────────────────────────────────────────────
CSS = """
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 15px;
      line-height: 1.75;
      color: #1a1a1a;
      background: #eef0ee;
      display: flex;
      height: 100vh;
      overflow: hidden;
    }

    /* ── Sidebar ── */
    #sidebar {
      width: 260px;
      min-width: 260px;
      background: #1c2b3a;
      color: #c8d8e8;
      display: flex;
      flex-direction: column;
      overflow-y: auto;
      flex-shrink: 0;
      transition: width 0.2s ease, min-width 0.2s ease;
    }
    #sidebar.collapsed {
      width: 48px;
      min-width: 48px;
      overflow: hidden;
    }
    #sidebar.collapsed .chapter-group,
    #sidebar.collapsed #sidebar-header h1,
    #sidebar.collapsed #sidebar-header p {
      display: none;
    }

    #sidebar-header {
      padding: 20px 18px 14px;
      border-bottom: 1px solid #2e4257;
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 8px;
    }
    #sidebar.collapsed #sidebar-header {
      padding: 14px 0;
      justify-content: center;
      border-bottom: none;
    }
    #sidebar-header h1 {
      font-size: 0.95em;
      font-weight: 700;
      color: #fff;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }
    #sidebar-header p {
      font-size: 0.75em;
      color: #7a9bb5;
      margin-top: 2px;
    }

    #collapse-btn {
      background: none;
      border: none;
      cursor: pointer;
      color: #5a7a96;
      padding: 2px;
      flex-shrink: 0;
      line-height: 0;
      transition: color 0.15s;
    }
    #collapse-btn:hover { color: #fff; }

    .chapter-group { margin-top: 8px; }
    .chapter-label {
      font-size: 0.68em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: #5a7a96;
      padding: 10px 18px 4px;
    }

    .session-btn {
      display: block;
      width: 100%;
      text-align: left;
      text-decoration: none;
      padding: 7px 18px;
      color: #b0c8dc;
      font-size: 0.82em;
      line-height: 1.4;
      transition: background 0.15s;
    }
    .session-btn:hover { background: #243546; color: #fff; }
    .session-btn.active {
      background: #2d4a62;
      color: #fff;
      border-left: 3px solid #c9a84c;
      padding-left: 15px;
    }
    .session-btn .session-id {
      font-weight: 700;
      font-size: 0.9em;
      color: #c9a84c;
      display: block;
    }
    .session-btn.active .session-id { color: #e8c96a; }

    /* ── Main area ── */
    #main {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    /* ── Toolbar ── */
    #toolbar {
      display: flex;
      align-items: center;
      justify-content: flex-end;
      padding: 8px 16px;
      background: #f5f6f4;
      border-bottom: 1px solid #dde0da;
      flex-shrink: 0;
    }

    #toggle-btn {
      display: flex;
      align-items: center;
      gap: 7px;
      padding: 6px 14px;
      border-radius: 6px;
      border: 1px solid #c5c9c2;
      background: #fff;
      color: #444;
      font-size: 0.8em;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.15s, border-color 0.15s;
      letter-spacing: 0.02em;
    }
    #toggle-btn:hover { background: #eef0ee; border-color: #aaa; }
    #toggle-btn.active {
      background: #1c2b3a;
      color: #fff;
      border-color: #1c2b3a;
    }
    #toggle-btn svg { flex-shrink: 0; }

    /* ── Split view ── */
    #split-wrap {
      flex: 1;
      display: flex;
      overflow: hidden;
    }

    #pdf-pane {
      flex: 1;
      display: none;
      border-right: 2px solid #c9a84c;
      background: #555;
      overflow: hidden;
    }
    #pdf-pane.visible { display: flex; flex-direction: column; }

    #pdf-label {
      padding: 6px 14px;
      background: #3a3a3a;
      color: #c9a84c;
      font-size: 0.72em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      flex-shrink: 0;
    }

    #pdf-frame {
      flex: 1;
      width: 100%;
      border: none;
    }

    /* ── Simplified pane ── */
    #content-wrap {
      flex: 1;
      overflow-y: auto;
      padding: 40px 48px;
      min-width: 0;
    }

    #content {
      max-width: 780px;
      margin: 0 auto;
      background: #fff;
      padding: 56px 64px;
      border-radius: 4px;
      box-shadow: 0 2px 16px rgba(0,0,0,0.07);
    }

    body.split-mode #content-wrap { padding: 24px 28px; }
    body.split-mode #content { padding: 36px 40px; }

    /* ── Typography ── */
    #content h1 {
      font-size: 2em;
      font-weight: 700;
      line-height: 1.2;
      margin-bottom: 4px;
      color: #111;
    }
    #content h2 {
      font-size: 1em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #1a5276;
      margin-top: 40px;
      margin-bottom: 12px;
      padding-bottom: 6px;
      border-bottom: 2px solid #d4e6f1;
    }
    #content h3 {
      font-size: 1em;
      font-weight: 600;
      margin-top: 20px;
      margin-bottom: 6px;
    }
    #content p { margin-bottom: 10px; }
    #content hr {
      border: none;
      border-top: 1px solid #eaeaea;
      margin: 28px 0;
    }
    #content strong { font-weight: 600; }
    #content em { font-style: italic; }

    #content blockquote {
      margin: 14px 0;
      padding: 14px 20px;
      background: #fdf8ee;
      border-left: 4px solid #c9a84c;
      border-radius: 0 4px 4px 0;
      font-size: 0.96em;
      color: #333;
    }
    #content blockquote p { margin-bottom: 6px; }
    #content blockquote p:last-child { margin-bottom: 0; }

    #content table {
      width: 100%;
      border-collapse: collapse;
      margin: 8px 0 18px;
      font-size: 0.88em;
    }
    #content th {
      background: #1a5276;
      color: #fff;
      text-align: left;
      padding: 7px 12px;
      font-weight: 600;
    }
    #content td {
      padding: 6px 12px;
      border-bottom: 1px solid #eaeaea;
      vertical-align: top;
    }
    #content tr:nth-child(even) td { background: #f5f8fc; }
    #content tr:last-child td { border-bottom: none; }

    #content ul, #content ol {
      padding-left: 24px;
      margin-bottom: 10px;
    }
    #content li { margin-bottom: 3px; }

    #content p > em:only-child {
      font-size: 0.8em;
      color: #999;
    }

    /* ── Giscus ── */
    #giscus-section {
      max-width: 780px;
      margin: 24px auto 40px;
    }
    #giscus-section h3 {
      font-size: 0.75em;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: #5a7a96;
      margin-bottom: 12px;
      padding-bottom: 6px;
      border-bottom: 1px solid #dde0da;
    }

    /* ── Print ── */
    @media print {
      #sidebar, #toolbar, #pdf-pane, #giscus-section { display: none !important; }
      body { display: block; overflow: visible; }
      #content-wrap { padding: 0; overflow: visible; }
      #content { box-shadow: none; padding: 40px; max-width: 100%; }
    }
"""

JS = """
// Sidebar collapse
const collapseBtn = document.getElementById('collapse-btn');
const collapseIcon = document.getElementById('collapse-icon');
const sidebar = document.getElementById('sidebar');
const expandPath = '<path d="M11 4L6 9L11 14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>';
const collapsePath = '<path d="M7 4L12 9L7 14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>';

collapseBtn.addEventListener('click', () => {
  const collapsed = sidebar.classList.toggle('collapsed');
  collapseIcon.innerHTML = collapsed ? collapsePath : expandPath;
  collapseBtn.title = collapsed ? 'Expand sidebar' : 'Collapse sidebar';
});

// PDF split toggle
const toggleBtn = document.getElementById('toggle-btn');
const pdfPane = document.getElementById('pdf-pane');
const pdfFrame = document.getElementById('pdf-frame');
let pdfLoaded = false;

toggleBtn.addEventListener('click', () => {
  const active = pdfPane.classList.toggle('visible');
  toggleBtn.classList.toggle('active', active);
  document.body.classList.toggle('split-mode', active);
  if (active && !pdfLoaded && PDF_PATH) {
    pdfFrame.src = PDF_PATH;
    pdfLoaded = true;
  }
});
"""


def build_page(session):
    nav = build_sidebar(session["id"])
    pdf = session["pdf"]
    content = session["html"]
    title = session["title"]
    sid = session["id"]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — C201 Simplified</title>
  <script async src="https://hypothes.is/embed.js"></script>
  <style>{CSS}</style>
</head>
<body>

<nav id="sidebar">
  <div id="sidebar-header">
    <div>
      <h1>C201 Simplified</h1>
      <p>IELTS 3 Edition</p>
    </div>
    <button id="collapse-btn" title="Collapse sidebar">
      <svg id="collapse-icon" width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M11 4L6 9L11 14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </div>
  <div id="session-list">{nav}</div>
</nav>

<div id="main">
  <div id="toolbar">
    <button id="toggle-btn" title="Toggle side-by-side with source PDF">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="1" y="2" width="6" height="12" rx="1" stroke="currentColor" stroke-width="1.5"/>
        <rect x="9" y="2" width="6" height="12" rx="1" stroke="currentColor" stroke-width="1.5"/>
      </svg>
      Compare with Source
    </button>
  </div>

  <div id="split-wrap">
    <div id="pdf-pane">
      <div id="pdf-label">Source PDF</div>
      <iframe id="pdf-frame" title="Source PDF"></iframe>
    </div>
    <div id="content-wrap">
      <div id="content">{content}</div>
      <div id="giscus-section">
        <h3>Session Notes</h3>
        <div id="giscus-container"></div>
      </div>
    </div>
  </div>
</div>

<script>
const PDF_PATH = '{pdf}';

{JS}

// Giscus
(function() {{
  const s = document.createElement('script');
  s.src = 'https://giscus.app/client.js';
  s.setAttribute('data-repo', 'samuelscho92/c201-simplified');
  s.setAttribute('data-repo-id', 'R_kgDOSkR22Q');
  s.setAttribute('data-category', 'General');
  s.setAttribute('data-category-id', 'DIC_kwDOSkR22c4C9oLp');
  s.setAttribute('data-mapping', 'specific');
  s.setAttribute('data-term', '{sid}');
  s.setAttribute('data-reactions-enabled', '1');
  s.setAttribute('data-emit-metadata', '0');
  s.setAttribute('data-input-position', 'top');
  s.setAttribute('data-theme', 'light');
  s.setAttribute('data-lang', 'en');
  s.crossOrigin = 'anonymous';
  s.async = true;
  document.getElementById('giscus-container').appendChild(s);
}})();
</script>
</body>
</html>"""


# ── Build ──────────────────────────────────────────────────────────────────
for session in sessions:
    out_path = SESSIONS_DIR / f"{session['id']}.html"
    out_path.write_text(build_page(session), encoding="utf-8")

# index.html redirects to first session
first_id = sessions[0]["id"]
OUT.write_text(f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=sessions/{first_id}.html">
  <title>C201 Simplified</title>
</head>
<body>
  <p>Redirecting... <a href="sessions/{first_id}.html">Click here</a></p>
</body>
</html>""", encoding="utf-8")

print(f"Built {len(sessions)} session(s) in sessions/:")
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
        run(["git", "add", "index.html", "sessions", "C201_FM_Simplified", "rebuild_preview.py"]) and
        run(["git", "diff", "--cached", "--quiet"]) or
        (run(["git", "commit", "-m", msg]) and run(["git", "push"]))
    )
    if ok:
        print("  ✓ Pushed — https://samuelscho92.github.io/c201-simplified/")
else:
    print("\n(Skipped git push — run without --no-push to deploy)")
