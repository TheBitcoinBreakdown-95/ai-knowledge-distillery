# AI Knowledge Distillery

A knowledge system that synthesizes AI best practices and audits your projects against them.

Built with Claude Code. ~160 source files distilled into 12 topic files covering prompting, context engineering, workflows, agent design, testing, failure patterns, and more.

## What Makes This Different

| Approach | What happens to knowledge |
|----------|--------------------------|
| **Agent memory** | Articles get summarized, subject to compaction, duplicates pile up, contradictions go unnoticed |
| **RAG / vector search** | Retrieves relevant chunks but doesn't synthesize. 5 articles = 5 separate results, not one answer |
| **Knowledge Distillery** | Raw inputs are synthesized into a verified, deduplicated reference. Contradictions are flagged. Claims are traceable to sources. Your projects are audited against what you know |

## The Pipeline

```
Raw notes/articles
    --> /process-notes (extract, classify, deduplicate, detect contradictions)
        --> Synthesized KB (one concept = one place, cross-referenced)
            --> /consolidate-kb (merge into main body)
            --> /verify-kb (is this still true?)
            --> /audit (are we actually doing this?)
```

## Quick Start

1. **Browse the knowledge:** Start with [Knowledge Distillery/README.md](Knowledge%20Distillery/README.md) for the full topic index and concept glossary
2. **Follow the learning path:** [LEARNING-PATH.md](Knowledge%20Distillery/LEARNING-PATH.md) has 30 curated entries across 4 levels
3. **Search semantically:** The [kb-mcp/](kb-mcp/) search engine exposes 3 MCP tools (`search_kb`, `list_topics`, `get_section`)

## Topic Files

| File | Covers |
|------|--------|
| [prompt-engineering.md](Knowledge%20Distillery/prompt-engineering.md) | Prompt techniques, frameworks, anti-slop, meta-prompts |
| [context-engineering.md](Knowledge%20Distillery/context-engineering.md) | CLAUDE.md, context window, token management, auto memory |
| [workflow-patterns.md](Knowledge%20Distillery/workflow-patterns.md) | Vibe Engineering, Ralph loop, orchestration, batch processing |
| [agent-design.md](Knowledge%20Distillery/agent-design.md) | Personas, meta-agent, subagents, multi-agent architecture |
| [memory-persistence.md](Knowledge%20Distillery/memory-persistence.md) | Worklogs, claude-mem, decision traces, session continuity |
| [skills.md](Knowledge%20Distillery/skills.md) | Skills, slash commands, skill design |
| [tools-and-integrations.md](Knowledge%20Distillery/tools-and-integrations.md) | Hooks, MCP servers, SDK, CI/CD, plugins |
| [testing-verification.md](Knowledge%20Distillery/testing-verification.md) | Verification protocols, invariants, feedback loops |
| [failure-patterns.md](Knowledge%20Distillery/failure-patterns.md) | Named anti-patterns, security risks, debugging |
| [project-setup.md](Knowledge%20Distillery/project-setup.md) | Kickoff questions, CLAUDE.md template, /init workflow |
| [autonomous-agents.md](Knowledge%20Distillery/autonomous-agents.md) | OpenClaw, brain/muscles, local models, security |
| [community-insights.md](Knowledge%20Distillery/community-insights.md) | Curated tips, tools, tech stacks from community |

## Local Search Engine (MCP)

The `kb-mcp/` directory contains a hybrid BM25 + vector search engine exposed as an MCP server. Requires Python 3.10+ and Ollama with `mxbai-embed-large`.

```bash
cd kb-mcp
python -m venv .venv
.venv/Scripts/activate  # or source .venv/bin/activate on Linux/Mac
pip install -r requirements.txt
python indexer.py        # build the index
```

See [Knowledge Distillery/README.md](Knowledge%20Distillery/README.md#retrieval-layer-local-search-engine) for full setup details.

## Architecture Decisions

Every major design choice is documented in [DECISIONS.md](Knowledge%20Distillery/DECISIONS.md) with context, alternatives considered, and rationale.

## License

MIT
