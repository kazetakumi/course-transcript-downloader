---
id: stanford-004
title: Decide the download strategy and tooling for SEE materials
type: grilling
mode: HITL
status: closed
assignee: claude
blocked_by: [stanford-001]
parent: map-stanford-see
---

## Question

[Research stanford-001](../assets/stanford-001-see-structure.md) found SEE
gives **both** a per-course bulk `AllMaterials.zip` (handouts/notes/psets,
not videos) and fully predictable per-file paths once the materials slug and
CamelCase course title are known. Decide, mirroring the original map's
[download-strategy ticket](004-download-strategy-and-tooling.md):

1. **Bulk zip vs. per-file** for handouts/notes/psets/exams — use the zip
   (fewer requests, one unpack step) or stay per-file for consistency with
   the existing MIT engine's per-file approach and its retry/idempotent-skip
   behavior?
2. **Transcripts: HTML or PDF (or both)?** MIT's engine already cleans
   caption/PDF transcripts to plain `.txt` — decide the equivalent cleaning
   step for SEE's HTML transcripts (strip markup, keep speaker labels?) vs.
   just keeping the PDF as MIT does for its PDF-transcript-era courses.
3. **Videos** — confirmed out of scope by the original map; reconfirm that
   holds for SEE's direct `.mp4` links too (no new fog here, just a
   consistency check).
4. Retry/idempotent-skip and `--force` behavior — reuse the existing engine's
   logic as-is, or does SEE's flat static-file structure change anything?

## Resolution

1. **Per-file** (user's tie-break decision) — `see_download_course` reuses
   the shared `_get`/`_existing_sub`/`_store` helpers unchanged; the bulk
   `AllMaterials.zip` is explicitly skipped (`_see_categorize` filters it
   out) to avoid double-downloading its contents per-file too.
2. **Both, asymmetrically**: PDF kept as the native transcript file (mirrors
   MIT's PDF-transcript-era courses); HTML is fetched only to derive the
   cleaned `.txt` sidecar via a small `HTMLParser` subclass
   (`see_transcript_html_to_text`) that treats `<p>` as paragraph breaks and
   keeps bold speaker labels as inline text (SEE's transcript HTML has no
   head/body wrapper, just bare `<p>` prose — confirmed by fetching a real
   transcript directly). **Found and fixed during verification:** SEE serves
   these as Windows-1252 with no charset header — decoding as UTF-8 mangled
   apostrophes into replacement characters; switched to `cp1252` decoding.
3. **Reconfirmed out of scope** — `see_download_course` never fetches
   `.mp4` URLs, only counts them (`skipped_video`) via one increment per
   lecture number (1:1 video-per-lecture, confirmed by research).
4. **Reused as-is** — `_existing_sub`/`--force` needed no changes; SEE's flat
   structure didn't require anything new.

Verified end-to-end against CS223A — see
[stanford-007](stanford-007-build-and-verify.md) for the full verification.
