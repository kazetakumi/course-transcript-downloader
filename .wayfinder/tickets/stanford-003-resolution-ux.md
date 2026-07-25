---
id: stanford-003
title: Decide the combined MIT+SEE resolution UX
type: grilling
mode: HITL
status: closed
assignee: claude
blocked_by: [stanford-002]
parent: map-stanford-see
---

## Question

Extend the existing resolution UX (present candidates & confirm for topics;
resolve + quick confirm for numbers/URLs; warn on no-transcripts courses —
see the original map's
[Resolution UX ticket](003-resolution-ux.md)) to the two-institution case:

1. When the combined table (from
   [stanford-002](stanford-002-discover-and-resolve-see-courses.md)) has hits
   from both institutions, how is the user's pick disambiguated (index
   number? institution + code?).
2. SEE's "no materials" case — research found exams are inconsistently
   present (2 of 4 sampled courses had none) but **transcripts were present
   for 100% of sampled lectures**. Should the no-transcripts warning even
   apply to SEE, or does it become a narrower "some resource types missing"
   note instead?
3. Any SEE-specific confirmation the user should see before downloading (e.g.
   the CC BY-NC-SA **NonCommercial** licensing note from
   [stanford-001](../assets/stanford-001-see-structure.md), which MIT OCW
   doesn't carry)?

## Resolution

1. **Disambiguation:** no new UI needed — the existing "present candidates,
   ask which one" flow already works unchanged, since each combined-table
   entry is self-labeled with `institution` + `code`/`readable_id`. Recorded
   in `SKILL.md` step 1: "Present the top few by name (and institution)."
2. **No-transcripts warning:** reused the existing logic **as-is**, not
   narrowed — `transcripts_available` is still computed honestly from actual
   on-disk counts (`counts.get("transcripts", 0) > 0`) per course, not
   assumed true for SEE. It simply won't fire for today's SEE catalog (100%
   coverage confirmed), but stays correct if a future course lacks
   transcripts. Exams' inconsistent presence needed no special-casing —
   `_folder_counts`/README already only list folders that have files.
3. **Licensing note:** added to `SKILL.md`'s Notes & flags section (CC
   BY-NC-SA 4.0, NonCommercial) as agent-facing guidance to mention when
   relevant — not a blocking confirmation gate, since it doesn't change
   whether the download proceeds.
