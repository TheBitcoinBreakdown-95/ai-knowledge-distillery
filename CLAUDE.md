# AI Notes — Project Instructions

## What This Is
A collection of AI/LLM notes and a synthesized Knowledge Distillery. The raw notes live in topic folders (`Andrew Vibe Coding/`, `Claude Code/`, `Clawdbot aka Openclaw/`, `Threads/`, etc.). The synthesized reference lives in `Knowledge Distillery/`.

## Knowledge Distillery Structure
```
Knowledge Distillery/
  README.md                    # Index, concept glossary, AI reading instructions
  LEARNING-PATH.md             # 4-level curated learning paths (30 entries)
  OPTIMIZATION-PLAN.md         # Living optimization tracker (9 phases)
  DISCREPANCIES.md             # Review queue: outdated/wrong/contradicted claims
  DECISIONS.md                 # Architectural decision traces (why we built it this way)
  prompt-engineering.md        # Master prompting guide + templates
  context-engineering.md       # CLAUDE.md, context window, memory management
  workflow-patterns.md         # Vibe Engineering, Ralph loop, orchestration
  agent-design.md              # Personas, meta-agent, multi-agent architecture
  memory-persistence.md        # Worklogs, claude-mem, session continuity
  skills.md                    # Skills, slash commands, skill design
  tools-and-integrations.md    # Hooks, MCP, SDK, CI/CD, plugins
  testing-verification.md      # Verification protocols, invariants, feedback loops
  failure-patterns.md          # Named anti-patterns, security risks
  project-setup.md             # Kickoff questions, CLAUDE.md template, /init
  autonomous-agents.md         # OpenClaw setup, brain/muscles, security
  community-insights.md        # Curated thread tips, tools, tech stacks
  sources/
    source-index.md            # Maps every KB claim to its original file
    ingested-paths.txt         # Fast-lookup index: one path per line, sorted (used by /process-notes to detect new files)
    ingested-files.md          # Audit log: detailed processing history with routing and skip reasons (append-only after processing, read on demand)
    processing-log.md          # Tracks what's been ingested and when
```

## Key Commands
- **`/process-notes`** — Scans source directories, diffs against tracker, classifies, deduplicates, appends to `## Recent Additions`. Logs contradictions to DISCREPANCIES.md. Updates Concept Index.
- **`/consolidate-kb`** — Merges Recent Additions into main body of topic files (only files with 5+ entries, or 3+ sessions stale). Includes a framework impact check: proposes updates to workspace rules, audit checks, or CLAUDE.md files when new knowledge warrants it.
- **`/kb-status`** — Read-only diagnostic: pending ingestion, Recent Additions backlog, broken cross-refs, discrepancies, KB size
- **`/verify-kb [file]`** — Deep-researches claims in a topic file against current web sources. Flags outdated/wrong content to DISCREPANCIES.md
- **`/audit [path]`** — Audits a project directory against KB best practices. Read-only gap analysis with severity tiers and fix recommendations
- **Adding notes** — Drop any file into source directories (`AI Notes/` subfolders or `Clawdbot aka Openclaw/Research/`), then run `/process-notes`
- **Quality checks** — Run `/kb-status` after any KB edit to catch broken cross-refs, stale Recent Additions, or size anomalies

## Conventions
- KB files are synthesized (not copy-paste) — merge insights from multiple sources
- Deduplicate ruthlessly — each concept has ONE primary home
- Cross-reference format: `(see [concept](file.md#section-anchor))`
- Each KB file is self-contained but enriched by cross-references
- No emojis, no prose walls — headers, bullets, tables for scannability
- Source attribution tracked in `sources/source-index.md`
- Major topic sections should include applicability boundaries (best for / bad fit / constraints) and "when not to use this" guidance where relevant -- during consolidation, not retroactively

## Don't Rules
- Don't copy-paste from source notes — always synthesize across multiple sources
- Don't create new topic files without first checking if an existing file already covers the concept
- Don't mark ingested items as "duplicate" without verifying the existing entry captures the same nuance
- Don't modify source files — all files in source directories are read-only inputs
- Don't consolidate Recent Additions sections with fewer than 5 entries (unless stale per the 3-session rule below)
- Don't add non-AI content to community-insights.md — entries must be actionable, AI/LLM-related, and verifiable
- **Don't skip Twitter Bookmarks** — every bookmarked file gets processed into the KB, no exceptions. If content seems off-topic or thin, still extract what's there and route it. The user bookmarked it for a reason.
- **Don't skip "similar" articles** — two authors covering the same topic is NOT a duplicate. Different framing, different details, different replies all have value. Only skip if two files contain byte-for-byte identical content.
- **Don't force-fit content into community-insights.md** — if new learnings don't belong in any existing topic file, recommend creating a new topic file. Ask the user rather than cramming things where they don't belong.
- **Mandatory skip report** — if ANY file is skipped during /process-notes, the processing log MUST include a full itemized table of every skipped file with: file path, complete content summary (not just "thin" or "stub"), and the exact reason for skipping. This is not optional. No spot-check requests — the report IS the verification.

## KB Health Invariants
Binary pass/fail checks. Run after any KB edit. All must pass.

1. **Cross-ref integrity:** Every `(see [x](file.md#anchor))` link resolves to a real heading
2. **No orphan files:** Every topic `.md` in `Knowledge Distillery/` is listed in README.md's index
3. **Recent Additions backlog:** No file has Recent Additions entries pending for 3+ sessions — merge individually if threshold not met
4. **Concept Index coverage:** Every H2 section in topic files maps to a Concept Index entry in README.md
5. **Discrepancy resolution:** No open discrepancy in DISCREPANCIES.md older than 3 sessions

## Build Details
- **Built:** 2026-02-27
- **Source count:** ~160 files compressed to 12 topic files + meta-docs (~7,000+ lines post-consolidation)
- **Implementation plan:** `.claude/plans/compressed-yawning-cloud.md` (full per-file specs, source mappings, verification criteria)
- **Verification passed:** All 30 key concepts present, ~55 source files indexed

## Session Continuity
- At session start, read WORKLOG.md if it exists
- When the user says "save progress": read WORKLOG.md, update with work done, what's next, and any decisions. Keep concise — replace content, don't append.
- Optimization progress tracked in Knowledge Distillery/OPTIMIZATION-PLAN.md
