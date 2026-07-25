---
id: 002
title: Determine how to discover OCW courses and resolve topic / number / URL to a course
type: research
mode: AFK
status: closed
assignee: null
blocked_by: []
parent: map
---

## Question

Document **how the skill turns each of the three user inputs into a specific OCW
course**, and — critically — **how to filter/rank so results are courses that
actually have video transcripts** (per ticket 001's make-or-break filter).

Answer concretely, with example requests/URLs:

1. **Topic / keyword search.** Is there a search API or JSON endpoint on
   `ocw.mit.edu` (or the OCW search backend), or must search results be scraped
   from the search page? What does a result look like (title, course number,
   URL, department, level, whether it has media)?
2. **Ranking / relevance.** Given a topic, how do candidate courses come back
   and what signals are available to rank "most relevant" — and to **prefer
   courses that have lecture video with transcripts** over notes-only courses?
   (If search results expose a "has media / has video" facet, note it.)
3. **Course number / exact title.** How do you resolve a known identifier like
   `18.06` or `6.006` (or a title) directly to its course URL?
4. **Direct URL.** What URL forms should the skill accept, and how do you
   normalize a pasted course URL to the canonical landing page?
5. **What "no good match" looks like.** How the discovery layer signals that a
   topic has no OCW course with transcripts — this seeds the resolution-UX
   decision (ticket 003).

**Deliverable:** a markdown summary saved as a linked asset (e.g.
`.wayfinder/assets/002-ocw-discovery.md`).
