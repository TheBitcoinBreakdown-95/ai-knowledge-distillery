# Knowledge Distillery — Discrepancies

Review queue for claims that may be outdated, wrong, contradicted, or unverifiable. Items are added here by `/verify-kb` (deep research) and `/process-notes` (contradiction detection during ingestion).

**The user resolves these.** Once reviewed, mark the status as Resolved and note the action taken.

---

## Open Discrepancies

### CLAUDE.md Instruction Limit: ~100 lines vs ~150-200 instructions vs ~200 lines

**File:** context-engineering.md, memory-persistence.md
**Section:** What to Include (and What NOT to Include); Layer 1: CLAUDE.md
**Current claim (context-engineering.md):** "If it grows past ~100 lines, break information into separate docs"
**Current claim (memory-persistence.md):** "If your CLAUDE.md exceeds ~200 lines, break content into separate markdown files"
**New source says:** "LLMs only handle ~150-200 instructions before performance degrades" (cited from a best practices guide)
**Source:** deep-research-report.md (Section 4, Section 10)
**Date found:** 2026-02-28
**Assessment:** These three figures describe the same concern at different granularities. "~100 lines" is conservative guidance for keeping CLAUDE.md lean; "~200 lines" is a hard ceiling for memory files; "~150-200 instructions" refers to discrete instructions (not lines), which is a different unit of measure. They are compatible as a gradient (100 lines = keep it short, 150-200 distinct instructions = model performance ceiling, 200 lines = absolute max). However, the inconsistency between the two KB files (100 vs 200) should be reconciled during next consolidation.
**Status:** Resolved (Session 35) -- Compatible gradient, not a contradiction. ~100 lines = practical sweet spot, ~200 lines = hard ceiling, ~150-200 instructions = different unit (instructions vs lines). Official Anthropic guidance now says "under 500 lines" (see tools-and-integrations.md). No KB edits needed.

---

## Resolved

### Settings Count: 37 vs 38

- **Resolved (Session 14, 2026-03-01):** Updated skills-and-tools.md "Customization Scale" section from 37 to 38 settings. The detailed settings audit (claude-settings.md) counted 38; Boris Cherny's Feb 26 talk likely used an older count.

### Context Degradation Threshold: ~50% vs 20-40%

- **Resolved (Session 14, 2026-03-01):** No change needed. The figures describe a compatible gradient: quality degrades subtly at ~20-40%, manual compact recommended at ~50%, auto-compact failsafe at ~95%. Both figures remain documented with their sources.
