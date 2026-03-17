# AI Knowledge Distillery -- Project Instructions

## What This Is

A synthesized knowledge base of AI/LLM best practices, extracted from ~160 source files and compressed into 12 topic files. Includes a local semantic search engine (MCP server), slash commands for ingestion and verification, and a curated learning path.

## Structure

```
Knowledge Distillery/
  README.md                    # Index, concept glossary, AI reading instructions
  LEARNING-PATH.md             # 4-level curated learning paths (30 entries)
  DECISIONS.md                 # Architectural decision traces
  DISCREPANCIES.md             # Review queue: outdated/wrong/contradicted claims
  KB-PROCESS.md                # Pipeline internals and worked examples
  prompt-engineering.md        # 12 topic files covering AI/LLM best practices
  context-engineering.md
  workflow-patterns.md
  agent-design.md
  memory-persistence.md
  skills.md
  tools-and-integrations.md
  testing-verification.md
  failure-patterns.md
  project-setup.md
  autonomous-agents.md
  community-insights.md
  sources/
    source-index.md            # Maps every KB claim to its original source
kb-mcp/                        # Local semantic search engine (MCP server)
```

## Commands

- **`/process-notes`** -- Scan source directories, classify, deduplicate, append to Recent Additions. Logs contradictions to DISCREPANCIES.md.
- **`/consolidate-kb`** -- Merge Recent Additions into main body (5+ entries threshold, or 3+ sessions stale).
- **`/kb-status`** -- Read-only diagnostic: pending ingestion, backlog, broken cross-refs, KB size.
- **`/verify-kb [file]`** -- Deep-research claims against current web sources. Flags outdated content.
- **`/audit [path]`** -- Audit a project against KB best practices. Gap analysis with fix recommendations.
- **`/kickoff [task]`** -- KB-powered pre-work brief. Retrieves relevant practices, anti-patterns, and verification patterns before starting. See [kickoff-guide.md](Knowledge%20Distillery/kickoff-guide.md) for full reference.

## Conventions

- KB files are synthesized (not copy-paste) -- merge insights from multiple sources
- Deduplicate ruthlessly -- each concept has ONE primary home
- Cross-reference format: `(see [concept](file.md#section-anchor))`
- Each KB file is self-contained but enriched by cross-references
- No emojis, no prose walls -- headers, bullets, tables for scannability
- Source attribution tracked in `sources/source-index.md`

## Don't Rules

- Don't copy-paste from source notes -- always synthesize across multiple sources
- Don't create new topic files without first checking if an existing file covers the concept
- Don't mark ingested items as "duplicate" without verifying the existing entry captures the same nuance
- Don't modify source files -- all files in source directories are read-only inputs
- Don't consolidate Recent Additions with fewer than 5 entries (unless stale for 3+ sessions)
- Don't skip "similar" articles -- two authors covering the same topic is NOT a duplicate

## KB Health Invariants

Binary pass/fail checks. Run after any KB edit. All must pass.

1. **Cross-ref integrity:** Every `(see [x](file.md#anchor))` link resolves to a real heading
2. **No orphan files:** Every topic `.md` in `Knowledge Distillery/` is listed in README.md's index
3. **Recent Additions backlog:** No file has entries pending for 3+ sessions
4. **Discrepancy resolution:** No open discrepancy in DISCREPANCIES.md older than 3 sessions
