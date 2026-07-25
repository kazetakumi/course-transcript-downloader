# Research 002 — Discovering & resolving OCW courses

Verified live against `https://api.learn.mit.edu` on 2026-07-24.

## The three input modes → a course

### 1. Topic / keyword search
`GET /api/v1/learning_resources_search/?q=<topic>&platform=ocw&resource_type=course&limit=<n>`

Returns `{count, results:[...]}`. Each result has `id`, `readable_id`, `title`,
`url` (the `ocw.mit.edu/courses/<slug>/` page), `platform`, `resource_type`,
`course_feature`, and `runs[]` (with `year`, `semester`, `description`).
Results are already relevance-ranked by the API.

### 2. Course number / exact title
`GET /api/v1/courses/?readable_id=<url-encoded readable_id>` resolves a known
identifier directly. If the exact `readable_id` isn't known, fall back to the
search endpoint with the number/title as `q` and take the top match.

### 3. Direct URL
Accept any `https://ocw.mit.edu/courses/<slug>/...` URL. Extract `<slug>`, then
map slug → readable_id via `learning_resources_search?q=<slug words>` or by
requesting the course page and reading its metadata. Simplest robust path:
search by the slug's human words and match the result whose `url` contains the
slug.

## Ranking toward transcripts — DECISION: resolve-then-warn

The API exposes `course_feature` per course (e.g. `Lecture Videos`,
`Lecture Notes`) but there is **no `Transcripts` feature**, and "has video" does
NOT imply "has transcripts" (the 2010 archive.org era proves this). So:

- **At search time**, use the API's own relevance ranking; as a light nudge,
  prefer candidates whose `course_feature` includes `Lecture Videos`.
- **Authoritative transcript check happens AFTER** a course is chosen, by
  enumerating its contentfiles (see research 001). If the chosen course has no
  transcripts, **warn the user** and let them proceed or pick another — do not
  try to guarantee transcripts at search time.

## "No good match" signal

`count == 0` from the search endpoint, or a chosen course whose contentfile
enumeration yields zero transcript files → surface to the user as
"this course has no video transcripts on OCW".
