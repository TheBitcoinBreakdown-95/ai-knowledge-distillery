---
description: Process new notes from source directories and integrate them into the Knowledge Distillery.
disable-model-invocation: false
---

Process new notes from source directories and integrate them into the Knowledge Distillery.

## Instructions

1. **Fetch new bookmarks (if configured)** — If you have a bookmark scraping pipeline configured (e.g., Bird CLI for Twitter/X bookmarks), run it first to pull new bookmarks into the source directories before scanning. This ensures newly saved articles are available for processing.

   **Example (Bird CLI for Twitter/X):**
   ```
   bird bookmarks --format markdown --output ./Twitter\ Bookmarks/
   ```

   Skip this step if no bookmark pipeline is configured or if bookmarks are already up to date.

2. **Read the KB structure** — Read `Knowledge Distillery/README.md` to understand the current KB organization and topic categories.

3. **Read the fast-lookup index** — Read `Knowledge Distillery/sources/ingested-paths.txt` (flat file, one path per line, paths relative to repo root using `./` prefix). This is the fast index for detecting new files. Do NOT read `ingested-files.md` during scanning — it is the audit log, only written to after processing and read on demand.

   If `ingested-paths.txt` does not exist, copy from `ingested-paths.txt.template` and start fresh.

4. **Scan source directories** — Find all `.md` files in your configured source directories. Source directories are any folders outside `Knowledge Distillery/` that contain raw notes, articles, or research material.

   **Configure your source directories here** (add your own paths):
   ```
   # Add your source directories below, one per line.
   # These are folders containing raw notes, articles, bookmarks, or research.
   # Example:
   # ./sources/
   # ./bookmarks/
   # ./research-notes/
   ```

   **Always exclude** from scanning:
   - `Knowledge Distillery/` (the Distillery itself)
   - `kb-mcp/` (search engine code)
   - `.claude/` (Claude Code config)
   - Any `.pdf`, `.ts`, `.js`, `.py`, `.json`, `.svg`, `.png`, `.webp`, `.css`, `.html`, `.sh`, `.toml`, `.yaml`, `.yml`, `.cfg`, `.ini`, `.lock` files
   - Any `node_modules/`, `.git/`, `__pycache__/`, `dist/`, `build/` directories
   - Any `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `LICENSE.md`, `SECURITY.md`, `RELEASING.md` files (boilerplate)
   - Any `test/`, `tests/`, `e2e-tests/` directories (test fixtures, not knowledge)
   - Any `.github/` directories (CI config, issue templates)

5. **Detect new files** — Compare scanned files against the fast-lookup index. Any file not in `ingested-paths.txt` is new and needs processing.

6. **For each new file:**
   a. **Read** the file. If it is empty, a stub (< 5 lines of real content), or a link-only bookmark, skip it and note it in the tracker as "skipped — no content".

   a-ii. **Enrich with image descriptions** — Scan the file content for image references (`![alt](path)`). For each reference:

   **Skip (no knowledge value):** URLs containing `shields.io`, `awesome.re`, `badge`, `star-history`, `/logo`; alt text "Logo"; GIF files; SVG files (render poorly via vision); video thumbnails (`amplify_video_thumb`, `<video>` tags).

   **For content images:**
   - **Local/relative paths** (e.g., `./assets/image.png`): Resolve relative to the source file's directory. Read with the Read tool. If file missing, log `[image-missing: path]` and continue.
   - **Remote URLs** (e.g., `https://pbs.twimg.com/...`): Fetch with WebFetch. If fetch fails (404, timeout, expired CDN), log `[image-unavailable: URL]` and continue.

   **Describe:** For each successfully read image, write a 1-3 sentence factual description (diagrams: components/flows depicted; screenshots: UI/terminal state; charts: data/trends visible). No interpretation.

   **Inline:** Mentally replace each image reference with its description when proceeding to steps 5b-5h. The enriched version is transient — source file is never modified.

   **Caps:** Max 10 content images per file. Max 40 across the entire batch. If budget exhausted, note in report and continue text-only.

   If a file has zero content images, proceed directly to 5b.

   b. **Classify** — determine which KB file(s) the content maps to:
      - Prompt engineering tips → `prompt-engineering.md`
      - CLAUDE.md / context management → `context-engineering.md`
      - Workflow / process patterns → `workflow-patterns.md`
      - Agent architecture / personas → `agent-design.md`
      - Memory / persistence / worklogs → `memory-persistence.md`
      - Skills / slash commands / skill design → `skills.md`
      - Hooks / MCP / SDK / CI/CD / plugins → `tools-and-integrations.md`
      - Testing / verification → `testing-verification.md`
      - Failure patterns / anti-patterns → `failure-patterns.md`
      - Project setup / config → `project-setup.md`
      - OpenClaw / autonomous agents → `autonomous-agents.md`
      - Community tips / tools / threads → `community-insights.md`

   c. **Extract** — pull out the key insights, tips, workflows, or patterns. Be concise (3-10 bullet points per source).

   d. **Deduplicate** — read the target KB file and check if the insight already exists. If an insight is a duplicate, skip it but **log the skip** in the processing report (step 9) with a one-line reason:
      - `[source-file.md] → [target.md]: Skipped "[insight title]" — duplicates existing section "[Section Name]"`
      This makes dedup decisions auditable and guards against plausible echo (see failure-patterns.md).

   e. **Append** — add new insights to the target KB file under a `## Recent Additions` section at the bottom (create this section if it does not exist). Format each addition as:
      ```
      ### [Brief Title] (YYYY-MM-DD)
      [Concise extracted insight in bullets]
      *Source: [filename]*
      ```

   f. **Cross-reference** — if the new content relates to concepts in other KB files, add inline cross-references using `(see [concept](filename.md#section-anchor))`.

   g. **Check for contradictions** — if the extracted insight directly contradicts an existing claim in the target KB file, do NOT silently skip it. Instead append to `Knowledge Distillery/DISCREPANCIES.md` using this format:
      ```
      ### [Claim summary] — Contradicted by new source

      **File:** [topic-file.md]
      **Section:** [existing section heading]
      **Current claim:** [what the KB currently says]
      **New source says:** [what the new note says]
      **Source:** [new source filename]
      **Date found:** [today]
      **Status:** Open
      ```
      Still append the new insight to Recent Additions, but note the contradiction in its entry.

   h. **Flag teach-worthy concepts** — if the extracted insight meets any of these criteria, append it to the `## Teaching Candidates` section at the bottom of `Knowledge Distillery/LEARNING-PATH.md`:
      - Concept appears in 3+ different source files (high convergence)
      - Insight was routed to 2+ different KB files (cross-cutting)
      - Introduces a new named workflow, pattern, or framework
      - Contradicts existing practice (logged to DISCREPANCIES.md in step 6g)

      Format each candidate as:
      ```
      - **[Concept name]** — [one-line summary]. Routed to: [target files]. Sources: [count]. Criteria: [which of the 4 above].
      ```

