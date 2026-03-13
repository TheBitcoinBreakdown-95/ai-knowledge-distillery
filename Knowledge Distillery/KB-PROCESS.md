# Knowledge Distillery — Process Reference

How the KB works, end to end. Use this to audit, optimize, or teach the system.

---

## The Three Layers

All content moves through three layers as it matures:

| Layer | Location | What Happens | Modified By |
|-------|----------|--------------|-------------|
| **1. Raw Sources** | Source directories (e.g., `Old Notes/`, `Twitter Bookmarks/`, `Claude Code/`) | Original files — untouched, never moved or deleted | Human (drops files in) |
| **2. Recent Additions** | `## Recent Additions` at the bottom of each topic file | Extracted, classified, deduplicated insights staged for review | `/process-notes` |
| **3. Main Body** | Primary sections of each topic file | Fully integrated, reads as one coherent document | `/consolidate-kb` |

**Information loss risk:** None by design. Layer 1 is never modified. Layer 2 to Layer 3 is a move, not a delete — content is relocated from the staging section into the appropriate main body section of the same file. The consolidation command's rules explicitly state "never delete content — only move it."

---

## The 11 Topic Files

Every insight gets routed to exactly one of these during ingestion:

| File | Covers |
|------|--------|
| `prompt-engineering.md` | Prompt techniques, frameworks, anti-slop, meta-prompts |
| `context-engineering.md` | CLAUDE.md, context window, token management, auto memory |
| `workflow-patterns.md` | Vibe Engineering, Ralph loop, orchestration, batch processing |
| `agent-design.md` | Personas, meta-agent, subagents, multi-agent architecture |
| `memory-persistence.md` | Worklogs, claude-mem, decision traces, session continuity |
| `skills.md` | Skills, slash commands, skill design, skill examples |
| `tools-and-integrations.md` | Hooks, MCP servers, SDK, CI/CD, plugins |
| `testing-verification.md` | Verification protocols, invariants, feedback loops |
| `failure-patterns.md` | Named anti-patterns, security risks, debugging |
| `project-setup.md` | Kickoff questions, CLAUDE.md template, /init workflow |
| `autonomous-agents.md` | OpenClaw, brain/muscles, local models, security |
| `community-insights.md` | Curated tips, tools, tech stacks from threads/posts |

