---
id: stanford-008
title: Add Stanford course-microsite support (CS336) via vendored yttdl
type: task
mode: HITL
status: closed
assignee: claude
blocked_by: []
parent: map-stanford-see
---

## Question

**Process note first:** this ticket was not charted through the formal
"chart the map" flow (no destination-naming or breadth-first fog-mapping
session) — it was built live, through direct back-and-forth with the user
while testing the already-completed map's skill against a real query
("large language models"). That conversation functioned as an ad-hoc grilling
session (one question at a time, user confirming each step), so it's recorded
here after the fact rather than planned in advance. Flagging this explicitly
so the map stays an honest record of how the work actually happened.

**What happened:** the user tested `search "large language models"` and
asked why it missed `online.stanford.edu/courses/cs336-language-modeling-scratch`
(Stanford's CS336). Investigation found:
- That URL is Stanford Online's paid enrollment page — correctly out of
  scope per this map's existing "Out of scope" section.
- But the course's real free materials live on `cs336.stanford.edu` +
  `github.com/stanford-cs336` — a **third pattern**, distinct from both SEE
  and Stanford Online: an individual course microsite with no catalog, no
  shared structure with other courses, and (crucially) transcripts sourced
  from **YouTube captions**, not a native transcript file.
- The user supplied their own existing tool,
  `github.com/kazetakumi/ytube-transcript-downloader` (`yttdl`), for YouTube
  caption extraction (yt-dlp + browser impersonation + optional proxies,
  anti-IP-ban), and directed vendoring it in and extending Stanford coverage.

## Resolution

1. **Vendored `yttdl`** into `.claude/skills/ocw-downloader/yttdl/` (`.git`
   stripped, copied as plain source — its own `.gitignore` already excludes
   `.venv`, confirmed via `git add --dry-run`). Chose **`uv`** over `pip`
   after discussion: `yttdl` already ships `uv_build` + a committed
   `uv.lock`, `uv` was already installed locally at the exact pinned version,
   and `uv run` needs no persistent venv-activation state across invocations.
   This makes `uv` a hard requirement, but **only** for this microsite path —
   MIT and SEE remain pure stdlib.
2. **Added `MICROSITE_CATALOG`** to `ocw_download.py` — a hand-curated
   registry (currently one entry: CS336), explicitly *not* a search/API
   integration, since individual Stanford course sites have no shared catalog
   to query. Deliberately scoped to **transcripts only** — slides/assignments
   live in a per-course GitHub repo with its own structure, out of scope for
   this pass (stated in `SKILL.md`, not silently dropped).
3. **Lecture discovery**: enumerated from CS336's YouTube playlist (found via
   web search, not derivable from the course site — `cs336.stanford.edu`
   itself lists code/slides but no video links) via the vendored yt-dlp,
   subprocessed through `uv run --project <yttdl-dir>`. Lecture numbers
   parsed from video titles (`Lecture N` / `Lec. N`, both observed).
4. **Wired into the existing dispatch** (`combined_search`, `resolve_any`,
   `download_any`) alongside MIT and SEE, tagged
   `"institution": "Stanford (course site)"`.

**Verified end-to-end** against CS336 (Language Modeling from Scratch,
Hashimoto/Liang): all **17/17** lecture transcripts downloaded from YouTube
captions, 0 errors, re-run confirmed idempotent (0.9s vs. 59s on first run,
all skipped as existing). Sample transcript read back coherently (real
speech, not garbled).

`SKILL.md` updated: description, workflow, output layout, and Notes & flags
all now describe three sources, with the microsite path's narrower coverage
(hand-curated registry, transcripts-only, `uv` requirement) stated plainly
rather than implied to be as complete as MIT/SEE.
