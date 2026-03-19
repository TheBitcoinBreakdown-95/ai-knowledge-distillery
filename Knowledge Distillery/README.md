# AI Knowledge Distillery

A synthesized, deduplicated reference extracted from ~160 source files of AI/LLM notes. Each file below is self-contained and optimized for quick scanning — headers, bullets, tables, cross-references.

---

## Why This Exists

Most AI knowledge management is **accumulation** — save articles, hope you remember them, lose them to context window compaction. This system is **synthesis**: raw inputs are transformed into a verified, deduplicated reference that improves over time.

### The problem with existing approaches

| Approach | What happens to knowledge |
|----------|--------------------------|
| **OpenClaw / agent memory** | Articles get summarized into per-agent memory. Subject to compaction. Duplicates pile up. Contradictions go unnoticed. No provenance — 3 months later the agent "knows" something but can't say where it learned it. Knowledge is siloed per-agent. |
| **Claude Code / co-work** | Knowledge lives in conversation context (gone when session ends) or CLAUDE.md (persistent but flat, no system ensuring lessons get captured). Stale advice sits forever. No way to ask "am I following what I know?" |
| **RAG / vector search** | Retrieves relevant chunks but doesn't synthesize. 5 articles about the same topic = 5 separate results, not one unified answer. No contradiction detection. No verification against current sources. |

### What the Distillery does differently

**Synthesis over retrieval.** When 5 articles discuss prompting, they don't become 5 memory entries — they become one synthesized prompting guide where each concept has a single home, cross-referenced everywhere else.

**Contradiction detection.** When new information contradicts existing claims, it's flagged automatically to [DISCREPANCIES.md](DISCREPANCIES.md) for human review — not silently stored alongside the old version.

**Provenance tracking.** Every claim traces back to its original source via [source-index.md](sources/source-index.md). You can always ask "where did this come from?" and get an answer.

**Verification pipeline.** `/verify-kb` checks claims against current web sources. Knowledge that goes stale gets flagged, not quietly trusted.

**Actionable feedback loop.** `/audit` compares your actual project setup against KB best practices and tells you the gaps. This closes the loop between knowing and doing — the KB isn't just a reference, it feeds back into every project via CLAUDE.md updates.

**Compounding, not decaying.** Agent memory decays (compaction eats it, sessions end). The Distillery compounds — each new source makes the whole KB better, not just bigger. Duplicates are merged. Contradictions are surfaced. Nuances are integrated.

**Real-time coaching layer.** The KB doesn't just sit there waiting to be read. A coaching layer (`.claude/rules/coaching.md`) applies KB best practices proactively during work -- nudging specificity, verifying artifacts before marking done, and prompting kickoff questions on ambiguous tasks. Suggestions are soft (never blocking) and cite the KB source, so you learn the patterns by using them.

**Best practices integrated into workflow.** Knowledge flows back into every session via rules, hooks, and audit checks -- not as documentation you have to remember to read, but as active enforcement wired into how Claude operates. When `/consolidate-kb` merges new insights, it checks whether they should update workspace rules, coaching triggers, or audit criteria. The teaching queue (`.claude/rules/teaching-queue.md`) tracks concepts you haven't adopted yet and surfaces them when naturally relevant to your current task.

### The pipeline

```
Raw notes/articles/bookmarks
    → /process-notes (extract, classify, deduplicate, detect contradictions)
        → Synthesized KB (one concept = one place, cross-referenced)
            → /consolidate-kb (merge into main body + framework impact check)
                → Framework updates (rules, coaching, audit checks, CLAUDE.md)
            → /verify-kb (is this still true?)
            → /audit (are we actually doing this?)
            → Coaching layer (real-time suggestions during work)
            → Teaching queue (surface unused concepts when relevant)
```

The framework impact check during `/consolidate-kb` closes the loop: new knowledge doesn't just sit in the KB -- it flows back into the workspace rules, coaching layer, audit checks, and CLAUDE.md files that govern how every project operates. No separate command needed; the user is prompted inline during consolidation and approves or declines each change.

An agent reading articles gives you: `articles → memory → hope`.
The Distillery gives you: `articles → synthesis → verification → coaching → enforcement`.

---

## The Three Distillation Layers

Content flows through three layers as it matures from raw notes into verified reference material:

| Layer | Where It Lives | What Happens |
|-------|---------------|--------------|
| **1. Raw sources** | Your source directories (any folders you configure) | Original articles, threads, notes — untouched. Never moved or deleted. |
| **2. Recent Additions** | `## Recent Additions` sections at the bottom of topic files | `/process-notes` extracts, classifies, deduplicates, and appends new insights here. Content is usable but not yet integrated into the main narrative. |
| **3. Main body** | The primary sections of each topic file | `/consolidate-kb` merges Recent Additions into the main body. Content reads as one coherent reference with no temporal seams. |

The system is designed so that anyone forking this project can follow the same pipeline: drop notes into source directories, run `/process-notes` to extract into layer 2, run `/consolidate-kb` to promote to layer 3. Provenance is tracked at every step via `sources/source-index.md`.

---

## Retrieval Layer (Local Search Engine)

