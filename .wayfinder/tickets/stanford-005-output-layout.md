---
id: stanford-005
title: Decide whether courses/<slug>/ needs institution labeling
type: grilling
mode: HITL
status: closed
assignee: claude
blocked_by: [stanford-001]
parent: map-stanford-see
---

## Question

[Research stanford-001](../assets/stanford-001-see-structure.md) found **no
collision risk** between SEE's short course codes (`CS229`) and MIT's long
hyphenated slugs — a flat `courses/<slug>/` layout (unchanged from the
original map's [output-layout ticket](005-output-layout-and-transcript-format.md))
is structurally safe with no institution namespacing required.

The remaining decision is purely about **clarity, not correctness**: given a
user's `courses/` directory may now hold both MIT and SEE courses
side-by-side, does the existing `README.md`/`manifest.json` per course need
an added "institution" field, or is the course slug alone (e.g. `CS229` vs.
`18-06sc-linear-algebra-fall-2011`) self-evidently distinguishable enough to
skip that?

## Resolution

Added the institution field — cheap and low-risk, and directly answers a
question a user browsing `courses/` would otherwise have to infer from the
slug shape. `_write_readme` now emits an `Institution:` line and picks the
id label (`Readable id` vs `Course code`) accordingly; `manifest.json`
carries `institution` inside its `course` record for both engines (MIT via
`_summarize`, SEE via `_see_summarize`). Flat `courses/<slug>/` layout
otherwise unchanged — no folder namespacing added, per the research's
no-collision finding.