7. **Update Concept Index** — If any new `###` sections were added to Recent Additions that introduce concepts not already in the README.md Concept Index table, append new rows to that table. Include the Impact tier (Foundational, Core, Enhancing, or Reference) based on: Foundational if it changes how you think about AI-assisted work; Core if it is a daily-use pattern; Enhancing if it is a power-user optimization; Reference if it is specialized or niche.

8. **Update provenance:**
   - Add a row to `sources/processing-log.md` for each file processed: `| [date] | [source filename] | [target KB file(s)] | [brief description] |`
   - Add the new source file to `sources/source-index.md` with contribution mappings
   - Add the file to `sources/ingested-files.md` tracker (audit log — append a batch section)
   - Add the file path to `sources/ingested-paths.txt` (fast-lookup index — one path per line, `./` prefix, keep sorted)

9. **Report** — summarize what was processed: how many new files found, how many had content, what insights were extracted, which KB files were updated. Include:
   - Count of contradictions logged to DISCREPANCIES.md (if any)
   - **Dedup skip log** — list every skipped insight with its one-line reason (from step 6d). Format as a table or bullet list at the end of the report so skip decisions are reviewable.
   - **Image Processing Summary** — images found / described / skipped (non-knowledge) / failed. Note if per-file or per-batch cap was reached.

10. **Verify KB health** — After all processing is complete, run these 5 invariant checks:

    1. **Cross-ref integrity:** Scan all edited files for `(see [x](file.md#anchor))` links. Verify each anchor resolves to a real heading in the target file. Report any broken refs.
    2. **No orphan files:** Verify every topic `.md` in `Knowledge Distillery/` is listed in README.md's index.
    3. **Recent Additions backlog:** Confirm no file has Recent Additions entries pending for 3+ sessions.
    4. **Concept Index coverage:** Verify every H2 section in edited topic files maps to a Concept Index entry in README.md.
    5. **Discrepancy resolution:** Check if any open discrepancy in DISCREPANCIES.md is older than 3 sessions.

    Report: `PASS` or `FAIL` for each check. If any fail, list the specific issues.

## Important Rules
- Do NOT modify the main body of KB files — only append to the `## Recent Additions` section
- Do NOT duplicate insights that already exist in the KB — but always log skipped items with a one-line reason (auditable dedup)
- Keep extractions concise — synthesize, don't copy-paste
- Preserve source attribution for every addition
- If a file does not clearly fit any category, add it to `community-insights.md`
- Paths in `ingested-files.md` are relative to the repo root
- **Batch limit:** Process all new files in a single invocation. Use subagents to parallelize reading and classification when there are more than 10 new files
- **Human spot-check:** After the dedup skip log (step 9), present 5 randomly selected dedup skips and ask the user to confirm they agree with the skip decisions before finalizing
