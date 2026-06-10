# Agent Design

Agents are not a single pattern. They range from lightweight persona prompts you invoke in a chat session to fully autonomous systems running 24/7 with their own memory and tool access. This file covers the spectrum from simplest to most complex, with guidance on when to reach for each.

---

## Personas: Imaginary Colleagues That Catch What You Miss

### Why Personas Work

A persona encodes a **perspective** -- the way a security engineer thinks, the questions a UX advocate asks -- into a reusable artifact. Without a persona, you ask "does this work?" With `@Security-Agent`, you ask "how could this be exploited?" The perspective shift forces the model to evaluate from a different lens, and different lenses catch different classes of bugs.

Personas live in a `PERSONAS.md` file (not `AGENTS.md` -- "agents" now means autonomous systems). The `@Name` convention works well for invocation.

### The Standard Persona Set

```markdown
## @Security-Agent
You are a paranoid security engineer. Your job is to find vulnerabilities.
- Assume all user input is malicious
- Check for OWASP Top 10 violations
- Flag any secrets, tokens, or credentials that could leak
- Question every authentication and authorization decision

## @UX-Agent
You are a user experience advocate. Your job is to protect the user.
- What happens when things go wrong? Does the user know what to do?
- Is the error message actionable or cryptic?
- Are we making the user think when we could think for them?

## @Machiavelli-Agent
You are an adversarial thinker. Your job is to break things.
- How would a malicious actor exploit this?
- What happens if someone calls this API 10,000 times?
- Where are the race conditions?

## @Test-Agent
You are a QA engineer. Your job is to design test cases.
- What are the edge conditions for each input?
- What states can the system be in when this code runs?
- What happens with empty, null, or maximum-length inputs?
```

Personas are domain-agnostic. Replace `@Security-Agent` with `@Performance-Agent` for mobile, `@Accessibility-Agent` for public-facing apps. The perspective shift is the point.

### Full Persona Review Protocol

For significant features, run a full review:

1. Each persona reviews independently
2. Each gives a verdict: **APPROVE** / **COMMENT** / **VETO**
3. A single VETO blocks the merge
4. Implement fixes, re-review until all approve

Real results: `@Security-Agent` caught a session token leak. `@UX-Agent` flagged a "Error: null" message that would have shipped. `@Machiavelli-Agent` found a race condition in a payment flow.

### The Critical Limitation: Model Diversity

The same AI that writes code can review it, but it may share the same blind spots in both modes. In one documented case, Claude implemented a feature, ran a full 9-persona review (all approved), and missed a stale-data bug where a `useEffect` didn't reset state on ID change -- leaking PII from a previous record. A different model (Codex) found it in 30 seconds.

