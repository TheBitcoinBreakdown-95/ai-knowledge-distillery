---
description: Merge Recent Additions sections into the main body of Knowledge Distillery topic files.
disable-model-invocation: false
---

Merge Recent Additions sections into the main body of Knowledge Distillery topic files.

## Instructions

1. **Read the KB structure** — Read `Knowledge Distillery/README.md` to understand topic files and section organization.

2. **For each topic file in `Knowledge Distillery/`**, check if it has a `## Recent Additions` section. Skip files without one, or with fewer than 5 entries under it — **unless** the entries have been pending for 3+ sessions (stale rule), in which case merge them individually regardless of count.

3. **For each file with `## Recent Additions` to consolidate:**

   a. Read the full file. Understand the main body's `##` section structure.

   b. For each `###` entry under `## Recent Additions`:
      - Identify which existing main-body `##` section the entry belongs in by topic
      - If a matching section exists: insert the entry's content as a new `###` subsection within that section. Remove the date from the heading. Keep source attribution.
      - If no matching section exists: create a new `###` subsection within the closest thematic `##` section
      - Remove the entry from `## Recent Additions` after integrating it

   c. Once all entries are integrated, remove the empty `## Recent Additions` heading.

   d. Write the updated file.

4. **Preserve all cross-references.** Do not change any `(see [concept](file.md#anchor))` links.

5. **Update Concept Index** — If any newly consolidated sections introduce concepts not yet in the README.md Concept Index table, append them.

6. **Update the processing log** — Add a row to `sources/processing-log.md`:
   `| [date] | Consolidation pass | [files updated] | Merged N entries into main body |`

7. **Report** — List each file processed, how many entries were merged, and where each landed.

8. **Verify KB health** — After all consolidation is complete, run these 5 invariant checks:

   1. **Cross-ref integrity:** Scan all edited files for `(see [x](file.md#anchor))` links. Verify each anchor resolves to a real heading in the target file. Report any broken refs.
   2. **No orphan files:** Verify every topic `.md` in `Knowledge Distillery/` is listed in README.md's index.
   3. **Recent Additions backlog:** Confirm no file has Recent Additions entries pending for 3+ sessions.
   4. **Concept Index coverage:** Verify every H2 section in edited topic files maps to a Concept Index entry in README.md.
   5. **Discrepancy resolution:** Check if any open discrepancy in DISCREPANCIES.md is older than 3 sessions.

   Report: `PASS` or `FAIL` for each check. If any fail, list the specific issues.

## 9. Framework Impact Check

After all entries are merged, review each newly consolidated entry and ask: **does this change how the workspace should operate?**

Most entries won't — they add depth to existing topics. But some will. Check for:

- **New best practice** not covered by any existing rule in `.claude/rules/` → propose adding or updating a rule
- **Contradicts an existing rule** → propose updating or removing the outdated rule
- **New anti-pattern** worth detecting → propose a new audit check in `templates/audit-checks.md`
- **Tool/workflow change** → propose updating a CLAUDE.md file or command

If any entries are framework-relevant, tell the user directly:
> "This new insight suggests [specific change] to [specific file]. Want me to apply it?"

Apply on approval. If nothing is framework-relevant, say nothing — do not prompt unnecessarily.

## Important Rules
- Never delete content — only move it from Recent Additions into the main body
- Never change the voice or style of existing content
- If placement is ambiguous, ask the user before moving
- After consolidation, the file should read as one coherent document without temporal seams
- Do NOT consolidate files with fewer than 5 Recent Additions entries — unless the entries have been pending for 3+ sessions (stale rule). Stale entries get merged individually to prevent indefinite limbo
