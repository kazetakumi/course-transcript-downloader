---
id: stanford-002
title: Discover & resolve SEE courses, merged with MIT results into one combined table
type: grilling
mode: HITL
status: closed
assignee: claude
blocked_by: [stanford-001]
parent: map-stanford-see
---

## Question

[Research stanford-001](../assets/stanford-001-see-structure.md) established
that SEE has **no search API and a fixed, fully-enumerable 9-course catalog**
(vs. MIT's hundreds via `api.learn.mit.edu`). Decide, with the user:

1. **Topic search.** For a topic/keyword input, how does SEE contribute
   candidates — simple substring/keyword match against the static 9-course
   list (title, code, department), given there's no ranked search to call?
2. **Combined table.** The map's Destination already fixed the shape (one
   table, institution-labeled, per the "search across both, tag results by
   institution" decision from the charting session) — decide the concrete
   columns/format and how MIT's API-ranked results and SEE's static-match
   results merge into one ordering.
3. **Number/title/URL resolution.** How does a bare SEE course code
   (`CS229`), title, or a pasted `see.stanford.edu/Course/...` URL resolve
   directly (mirroring MIT's `resolve` subcommand)?
4. **Materials-slug & course-title lookup.** Since neither the materials
   directory slug (e.g. `aimlcs229`) nor the CamelCase transcript-filename
   title (e.g. `MachineLearning`) is derivable from the course code, decide
   where/when that scrape happens — at `search`/`resolve` time (slower, but
   then `transcripts_available` can be reported like MIT) or deferred to
   `download` time.

## Resolution

Built into `ocw_download.py`:

1. **Topic search** (`see_search_courses`): substring/keyword match against
   the hardcoded `SEE_CATALOG` (code, title, dept, instructor).
2. **Combined table** (`combined_search`): MIT's API-ranked hits first, then
   SEE's catalog matches appended, each tagged `"institution"`. Wired into the
   `search` CLI subcommand.
3. **Resolution** (`resolve_any` → `_is_see_target` dispatches on SEE course
   code or `see.stanford.edu` URL, else falls to MIT's `resolve_course`).
   `see_resolve_course` handles code, title (via catalog search fallback), and
   direct URL uniformly.
4. **Materials-slug & title lookup happens at resolve time** (chose "scrape
   now" over "defer to download") — and turned out to need only **one** regex
   scan of the course page (`_see_scan_page`, matching
   `/materials/<slug>/transcripts/<Title>-Lecture<NN>.html`), which yields the
   slug, the title, AND the exact list of lecture numbers with transcripts in
   one pass — better than the original plan (no probing/guessing needed, and
   `transcripts_available` is reported honestly like MIT's).

Verified live: `resolve "CS229"` correctly returns `materials_slug:
"aimlcs229"`, `title_camel: "MachineLearning"`, 20 lecture numbers,
`transcripts_available: true`. `search "machine learning"` returns 3 MIT hits
then CS229, each tagged.