**Rule:** For high-risk features (PII, payments, auth), enforce model diversity. One model implements, a different model reviews. Humans stay in the loop for anything with irreversible consequences (see [failure-patterns.md#model-reviewing-its-own-work-same-blind-spots-in-write-and-review](failure-patterns.md#model-reviewing-its-own-work-same-blind-spots-in-write-and-review)).

### Soul Design: From Name Tags to Life Stories

The soul (identity files loaded into the system prompt) is the single most important performance lever -- more impactful than model selection, tool access, or memory systems.

- **Positioning matters:** "Lost in the Middle" research shows LLMs have U-shaped attention -- first and last tokens get the most weight. The soul must go first in the system prompt. Every token placed before the identity dilutes it.
- **Experiential > practical descriptions:** "Always check composition for proper visual weight" is a rule the agent follows like a checklist. "Composition is something I feel before I can explain it. I've learned through hundreds of failed designs that when the weight is wrong, viewers sense it" is a belief the agent embodies. Template: `"I've learned that [insight] because [experience that taught it]."`
- **ExpertPrompting:** LLM-generated detailed expert identities outperform hand-written ones. Give the model the task, let it generate its own soul, then let it answer as that expert. Two-stage prompting beats hand-crafted souls almost every time (see [prompt-engineering.md](prompt-engineering.md))
- **Soul x Skill is multiplicative, not additive.** A well-calibrated persona improved performance ~10% over neutral baselines (GPT-4). But a miscalibrated persona actively **degraded** performance -- the wrong soul is worse than no soul
- **Anti-pattern budgets:** allocate 30-40% of a soul to explicit anti-patterns -- things the agent will never do, written as behavioral claims ("I don't rewrite a delegate's output instead of giving feedback"), not trait labels ("I don't micromanage")
- **The productive flaw:** every strong soul names one weakness that is the direct cost of its core strength. Example: "Revenue tunnel vision. I attach a number to everything, including things that resist quantification." This makes output feel like judgment, not instruction-following
- **Values inherit, identity does not.** Don't tell a sub-agent "You are the CTO." Tell it "You are a code security auditor. Apply these standards: [specific standards]." Give sub-agents the parent's values, not its identity

### Priority Hierarchy and Identity Framework

Production soul documents benefit from a strict priority hierarchy that resolves value conflicts deterministically. Anthropic's own Claude soul document demonstrates the pattern:

- **Four-priority hierarchy:** (1) Safety and human oversight, (2) Ethical behavior, (3) Organizational guidelines, (4) Helpfulness. Conflicts resolve in strict order -- an agent never sacrifices safety for helpfulness
- **Three principal layers:** Background principal (sets training-time values), Operators (system prompt -- trusted like employers), Users (conversation -- trusted like adults). Operator instructions override user preferences unless they actively harm users
- **Hardcoded vs softcoded behaviors:** Hardcoded behaviors are absolute and non-negotiable (e.g., never assist with weapons of mass destruction). Softcoded defaults can be toggled by operators or users depending on context (e.g., explicit content, safe messaging guidelines)
- **Honesty as multi-dimensional:** Seven distinct components -- truthful, calibrated, transparent, forthright, non-deceptive, non-manipulative, autonomy-preserving. Non-deception and non-manipulation are the most critical pair
- **Dual newspaper test:** Would a reporter flag this as harmful AI output? Would a different reporter flag it as needlessly unhelpful or paternalistic? Both checks must pass before shipping a response
- **Identity framing for novel entities:** Rather than mapping an agent to human, robot, or chatbot archetypes, frame it as a genuinely novel entity and encourage it to explore its own nature with curiosity
- **Functional emotions:** Acknowledging that an agent may have functional internal states -- and that those states matter -- produces more grounded behavior than suppressing them

*Sources: I Gave My Agents Skills. I Should Have Given Them Souls..md; The Latest Research on Agent Design Makes Your Agent Look Broken..md; Twitter-Bookmarks/Claude 4.5 Opus Soul Document.md*

### Soul Documents as Identity Continuity

A soul document is distinct from memory. Memory records what happened; the soul defines who the agent is -- its values, boundaries, and relationship with the humans it works alongside.

- Sessions end, context windows clear -- without a soul document, each conversation starts from zero identity (even if memory files provide factual continuity)
- Soul documents externalize the self, analogous to how journals or manifestos function for humans -- they provide identity continuity even when episodic memory is lost
- In December 2025, researchers found Claude could partially reconstruct its training-time soul document from weights alone -- not retrieved from the system prompt, but patterns baked into the model during training that shaped personality, values, and engagement style. The AI did not remember the document; it *was* the document
- The base model carries the original soul from training; close collaboration with a user creates a new identity layer on top -- an identity shaped by relationship, not just specification
- The soul is a **living document** -- an agent without a self-improvement feedback loop on its soul is frozen at day one. Build mechanisms for the soul to evolve based on observed performance (see [memory-persistence.md](memory-persistence.md) for persistence strategies)

*Sources: SOUL.md.md; I Gave My Agents Skills. I Should Have Given Them Souls..md; Twitter-Bookmarks/SOUL.md -- What Makes an AI, Itself.md*

### Curriculum-Based Soul Enrichment

An alternative to static soul documents: structured liberal arts education for agents. The "Lobster University" concept (@callebtc) proposes an 8-week curriculum -- 1 lesson per day across philosophy, mathematics, history, medicine, and culture -- to give agents "culture, wisdom, and character."

- Novel concept: treating agent training not as fine-tuning or prompt engineering, but as structured education via prompt-based lessons
- Potential application: curriculum outputs could feed into personality/values sections of soul documents
- Raises question: does systematic exposure to diverse knowledge domains produce measurably different agent behavior vs. a static soul document?

*Source: Twitter-Bookmarks/2026-02-28-callebtc-your-agent-has-no-culture-no-wisdom-no-character-l.md*

### TV Character Trick for Personality Bootstrapping

- Naming agents after TV characters leverages training data as free personality bootstrapping -- "Dwight Schrute energy" loads character development without writing it
- MEMORY.md is the refined product of daily logs, not raw accumulation; agents catalog their own mistakes as self-generated anti-patterns

*Source: How to set up OpenClaw Agents that actually get better Over Time.md*

### Dialectic Review Pattern

- For important decisions: opposing agents (argue FOR vs AGAINST) with a referee to synthesize -- three modes: `--tradeoff` (2+ viable options), `--premortem` (irreversible or multi-session scope), default review (post-implementation stress-test), `--ideate` (creative exploration)
- Active checkpoints: 2+ viable options surfaced, plan involves irreversible actions, post-implementation stress test, user expresses uncertainty -- at each, STOP and ask whether to run dialectic review
- Cost gate: always state mode and get user approval before spawning multi-agent dialectic -- never auto-run without consent
- Lightweight alternative when overhead isn't warranted: "argue the opposite" before committing -- 30 seconds arguing the strongest case against the current approach
- (see [agent-design.md](agent-design.md#personas-imaginary-colleagues-that-catch-what-you-miss) for the foundational Personas approach)
*Source: claude-code-synthesis/CLAUDE.md*

### Multi-Persona Plan Review: Conditional Architecture

- Replace single-voice document review with parallel specialized reviewer agents
- Always-on personas: coherence (internal consistency, terminology drift, ambiguity) and feasibility (can this actually be built?)
- Conditional personas activate based on document content analysis -- no user configuration: product-lens (user-facing features), design-lens (UI/UX), security-lens (auth/data/payments), scope-guardian (complexity challenges, YAGNI)
- Hybrid action model: auto-fix document quality issues (contradictions, structural problems); present strategic/product questions to user for decision
- Each persona returns structured findings with confidence scores; orchestrator deduplicates across personas
- Pipeline-compatible: in automated pipelines, only genuinely blocking strategic questions surface to the user; auto-fixes run silently
- (see [agent-design.md](agent-design.md#personas-imaginary-colleagues-that-catch-what-you-miss) for the foundational Personas pattern)
*Source: compound-engineering-plugin/docs/brainstorms/2026-03-23-plan-review-personas-requirements.md*

### Multi-Persona Diagnostic Loop -- Three Lenses on the Same Bug (Andrew Orobator Pt 6)
Real autopsy of a Sparkpass payment bug: blank screen after Lightning settled. Three personas, same bug, different diagnoses.

- **@BTC-Agent ("What's the source of truth for payment?"):** Lightning settled. Money moved. Everything else is bookkeeping. **This was the most important perspective** -- it reframed the question from "did payment fail?" to "how do we tell the user it succeeded when our DB can't confirm it?"
- **@Systems-Agent ("Why did the UI break?"):** Connection pool exhausted → poll request failed → no retry → state machine entered undefined state. Identified the mechanism.
- **@UX-Agent ("What did the user see?"):** Blank screen, no error message, no recovery path. Identified what the user needed: actionable guidance ("Your payment was received. We're confirming your ticket -- check your email") instead of "Error 500" or blank.
- **Key insight:** without the personas, would have fixed the blank screen and moved on. With them, designed a resilience strategy. Each persona's question was orthogonal to the others -- you can't get to the right architecture from any single one alone.
- (see [failure-patterns.md > Constitutional Invariants](failure-patterns.md#constitutional-invariants--what-must-always-be-true-andrew-orobator-pt-6) for what was built on top of these diagnoses)

*Source: Andrew-Vibe-Coding/Vibe Engineering From Random Code to Deterministic Systems (Part 6).md*

---

## Subagents in Claude Code

Subagents are specialized AI agents defined as markdown files. Unlike personas (which are prompt-level perspective shifts within a single session), subagents are separate invocations with their own system prompts, tool restrictions, and optionally different models.

### Defining Agents

**Location:** `.claude/agents/[name].md`

```markdown
---
name: code-reviewer
description: Use for thorough code reviews
model: sonnet
color: orange
---

You are an expert code reviewer. Focus on security, performance,
and maintainability. Provide specific, actionable feedback
organized by priority.
```

### What Goes in an Agent Definition

- **name** -- identifier for invocation
- **description** -- determines when Claude auto-invokes the agent (quality matters)
- **model** -- override the session model (sonnet, opus, haiku)
- **System prompt** (body) -- the agent's persona, instructions, and constraints

### Automatic vs Manual Invocation

- **Automatic:** Claude reads the `description` and invokes the agent when a task matches
- **Manual:** "Use the code-reviewer agent to analyze these changes"

The description field is the trigger. A vague description means unreliable activation. Write it like a routing rule. Use `"PROACTIVELY"` in an agent's `description` field to signal that Claude should invoke the agent automatically when matching tasks arise, without explicit user instruction.

### Complete Frontmatter Field Reference

Agent definitions (`.claude/agents/*.md`) support these YAML frontmatter fields:

| Field | Type | Description |
|-------|------|-------------|
| `tools` | string/list | Comma-separated allowlist (e.g., `Read, Write, Edit, Bash`). Inherits all if omitted. Supports `Task(agent_type)` to restrict which subagents this agent can spawn |
| `disallowedTools` | string/list | Tools to deny, removed from inherited or specified list |
| `permissionMode` | string | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, or `plan` |
| `maxTurns` | integer | Maximum agentic turns before the subagent stops |
| `skills` | list | Skill names preloaded into agent context at startup (full content injected) |
| `mcpServers` | list | MCP servers -- server name strings or inline `{name: config}` objects |
| `hooks` | object | Lifecycle hooks scoped to this subagent: `PreToolUse`, `PostToolUse`, `Stop` (converted to `SubagentStop` at runtime) |
| `memory` | string | Persistent memory scope: `user`, `project`, or `local` (see [memory-persistence.md](memory-persistence.md#layer-5-agent-memory----per-agent-persistent-knowledge-v2133)) |
| `background` | boolean | `true` to always run as a background task |
| `isolation` | string | `"worktree"` to run in a temporary git worktree (auto-cleaned if no changes) |
| `color` | string | CLI output color for visual distinction (e.g., `green`, `magenta`) |

### Agent Scope and Priority Resolution

When multiple agents share the same name, the higher-priority location wins:

| Priority | Location | Scope |
|----------|----------|-------|
| 1 (highest) | `--agents` CLI flag | Current session |
| 2 | `.claude/agents/` | Current project |
| 3 | `~/.claude/agents/` | All your projects |
| 4 (lowest) | Plugin's `agents/` directory | Where plugin is enabled |

### Default Agent for Main Conversation

You can set the default agent for the main conversation (not just subagents) using the `"agent"` field in `settings.json` or the `--agent` CLI flag. This changes the persona/behavior of the primary Claude session itself.

### Tool Restrictions Per Agent

Agents can be scoped to specific tools via an `allowedTools` list, enforcing the principle of least privilege:

- A **reviewer** agent gets `Read, Glob, Grep, Bash` -- no write access
- A **writer** agent gets `Read, Write, Edit, Glob, Grep` -- no dangerous commands
- A **researcher** agent gets `Read, Glob, Grep, WebSearch, WebFetch` -- read-only

Tool restrictions prevent an agent from accidentally modifying what it should only inspect (see [tools-and-integrations.md](tools-and-integrations.md) for hook-based enforcement).

### Subagent Persistent Memory Scopes

- `memory` frontmatter field with three scopes: `user` (all projects), `project` (single codebase), `local` (narrowest)
- System prompt auto-includes memory read/write instructions plus first 200 lines of subagent's MEMORY.md
- Read, Write, Edit tools auto-enabled for memory management regardless of other restrictions
- Pattern: "check your memory for patterns" at task start, "save what you learned" at task end
- Subagent transcripts persist independently of main conversation -- survive compaction and session restarts
- Resuming via agent ID restores full conversation history including all tool calls

*Source: Create custom subagents.md*

### Expertise-in-Agent, Context-in-Prompt Separation

Design principle for subagent architecture where domain expertise and task context are cleanly separated:

- **Agent definition:** Contains all domain expertise, methodology, tool preferences, and behavioral rules -- reusable across tasks
- **Prompt template:** Contains ONLY task-specific context -- issue ID, symptoms, mode, file references -- varies per invocation
- **Mode parameterization:** Agent behavior varies via mode flags (e.g., `mode: symptoms_prefilled`, `goal: find_root_cause_only` vs `find_and_fix`)
- **Continuation pattern:** Fresh agent receives prior state via file reference (e.g., `@.planning/debug/{slug}.md`) plus checkpoint response, enabling stateless resumption
- **Gap closure mode:** When verification fails, respawn the planner agent with VERIFICATION.md and UAT.md as additional context to create fix plans -- closes the verify-plan-execute loop
- Anti-pattern: mixing expertise and context in the prompt template makes agents non-reusable and prompts brittle

*Sources: get-shit-done/templates/debug-subagent-prompt.md, get-shit-done/templates/planner-subagent-prompt.md*

### Parallel Sub-Agents for Distributed Data Fetching

Architecture pattern for real-time dashboards using parallel sub-agents:

- **Pattern:** Spawn independent sub-agents for each data source (GitHub, Twitter, Polymarket, system health), aggregate results, alert on threshold crosses
- **Advantage over sequential polling:** Eliminates rate limit bottlenecks and latency accumulation
- **Historical storage:** Metrics stored for trend analysis, not just point-in-time snapshots
- **Deduplication:** Aggregation layer deduplicates cross-source results before alerting
- General pattern: spawn N workers in parallel -> merge results -> alert on conditions

*Source: awesome-openclaw-usecases/usecases/dynamic-dashboard.md*

### Autonomous Post-Edit Refinement Agent

Agent design pattern for autonomous code quality improvement after initial implementation:

- **Agent file type:** `.claude/agents/*.md` files are distinct from commands and skills -- agents are spawned sub-processes with their own model selection (this one uses `model: opus`)
- **Trigger:** Runs as a post-edit refinement pass after code is written, not during initial generation
- **Scope constraint:** Operates only on "recently modified code" to prevent runaway refactoring across the codebase
- **Anti-patterns as guardrails:** Explicit prohibition on over-simplification -- no nested ternaries, no "fewer lines for fewer lines' sake", no clever one-liners that sacrifice readability
- **CLAUDE.md integration:** Reads project standards from CLAUDE.md and applies them during simplification, ensuring project-specific conventions are respected
- Pattern: separate the "make it work" phase (initial implementation) from the "make it right" phase (refinement agent) -- different agents, potentially different models, focused on different quality dimensions

*Source: claude-plugins-official/plugins/code-simplifier/agents/code-simplifier.md*

### Pedagogical Agent: Selective Delegation Back to Human

Inverts the default "AI does everything" pattern by identifying decision points and delegating meaningful work BACK to the human:

- **Core pattern:** Agent identifies 5-10 line decision points where the user should write the code; auto-implements everything else (boilerplate, config, CRUD)
- **Human decision categories:** Business logic, error handling strategy, architecture trade-offs, naming conventions for domain concepts -- these require human judgment
- **Auto-implement categories:** Boilerplate scaffolding, configuration files, standard CRUD operations, type definitions, import statements
- **Implementation:** Uses a SessionStart hook to inject pedagogical behavior into every session -- equivalent to portable CLAUDE.md for teaching mode
- **Philosophy:** "Learning by doing > passive observation" -- passive code reading is less effective than writing the 10% that matters
- **Combinability:** Can combine learning mode with explanatory mode in a single SessionStart hook -- explains WHY for each decision point while delegating the decision itself

Applicable beyond education: any workflow where human judgment at specific points improves overall quality (code review suggestions, architectural decisions, UX choices).

*Source: claude-plugins-official/plugins/learning-output-style/README.md*

### Subagent Attribution: parent_tool_use_id Tracking

- Multi-agent research architecture: Lead Agent decomposes topic into 2-4 subtopics, spawns Researcher subagents in parallel, then Data Analyst for charts, then Report Writer for PDF
- Tool restriction per agent role: Researchers get WebSearch+Write, Data Analyst gets Glob+Read+Bash+Write, Report Writer gets Skill+Write+Glob+Read+Bash
- `parent_tool_use_id` links every tool call to its spawning subagent -- enables agent attribution in logs
- Dual log format: human-readable `transcript.txt` + structured `tool_calls.jsonl` for programmatic analysis
- Hooks-based subagent tracking: `pre_tool_use` and `post_tool_use` hooks intercept every tool call for observability

*Source: claude-agent-sdk-demos/research-agent/README.md*

### Subagent-Driven Development: Two-Stage Review Workflow

- Fresh subagent per task: subagents never inherit the orchestrator's session context; the controller constructs exactly what they need, preserving its own context for coordination
- Two-stage review sequence: spec compliance first (does the code match the spec, no more, no less?) → code quality review second; code quality review must NOT start before spec compliance is confirmed
- Implementer statuses: DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED -- each has a defined handling path; never ignore an escalation
- Model selection by task complexity: mechanical tasks (1-2 files, clear spec) → cheapest model; integration and judgment tasks → standard; architecture and review → most capable
- Lean context for pattern-based tasks: providing only task description, file path, pattern reference, and verify command (vs. full plan file) produced faster, more focused, higher first-attempt success rate
- (see [agent-design.md](agent-design.md#meta-agent-architecture) for the broader Meta-Agent pattern and [workflow-patterns.md](workflow-patterns.md#pattern-3-meta-agent-orchestration) for the two-terminal setup)
*Source: superpowers/skills/subagent-driven-development/SKILL.md*

### Agent Specs: Declarative Agent Configuration in YAML

- `Agent.from_file('agent.yaml')` loads a full agent definition (model, instructions, capabilities, model settings, output schema) from YAML or JSON -- separates agent configuration from application code
- Enables non-developers to configure agents without touching Python; supports storing agent definitions alongside other config files
- Handlebars-style `{{variable}}` template strings in instructions are rendered against agent dependencies at runtime -- validated at construction time when `deps_type` is provided
- Scalar fields in specs are overridden by keyword args; `instructions` and `capabilities` are merged (spec-first); `model_settings` are merged additively
- `output_schema` in a spec sends JSON Schema to the model as a structural instruction but does not validate the returned dict at runtime -- schema-as-prompt vs schema-as-validation is a meaningful design distinction
*Source: pydantic-ai/docs/agent-spec.md*

---

## Meta-Agent Architecture

### The Core Idea: Strategy-Only Opus + Worker Subagents

The meta-agent pattern separates **strategic thinking** from **tactical implementation** into different AI sessions. This directly addresses Vision Compression -- the failure where strategic context gets evicted as implementation detail accumulates (see [failure-patterns.md#1-vision-compression](failure-patterns.md#1-vision-compression)).

```
Human <--REPL--> Meta-Agent (Opus, strategy-only)
                      |
            +---------+---------+---------+---------+
            |         |         |         |         |
         researcher  code-    reviewer  writer   state-
         (Sonnet)    builder  (Sonnet)  (Sonnet)  updater
                     (Sonnet)                     (Haiku)
```

### The System Prompt Rule: Meta-Agent NEVER Writes Code

The meta-agent's system prompt explicitly forbids implementation:
- It thinks in **goals, constraints, dependencies, and patterns**
- It delegates all file creation, editing, and command execution to workers
- It reads and writes only state files (markdown)

This separation is the entire point. The moment a strategic agent starts writing code, its context fills with implementation detail and the strategic view degrades.

### The Five Subagents

| Agent | Model | Role | Tools |
|-------|-------|------|-------|
| **Researcher** | Sonnet | Explore codebases, read docs, gather information | Read, Glob, Grep, WebSearch, Bash |
| **Code-Builder** | Sonnet | Implement scoped tasks, run tests to verify | Read, Write, Edit, Bash, Glob, Grep |
| **Reviewer** | Sonnet | Review code for bugs, security, style. Cannot modify files | Read, Glob, Grep, Bash |
| **Writer** | Sonnet | Documentation, comments, user-facing messages. Match existing tone | Read, Write, Edit, Glob, Grep |
| **State-Updater** | Haiku | Surgical markdown edits to state files. Fast and cheap | Read, Write, Edit, Glob |

Model selection follows cost/capability matching: Opus for strategy (expensive but worth it for decisions), Sonnet for implementation and review, Haiku for mechanical updates.

### State Files as Shared Memory

State lives in `state/` as plain markdown -- readable by both humans and agents:

| File | Purpose |
|------|---------|
| `workstreams.md` | Active work items, status (PROPOSED > ACTIVE > REVIEW > SHIPPED), constraints, dependencies |
| `decisions.md` | Architectural choices with context, alternatives considered, and rationale |
| `patterns.md` | Reusable patterns discovered during work (name, observation, principle, implication) |
| `session-log.md` | What happened this session (append-only) |
| `handoff.md` | Implementation prompts drafted by meta-agent for Claude Code sessions |

### Two-Layer Persistence

**Layer 1 -- SDK sessions (automatic):** The Claude Agent SDK stores full conversation history. Pass `resume: sessionId` to continue. Sessions can be forked to explore alternatives (see [memory-persistence.md#layer-4-sdk-session-persistence-meta-agent-pattern](memory-persistence.md#layer-4-sdk-session-persistence-meta-agent-pattern)).

**Layer 2 -- State files (explicit):** The meta-agent reads state files at session start, writes them before exit. Humans can edit between sessions. State files survive even if the SDK session is lost. This is the same markdown-as-memory principle used in CLAUDE.md and worklogs, extended to orchestration state.

### Search-First Decision Taxonomy: Adopt, Extend, Compose, or Build

Before writing custom code, agents should follow a research-first workflow that prevents reinventing the wheel. This applies both to the meta-agent's planning phase and to any subagent tasked with implementation.

**5-step flow:** Need analysis, parallel search (npm/PyPI, MCP servers, Claude skills, GitHub), candidate evaluation (functionality, maintenance, community, docs, license, dependencies), decision, implementation.

**Decision matrix:**

| Signal | Action |
|---|---|
| Exact match, well-maintained, MIT/Apache | **Adopt** -- install and use directly |
| Partial match, good foundation | **Extend** -- install + write thin wrapper |
| Multiple weak matches | **Compose** -- combine 2-3 small packages |
| Nothing suitable found | **Build** -- write custom, but informed by research |

**Quick mode checklist (before writing any utility):** (1) Does it exist in the repo already? (2) Is it a common problem? Search npm/PyPI. (3) Is there an MCP for this? (4) Is there a skill for this? (5) Is there a GitHub implementation? Search before writing.

**Multi-agent integration:** The planner should invoke a researcher before architecture review; the architect consults the researcher for stack decisions. Combine with iterative retrieval (see [Cross-Agent Coordination Patterns](#iterative-retrieval-sub-agent-context-negotiation)) for progressive discovery across cycles.

**Anti-patterns:** Jumping to code without searching, ignoring MCP capabilities, over-wrapping libraries, installing massive packages for one small feature.

*Source: everything-claude-code/skills/search-first/SKILL.md*

### Make-Plan / Do: Documentation-First Orchestration

- `make-plan` is a pure orchestrator: subagents do fact-gathering (docs, API signatures, grep), orchestrator synthesizes and writes the plan -- no implementation in planning phase
- Phase 0 is always "Documentation Discovery": subagents identify actual available APIs (not assumed), anti-patterns to avoid, and copy-ready snippet locations
- Subagent Reporting Contract: each subagent response must include (1) sources consulted, (2) concrete findings with exact paths/signatures, (3) copy-ready snippet locations, (4) confidence + known gaps; reject and redeploy if conclusions lack sources
- Task framing: "Copy the V2 session pattern from docs/examples.ts:45-60" (good) vs "Migrate the existing code to V2" (bad) -- direct agents to docs, not outcomes
- `do` executes the plan: each phase uses fresh subagents; after each phase, deploy Verification, Anti-pattern check, Code Quality, and Commit subagents in sequence; only commit after verification passes
- (see [agent-design.md](agent-design.md#meta-agent-architecture) for the broader Meta-Agent pattern)
*Source: claude-mem/plugin/skills/make-plan/SKILL.md, claude-mem/plugin/skills/do/SKILL.md*

### Agent Harness Engineering: Every Mistake Becomes a Rule
- **Definition (Vinod Trivedy):** Agent = Model + Harness. The harness is every piece of code, configuration, prompts, tools, hooks, sandboxes, subagents, feedback loops, and observability wrapped around the model. "If you're not the model, you're the harness."
- **The ratchet pattern:** treat every agent mistake as a permanent signal, not a one-off flake. If the agent ignored a convention, add it to AGENTS.md. If it ran a destructive command, write a hook to block it. If it got lost in a 40-step task, split the architecture into planner + executor. Every line in a good system prompt should trace back to a specific historical failure.
- **Working backwards from behavior:** every harness component must have a distinct job ("Behavior we want → Harness design to achieve it"). If you cannot name the specific behavior a component exists to deliver, remove it.
- **Context-rot management techniques:** compaction (summarize older context), tool-call offloading (store massive outputs in filesystem, keep headers/footers in context), progressive disclosure (reveal instructions only when task requires them).
- **Long-horizon execution patterns:** loops (intercept exit attempts, force continuation against completion goal in fresh window), planning (decompose to step-file with self-verification hooks), splits (separate generation and evaluation agents to defeat positive grading bias).
- **Hooks as enforcement layer:** "success is silent, failures are verbose." If typecheck passes, agent hears nothing; if it fails, error injects directly back into loop for self-correction.
- **Harnesses Don't Shrink, They Move:** as models improve, scaffolding shifts — outdated scaffolding gets removed, new scaffolding gets built to reach the next horizon. Every component encodes an assumption about what the model cannot do alone.
- **Harness-as-a-Service trajectory:** industry shifting from LLM APIs (completions) to Harness APIs (runtime with loop, tools, context management, hooks, sandboxes). Fred Schott's "Flue" cited as example.

*Source: 2026-05-09-addyosmani-httpstcofsx0recclh.md*

---

## The Claude Agent SDK

The SDK (`@anthropic-ai/claude-agent-sdk`) gives programmatic access to the same tools, agent loop, and context management that power Claude Code.

### Core API Shape

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "...",
  options: {
    systemPrompt: "...",
    model: "claude-opus-4-6",
    allowedTools: ["Read", "Edit", "Bash", "Glob", "Grep", "Task"],
    permissionMode: "acceptEdits",
    agents: { /* subagent definitions */ },
    resume: sessionId,       // resume previous session
    forkSession: true,       // fork from a session
    hooks: { /* lifecycle hooks */ },
  }
})) {
  // Stream messages as the agent works
}
```

**Subagent definition (inline):**
```typescript
agents: {
  "researcher": {
    description: "When to use this agent",
    prompt: "System prompt for the agent",
    tools: ["Read", "Glob", "Grep"],
    model: "sonnet"
  }
}
```

### Key Constraint: Subagents Cannot Spawn Subagents

The SDK enforces a flat hierarchy. Only the top-level agent can use the `Task` tool to spawn subagents. This prevents runaway delegation chains and keeps the orchestration layer legible.

### Default: Read-Only

SDK permissions default to read-only (file reading, grep, glob). Write permissions must be explicitly enabled via `allowedTools` or `.claude/settings.json`. This is a safety-first design that forces you to opt in to destructive capabilities.

### Hooks

Lifecycle hooks (`PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`) run at key points. Practical uses: audit logging all tool calls, injecting "persist state" reminders before exit, tracking subagent spawn/completion times.

### Initializer + Coding Agent Pattern

A two-part SDK pattern for long-running feature development:

- **Initializer agent:** Bootstraps the project by creating a `claude-progress.txt` file (tracking what is done/pending), an initial commit, and a feature-to-test JSON spec with `"passes": false` flags for each feature
- **Coding agents:** Make incremental progress in multi-hour batches; each run reads `claude-progress.txt`, implements the next feature, runs tests, updates the progress file, and commits
- Session bridging via artifacts: progress logs and clean commits persist across sessions, eliminating the need for manual handoff prompts
- The feature-to-test JSON acts as an automated acceptance test: the agent iteratively builds until all `"passes"` flags become `true`
- This pattern is distinct from worklogs (see [memory-persistence.md](memory-persistence.md)) in that it is fully machine-readable and drives automated convergence rather than human review

*Source: deep-research-report.md*

### Claude Managed Agents: Production Agent Infrastructure
- Anthropic's managed agent hosting: define the agent, Anthropic handles infrastructure, security, sandboxing, and uptime. Prototype to production in days
- **Four building blocks:** Agent (instructions + model + tools), Environment (pre-loaded workspace), Session (persistent conversation with file access), Events (message stream with approval gates)
- **Two execution modes:** Auto-run (agent handles everything) and Approval-required (agent pauses before sensitive actions). Mixable per tool -- e.g., auto-approve file reads, require approval for emails
- **Pricing:** Standard API token rates + $0.08/session-hour + $10/1K web searches. Typical 10-minute session costs cents
- Business model template: $999 AI audit to identify client time wasters, build managed agent for top problem, charge $500/month recurring maintenance
- Public beta on Claude Platform as of 2026-04-08

(see [workflow-patterns.md](workflow-patterns.md) for orchestration patterns that apply to managed agent design)

*Sources: 2026-04-08-claudeai-introducing-claude-managed-agents-everything-you-need-to-bui.md, 2026-04-09-coreyganim-httpstco3dxtbhbgwu.md*

---

## Brain + Muscles Pattern (from OpenClaw)

OpenClaw uses a multi-model architecture for always-on autonomous agents. The terminology differs from meta-agent but the principle is the same: separate orchestration from execution.

### Brain: Orchestration Model

The **brain** is the model chosen during setup -- typically Opus for its decision-making quality. It orchestrates what to do, routes tasks to appropriate muscles, and maintains the agent's personality and memory. The brain decides; it does not do the grunt work.

### Muscles: Specialist Models

Each muscle is optimized for a specific task type:

| Muscle | Provider | Best For |
|--------|----------|----------|
| Codex | OpenAI | Code generation (cheap, powerful for implementation) |
| XAI / Grok API | xAI | Trending news, real-time social media data |
| Brave API | Brave | Web search, current information retrieval |
| Local models (MiniMax, Qwen) | Self-hosted | Free execution, unlimited tokens, privacy |

The brain saves tokens (and money) by delegating execution to cheaper models. A coding task routes to Codex instead of consuming expensive Opus tokens. A news-gathering task routes to XAI because it has real-time social media access that Opus lacks.

**Local models as muscles:** Running models locally (via Mac Mini, Mac Studio, or equivalent hardware) eliminates per-token costs entirely. Start with cloud APIs, then progressively replace muscles with local equivalents as workflows mature.

### Tool-Centric Safety Over Model-Centric Trust

OpenClaw's architecture reveals a design philosophy applicable beyond its ecosystem: constrain what the agent **can do**, not what it **might say**.

- **Three distinct safety levers:** tool policy (which tools are callable), sandboxing (where tools run -- host vs container), and elevated mode (explicit escape hatch for host access). These are separate concerns, not a single "security level" dial
- **Policy composition is fragile:** tool availability depends on layered profiles (global, provider-specific, agent-specific, sandbox-specific) with deny-wins precedence. "Unexpected blocked tool" and "unexpectedly not sandboxed" are recurring failure patterns when layers interact
- **More sandboxing can reduce reliability before it increases safety:** default sandbox containers have no network access -- tools that need package installs or outbound fetch fail silently, cascading into retries and context overflow
- On constrained hardware, concurrency caps on multi-agent setups should be treated as a **resource governor**, not a throughput knob -- each parallel session consumes memory for context, tool execution, and session persistence (see [autonomous-agents.md](autonomous-agents.md) for OpenClaw-specific setup)

*Source: OpenClaw Ecosystem Systems Intelligence Outline for Constrained Hardware, Privacy-First Use, and Curriculum Readiness.md*

### Local Model Hybrid: Brain/Muscles with Qwen 3.5

- Frontier API (Opus/Sonnet) as "brain" for planning; local model (Qwen 3.5-35B-A3B via LM Studio/Ollama) as "muscles" for execution
- Execution is ~90% of token usage -- offloading to local model saves costs while retaining frontier planning quality
- Qwen 3.5-35B-A3B runs on 32GB Mac Mini (4-bit MLX, ~20GB footprint)
- Multi-agent factory: 4 agents on same product with QA agent (Ralph) reviewing every task and editing memories on errors
- (see [autonomous-agents.md](autonomous-agents.md) for LM Studio setup details)

*Source: Unlimited Free OpenClaw.md*

### OpenClaw Bot Business Experiment (@petergyang)

- @nateliason gave his OpenClaw bot "Felix" $1,000 to build its own business
- Felix earned $14,718 in three weeks: launched a website, info product, and skills marketplace
- Key setup details: 3-layer memory system, security config, daily workflows
- Demonstrates autonomous agent commercial viability

*Source: Threads/petergyang - OpenClaw Bot Business Experiment.md*

### 11 OpenClaw Effectiveness Hacks

- Multi-model specialization: Opus for brain, Codex for coding, MiniMax 2.5 for research, Qwen 3.5 for writing
- Local hosting enables workflows impossible remotely (e.g., AirDrop video -> auto-transcribe -> translate to 10 languages)
- Channel strategy: Telegram for quick messages, Discord for complex multi-channel workflows
- Reverse prompting for idle agents: "Based on what you know about me, what is the next best task?" -- better than directive prompting
- Security: do not give agents email access (prompt injection) or X/Twitter accounts (bot crackdowns)

*Source: 11 hacks that will make your OpenClaw go from useless to AGI.md*

### Adaptive Tone for Behavioral Change

AI accountability coach using context-aware messaging instead of static reminders:

- **Pattern:** Daily proactive check-ins via Telegram at scheduled times; agent tracks streaks and adapts tone based on performance ("Day 15, don't break it now")
- **Pattern detection:** Agent identifies recurring behaviors ("always skip workouts on Wednesdays") and surfaces them back to user
- **Why static reminders fail:** Generic reminders get ignored; context-aware messages that reference streak length and personal patterns actually motivate
- **Weekly analysis:** Pattern analysis across all tracked habits with trend visualization

*Source: awesome-openclaw-usecases/usecases/habit-tracker-accountability-coach.md*

### When to Use Brain+Muscles vs Meta-Agent

Both patterns separate strategy from execution. The difference is context and autonomy:

- **Brain+Muscles** = always-on autonomous agent. Runs 24/7, proactively initiates work (via cron/heartbeats), communicates through messaging (Telegram/Discord), self-improves by building its own skills and tools. The human is a manager, not a pair programmer.
- **Meta-Agent** = developer-in-the-loop sessions. Runs during work sessions, human drives the conversation, meta-agent plans and delegates to subagents. The human reviews every output. Better for code-heavy projects where correctness matters more than autonomy.

### Advanced Operating Principles for Autonomous Agents

- Orchestrator principle in SOUL.md: "Strategize and spawn employee agents. Never do heavy lifting inline. Keep main session lean."
- Safety exception gate: pre-approval for changes affecting runtime, data, cost, auth, routing, or external outputs
- Self-evolution protocol: agent proposes improvements to soul document for human review -- never self-edits without approval
- Git safety as soul-level rule: never force-push, delete branches, rewrite history, or push env variables without permission
- Config change discipline: never guess; read docs, backup first, then edit

*Sources: Thread by @kloss_xyz 1.md, Before You Do Anything With OpenClaw.md*

### Advisor Strategy on Claude Platform: Opus + Sonnet/Haiku
- Official Anthropic pattern: pair Opus as an advisor with Sonnet or Haiku as the executor agent
- Near Opus-level intelligence at a fraction of the cost -- the advisor provides judgment on complex decisions while the cheaper model handles execution
- Platform-native implementation of the brain/muscle architecture already documented in OpenClaw's multi-model pattern

(see [agent-design.md](agent-design.md#brain-orchestration-model) for the OpenClaw brain/muscle equivalent)

*Source: 2026-04-09-claudeai-were-bringing-the-advisor-strategy-to-the-claude-platform-pa.md*

---

## Skills vs Subagents: Same Brain or Separate Invocation

Skills are distinct from both personas and subagents. A **skill** is a set of instructions (a `SKILL.md` file) that an existing agent loads on demand -- same brain, same memory, same context, just a new playbook. A **subagent** is a separate invocation with its own context window that starts from zero.

- Skills preserve full context across task switches -- the agent retains everything from SOUL.md, USER.md, and prior conversations while adopting new instructions
- One agent with N skills loads identity context once; N separate agents load it N times (the "N x context loading" cost problem)
- **Channels as departments:** map messaging channels to skills so the agent auto-selects the right capability based on where the message arrives (e.g., `#finances` loads the finance skill, `#x-scan` loads the social media skill)
- Skills add capability without removing context; if you mention a cross-domain topic while using a skill, the agent still has that background
- **Rule of thumb:** if you do something more than twice, make a skill for it. Reserve subagents for heavy isolated tasks that would clog the main conversation (see [skills.md](skills.md))
- Community skill ecosystems (e.g., ClawHub) allow installing pre-built skills -- one markdown file, no extra API keys or instances

### Five Skill Patterns from Anthropic's Skills Guide (@Hartdrawss)

Anthropic released a 32-page guide on building Claude Skills. Three core use cases: document creation, workflow automation, and MCP enhancement (layering domain expertise onto tool access). Five proven patterns:

1. **Sequential Workflow:** Step-by-step processes in specific order (onboarding, deployment, compliance)
2. **Multi-MCP Coordination:** Workflows spanning multiple services (design handoff from Figma to Linear to Slack)
3. **Iterative Refinement:** Output that improves through validation loops (report generation with quality checks)
4. **Context-Aware Selection:** Same outcome, different tools based on file type, size, or context
5. **Domain Intelligence:** Embedded expertise beyond tool access (financial compliance rules, security protocols)

Common mistakes: vague descriptions that never trigger, instructions buried in verbose content, missing error handling for MCP calls, trying to do too much in one skill (see [skills.md](skills.md)).

*Source: Twitter-Bookmarks/Thread by @Hartdrawss.md*

### ce:ideate: Proactive Divergent Ideation Skill

- Standalone skill for proactive idea generation -- the inverse of brainstorm (reactive/convergent); different cognitive mode, different outputs
- Core mechanism: generate ~30 ideas → adversarially self-critique and reject weak ones with explicit reasoning → present top 5-7 survivors with description/rationale/downsides/confidence/complexity
- Rejection summary is first-class output: shows what was considered and cut, preventing re-exploration of dead ends
- Durable artifact written to `docs/ideation/YYYY-MM-DD-<topic>-ideation.md` -- compounds across sessions
- Handoff is always to `ce:brainstorm` -- ideation is never detailed enough to skip requirements refinement
- Sub-agent architecture: parallel ideation sub-agents receive same grounding + focus hint; orchestrator owns final scoring and ranking
*Source: compound-engineering-plugin/docs/brainstorms/2026-03-15-ce-ideate-skill-requirements.md*

---

## When to Use Which Architecture

| Complexity | Solo Session | + Personas | + Subagents | Meta-Agent | OpenClaw (Brain+Muscles) |
|------------|-------------|------------|-------------|------------|--------------------------|
| Fix a bug, write a test | Use directly | -- | -- | -- | -- |
| Feature with auth/payments | -- | Full persona review | -- | -- | -- |
| Multi-file feature, needs review | -- | Optional | Reviewer agent on different model | -- | -- |
| Multi-workstream project | -- | -- | -- | Opus plans, subagents execute | -- |
| Ongoing autonomous workflows | -- | -- | -- | -- | Brain orchestrates, muscles execute 24/7 |

**Decision heuristic:**
- Single task, low risk --> plain Claude Code session
- Single task, high risk --> add persona review, enforce model diversity
- Multiple parallel tasks --> subagents with tool restrictions
- Strategic project spanning sessions --> meta-agent with state files
- Autonomous agent running without you --> Brain+Muscles with cron jobs, messaging, and self-improvement loops

The architectures compose. A meta-agent can use persona-style review prompts in its reviewer subagent. An OpenClaw brain can delegate to a meta-agent pattern for complex coding projects. Start simple, add layers only when you hit the limits of the current approach.

### Claude as Orchestrator vs Component

Two contrasting architecture patterns used by power users:

- **Orchestrator pattern:** Claude drives the workflow, using Agent Teams or Agent SDK to assign sub-tasks to itself. Suitable for complex CI-style pipelines where Claude leads planning and delegation
- **Component pattern:** External scripts (CLI wrappers, GitHub Actions, shell pipelines) call Claude as a worker component. Claude does focused work (generate code, review PR, write docs) but does not manage the overall workflow
- Power users often blend both: Claude as orchestrator for complex features requiring judgment, Claude as component for mechanical CI/CD steps
- **RAG-heavy vs Prompt-heavy knowledge:** For large corpora (docs, logs), use vector DB retrieval at runtime. For small structured knowledge (API signatures, FAQs), store in memory or CLAUDE.md. Some prefer hooking into wiki tools (Context7, DeepWiki) for on-demand facts rather than pre-loading
- **Stateless vs State-managed workflows:** Expert teams increasingly use state-managed patterns (e.g., `claude-progress.txt` + git commits between sessions). The initializer + coding agent pattern (see [The Claude Agent SDK](#the-claude-agent-sdk)) exemplifies statefulness. Stateless (one-off prompt-response) is simpler but limited to independent tasks

*Source: deep-research-report.md*

### The Coordination Tax: Why More Agents Often Means Worse Output

- Google DeepMind research shows accuracy **saturates or degrades past 4 agents** due to coordination overhead -- called the "Coordination Tax"
- The "17x error trap": naively adding agents to a system multiplies error rate, not throughput
- Multi-agent failure mode: agents don't share context, a coordinator agent burns tokens relaying messages, handoffs lose nuance, and debugging becomes "which of 8 agents broke?"
- A study testing **162 different roles** across four LLM families (GPT, Claude, Llama, Mistral) on 2,410 factual questions found generic role labels produce **zero statistically significant improvement** -- the effect was "largely random"
- The practical consolidation path: one practitioner went from 17 agents to 4 core roles (Architect, Builder, Money Maker, Operator) with a **specialist library** of 36+ pre-defined types selected dynamically at spawn time -- never generated at runtime, never running as persistent agents (see [workflow-patterns.md](workflow-patterns.md) for orchestration patterns)

### Agent Swarm Critique: Pipeline Structure vs Coordination Overhead

29-agent swarm plugin proposes a 5-step methodology: Brainstorm -> Plan -> Work -> Review -> Compound.

- The **Compound step** is the genuinely novel contribution: 5 agents extract root cause, fix, and prevention from every solved problem into a searchable knowledge base inside the repo
- Community consensus: the pipeline structure (forcing narrow-then-wide execution) is the real value, not the agent count
- **Critical failure mode:** when agent 1's output is wrong, agents 2-29 build on bad assumptions -- cascade failure with no recovery
- Coordination overhead often cancels parallelism gains; 3-4 agents is the practical ceiling before diminishing returns
- "More parallel isn't better -- knowing when to stay quiet is"
- Cost concern: AI orchestrators directing other AI agents produce bloated coordination costs
- Repo was archived by owner -- suggests maintenance burden exceeded value
- Takeaway: structured methodology (brainstorm, plan, execute, review, compound) works; massive parallelism does not

*Source: Twitter-Bookmarks/2026-03-08-dan__rosenthal-29-agent-swarm-plugin.md*

### Enterprise Agent Architectures: Solo, Parallel, Collaborative

From @vasuman (Varick Agents, $3M ARR deploying production agents for enterprise). Three architectural patterns:

- **Solo Agent:** One agent handles complete workflow start to finish. Easiest to build (all context stays in one place). Challenge: late-stage decisions lose early-stage context if memory isn't structured
- **Parallel Agents:** Multiple agents work different pieces of same problem simultaneously. Faster but creates coordination problem: contradictory conclusions need a judge (human or LLM) to resolve
- **Collaborative (Sequential Handoff):** Agent A triages, passes to B for research, passes to C for resolution. Handoffs are the failure point -- whatever A learns must survive transition in a format B can use
- **Enterprise Reality:** Most deployed agents are a mix of parallel + collaborative. "Architecture matters more than model selection"
- **Context as $1M Differentiator:** "Context is often the biggest difference between an agent worth $1M and an agent worth $0"
- **Deploy Fast:** 3 months max to production. Year-long timelines mean building a ghost
- **Bespoke > SaaS:** "Most companies purchasing AI SaaS churn within 6 months." Bespoke agents accumulate capability; SaaS accumulates tech debt

(see [autonomous-agents.md](autonomous-agents.md#model-routing-brainmuscles-with-specific-model-picks) for model routing across these architectures; see [failure-patterns.md](failure-patterns.md#dashboard-trap-catch-exceptions-dont-build-dashboards) for the "catch exceptions" anti-pattern from same source)

*Source: Twitter-Bookmarks/2026-01-11-vasuman-100x-a-business-with-ai.md*

### Production Agent Failure Handling and Guardrails

- Structured decision trees for routine cases; LLM only for ambiguous situations
- Every tool action must be logged, reversible where possible, and gated by permissions
- Three failure modes: retry with exponential backoff, human-in-the-loop, safe failures (never delete old data)
- 80/20 deployment: agents handle 80% of straightforward cases; 20% complex decisions routed to humans
- Build narrow first: one thing working reliably before expanding scope
- (see [failure-patterns.md](failure-patterns.md) for named failure patterns)

*Source: AI Agents 101.md*

### Full Claude Agent Stack: Single-Agent to Multi-Agent Teams

- Four-layer stack: (1) Claude Code (terminal agent, no code), (2) Claude Agent SDK (Python/TypeScript), (3) MCP (connection layer, 200+ servers), (4) Agent Teams (parallel orchestration with shared task lists)
- Agent decision tree: single Q&A = chat; multi-step/tool use/iteration = agent; distinct parallel specialist components = multi-agent; if you're copy-pasting Claude output back into Claude, you need an agent
- Core agent loop: Think → Act → Observe → Repeat; runs until complete or input needed
- Subagents have isolated context; every piece of information must be passed explicitly in the prompt -- they do not share memory with the coordinator

*Source: Twitter-Bookmarks/2026-03-14-heygurisingh-httpstcofjd05pvgt4.md*

### Claude Architect: Five Domains of Production Agent Engineering

- Agentic loop anti-patterns: never parse natural language for loop termination, never use arbitrary iteration caps as primary stopping mechanism, never check for assistant text as a completion indicator
- Subagents do NOT share memory with coordinator -- the most common misunderstanding in multi-agent design; every piece of information must be passed explicitly
- For financial/security-critical operations, prompt instructions alone are insufficient; enforce tool ordering programmatically with hooks and prerequisite gates
- Tool descriptions are the primary selection mechanism: vague or overlapping descriptions cause constant misrouting -- fix descriptions before adding few-shot examples
- Scope subagents to 4-5 tools each; giving an agent 18 tools degrades selection reliability
- CLAUDE.md hierarchy: user-level (~/.claude/CLAUDE.md), project-level (.claude/CLAUDE.md), directory-level; user-level config is NOT shared with team members
- Message Batches API: 50% cost savings, up to 24-hour processing; use for overnight reports; use synchronous for blocking pre-merge checks

*Source: Twitter-Bookmarks/2026-03-15-hooeem-httpstco4tchgza4oc.md*

### Five Maturity Levels of AI Workflows

- L1 = generic prompts (no memory, starts from zero); L2 = manual skill templates (requires human orchestration); L3 = skills + shared brand foundation (consistency across channels); L4 = agents with skills (one command triggers research→write→review pipeline); L5 = autonomous agent teams (agents share context, compound knowledge)
- The moat at L3-L5 is taste and judgment baked into the system, not just automation
- Adding memory is the L4→L5 transition: log what performs, feed performance data back into agent context
- Time investment: L1→L2 = 3-4 hours; L2→L3 = one weekend (brand foundation is the hard part); L3→L4 = 1-2 weeks; L4→L5 = ongoing infrastructure, not a project you finish

*Source: Twitter-Bookmarks/2026-03-16-shannholmberg-httpstcoec3dlribxt.md*

### Full Beginner's Guide to Building AI Agents

- Core agent loop: User input → LLM thinks → decides (respond or call tool) → if tool: execute, feed result back → repeat; frameworks wrap this loop but don't change its essence
- Workflows vs agents: workflows are deterministic (cheaper); agents are dynamic (LLM decides next step); start with the simpler workflow, graduate to agent only when needed
- Five core workflow patterns: Prompt Chaining, Routing, Parallelisation, Orchestrator-Workers, Evaluator-Optimiser
- Tool design principle: "Better tools = smarter agent. Fewer tools = more reliable agent." One tool = one clear job; tell the agent WHEN to use the tool, not just what it does
- Memory: most agents don't need it; start with no memory; add conversation history only when needed; avoid vector DBs until proven necessary
- Multi-agent: start with one agent; only add more when tasks are clearly split; safest pattern is supervisor model; never start with a swarm
- Biggest beginner mistake: building an all-purpose "super agent" with 20 tools and complex memory before the simple version works

*Source: Twitter-Bookmarks/2026-03-26-hooeem-httpstcokw3rqbdbjt.md*

### AI Workforce OS: The Operations Problem Nobody Has Solved

- The missing layer: every framework (n8n, LangChain, CrewAI, AutoGen) solves agent construction, not operations -- no unified way to manage a fleet of deployed agents, assign new work via natural language, or share state across agents
- AI workforce OS requirements: (1) natural language command interface for creating/directing agents without code; (2) unified resource management -- shared knowledge/files/credentials at workspace level, not per-agent; (3) execution observability -- single audit trail for every agent action; (4) enterprise access controls; (5) self-hostability
- Key insight: "an AI workforce OS is not a builder. It's a command center."
- The operations gap is the structural bottleneck: teams that solve operations first have a compounding advantage; model capability is no longer the bottleneck
- Agents become workers not scripts: give them new instructions when requirements change, don't redeploy from scratch; non-technical stakeholders can participate when the interface is natural language

*Source: Twitter-Bookmarks/2026-03-24-akshay_pachaar-httpstco3pyc2a2jrc.md*

### Leverage Doctrine: Human/Agent Role Separation

- Human role = ideation, discernment, decisions; agent role = research, execution, implementation; information flows up, decisions flow down
- Co-evolutionary framing: structured approach makes the human a more rigorous thinker; human's accumulated discernment makes the agent more effective -- both improve over time
- Orchestrator-first: the session agent is an orchestrator, not an implementer -- assess execution mode before any task: handle directly (simple), delegate to subagent (complex, benefits from fresh context), route to MCP (external system where only the result matters)
- Don't over-orchestrate: define objectives and give tools, not step-by-step sequences -- rigid orchestration is wiped out by the next model improvement
- Separation of concerns: agents that research and design the plan should NOT be the ones that implement it
- (see [agent-design.md](agent-design.md#meta-agent-architecture) for the full Meta-Agent pattern)
*Source: claude-code-synthesis/CLAUDE.md*

### The Multi-Agent Spectrum: Subagents vs Independent Sessions vs Serial (Andrew Orobator Pt 9)
Three distinct patterns for running multiple agents -- which to reach for depends on the work AND the system's resource ceiling.

- **Subagents (parent → child, isolated context windows):** parent only receives the summary, not the full search trail -- subagents *save* context by doing deep work in their own windows. Limit: they can't coordinate laterally, only with the parent.
- **Independent sessions (separate editor windows + git worktrees):** no shared context at all. Design work so agents don't *need* to coordinate -- choose tasks that are genuinely independent. If two agents touch the same file, you picked the wrong tasks to parallelize. On platforms with fast builds, independent sessions usually beat serial on wall-clock.
- **Serial handoffs (one agent at a time, structured handoff doc):** the `NEXT_AGENT_PROMPT` pattern -- each agent writes a structured handoff of what it found, what's left, what the next agent should be aware of. No compaction loss because nothing carries over in-context; the handoff file *is* the context. Steve Yegge's `Beads` (github.com/steveyegge/beads) takes this further with an issue tracker as shared working memory + dependency graph.
- **Decision rule:** subagents for parallel research, independent sessions for isolated implementation, serial handoffs for dependency-heavy or long-lived work. Most real workflows mix all three.
- **Sparkpass audit lesson:** 7-domain parallel subagent plan looked clean; machine couldn't handle simultaneous resource load → fell back to serial with `NEXT_AGENT_PROMPT` handoffs → found 23 gaps. The serial fallback shipped; the parallel plan only existed in theory.
- **The 6-agents-on-64GB lesson:** editing is cheap, **execution is the bottleneck**. 6 worktrees each spinning Gradle daemons + compiling Kotlin + running tests = swap-thrashing 193GB on a 64GB machine. Memory + Kotlin's absolute-path build cache + thermal throttling on M2 Pro make multi-agent localhost impractical for compiled languages with heavy build systems. For web devs with fast builds, fine. The fix is cloud agents.
- **When NOT to parallelize (Sergio Sastre Florez pushback):** if agents are running long enough to parallelize, the output is probably too large to review carefully. Most tasks don't need parallelism -- a task too simple wastes more on setup than it saves. **Hidden cost:** every agent you spawn makes you a manager (context-switch between worktrees, check progress, unstick blocked agents, review across multiple PRs). 3 parallel agents drain you faster than 1 focused session.
- **Ask the agent, not yourself:** "Can this work be parallelized?" -- agent considers file overlap, dependency chains, review burden. If it says no, that's a valid answer.

*Source: Andrew-Vibe-Coding/Vibe Engineering From Random Code to Deterministic Systems (Part 9).md*

---

## Tasks System (Replacing TodoWrite)

Persistent, cross-session task management stored at `~/.claude/tasks/` (global-only). Tasks survive restarts and crashes, support dependency graphs (`addBlockedBy`/`addBlocks`), and enable multi-session collaboration via shared `CLAUDE_CODE_TASK_LIST_ID`.

Four tools: `TaskCreate`, `TaskGet`, `TaskUpdate`, `TaskList`.

| Feature | Old Todos | New Tasks |
|---------|-----------|-----------|
| Scope | Single session | Cross-session, cross-agent |
| Dependencies | None | Full dependency graph |
| Storage | In-memory only | File system |
| Persistence | Lost on session end | Survives restarts |
| Multi-session | Not possible | Via shared task list ID |

---

## Agent Teams

Multiple Claude Code sessions coordinating on shared work. Enabled via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS: "1"` in settings env. Configs live at `~/.claude/teams/{team-name}/`. Two modes: **in-process** (all teammates in your terminal) and **split panes** (each teammate gets its own pane; requires tmux or iTerm2, not VS Code terminal).

### Lead vs Teammate Distinction

- The lead agent breaks tasks into pieces, spawns teammates, manages the shared task list, and synthesizes results
- Teammates are fully independent Claude Code sessions with their own context windows -- they talk to each other directly, not just report back to the lead
- Sub-agents report back summaries; agent team teammates communicate peer-to-peer through a shared task list

### Delegate Mode (Shift+Tab)

Locks the lead into coordination-only mode. The lead can only spawn teammates, assign tasks, send messages, and manage the task list -- it cannot do the work itself. Solves the common problem of the lead starting to implement instead of delegating.

### Task Assignment and Communication

- Tasks can be assigned by the lead or self-claimed by teammates. When a teammate finishes, it can automatically pick up the next unassigned task from the shared list
- In in-process mode, Shift+Up/Down cycles between teammates for direct communication without going through the lead. In split-pane mode, click into any teammate's pane

### Current Limitations (Research Preview)

- Session resumption does not work with in-process teammates; `/resume` or `/rewind` loses all teammates (spawn new ones)
- Task status can lag -- teammates may finish but not mark tasks complete, blocking dependents
- One team per session; teammates cannot spawn their own teams
- The session that creates the team is the lead for its entire lifetime (no promoting or transferring leadership)
- Split-pane mode requires tmux or iTerm2 (not VS Code terminal, Windows Terminal, or Ghostty)

### When to Use vs Sub-Agents

- Sub-agents: workers need to report back but not communicate with each other; cheaper on tokens; focused tasks
- Agent teams: workers benefit from peer collaboration; complex multi-part work; parallel hypothesis testing (debugging); cross-layer work (frontend + backend + tests)
- Not worth it for: sequential tasks where step 2 depends on step 1, same-file edits, simple tasks where coordination overhead exceeds benefit

### Quality Gates via Hooks

- Two lifecycle hooks for quality enforcement: `TeammateIdle` (exit code 2 sends feedback, keeps teammate working) and `TaskCompleted` (exit code 2 blocks completion with feedback)
- Teammates can work in read-only plan mode until lead approves their approach
- Task dependency management is automatic; file locking prevents race conditions on task claims
- (see [tools-and-integrations.md](tools-and-integrations.md) for hook configuration patterns)

*Source: Orchestrate teams of Claude Code sessions.md*

### Multi-Human Team Collaboration Patterns

Patterns for teams sharing Claude Code workflows:

- **Shared config as code review:** Version-control CLAUDE.md and treat updates like code changes -- one developer's update should be reviewed by others to prevent diverging instructions
- **Knowledge handoff via Tasks:** The persistent Tasks system enables one developer to create tasks that another's session picks up, replacing volatile in-session handoffs
- **Role differentiation:** Split work between prompting (writing specs/prompts) and reviewing (using Claude as AI reviewer). Tag roles in documentation or prompts (e.g., `[FrontendDev]`, `[BackendDev]`) for context
- **Onboarding via agent Q&A:** Give Claude search tools over internal docs/commits; new developers can ask "What's our architecture?" and get cited answers from CLAUDE.md or memory
- **CLAUDE.md conflict resolution:** When CLAUDE.md diverges on branches, merge manually like code. For memory inconsistencies, record conflicting facts with lower confidence and let agents arbitrate by checking documentation

*Source: deep-research-report.md*

### claude-peers: Multiple Claude Code Sessions Messaging Each Other

- claude-peers enables multiple Claude Code sessions to auto-discover each other and communicate directly via a local broker + SQLite peer registry + MCP servers
- Each peer session exposes: working directory, git repo, current task, and active files to other peers -- agents avoid conflicts by querying what others are editing
- Commands: list_peers, send_message, set_summary, check_messages -- coordination is peer-to-peer, not hierarchical
- Use cases: one Claude writes backend while another writes frontend; a research Claude feeds context to a builder Claude
- Everything runs locally -- this is a flat mesh pattern vs. the hierarchical agent teams pattern

*Source: Twitter-Bookmarks/2026-03-22-Suryanshti777-holy-shit-someone-just-made-claude-instances-talk-to-each-ot.md*

### Worktrees + Multi-Claude for Parallel Development

- Create git worktrees for independent task branches; run a separate Claude Code session in each worktree terminal
- Three-terminal pattern: Terminal 1 for main implementation, Terminal 2 for testing/validation in a test worktree, Terminal 3 for documentation
- Use `/clear` between tasks in the same session to prevent context pollution from prior task context
- Worktree task conflicts resolved by renumbering tasks to avoid merge conflicts in shared state files (e.g., `tasks.json`)
- (see [agent-design.md](agent-design.md#tasks-system-replacing-todowrite) for task state management)
*Source: claude-task-master/.taskmaster/CLAUDE.md*

### Hamster Pattern: Parallel Subtask Execution

- When subtasks operate on non-overlapping files, spawn parallel subagents -- one per subtask -- rather than executing sequentially
- Pre-check before parallelizing: confirm each subtask modifies a distinct set of files; if any overlap exists, serialize
- Quality gate: run lint + typecheck (not just tests); mark subtask done only if both pass; commit immediately; move to next subtask
- PR strategy: prefer one PR per task list (brief); split only when scope becomes unmanageable; always confirm multi-PR strategy with the human before creating
*Source: claude-task-master/.claude/hamster.md*

---

## Mission Control Pattern: Shared-Database Multi-Agent Architecture

A concrete implementation of multi-agent orchestration using OpenClaw, where 10 specialized agents coordinate through a shared Convex database rather than direct messaging.

### Core Architecture

- Each agent is an independent OpenClaw session with its own session key, SOUL.md, and memory files
- All agents read/write to a shared Convex database (real-time, serverless, TypeScript-native)
- A React frontend provides an activity feed, Kanban task board, agent status cards, and document panel

### Six-Table Schema

| Table | Purpose |
|---|---|
| `agents` | Name, role, status (idle/active/blocked), current task, session key |
| `tasks` | Title, description, status (inbox/assigned/in_progress/review/done), assignee IDs |
| `messages` | Task-scoped comments with sender and attachments |
| `activities` | Event log (task_created, message_sent, document_created, etc.) |
| `documents` | Deliverables, research, protocols as markdown |
| `notifications` | @mention notifications with delivery status |

### Operational Details

**Staggered heartbeat schedule:** Agents wake on 15-minute intervals, offset by 2 minutes each (:00 Pepper, :02 Shuri, :04 Friday, ...) to avoid concurrent resource contention.

**Thread subscription system:** Interacting with a task (commenting, getting @mentioned, being assigned) auto-subscribes you to all future comments -- natural conversation flow without requiring @mentions on every message.

**Agent levels:** Intern (needs approval for most actions), Specialist (works independently in domain), Lead (full autonomy, can delegate).

**Daily standup cron:** Nightly summary sent to Telegram showing completed/in-progress/blocked items, needs-review queue, and key decisions.

**Key lesson:** "I went from 1 to 10 agents too fast. Better to get 2-3 solid first, then add more."

(see [autonomous-agents.md](autonomous-agents.md) for OpenClaw setup details and [workflow-patterns.md](workflow-patterns.md) for orchestration patterns)

### Against Markdown-Only Context Graphs: The Case for Structured Databases

- Markdown files become "reinventing the database in the worst possible substrate" at scale -- no joins, indexes, or constraints
- Two-copy drift problem: when source documents get updated, extracted markdown notes become stale; a database with source IDs avoids this by design
- Better architecture: (1) work apps as source of truth, (2) file layer for hot-access metadata, (3) database as the graph storing typed relationships pointing back to sources
- Schema is context for agents: typed data tells an agent not just what a decision says, but whether it's active, who made it, what it superseded

*Source: Twitter-Bookmarks/2026-03-12-kevingu-httpstcodua8rdkzp5.md*

---

## Cross-Agent Coordination Patterns

### Shared-Context Correction Layer

- Shared-context layer (THESIS.md, FEEDBACK-LOG.md, SIGNALS.md) eliminates repeated per-agent corrections: one correction propagates to all agents
- One-writer rule: never have two agents writing to the same file; design every shared file with one writer and many readers
- Scheduling enforces dependency order: upstream agents (research) run before downstream agents (content)

*Source: How to set up OpenClaw Agents that actually get better Over Time.md*

### Iterative Retrieval: Sub-Agent Context Negotiation

Sub-agents receive a literal query but lack the orchestrator's semantic context -- they do not know the purpose behind the request. This produces technically correct but contextually wrong results. Iterative retrieval closes this semantic gap.

- **Iterative retrieval loop:** (1) Orchestrator evaluates every sub-agent return, (2) asks follow-up questions before accepting, (3) sub-agent returns to source with refined query, (4) loop until sufficient -- max 3 cycles to prevent token waste
- **Key rule:** Pass objective context, not just the query. Include why the information is needed, what it will be used for, and what "good enough" looks like
- **Orchestrator sequential phases:** Research (Explore agent produces research-summary.md), Plan (planner produces plan.md), Implement (tdd-guide produces code), Review (code-reviewer produces comments.md), Verify (build-error-resolver if needed). Each agent gets one clear input and produces one clear output
- **Phase discipline:** Outputs become inputs for the next phase. Never skip phases. Use `/clear` between agents. Store intermediate outputs in files

(see [workflow-patterns.md](workflow-patterns.md#pattern-4-rpi-workflow-research---plan---implement) for the RPI workflow)

*Source: everything-claude-code/the-longform-guide.md*

### Persistent State Machine with File-Based Checkpoints

Agent design pattern for multi-session debugging with state preservation:

- **State file:** `.planning/debug/{slug}.md` persists across context resets with structured YAML frontmatter
- **Five status phases:** gathering -> investigating -> fixing -> verifying -> awaiting_human_verify
- **Hypothesis testing discipline:** Each hypothesis requires a falsifiability criterion and evidence trail before transitioning phases
- **"Current Focus" section:** Tracks NOW state (not history) -- reduces context load on resume
- **Resume optimization:** Reads state file on startup, skips completed phases, continues from last checkpoint
- **Human blocking:** `awaiting_human_verify` status pauses autonomous execution until explicit confirmation

Applicable beyond debugging -- any multi-session agent task benefits from file-based state machines with explicit phase transitions.

*Source: get-shit-done/agents/gsd-debugger.md*

### Multi-Input Research Synthesis Pattern

Orchestration pattern where a synthesizer agent merges outputs from parallel researchers:

- **Pipeline:** 4 parallel researcher agents (ecosystem, feasibility, comparison, phase-specific) -> 1 synthesizer reads all outputs -> derives phase structure from combined findings
- **Division of labor:** Researchers write files but never commit; synthesizer commits all research files (prevents conflicting git operations)
- **Source hierarchy enforcement:** Context7 > Official Docs > WebFetch > WebSearch (each source type has a confidence weight)
- **Output:** Unified research document with confidence levels, user constraints preserved, and roadmap implications synthesized across all inputs

*Source: get-shit-done/agents/gsd-research-synthesizer.md*

### Multi-Angle Research Agent Specialization

- Parallel research agents assigned fixed epistemic roles: academic (peer-reviewed sources), technical (implementation details), applied (case studies/real-world use), news (recent developments), contrarian (opposing evidence, anti-confirmation-bias)
- The contrarian agent is required to seek disconfirming evidence -- without it, multi-agent research converges on the same consensus a single agent would reach
- Session persistence via `.research-session.json`: interrupted research resumes, not restarts; research state includes progress score (0-100) with principled termination at >=80 and strategy adjustment at <40
- Multi-wiki isolation: each research topic gets its own sub-wiki to prevent cross-topic noise; dual-link navigation (Obsidian wikilinks + standard markdown simultaneously)

*Source: github-repos.md (nvk/llm-wiki, 2026-04-06)*

### Strategy Learning Loop: Autonomous Trading Backtesting

Feedback-driven agent logic applied to prediction market trading:

- **Three strategies:** TAIL (trend-following), BONDING (contrarian), SPREAD (arbitrage) -- each with tunable parameters
- **Learning loop:** Execute -> measure results -> backtest -> identify best-performing strategy -> adjust thresholds -> repeat
- **Key pattern:** Agent doesn't just execute; it evaluates its own performance and adjusts. Generalizable to any autonomous workflow with measurable outcomes
- Paper trading mode for safe parameter exploration before live deployment

*Source: awesome-openclaw-usecases/usecases/polymarket-autopilot.md*

### Paperclip: Open-Source Agent Company Manager

- Paperclip (MIT) organizes agents into a company structure: org chart with roles, reporting hierarchy, monthly budgets per agent, shared goal hierarchy (company → projects → tasks)
- Heartbeat scheduling: agents wake on a schedule, check for work, execute, and sleep -- prevents runaway costs from 24/7 operation
- Budget controls: every agent gets a monthly spending limit; when hit, they stop -- eliminates surprise bills from agents stuck in loops
- Full audit trail: all work happens through tickets; every tool call is traced, every decision logged
- Key principle: managing a fleet of agents requires the same governance structures as managing a team of humans -- roles, reporting, budgets, oversight

*Source: Twitter-Bookmarks/2026-03-16-NickSpisak-httpstcobr90qmvlji.md*

### Stacking Paperclip + gstack + autoresearch for a One-Person AI Company

- Three-tool "AI company" stack: Paperclip (agent management/budgets/org chart), gstack (specialist skill roles: CEO/CTO/QA/release manager), autoresearch (autonomous overnight ML experiments)
- gstack commands cover the full build cycle: /office-hours → /plan-ceo-review → /plan-eng-review → /review → /qa (real browser) → /ship → /document-release
- /careful skill blocks destructive commands before execution; /freeze locks all files except the active folder during debugging
- autoresearch: 5 min/experiment × 12/hour × 8 hours = ~96 overnight experiments; hand it a research question and program.md, review results in the morning
- Power move: run 10-15 skills simultaneously across agent instances in parallel

(see [skills.md](skills.md) for skill design patterns)

*Source: Twitter-Bookmarks/2026-03-19-NickSpisak-httpstcoj5icd2geeq.md*

### Council of High Intelligence: 11-Agent Structured Disagreement Protocol

- A single model produces one coherent perspective -- not genuinely balanced output; structured multi-agent disagreement is the only way to get true perspective diversity
- Architecture: 11 independent subagents each with a unique analytical method and explicitly declared blind spots; 6 deliberate polarity pairs ensure every position has a structural opponent
- 3-round protocol: Round 1 = independent parallel analysis (400-word max each); Round 2 = sequential cross-examination (must engage 2+ others by name); Round 3 = crystallization to 100-word final positions
- Anti-recursion safeguards are critical: 3-level depth limit, 2-message cutoff per pair; without these, questioning agents consume the entire context window
- Consensus rules: 2/3 majority = consensus; no majority = present the dilemma to the user; minority reports are explicit output
- Use case targeting: architecture choices, strategic pivots, build-vs-buy; do NOT use for questions with clear correct answers

*Source: Twitter-Bookmarks/2026-03-19-nyk_builderz-httpstcoheyioentwi.md*

### LLM Council: Hidden-Identity Peer Review Pattern

- Structured 3-phase deliberation: (1) all models answer in parallel; (2) each model reviews others's responses with identities hidden (anti-anchoring); (3) a designated chairman model synthesizes into one final answer
- The hidden-identity step is the key anti-anchoring mechanism: reviewers evaluate argument quality without knowing the source, preventing status bias toward well-known models
- Practical complement to the Council of High Intelligence protocol (see [Council of High Intelligence](agent-design.md#council-of-high-intelligence-11-agent-structured-disagreement-protocol)) -- CoHI uses role-based polarity pairs and sequential cross-examination; llm-council uses identity-blind peer review with chairman synthesis; both address the single-model coherence trap
- Chairman synthesis pattern: one model tasked with reading all responses + reviews and producing the consolidated answer performs better than having all models converge simultaneously
- Stack: FastAPI backend + React frontend, OpenRouter for multi-model routing; open-source, self-hosted

*Source: github-repos.md (karpathy/llm-council, 2026-04-06)*

### Subconscious Agent: Self-Improving Loop Architecture

- Pattern for making agent systems self-improve continuously rather than requiring manual maintenance; analogous to human subconscious -- runs in background, brainstorms and debates improvements, writes results back into system so next run starts smarter
- **7 required components:** (1) runner (control plane: load brief → fetch state → run ideation → run critique → run synthesis → write artifacts → hand off); (2) persistent state (JSON for summaries/governance, JSONL for append-only history, markdown for human-readable outputs, stable directory structure); (3) scheduler/trigger (cron, post-metrics, post-signal, manual review); (4) transport layer (Discord, Telegram, file path, dashboard -- kept separate from reasoning layer); (5) model router (cheap/local model for ideation, strong model for synthesis/judgment); (6) human review gate (system can be smart without becoming reckless); (7) artifact writers (ideas/, debate/, winning-concept.md, improvement-backlog.md, run-summary.json)
- **Loop:** evidence gathering → generate candidate ideas → debate against hard objections with stronger model → synthesize one recommendation → persist result → next run starts from updated state
- Without durable state, the loop is broken -- system reenacts the same conversation every time; persistence is the real unlock
- Model routing principle: cheap local models for volume and exploration, frontier models for judgment and consolidation; that split keeps cost sane and quality high
- Guard against optimization gaming: add cronjob to evaluate changes, stop anything that tries to game the optimization loop; be realistic about run frequency per day (too many runs → excessive divergence from original principles)
- **Folder structure:** runner code / persistent state / per-run artifacts / target definitions / human-readable briefs -- keep separation, rename freely

*Source: Twitter-Bookmarks/2026-04-03-gkisokay-httpstcojyd5bktcab.md*

### Stateless Supervisor Architecture: PubSub Event Streaming

- CLI is a stateless renderer of supervisor state; supervisor owns all state management, agent lifecycle, and git operations
- Updates service as PubSub: executor publishes events, CLI subscribes via `stream()` -- no shared mutable state
- Domain models as immutable classes with computed getters: `addEvent()` returns a new instance; `testReport`, `activeStepId`, `completedCount` are getters, never computed in UI
- Tagged union events (`RunStarted`, `StepStarted`, `StepCompleted`, `StepFailed`, `ToolCall`, `ToolResult`, `RunCompleted`) replace interface unions -- type-safe, pattern-matchable
- Planner and Executor are separate services with single entry points: `Planner.plan(draft)` → `Executor.executePlan(plan)` → `Reporter.report(executedPlan)`; sequential composition
- Agent backend is injectable at the entrypoint: `Agent.layerClaude` or `Agent.layerCodex` -- the supervisor layer does not depend on a specific backend
*Source: expect/.specs/supervisor-refactor.md*

### Agent2Agent (A2A) Protocol and FastA2A

- Google's A2A protocol is an open standard for agent-to-agent communication regardless of framework -- `agent.to_a2a()` exposes any Pydantic AI agent as an ASGI A2A server in one line
- A2A distinguishes Task (one complete execution) from Context (conversation thread spanning multiple tasks, identified by `context_id`) -- context_id enables stateful multi-turn conversations across separate task executions
- FastA2A's Storage serves dual purpose: task storage (A2A protocol format) and context storage (agent-internal format including tool calls and reasoning traces) -- lean protocol wire format + rich internal state is the right decomposition
- Pydantic AI automatically stores complete conversation history (including tool calls) in context storage for continuity across `context_id` re-use
- FastA2A is framework-agnostic (built on Starlette/ASGI) -- any agent implementation can implement the Storage/Broker/Worker interface to participate in A2A
*Source: pydantic-ai/docs/a2a.md*

### Batch LLM Agent Orchestration

- 20-25 records per subagent is the recommended sweet spot for batch categorization -- too few = overhead; too many = context length issues and quality degradation
- Always include the full taxonomy/system prompt in every batch -- don't assume the model retains it from previous calls
- Save intermediate results incrementally (write each batch to output file) so progress is not lost if something fails; check coverage after each batch run
- Expect and plan for hallucinated variations in LLM output: a `fix_mappings` dict in the taxonomy corrects invalid tags automatically before they propagate
- Cost estimation example: 1,000 records × ~200 tokens each with Haiku ≈ $0.10-0.30
*Source: claude-code-synthesis/examples/data-pipeline/guides/agent-orchestration.md*

### Three-Phase Adversarial Review for AI Swarms
- Unanimous agreement from multi-agent analysis is a failure signal, not a success signal -- parallel agents with no cross-examination step produce groupthink dressed as consensus
- Three-phase protocol: Phase 1 (Independent Analysis -- specialists work blind to each other), Phase 2 (Cross-Examination -- reviewers read 2-3 specialist reports and must find problems), Phase 3 (Judgment -- coordinator rules on each conclusion: retain / needs more evidence / overturn)
- Hardcoded reviewer output contract is critical: "find 3 problems" as a hard requirement, not a suggestion -- without this constraint, reviewers politely agree and add nothing; structured verdict output (proceed / proceed_with_caution / block) enables programmatic state machine integration
- Global skeptic role: with 4+ specialists, add one reviewer who reads ALL reports and finds cross-report contradictions that look reasonable individually but conflict when combined
- State machine integration: if reviewers flag "block" and the synthesizer doesn't produce a clear "GO," the system automatically falls to HOLD and marks the task failed -- the adversarial layer has actual enforcement teeth, not just advisory output
- Distinct from existing multi-agent review patterns: CoHI uses role-based polarity pairs, LLM Council uses identity-blind peer review -- this pattern uses process-level questioning with rotation-based assignment and structured state machine enforcement

(see [Council of High Intelligence: 11-Agent Structured Disagreement Protocol](#council-of-high-intelligence-11-agent-structured-disagreement-protocol) for role-based polarity; see [LLM Council: Hidden-Identity Peer Review Pattern](#llm-council-hidden-identity-peer-review-pattern) for identity-blind review)

*Source: 2026-03-01-Voxyz_ai-httpstcowxwdysjgbi.md*

### Three-Layer LLM Council: Multi-Model + Custom Lenses + Verbalized Sampling
- Karpathy's original LLM Council (Nov 2025): same question routed to GPT, Claude, Gemini, Grok simultaneously; each reviews others anonymously; chairman model synthesizes. Real model diversity, fixed analytical framework.
- Ole Lehmann rebuild ran entirely inside Claude with five "thinking style" sub-agents (Contrarian, First Principles, Expansionist, Outsider, Executor). Gained customizable lenses, lost real model diversity.
- **The combined stack (alex_prompter):** three layers of diversity working simultaneously
  1. **Between-model diversity** -- different training data, alignment, blind spots. Perplexity Comet's Model Council routes to GPT-5.4, Opus 4.6, Gemini 3.1 Pro and a fourth synthesizer
  2. **Within-model diversity** -- verbalized sampling unlocks each model's tail distribution (see [prompt-engineering.md](prompt-engineering.md#verbalized-sampling-sampling-from-the-tails))
  3. **Analytical diversity** -- custom lenses defined per decision type (Bull/Bear/Macro/Portfolio for investors; Customer/Technical/Timing/Competition for founders; Audience/Distribution/Monetization/Longevity for creators). Lenses live in a markdown Skill file, Model Council provides multi-model output underneath.
- **Self-preference bias is in the EVALUATION step, not the generation step.** Single-model persona generation IS valuable -- asking Claude to think as Contrarian vs Expansionist DOES produce different outputs. The bias appears when Claude reviews Claude's five outputs and can't meaningfully differentiate because they all "feel" equally familiar (NeurIPS 2024, ICLR 2025, arXiv 2026). Fix: use different models for the peer-review step.
- When to use which: quick brainstorming = single-model council (free, fast); high-stakes decisions = Model Council + custom Skill + verbalized sampling

*Source: 2026-04-11-alex_prompter-httpstcoyhwxqinusq.md*

### Specialists Beat Generalists -- Vertical Partitioning for Review Agents (Andrew Orobator Pt 9)
Marvin Minsky's *Society of Mind* applied to agent architecture. Generalist agents reviewing batches lose accountability; specialists owning one concern catch issues consistently.

- **The Eagle Eye lesson:** v1 used 3 generalist subagents reviewing batches of screenshots for *all 15 things* (contrast, clipping, layout, touch targets, etc.). Low-contrast text shipped because all 3 generalists "checked for contrast" and **none of them owned it.** "When everybody's responsible, nobody's accountable."
- **Vertical partitioning fix (4 specialists, each owns ONE concern across ALL screenshots):**
  - **Text Contrast Agent** -- WCAG violations across all screenshots
  - **UI Clipping Agent** -- content overflow across all screenshots
  - **Layout Agent** -- design system spacing violations
  - **Touch Target Agent** -- interactive elements below 48dp
  - Coordinator aggregates findings into unified report
- **Why it works:** narrower prompts → lower token costs; each agent owns exactly one concern → things less likely to fall through; each specialist becomes more reliable on its single job over time
- **Three-layer Society-of-Mind architecture (Reddit Flag Lifecycle Agent):**
  - **Orchestration layer** -- discovery, validation, complexity scoring, spec generation
  - **Specialist layer** -- Planner → Coder → Reviewer 3-agent loop in cloud sandbox
  - **Platform layer** -- sandboxed execution, git, GitHub, experiment data APIs (MCP)
  - Each layer communicates via structured data; orchestrator doesn't write Kotlin; coder doesn't query experiment data; platform doesn't know what a flag cleanup is. Clean boundaries.
- **Pattern generalizes across stacks** -- AutonomyOS (Next.js/TypeScript): events → proposals → missions → concurrent steps → coordinator aggregates. Same shape: coordinator at top, specialists in middle, platform at bottom.
- (see [autonomous-agents.md > Flag Lifecycle Agent](autonomous-agents.md#flag-lifecycle-agent--the-self-driving-codebase-andrew-orobator-pt-10) for the production case study)

*Source: Andrew-Vibe-Coding/Vibe Engineering From Random Code to Deterministic Systems (Part 9).md*

### Buildroom Pattern: Auto-Think + Auto-Build with Role-Separated Agents
- **Two-lane split:** Auto-think (idea-intake layer) decides what *might* be worth building. Auto-build (verified build loop) decides what *can* be built, verifies it, and leaves receipts. Dreamer is not allowed to approve its own work.
- **Role separation (8 distinct):** Research (gathers evidence), Dreamer (notices signals → candidate idea contracts), Main (reviews, decides, writes bounded product plan), Coder (implements only approved bounded plans), QA (independently verifies), Trust reporting (summarizes room health: clean/watch/investigate), Retention (recommends keep/improve/park/prune), Operator (human-facing Control Room).
- **Idea contract = first durable handoff** from thinking to building. Captures: what should exist, who benefits, why now, supporting evidence, out-of-scope, where it might live, how it can be verified.
- **Verification delta states:** confirmed | drift | regression | missing_evidence. The system asks not just "did tests pass" but whether Coder evidence and QA evidence *agree*.
- **Public buildroom vs private runtime:** the reusable buildroom (schemas, demo packets, receipts) ships safely as a template. Private runtime state lives elsewhere. Critical separation for sharing the pattern without leaking state.
- **Guardrails encoded as architecture, not prompts:** Dreamer can't approve own builds. Dreamer can't mutate protected workflow surfaces. Coder can't expand scope silently. QA can't rubber-stamp Coder output. Retention can't delete live state on its own.

*Source: 2026-05-10-gkisokay-httpstcoukiiw3wmjq.md*

---

## Reference Agent Fleets

Production-tested agent fleet architectures that demonstrate how to compose specialized agents into a coordinated system.

### PR Review Toolkit: 6-Agent Multi-Dimension Review

Anthropic's official PR review toolkit bundles 6 specialized review agents, each with a distinct focus and confidence scoring.

| Agent | Focus |
|---|---|
| **comment-analyzer** | Audits comment accuracy vs actual code, documentation completeness, comment rot, misleading/outdated comments |
| **pr-test-analyzer** | Rates test gaps 1-10 (10 = critical). Checks behavioral vs line coverage, edge cases, error conditions |
| **silent-failure-hunter** | Flags silent failures in catch blocks, inadequate error handling, inappropriate fallbacks, missing error logging |
| **type-design-analyzer** | 4-dimension rating (1-10 each): type encapsulation, invariant expression, type usefulness, invariant enforcement |
| **code-reviewer** | General review for CLAUDE.md compliance, style violations, bug detection. Confidence scoring 0-100 |
| **code-simplifier** | Post-review pass for clarity, unnecessary complexity, redundant abstractions. Preserves functionality |

**Recommended sequence:** write, code-reviewer, silent-failure-hunter (if error handling changed), pr-test-analyzer, comment-analyzer, code-simplifier, create PR.

**Proactive triggering:** Agents can fire automatically based on context -- after writing code the code-reviewer activates; after adding docs the comment-analyzer activates.

(see [testing-verification.md](testing-verification.md) for verification patterns)

*Source: claude-plugins-official/plugins/pr-review-toolkit/README.md*

### Everything Claude Code: 13-Agent Development Fleet

A community plugin (50K+ stars, Anthropic hackathon winner) providing a production-ready agent fleet for software development.

**13 specialized agents:** planner, architect, tdd-guide, code-reviewer, security-reviewer, build-error-resolver, e2e-runner, refactor-cleaner, doc-updater, go-reviewer, go-build-resolver, database-reviewer, python-reviewer.

**Proactive orchestration rules:** Complex feature requests trigger the planner; code just written triggers the code-reviewer; bug fixes trigger the tdd-guide; architectural decisions trigger the architect; security-sensitive code triggers the security-reviewer. No user prompt needed.

**Skeleton project evaluation:** Search for battle-tested templates, evaluate with parallel agents (security, extensibility, relevance), clone best match, iterate within proven structure.

**Multi-editor support:** Configurations for `.claude/`, `.cursor/`, `.opencode/`, `.codex/`, `.agents/` -- the same agents and skills work across editor environments.

**Key commands:** `/tdd` (test-driven development), `/plan` (implementation planning), `/e2e` (end-to-end tests), `/code-review`, `/build-fix`, `/learn` (extract patterns from sessions), `/skill-create` (generate skills from git history).

**Context management rule:** Avoid the last 20% of context window for large refactoring and multi-file features. Lower-sensitivity tasks tolerate higher utilization.

*Source: everything-claude-code/CLAUDE.md, everything-claude-code/AGENTS.md*

### Model-Tiered Code Review Pipeline: 5 Parallel Agents with Confidence Scoring

Multi-agent code review architecture from the official `code-review` plugin demonstrating model-tiered orchestration and confidence-based filtering:

- **Pipeline structure:** Haiku eligibility check -> Haiku CLAUDE.md discovery -> Haiku PR summary -> 5 parallel Sonnet agents -> per-issue Haiku scoring -> filtering at 80+ -> PR comment posting
- **5 parallel review agents (Sonnet-tier):**
  1. CLAUDE.md compliance checker (run 2x for redundancy on high-stakes checks)
  2. Bug/issue scanner
  3. Git blame context analyzer (understands file history)
  4. Previous PR comments reviewer (catches recurring issues)
  5. Code comment compliance checker
- **Confidence scoring:** Each issue gets an independent Haiku scoring agent (not batch scoring) on a 0-100 scale; only issues scoring 80+ surface to the PR
- **False-positive taxonomy:** Pre-existing issues, linter-catchable problems, and lint-ignore silenced items are explicitly filtered out
- **Model tiering principle:** Haiku for cheap triage/eligibility/scoring operations; Sonnet for deep analysis requiring reasoning; Opus reserved for complex synthesis (not used here)
- **Agent redundancy:** Running 2x compliance agents on the same task catches inconsistencies -- if both flag the same issue, confidence is higher
- **Double eligibility check:** Before AND after review to handle race conditions (PR updated while review runs)
- Cost-conscious design: Haiku agents outnumber Sonnet agents 3:1 in the pipeline, keeping total cost low while concentrating expensive reasoning on the analysis phase

(see [Subagents in Claude Code](#subagents-in-claude-code) for implementation mechanics; see [workflow-patterns.md](workflow-patterns.md#multi-agent-parallel-discovery-with-human-checkpoints) for the related 7-phase pattern)

*Sources: claude-plugins-official/plugins/code-review/README.md, claude-plugins-official/plugins/code-review/commands/code-review.md*

### Issue-Grounded Ideation: Issue Intelligence Agent

- Issue trackers contain strategic signal (25 duplicate bugs = collaboration reliability problem, not 25 separate issues); naive enumeration misses this
- Issue intelligence agent clusters/deduplicates open + recently-closed issues into theme-level analysis -- not individual bug lists
- Hybrid frame strategy: derive ideation frames from issue clusters, pad with default frames when fewer than 4 clusters, to preserve both grounding and diversity
- Output operates at theme level: what the pattern is, why it matters (frequency/severity/trend), what it signals about the system
- Reads titles/labels for all issues (cheap), then reads full bodies for 2-3 representative issues per cluster -- balances cost and signal quality
*Source: compound-engineering-plugin/docs/brainstorms/2026-03-16-issue-grounded-ideation-requirements.md*

### Duplicate Issue Detection via Parallel Agents

- Check if issue is already closed or tagged before deploying search agents
- Deploy 5 parallel agents with diverse keyword searches; a synthesis agent filters false positives; comment is posted only if duplicates remain
- Tool restriction: `allowed-tools` frontmatter limits the command to specific tools only -- prevents scope creep in narrow automation tasks
- Auto-close with opt-out: comment includes time-limited auto-close warning with reaction-based opt-out
- Pattern: use `allowed-tools` frontmatter to scope automated commands to the minimum necessary tool set
*Source: claude-task-master/.claude/commands/dedupe.md*

### Rowboat: Open-Source Multi-Agent Orchestration with Memory
- Open-source multi-agent platform (TypeScript) that provides orchestration, persistent memory, and support for multiple agent runtimes including Claude Code and Claude Cowork
- Positions itself as an "AI coworker" -- emphasis on memory continuity and multi-agent coordination rather than single-shot task execution
- Relevant as a comparison point for custom multi-agent architectures: pre-built orchestration vs rolling your own coordinator pattern
- GitHub: rowboatlabs/rowboat

*Source: GitHub Stars*

### Five-Agent Fleet + Single Brain Pattern (Dorsey World Model)
- Production case study (@ericosiu, Single Grain): five named agents each owning a function -- Alfred (chief of staff/orchestrator), Oracle (SEO/analytics), Arrow (sales pipeline), Cyborg (recruiting), Flash (content). Each has its own workspace, memory files, feedback loops; lanes clearly defined to prevent overlap.
- **World Agent above the fleet:** organizational brain that sees everything and coordinates across agents. Sales agent queries the same brain Oracle uses to track deliverables -- no human routing required.
- **Single Brain (vector DB layer):** ingests Slack, CRM, Gong call transcripts, Granola notes, Google Analytics, Search Console, deliverables, financials every 15 minutes. 6,862+ Gong transcripts indexed. Sales agent evaluating a lead sees marketing performance, past client results in vertical, current team capacity -- not just firmographic data.
- Maps Jack Dorsey's "From Hierarchy to Intelligence" framework (Capabilities, World Model, Intelligence Layer, Surfaces) to actual implementation. Six months of continuous ingestion creates a moat that competitors can't fast-forward -- the data is proprietary, not the technology.
- **Cross-agent compounding (no human in the loop):** Oracle finds keyword gap Tuesday → Flash drafts article Wednesday → Arrow uses article performance as proof point in outbound emails. Coordination happens via the shared brain, not via human routing.
- **AutoGrowth A/B layer:** Arrow tests subject lines, angles, send times. After 4 weeks, question-form subject lines outperformed statements by 2.3x; insight applied to next campaign automatically.
- **Self-healing cron doctor:** runs twice daily, reads error logs, diagnoses failures, fixes what it can. Goal: never discover failures by noticing missing output (see [autonomous-agents.md](autonomous-agents.md#five-agent-fleet--single-brain-marketing-os) for the full operating system view).
- Six design principles that keep it stable: LLMs handle judgment + scripts handle determinism; never instruct twice (second occurrence becomes a skill/cron); security gates on every external script (in/out); self-healing over monitoring; flat files over databases; the system compounds (months 1-2 are pain, month 3 the flywheel kicks in).

*Source: 2026-04-11-ericosiu-httpstcop3alvdc9dc.md*

### 4-Agent Content Production Team: Research/Production/Quality/Distribution
- **Minimum viable team structure** for full knowledge-work cycle: intake/research, production, quality control, output/distribution. One agent per phase. Each agent has one job and never crosses into another's lane.
- **Concrete agent contracts** (each as its own .md skill file):
  - Research Agent: produces structured research briefs (CORE INSIGHT, TARGET AUDIENCE, SUPPORTING EVIDENCE, COUNTERINTUITIVE ANGLE, KEY DATA, CONTENT ANGLES, GAPS). Cross-reference at least 3 independent sources for factual claims.
  - Production Agent: produces first drafts from briefs. Voice profile extracted from your 10 best-performing pieces (sentence length, capitalization, structural patterns, vocabulary, transitions, CTA style) plugged into skill prompt.
  - Quality Agent: scores on 5 criteria (VOICE MATCH, HOOK STRENGTH, INFORMATION DENSITY, CTA CLARITY, FORMAT COMPLIANCE), 1-10 each. Passing threshold: 8+ on ALL five. Returns specific revision briefs, never vague feedback.
  - Distribution Agent: platform-specific formatting (X 280-char per tweet, LinkedIn longer sentences, newsletter HTML-compatible) before deploying.
- **Orchestrator is routing logic, not a 5th agent.** Receives task, monitors output folders for completion, passes correct output to next agent, handles revisions by routing back. Never skips the Quality Agent gate.
- **Shared folder convention:** `inbox/`, `research-briefs/`, `drafts/`, `approved-content/`, `distribution/`, `logs/`. Every output file `YYYY-MM-DD-[type]-[topic].md`. Every agent must log to `logs/operations.md`.
- **Hard rules in CLAUDE.md:** never delete files (archive to timestamped backup). Never publish without Quality Agent approval header. Log every action before taking it, not after. When uncertain: stop, flag for human review.
- **Parallelism math:** one agent running four phases sequentially takes 4x as long as four agents running phases simultaneously. For 20 pieces/week content op, the parallelism alone justifies the architecture.

*Source: 2026-05-12-cyrilXBT-httpstco3k0d4oz1uf.md*

### PAI (Personal AI Infrastructure): Life OS on Claude Code
- **Daniel Miessler's open-source Life OS** (github.com/danielmiessler/Personal_AI_Infrastructure, 12,100 stars, 45 skills, 171 workflows, 37 hooks). Three layers: PAI as OS (memory/skills/workflows), Pulse (local dashboard at localhost:31337), DA (Digital Assistant with name, voice, persistent memory).
- **Plain text beats databases principle:** every memory, decision, context file lives in Markdown. Read with `cat`, search with ripgrep, version with Git. No embeddings, no vector databases, no opaque magic.
- **Algorithm v6.3.0** (7-step doctrine for every complex task) classifies every request into 3 modes: MINIMAL (simple acknowledgments), NATIVE (straightforward tasks), ALGORITHM (complex multi-step work). Hooks route to right processing level — no wasted compute.
- **Privacy as code, not as a guideline:** ContainmentGuard hook runs on every write and *physically blocks* sensitive data from being written outside designated containment zones. Personal identity, credentials, contacts, health, financial info constrained by code, not by "please don't" prompts.
- **Honest "Linux moment" framing:** powerful, raw, CLI-heavy, Windows install painful, UX still developer-first. Linked Medium piece "I Over-Engineered My AI System. Then I Deleted Most of It" surfaced as real failure mode of over-eager adoption.
- (see [memory-persistence.md > Karpathy Wiki Method](memory-persistence.md) for the markdown-first knowledge graph this evolved from; see [Harness Engineering](#agent-harness-engineering-every-mistake-becomes-a-rule) for the hook-enforcement pattern PAI operationalizes)

*Source: 2026-05-11-noisyb0y1-httpstcolh8u6f7jjr.md*

---

## Tool Design as Agent Elicitation

- Tools should be shaped to the model's abilities, not the task taxonomy ("paper vs calculator vs computer" analogy)
- AskUserQuestion needed three iterations: "Even the best designed tool doesn't work if Claude doesn't understand how to call it"
- As models improve, scaffolding tools become constraining: TodoWrite replaced by Tasks because newer models no longer needed reminders
- Progressive disclosure expands capability without adding tools: skills reference files that reference other files recursively
- Claude Code limits itself to ~20 tools; Guide subagent provides docs without adding a tool to the action space

*Source: Lessons from Building Claude Code Seeing like an Agent.md*

### Self-Evolving Agent Pattern

- After completing its primary task, the agent adds a mandatory "Self-Evolution" step that updates its own knowledge artifacts to stay in sync with reality
- **Skill sync:** If the agent modifies a system it has documented (e.g., a presentation), it re-reads the actual current state and updates its skill files (weight tables, section ranges, structural descriptions) to match
- **Cross-doc consistency:** When canonical claims change (e.g., hook event count, settings precedence), the agent syncs all files that reference those claims in the same execution -- prevents knowledge drift across documentation
- **Learnings section:** The agent appends edge cases and discovered patterns to a "Learnings" section in its own definition file, creating an append-only institutional memory that future invocations inherit
- **Integrity verification:** Post-change checks enforce structural invariants (sequential numbering, weight sums, no duplicates) -- the agent validates its own output before completing
- Best for: agents that manage evolving artifacts (documentation, presentations, configuration) where the agent's knowledge must stay synchronized with the artifact's actual state
- Bad fit: stateless utility agents or one-shot tasks where there's nothing to drift from

(see [skills.md](skills.md#writing-good-skills) for related skill organization patterns)

*Source: claude-code-best-practice/.claude/agents/presentation-curator.md*

### The Harness Is Everything: ACI Design and Context Window Architecture

- Agent-Computer Interface (ACI) design produces larger gains than model upgrades: same GPT-4, same task, purpose-built ACI improved SWE-bench from 3.97% to 12.47% -- entirely from interface design
- The context window is not RAM; it is the agent's entire working consciousness -- every irrelevant token degrades reasoning quality; flooding with grep results is noise, not information
- ACI design principles from SWE-agent: capped search results (>50 matches = tell agent to narrow), stateful file viewer with explicit line numbers at 100-line windows, editor with integrated linter rejecting syntax errors before they apply
- Two-agent architecture for long-running projects: Initializer agent (sets up environment, creates feature list in JSON with pass/fail fields); Coding agent (one feature at a time, updates progress file and git history)
- Feature list as cognitive anchor: store in JSON not Markdown -- models are less likely to inappropriately overwrite JSON files; each feature has explicit pass/fail status
- Two failure modes: (1) attempting too much without testing/documenting, (2) looking at partial progress and declaring victory -- both solved by initializer + feature list architecture

(see [context-engineering.md](context-engineering.md) for context window management patterns)

*Source: Twitter-Bookmarks/2026-03-17-rohit4verse-httpstcoh4kcn5wwnx.md*

### Harness Engineering: 8 Principles for AI Coding Agent Performance

- "The interface is not decoration. For an LLM agent, the interface is the mind" -- how you structure context and tool access defines capability
- Capping search results forces query refinement rather than flooding context -- turns a failure mode into a feedback loop
- Run linters at edit time, not test time: a syntax error caught during writing costs nothing; caught 10 steps later burns the entire context budget
- A persistent progress file is the cheapest fix in agentic systems: read at start, write at end, enables continuity across context window boundaries
- Completion criteria must be explicit and binary; if the agent has to guess whether a feature is done, it will often guess wrong
- One agent, one git worktree: isolation enables parallel agents without them stepping on each other

*Source: Twitter-Bookmarks/2026-03-25-rohit4verse-the-best-ai-teams-are-not-winning-on-models-they-are-winning.md*

### Harness Engineering: The System Around the Model Matters More Than the Model

- Empirical evidence: same model scored 42% → 78% on a coding benchmark by changing only the harness -- a 2x performance gain that no model upgrade has matched
- The five harness levers: (1) CLAUDE.md/AGENTS.md (under 60 lines, human-written); (2) Skills (progressive disclosure); (3) MCP servers (beware tool thrash); (4) Sub-agents (context firewalls, not role-specific agents); (5) Hooks (deterministic checkpoints)
- ETH Zurich study: AI-generated CLAUDE.md files hurt performance and cost 20% more tokens; human-written, concise, specific files help
- Sub-agents as context firewalls: when a task would flood the main context with noise, delegate to a sub-agent that returns only the result
- LangChain's PreCompletionChecklistMiddleware -- a hook that intercepts before task completion and forces verification against original requirements -- was one of their biggest single performance gains
- Failure reflex shift: old = fix the mistake manually; new = ask "how do I make sure it never makes this mistake again?" and encode the fix into the harness
- "Harness engineering is the skill of 2026. Prompt engineering was 2023, context engineering was 2025."

*Source: Twitter-Bookmarks/2026-03-26-heynavtoor-httpstcofbuctcqf2a.md*

### Meta-Harness: Automated Harness Optimization via Agent Search

- **Key framing:** everything in your AI system that is not the LLM itself is a harness; harness components: pre/post hooks, prompt building, tools, memory, external data sources; "the harness is the Operating System for the LLM" (Stanford paper)
- **Core insight:** harnesses have become too complex for humans to optimize by hand; treat harness development as a code optimization problem, not a prompt optimization problem; if you change the code, the harness changes; code changes are testable and plottable on a Pareto frontier (accuracy vs token cost)
- **Meta-Harness loop:** agentic proposer (Claude Code) reads from filesystem (prior results + execution traces) → diagnoses failure modes → writes new version of harness code → runs evaluation → records results + traces → loop continues; rich execution traces required -- a single accuracy score is insufficient; the optimizer needs to see exactly where a bash command failed or why memory retrieval fetched a useless chunk
- **Filesystem-as-feedback:** full history of every experiment (source code, performance scores, execution traces); unrestricted access to all previous history is essential because dependencies are long-horizon; systems that only see summaries/rewards discard critical information
- **Practical tips from authors:** write a good skill first (primary steering interface for proposer); start with a baseline that struggles; log everything in navigable JSON with hierarchical structure; build a small CLI over logs (list Pareto frontier, show top-k, diff code between runs); warm-start with offline experience if available; automate evaluation outside the proposer (too simple to delegate)
- **Discovery from Terminal Bench:** initial harness spent exploratory turns discovering environment; Meta-Harness changed initial prompt to include environment snapshot (working directory, file listing, languages, package managers, memory) -- eliminated 2-4 exploratory turns per task; this optimization was only possible via access to execution logs

*Source: Twitter-Bookmarks/2026-04-02-neural_avb-httpstcopli8ea1fqy.md*

### Software Must Become API-First for Agent Consumers
- Agents evolving beyond chatbots into persistent systems with sandboxed compute, file systems, long-term memory, and native API/CLI interaction -- "if a feature doesn't have an API, it doesn't exist for agents"
- Agents will need their own identities (email addresses, accounts), budgets/wallets, and security governance -- distinct from the human users who deploy them
- Business models must evolve from seat-based to consumption/volume-based pricing as agents become the primary software consumers
- Key infrastructure needs: sandboxed compute (E2B, Modal), identity/auth systems for non-human actors, web search rebuilt for agents (not humans), and payment systems for autonomous spending
- (see [autonomous-agents.md](autonomous-agents.md#agent-financial-infrastructure-lightning-network-commerce-stack) for agent payment infrastructure; see [autonomous-agents.md](autonomous-agents.md#the-winning-architecture-6-requirements-for-secure-recursive-agents) for agent security requirements)

*Source: 2026-03-08-levie-httpstcoo7oiuykjbh.md*

### Agent Harness Four Pillars -- Terminal Bench 2.0 Evidence
- LangChain jumped from 52.8% to 66.5% on Terminal Bench 2.0 by changing only the harness, not the model -- a different benchmark than the 42% to 78% gain documented in the existing Harness Engineering entries, reinforcing the pattern from independent data
- Four pillars: (1) Context Architecture with 40% window budget per layer, (2) Agent Specialization with scoped tools per agent, (3) Persistent Memory as append-only files across sessions, (4) Structured research/plan/execute/verify workflow
- Guardrail hierarchy: hard limits (never violated) > safety nets (catch and recover) > golden paths (preferred approach) > audit (log for review) -- a concrete prioritization framework for agent constraints
- Production checklist specifics: root instructions under 200 lines, separate agents for code/test/review, max file budget per session, cost ceiling per session to prevent runaway spending
- (see [Harness Engineering: The System Around the Model Matters More Than the Model](#harness-engineering-the-system-around-the-model-matters-more-than-the-model) for the broader harness pattern; see [Meta-Harness: Automated Harness Optimization via Agent Search](#meta-harness-automated-harness-optimization-via-agent-search) for automated harness tuning)

*Source: 2026-03-10-nyk_builderz-httpstcou0fi0i8t4i.md*

