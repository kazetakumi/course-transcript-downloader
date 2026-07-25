# Wayfinder — local-markdown tracker

No issue tracker was configured for this repo, so wayfinder is using its
**local-markdown** fallback. This directory *is* the tracker.

## Layout

- `map.md` / `map-<effort>.md` — one file per map issue (label `wayfinder:map`).
  Each is the low-resolution index of one effort, loaded once per session.
  There can be more than one map over a repo's lifetime — a redrawn destination
  (e.g. scope that was ruled out-of-scope on an earlier, completed map)
  starts a **fresh** map file rather than reopening the old one.
- `tickets/NNN-slug.md` — one file per child ticket. `NNN` is the ticket id,
  unique per map. When a repo has multiple maps, later maps prefix their
  ticket ids/filenames with a short effort tag (e.g. `stanford-001-slug.md`)
  so ids never collide across maps. A ticket's `parent` field names its map
  file (without `.md`).

## Ticket frontmatter

```yaml
id: 001                     # identity; matches the filename prefix
title: <human name>         # ALWAYS refer to a ticket by this, never a bare id
type: research              # research | prototype | grilling | task
mode: AFK                   # AFK (agent-only) | HITL (human in the loop)
status: open                # open | closed
assignee: null             # the claim — null means unclaimed
blocked_by: []              # list of ticket ids that must be closed first
parent: map
```

## Computing the frontier

The **frontier** = open, unblocked, unclaimed tickets — the edge you can work now.

- **open**: `status: open`
- **unblocked**: every id in `blocked_by` points to a ticket whose `status: closed`
- **unclaimed**: `assignee: null`

## Working a ticket (later sessions)

1. Load `map.md` (not every ticket body).
2. Pick the first frontier ticket (or the one the user named). **Claim it** —
   set `assignee` before any work.
3. Resolve it. Record the answer as a `## Resolution` section appended to the
   ticket file, set `status: closed`, and add a one-line pointer to the map's
   *Decisions so far*.
4. Create any newly-surfaced tickets; graduate fog from *Not yet specified*.

**Never resolve more than one ticket per session.**
