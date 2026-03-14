# AI Knowledge Distillery

160+ source files distilled into 12 topic files. 550+ concepts. 267 cross-references. A living, evolving reference for AI/LLM best practices -- built with Claude Code, for Claude Code.

This is not a bookmark folder or a RAG index. It is a synthesized, deduplicated, contradiction-checked, source-traced knowledge base that audits your projects, coaches you in real time, and gets better every time you feed it.

---

## What Makes This Different

### It synthesizes, not retrieves

Most knowledge systems store articles and retrieve chunks. Five articles about prompting become five separate results. The Distillery merges them into one entry where each concept has a single home, cross-referenced everywhere else. Duplicates are caught. Contradictions are flagged to [DISCREPANCIES.md](Knowledge%20Distillery/DISCREPANCIES.md) for human review -- not silently stored alongside the old version.

### It coaches you while you work

The KB is not documentation you have to remember to read. A [coaching layer](Knowledge%20Distillery/community-insights.md) (`.claude/rules/coaching.md`) applies best practices proactively during Claude Code sessions:

- **Adaptive Kickoff** -- asks clarifying questions on ambiguous tasks before you waste a generation
- **Specificity Nudge** -- catches underspecified requests ("A few details would help me get this right on the first try...")
- **Verification Before Done** -- refuses to self-report "done" without evidence. "I updated the file" is not verification; "I updated the file and confirmed the new function is present at line 42" is

Every suggestion cites the KB source. Every suggestion is soft -- say "just do it" to skip. You learn the patterns by seeing them applied, not by reading a manual.

### It audits your projects against what you know

`/audit` runs a gap analysis: your actual CLAUDE.md, hooks, skills, testing setup compared against KB best practices. It tells you exactly what you are missing and why it matters -- scored, with fix recommendations. The gap between "I read about it" and "I actually do it" is where most knowledge systems fail. The audit closes that gap.

### It catches contradictions and tracks provenance

Every claim traces back to its original source via [source-index.md](Knowledge%20Distillery/sources/source-index.md). When new information contradicts existing content, it gets flagged automatically -- not silently overwritten. You can always ask "where did this come from?" and get an answer.

### It keeps itself honest

4 health invariants run after every edit. All binary pass/fail:

1. **Cross-ref integrity** -- every internal link resolves to a real heading
2. **No orphan files** -- every topic file is indexed
3. **Recent Additions backlog** -- nothing sits unprocessed for more than 3 sessions
4. **Discrepancy resolution** -- no contradiction stays open longer than 3 sessions

### It evolves without bloating

New sources are continuously integrated via `/process-notes`. But we designed explicitly against overengineering and bureaucratic bloat:

- **Thin skills principle** -- commands are ~40-line orchestrators that reference templates, not 200-line monoliths
- **Consolidation thresholds** -- new content stages in "Recent Additions" before merging into the main body, preventing churn
- **Auditable dedup** -- every skip decision is logged with a one-line reason, guarding against the "plausible echo" failure pattern where the AI convinces itself something is already covered
- **15 architectural decisions documented** in [DECISIONS.md](Knowledge%20Distillery/DECISIONS.md) with context, alternatives, and rationale -- including decisions we rejected and why

---

## The Pipeline

```
Raw notes/articles/bookmarks
    --> /process-notes (extract, classify, deduplicate, detect contradictions)
        --> Synthesized KB (one concept = one place, cross-referenced)
            --> /consolidate-kb (merge into main body + framework impact check)
                --> Framework updates (rules, coaching, audit checks, CLAUDE.md)
            --> /verify-kb (is this still true?)
            --> /audit (are we actually doing this?)
            --> Coaching layer (real-time suggestions during work)
            --> Teaching queue (surface unused concepts when relevant)
```

An agent reading articles gives you: `articles --> memory --> hope`.
The Distillery gives you: `articles --> synthesis --> verification --> coaching --> enforcement`.

---

## Scale and Architecture

| Metric | Value |
|--------|-------|
| Source files processed | 160+ (articles, threads, course notes, bookmarks) |
| Topic files | 12 (synthesized, cross-referenced) |
| Total KB size | ~10,300 lines across 12 topic files |
| Concepts (H3 sections) | 550+ |
| Cross-references | 267 inline links between files |
| Learning path entries | 30 curated across 4 levels |
| Ingested paths tracked | 1,800+ |
| Health invariants | 4 (all passing) |
| Architectural decisions documented | 15 |

### Retrieval: LanceDB Hybrid Search

