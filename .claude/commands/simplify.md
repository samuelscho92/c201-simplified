Simplify a C201 session PDF into an IELTS 3 markdown file, then deploy.

The argument is a session ID like `2A`, `2B`, `3C`, etc. If no argument is given, ask which session to process.

## Your Task

1. **Find the source PDF** in `C201_Source_PDFs/Ch{N}/C201_{ID}_Booklet.pdf` — where N is the chapter number and ID is the session ID (e.g. `C201_Source_PDFs/Ch2/C201_2A_Booklet.pdf`).

2. **Read the PDF** using the Read tool.

3. **Write the simplified markdown file** to `C201_FM_Simplified/C201_{ID}_{Title}.md` following all requirements in CLAUDE.md exactly:
   - IELTS Level 3 English (A2 — very basic vocabulary, short sentences, one idea per sentence)
   - Start with a Key Words table
   - Convert all Bible verses to NLT
   - Simplify or remove quotes that are too complex; note *(Simplified from original)*
   - Add definition tables (with superscripts) after any Bible verse or quote containing hard words
   - Use *Example:* blocks for abstract concepts
   - Keep opening hymns as-is with a "What this means:" summary below
   - End with Discussion Questions

4. **Run the deploy command:**
   ```bash
   python3 rebuild_preview.py
   ```

5. **Report back** with:
   - The session title and file path written
   - Any content decisions made (quotes removed, examples added, etc.)
   - Confirmation that deploy succeeded

## Session ID: $ARGUMENTS