The KB includes a local semantic search engine exposed as an MCP server. Claude can search across all 12 topic files on demand without loading them entirely -- hybrid keyword + vector search returns just the relevant sections.

### How It Works

```
Query ("how to write CLAUDE.md")
    -> BM25 keyword search (exact term matching)
    -> Vector search via Ollama mxbai-embed-large (semantic similarity)
    -> Reciprocal Rank Fusion (merges both result sets)
    -> Top 3 results with full text, rest as previews
```

Falls back to keyword-only if Ollama is unavailable.

### Three MCP Tools

| Tool | What It Does |
|------|-------------|
| `search_kb` | Hybrid semantic + keyword search across all KB files. Returns ranked sections. |
| `list_topics` | Lists all 12 topic files with their H2 section headings. Browse before searching. |
| `get_section` | Retrieves a specific section by file name and heading. Fuzzy matching supported. |

### Infrastructure

| Component | Location | Purpose |
|-----------|----------|---------|
| `kb-mcp/chunker.py` | Splits topic files into sections (one per H2 heading) | Indexing |
| `kb-mcp/indexer.py` | Embeds sections via Ollama, stores in LanceDB + BM25 index | Indexing |
| `kb-mcp/kb_mcp_server.py` | FastMCP server exposing the three tools | Runtime |
| `kb-mcp/eval.py` | 30-query evaluation harness for search quality | Testing |
| `.mcp.json` (workspace root) | Claude Code MCP config pointing to the server | Config |

### Keeping the Index Current

- **Automatic:** A reindex hook triggers `indexer.py --changed` when KB files are edited through Claude. Only changed files re-embed.
- **Manual:** After editing KB files outside Claude: `cd kb-mcp && .venv/Scripts/python indexer.py --changed`
- **Full rebuild:** `cd kb-mcp && .venv/Scripts/python indexer.py` (all chunks, ~3 minutes)

### Requirements

- Python 3.10+ with venv at `kb-mcp/.venv/`
- Ollama running locally with `mxbai-embed-large` model
- LanceDB and FastMCP in the venv (`kb-mcp/requirements.txt`)

---

## Quick Navigation

| If you want to... | Read this |
|---|---|
| Write better prompts | [prompt-engineering.md](prompt-engineering.md) |
| Set up a new project with Claude Code | [project-setup.md](project-setup.md) |
| Choose a development workflow | [workflow-patterns.md](workflow-patterns.md) |
| Design an agent system (personas, subagents) | [agent-design.md](agent-design.md) |
| Add skills or slash commands | [skills.md](skills.md) |
| Add hooks, MCP servers, or SDK integrations | [tools-and-integrations.md](tools-and-integrations.md) |
| Manage memory across sessions | [memory-persistence.md](memory-persistence.md) |
| Set up verification and testing gates | [testing-verification.md](testing-verification.md) |
| Understand common failure patterns | [failure-patterns.md](failure-patterns.md) |
| Configure CLAUDE.md and context | [context-engineering.md](context-engineering.md) |
| Run an autonomous 24/7 agent (OpenClaw) | [autonomous-agents.md](autonomous-agents.md) |
| Browse community tips and tools | [community-insights.md](community-insights.md) |
| Understand the /kickoff command | [kickoff-guide.md](kickoff-guide.md) (guide) / [commands/kickoff.md](commands/kickoff.md) (source) |
| Search the KB semantically | Use `search_kb` MCP tool (see [Retrieval Layer](#retrieval-layer-local-search-engine)) |
| Understand why we built it this way | [DECISIONS.md](DECISIONS.md) |
| Understand the KB pipeline internals | [KB-PROCESS.md](KB-PROCESS.md) |

---

## Concept Index

Moved to [CONCEPT-INDEX.md](CONCEPT-INDEX.md) (339 entries, not published to GitHub). Use `search_kb` MCP tool for concept lookup, or [LEARNING-PATH.md](LEARNING-PATH.md) for curated progression.

---

## For AI Agents Reading This KB

1. **Read this README first.** It is your map. If the `kb-retrieval` MCP server is available, use `search_kb` for targeted queries instead of reading entire files.
2. **Each KB file is self-contained.** You do not need to read all files.
3. **Start with the file matching your current task** using the Quick Navigation table above.
4. **Follow cross-references only when needed.** Each file links to related files with `(see [concept](file.md#section))` format.
5. **The two foundational files** are `prompt-engineering.md` and `context-engineering.md`. Most other files assume familiarity with these concepts.
6. **For original source material** (full articles, transcripts, video notes), check `sources/source-index.md` for the mapping.
7. **To build new workflows**, combine patterns from `workflow-patterns.md` with skills from `skills.md`, tools from `tools-and-integrations.md`, and verification from `testing-verification.md`.

---

## Adding New Notes

1. Drop notes anywhere in the configured source directories
2. Run `/process-notes` -- Claude scans all source directories, compares against tracked files, and processes only new (untracked) files
3. New content appears in `## Recent Additions` sections at the bottom of updated KB files
4. Processing is logged in provenance files under `sources/`

---

## Source Attribution

See [sources/source-index.md](sources/source-index.md) for a complete mapping of every KB file to its original source material.
