# Contributing

Contributions that improve the knowledge base are welcome. Here's how the system works and how you can help.

## How the KB Works

The Knowledge Distillery follows a synthesis model: raw inputs are extracted, classified, deduplicated, and merged into topic files. Each concept has exactly one primary home. Cross-references connect related ideas across files.

See [KB-PROCESS.md](Knowledge%20Distillery/KB-PROCESS.md) for the full pipeline walkthrough.

## What Makes a Good Contribution

**Improving existing content:**
- Correcting outdated claims (tools change, APIs evolve)
- Adding nuance or boundary conditions to existing advice
- Fixing broken cross-references
- Improving clarity without changing meaning

**Adding new content:**
- New AI/LLM best practices with source attribution
- Named patterns or anti-patterns from production experience
- Tool comparisons or integration guides

**Improving the system:**
- Search engine improvements (chunker, indexer, eval harness)
- New slash commands or command improvements
- Better audit checks

## Conventions

- Each concept has ONE primary home -- check the Concept Index in README.md before adding
- Cross-reference format: `(see [concept](file.md#section-anchor))`
- No emojis. Headers, bullets, tables for scannability.
- Synthesize across sources -- don't copy-paste from a single article
- Include source attribution for verifiable claims

## Submitting Changes

1. Fork the repo
2. Make your changes
3. Run `/kb-status` if you have Claude Code to verify cross-ref integrity
4. Open a PR with a clear description of what changed and why
