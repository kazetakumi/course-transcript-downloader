---
id: 001
title: Map how OCW serves course content and how to detect transcript availability
type: research
mode: AFK
status: closed
assignee: null
blocked_by: []
parent: map
---

## Question

For MIT OpenCourseWare (`ocw.mit.edu`), document — from real sample courses —
**how course content is structured and served**, and specifically **how to
detect whether a given course has downloadable video transcripts and in what
format**. This is the foundational research that unblocks the download strategy
and output-layout decisions.

Answer concretely, with example URLs, for at least 2–3 real courses (ideally a
mix: one video-rich course and one that is notes/pset-only):

1. **Course URL scheme.** How is a course addressed
   (`ocw.mit.edu/courses/<dept-num-title>/...`)? How do you get from a landing
   page to its lectures and resource lists?
2. **Video transcripts — the make-or-break resource.**
   - How are transcripts served? (Caption files — `.vtt` / `.srt`? Inline text
     on a page? A separate "transcript" download?)
   - **How do you programmatically detect that a course actually HAS lecture
     video with transcripts vs. is notes/pset-only?** (Verify the assumption
     that many OCW courses have no video at all — don't hardcode it, confirm it.)
   - What identifies each lecture and orders them?
3. **Lecture notes / slides / PDFs.** Where do they live, how are they linked,
   what formats?
4. **Problem sets / assignments / exams (+ solutions).** Same: location, linkage,
   formats.
5. **Bulk vs. per-file.** Does OCW offer a bulk course download (e.g. a `.zip`),
   a data/JSON endpoint, or a public API/mirror (e.g. a GitHub mirror)? Or must
   everything be scraped per-file? Note anything that makes fetching easier.
6. **Availability variance.** How much does the presence of each resource type
   vary across courses, and how would the skill know what a course offers before
   downloading?

**Deliverable:** a markdown summary saved as a linked asset (e.g.
`.wayfinder/assets/001-ocw-structure.md`) that the download-strategy and
output-layout tickets can build on directly.