**Why 12?** See [DECISIONS.md](DECISIONS.md#decision-11-topic-files-not-fewer-not-more). `skills-and-tools.md` was split into two files (Session 19) because it exceeded 970 lines — a monolith by KB standards. The Concept Index in README.md provides cross-file discovery.

---

## The Commands

### `/process-notes` — Ingestion (Layer 1 → Layer 2)

**What it does:** Scans source directories, finds files not yet tracked, extracts insights, and stages them.

**Step-by-step:**

1. **Read KB structure** — loads README.md to understand topic categories
2. **Read tracker** — loads `sources/ingested-files.md` (list of all previously processed files)
3. **Scan source directories** — finds all `.md` files in 11 configured directories, excluding code files, images, and the Distillery itself
4. **Diff** — compares scanned files against the tracker. Anything not in the tracker is new.
5. **For each new file:**
   - **a. Read it.** Skip if empty, stub (< 5 lines), or link-only bookmark. Log as skipped.
   - **b. Classify** — determine which of the 11 topic files the content maps to
   - **c. Extract** — pull out 3-10 bullet points of key insights (synthesized, not copy-pasted)
   - **d. Deduplicate** — check if the insight already exists in the target file. If duplicate, skip it and **log the reason** (e.g., `Skipped "prompt caching" — duplicates existing section "Prompt Cache Architecture"`). This makes every skip auditable.
   - **e. Append** — add new insights to `## Recent Additions` at the bottom of the target file, formatted with title, date, bullets, and source attribution
   - **f. Cross-reference** — add `(see [concept](file.md#section))` links to related content in other files
   - **g. Contradiction check** — if the new insight contradicts an existing claim, log it to `DISCREPANCIES.md` (not silently merged, not silently dropped)
   - **h. Flag teach-worthy** — if the concept appears in 3+ sources, routes to 2+ files, introduces a new named pattern, or contradicts existing practice, flag it in LEARNING-PATH.md
6. **Update Concept Index** — new concepts get added to README.md's table with an Impact tier
7. **Update provenance** — add entries to `processing-log.md`, `source-index.md`, `ingested-files.md`
8. **Report** — summary of what was processed, including a dedup skip log for review

**Key rules:**
- Never modifies the main body of KB files — only appends to `## Recent Additions`
- Never modifies source files — they are read-only inputs
- Always synthesizes — no copy-paste from sources
- Every skip logged with a reason (guards against "plausible echo" — a failure pattern where the AI confidently claims something was already covered when it wasn't)

---

### `/consolidate-kb` — Promotion (Layer 2 → Layer 3)

**What it does:** Merges staged Recent Additions into the main body of each topic file.

**Step-by-step:**

1. **Read KB structure** from README.md
2. **Check each topic file** for a `## Recent Additions` section
   - Skip files with fewer than 5 entries — **unless** entries have been pending for 3+ sessions (stale rule prevents indefinite limbo)
3. **For each file with entries to consolidate:**
   - a. Read the full file and understand its `##` section structure
   - b. For each `###` entry under Recent Additions:
     - Find the matching main body section by topic
     - Insert the content as a new `###` subsection (remove the date from the heading, keep source attribution)
     - If no matching section exists, create one under the closest thematic parent
   - c. Remove the now-empty `## Recent Additions` heading
   - d. Write the updated file
4. **Preserve cross-references** — no link changes
5. **Update Concept Index** if any newly consolidated sections introduce new concepts
6. **Log** to processing-log.md
7. **Report** — which files were updated, how many entries merged, where each landed

**Key rules:**
- Never deletes content — only moves it
- Never changes voice or style of existing content
- If placement is ambiguous, asks the user
- After consolidation, the file should read as one coherent document with no temporal seams

**Information loss:** None. The content moves from the bottom of the file into the appropriate section of the same file. Source attribution is preserved. Cross-references are preserved.

---

### `/kb-status` — Health Check (Read-Only)

**What it does:** Diagnostic report without modifying anything.

**Checks:**
1. **Pending ingestion** — untracked files in source directories
2. **Recent Additions backlog** — count per file, flags files with 3+ entries as ready for consolidation
3. **Broken cross-references** — validates all `(see [concept](file.md#section))` links resolve
4. **Open discrepancies** — count of unresolved items in DISCREPANCIES.md
5. **KB size** — line count per file and total
6. **Optimization progress** — pending items per phase from OPTIMIZATION-PLAN.md

---

### `/verify-kb [file]` — Fact-Checking (Layer 3 → DISCREPANCIES.md)

**What it does:** Deep-researches claims in a topic file against current web sources.

**Step-by-step:**
1. Read the target topic file
2. Extract verifiable factual claims (tool names, versions, specific workflows, API details — not general principles)
3. Search the web for current documentation and community discussions
4. Classify each claim: Confirmed, Outdated, Wrong, Unverifiable, or Contradicted
5. Log anything not Confirmed to DISCREPANCIES.md with the current claim, what research found, source URL, and date
6. Report: total claims checked, breakdown by classification

**Key rules:**
- Does NOT modify topic files — only writes to DISCREPANCIES.md
- The user decides what to update (this command flags, doesn't fix)
- Conservative: only flags when there's a concrete source showing the claim is wrong

---

### `/audit [path]` — Project Assessment (KB → Real Project)

**What it does:** Audits any project directory against the KB's best practices. This is the feedback loop — the KB isn't just a reference, it checks whether you're actually following what it teaches.

**How it works:**
1. Resolve target directory
2. Load KB context (project-setup, context-engineering, failure-patterns, testing-verification, memory-persistence, skills-and-tools, workflow-patterns)
3. Load check definitions from `templates/audit-checks.md` (24 checks across 6 categories: Foundation, Configuration, Workflow, Memory, Verification, Security)
4. Run all checks: PASS / WARN / FAIL / N/A
5. Compile report: summary scorecard, detailed findings for WARN/FAIL, top 3 recommendations

**Current limitation (Phase 9.3a):** Checks file existence (does CLAUDE.md exist?) but not substantive adherence (does it follow WHAT/WHY/HOW framing? are invariants defined?). Redesign is pending.

---

---

## Provenance System

Three files track where everything came from:

| File | Purpose |
|------|---------|
| `sources/ingested-files.md` | Master list of every file ever scanned — path, status (content/stub/empty/duplicate), and what was extracted |
| `sources/processing-log.md` | Audit trail — date, source file, target KB file(s), brief description |
| `sources/source-index.md` | Maps each KB file to its contributing source files |

This means you can always ask: "Where did this claim come from?" and trace it back to the original note.

---

## Quality Controls

### 5 Health Invariants (from CLAUDE.md)

Binary pass/fail checks. Should be run after any KB edit.

1. **Cross-ref integrity** — every `(see [x](file.md#anchor))` link resolves to a real heading
2. **No orphan files** — every topic `.md` is listed in README.md's index
3. **Recent Additions backlog** — no file has entries pending for 3+ sessions
4. **Concept Index coverage** — every H2 section in topic files maps to a Concept Index entry
5. **Discrepancy resolution** — no open discrepancy older than 3 sessions

### DISCREPANCIES.md

A review queue for the human. Entries come from two sources:
- `/process-notes` step 5g — new content contradicts existing claims
- `/verify-kb` — web research finds a claim is outdated/wrong

Each entry has: current claim, contradicting source, date found, status (Open/Resolved).

### Auditable Dedup

Every time `/process-notes` skips an insight as a duplicate, it logs a one-line reason. This guards against "plausible echo" — where the AI confidently says something was already covered when it actually wasn't.

### 5 Don't Rules (from CLAUDE.md)

1. Don't copy-paste from source notes — always synthesize
2. Don't create new topic files without checking if an existing one covers the concept
3. Don't mark items as "duplicate" without verifying the existing entry captures the same nuance
4. Don't modify source files — they are read-only inputs
5. Don't consolidate Recent Additions sections with fewer than 5 entries (unless stale for 3+ sessions)

---

## Concept Index and Learning Path

- **Concept Index** (in README.md) — table mapping every major concept to its file, section, and Impact tier (Foundational, Core, Enhancing, Reference)
- **LEARNING-PATH.md** — curated progression for humans learning the material. 30 entries across 4 levels with prerequisites and depth estimates.
- `/process-notes` maintains both: step 5h flags teach-worthy concepts, step 6 adds new Concept Index entries with Impact tiers.

---

## Decision Traces

[DECISIONS.md](DECISIONS.md) records 11 major architectural choices with context, alternatives considered, decision, and rationale. Examples:
- Why 11 topic files (not fewer, not more)
- Why tracking-based ingestion (not inbox/file-moving)
- Why synthesis over RAG
- Why the staging pattern (Recent Additions before main body)
- Why publish the system, not the content

---

## Current State

- **Scale:** ~160 source files compressed to 11 topic files (~6,500+ lines)
- **Optimization:** Phases 1-3, 7, 8 complete. Phase 9.1-9.2 complete. Pending: 9.3a (redesign /audit), consolidation of 59 Recent Additions.
- **Full history:** SESSION-HISTORY.md (sessions 9-19) + SESSION-ARCHIVE.md (Sessions 1-8)
- **Tracking:** OPTIMIZATION-PLAN.md (living optimization tracker with per-session notes)

---

## Worked Example: Processing a New Note

Say you drop a file `New-Prompting-Tips.md` into `AI Notes/Threads/`:

1. **You run `/process-notes`**
2. The command scans `Threads/` and finds `New-Prompting-Tips.md` is not in `ingested-files.md`
3. It reads the file. The file has 20 lines of real content — not a stub.
4. It classifies the content: most tips are about prompt structure → routes to `prompt-engineering.md`
5. It extracts 5 key insights as concise bullets
6. It reads `prompt-engineering.md` and checks for duplicates:
   - Insight 1 ("use XML tags for structure") — already in the "Structuring Prompts" section → **skipped**, logged: `Skipped "XML tags" — duplicates existing section "Structuring Prompts"`
   - Insight 2 ("chain-of-thought for math") — already covered → **skipped**, logged
   - Insight 3 ("reverse prompting technique") — new! Not in the file.
   - Insight 4 ("few-shot with edge cases") — new!
   - Insight 5 ("temperature 0 for deterministic output") — new!
7. Insights 3-5 get appended to `prompt-engineering.md` under `## Recent Additions`:
   ```
   ### Reverse Prompting (2026-03-01)
   - Have the model generate the prompt that would produce a given output
   - Useful for reverse-engineering effective prompt patterns
   *Source: Threads/New-Prompting-Tips.md*
   ```
8. Cross-reference added: `(see [prompt entropy](failure-patterns.md#the-four-named-patterns))`
9. No contradictions found.
10. Concept Index updated if "reverse prompting" is a new concept.
11. Provenance files updated. Report generated.

**Later, you run `/consolidate-kb`:**

12. It sees `prompt-engineering.md` has 3 Recent Additions (meets threshold).
13. "Reverse Prompting" fits under the existing `## Advanced Techniques` section → moved there as a `###` subsection, date removed, source kept.
14. "Few-shot with edge cases" fits under `## Example-Based Prompting` → moved there.
15. "Temperature settings" fits under `## Model Parameters` → moved there.
16. The `## Recent Additions` heading is removed.
17. `prompt-engineering.md` now reads as one document — no seams visible.

The original `New-Prompting-Tips.md` in `Threads/` is untouched throughout.
