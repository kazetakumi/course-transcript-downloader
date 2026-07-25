---
id: 003
title: Decide the topic-to-course resolution UX
type: grilling
mode: HITL
status: closed
assignee: null
blocked_by: [002]
parent: map
---

## Question

When the user gives a **topic/keyword**, how does the skill choose *which* course
to download — and how much does it involve the user?

Decide, grounded in what ticket 002 finds discovery actually returns:

- **Auto-pick vs. confirm.** Silently take the top-ranked course, or present a
  short shortlist of candidates for the user to confirm before downloading?
- **Ambiguous identifiers.** What happens when a course number/title matches
  more than one course (e.g. multiple offerings/years)?
- **No-video fallback.** When the best topic match has **no lecture video /
  transcripts** (the make-or-break case from tickets 001–002), what does the
  skill do? Offer the notes/pset-only course anyway? Suggest the nearest course
  that *does* have transcripts? Refuse and explain?
- **Confirmation surface.** If it confirms, what does the user see (title,
  number, resource counts, "has transcripts" flag)?

Use `/grilling` (and `/prototype` for a rough confirmation-prompt mockup if the
shape is unclear).
