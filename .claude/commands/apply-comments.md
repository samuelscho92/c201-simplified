Fetch all Hypothes.is annotations on the C201 simplified site, apply each one using best judgment, delete them via the API, then rebuild and push.

If the argument is `case-by-case`, present each annotation one at a time and wait for approval before applying. For each annotation, show:
- **Session** — which session it's in (e.g. Session 1B)
- **Highlighted text** — the full sentence or passage that was annotated, with 1–2 sentences of surrounding context so the location is clear
- **Comment** — exactly what was written
- **Proposed change** — what you plan to do and the exact new wording, so the user can approve, adjust, or reject it

Do not apply or move to the next annotation until the user confirms.

## Arguments: $ARGUMENTS

## Hypothes.is Config
- API token: stored in `.env` as `HYPOTHESIS_TOKEN`
- API base: `https://api.hypothes.is/api`
- Site URL pattern: `https://samuelscho92.github.io/c201-simplified/*`

## Step 1 — Fetch annotations

Load the token from `.env` first:

```bash
export $(grep -v '^#' .env | xargs)
```

Then fetch:

```bash
curl -s "https://api.hypothes.is/api/search?wildcard_uri=https://samuelscho92.github.io/c201-simplified/*&user=acct:samuelscho92@hypothes.is&limit=50" \
  -H "Authorization: Bearer $HYPOTHESIS_TOKEN"
```

Each annotation has:
- `id` — needed for deletion
- `text` — the comment left by the user
- `target[0].selector` — includes a `TextQuoteSelector` with `exact` (the highlighted text) and `prefix`/`suffix` (surrounding context)
- `uri` — the session page URL (e.g. `.../sessions/C201_1B_Seeing_Myself.html`)

## Step 2 — Map to markdown files

Extract the session ID from the URI:
- `…/sessions/C201_1B_Seeing_Myself.html` → `C201_FM_Simplified/C201_1B_Seeing_Myself.md`

## Step 3 — Apply each annotation

For each annotation, read the relevant markdown file and apply the comment using best judgment:

- **Wording change requests** ("use X instead", "something more like…") → rewrite the highlighted sentence/phrase as instructed
- **Remove requests** ("remove this", "delete this") → remove the highlighted text or element
- **Add requests** ("add an example", "add X before Y") → insert the requested content in the right place
- **Clarification requests** ("is this clear?", "does X make sense?") → rewrite for clarity at IELTS 3 level
- **Question rewrites** → rewrite the discussion question as requested

Always preserve IELTS 3 level English. Do not change anything outside the scope of each annotation.

## Step 4 — Delete annotations

After all edits are applied, delete every annotation via the API:

```bash
curl -s -X DELETE "https://api.hypothes.is/api/annotations/{id}" \
  -H "Authorization: Bearer $HYPOTHESIS_TOKEN"
```

## Step 5 — Rebuild and push

```bash
python3.11 rebuild_preview.py
```

## Step 6 — Report back

List every annotation that was applied with:
- The session it was in
- The highlighted text
- What change was made
