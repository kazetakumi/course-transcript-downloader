---
labels: [wayfinder:map]
tracker: local-markdown
---

# MIT OpenCourseWare course-downloader skill

## Destination

A **working Claude Code skill**, living in this `mit-course-transcript-downloader`
repo, that — given a **topic/keyword**, an **MIT course number/title**, or a
**direct MIT OCW URL** — discovers the relevant **MIT OpenCourseWare** course
*that actually has video transcripts*, and downloads its **video transcripts**,
**lecture notes / slides / PDFs**, and **problem sets / assignments / exams**
into an organized folder inside this repo. Pure fetch-and-organize.

**Map done =** the skill runs end-to-end and has been **verified against at least
one real OCW course** — not merely a locked design.

## Notes

- **Execution override.** This map is *not* planning-only. Its final tickets
  build and test the real skill. The destination is a running, verified skill.
- **Domain:** MIT OpenCourseWare (`ocw.mit.edu`) only.
- **Skills to consult:** `/grilling` + `/domain-modeling` for HITL tickets;
  `/research` for the AFK research tickets; `/prototype` for shape/UX tickets;
  `/write-a-skill` when the build fog graduates into authoring `SKILL.md`.
- **Tracker:** local-markdown — see `.wayfinder/README.md`.

## Decisions so far

<!-- one line per closed ticket; zoom the link for detail -->

- [Map how OCW serves content & detect transcripts](tickets/001-map-ocw-content-structure-and-transcript-availability.md) — MIT Learn API (`api.learn.mit.edu`): resolve → run id → paginate `contentfiles?run_id=`; raw files scraped from resource pages; transcripts detected by caption ext **or** `*transcript*.pdf`. Findings in [asset 001](assets/001-ocw-structure.md).
- [Discover / resolve topic·number·URL](tickets/002-course-discovery-and-resolution.md) — search via `learning_resources_search`, numbers via exact course-number match, URLs via slug; **resolve-then-warn** rather than guaranteeing transcripts at search time. Findings in [asset 002](assets/002-ocw-discovery.md).
- [Resolution UX](tickets/003-resolution-ux.md) — topics → present candidates & confirm (never auto-pick); numbers/URLs → resolve + quick confirm; no-transcript course → warn and offer alternatives.
- [Download strategy & tooling](tickets/004-download-strategy-and-tooling.md) — per-file (no reliable bulk zip); pure Python stdlib; two-pass: video pages → per-video transcripts, then notes/psets/exams; retries + idempotent skip; non-English captions routed aside.
- [Output layout & transcript format](tickets/005-output-layout-and-transcript-format.md) — `courses/<slug>/{transcripts,lecture-notes,problem-sets,exams,other}/` + `README.md` + `manifest.json`; captions kept native **and** cleaned to `.txt`.

**Destination reached.** The skill lives at
[`.claude/skills/mit-ocw-downloader/`](../.claude/skills/mit-ocw-downloader/SKILL.md)
(bundled engine `ocw_download.py`). Verified end-to-end against three contrasting
real courses: 18.06SC (80 English transcripts + 24 translated, 43 notes, 62
psets, 8 exams — counts verified against disk), 18.06 2010
(39 PDF transcripts, archive.org era), 24.200 Ancient Philosophy (notes-only →
correctly warns "no transcripts").

## Not yet specified

_(empty — the way to the destination is fully walked.)_

## Possible future work (beyond this destination)

- Optional `yt-dlp` caption fallback for videos whose page lacks a transcript.
- A `--languages` flag to opt into non-English translated captions.
- Politeness knobs (configurable rate-limit/concurrency) for very large courses.

## Out of scope

- **AI-generated study notes / summaries** from the transcripts — download MIT's
  material only, no synthesis stage.
- **Lecture video file downloads** — transcripts stand in for the video.
- **Non-MIT sources** (YouTube, edX, Coursera, arbitrary URLs) — MIT OCW only.
