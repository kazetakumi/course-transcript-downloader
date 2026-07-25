# Research stanford-001 — How SEE serves content & how to detect materials

Verified live against **four contrasting courses** (spanning CS, AI, EE, and
Robotics) plus the catalog page, on 2026-07-25.

## The full catalog (fixed, enumerable — unlike MIT's hundreds of courses)

Fetched from `https://see.stanford.edu/Course`. **10 listed, 9 actually on
SEE's own infrastructure:**

| Code | Title | Instructor |
|---|---|---|
| CS106A | Programming Methodology | Mehran Sahami |
| CS106B | Programming Abstractions | Julie Zelenski |
| CS107 | Programming Paradigms | Jerry Cain |
| CS223A | Introduction to Robotics | Oussama Khatib |
| CS229 | Machine Learning | Andrew Ng |
| EE261 | The Fourier Transform and its Applications | Brad Osgood |
| EE263 | Introduction to Linear Dynamical Systems | Stephen Boyd |
| EE364A | Convex Optimization I | Stephen Boyd |
| EE364B | Convex Optimization II | Stephen Boyd |
| LOGIC | Stanford Introduction to Logic | Michael Genesereth | **external site** (`intrologic.stanford.edu`, different licensing) — not part of SEE proper, treat as out of scope / skip.

No pagination, no search — the whole discoverable catalog is this one page.
There is **no API**; everything is static server-rendered HTML.

## Course addressing

- Course landing page: `https://see.stanford.edu/Course/<CODE>` (e.g.
  `/Course/CS229`).
- Each course also has an internal **materials-directory slug**, unrelated to
  the course code, embedded in every asset path:
  `icspmcs106a` (CS106A), `aimlcs229` (CS229), `lsocoee364a` (EE364A),
  `aiircs223a` (CS223A). **This slug can't be derived from the course code —
  it must be scraped from the course page's asset links** (e.g. first PDF
  href) before any file URLs can be built.

## Enumerating a course's lectures

Each course page lists its lecture sessions; each lecture has its own page:
`https://see.stanford.edu/Course/<CODE>/<numeric-id>`. **Ids are internal
database ids, non-sequential and non-derivable** (e.g. EE364A's 19 lectures
use ids `85, 94, 93, 77, 78, ...` — lecture order ≠ id order). The course page
is the only place that maps lecture number → id; must be scraped, not guessed.

## Video + transcript — the make-or-break resource

**Every one of the 4 courses checked has transcripts for every lecture, in
two parallel formats, at predictable paths once the materials slug is known:**

```
https://see.stanford.edu/videos/courses/see/<CODE>/<CODE>-lectureNN.mp4
https://see.stanford.edu/materials/<slug>/transcripts/<CourseTitle>-LectureNN.html
https://see.stanford.edu/materials/<slug>/transcripts/<CourseTitle>-LectureNN.pdf
```

`<CourseTitle>` is a CamelCase rendering of the course title (e.g.
`ProgrammingMethodology`, `MachineLearning`, `ConvexOptimizationI`,
`IntroductionToRobotics`) — **also not derivable from the course code**, must
be read off one confirmed transcript link on the course/lecture page.

Confirmed by fetching real transcript HTML for all 4 courses: genuine
full-prose spoken transcripts, bold speaker labels
(`Instructor (<Name>):`, `Student:`), `[inaudible]`/`[Music playing.]`
annotations, a duration note at the end. **No timestamps, no `.vtt`/`.srt`
caption files anywhere** — structurally different from MIT's newer courses
(which use caption files) and closer to MIT's PDF-transcript era, except SEE
also gives an HTML variant.

**Detection rule (unlike MIT, this doesn't need per-file sniffing):** SEE's
uniform structure means transcript existence can be checked directly — HEAD
`.../transcripts/<CourseTitle>-LectureNN.html` for each lecture number found
on the course page. Across all 4 sampled courses (16–28 lectures each),
**100% of lectures had transcripts** — worth verifying this holds for the
remaining 5 unchecked courses before assuming it's universal, but no course
so far has been video-without-transcript the way some MIT courses are.

## Handouts / lecture notes / syllabus

All PDF, all under `https://see.stanford.edu/materials/<slug>/<file>.pdf`,
flat (no subfolder categorization beyond `transcripts/`). Counts varied 8–28
per course. No consistent filename convention across courses (numbered
`01-...pdf` for CS106A, topic-named `handout1_CourseInfo.pdf` for CS223A,
`cs229-notesN.pdf` for CS229) — **must be discovered from the course page's
"Handouts" section links, not guessed from a pattern.**

## Homework / problem sets / exams

Same materials directory, PDF (+ occasional `.zip` data bundles and `.m`
MATLAB files for the more technical courses). **Exams are inconsistent across
courses** — EE364A has practice + final exams, CS106A has practice
midterm/final, CS229 and CS223A have **none**. Must detect per-course, not
assume presence.

## Bulk download — better than MIT

**Every course checked has a single bulk zip** covering handouts/notes/psets
(not videos):
`https://see.stanford.edu/materials/<slug>/<CourseTitle>AllMaterials.zip`
(e.g. `ProgrammingMethodologyAllMaterials.zip`). This is a real advantage over
MIT OCW, which has no reliable bulk archive (see
[asset 001](001-ocw-structure.md), "Bulk download"). Videos/transcripts are
still per-file only.

## Course-identifier collisions with the existing `courses/<slug>/` MIT output

None possible in practice: MIT slugs are long hyphenated titles
(`18-06sc-linear-algebra-fall-2011`); SEE course codes are short
department-prefixed codes (`CS229`, `EE364A`) that never collide with MIT's
department-number scheme (`18.06`, `6.006`) even before slugifying. **A
prefix-free flat `courses/<slug>/` layout is safe** — no institution
namespacing is structurally required to avoid collisions, though one may
still be wanted for clarity/browsability.

## Licensing — inconsistent, worth flagging (not building, just noting)

- SEE's homepage states materials are under **Creative Commons BY-NC-SA
  4.0**, but this notice is **sitewide, not repeated on every course page**.
- CS223A's page notes some archival video clips were **cut for copyright**
  reasons (pre-existing conference footage), implying licensing isn't
  perfectly uniform course-to-course the way MIT OCW's is.
- Not a blocker for downloading transcripts/notes/psets (the destination's
  scope), but the eventual `SKILL.md`/README should carry SEE's CC BY-NC-SA
  attribution requirement (**NC** — noncommercial — differs from MIT OCW's
  license terms and is worth a one-line callout to the user).
