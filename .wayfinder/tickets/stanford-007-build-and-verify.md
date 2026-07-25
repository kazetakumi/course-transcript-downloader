---
id: stanford-007
title: Build the unified engine and verify end-to-end against a real SEE course
type: task
mode: HITL
status: closed
assignee: claude
blocked_by: [stanford-002, stanford-003, stanford-004, stanford-005, stanford-006]
parent: map-stanford-see
---

## Question

Per this map's Notes ("Execution override"), this is the final ticket that
actually builds and verifies the skill — not just decides its shape.

1. Extend `ocw_download.py` (or its renamed successor, per
   [stanford-006](stanford-006-rename-skill-and-repo.md)) with a SEE-aware
   engine implementing the decisions recorded in
   [stanford-002](stanford-002-discover-and-resolve-see-courses.md) through
   [stanford-005](stanford-005-output-layout.md), sharing the
   `search`/`resolve`/`download` subcommand contract with the existing MIT
   engine.
2. Update `SKILL.md` to describe both institutions, the combined-table search
   behavior, and the SEE licensing callout.
3. **Verify against at least one real SEE course end-to-end** (per the map's
   "Map done" criterion) — download, check `manifest.json` and per-folder
   counts against what's actually on disk, the way the original MIT effort
   verified against 18.06SC / 18.06 (2010) / 24.200.
4. Record the resolution: which course was verified, counts confirmed, any
   deviations from the plan discovered during the build.

## Resolution

Extended `ocw_download.py` (now under `.claude/skills/ocw-downloader/`) with:
`SEE_CATALOG`, `see_search_courses`, `see_resolve_course`, `_see_scan_page`,
`combined_search`, `resolve_any`/`download_any` dispatch, `see_download_course`,
`see_transcript_html_to_text`, `_see_categorize`. `SKILL.md` rewritten for
both institutions. Full diff lives in this session's uncommitted working tree
(not committed — awaiting the user's review/commit).

**Verified end-to-end** against **CS223A — Introduction to Robotics**
(`courses/CS223A/`, run from the repo root):

| | Expected (from stanford-001 research) | Actual on disk |
|---|---|---|
| Transcripts | 16 lectures, all present | 16 (`.pdf` + `.txt`) |
| Handouts | 8 | 8 |
| Problem sets | 6 | 6 |
| Exams | none (confirmed in research) | none — correctly absent |
| Errors | — | 0 |

Manifest's `course.institution: "Stanford SEE"`, README's `Institution:`
line, and `transcripts_available: true` all correct. MIT path
regression-checked (`resolve "18.06"`) — unaffected by the shared-helper
changes.

**Deviation found during verification (fixed, not deferred):** SEE serves
transcript HTML as **Windows-1252**, not UTF-8, with no charset header —
decoding as UTF-8 silently mangled smart-quote apostrophes into replacement
characters. Caught by inspecting the actual `.txt` output, not assumed;
fixed by decoding as `cp1252` in `see_transcript_html_to_text`. This is new
information beyond stanford-001's research (which confirmed transcript
*content* but not byte encoding) — no fog reopened, just a build-time fix.

**Map done.** Combined MIT + Stanford SEE, verified against real courses from
both institutions.
