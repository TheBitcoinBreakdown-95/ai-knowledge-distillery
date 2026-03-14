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

### The pipeline

```
Raw notes/articles
    → /process-notes (extract, classify, deduplicate, detect contradictions)
        → Synthesized KB (one concept = one place, cross-referenced)
            → /consolidate-kb (merge into main body + framework impact check)
                → Framework updates (rules, audit checks, CLAUDE.md -- proposed inline, applied on approval)
            → /verify-kb (is this still true?)
            → /audit (are we actually doing this?)
```

The framework impact check during `/consolidate-kb` closes the loop: new knowledge doesn't just sit in the KB -- it flows back into the workspace rules, audit checks, and CLAUDE.md files that govern how every project operates. No separate command needed; the user is prompted inline during consolidation and approves or declines each change.

An agent reading articles gives you: `articles → memory → hope`.
The Distillery gives you: `articles → synthesis → verification → enforcement`.

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
| Search the KB semantically | Use `search_kb` MCP tool (see [Retrieval Layer](#retrieval-layer-local-search-engine)) |
| Understand why we built it this way | [DECISIONS.md](DECISIONS.md) |
| Understand the KB pipeline internals | [KB-PROCESS.md](KB-PROCESS.md) |

---

## Concept Index

Impact tiers: **Foundational** (learn first), **Core** (daily use), **Enhancing** (power user), **Reference** (specialized). See [LEARNING-PATH.md](LEARNING-PATH.md) for the full curated progression.

| Concept | File | Section | Impact |
|---------|------|---------|--------|
| agent-vault | [failure-patterns.md](failure-patterns.md) | Security Failure Patterns | Reference |
| binary pass/fail | [testing-verification.md](testing-verification.md) | Binary Pass/Fail Criteria | Core |
| brain + muscles | [agent-design.md](agent-design.md) | Brain + Muscles Pattern | Enhancing |
| catfish code | [failure-patterns.md](failure-patterns.md) | AI-Specific Anti-Patterns | Core |
| CLAUDE.md | [context-engineering.md](context-engineering.md) | CLAUDE.md: Your Always-Loaded Memory | Foundational |
| claude-mem plugin | [memory-persistence.md](memory-persistence.md) | Layer 3: claude-mem Plugin | Reference |
| /compact | [context-engineering.md](context-engineering.md) | Context Window Management | Foundational |
| /clear | [context-engineering.md](context-engineering.md) | Context Window Management | Foundational |
| context pollution | [failure-patterns.md](failure-patterns.md) | The Four Named Patterns | Foundational |
| decision traces | [memory-persistence.md](memory-persistence.md) | Decision Traces: Strategic Memory | Enhancing |
| do-not section | [prompt-engineering.md](prompt-engineering.md) | Anti-Slop Controls | Foundational |
| feedback loop | [testing-verification.md](testing-verification.md) | The Feedback Loop | Core |
| hooks | [tools-and-integrations.md](tools-and-integrations.md) | Hooks: Pre/Post Tool Automation | Core |
| /init | [project-setup.md](project-setup.md) | Day-Zero Workflow | Core |
| invariants | [testing-verification.md](testing-verification.md) | Invariants vs Requirements | Core |
| kitchen-sink skills | [failure-patterns.md](failure-patterns.md) | AI-Specific Anti-Patterns | Core |
| MCP servers | [tools-and-integrations.md](tools-and-integrations.md) | MCP Servers: Extending Capabilities | Enhancing |
| meta-agent | [agent-design.md](agent-design.md) | Meta-Agent Architecture | Enhancing |
| morning brief | [autonomous-agents.md](autonomous-agents.md) | First Steps After Setup | Reference |
| personas | [agent-design.md](agent-design.md) | Personas: Imaginary Colleagues | Enhancing |
| plan mode | [context-engineering.md](context-engineering.md) | Plan Mode and Think Mode | Enhancing |
| plausible echo | [failure-patterns.md](failure-patterns.md) | The Four Named Patterns | Foundational |
| premature completion | [failure-patterns.md](failure-patterns.md) | The Four Named Patterns | Foundational |
| progressive disclosure | [context-engineering.md](context-engineering.md) | Structuring Context for AI | Core |
| Ralph loop | [workflow-patterns.md](workflow-patterns.md) | Pattern 2: The Ralph Loop | Enhancing |
| reverse prompting | [autonomous-agents.md](autonomous-agents.md) | The OpenClaw Mindset | Reference |
| rule of three | [skills.md](skills.md) | Skills: SOPs for AI Agents | Core |
| self-improvement loop | [memory-persistence.md](memory-persistence.md) | Self-Improvement Loop | Enhancing |
| skills | [skills.md](skills.md) | Skills: SOPs for AI Agents | Core |
| slash commands | [skills.md](skills.md) | Slash Commands | Core |
| spec-driven development | [prompt-engineering.md](prompt-engineering.md) | Spec-Driven Development | Core |
| subagents | [agent-design.md](agent-design.md) | Subagents in Claude Code | Core |
| thin skills principle | [skills.md](skills.md) | Writing Good Skills | Core |
| Vibe Engineering | [workflow-patterns.md](workflow-patterns.md) | The Vibe Engineering Stack | Core |
| vision compression | [failure-patterns.md](failure-patterns.md) | The Four Named Patterns | Foundational |
| What-Why-Constraints | [prompt-engineering.md](prompt-engineering.md) | Quick-Use Frameworks | Foundational |
| worklogs | [memory-persistence.md](memory-persistence.md) | Layer 2: Worklogs | Core |
| prompt entropy | [failure-patterns.md](failure-patterns.md) | The Four Named Patterns | Core |
| over-automation collapse | [failure-patterns.md](failure-patterns.md) | The Four Named Patterns | Enhancing |
| state corruption | [failure-patterns.md](failure-patterns.md) | The Four Named Patterns | Core |
| anchor files | [failure-patterns.md](failure-patterns.md) | Anchor Files: Compaction-Resistant Rules | Enhancing |
| silent session replacement | [failure-patterns.md](failure-patterns.md) | Silent Session Replacement | Core |
| auto memory | [context-engineering.md](context-engineering.md) | Auto Memory: Claude's Self-Managed Memory Scratchpad | Core |
| plugins | [tools-and-integrations.md](tools-and-integrations.md) | Plugin System and Marketplaces | Core |
| fan-out batch processing | [workflow-patterns.md](workflow-patterns.md) | Fan-Out Batch Processing Pattern | Enhancing |
| closed-loop architecture | [autonomous-agents.md](autonomous-agents.md) | Closed-Loop Agent Architecture | Enhancing |
| agents of chaos | [failure-patterns.md](failure-patterns.md) | Agents of Chaos: Multi-Agent Security Vulnerabilities | Reference |
| context rot | [workflow-patterns.md](workflow-patterns.md) | GSD: Context-Aware Spec-Driven Execution | Core |
| wave execution | [workflow-patterns.md](workflow-patterns.md) | GSD: Context-Aware Spec-Driven Execution | Enhancing |
| immutable test list | [workflow-patterns.md](workflow-patterns.md) | Autonomous Coding: Immutable Test List Pattern | Enhancing |
| feature-dev workflow | [workflow-patterns.md](workflow-patterns.md) | Feature-Dev: 7-Phase Multi-Perspective Workflow | Enhancing |
| context monitor hook | [tools-and-integrations.md](tools-and-integrations.md) | Context Window Monitor Hook Pattern | Enhancing |
| hookify | [tools-and-integrations.md](tools-and-integrations.md) | Hookify: Declarative Hook Authoring via Markdown | Core |
| Nyquist validation | [testing-verification.md](testing-verification.md) | Pre-Implementation Validation Mapping (Nyquist Layer) | Enhancing |
| agent sleep architecture | [memory-persistence.md](memory-persistence.md) | Agent Sleep Architecture | Enhancing |
| Supermemory | [memory-persistence.md](memory-persistence.md) | Supermemory: Hybrid Persistent Memory Plugin | Reference |
| memory persistence hooks | [memory-persistence.md](memory-persistence.md) | Memory Persistence Hooks and Continuous Learning | Core |
| OpenClaw cost optimization | [autonomous-agents.md](autonomous-agents.md) | OpenClaw Cost Anatomy and Optimization | Core |
| OpenClaw 6-component architecture | [autonomous-agents.md](autonomous-agents.md) | OpenClaw 6-Component Architecture | Enhancing |
| reference agent fleets | [agent-design.md](agent-design.md) | Reference Agent Fleets | Enhancing |
| soul document | [agent-design.md](agent-design.md) | Soul Design: From Name Tags to Life Stories | Enhancing |
| Voice DNA | [prompt-engineering.md](prompt-engineering.md) | Voice DNA: Persistent Writing Style Matching | Enhancing |
| CLAUDE.md four pillars | [context-engineering.md](context-engineering.md) | What to Include (and What NOT to Include) | Core |
| context window budget | [context-engineering.md](context-engineering.md) | MCP Context Budget Rule of Thumb | Core |
| /simplify | [skills.md](skills.md) | /simplify and /batch: Built-in PR Lifecycle Skills | Core |
| /batch | [skills.md](skills.md) | /simplify and /batch: Built-in PR Lifecycle Skills | Core |
| delegation failure pattern | [failure-patterns.md](failure-patterns.md) | OpenClaw Delegation Failure Pattern | Core |
| parallelization cascade | [workflow-patterns.md](workflow-patterns.md) | Parallelization Patterns: Cascade and Two-Instance Kickoff | Enhancing |
| six hook types | [tools-and-integrations.md](tools-and-integrations.md) | Six Hook Types: Practical Reference | Core |
| MiniClaw philosophy | [autonomous-agents.md](autonomous-agents.md) | MiniClaw Philosophy: Single Access Point Architecture | Enhancing |
| OpenClaw Paradox | [autonomous-agents.md](autonomous-agents.md) | MiniClaw Philosophy: Single Access Point Architecture | Core |
| winning architecture | [autonomous-agents.md](autonomous-agents.md) | The Winning Architecture: 6 Requirements for Secure Recursive Agents | Enhancing |
| agent security threat model | [failure-patterns.md](failure-patterns.md) | Agent Security Threat Model: 6 Attack Classes | Core |
| MCP tool poisoning (rug pull) | [failure-patterns.md](failure-patterns.md) | Agent Security Threat Model: 6 Attack Classes | Core |
| transitive prompt injection | [failure-patterns.md](failure-patterns.md) | Agent Security Threat Model: 6 Attack Classes | Core |
| memory poisoning | [failure-patterns.md](failure-patterns.md) | Agent Security Threat Model: 6 Attack Classes | Enhancing |
| OWASP agentic top 10 | [failure-patterns.md](failure-patterns.md) | Agent Security Threat Model: 6 Attack Classes | Reference |
| AgentShield | [tools-and-integrations.md](tools-and-integrations.md) | AgentShield and Sandboxing Hierarchy | Enhancing |
| sandboxing hierarchy | [tools-and-integrations.md](tools-and-integrations.md) | AgentShield and Sandboxing Hierarchy | Core |
| reverse prompt injection guardrail | [tools-and-integrations.md](tools-and-integrations.md) | AgentShield and Sandboxing Hierarchy | Enhancing |
| GSD (Get Shit Done) | [workflow-patterns.md](workflow-patterns.md) | Pattern 6: GSD Execution Framework | Core |
| immutable test list | [workflow-patterns.md](workflow-patterns.md) | Immutable Test List Pattern | Enhancing |
| pass@k vs pass^k | [testing-verification.md](testing-verification.md) | Eval Metrics: pass@k vs pass^k | Enhancing |
| dynamic system prompt injection | [context-engineering.md](context-engineering.md) | Dynamic System Prompt Injection via CLI Aliases | Enhancing |
| iterative retrieval | [agent-design.md](agent-design.md) | Iterative Retrieval: Sub-Agent Context Negotiation | Core |
| plugin-dev toolkit | [tools-and-integrations.md](tools-and-integrations.md) | Plugin Development Toolkit: 8-Phase Create-Plugin Workflow | Reference |
| Claude Code Action | [tools-and-integrations.md](tools-and-integrations.md) | Claude Code Action: CI/CD GitHub Integration | Core |
| OpenTelemetry monitoring | [tools-and-integrations.md](tools-and-integrations.md) | Claude Code ROI and Monitoring via OpenTelemetry | Enhancing |
| Python Agent SDK | [tools-and-integrations.md](tools-and-integrations.md) | Python Agent SDK: In-Process MCP and Permission Gates | Reference |
| OpenClaw security hardening | [autonomous-agents.md](autonomous-agents.md) | Security Hardening: 13-Step Checklist | Core |
| OpenClaw cost anatomy | [autonomous-agents.md](autonomous-agents.md) | Cost Anatomy and Optimization | Core |
| direct vs boss routing | [autonomous-agents.md](autonomous-agents.md) | Multi-Agent Communication: Direct vs Boss Routing | Core |
| instinct-based learning | [skills.md](skills.md) | Instinct-Based Learning: Continuous Learning v2 | Core |
| strategic compaction | [context-engineering.md](context-engineering.md) | /compact: Compress Without Losing Knowledge | Core |
| eval-driven development (EDD) | [testing-verification.md](testing-verification.md) | Eval-Driven Development (EDD) | Core |
| cost-aware LLM pipeline | [context-engineering.md](context-engineering.md) | Token Economics: Model Routing and Cost Data | Enhancing |
| priority hierarchy | [agent-design.md](agent-design.md) | Priority Hierarchy and Identity Framework | Enhancing |
| search-first | [agent-design.md](agent-design.md) | Search-First: Adopt/Extend/Compose/Build Decision Taxonomy | Core |
| goal-backward plan verification | [testing-verification.md](testing-verification.md) | Goal-Backward Plan Verification: 8-Dimension Framework | Enhancing |
| four-level verification hierarchy | [testing-verification.md](testing-verification.md) | Four-Level Verification Hierarchy: Exists -> Substantive -> Wired -> Functional | Core |
| TDD methodology | [testing-verification.md](testing-verification.md) | TDD Methodology: Decision Heuristic and Execution Protocol | Core |
| MCP server design patterns | [tools-and-integrations.md](tools-and-integrations.md) | MCP Server Design Patterns: Building Production-Quality Tool Servers | Enhancing |
| hookify rule system | [tools-and-integrations.md](tools-and-integrations.md) | Hookify Rule System: Markdown-Based Event Rules | Core |
| cloud provider auth for CI/CD | [tools-and-integrations.md](tools-and-integrations.md) | Cloud Provider Authentication for CI/CD | Reference |
| multi-agent team pattern | [autonomous-agents.md](autonomous-agents.md) | Multi-Agent Team Pattern for Solo Founders | Enhancing |
| autonomous project management | [autonomous-agents.md](autonomous-agents.md) | Autonomous Project Management via STATE.yaml | Enhancing |
| RAG knowledge base composition | [autonomous-agents.md](autonomous-agents.md) | RAG Knowledge Base: Cross-Workflow Composition | Enhancing |
| CLAUDE.md quality rubric | [context-engineering.md](context-engineering.md) | CLAUDE.md Quality Rubric: 6-Criterion Scoring System | Core |
| model profiles | [context-engineering.md](context-engineering.md) | Model Profiles: Three-Tier Task-to-Model Matching | Enhancing |
| skill creation methodology | [skills.md](skills.md) | Skill Creation Methodology: Eval-Driven Iteration Loop | Core |
| GSD executor deviation rules | [workflow-patterns.md](workflow-patterns.md) | GSD Executor: Deviation Rules and Analysis Paralysis Guard | Core |
| subagent attribution | [agent-design.md](agent-design.md) | Subagent Attribution: parent_tool_use_id Tracking | Enhancing |
| zero-friction capture | [memory-persistence.md](memory-persistence.md) | Zero-Friction Capture: Conversation as Interface | Core |
| reconnaissance-then-action | [testing-verification.md](testing-verification.md) | Web Application Testing: Server Lifecycle and Reconnaissance Pattern | Enhancing |
| blind comparison evaluation | [skills.md](skills.md) | Skill Improvement: Blind Comparison and Iteration Principles | Enhancing |
| memory defense-in-depth | [memory-persistence.md](memory-persistence.md) | OpenClaw Memory Lifecycle: Defense-in-Depth Configuration | Core |
| knowledge type placement matrix | [context-engineering.md](context-engineering.md) | Knowledge Type Placement Matrix | Core |
| scaling strategy matrix | [context-engineering.md](context-engineering.md) | Scaling Strategy Matrix: When to Add Complexity | Enhancing |
| knowledge layer evaluation | [testing-verification.md](testing-verification.md) | Knowledge Layer Evaluation Framework | Enhancing |
| staged implementation roadmap | [project-setup.md](project-setup.md) | Staged Implementation Roadmap | Core |
| GrepRAG | [tools-and-integrations.md](tools-and-integrations.md) | GrepRAG: Identifier-Focused Retrieval for Code | Enhancing |
| plugin agent authoring | [skills.md](skills.md) | Plugin Agent Authoring Specification | Reference |
| extended command frontmatter | [skills.md](skills.md) | Extended Command Frontmatter and Dynamic Patterns | Enhancing |
| AskUserQuestion tool | [skills.md](skills.md) | AskUserQuestion Tool: Interactive Command Input | Reference |
| plugin hooks.json | [tools-and-integrations.md](tools-and-integrations.md) | Plugin Hook Configuration: hooks.json Format and Runtime Semantics | Enhancing |
| plugin MCP naming | [tools-and-integrations.md](tools-and-integrations.md) | Plugin MCP Integration: Naming Convention and Lifecycle | Reference |
| plugin settings .local.md | [tools-and-integrations.md](tools-and-integrations.md) | Plugin Settings Pattern: .local.md Convention Expanded | Reference |
| /loop | [skills.md](skills.md) | /loop Skill: Built-in Recurring Task Scheduling | Core |
| skill integration protocol | [skills.md](skills.md) | Skill Integration Guide: Agent-Side Discovery Protocol | Enhancing |
| session audit pattern | [workflow-patterns.md](workflow-patterns.md) | Session Audit Pattern: Self-Analyzing Workflow Efficiency | Core |
| CLAUDE.md operating template | [workflow-patterns.md](workflow-patterns.md) | CLAUDE.md 7-Section Operating Template | Enhancing |
| model routing 2026 | [autonomous-agents.md](autonomous-agents.md) | Model Routing 2026: Brain/Muscles with Specific Model Picks | Core |
| Telegram forum topics | [autonomous-agents.md](autonomous-agents.md) | Telegram Forum Topics for Session Isolation | Reference |
| CEO-only agent | [autonomous-agents.md](autonomous-agents.md) | CEO-Only Main Agent Pattern | Core |
| agent swarm critique | [agent-design.md](agent-design.md) | Agent Swarm Critique: Pipeline Structure vs Coordination Overhead | Enhancing |
| LSP integration | [tools-and-integrations.md](tools-and-integrations.md) | LSP Integration: Reality Check and Actual Benefits | Reference |
| Google Workspace CLI | [tools-and-integrations.md](tools-and-integrations.md) | Google Workspace CLI as Installable Skill | Reference |
| Chief of Staff pattern | [workflow-patterns.md](workflow-patterns.md) | Chief of Staff Pattern: Non-Programmer Builds Full Autonomous Workflow | Enhancing |
| Cowork context files | [workflow-patterns.md](workflow-patterns.md) | Cowork Context Files Strategy: Better Files Beat Better Prompts | Core |
| God Parent pattern | [autonomous-agents.md](autonomous-agents.md) | God Parent Pattern: First Documented Autonomous Agent Reproduction | Reference |
| post-install hardening | [autonomous-agents.md](autonomous-agents.md) | Post-Install Hardening Checklist: 9-Section Production Readiness | Core |
| enterprise agent architectures | [agent-design.md](agent-design.md) | Enterprise Agent Architectures: Solo, Parallel, Collaborative | Core |
| Dashboard Trap | [failure-patterns.md](failure-patterns.md) | Dashboard Trap: Catch Exceptions, Don't Build Dashboards | Core |
| Cowork plugin tier list | [tools-and-integrations.md](tools-and-integrations.md) | Cowork Plugin Tier List: 21 Plugins Ranked S/A/B/C | Reference |
| _MANIFEST.md | [context-engineering.md](context-engineering.md) | _MANIFEST.md: Preventing Context Pollution in Working Folders | Core |
| gamification prompt design | [prompt-engineering.md](prompt-engineering.md) | Prompt-as-Spec: Gamification with Dopamine Mechanics | Reference |
| plugin auto-discovery | [tools-and-integrations.md](tools-and-integrations.md) | Plugin Auto-Discovery Mechanism and Portable Paths | Enhancing |
| credential isolation | [tools-and-integrations.md](tools-and-integrations.md) | Credential Isolation Architecture via n8n Proxy | Core |
| skill authoring standards | [skills.md](skills.md) | Skill Authoring Standards: Word Counts, Writing Style, Common Mistakes | Core |
| bugs-first enforcement | [autonomous-agents.md](autonomous-agents.md) | Bugs-First Autonomous Priority Enforcement | Enhancing |
| ambient monitoring | [autonomous-agents.md](autonomous-agents.md) | Ambient Monitoring Pattern | Enhancing |
| multi-layer cron | [autonomous-agents.md](autonomous-agents.md) | Multi-Layer Cron Defense-in-Depth | Core |
| channel-isolated chains | [workflow-patterns.md](workflow-patterns.md) | Channel-Isolated Parallel Agent Chains | Enhancing |
| requirements-driven derivation | [workflow-patterns.md](workflow-patterns.md) | Requirements-Driven Phase Derivation | Core |
| parallel discovery with checkpoints | [workflow-patterns.md](workflow-patterns.md) | Multi-Agent Parallel Discovery with Human Checkpoints | Enhancing |
| persistent state machine | [agent-design.md](agent-design.md) | Persistent State Machine with File-Based Checkpoints | Core |
| sub-agent parallelization | [agent-design.md](agent-design.md) | Sub-Agent Parallelization for Distributed Data Fetching | Enhancing |
| multi-input synthesis | [agent-design.md](agent-design.md) | Multi-Input Research Synthesis Pattern | Enhancing |
| concurrent file editing race | [failure-patterns.md](failure-patterns.md) | Concurrent File Editing Race Condition | Core |
| pre-build validation gate | [testing-verification.md](testing-verification.md) | Pre-Build Validation Gate with Real Data Sources | Enhancing |
| event sourcing for state | [memory-persistence.md](memory-persistence.md) | Event Sourcing for Project State | Enhancing |
| model-tiered code review | [agent-design.md](agent-design.md) | Model-Tiered Code Review Pipeline | Enhancing |
| pedagogical agent | [agent-design.md](agent-design.md) | Pedagogical Agent: Selective Delegation Back to Human | Reference |
| expertise-in-agent separation | [agent-design.md](agent-design.md) | Expertise-in-Agent, Context-in-Prompt Separation | Core |
| tool design as elicitation | [agent-design.md](agent-design.md) | Tool Design as Agent Elicitation | Core |
| GSD state management | [workflow-patterns.md](workflow-patterns.md) | GSD State Management Templates | Enhancing |
| GSD verification architecture | [testing-verification.md](testing-verification.md) | Three-Tier Artifact Checks and Wiring Verification (GSD) | Enhancing |
| section mutation rules | [workflow-patterns.md](workflow-patterns.md) | GSD State Management Templates | Core |
| must-haves contract | [workflow-patterns.md](workflow-patterns.md) | GSD Planning Templates: Must-Haves Contract | Enhancing |
| three-tier artifact verification | [testing-verification.md](testing-verification.md) | Three-Tier Artifact Checks and Wiring Verification (GSD) | Core |
| domain expertise encoding | [skills.md](skills.md) | Domain Expertise Encoding in Skills | Core |
| anti-slop guardrails | [skills.md](skills.md) | Anti-Slop Guardrails and Diversity-Forcing | Enhancing |
| plugin extension taxonomy | [skills.md](skills.md) | Plugin Extension Taxonomy: Commands vs Skills vs Agents | Core |
| SessionStart hooks | [tools-and-integrations.md](tools-and-integrations.md) | SessionStart Hooks vs Subagents | Enhancing |
| God Parent pattern | [autonomous-agents.md](autonomous-agents.md) | God Parent Pattern | Reference |
| transcript-to-advisor | [workflow-patterns.md](workflow-patterns.md) | Transcript-to-Advisor Pipeline | Enhancing |
| director mental model | [workflow-patterns.md](workflow-patterns.md) | The Director Mental Model (Non-Programmer Framing) | Foundational |
| feature addition 5-phase | [workflow-patterns.md](workflow-patterns.md) | Feature Addition: 5-Phase Workflow | Core |
| bug fix 5-step | [workflow-patterns.md](workflow-patterns.md) | Bug Fix: 5-Step Workflow | Core |
| director-level version control | [workflow-patterns.md](workflow-patterns.md) | Director-Level Version Control | Foundational |
| troubleshooting taxonomy | [failure-patterns.md](failure-patterns.md) | Troubleshooting Taxonomy: Three Problem Types | Core |
| error reading framework | [failure-patterns.md](failure-patterns.md) | Error Reading Framework | Foundational |
| conversation patterns | [prompt-engineering.md](prompt-engineering.md) | Claude Code Conversation Patterns | Core |
| revision cycle | [prompt-engineering.md](prompt-engineering.md) | The Revision Cycle as Workflow | Foundational |
| enforcement guarantee ladder | [context-engineering.md](context-engineering.md) | Enforcement Guarantee Ladder | Core |
| /btw | [skills.md](skills.md) | /btw: Side Questions During Active Work | Core |
| built-in Code Review | [tools-and-integrations.md](tools-and-integrations.md) | Claude Code Built-in Code Review | Core |
| single-rule compounding memory | [memory-persistence.md](memory-persistence.md) | Single-Rule Compounding Memory for OpenClaw | Enhancing |
| self-evolving agent pattern | [agent-design.md](agent-design.md) | Self-Evolving Agent Pattern | Enhancing |
| agent-browser | [tools-and-integrations.md](tools-and-integrations.md) | agent-browser: Browser Automation CLI for AI Agents | Reference |
| per-hook disable | [tools-and-integrations.md](tools-and-integrations.md) | Per-Hook Disable Configuration Pattern | Enhancing |

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
