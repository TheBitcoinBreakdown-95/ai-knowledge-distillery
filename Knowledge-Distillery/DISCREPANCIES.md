# Knowledge Distillery — Discrepancies

Review queue for claims that may be outdated, wrong, contradicted, or unverifiable. Items are added here by `/verify-kb` (deep research) and `/process-notes` (contradiction detection during ingestion).

**The user resolves these.** Once reviewed, mark the status as Resolved and note the action taken.

---

## Open Discrepancies

*(none)*

---

## Resolved

### CLAUDE.md Instruction Limit: ~100 lines vs ~150-200 instructions vs ~200 lines

- **Resolved:** Compatible gradient, not a contradiction. ~100 lines = practical sweet spot, ~200 lines = hard ceiling, ~150-200 instructions = different unit (instructions vs lines). Official Anthropic guidance now says "under 500 lines" (see tools-and-integrations.md). No KB edits needed.

### Settings Count: 37 vs 38

- **Resolved:** Updated skills-and-tools.md "Customization Scale" section from 37 to 38 settings. The detailed settings audit counted 38; Boris Cherny's Feb 26 talk likely used an older count.

### Context Degradation Threshold: ~50% vs 20-40%

- **Resolved:** No change needed. The figures describe a compatible gradient: quality degrades subtly at ~20-40%, manual compact recommended at ~50%, auto-compact failsafe at ~95%. Both figures remain documented with their sources.
