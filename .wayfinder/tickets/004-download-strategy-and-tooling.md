---
id: 004
title: Decide the download strategy and tooling per resource type
type: grilling
mode: HITL
status: closed
assignee: null
blocked_by: [001]
parent: map
---

## Question

Given OCW's real content structure (ticket 001), decide **how the skill actually
fetches each resource type**.

- **Bulk vs. per-file.** If OCW offers a bulk `.zip` / data endpoint / mirror,
  do we use it, or fetch each resource individually? Tradeoffs (completeness,
  speed, fragility to markup changes).
- **Transcripts.** How to fetch caption files vs. inline transcript text; whether
  to hit a caption endpoint (`.vtt`/`.srt`) directly or scrape.
- **PDFs / notes / psets.** Plain HTTP download; how to discover every file link
  on a resource page.
- **Tooling.** What does the skill lean on — plain `curl`/`wget`/`fetch`, a
  scripting language (Python `requests` + `beautifulsoup`?), `yt-dlp` for caption
  extraction? Keep it to dependencies that are reasonable to require.
- **Politeness & resilience.** Concurrency limits, delays, retries, resume on
  partial failure, and behavior when a resource type is absent for a course.

Use `/grilling`; pull in `/research` if a specific tool's capability needs
verifying.
