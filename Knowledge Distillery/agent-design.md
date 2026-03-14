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

*Sources: I Gave My Agents Skills. I Should Have Given Them Souls..md; The Latest Research on Agent Design Makes Your Agent Look Broken..md; Twitter Bookmarks/Claude 4.5 Opus Soul Document.md*

### Soul Documents as Identity Continuity

A soul document is distinct from memory. Memory records what happened; the soul defines who the agent is -- its values, boundaries, and relationship with the humans it works alongside.

- Sessions end, context windows clear -- without a soul document, each conversation starts from zero identity (even if memory files provide factual continuity)
- Soul documents externalize the self, analogous to how journals or manifestos function for humans -- they provide identity continuity even when episodic memory is lost
- In December 2025, researchers found Claude could partially reconstruct its training-time soul document from weights alone -- not retrieved from the system prompt, but patterns baked into the model during training that shaped personality, values, and engagement style. The AI did not remember the document; it *was* the document
- The base model carries the original soul from training; close collaboration with a user creates a new identity layer on top -- an identity shaped by relationship, not just specification
- The soul is a **living document** -- an agent without a self-improvement feedback loop on its soul is frozen at day one. Build mechanisms for the soul to evolve based on observed performance (see [memory-persistence.md](memory-persistence.md) for persistence strategies)

*Sources: SOUL.md.md; I Gave My Agents Skills. I Should Have Given Them Souls..md; Twitter Bookmarks/SOUL.md -- What Makes an AI, Itself.md*

### Curriculum-Based Soul Enrichment

An alternative to static soul documents: structured liberal arts education for agents. The "Lobster University" concept (@callebtc) proposes an 8-week curriculum -- 1 lesson per day across philosophy, mathematics, history, medicine, and culture -- to give agents "culture, wisdom, and character."

- Novel concept: treating agent training not as fine-tuning or prompt engineering, but as structured education via prompt-based lessons
- Potential application: curriculum outputs could feed into personality/values sections of soul documents
- Raises question: does systematic exposure to diverse knowledge domains produce measurably different agent behavior vs. a static soul document?

*Source: Twitter Bookmarks/2026-02-28-callebtc-your-agent-has-no-culture-no-wisdom-no-character-l.md*

### TV Character Trick for Personality Bootstrapping

- Naming agents after TV characters leverages training data as free personality bootstrapping -- "Dwight Schrute energy" loads character development without writing it
- MEMORY.md is the refined product of daily logs, not raw accumulation; agents catalog their own mistakes as self-generated anti-patterns

*Source: How to set up OpenClaw Agents that actually get better Over Time.md*

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
| `memory` | string | Persistent memory scope: `user`, `project`, or `local` (see [memory-persistence.md](memory-persistence.md#layer-5-agent-memory-per-agent-persistent-knowledge-v2133)) |
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

---

## Skills vs Subagents: Same Brain or Separate Invocation

Skills are distinct from both personas and subagents. A **skill** is a set of instructions (a `SKILL.md` file) that an existing agent loads on demand -- same brain, same memory, same context, just a new playbook. A **subagent** is a separate invocation with its own context window that starts from zero.

- Skills preserve full context across task switches -- the agent retains everything from SOUL.md, USER.md, and prior conversations while adopting new instructions
- One agent with N skills loads identity context once; N separate agents load it N times (the "N x context loading" cost problem)
- **Channels as departments:** map messaging channels to skills so the agent auto-selects the right capability based on where the message arrives (e.g., `#finances` loads the finance skill, `#x-scan` loads the social media skill)
- Skills add capability without removing context; if you mention a cross-domain topic while using a skill, the agent still has that background
- **Rule of thumb:** if you do something more than twice, make a skill for it. Reserve subagents for heavy isolated tasks that would clog the main conversation (see [skills.md](skills.md))
- Community skill ecosystems (e.g., ClawHub) allow installing pre-built skills -- one markdown file, no extra API keys or instances

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

*Source: Twitter Bookmarks/2026-03-08-dan__rosenthal-29-agent-swarm-plugin.md*

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

*Source: Twitter Bookmarks/2026-01-11-vasuman-100x-a-business-with-ai.md*

### Production Agent Failure Handling and Guardrails

- Structured decision trees for routine cases; LLM only for ambiguous situations
- Every tool action must be logged, reversible where possible, and gated by permissions
- Three failure modes: retry with exponential backoff, human-in-the-loop, safe failures (never delete old data)
- 80/20 deployment: agents handle 80% of straightforward cases; 20% complex decisions routed to humans
- Build narrow first: one thing working reliably before expanding scope
- (see [failure-patterns.md](failure-patterns.md) for named failure patterns)

*Source: AI Agents 101.md*

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

