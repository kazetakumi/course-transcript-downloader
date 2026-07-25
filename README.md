# MIT Course Transcript Downloader

A [Claude Code](https://claude.com/claude-code) skill that finds a relevant
**MIT OpenCourseWare** course and downloads its **video transcripts**,
**lecture notes / slides / PDFs**, and **problem sets / assignments / exams**
into an organized local folder.

Give it a topic (`"linear algebra"`), an MIT course number (`18.06`, `6.006`),
a course title, or a direct `ocw.mit.edu` course URL — it resolves the course
via the MIT Learn API, downloads the materials, and organizes them with a
`README.md` index and a `manifest.json` (every file plus its source URL).

Lecture **video files** and non-MIT sources are out of scope by design — the
transcripts stand in for the video.

## The skill

Lives in [`.claude/skills/mit-ocw-downloader/`](.claude/skills/mit-ocw-downloader/):

- `SKILL.md` — how the skill resolves input, confirms the course, downloads, and reports
- `ocw_download.py` — the engine (pure Python 3 standard library — no `pip install`)

## Using the engine directly

```bash
SKILL=.claude/skills/mit-ocw-downloader/ocw_download.py

# 1. Search candidate courses for a topic
python3 "$SKILL" search "quantum mechanics" --limit 6

# 2. Resolve a number, title, or URL to one course
python3 "$SKILL" resolve "18.06"

# 3. Download a course's materials into ./courses/<slug>/
python3 "$SKILL" download "18.06SC+fall_2011" --dest .
```

The `download` command prints a JSON summary including `transcripts_available`
and per-folder counts. Re-runs are idempotent (existing files are skipped;
use `--force` to re-download).

## Output layout

```
courses/<slug>/
  README.md            # human-readable index
  manifest.json        # every file + its OCW source URL
  transcripts/         # per-lecture transcripts (PDF and/or caption files)
    *.txt              # cleaned plain-text of any caption file
    other-languages/   # non-English translated captions, kept aside
  lecture-notes/
  problem-sets/        # includes assignments + solutions
  exams/               # includes exam solutions
  other/               # uncategorized course documents
```

## How it works

- **Resolve** via the MIT Learn API (`api.learn.mit.edu`) — topic search, exact
  course-number matching, or URL/slug matching.
- **Two-pass download**: each lecture video's page is visited to grab its
  transcript (OCW does not index per-video transcripts as standalone files),
  then lecture notes, problem sets, and exams are fetched.
- Handles **both transcript vintages** — modern caption files (`.vtt`/`.srt`)
  and older per-video transcript PDFs — cleans captions to plain text, routes
  non-English translated captions aside, and honestly reports courses that have
  no transcripts.

Verified end-to-end against contrasting real courses (18.06SC Scholar,
18.06 2010 archive-era, and a notes-only humanities course).