The KB includes a local semantic search engine as an MCP server. Not because you need it (the full KB fits in context at ~37K tokens), but because targeted retrieval is faster for specific lookups.

| Component | Why This |
|-----------|----------|
| **LanceDB** (not ChromaDB) | Built-in hybrid BM25+vector search. No server process. Apache Arrow-native. ChromaDB requires bolting on BM25 separately |
| **Hybrid BM25+vector** (not keyword-only) | BM25 alone fails on conceptual queries ("how should I structure agent memory?"). Vector alone misses exact terms. Hybrid gets both |
| **Section-level chunks** (not paragraphs) | Each H2 heading becomes one chunk. Preserves context that paragraph chunking destroys |
| **MCP server** (not subprocess calls) | Claude Code native integration. 3 tools: `search_kb`, `list_topics`, `get_section` |
| **CAG fallback** | At ~37K tokens, full context loading (CAG) beats retrieval on accuracy (ICML 2025). Retrieval adds value for the source corpus (~1M tokens), constrained context, and cross-topic discovery |

Compared to QMD (Shopify CEO Tobi Lutke's search engine, 14.5k stars): same architectural approach (BM25+vector, markdown heading chunks), validated independently. We borrow QMD's pipeline design (query expansion, Reciprocal Rank Fusion) while integrating via MCP instead of subprocess calls.

```bash
cd kb-mcp
python -m venv .venv
.venv/Scripts/activate  # or source .venv/bin/activate on Linux/Mac
pip install -r requirements.txt
python indexer.py        # build the index
```

---

## Topic Files

| File | Lines | Covers |
|------|-------|--------|
| [prompt-engineering.md](Knowledge%20Distillery/prompt-engineering.md) | 493 | Prompt techniques, specificity, anti-slop, spec-driven development |
| [context-engineering.md](Knowledge%20Distillery/context-engineering.md) | 644 | CLAUDE.md design, context window management, progressive disclosure |
| [workflow-patterns.md](Knowledge%20Distillery/workflow-patterns.md) | 974 | Vibe Engineering stack, Ralph loop, GSD workflow, batch processing |
| [agent-design.md](Knowledge%20Distillery/agent-design.md) | 817 | Personas, meta-agent, subagents, agent frontmatter, multi-agent architecture |
| [memory-persistence.md](Knowledge%20Distillery/memory-persistence.md) | 620 | 5-layer memory model, worklogs, decision traces, compaction strategies |
| [skills.md](Knowledge%20Distillery/skills.md) | 745 | Skill design, lifecycle, slash commands, skill graphs, thin skills principle |
| [tools-and-integrations.md](Knowledge%20Distillery/tools-and-integrations.md) | 933 | 16 hook event types, MCP servers, SDK, CI/CD, plugins, Cowork |
| [testing-verification.md](Knowledge%20Distillery/testing-verification.md) | 509 | Binary pass/fail, invariants, feedback loops, verification protocols |
| [failure-patterns.md](Knowledge%20Distillery/failure-patterns.md) | 464 | 4 named patterns (context pollution, plausible echo, premature completion, vision compression), troubleshooting taxonomy |
| [project-setup.md](Knowledge%20Distillery/project-setup.md) | 505 | 8 kickoff questions, CLAUDE.md template, /init workflow, settings |
| [autonomous-agents.md](Knowledge%20Distillery/autonomous-agents.md) | 1077 | OpenClaw, brain/muscles, cron architecture, agent economics, security |
| [community-insights.md](Knowledge%20Distillery/community-insights.md) | 922 | Curated community tips, tools, tech stacks, real-world agent deployments |

---

## Quick Start

1. **Browse the knowledge** -- start with [Knowledge Distillery/README.md](Knowledge%20Distillery/README.md) for the full topic index
2. **Follow the learning path** -- [LEARNING-PATH.md](Knowledge%20Distillery/LEARNING-PATH.md) has 30 curated entries across 4 levels (Foundations -> Daily Use -> Power User -> Specialized)
3. **Search semantically** -- the [kb-mcp/](kb-mcp/) search engine exposes 3 MCP tools
4. **Fork and fill** -- the system is designed so you can replace our topic files with your own domain knowledge. Drop notes in source directories, run `/process-notes`, repeat

## Architecture Decisions

Every major design choice is documented in [DECISIONS.md](Knowledge%20Distillery/DECISIONS.md) with context, alternatives considered, and rationale. Including: why synthesis over RAG, why LanceDB over ChromaDB, why thin skills over monolithic commands, why behavioral coaching over a separate app, and why we raised the consolidation threshold from 3 to 5.

## License

MIT
