---
id: 005
title: Decide the output directory layout and transcript format
type: prototype
mode: HITL
status: closed
assignee: null
blocked_by: [001]
parent: map
---

## Question

Decide **how downloaded content is organized on disk inside this repo**, and
**what form transcripts take**.

- **Directory layout.** Structure for a downloaded course — e.g.
  `courses/<course-slug>/lectures/NN-<title>/transcript.txt`, `notes/`,
  `problem-sets/`, `exams/`. Naming, ordering, how lecture number/title map to
  folders.
- **Transcript format.** Raw `.vtt`/`.srt`, cleaned plain text (timestamps
  stripped), or timestamped text? One file per lecture; naming.
- **Manifest / index.** Does the skill write a per-course index (e.g. a
  `README.md` or `manifest.json` listing lectures + which resources were found /
  skipped)? What does it record about availability and provenance (source URLs)?
- **Collisions & re-runs.** What happens on re-download (overwrite, skip, resume).

Use `/prototype` to sketch a concrete example tree to react to, then `/grilling`
to settle it.
