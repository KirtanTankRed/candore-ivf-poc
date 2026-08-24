# IVF Report Summary POC — Tech Stack & Execution Plan

Builds on `requirement.txt`, `Domain Knowledge.pdf`, `project planning and execution.txt`,
and the analysis in `docs/reference docs/for-llm/` (ivf-domain-knowledge.md,
sample-reports-analysis.md). This doc records the chosen stack and turns the original
6-phase plan into concrete steps for this stack.

## Tech Stack (decided)

| Layer | Choice | Why |
|---|---|---|
| Backend | Python 3 + FastAPI | Best-fit ecosystem if any PDF/image preprocessing (PyMuPDF, pdf2image) is needed later; async-friendly for calling the LLM API |
| Frontend | Vite + React (TypeScript), minimal SPA | Single upload page, no routing/state libraries needed for V1 |
| Document understanding + summarization | Claude API (Anthropic), sent the PDF/image directly | No separate OCR step for V1 — this conversation already validated that Claude reads dense lab tables, hand-highlighter marks, and glare-y phone photos from these exact sample reports accurately. One LLM call per report instead of an OCR→text→LLM pipeline. |
| Storage | None | Files handled transiently per-request; summary returned in the response body; nothing persisted server-side (per plan doc: "No database unless needed") |
| Deployment | Vercel | Frontend as static build; backend as Python Serverless Function(s) under `/api` (Vercel's standard FastAPI pattern — single ASGI entrypoint + `vercel.json` rewrites) |

### Known constraints to validate early (don't assume — check against current Vercel docs/skill before it blocks you)
- **Request body size limit** on Vercel Functions — one sample PDF in our set is ~1.5MB; confirm this is comfortably under whatever the current limit is before building around direct multipart upload to the function.
- **Execution time limit** — an LLM call over a multi-page PDF plus network latency could approach default serverless timeouts on lower tiers; confirm current limits.
- **Ephemeral filesystem** (`/tmp` only, cleared between invocations) — fine for this design since nothing is persisted, but don't assume any local file survives across requests.
- Use the `vercel:vercel-functions` skill / current docs when actually wiring the Python function, rather than relying on older assumptions about Vercel's Python support.

### Explicitly out of scope for V1 (per requirement.txt / plan doc)
No Google Drive integration, no auth, no database, no patient portal, no dashboard, no
automated clinical recommendations, no cross-report/longitudinal tracking (even though
[[ivf-domain-knowledge]]'s antenatal section notes trends-across-visits are valuable
clinically — that's a natural V2, not V1). Also considered and deferred: streaming the
summary response token-by-token instead of returning it as one JSON blob — evaluated as
~1hr of contained work (Anthropic SDK + FastAPI `StreamingResponse` + Vercel's Python
runtime all support it), but not worth the UX gain for a POC.

## Execution Plan

### Phase 0 — Foundations (done)
- Domain knowledge captured → `for-llm/ivf-domain-knowledge.md`
- Client sample reports analyzed → `for-llm/sample-reports-analysis.md`
- Requirements captured → `requirement.txt`
- Tech stack decided → this doc

### Phase 1 — Project scaffold ✅ done
- `backend/`: FastAPI skeleton, Anthropic Python SDK wired, `.env` for `ANTHROPIC_API_KEY` (never exposed to frontend, supplied by Kirtan directly — see [[feedback-no-secrets-access]])
- `frontend/`: Vite + React + TS scaffold
- `.gitignore` covering `.env`, `node_modules`, `__pycache__`, `secret/`, etc.
- Deferred to Phase 5: Vercel project link + `vercel.json` routing (static frontend + `/api` Python function) — not needed until actual deploy.

### Phase 2 — Core loop: Upload → Extract → Summarize → Display ✅ backend+frontend built, smoke-tested
Matches requirement.txt's Core Flow exactly.
- Backend `POST /api/summarize`: accept multipart file (pdf/jpg/jpeg/png, plus txt/md for
  labs that export plain-text or Markdown reports), validate type, forward file bytes
  directly to Claude with an extraction+summary prompt, return structured summary.
- Prompt/schema for the LLM call should be built directly from what's already documented:
  - The **priority field list** in `ivf-domain-knowledge.md` (pre-IVF panel fields +
    pregnancy/antenatal priority fields) — tells the model what to look for depending on
    report type.
  - The **cross-cutting extraction rules** in `sample-reports-analysis.md`: drop
    boilerplate/methodology/marketing pages, respect conditional reference ranges (e.g.
    Prolactin pregnant vs non-pregnant), prefer the lab's own printed interpretation/flags
    over re-deriving normal/abnormal from raw numbers, never infer legally-withheld info
    (e.g. fetal sex under PC-PNDT).
  - "Do not make unsupported clinical conclusions" (requirement.txt #2) as an explicit
    system-prompt constraint.
- Frontend: file picker → submit → side-by-side view of the uploaded report (PDF/image
  preview) and the generated summary; loading + error states (bad file type, oversized
  file, LLM/network failure).

**Status:** built and smoke-tested end-to-end via `curl` against a real sample report
(Priyal Kalthiya's CBC report) — Claude correctly flagged the low Hb/microcytic pattern
and correctly noted the lab printed no narrative interpretation line. Both dev servers
run locally (`backend` on :8000, `frontend` on :5173) and CORS between them verified.
**Not yet done:** an actual human click-through of the browser UI — no browser automation
tool is available in this environment, so Kirtan should open http://localhost:5173,
upload a couple of the sample reports himself, and confirm the preview/summary panels
look and behave as expected before this phase is considered fully closed.

### Phase 3 — Validation against the real sample reports
Use the actual client-provided reports catalogued in `sample-reports-analysis.md` — 4
distinct patients, both clean digital PDFs and phone-photographed/highlighted variants:
- Mital Janak Ghevariya — InsighT NIPS report
- Tinkal Divyang Sangani — First-Trimester Combined Screening
- Priyal Kalthiya — CBC+RBS, and TSH+Prolactin
- Nisha Nath Yogi — Hemoglobin Electrophoresis (photo-only source)

For each, run the requirement.txt Validation checklist: extraction accuracy, missing
information, hallucinated/incorrect information, summary readability, usefulness to a
practitioner. Specifically stress-test the photographed/highlighted images — glare, skew,
pen marks — as the OCR-robustness case requirement.txt #5 calls for.

### Phase 4 — Practitioner feedback loop
- Get the summaries reviewed by an IVF practitioner (Dr. Jaydev Dhameliya is the referring
  doctor across every sample report, so a natural first reviewer if available).
- Ask: what's missing, what's unnecessary, what should be first, what makes it clinically
  useful.
- Refine prompt/schema, retest against Phase 3's sample set.

### Phase 5 — Deploy & wrap up POC

**Deployment architecture (decided):** Vercel **Services** — `backend/` (FastAPI,
entrypoint `app.main:app`) and `frontend/` (Vite static build) as two services in one
project/domain, routed via root `vercel.json` (`/api/*` → backend, everything else →
frontend). Same-origin in production, so CORS is moot there; `VITE_API_BASE_URL` stays
unset in prod and calls fall back to relative `/api/summarize`.

Before actually deploying:
- **API usage fencing — ✅ decided.** Kirtan is setting rate/spend limits directly on the
  API key in the Anthropic Console rather than building app-level rate limiting — this is
  a manual step on his end, confirm it's actually done before the link goes public. The
  backend's existing 10MB file-size cap remains as a secondary guard.
- **CEO review — happens post-deploy**, on the live deployed link rather than a local
  demo. Not a pre-deploy blocker — deploying is the mechanism that produces the artifact
  for review. After deploying, that's the checkpoint to loop the CEO in. Wider external
  sharing (client/practitioner) beyond that internal review is a separate, later step.
- Set the required env vars in the Vercel project (not committed anywhere): `ANTHROPIC_API_KEY`,
  `CLAUDE_MODEL`, `CLAUDE_MAX_TOKENS`, `MAX_FILE_SIZE_MB`. `ALLOWED_ORIGIN`/CORS becomes
  irrelevant once same-origin in production.
- Deploy to Vercel, verify the end-to-end flow on the hosted link (not just localhost).
- Confirm basic error handling covers bad file type, oversized file, and LLM/API failure.
- Check against the POC Success Criteria in requirement.txt: *"A doctor should be able to
  quickly understand the important information in the IVF report without reading the
  entire report."*

## Known gaps to flag to the client (carried over from sample-reports-analysis.md)
- All 4 sample patients are female / pregnancy-related — no male-partner report (semen
  analysis, male hormonal profile) was provided, so that extraction path is untested.
- No classic ovarian-reserve panel (AMH/FSH/LH) report was provided either.
