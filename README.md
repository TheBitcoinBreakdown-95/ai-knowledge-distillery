# AI Knowledge Distillery

**Stop saving articles you'll never find again.** This is a complete system for turning raw AI/LLM notes into a verified, searchable knowledge base that your AI agent actually uses -- with coaching, verification, and a feedback loop that makes every session smarter than the last.

Built for Claude Code. Forkable. Replace our content with your domain and the pipeline still works.

---

## The Problem

You read a great article about prompt engineering. You save it. Three months later, your agent gives you bad prompting advice because that article is buried in a folder, compacted out of memory, or contradicted by something newer you also saved. You know better than your tools do.

The Knowledge Distillery fixes this. It takes raw notes and transforms them into a **synthesized, deduplicated, cross-referenced** reference -- then wires it into your workflow so the knowledge gets used automatically, not just stored.

```
What most people have:  articles -> memory -> hope
What this gives you:    articles -> synthesis -> verification -> coaching -> enforcement
```

---

## What You Get

**12 topic files** covering AI/LLM best practices -- prompting, context engineering, agent design, memory, skills, testing, failure patterns, tools, workflows, project setup, autonomous agents, and community insights. Each file is self-contained, scannable, and cross-referenced.

| Metric | Value |
|--------|-------|
| Source files processed | 160+ (articles, threads, course notes, bookmarks) |
| Topic files | 12 (synthesized, cross-referenced) |
| Total KB size | ~10,300 lines across 12 topic files |
| Concepts (H3 sections) | 550+ |
| Cross-references | 267 inline links between files |
| Learning path entries | 30 curated across 4 levels |
| Health invariants | 4 (all passing) |
| Architectural decisions documented | 15+ |

**6 slash commands** that turn the KB into an active tool:

| Command | What it does |
|---------|-------------|
| `/kickoff [task]` | Pre-work brief -- queries the KB for relevant practices, anti-patterns, and verification patterns before you start. [Full guide](Knowledge%20Distillery/kickoff-guide.md) |
| `/audit [path]` | Gap analysis -- compares your project setup against KB best practices and tells you what's missing |
| `/process-notes` | Ingestion -- scans source directories, classifies, deduplicates, detects contradictions, appends to KB |
| `/consolidate-kb` | Promotion -- merges staged content into the main body + checks for framework-level impact |
| `/verify-kb [file]` | Fact-checking -- deep-researches KB claims against current web sources, flags what's stale |
| `/kb-status` | Health check -- pending ingestion, backlog, broken cross-refs, KB size |

**A pre-work brief system** ([`/kickoff`](Knowledge%20Distillery/kickoff-guide.md)) that queries the KB before you start any non-trivial task. It reads your project context, generates 10-30 targeted searches across the KB, and presents a structured brief: relevant practices, anti-patterns, failure modes, verification plan, and applicable invariants. Three modes:

- **Task brief** -- you specify the task, it pulls everything the KB knows that's relevant
- **Setup brief** -- new project with no CLAUDE.md? It detects what's missing, asks the right questions, and proposes a setup plan
- **Ready check** -- initialized project, no task given? It shows project health and open tracker items, then asks what you're working on

Think of it as a senior colleague saying "here's what I'd keep in mind before starting this" -- except backed by 160+ synthesized sources instead of anecdotes.

**A coaching layer** that applies KB best practices in real time. `/kickoff` answers from the KB; coaching asks *you* for missing context. They complement each other:

- **Adaptive Kickoff** -- asks clarifying questions on ambiguous tasks before you waste a generation
- **Specificity Nudge** -- catches underspecified requests ("A few details would help me get this right on the first try...")
- **Verification Before Done** -- refuses to self-report "done" without evidence. "I updated the file" is not verification; "I updated the file and confirmed the new function is present at line 42" is

Every suggestion cites the KB source. Every suggestion is soft -- say "just do it" to skip. You learn the patterns by seeing them applied, not by reading a manual.

**A soul** ([SOUL.md](Knowledge%20Distillery/SOUL.md)) that gives the agent a KB-aware identity -- its default instinct is to check the KB before advising, cite sources, and use available tools. This is what makes the difference between a generic assistant and a working partner backed by verified knowledge.

**A local search engine** (MCP server) with hybrid BM25 + vector search across all topic files. Claude queries it on demand -- no need to load entire files into context.

---

## Quick Start

