---
id: stanford-001
title: Map how Stanford Engineering Everywhere serves course content and how to detect materials availability
type: research
mode: AFK
status: closed
assignee: claude
blocked_by: []
parent: map-stanford-see
---

## Question

For **Stanford Engineering Everywhere** (`see.stanford.edu`), document — from
the real course catalog — **how course content is structured and served**, and
specifically **how to detect whether a given course has downloadable video
transcripts and in what format**. This is the foundational research that
unblocks every later decision on this map (discovery/resolution, download
strategy, output layout, architecture).

Answer concretely, with example URLs, covering the **full course catalog**
(SEE's is small and fixed, unlike MIT's — enumerate it rather than sampling):

1. **Catalog & course URL scheme.** What is the complete list of SEE courses,
   and their stable identifiers/slugs? Is there a catalog/index page, or must
   it be assembled by hand? How is a course addressed
   (`see.stanford.edu/Course/<code>`?) and how do you get from a course landing
   page to its lecture list and resource list?
2. **Video transcripts — the make-or-break resource.**
   - How are transcripts served? (Caption files? Separate transcript
     downloads/PDFs? Inline on the page? None at all for some/all courses?)
   - **How do you programmatically detect that a course actually HAS
     transcripts**, vs. video-only or notes-only? Don't assume — verify against
     real course pages.
   - What identifies each lecture and orders them within a course?
3. **Lecture notes / slides / handouts / syllabi.** Where do they live, how are
   they linked, what formats?
4. **Homework / problem sets / exams (+ solutions).** Same: location, linkage,
   formats.
5. **Bulk vs. per-file.** Any bulk download (zip), API, or data endpoint? Or is
   everything scraped per-file from static HTML? Note anything that makes
   fetching easier or harder than MIT's `api.learn.mit.edu`.
6. **Course-identifier collisions.** Do SEE's course codes/slugs ever collide
   with MIT course-number slugs already used under `courses/<slug>/`? (Needed
   to answer the output-layout fog item.)
7. **Availability variance.** How much do these resource types vary across
   SEE's (small) catalog, and how would the skill know what a course offers
   before downloading?

**Deliverable:** a markdown summary saved as a linked asset (e.g.
`.wayfinder/assets/stanford-001-see-structure.md`) that the later
discovery/resolution, download-strategy, and output-layout tickets on this map
can build on directly — mirroring how
[asset 001](../assets/001-ocw-structure.md) grounded the original MIT map.

## Resolution

Findings: [asset stanford-001](../assets/stanford-001-see-structure.md).
Fanned out 4 parallel agents against real course pages (CS106A, CS229,
EE364A, CS223A) spanning CS/AI/EE/Robotics, plus a direct fetch of the
catalog page. Headline findings:

- **Catalog is fixed and fully enumerable**: 9 courses on SEE's own
  infrastructure (a 10th, LOGIC, is hosted externally on a different site/
  license — treat as out of scope). No API, no search — the catalog page
  *is* the whole index.
- **Every course has transcripts for every lecture** (100% across the 4
  sampled, 16–28 lectures each), in parallel HTML + PDF form at
  `/materials/<slug>/transcripts/<CourseTitle>-LectureNN.{html,pdf}` — no
  `.vtt`/`.srt` captions anywhere, closer to MIT's PDF-transcript era but
  with an HTML variant too.
- **Two non-derivable identifiers must be scraped per course before any file
  URL can be built**: the materials-directory slug (e.g. `aimlcs229` for
  CS229) and the CamelCase course title used in transcript filenames (e.g.
  `MachineLearning`). Neither maps predictably from the course code.
- **Every course has a bulk `AllMaterials.zip`** for handouts/notes/psets
  (not videos) — an advantage MIT OCW lacks.
- **No collision risk** between SEE's short course codes (`CS229`) and MIT's
  long hyphenated slugs — flat `courses/<slug>/` stays safe, no institution
  namespacing is structurally required.
- **Licensing is CC BY-NC-SA 4.0 sitewide** (noncommercial clause, unlike
  MIT OCW) but isn't repeated per-course page — worth a one-line attribution
  callout in the eventual skill, not a blocker.
- Exams are inconsistently present (2 of 4 sampled courses have none) —
  must detect per-course, not assume.
