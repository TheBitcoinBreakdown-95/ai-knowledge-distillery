---
description: Report the current health and status of the AI Notes Knowledge Distillery. This is a read-only di...
---

Report the current health and status of the AI Notes Knowledge Distillery. This is a read-only diagnostic — do not modify any files.

## Instructions

1. **Read the ingestion tracker** — Read `Knowledge Distillery/sources/ingested-files.md`.

2. **Scan source directories** — Scan the same source directories configured in `/process-notes`. Find all `.md` files and compare against the tracker.

3. **Detect untracked files** — Compare scanned files against ingested-files.md. List any not in the tracker.

4. **Count Recent Additions** — For each topic file in `Knowledge Distillery/`, count `###` entries under `## Recent Additions`. Flag files with 3+ entries as ready for `/consolidate-kb`.

5. **Check cross-references** — Scan all `(see [concept](file.md#section))` patterns in topic files. For each, verify the target file exists and the section heading exists. Report broken links.

6. **Count KB size** — Total line count per topic file and grand total.

7. **Check DISCREPANCIES.md** — If it exists, report count of open (unresolved) discrepancies.

8. **Display report:**

```
## Knowledge Distillery Status — [date]

### Pending Ingestion
[List of untracked files, or "All source files tracked"]

### Recent Additions Backlog
| File | Entries | Ready to Consolidate? |
[files with counts, flag 3+]

### Broken Cross-References
[List, or "None detected"]

### Discrepancies
[Count of open items, or "None" / "File not yet created"]

### KB Size
| File | Lines |
[table + total]
```

## Important Rules
- Read-only — do not modify any files
- Report findings clearly; do not attempt to fix issues
- If cross-reference anchor matching is ambiguous, note it for manual review