1. **Fork this repo**
2. **Read the topic files** that match your current work (see [What's Inside](#whats-inside) below)
3. **Run `/kickoff` on your first task** -- it queries the KB and tells you everything relevant before you start
4. **Copy the [commands/](Knowledge%20Distillery/commands/) to your `.claude/commands/`** to get `/kickoff`, `/audit`, etc.
5. **Set up the search engine** (optional): see [kb-mcp/](kb-mcp/) for the MCP server setup
6. **Drop your own notes** into a source directory, run `/process-notes`, and the pipeline handles the rest

To replace our content with your domain: keep the file structure, clear the topic files, and start ingesting your own sources. The pipeline, commands, and coaching layer work with any subject matter.

---

## What's Inside

### Topic Files (the knowledge)

| File | Lines | Covers |
|------|-------|--------|
| [prompt-engineering.md](Knowledge%20Distillery/prompt-engineering.md) | 493 | Prompt techniques, specificity, anti-slop, spec-driven development |
| [context-engineering.md](Knowledge%20Distillery/context-engineering.md) | 644 | CLAUDE.md design, context window management, progressive disclosure |
| [workflow-patterns.md](Knowledge%20Distillery/workflow-patterns.md) | 974 | Development workflows, session patterns, multi-agent coordination |
| [agent-design.md](Knowledge%20Distillery/agent-design.md) | 817 | Personas, sub-agents, meta-agent architecture, agent teams |
| [memory-persistence.md](Knowledge%20Distillery/memory-persistence.md) | 620 | 4-layer memory model, worklogs, cross-session memory, QMD, decision traces |
| [skills.md](Knowledge%20Distillery/skills.md) | 745 | Skill design, lifecycle, slash commands, skill graphs, thin skills principle |
| [tools-and-integrations.md](Knowledge%20Distillery/tools-and-integrations.md) | 933 | 16 hook event types, MCP servers, SDK, CI/CD, plugins, voice mode, remote control |
| [testing-verification.md](Knowledge%20Distillery/testing-verification.md) | 509 | Binary pass/fail, invariants, feedback loops, verification protocols |
| [failure-patterns.md](Knowledge%20Distillery/failure-patterns.md) | 464 | 4 named patterns (context pollution, plausible echo, premature completion, vision compression) |
| [project-setup.md](Knowledge%20Distillery/project-setup.md) | 505 | 8 kickoff questions, CLAUDE.md template, /init workflow, settings |
| [autonomous-agents.md](Knowledge%20Distillery/autonomous-agents.md) | 1077 | 24/7 agents, security hardening, cost anatomy, model routing |
| [community-insights.md](Knowledge%20Distillery/community-insights.md) | 922 | Community tools, local AI setups, marketing tactics, cool projects |

### Project Docs (the system)

| File | Purpose |
|------|---------|
| [SOUL.md](Knowledge%20Distillery/SOUL.md) | Agent identity -- KB-aware working partner instincts |
| [kickoff-guide.md](Knowledge%20Distillery/kickoff-guide.md) | Comprehensive /kickoff command reference (3 modes, best practices) |
| [commands/kickoff.md](Knowledge%20Distillery/commands/kickoff.md) | The actual /kickoff command source (copy to `.claude/commands/`) |
| [LEARNING-PATH.md](Knowledge%20Distillery/LEARNING-PATH.md) | Curated 4-level learning progression (30 entries) |
| [DECISIONS.md](Knowledge%20Distillery/DECISIONS.md) | 15+ architectural decision traces with rationale |
| [DISCREPANCIES.md](Knowledge%20Distillery/DISCREPANCIES.md) | Review queue for outdated or contradicted claims |
| [KB-PROCESS.md](Knowledge%20Distillery/KB-PROCESS.md) | Pipeline internals and worked examples |
| [sources/source-index.md](Knowledge%20Distillery/sources/source-index.md) | Maps every KB claim to its original source |

---

## How It Works

### The Pipeline

```
Raw notes/articles/bookmarks
    -> /process-notes (extract, classify, deduplicate, detect contradictions)
        -> Synthesized KB (one concept = one place, cross-referenced)
            -> /consolidate-kb (merge into main body + framework impact check)
                -> Framework updates (rules, coaching, audit checks)
            -> /verify-kb (is this still true?)
            -> /audit (are we actually doing this?)
            -> /kickoff (brief me before I start this task)
            -> Coaching layer (real-time suggestions during work)
```

### Three Distillation Layers

Content matures through three layers:

| Layer | Where | What Happens |
|-------|-------|--------------|
| **1. Raw** | Your source directories | Original articles and notes -- untouched, never moved |
| **2. Staged** | `## Recent Additions` in topic files | `/process-notes` extracts and appends here. Usable but not yet integrated |
| **3. Main body** | Primary sections of topic files | `/consolidate-kb` merges staged content in. Reads as one coherent reference |

### The Coaching Loop

The KB is not passive documentation. Three mechanisms keep it active:

- **Coaching rules** fire on specific triggers -- ambiguous requests get kickoff questions, missing constraints get specificity nudges, completed tasks get verification checks. Each cites the KB source.
- **Teaching queue** tracks 5 KB concepts you haven't adopted yet and surfaces them when naturally relevant to your current task. You learn the KB by working, not by reading.
- **Framework impact checks** during consolidation ask: "does this new insight change how the workspace should operate?" New best practices flow back into rules, coaching triggers, and audit criteria automatically.

### It Keeps Itself Honest

4 health invariants run after every edit. All binary pass/fail:

1. **Cross-ref integrity** -- every internal link resolves to a real heading
2. **No orphan files** -- every topic file is indexed
3. **Recent Additions backlog** -- nothing sits unprocessed for more than 3 sessions
4. **Discrepancy resolution** -- no contradiction stays open longer than 3 sessions

### It Evolves Without Bloating

- **Thin skills principle** -- commands are ~40-line orchestrators that reference templates, not 200-line monoliths
- **Consolidation thresholds** -- new content stages in "Recent Additions" before merging into the main body, preventing churn
- **Auditable dedup** -- every skip decision is logged with a one-line reason, guarding against the "plausible echo" failure pattern
- **Provenance tracking** -- every claim traces back to its original source via [source-index.md](Knowledge%20Distillery/sources/source-index.md)

---

## Search and Retrieval

The KB includes a local MCP server for semantic search, plus `/kickoff` as the primary retrieval interface for task-specific knowledge.

| Tool | What It Does |
|------|-------------|
| `/kickoff [task]` | Highest-level retrieval -- generates 10-30 queries across the KB based on your project and task, returns a structured brief. [Full guide](Knowledge%20Distillery/kickoff-guide.md) |
| `search_kb` | Hybrid BM25 + vector search across all KB files. Returns ranked sections. Used by `/kickoff` internally and available for ad-hoc queries. |
| `list_topics` | Lists all 12 topic files with their H2 headings. Browse before searching. |
| `get_section` | Retrieves a specific section by file and heading. Fuzzy matching supported. |

### Why LanceDB

| Component | Why This |
|-----------|----------|
| **LanceDB** (not ChromaDB) | Built-in hybrid BM25+vector search. No server process. Apache Arrow-native |
| **Hybrid BM25+vector** (not keyword-only) | BM25 alone fails on conceptual queries. Vector alone misses exact terms. Hybrid gets both |
| **Section-level chunks** (not paragraphs) | Each H2 heading becomes one chunk. Preserves context that paragraph chunking destroys |
| **MCP server** (not subprocess calls) | Claude Code native integration. 3 tools exposed directly |
| **CAG fallback** | At ~37K tokens, full context loading beats retrieval on accuracy (ICML 2025). Retrieval adds value for source corpus, constrained context, and cross-topic discovery |

```bash
cd kb-mcp
python -m venv .venv
.venv/Scripts/activate  # or source .venv/bin/activate on Linux/Mac
pip install -r requirements.txt
python indexer.py        # build the index
```

`/kickoff` works without the MCP server but produces better results with it.

---

## For AI Agents

1. **Read [SOUL.md](Knowledge%20Distillery/SOUL.md) first.** It defines your relationship to this KB -- check it before advising, cite sources, use available tools.
2. **This README is your map.** Use the tables above to find the right file for your current task.
3. If `search_kb` is available, use it for targeted queries instead of reading entire files.
4. **Each file is self-contained.** You do not need to read all files.
5. **Follow cross-references only when needed.** Format: `(see [concept](file.md#section))`.
6. **The two foundational files** are `prompt-engineering.md` and `context-engineering.md`. Most others assume familiarity with these.
7. **To build new workflows**, combine patterns from `workflow-patterns.md` + skills from `skills.md` + tools from `tools-and-integrations.md` + verification from `testing-verification.md`.

---

## Architecture

Every major design choice is documented in [DECISIONS.md](Knowledge%20Distillery/DECISIONS.md) with context, alternatives considered, and rationale. Including: why synthesis over RAG, why LanceDB over ChromaDB, why thin skills over monolithic commands, why behavioral coaching over a separate app, and why we raised the consolidation threshold from 3 to 5.

- [DECISIONS.md](Knowledge%20Distillery/DECISIONS.md) -- 15+ decision traces
- [KB-PROCESS.md](Knowledge%20Distillery/KB-PROCESS.md) -- pipeline internals and worked examples
- [sources/source-index.md](Knowledge%20Distillery/sources/source-index.md) -- complete provenance mapping

## License

MIT
