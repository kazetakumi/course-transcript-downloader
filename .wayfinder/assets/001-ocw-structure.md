# Research 001 — How OCW serves content & how to detect transcripts

Verified live against three contrasting courses via the **MIT Learn API**
(`https://api.learn.mit.edu`) on 2026-07-24.

## Course addressing

- Courses live at `https://ocw.mit.edu/courses/<slug>/` where `<slug>` is e.g.
  `18-06sc-linear-algebra-fall-2011`.
- The API `readable_id` is a different form, e.g. `18.06SC+fall_2011`
  (course-number `+` `<semester>_<year>`). Both appear in API responses.

## Enumerating a course's files

1. Resolve the course → its **numeric run id**:
   `GET /api/v1/courses/?readable_id=<url-encoded readable_id>` →
   `results[0].runs[0].id` (numeric, e.g. `3434`). Also gives
   `course_feature` (a list like `["Lecture Videos","Lecture Notes",...]`).
2. List every file for that run (paginated, 100/page, **filter is the numeric
   `run_id`** — the hash/string ids do NOT filter):
   `GET /api/v1/contentfiles/?run_id=<num>&limit=100&offset=<n>`
   Loop `offset` until `offset >= count`.

### Useful contentfile fields
`title`, `content_feature_type` (list), `file_extension`, `youtube_id`,
`url` (the resource **page**, not the raw file), `key` (ends `/resources/<slug>/`).

## Getting the RAW downloadable file

`contentfiles[].url` is the human resource page. The actual file link is inside
that page as `href="/courses/<slug>/<Filename>.<ext>"`. Scrape the page and pick
the href whose extension matches the file (prefer the one whose basename maps to
the contentfile `key`'s trailing slug — pages can list several files).

Raw files are served from `https://ocw.mit.edu/courses/<slug>/<Filename>.<ext>`.

## Transcript availability — the make-or-break filter (verified variance)

Transcript representation **varies by course vintage**:

| Course | Videos | Transcript form |
|---|---|---|
| 18.06SC (2011, Scholar) | 146 mp4 | `.srt`/`.vtt`/`.webvtt` caption files (25) |
| 18.06 (2010, archive.org era) | 37 mp4 | mostly **`<id>_transcript.pdf`**, only 1 `.webvtt` |
| 24.200 Ancient Philosophy (2004) | 0 | none — notes/assignments only |

**Detection rule:** a course "has transcripts" if any contentfile has extension
in `{.vtt, .srt, .webvtt}` **OR** `transcript` appears in its title/url and it is
a PDF. Videos also expose `youtube_id`, enabling a `yt-dlp` caption fallback.

## Categorization — `content_feature_type` is NOT sufficient

208 of 396 files in 18.06SC came back `(uncategorized)` — including **all** the
caption transcripts. Categorize with **extension + feature + title/path** together:

- **transcripts/**: ext ∈ {.vtt,.srt,.webvtt} OR (pdf with `transcript` in name)
- **lecture-notes/**: feature ∈ {Lecture Notes, Readings}
- **problem-sets/**: feature ∈ {Problem Sets, Problem Set Solutions, Assignments,
  Written Assignments}
- **exams/**: feature ∈ {Exams, Exam Solutions}
- **other/**: remaining docs (uncategorized PDFs, `.m`, etc.)
- **skip**: `.mp4` (video — out of scope), `.jpg/.png` (thumbnails), `(none)` ext

## Bulk download

The per-course `/download` page is JS-driven and exposes no static ZIP, so
**per-file download is the reliable path** (no bulk archive to rely on).
