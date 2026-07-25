---
id: stanford-006
title: Rename the skill directory, SKILL.md, and the GitHub repo
type: task
mode: HITL
status: closed
assignee: claude
blocked_by: []
parent: map-stanford-see
---

## Question

Per the charting session's decision (map Notes), the skill and this repo
should be renamed to something institution-agnostic now that the destination
covers MIT + SEE. Nothing blocks starting this — it's independent of the
other tickets — but it doesn't need to *finish* before them either.

1. Pick the new skill directory name and `SKILL.md` `name`/`description`
   (currently `mit-ocw-downloader`).
2. Pick the new repo name (currently `mit-course-transcript-downloader`).
3. **Renaming the GitHub repo touches the remote** (`git remote -v` shows
   `origin` pointing at `github.com/kazetakumi/mit-course-transcript-downloader`)
   — this is a hard-to-reverse, shared-system action. Confirm explicitly with
   the user immediately before running `gh repo rename` or equivalent, even
   though this ticket itself is pre-approved for renaming to happen.
4. Record what was actually renamed (old → new names, new clone URL if the
   repo was renamed) as this ticket's resolution — later tickets/sessions
   will refer to paths by the new names.

## Resolution

User confirmed both renames explicitly via a direct question before either
was executed.

- **Skill:** `.claude/skills/mit-ocw-downloader/` → `.claude/skills/ocw-downloader/`
  (via `git mv`, preserving history). `SKILL.md` `name:` and `description:`
  updated to cover both institutions.
- **GitHub repo:** `kazetakumi/mit-course-transcript-downloader` →
  `kazetakumi/course-transcript-downloader`, via `gh repo rename
  course-transcript-downloader --yes`. Local `origin` remote auto-updated to
  `https://github.com/kazetakumi/course-transcript-downloader.git` (confirmed
  via `git remote -v`). The local working-directory folder name was left
  unchanged (renaming it mid-session risked disrupting the active session's
  path references — not required for anything to function).
