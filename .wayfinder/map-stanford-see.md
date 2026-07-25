---
labels: [wayfinder:map]
tracker: local-markdown
---

# Extend course-downloader to Stanford Engineering Everywhere

## Destination

A **generalized, multi-institution course-downloader skill** — expanding the
existing `mit-ocw-downloader` — that, given a **topic/keyword**, a **course
number/title**, or a **direct course URL**, discovers matching courses across
**MIT OpenCourseWare** (`ocw.mit.edu`) *and* **Stanford Engineering Everywhere**
(`see.stanford.edu`), presents cross-institution topic results as a **single
table labeled by institution**, and downloads each course's **video
transcripts**, **lecture notes/slides**, and **problem sets/assignments/exams**
into the existing `courses/<slug>/` layout. The skill (and this repo) are
renamed to something institution-agnostic once the shape is settled.

**Map done =** the renamed skill runs end-to-end for **both** institutions, a
combined topic search returns a single institution-labeled table, and it has
been **verified against at least one real SEE course** end-to-end (in addition
to the MIT courses already verified by the prior effort) — not merely a locked
design.

## Notes

- **Prior effort.** This repo already carries a *completed* map —
  [`.wayfinder/map.md`](map.md) — for the MIT-only version, which explicitly
  scoped "non-MIT sources" out. This map **redraws that boundary**, opened only
  to Stanford SEE. Treat the old map as historical baseline; don't edit it.
- **Domain:** `ocw.mit.edu` (existing) + `see.stanford.edu` (new). **Not**
  Stanford Online / edX Stanford MOOCs — see Out of scope.
- **Execution override.** Like the prior map, this one is not planning-only —
  its final tickets build and verify the real, renamed, working skill.
- **Skills to consult:** `/grilling` + `/domain-modeling` for HITL tickets;
  `/research` for the AFK research ticket; `/prototype` for UX/shape questions;
  the existing `.claude/skills/mit-ocw-downloader/ocw_download.py` as the
  reference architecture to extend.
- **Tracker:** local-markdown. Tickets for *this* map use a `stanford-` filename
  prefix in `.wayfinder/tickets/` to avoid colliding with the original map's
  `001`–`005` ids.
- **Renaming the GitHub repo** is a hard-to-reverse, shared-system action —
  confirm explicitly with the user immediately before executing it, regardless
  of ticket-claim status.

## Decisions so far

<!-- one line per closed ticket; zoom the link for detail -->

- [Map how SEE serves course content & detect materials availability](tickets/stanford-001-map-see-content-structure-and-transcript-availability.md) — no API, fixed 9-course catalog (10th, LOGIC, is externally hosted → out of scope); every sampled course has HTML+PDF transcripts for every lecture; materials-slug and CamelCase course-title are non-derivable, must be scraped per course; bulk `AllMaterials.zip` exists per course; no slug-collision risk with MIT; sitewide CC BY-NC-SA 4.0. Findings in [asset stanford-001](assets/stanford-001-see-structure.md).
- [Discover & resolve SEE courses, merged with MIT results into one combined table](tickets/stanford-002-discover-and-resolve-see-courses.md) — substring match against the hardcoded catalog; combined table = MIT hits then SEE hits, both tagged; materials-slug/title/lecture-numbers all resolved in one page-scrape at resolve time.
- [Decide the combined MIT+SEE resolution UX](tickets/stanford-003-resolution-ux.md) — existing present-and-confirm flow reused unchanged; no-transcripts warning stays honest per-course rather than assumed; SEE's CC BY-NC-SA NonCommercial licensing noted in `SKILL.md` for the agent to mention.
- [Decide the download strategy and tooling for SEE materials](tickets/stanford-004-download-strategy-and-tooling.md) — per-file (bulk zip skipped); transcript PDF kept native + HTML cleaned to `.txt`; found and fixed a Windows-1252 encoding bug during verification; retry/`--force` logic reused unchanged.
- [Decide whether courses/<slug>/ needs institution labeling](tickets/stanford-005-output-layout.md) — no folder namespacing needed (no collision risk); added an `institution` field to `manifest.json` and README instead.
- [Rename the skill directory, SKILL.md, and the GitHub repo](tickets/stanford-006-rename-skill-and-repo.md) — `mit-ocw-downloader` → `ocw-downloader`; GitHub repo `mit-course-transcript-downloader` → `course-transcript-downloader` (executed, remote confirmed updated).
- [Build the unified engine and verify end-to-end against a real SEE course](tickets/stanford-007-build-and-verify.md) — built and verified against Stanford SEE's CS223A (Introduction to Robotics): 16/16 transcripts, 8 handouts, 6 problem sets, 0 exams (correctly none), 0 errors — matches research exactly.
- [Add Stanford course-microsite support (CS336) via vendored yttdl](tickets/stanford-008-microsite-course-support.md) — **post-destination addition**, done live through direct conversation rather than the formal chart-the-map flow (see the ticket's process note). Added a third source — individual Stanford course microsites, hand-curated registry, transcripts-only via YouTube captions (vendored `yttdl`, needs `uv`). Verified against CS336: 17/17 transcripts, 0 errors.

**Destination reached.** The skill lives at
[`.claude/skills/ocw-downloader/`](../.claude/skills/ocw-downloader/SKILL.md)
(bundled engine `ocw_download.py`, shared between both institutions). Combined
search/resolve/download verified for MIT (regression-checked, unaffected) and
Stanford SEE (CS223A, full counts matched). Changes are in this session's
working tree, uncommitted — awaiting the user's review before committing.

## Not yet specified

_(empty — the way to the destination is fully walked.)_

## Possible future work (beyond this destination)

- Verify the remaining 5 unchecked SEE courses (CS106B, CS107, EE261, EE263,
  EE364B) actually have transcripts too — 100% held across the 4 sampled +
  the 1 built-and-verified, but not exhaustively confirmed.
- A `--languages` flag (inherited idea from the original MIT map) doesn't
  apply to SEE (no translated captions observed there).

## Out of scope

- **LOGIC — Stanford Introduction to Logic**, listed on SEE's catalog page but
  actually hosted at `intrologic.stanford.edu` under different licensing —
  not part of SEE's own infrastructure. See
  [stanford-001](tickets/stanford-001-map-see-content-structure-and-transcript-availability.md).
- **Stanford Online / edX Stanford courses** (`online.stanford.edu`,
  `edx.org/school/stanfordonline`) — paid/audit MOOCs, not open-licensed
  downloadable materials. Only Stanford **Engineering Everywhere** is in scope
  for "Stanford" here.
- **Any other non-MIT, non-SEE source** (YouTube, Coursera, arbitrary
  universities) — inherited from the original map.
- **AI-generated study notes/summaries** and **lecture video file downloads** —
  inherited from the original map.
