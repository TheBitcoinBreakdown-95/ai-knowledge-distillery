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

**6 slash commands** that turn the KB into an active tool:

| Command | What it does |
|---------|-------------|
| `/kickoff [task]` | Pre-work brief -- queries the KB for relevant practices, anti-patterns, and verification patterns before you start. [Full guide](kickoff-guide.md) |
| `/audit [path]` | Gap analysis -- compares your project setup against KB best practices and tells you what's missing |
| `/process-notes` | Ingestion -- scans source directories, classifies, deduplicates, detects contradictions, appends to KB |
| `/consolidate-kb` | Promotion -- merges staged content into the main body + checks for framework-level impact |
| `/verify-kb [file]` | Fact-checking -- deep-researches KB claims against current web sources, flags what's stale |
| `/kb-status` | Health check -- pending ingestion, backlog, broken cross-refs, KB size |

**A pre-work brief system** ([`/kickoff`](kickoff-guide.md)) that queries the KB before you start any non-trivial task. It reads your project context, generates 10-30 targeted searches across the KB, and presents a structured brief: relevant practices, anti-patterns, failure modes, verification plan, and applicable invariants. Three modes: task brief (you specify the task), setup brief (new project with no CLAUDE.md), and ready check (initialized project, no task given). This is the primary way the KB's knowledge reaches you at the moment it matters.

**A coaching layer** that applies KB best practices in real time -- nudging specificity before you start, verifying artifacts before marking done, and surfacing relevant practices you haven't adopted yet. `/kickoff` answers from the KB; coaching asks *you* for missing context. They complement each other. Suggestions are soft (never blocking) and always cite the KB source, so you learn the system by using it.

**A local search engine** (MCP server) with hybrid BM25 + vector search across all topic files. Claude queries it on demand -- no need to load entire files into context.

**A soul** ([SOUL.md](SOUL.md)) that gives the agent a KB-aware identity: check the KB before advising, cite sources, use available tools. This is what makes the difference between a generic assistant and a working partner backed by verified knowledge.

---

## Quick Start

1. **Fork this repo**
2. **Read the topic files** that match your current work (see [What's Inside](#whats-inside) below)
3. **Copy [commands/](commands/) to your `.claude/commands/`** to get the slash commands
4. **Set up the search engine** (optional): see [kb-mcp/README.md](../kb-mcp/README.md) for the MCP server setup
5. **Drop your own notes** into a source directory, run `/process-notes`, and the pipeline handles the rest

To replace our content with your domain: keep the file structure, clear the topic files, and start ingesting your own sources. The pipeline, commands, and coaching layer work with any subject matter.

---

## What's Inside

### Topic Files (the knowledge)

| File | Covers |
|------|--------|
| [prompt-engineering.md](prompt-engineering.md) | Writing effective prompts, specificity, structured output, few-shot patterns |
| [context-engineering.md](context-engineering.md) | CLAUDE.md design, context window management, progressive disclosure |
| [workflow-patterns.md](workflow-patterns.md) | Development workflows, session patterns, multi-agent coordination |
| [agent-design.md](agent-design.md) | Personas, sub-agents, meta-agent architecture, agent teams |
| [skills.md](skills.md) | Skill design, slash commands, skill graphs, agent authoring |
| [tools-and-integrations.md](tools-and-integrations.md) | Hooks, MCP servers, SDK, CI/CD, plugins, voice mode, remote control |
| [memory-persistence.md](memory-persistence.md) | 4-layer memory model, worklogs, cross-session memory, QMD, decision traces |
| [testing-verification.md](testing-verification.md) | Verification hierarchy, TDD, eval-driven development, artifact checks |
| [failure-patterns.md](failure-patterns.md) | Context corruption, compaction amnesia, premature completion, scope drift |
| [project-setup.md](project-setup.md) | First session checklist, 8 kickoff questions, project bootstrapping |
| [autonomous-agents.md](autonomous-agents.md) | 24/7 agents, security hardening, cost anatomy, model routing |
| [community-insights.md](community-insights.md) | Community tools, local AI setups, marketing tactics, cool projects |

### Project Docs (the system)

| File | Purpose |
|------|---------|
| [SOUL.md](SOUL.md) | Agent identity -- KB-aware working partner instincts |
| [kickoff-guide.md](kickoff-guide.md) | Comprehensive /kickoff command reference |
| [commands/kickoff.md](commands/kickoff.md) | The actual /kickoff command source (copy to `.claude/commands/`) |
| [LEARNING-PATH.md](LEARNING-PATH.md) | Curated 4-level learning progression (30 entries) |
| [DECISIONS.md](DECISIONS.md) | Architectural decision traces with rationale |
| [DISCREPANCIES.md](DISCREPANCIES.md) | Review queue for outdated or contradicted claims |
| [KB-PROCESS.md](KB-PROCESS.md) | Pipeline internals and worked examples |
| [sources/source-index.md](sources/source-index.md) | Maps every KB claim to its original source |

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

---

## Search and Retrieval

The KB includes a local MCP server for semantic search, plus `/kickoff` as the primary retrieval interface for task-specific knowledge.

| Tool | What It Does |
|------|-------------|
| `/kickoff [task]` | Highest-level retrieval -- generates 10-30 queries across the KB based on your project and task, returns a structured brief. [Full guide](kickoff-guide.md) |
| `search_kb` | Hybrid BM25 + vector search across all KB files. Returns ranked sections. Used by `/kickoff` internally and available for ad-hoc queries. |
| `list_topics` | Lists all 12 topic files with their H2 headings. Browse before searching. |
| `get_section` | Retrieves a specific section by file and heading. Fuzzy matching supported. |

MCP server setup: see [kb-mcp/](../kb-mcp/) for installation (Python 3.10+, Ollama, LanceDB). Falls back to keyword-only if Ollama is unavailable. `/kickoff` works without the MCP server but produces better results with it.

---

## For AI Agents

1. **Read [SOUL.md](SOUL.md) first.** It defines your relationship to this KB -- check it before advising, cite sources, use available tools.
2. **This README is your map.** Use the tables above to find the right file for your current task.
3. If `search_kb` is available, use it for targeted queries instead of reading entire files.
4. **Each file is self-contained.** You do not need to read all files.
5. **Follow cross-references only when needed.** Format: `(see [concept](file.md#section))`.
6. **The two foundational files** are `prompt-engineering.md` and `context-engineering.md`. Most others assume familiarity with these.
7. **To build new workflows**, combine patterns from `workflow-patterns.md` + skills from `skills.md` + tools from `tools-and-integrations.md` + verification from `testing-verification.md`.

---

## Architecture

This system was built through deliberate architectural choices, each documented with context, alternatives considered, and rationale:

- [DECISIONS.md](DECISIONS.md) -- 15+ decision traces covering everything from file structure to retrieval strategy to coaching design
- [KB-PROCESS.md](KB-PROCESS.md) -- pipeline internals, worked examples, and the full ingestion/consolidation workflow
- [sources/source-index.md](sources/source-index.md) -- complete provenance mapping from KB claims to original sources
