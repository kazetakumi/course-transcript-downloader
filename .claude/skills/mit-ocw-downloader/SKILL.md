---
name: mit-ocw-downloader
description: Find a relevant MIT OpenCourseWare course and download its video transcripts, lecture notes, problem sets, and exams into an organized folder. Use when the user names a topic (e.g. "linear algebra"), an MIT course number ("18.06", "6.006"), a course title, or pastes an ocw.mit.edu course URL and wants the course materials downloaded locally.
---

# MIT OpenCourseWare downloader

Downloads a course's **video transcripts**, **lecture notes/slides/PDFs**, and
**problem sets / assignments / exams** from MIT OpenCourseWare into an organized
`courses/<slug>/` folder. Video files themselves are intentionally skipped — the
transcripts stand in for them.

The engine is the bundled script `ocw_download.py` (pure Python 3 stdlib — no
`pip install` needed). It talks to the MIT Learn API (`api.learn.mit.edu`) and
`ocw.mit.edu`. Run it via the skill's own directory — `<skill-dir>` below is this
skill's base directory (shown when the skill loads):

```
python3 "<skill-dir>/ocw_download.py" <subcommand> ...
```

## The three inputs → a course

- **Topic / keyword** ("quantum mechanics") → run `search`, then confirm a choice.
- **Course number or title** ("18.06", "Introduction to Algorithms") → `resolve`.
- **Direct OCW URL** (`https://ocw.mit.edu/courses/<slug>/`) → `resolve`.

## Workflow

1. **If the input is a topic/keyword**, list candidates first and let the user pick:
   ```
   python3 "<skill-dir>/ocw_download.py" search "quantum mechanics" --limit 6
   ```
   This prints a JSON array (`readable_id`, `title`, `year`, `likely_has_video`).
   Present the top few by **name** and ask the user which one — do **not**
   auto-pick a topic match on their behalf. `likely_has_video` is only a hint;
   it is not a guarantee of transcripts (see step 3).

2. **If the input is a course number, title, or URL**, resolve it directly:
   ```
   python3 "<skill-dir>/ocw_download.py" resolve "18.06"
   ```
   Show the resolved course name and ask for a quick confirm before downloading.

3. **Download the confirmed course.** Pass the `readable_id` (best) or URL of the
   course the user chose in step 1/2 — not a bare topic. (Passing a raw topic
   works but silently auto-picks the top hit, skipping confirmation; avoid it.)
   Use `--dest` to control where `courses/` is created (default: cwd; for this
   repo, run it from the repo root so downloads land here):
   ```
   python3 "<skill-dir>/ocw_download.py" download "18.06SC+fall_2011" --dest .
   ```
   The command prints a JSON summary. **Check `transcripts_available`:**
   - `true` → report the per-folder counts to the user.
   - `false` → **warn the user** this course has no video transcripts on OCW
     (it may be a notes-only course), and offer to pick a different course or
     keep just the notes/psets it does have.

4. **Report** what landed, referring to the course by name. Point the user at
   `courses/<slug>/README.md` (human index) and `manifest.json` (full file list
   with source URLs). Mention any `errors` count from the summary.

## Output layout

```
courses/<slug>/
  README.md            # human-readable index
  manifest.json        # every file + its OCW source URL
  transcripts/         # per-lecture transcripts (PDF and/or caption files)
    *.txt              # cleaned plain-text version of any caption file
    other-languages/   # non-English translated captions, kept aside
  lecture-notes/
  problem-sets/        # includes assignments + solutions
  exams/               # includes exam solutions
  other/               # uncategorized course documents
```

## Notes & flags

- `--force` re-downloads files that already exist (default: skip → safe re-runs).
- Transcripts vary by course vintage: newer courses have caption files
  (`.vtt`/`.srt`), older ones have transcript PDFs on each video page — the
  script handles both, and detects the "no transcripts" case honestly.
- Out of scope by design: lecture **video files**, AI-generated summaries, and
  non-MIT sources. Don't try to add these here.
- If `search` returns nothing, tell the user no OCW course matched.
