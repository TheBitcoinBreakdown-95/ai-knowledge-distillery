# Knowledge Distillery — Decision Traces

Major architectural choices and the reasoning behind them. Each entry follows the format from [memory-persistence.md](memory-persistence.md#decision-traces-strategic-memory): context, alternatives, decision, rationale.

---

## Decision: 11 Topic Files (Not Fewer, Not More)

- **Context:** The KB needed a structure that balances findability with avoiding fragmentation. Too few files = monoliths. Too many = scattered concepts with unclear homes.
- **Alternatives Considered:**
  - Flat folder of ~30 granular files (one per concept)
  - 3-5 broad category files (e.g., "building", "operating", "debugging")
  - Tag-based system with no fixed file structure
- **Decision:** 11 topic files organized by domain (prompting, context, workflows, agents, memory, skills, testing, failures, setup, autonomous, community).
- **Rationale:** 11 files fit comfortably in context. Each file is self-contained and scannable. The Concept Index in README.md provides cross-file discovery. Granular files would create routing ambiguity during ingestion; broad files would force unrelated concepts together.

---

## Decision: Tracking-Based Ingestion (Not Inbox/File-Moving)

- **Context:** Needed a way to detect new notes without requiring the user to move files to an inbox folder or tag them manually.
- **Alternatives Considered:**
  - Inbox folder pattern (drop files → process → move to archive)
  - Git-based diffing (detect new/changed files via `git status`)
  - Manual file list (user tells the system which files to process)
- **Decision:** `ingested-files.md` tracker. `/process-notes` scans source directories and diffs against the tracker. New files = anything not in the tracker.
- **Rationale:** No file moving means source files stay where they are — the user's folder structure is preserved. No git dependency means this works with any file system. The tracker is human-readable and auditable. Downside: tracker can drift if files are renamed, but this is rare and detectable.

---

## Decision: Synthesis Over RAG

- **Context:** Most knowledge systems use retrieval-augmented generation — embed chunks, search by similarity, return top-k results. Should this KB do the same?
- **Alternatives Considered:**
  - Vector-indexed RAG (MCP server + embeddings)
  - Keyword search over raw notes
  - The current approach: pre-synthesized topic files
- **Decision:** Pre-synthesize into topic files. No retrieval layer.
- **Rationale:** RAG returns 5 chunks about a concept; synthesis gives 1 unified answer. At ~160 source files compressed to 15 topic files, the entire KB fits in context — retrieval adds complexity without benefit. Synthesis also catches contradictions and forces dedup, which RAG cannot. Revisit if scale exceeds context limits (see Phase 4.1 in OPTIMIZATION-PLAN.md).

---

## Decision: Recent Additions Staging Pattern

- **Context:** Ingested content needs to land somewhere before being merged into the main body. Should it go directly into the main narrative, or stage first?
- **Alternatives Considered:**
  - Direct insertion into main body sections during ingestion
  - Separate staging file per ingestion batch
  - `## Recent Additions` section at the bottom of each topic file
- **Decision:** `## Recent Additions` sections at the bottom of each topic file. Promoted to main body by `/consolidate-kb` when 3+ entries accumulate (or after 3 sessions regardless).
- **Rationale:** Direct insertion risks breaking the narrative flow and makes it hard to review what's new. A separate staging file would disconnect additions from their topic context. Inline staging keeps new content co-located with its topic while visually separating it from the verified main body. The 3-entry threshold balances consolidation effort with staleness risk.

---

## Decision: 3-Entry Consolidation Threshold + 3-Session Stale Rule

- **Context:** When should Recent Additions be merged into the main body? Too early = churn. Too late = stale staging area.
- **Alternatives Considered:**
  - Consolidate after every ingestion (immediate)
  - Consolidate on a fixed schedule (weekly)
  - Threshold-based with a staleness backstop
- **Decision:** Consolidate when a file has 3+ Recent Additions entries. Backstop: merge individually after 3 sessions regardless of count.
- **Rationale:** 3 entries provides enough material to synthesize coherently rather than just appending. The 3-session stale rule (added Session 14, from failure-patterns.md > State Corruption) prevents orphaned entries that never reach threshold from accumulating indefinitely.

---

## Decision: No Git for Content Tracking

- **Context:** Should the KB use git history to track changes, or a custom provenance system?
- **Alternatives Considered:**
  - Git-based history (diffs, blame, tags per ingestion batch)
  - Custom provenance: `source-index.md` + `ingested-files.md` + `processing-log.md`
- **Decision:** Custom provenance files, no git dependency for KB operations.
- **Rationale:** The KB lives inside a larger repo (`Ai Playground`) that includes unrelated projects. Git history would mix KB changes with code changes. Custom provenance is human-readable, portable, and doesn't require git literacy. Trade-off: no automatic rollback, but the three-layer structure (raw sources preserved, staging area, main body) provides implicit recovery.

---

## Decision: Publish the System, Not the Content

- **Context:** Phase 6 planning — what goes into the public repo?
- **Alternatives Considered:**
  - Publish everything (notes + synthesized KB + commands)
  - Publish only commands and templates (the system)
  - Publish a curated "starter KB" alongside the system
- **Decision:** Publish the system first (commands, templates, empty KB scaffold). Personal content stays private. Verified starter content may follow as Phase 6.2B.
- **Rationale:** The value is the methodology, not the personal notes. Users fork and build their own KB from their own sources. Publishing raw notes would expose personal context. Publishing synthesized content without verification could spread errors. System-first also means the repo is immediately useful without requiring our specific domain knowledge.

---

## Decision: "Knowledge Distillery" Name

- **Context:** Session 3 — the project needed a name beyond "Knowledge Base."
- **Alternatives Considered:** Knowledge Base, Knowledge Graph, Knowledge Engine, Knowledge Distillery
- **Decision:** Knowledge Distillery.
- **Rationale:** "Base" is generic and implies storage. "Distillery" captures the core value proposition — raw inputs are refined into concentrated, purified output. The metaphor extends naturally: sources are ingredients, ingestion is fermentation, synthesis is distillation, the output is spirit (concentrated essence).

---

## Decision: Thin Skills Pattern for Commands

- **Context:** Self-audit (Session 12) found two commands exceeding 200 lines — audit.md (225 lines) and transition.md (226 lines). The KB's own Thin Skills Principle says good skills are ~40 lines.
- **Alternatives Considered:**
  - Leave as-is (they work)
  - Split into multiple smaller commands
  - Extract templates/check-tables to separate files, keep commands as thin orchestrators
- **Decision:** Extract templates to `.claude/commands/templates/`, keep commands as orchestrators that reference the templates.
- **Rationale:** Splitting into separate commands would break the single-invocation workflow. Extracting templates preserves the one-command interface while keeping the orchestration logic readable. Templates are lazy-loaded — only pulled into context when the command runs.

---

## Decision: Concept Index with Impact Tiers

- **Context:** Phase 7 (teaching layer) — the KB synthesizes well for AI agents but the human needs a filtered view of what matters most.
- **Alternatives Considered:**
  - Separate "highlights" file with curated summaries
  - Tags on each section header (e.g., `[CORE]`, `[ADVANCED]`)
  - Impact column in the existing Concept Index table
- **Decision:** Added Impact column to README.md Concept Index (Foundational, Core, Enhancing, Reference) plus a standalone LEARNING-PATH.md with curated learning progressions.
- **Rationale:** The Concept Index already existed as a navigational aid. Adding Impact tiers reuses the existing structure without creating a parallel index. LEARNING-PATH.md provides the curated sequence for humans who want to learn systematically, not just look things up. Both are maintained by `/process-notes` (step 5h and step 6).

---

## Decision: Auditable Dedup (Log Skip Reasons)

- **Context:** Self-audit (Session 12, finding #6) identified plausible echo risk in dedup — when `/process-notes` skips an item as "duplicate," there's no way to verify the skip was correct.
- **Alternatives Considered:**
  - Trust the dedup (status quo)
  - Full diff log of every comparison
  - One-line skip reasons in the processing report
- **Decision:** One-line skip reasons logged in the processing report (step 8) for every skipped item.
- **Rationale:** Full diffs would be noisy and rarely reviewed. No logging means bad dedup decisions are invisible — a textbook plausible echo. One-line reasons (e.g., "Skipped 'prompt caching' — duplicates existing section 'Prompt Cache Architecture'") are lightweight to produce and easy to spot-check. Added Session 15.

---

## Decision: Split skills-and-tools.md into Two Files (11→12 Topic Files)

- **Context:** Session 18 architecture review found skills-and-tools.md had grown to 993 lines — the largest file by far, covering two distinct domains (skill design vs tool infrastructure).
- **Alternatives Considered:**
  - Keep as one file and rely on internal navigation
  - Split into 3 files (skills, tools, integrations separately)
  - Move only the overflowing sections to other existing files
- **Decision:** Split into `skills.md` (501 lines: skill theory, design, examples, slash commands) and `tools-and-integrations.md` (492 lines: hooks, MCP, SDK, CI/CD, plugins, compound effect). Topic count goes from 11 to 12.
- **Rationale:** Two files keeps each under 500 lines while maintaining coherent themes. The cut is clean — skills are about *what to encode*, tools are about *infrastructure*. Three files would fragment the compound effect section. Moving sections to existing files would make those files overloaded instead. Added Session 19.

---

## Decision: Relocate Misplaced context-engineering.md Sections

- **Context:** Session 18 review identified 4 sections in context-engineering.md that were about tools/agents/setup, not context strategy: SDK architecture, Agent Teams, Tasks System, Running Locally.
- **Alternatives Considered:**
  - Leave them (they were already there)
  - Move to a new "miscellaneous" file
  - Distribute to topically correct existing files
- **Decision:** Move each section to its natural home — SDK to tools-and-integrations.md, Agent Teams + Tasks to agent-design.md, Running Locally to project-setup.md. context-engineering.md dropped from 556 to 472 lines.
- **Rationale:** Every section had an obvious better home. Leaving them created false expectations — readers looking for SDK docs in context-engineering.md, or Agent Teams scattered across two files. The agent-design.md Agent Teams section already said "see context-engineering.md for basics" — merging eliminates the indirection. Added Session 19.

---

## Decision: Batch Limits + Human Spot-Check on /process-notes

- **Context:** Session 16 ingested ~105 files in a single run with ~175 dedup decisions, all unreviewed. Session 18 review flagged this as a quality gate gap.
- **Alternatives Considered:**
  - No limits (status quo)
  - Hard human review of every dedup decision
  - Batch cap + random sample review
- **Decision:** Cap at 20 files per invocation. After processing, present 5 randomly selected dedup skips for human confirmation before finalizing.
- **Rationale:** 20 files is enough for a substantial session without overwhelming review. Reviewing every decision (175 in Session 16) is impractical. Random sampling catches systematic errors (wrong dedup criteria) without requiring exhaustive review. The 5-skip sample is a proportional check — enough to detect patterns, fast enough to not slow the workflow. Added Session 19.

---

## Decision: Raise Consolidation Threshold from 3 to 5

- **Context:** Session 18 review found that 3-entry consolidation batches weren't producing meaningful quality improvements — the overhead of reading and reorganizing the file was barely justified for 3 entries.
- **Alternatives Considered:**
  - Keep at 3 (status quo)
  - Raise to 10 (aggressive batching)
  - Remove threshold entirely (always consolidate)
- **Decision:** Raise to 5, keep the 3-session stale backstop.
- **Rationale:** 5 entries give enough critical mass for intelligent placement — the consolidator can see patterns in where entries cluster. 10 would delay too long, risking large backlog issues like Session 16. The stale backstop (3+ sessions) ensures even 1-2 entries don't sit forever. Added Session 19.

---

## Validation: Knowledge Layer Architecture (Session 30)

A deep research report on Claude Code knowledge layers (`deep-research-report-claudecodeknowledgelayer.md`) independently arrived at many of the same architectural conclusions we built. This section documents where our decisions were validated and where we went beyond the report's recommendations.

### Validated Decisions

**Synthesis over retrieval (Decision: Synthesis Over RAG)**
The report's central thesis is "don't build RAG, use the primitives." Our approach goes further — we don't just consume knowledge through primitives, we *produce* synthesized knowledge from raw sources. The 3-layer distillation pipeline (raw → Recent Additions → main body) has no equivalent in the report. The report assumes knowledge exists in its original form and gets retrieved; we create deduplicated, cross-referenced, single-source-of-truth entries. This is a genuinely novel layer the report doesn't cover.

**Disciplined CLAUDE.md (Decision: context-engineering.md guidance)**
The report warns heavily about CLAUDE.md bloat — "overly long CLAUDE.md causes instruction loss." Our AI Notes CLAUDE.md contains only: commands, structure, conventions, don't rules, invariants. No prose walls. The report's empirical study of 253 public CLAUDE.md files found the same pattern we follow — practical operational guidance over abstract principles.

**Thin skills with templates (Decision: Thin Skills Pattern)**
The report recommends skills as "retrieval wrappers" with supporting files for large references. We implemented this pattern in Session 12 (Phase 9.2c-d) — extracting check tables and step details to `.claude/commands/templates/`, keeping commands as thin orchestrators. The report independently validates this as "cleanest way to encode checklists and debugging playbooks without bloating every session."

**Auto memory index + topic files (Decision: Phase 15.1)**
The report describes the exact pattern we implemented: "`MEMORY.md` acts as a concise always-loaded index (first 200 lines), with topic files read on demand." Our Phase 15.1 restructured MEMORY.md from 131 lines of project detail to a ~45-line index with pointers to 3 detail files (`openclaw-course.md`, `freedomlab.md`, `knowledge-distillery.md`).

**Path-scoped rules (Decision: Phase 15.4)**
The report calls path-scoped rules "the single best noise reduction lever for monorepos." Phase 15.4 created `.claude/rules/kb-editing.md` scoped to `Knowledge Distillery/**/*.md` with 6 editing constraints. The report validates this as reducing token cost and instruction noise.

**Staged implementation (Decision: Optimization Plan structure)**
The report recommends "stage-gated, anti-overengineering" implementation with explicit "stop signs." Our 15-phase optimization plan with dependencies, status tracking, and "parked" items for premature ideas matches this philosophy exactly.

**Subagents for context isolation (Decision: Phase 15.3)**
The report says "use subagents for investigation so verbose exploration doesn't pollute the main context." Phase 15.3 defined 3 specialized agents (kb-researcher, kb-processor, verify-claims) with scoped tool access — read-only for researchers, full access for processors.

**LanceDB hybrid retrieval (Decision: Phase 11)**
The report's Stage 2 recommendation — "hybrid BM25+vector, section-level chunks, MCP server" — is exactly what Phase 11 specifies. Our research (Session 23) independently chose LanceDB for the same reasons the report cites: built-in hybrid search, embedded (no server), section-level retrieval. The report also validates our CAG Note: at ~37K tokens, full context loading beats retrieval on accuracy.

### Where We Exceed the Report

**Verification loops.** The report recommends abstract evaluation frameworks. We have concrete, automated verification: 5 binary health invariants, auto-verify in `/process-notes` and `/consolidate-kb`, contradiction detection logged to DISCREPANCIES.md, `/verify-kb` for deep-research fact-checking against current web sources. This is more rigorous than anything the report prescribes.

**Provenance tracking.** The report mentions source attribution as important but doesn't prescribe a system. We have three provenance files: `source-index.md` (maps claims to sources), `ingested-files.md` (tracks processed files), `processing-log.md` (logs every operation). Full audit trail from raw note to synthesized KB entry.

**Decision traces.** The report mentions ADRs (Architecture Decision Records) as "architecture invariants" to document. We went further with a structured DECISIONS.md capturing context, alternatives, decision, and rationale for every major choice -- this file itself being the evidence.

**Quality gates on ingestion.** The report doesn't address knowledge production quality. We have: batch limits (20 files), human spot-check (5 random dedup reviews), contradiction detection, auditable dedup logging, and a consolidation threshold with staleness backstop. These prevent the "plausible echo" failure pattern the report never considers because it assumes knowledge is consumed, not produced.

**Coaching layer vision.** The report describes a passive knowledge infrastructure -- "use the primitives to surface knowledge." The coaching layer goes beyond: the AI proactively applies KB best practices, pushes back on suboptimal requests, and surfaces workflow optimizations in real time. The report says "make knowledge available." We say "make the AI use it automatically."

---

## Decision: Tier 2 LanceDB Hybrid Retrieval (Not Tier 1 or ChromaDB)

- **Context:** KB is 12 files, ~37K tokens. The coaching layer needs real-time conceptual retrieval. Needed to choose a retrieval tier.
- **Alternatives Considered:**
  - (a) Do nothing -- rely on full-context loading (CAG)
  - (b) Tier 1: BM25-only keyword search over headings, returns file names
  - (c) ChromaDB with vector search
  - (d) Tier 2: LanceDB hybrid BM25+vector over H2 chunks via MCP
  - (e) Tier 3: Full production (GraphRAG, ColBERT)
  - (f) QMD directly (Tobi Lutke's CLI search engine)
- **Decision:** Option (d) -- LanceDB hybrid with QMD-inspired pipeline enhancements (query expansion, RRF merging).
- **Rationale:** Tier 1 rejected because BM25-only fails on conceptual queries and returns whole files, not sections. ChromaDB rejected because LanceDB has built-in hybrid BM25+vector (ChromaDB requires bolting on BM25 separately), is embedded (no server), and Apache Arrow-native. Tier 3 unnecessary for a 12-file collection -- confirmed by QMD's production use at similar scale. QMD rejected as direct replacement because it integrates via subprocess calls to OpenClaw's memory_search; our system needs an MCP server for Claude Code. We borrow QMD's pipeline design (query expansion via Claude, Reciprocal Rank Fusion for result merging) while skipping its local reranker/query-expansion models since Claude handles both for free.
- **QMD validation:** QMD (github.com/tobi/qmd) uses the same hybrid BM25+vector approach and markdown heading-based chunking, production-proven by Shopify CEO's daily use. Confirms our architecture is sound and Tier 3 is unnecessary.
- **CAG note:** For the synthesized KB (~37K tokens), full context loading (CAG) beats retrieval on accuracy AND speed (ICML 2025). Retrieval is for: source corpus (~1M tokens), constrained context, cross-topic discovery.

---

## Decision: Transient Image Enrichment (Not Pre-Processing or Ignoring)

- **Context:** ~265 content images across source files contain visual knowledge not captured in surrounding text. Pipeline was text-only.
- **Alternatives Considered:**
  - (a) Ignore images permanently
  - (b) Pre-process images into separate description files
  - (c) Inline transient enrichment during ingestion
- **Decision:** Option (c) -- transient enrichment. Vision-generated descriptions are injected during `/process-notes` but not persisted as standalone files.
- **Rationale:** Minimal addition to existing pipeline. No new files to maintain. Graceful degradation (missing/broken images logged, never fatal). Skip rules (badges, logos, GIF, SVG) + caps (10 per file, 40 per batch) prevent waste. Siftly's structured vision output (OCR, tags, classification) may improve on free-text descriptions -- evaluation planned.

---

## Decision: Behavioral Instructions for Coaching (Not Separate App)

- **Context:** KB has 30+ concepts but they're passive -- the AI only uses them when explicitly asked. The AI should internalize best practices and actively apply them.
- **Alternatives Considered:**
  - (a) Teach via LEARNING-PATH.md (human reads and learns)
  - (b) Build a separate coaching application
  - (c) Behavioral instructions in CLAUDE.md/rules that make AI proactively apply KB practices
- **Decision:** Option (c) -- behavioral instructions with gentle coaching (suggest, don't block) and an escape hatch ("just do it").
- **Rationale:** Zero new infrastructure. Compounds over time as the AI learns user preferences. Human learns through repetition of seeing best practices applied. The coaching layer includes a teaching queue of 5 unused KB concepts taught in dependency order, plus post-task optimization suggestions drawn from KB practices the user hasn't adopted.

---

## Decision: Browser Console Export for Bookmarks (Not Bird CLI or API)

- **Context:** Bird CLI auth broken by Chrome 145 cookie encryption. Manual DevTools cookie extraction was a fragile workaround.
- **Alternatives Considered:**
  - (a) Keep Bird CLI + manual cookie extraction
  - (b) Browser console export (Siftly/gd3kr approach)
  - (c) Twitter API v2 (requires developer account)
  - (d) Third-party export tools (twitter-web-exporter, Chrome extensions)
- **Decision:** Option (b) -- browser console script (`export_bookmarks.js`) + Python parser (`parse_bookmarks.py`).
- **Rationale:** Runs in already-authenticated browser session, zero auth overhead. Three proven open-source scripts validated the pattern. fxtwitter API provides full text enrichment without auth. Output format matches Bird CLI for pipeline compatibility. Parser supports `--skip-existing` for incremental runs.
