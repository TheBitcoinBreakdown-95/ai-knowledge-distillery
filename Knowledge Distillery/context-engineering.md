# Context Engineering

## Why Context Matters More Than Prompts

A perfect prompt in the wrong context fails. Context is the information environment surrounding the prompt -- the files loaded, the conversation history, the architectural knowledge, the memory from past sessions. Prompt engineering optimizes *what you say*; context engineering optimizes *what the AI already knows when you say it*.

Context problems compound silently. As a codebase grows, module relationships, domain patterns, and team conventions do not surface on their own. Without deliberate context management, you re-explain the same architectural decisions at the start of every session, the AI drifts from your conventions, and accumulated noise drowns out signal (see [failure-patterns.md#4-context-pollution](failure-patterns.md#4-context-pollution)).

Core philosophy: "Prompting is temporary. Structure is permanent." The CLAUDE.md file, the documentation spine, and the context management habits below are structural investments that compound across every session.

---

## CLAUDE.md: Your Always-Loaded Memory

CLAUDE.md is injected into the system prompt at the start of every conversation. It is the single most important context mechanism -- always present, zero manual effort per session.

### Three Scopes

| Scope | Location | Visibility | Use Case |
|-------|----------|------------|----------|
| Project | `CLAUDE.md` at repo root | Shared, committed to git | Team conventions, build commands, architecture |
| Local | `CLAUDE.local.md` or `.claude/CLAUDE.md` | Personal, gitignored | Personal preferences, local env notes |
| Global | `~/.claude/CLAUDE.md` | All projects on machine | Universal coding style, global workflows |

In monorepos, CLAUDE.md files in parent and child directories also load -- parent directories eagerly, child directories on demand when Claude works in that subdirectory.

### CLAUDE.md Loading in Monorepos: Ancestor vs Descendant

Two distinct mechanisms control which CLAUDE.md files load:

- **Ancestor loading (UP the tree):** On startup, Claude walks upward from cwd toward the filesystem root and loads every CLAUDE.md it finds. Always immediate.
- **Descendant loading (DOWN the tree, lazy):** Subdirectory CLAUDE.md files load only when Claude reads/edits files in that subdirectory during the session. Not at launch.
- **Sibling isolation:** Working in `frontend/` never loads `backend/CLAUDE.md` or `api/CLAUDE.md`.

**Best practices for monorepos:**
- Root CLAUDE.md: shared conventions, coding standards, commit formats
- Component CLAUDE.md: framework-specific patterns, local testing conventions
- `CLAUDE.local.md`: personal preferences, `.gitignore`'d

This design prevents irrelevant context from bloating sessions while ensuring shared instructions propagate down.

### CLAUDE.md Imports and Cross-Directory Loading

- `@path/to/import` syntax expands and loads referenced files at launch; relative and absolute paths; recursive up to 5 hops
- `CLAUDE.local.md` auto-loaded and auto-added to `.gitignore` for private preferences
- `--add-dir` gives access to additional directories; `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` env var loads their CLAUDE.md files too
- `claudeMdExcludes` setting skips specific CLAUDE.md files in large monorepos (managed policy CLAUDE.md cannot be excluded)
- Official guidance now recommends under 500 lines per CLAUDE.md (up from community heuristic of ~100-200); longer files reduce adherence

*Sources: How Claude remembers your project.md, Best Practices for Claude Code.md*

### Rules Folder: Modular Alternative to CLAUDE.md

An alternative to a single CLAUDE.md file: a `~/.claude/rules/` directory with modular `.md` files grouped by concern:

```
~/.claude/rules/
  security.md       # No hardcoded secrets, validate inputs
  coding-style.md   # Immutability, file organization
  testing.md        # TDD workflow, 80% coverage
  git-workflow.md   # Commit format, PR process
  agents.md         # When to delegate to subagents
  performance.md    # Model selection, context management
```

**When to use which:**
- Single CLAUDE.md: simpler projects, team sharing via git, when all rules fit under ~150 lines
- Rules folder: large projects with many concerns, when different rules apply to different workflows, personal global config across all projects

Both approaches can coexist (project CLAUDE.md + personal rules folder).

### Rules Directory: Path-Specific Scoping

- `.claude/rules/` files support YAML frontmatter with a `paths` field for conditional loading (e.g., `paths: ["*.tsx", "*.jsx"]`)
- Rules without `paths` frontmatter load unconditionally (same priority as `.claude/CLAUDE.md`)
- Path-scoped rules trigger on file read, not on every tool use -- reducing noise and saving context
- Supports symlinks for sharing rules across projects; circular symlinks handled gracefully
- User-level rules (`~/.claude/rules/`) load before project rules, giving project rules higher priority

*Sources: How Claude remembers your project.md, Best Practices for Claude Code.md*

### What to Include (and What NOT to Include)

**The Four-Pillar Framework:** A CLAUDE.md is repo memory, not a prompt dump. Structure it around four things Claude needs:

1. **The Why** -- project purpose, domain constraints, key goals
2. **The Map** -- where things live (directories, key files, architecture)
3. **The Rules** -- what's allowed and what's not (coding standards, gotchas, warnings)
4. **The Workflows** -- how work gets done (build, test, lint, deploy commands)

**Include:**
- Build, lint, test commands (the ones you actually use)
- High-level architecture and key directories
- Coding standards and conventions
- Repository etiquette (branch naming, merge vs rebase)
- Project-specific warnings and gotchas
- References to critical files (e.g., database schema path)
- MCP server usage rules and constraints

**Do NOT include:**
- API keys, credentials, or connection strings
- Exhaustive documentation (break into separate files and reference them)
- Generic advice that does not match your actual workflow
- Anything you would not want shared publicly

**Keep it concise.** CLAUDE.md consumes tokens on every request. Every line should prevent a specific mistake. If it grows past ~100 lines, break information into separate docs and link from CLAUDE.md (see [project-setup.md#full-operating-manual-18-sections](project-setup.md#full-operating-manual-18-sections) for the layered documentation spine approach).

**Local CLAUDE.md files near risky modules:** Place small, targeted files near areas with known gotchas (`src/auth/CLAUDE.md`, `src/persistence/CLAUDE.md`, `infra/CLAUDE.md`) so Claude sees warnings exactly when working in those directories.

**Progressive context via docs/:** Architecture overviews, ADRs, and operational runbooks belong in `docs/` -- Claude knows where truth lives without bloating CLAUDE.md.

*Source: Twitter Bookmarks/2026-03-06-BharukaShraddha-most-people-treat-claude-md.md*

### WHAT / WHY / HOW Framing

An alternative organizational framework for CLAUDE.md content:

- **WHAT:** Tech stack, repo layout, version info -- what the project is made of
- **WHY:** Project purpose, domain constraints, key goals -- why it exists and what matters
- **HOW:** Build/test commands, CI/CD process, style rules (reference configs, do not duplicate them) -- how development works
- Each section recommended under ~40 lines; focus on must-know info only

This framing overlaps with but is more explicit than the "What to Include" guidance above. The Four-Pillar and WHAT/WHY/HOW frameworks are complementary -- use whichever structure makes your CLAUDE.md most scannable.

*Source: deep-research-report.md*

### CLAUDE.md Quality Rubric: 6-Criterion Scoring System

- 6 weighted criteria for CLAUDE.md quality: Commands/workflows, Architecture clarity, Non-obvious patterns, Conciseness, Currency, Actionability -- totaling 100 points
- Letter grade scale: A (90-100) through F (0-29) for quantified CLAUDE.md assessment
- 5-phase improvement workflow: Discovery (find all CLAUDE.md files) -> Quality Assessment -> Report -> Targeted Updates -> Apply
- Update guideline: propose targeted additions only -- avoid restating obvious code, generic best practices, one-off fixes, verbose explanations
- 6 common issues to flag: stale commands, missing dependencies, outdated architecture, missing env setup, broken test commands, undocumented gotchas
- Recommended sections: Commands, Architecture, Key Files, Code Style, Environment, Testing, Gotchas, Workflow

(see [What to Include (and What NOT to Include)](context-engineering.md#what-to-include-and-what-not-to-include))

*Source: claude-plugins-official/plugins/claude-md-management/skills/claude-md-improver/SKILL.md*

### /init: Bootstrap from Codebase Analysis

Run `/init` in any Claude Code session to auto-generate a starter CLAUDE.md. Claude examines package files, config, existing docs, and code structure, then produces build commands, key directories, and detected conventions. Treat the output as a starting point -- review for accuracy, add what Claude could not infer (deployment processes, branch naming), remove generic filler.

Running `/init` on a project that already has a CLAUDE.md suggests improvements based on fresh codebase analysis.

### The # Shortcut for Quick Memory Additions

Press `#` followed by a note to instantly write to CLAUDE.md without leaving the conversation:

```
# Always use 2-space indentation for JavaScript
# Run integration tests before merging to main
```

Use this when you catch yourself repeating an instruction. The note persists across all future sessions.

### Dynamic System Prompt Injection via CLI Aliases

An alternative to putting everything in CLAUDE.md: use shell aliases to inject context surgically at session start.

- **Mechanism:** `claude --system-prompt "$(cat memory.md)"` injects file content as system prompt at session start
- **Authority hierarchy:** System prompt > user messages > tool results. Content injected this way has higher authority than anything typed during the session
- **Mode-specific aliases:** Create named profiles for different work modes:
  - `alias claude-dev='claude --system-prompt "$(cat ~/.claude/contexts/dev.md)"'`
  - `alias claude-review='claude --system-prompt "$(cat ~/.claude/contexts/review.md)"'`
  - `alias claude-research='claude --system-prompt "$(cat ~/.claude/contexts/research.md)"'`
- **Why this complements CLAUDE.md:** CLAUDE.md loads every session regardless of task type. CLI injection loads context specific to the current workflow, keeping each session leaner
- **Session-end learning capture:** Use Stop hooks (not UserPromptSubmit) for learning capture -- Stop runs once at session end, while UserPromptSubmit adds latency to every prompt

*Source: everything-claude-code/the-longform-guide.md*

---

## Auto Memory: Claude's Self-Managed Memory Scratchpad

Built-in feature (on by default) where Claude writes notes for itself across sessions -- build commands, debugging insights, architecture notes, code style, workflow habits.

- **Storage:** `~/.claude/projects/<project>/memory/MEMORY.md` + topic files; first 200 lines injected at session start
- **Distinction:** CLAUDE.md = your instructions to Claude; MEMORY.md = Claude's own scratchpad updated autonomously
- **Shared scope:** All worktrees and subdirectories within the same git repo share one auto memory directory; machine-local (not synced)
- **Toggle:** `/memory` command, `autoMemoryEnabled` setting, or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` env var
- **Compaction behavior:** CLAUDE.md fully survives compaction (re-read from disk); if instructions disappeared after `/compact`, they were only in conversation

(see [memory-persistence.md](memory-persistence.md) for the full memory layer model)

*Sources: How Claude remembers your project.md, Thread by @trq212.md*

---

## Structuring Context for AI Consumption

### Give the AI a Map (Directory Trees, Architecture Diagrams)

A simple directory tree eliminates entire classes of "where does this live?" questions:

```
src/
  api/        # Route handlers
  models/     # Database models
  core/       # Config and utilities
  components/ # React components
```

Include major dependencies, architectural patterns (DDD, microservices, monorepo), and any non-standard organizational choices. Claude uses this map to decide where to find code and where to make changes.

### Documentation Spine (Ordered List of What to Read First)

Define a canonical navigation order so Claude reads summaries before source code:

1. `CLAUDE.md` -- behavioral rules and orientation
2. `docs/ARCHITECTURE.md` -- system design and constraints
3. `docs/DECISIONS.md` -- tradeoffs and things not to change casually
4. `docs/WORKFLOWS.md` -- how work gets done
5. `docs/COMPONENTS/` -- per-subsystem docs
6. Raw source code -- only when summaries are insufficient

When behavior changes, update the documentation. Treat docs as maintained artifacts, not one-time writeups.

### Progressive Disclosure (Summary First, Details on Demand)

Front-load short summaries. Let Claude drill into source files only when the summary is not enough. This principle applies everywhere -- CLAUDE.md should reference rather than inline, worklogs should be 50-100 lines not 787, and memory plugins should return compact indexes before full observation details.

---

## Context Window Management

### /compact: Compress Without Losing Knowledge

`/compact` summarizes older messages while preserving what Claude has learned about the current task. Use it proactively during long sessions. Optionally focus: `/compact focus on authentication errors` keeps auth-related context while compressing everything else.

**Strategic compaction decision guide:** Manual `/compact` is preferable to relying on auto-compaction, which triggers at arbitrary points and often mid-task. Use the phase transition table to decide:

| Transition | Compact? | Why |
|---|---|---|
| Research -> Planning | Yes | Research context is bulky; plan is the distilled output |
| Planning -> Implementation | Yes | Plan is in TodoWrite or a file; free up context for code |
| Implementation -> Testing | Maybe | Keep if tests reference recent code; compact if switching focus |
| Debugging -> Next feature | Yes | Debug traces pollute context for unrelated work |
| Mid-implementation | No | Losing variable names, file paths, and partial state is costly |
| After a failed approach | Yes | Clear the dead-end reasoning before trying a new approach |

**What survives compaction:** CLAUDE.md instructions, TodoWrite task list, Memory files (`~/.claude/memory/`), Git state (commits, branches), files on disk.

**What is lost:** Intermediate reasoning, file contents previously read, multi-step conversation context, tool call history, verbally stated preferences.

**Best practices:** Write important context to files before compacting. Use `/compact` with a summary message for targeted retention: `/compact Focus on implementing auth middleware next`. A PreToolUse hook on Edit/Write can track tool call count and suggest compaction at configurable thresholds (default: 50 calls, reminder every 25 after).

*Source: everything-claude-code/skills/strategic-compact/SKILL.md*

### /clear: Hard Reset Between Tasks

`/clear` wipes conversation history completely. CLAUDE.md survives (it reloads from disk). Use `/clear` when switching from debugging authentication to implementing a new API endpoint -- the auth details would only pollute the new task (see [failure-patterns.md#4-context-pollution](failure-patterns.md#4-context-pollution)).

### /context: Monitor Token Usage

`/context` shows how much of the context window is consumed. Check it periodically. When usage is high, decide between `/compact` (preserve knowledge) and `/clear` (fresh start).

### Escape and Double-Escape

- **Single Escape** -- stops Claude mid-response. Use when the output is heading in the wrong direction. Pair with `#` to add a memory note preventing recurrence.
- **Double Escape** -- rewinds the conversation to an earlier message. Lets you jump back past irrelevant debugging tangents while keeping the useful context from before.

When Claude makes a repetitive mistake across conversations, the most effective fix combines Escape (stop the bad output) with `#` (add a memory note preventing recurrence). The correction persists in CLAUDE.md and applies to all future sessions, eliminating an entire class of repeated errors. Double-Escape shows all sent messages and lets you jump back to an earlier point, preserving valuable context (like codebase understanding) while removing distracting debugging tangents.

*Source: Anthropic Course - Claude Code in Action*

### Plan Mode and Think Mode

- **Plan Mode** (Shift+Tab x2, or once if already auto-accepting edits) -- breadth. Claude reads more files, builds a detailed implementation plan before executing. Use for multi-step tasks that touch many parts of the codebase.
- **Think Mode** -- depth. Extended reasoning budget for complex logic or tricky debugging. Use for single hard problems. Thinking modes offer progressive granularity, each giving Claude more tokens for reasoning:
  - "Think" -- basic reasoning
  - "Think more" -- extended reasoning
  - "Think a lot" -- comprehensive reasoning
  - "Think longer" -- extended time reasoning
  - "Ultrathink" -- maximum reasoning capability
- Both consume additional tokens. Combine them for complex tasks that need wide understanding *and* deep reasoning.

**When to use Plan Mode vs. skipping it:** Plan Mode adds overhead -- it is not free. For clear-scope, small tasks (fixing a typo, adding a log line, renaming a variable), ask Claude to do it directly. Use planning when you are uncertain about the approach, the change modifies multiple files, or you are unfamiliar with the code being modified. Quick heuristic: if you could describe the diff in one sentence, skip the plan.

*Sources: Anthropic Course - Claude Code in Action, claude-code-best-practice/reports/best-practices-claude-code.md*

### Extended Thinking: Adaptive Reasoning on Opus 4.6

- Opus 4.6 introduces adaptive reasoning: dynamically allocates thinking based on effort level (low/medium/high) instead of fixed budget
- `MAX_THINKING_TOKENS` is ignored on Opus 4.6 and Sonnet 4.6 (except `=0` which disables entirely)
- Phrases like "think", "think hard", "ultrathink" are interpreted as regular prompt text -- they do NOT allocate thinking tokens
- Toggle visibility: Ctrl+O (verbose mode); toggle on/off: Option+T / Alt+T

*Source: Common workflows.md*

### Session Management: Checkpoints, Rewind, and Named Sessions

- Every Claude action creates a checkpoint; double-tap Escape or `/rewind` opens a menu (restore conversation, code, both, or summarize)
- Checkpoints persist across sessions; only track changes made by Claude, not external processes
- `/rename` gives descriptive names; `/resume` shows metadata (name, time, message count, branch); `--from-pr <number>` resumes PR-linked sessions
- `/compact <instructions>` accepts focus directives (e.g., `/compact Focus on the API changes`); partial compaction via rewind + "Summarize from here"
- Customizable compaction via CLAUDE.md: "When compacting, always preserve the full list of modified files and any test commands"

*Sources: Common workflows.md, Best Practices for Claude Code.md*

### Context Degradation Threshold: Earlier Than Expected

Multiple practitioners report context quality degrading earlier than the commonly cited "around 50%":

- One SWE with 7 years experience (Amazon, Disney, Capital One) reports degradation starting at **20-40%** context usage, not at the 100% mark
- Compaction after degradation does not restore quality: "The model was already degraded before the compaction happened, and compaction doesn't magically restore quality"
- A second practitioner confirms 200K context window with "too many tools enabled" reduces effective context to ~70K

**The copy-paste reset trick:** When context is bloated -- copy everything important from the terminal, run `/compact` for a summary, `/clear` the context entirely, then paste back only what matters. Fresh context with critical information preserved. More effective than letting Claude struggle through degraded context.

**External memory files as buffer:** Use SCRATCHPAD.md or plan.md to persist plans and progress across sessions. These survive `/clear` and let Claude pick up where it left off instead of starting from zero. Place these at the top of any file hierarchy so they apply to all tasks.

**CLAUDE.md quality heuristic:** "Bad CLAUDE.md looks like documentation written for a new hire. Good CLAUDE.md looks like notes you'd leave yourself if you knew you'd have amnesia tomorrow."

### MCP Context Budget Rule of Thumb

Practical guidance on managing MCP server impact on context windows:

- A 200K context window can shrink to ~70K with too many MCPs and plugins enabled simultaneously
- Configure 20-30 MCP servers at the user level, but keep **under 10 enabled per project** and **under 80 tools active** total
- Disable unused MCPs per project using `disabledMcpServers` in `~/.claude.json` under projects.[path]
- Same principle applies to plugins -- keep 4-5 enabled at a time even if more are installed
- "Went overboard with MCPs thinking more = better. Ended up using only 4 daily" -- consistent report across multiple users
- **mgrep plugin** (Mixedbread) provides ~50% token reduction vs ripgrep/grep for code search -- significant context savings on search-heavy workflows
- **Replace MCPs with CLI-backed skills/commands** where possible to free context window and reduce per-call token cost

This aligns with the "went overboard" warning documented in [tools-and-integrations.md](tools-and-integrations.md#curated-daily-use-mcp-recommendations) but adds the specific numeric thresholds.

*Sources: Twitter Bookmarks/The Shorthand Guide to Everything Claude Code 1.md, Twitter Bookmarks/The Longform Guide to Everything Claude Code.md*

---

## The @ Symbol: Targeted File References

Prefix a file or directory path with `@` to pull it directly into context:

```
Analyze this code @./src/auth/login.ts
Review all components @./src/components/
```

This is more precise and cheaper than letting Claude search the codebase. Reference critical files (like a database schema) in your CLAUDE.md so they are always available without manual `@` mentions.

Beyond using `@` in conversation prompts, you can embed `@file` references directly in CLAUDE.md -- the referenced file's contents are automatically included in every request. For example, referencing a database schema file (e.g., `@prisma/schema.prisma`) ensures Claude can answer structural questions immediately without searching for and reading the file each time. Trade-off: every `@` reference in CLAUDE.md adds tokens to every request; only reference files that are genuinely relevant across many tasks.

Screenshots can be pasted into Claude Code with Ctrl+V for visual context -- Claude can see the actual rendered output, not just code, enabling more informed UI/styling decisions.

*Source: Anthropic Course - Claude Code in Action*

---

## Prompt Cache Architecture

Prompt caching works by prefix matching -- the API caches everything from the start of the request up to each `cache_control` breakpoint; any change anywhere in the prefix invalidates everything after it. This makes ordering critical. Design the request structure so static content comes first and dynamic content comes last:

1. Static system prompt and tool definitions (globally cached)
2. CLAUDE.md content (cached within a project)
3. Session context (cached within a session)
4. Conversation messages (dynamic, per-turn)

Cache fragility examples: putting a detailed timestamp in the system prompt, shuffling tool definition order non-deterministically, updating tool parameters mid-session -- all break the cache. Monitor cache hit rate like you monitor uptime; the Claude Code team runs alerts on cache hit rate and declares SEVs when it drops -- a few percentage points of cache miss rate dramatically affects cost and latency.

*Source: Prompt Caching Is Everything (Claude Code team)*

### Never Change Tools or Models Mid-Session

Changing the tool set mid-conversation invalidates the entire cached prefix -- even though it seems intuitive to give the model only the tools it needs right now. Plan Mode is implemented as tools, not tool-set changes: `EnterPlanMode` and `ExitPlanMode` are tools the model can call; a system message explains the mode constraints; the tool definitions never change; bonus: the model can autonomously enter plan mode when it detects a hard problem (see [Plan Mode and Think Mode](#plan-mode-and-think-mode)).

When dozens of MCP tools are loaded, use `defer_loading` stubs instead of removing tools -- lightweight name-only entries with `defer_loading: true` that the model discovers via a `ToolSearch` tool; full schemas load only on selection (see [tools-and-integrations.md#tool-search-defer-loading-for-cache-stability](tools-and-integrations.md#tool-search-defer-loading-for-cache-stability)).

If you must switch models, use subagents -- Opus prepares a handoff message for Haiku/Sonnet rather than switching the main conversation's model (which would require rebuilding the entire cache for the new model).

*Source: Prompt Caching Is Everything (Claude Code team)*

### Use Messages for Updates, Not System Prompt Changes

When information in the prompt becomes stale (time, file state), resist updating the system prompt -- that causes a cache miss across the entire prefix. Instead, pass updated information as a `<system-reminder>` tag in the next user message or tool result; the model processes the update without invalidating the cache. This pattern applies to any dynamic state: current time, feature flags, changed configuration, file modification status.

*Source: Prompt Caching Is Everything (Claude Code team)*

### Cache-Safe Compaction

Naive compaction (summarize conversation in a separate API call with a different system prompt and no tools) wastes all cached tokens -- the new call's prefix does not match the parent conversation. Cache-safe compaction uses the exact same system prompt, user context, session context, and tool definitions as the parent conversation; prepends the parent's conversation messages; appends the compaction prompt as a new user message at the end. From the API's perspective, this request looks nearly identical to the parent's last request -- same prefix, same tools, same history -- so the cached prefix is reused; the only new tokens are the compaction prompt itself.

Trade-off: requires reserving a "compaction buffer" so there is room in the context window for both the compact instruction and the summary output tokens. This pattern is now built into the Claude API's compaction endpoint, so you do not need to implement it manually.

*Source: Prompt Caching Is Everything (Claude Code team)*

### Token Economics: Model Routing and Cost Data

Specific cost benchmarks and environment variable settings for managing Claude Code costs (see [workflow-patterns.md](workflow-patterns.md) for model selection strategy):

**Cost benchmarks:**
- Haiku 4.5 achieves ~73% on SWE-bench at ~$1/$5 per million tokens (66% cheaper than Sonnet 4), enabling 10-agent workflows for ~$0.01-0.05 per code review
- Real-world cost range: $6/user/day average (Anthropic estimate), but power users report $30-60/developer-day on intense coding sessions
- Subagent strategy for token savings: 5 mini-sessions with focused contexts can use fewer total tokens than one giant conversation, though each subagent incurs initial system prompt overhead
- Cache hit rate impact: one user reported 1.5M tokens input but only 66K new output, costing $2.47 vs expected $3-4 -- aggressive caching yields 30-40% savings
- Token budgeting practice: set per-session or per-task caps and enforce with compaction/resume checkpoints
- Pricing ratios (2025-2026): Haiku = 1x, Sonnet = ~4x, Opus = ~19x. Know these ratios for budgeting

**Recommended defaults for `~/.claude/settings.json`:**
- `model: "sonnet"` -- handles ~80% of coding tasks; switch to Opus via `/model opus` only for complex reasoning. ~60% cost reduction vs Opus default
- `MAX_THINKING_TOKENS: "10000"` -- default 31,999 reserves tokens for internal reasoning. Reducing to 10K cuts hidden cost ~70%. Set to `0` for trivial tasks
- `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE: "50"` -- default 95% is too late; quality degrades before compaction triggers. Compacting at 50% keeps sessions healthier
- `CLAUDE_CODE_SUBAGENT_MODEL: "haiku"` -- subagents (Task tool) run on Haiku: ~80% cheaper, sufficient for exploration, file reading, test running

**Strategic compaction timing:** Compact after exploration (before implementation), after milestones, after debugging (before new work), before context shifts. Do NOT compact mid-implementation, during active debugging, or during multi-file refactoring.

**MCP server cost:** Each enabled MCP adds tool definitions to context. Keep under 10 per project. Prefer CLI tools (`gh` vs GitHub MCP).

**Agent Teams cost warning:** Each teammate spawns an independent context window. Use only when parallelism adds clear value; for sequential tasks, subagents are more efficient.

### Model Profiles: Three-Tier Task-to-Model Matching

- Three profiles for multi-agent systems: quality (max reasoning), balanced (smart allocation), budget (minimal expensive model usage)
- Task-to-model matching: planning/architecture -> Opus (highest impact); execution -> Sonnet (follows explicit instructions); read-only verification -> Haiku (structured output, no reasoning needed)
- Per-agent overrides allow fine-tuning without changing the entire profile
- "inherit" alias lets users' configured model version pass through -- avoids hardcoding specific version names
- Verification needs reasoning (Sonnet), not just pattern matching (Haiku) -- goal-backward reasoning requires understanding

*Source: get-shit-done/get-shit-done/references/model-profiles.md*

**Model routing by complexity (for applications calling LLM APIs):**
- Use concrete thresholds -- text > 10K chars or > 30 items routes to Sonnet; everything else routes to Haiku (3-4x cheaper). Always start with the cheapest model and escalate
- Budget tracking: use immutable cost records (frozen dataclasses). Each API call returns a new tracker, never mutates state. Check `over_budget` before each call and fail early
- Narrow retry logic: only retry transient errors (connection, rate limit, server error). Fail fast on auth/validation errors -- retrying these wastes budget on permanent failures
- For system prompts > 1024 tokens, use `cache_control: {"type": "ephemeral"}` to avoid resending on every request
- Anti-patterns: using expensive model for all requests, retrying all errors, hardcoding model names, ignoring prompt caching

(see [project-setup.md](project-setup.md#key-environment-variables) for the full env var reference, [autonomous-agents.md](autonomous-agents.md) for OpenClaw cost optimization)

*Sources: deep-research-report.md, everything-claude-code/docs/token-optimization.md, everything-claude-code/skills/cost-aware-llm-pipeline/SKILL.md*

---

## claude-mem Plugin: Persistent Memory Across Sessions

Claude Code conversations are ephemeral -- when a session ends, context is gone. The `claude-mem` plugin solves this by automatically capturing observations during sessions, compressing them with AI, and injecting relevant context into future sessions.

### How It Works (Lifecycle Hooks)

claude-mem uses five lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd) to observe tool usage, generate semantic summaries, and store them in a local SQLite database with FTS5 full-text search and Chroma vector search. On session start, relevant past context is automatically injected.

### 3-Layer Retrieval Workflow

| Layer | Tool | Tokens per result | Purpose |
|-------|------|-------------------|---------|
| 1 | `search` | ~50-100 | Get compact index with IDs, filter broadly |
| 2 | `timeline` | varies | See chronological context around a result |
| 3 | `get_observations` | ~500-1,000 | Fetch full details for selected IDs only |

This layered approach yields roughly 10x token savings compared to loading full observations upfront.

### Endless Mode

Beta feature for extended sessions. Biomimetic memory architecture that uses ~95% fewer tokens and supports ~20x more tool calls. Enable from the web viewer UI at `http://localhost:37777`.

### Privacy Controls

Wrap sensitive content in `<private>` tags to exclude it from storage. claude-mem never captures content inside these tags.

For deeper discussion of memory layers and persistence strategies, see [memory-persistence.md](memory-persistence.md).

---

## Subagents for Context Isolation

Long conversations accumulate context that interferes with new tasks. Debugging details color a subsequent security review; implementation specifics bias architectural analysis.

Subagents solve this by running in isolated context windows:

- "Use a subagent to perform a security review of that code" -- the subagent sees only the code, not your debugging history.
- One subagent for implementation, another for review, a third for log analysis.
- Define reusable subagents in `.claude/agents/[name].md` with specific roles, tools, and models.

Use subagents whenever a task requires a *different perspective* from the one you have been building in the current conversation. Context separation keeps both analyses sharp (see [failure-patterns.md#1-vision-compression](failure-patterns.md#1-vision-compression) for why mixing strategic and tactical context in one window degrades output).

### Built-In Subagent Types

Claude Code includes three built-in subagent types beyond custom agents:

| Subagent | Mode | Use Case |
|---|---|---|
| **Explore** | Read-only, fast | Searching and analyzing codebases without making changes. Claude specifies thoroughness: quick, medium, or very thorough |
| **Plan** | Read-only, research | Gathers context during plan mode before presenting implementation plans |
| **General-purpose** | Full capabilities | Complex multi-step tasks requiring both exploration and action |

These are automatically invoked by Claude's orchestration layer -- you do not define them in `.claude/agents/`. Custom subagents supplement these built-in types for domain-specific work.

(see [agent-design.md#subagents-in-claude-code](agent-design.md#subagents-in-claude-code) for custom subagent definitions)

---

## Anti-Pattern: Context Pollution

**What it is:** Irrelevant information from earlier tasks accumulates in the context window, degrading Claude's focus and output quality. File contents from debugging sessions, tangential conversations, and stale command outputs create noise that competes with the actual task.

**How to spot it:**
- Claude's responses become less focused or reference old topics
- Token usage is high but the current task is simple
- Claude makes suggestions based on earlier (now-irrelevant) context
- Output quality improves dramatically after `/clear`

**How to prevent it:**
- Run `/clear` between unrelated tasks
- Use `/compact` during long sessions before context degrades
- Launch subagents for distinct phases of work
- Monitor `/context` and act before the window fills
- Keep CLAUDE.md lean -- every token there is loaded on every request

For the full taxonomy of failure patterns including vision compression, premature completion, and plausible echo, see [failure-patterns.md](failure-patterns.md).

### _MANIFEST.md: Preventing Context Pollution in Working Folders

From practitioners using Cowork (and applicable to any AI tool that ingests folders):

- **Problem:** When an AI reads a folder, it ingests everything -- including outdated drafts and replaced documents. A 462-file consulting folder produced contradictory output from pricing models replaced 3 months earlier
- **Fix:** Create a `_MANIFEST.md` in any working folder that declares: which documents are source of truth, which subfolders map to which domains, and what to skip entirely
- **Claude Code Equivalent:** This is the working-folder analog of `.claude/rules/` path-scoped rules -- both solve context pollution but for different environments (see [Rules Directory](#rules-directory-path-specific-scoping))

*Source: Twitter Bookmarks/2026-03-01-heynavtoor-17-best-practices-claude-cowork.md*

---

## Template: Minimal CLAUDE.md Starter

Copy this and customize. For the full operating manual template, see [project-setup.md#minimal-starter-10-lines](project-setup.md#minimal-starter-10-lines).

```markdown
# Project Context

## About
[One sentence: what this project is and what it does.]

## Tech Stack
[Language, framework, database, key libraries.]

## Commands
[Build, test, lint, dev server -- the ones you actually run.]

## Key Directories
- `src/` -- [what lives here]
- `tests/` -- [test framework and conventions]

## Standards
- [Your most important coding convention]
- [Your second most important convention]

## Notes
[One or two gotchas a new developer would hit.]
```

---

## Global-Only vs Dual-Scope Feature Design

Claude Code features follow a scope hierarchy with a clear design principle: personal state and cross-project coordination live globally (`~/.claude/`); team-shareable project config can live at the project level (`.claude/`).

**Global-only features** (cannot be scoped to a project):

| Feature | Location |
|---------|----------|
| Tasks | `~/.claude/tasks/` |
| Agent Teams | `~/.claude/teams/` (experimental, Feb 2026) |
| Auto-memory | `~/.claude/projects/<hash>/memory/` |
| Credentials/OAuth | System keychain + `~/.claude.json` |
| Keybindings | `~/.claude/keybindings.json` |
| MCP user servers | `~/.claude.json` (`mcpServers` key) |

**Dual-scope features** (project overrides global): settings, CLAUDE.md, rules, agents, commands, skills, hooks, MCP servers.

---

## OneContext: Cross-Session Persistent Context Layer

An open-source tool that creates a persistent context layer across sessions, devices, and agents (Claude Code, Codex):

- Records everything but shows agents a high-level summary by default; agents drill down into specific details on demand
- Architecture: Git for time-level management, file system for space-level management
- Improves Claude Code by ~13% on SWE-Bench (paper: arxiv.org/abs/2508.00031)
- Shareable context via link -- anyone can continue building on the same shared context
- Solves the "single .md file is too general" problem: a single summary file loses detail, but loading everything bloats context. OneContext provides progressive disclosure at the context layer.
- Install: `npm i -g onecontext-ai` (macOS only initially)

(see [community-insights.md](community-insights.md) for full tool details, [memory-persistence.md](memory-persistence.md) for related patterns)

---

## Knowledge Type Placement Matrix

A unified decision matrix mapping knowledge types to their optimal home, format, load strategy, and update cadence across Claude Code's primitives:

| Knowledge Type | Best Home | Format | Load Strategy | Update Cadence |
|---|---|---|---|---|
| Durable project rules ("always do X") | `CLAUDE.md` + `.claude/rules/` (if large) | Short bullets + exact commands; no long prose | Always loaded | Review when failures occur |
| Directory/language-specific conventions | Path-scoped `.claude/rules/*.md` | YAML `paths:` + tight rules + examples | Loaded only when matching files touched | As code evolves |
| Architecture invariants + "why" | Repo docs (ADRs) + short pointer in CLAUDE.md | One-paragraph invariant + link/pointer | Retrieve on demand | On major changes |
| Implementation recipes (repeatable patterns) | Reference skill + supporting files | `SKILL.md` navigation + `reference.md`/`examples.md` | On-demand (invoked or relevant) | Quarterly pruning |
| Debugging playbooks | Skill and/or auto memory topic file | Checklist: symptom -> likely cause -> verify -> fix | On-demand; always-loaded index minimal | After significant incidents |
| Workflow checklists (PR review, refactor, release) | Action skill | `disable-model-invocation: true` for side effects; explicit steps | User-invoked | Whenever workflow changes |
| Environment/setup instructions | Repo docs + minimal CLAUDE.md "must-run" commands | Exact setup commands + expected outputs | Mostly retrieved | When setup changes |
| Lessons learned / recurring mistakes | Auto memory + periodic "promote to rules/skills" | Short entries + pointers to detailed topic files | Index always-loaded; details on demand | Continuous |
| User preferences (cross-project) | `~/.claude/rules/` + personal skills | `Preferences.md` / `workflows.md` | Always loaded (user rules) | Rarely |

Consolidates guidance scattered across CLAUDE.md (see [What to Include](#what-to-include-and-what-not-to-include)), Rules Directory (see [Rules Directory](#rules-directory-path-specific-scoping)), Skills (see [skills.md](skills.md)), and Auto Memory (see [Auto Memory](#auto-memory-claudes-self-managed-memory-scratchpad)) into a single actionable reference.

*Source: deep-research-report-claudecodeknowledgelayer.md*

### Enforcement Guarantee Ladder

Decision rule for choosing where knowledge lives, ordered by enforcement strength:

| Guarantee Level | Primitive | When to Use | Enforcement | Example |
|---|---|---|---|---|
| **Deterministic** | Hook (PreToolUse exit 2) | Rule must NEVER be violated | Hard block -- tool call rejected | Source file write protection |
| **Validated** | Hook (PostToolUse) | Output must meet format/integrity constraints | Post-hoc check with error report | Cross-ref validation after KB edits |
| **Always-loaded** | CLAUDE.md / `.claude/rules/` | Rule is always true for this project | Advisory but always in context | Code style, architecture invariants |
| **On-demand** | Skill (`.claude/commands/`) | Relevant only during specific workflows | Only active when user invokes | `/process-notes`, `/consolidate-kb` |
| **Accumulated** | Auto memory (`~/.claude/projects/`) | Learned through experience over sessions | Passive -- loaded at session start | User preferences, recurring patterns |

**Decision flowchart:** Will violating this cause data loss or corruption? -> Hook. Is this always relevant? -> CLAUDE.md/rules. Is this workflow-specific? -> Skill. Is this a learned preference? -> Auto memory.

Complements the Knowledge Type Placement Matrix above by adding the enforcement dimension -- the matrix answers "where does this type of knowledge go?", the ladder answers "how strongly must it be enforced?"

*Source: deep-research-report-claudecodeknowledgelayer.md, Phase 16 implementation experience*

---

## Scaling Strategy Matrix: When to Add Complexity

A tier-based guide for sizing your Claude Code knowledge infrastructure. Key principle: start minimal, only add complexity when you can demonstrate the current tier is insufficient.

| Scale Tier | What "Enough" Looks Like | When Plain Docs Suffice | When Search Becomes Necessary | When Vector/Hybrid Is Worth It |
|---|---|---|---|---|
| **Tiny** | `CLAUDE.md` + 1-3 rules files | If grep finds everything in <30s | When you repeatedly re-explain basics | Rarely |
| **Small** | Add path-scoped `.claude/rules/` + a few skills | If skills reliably cover recurring workflows | When docs exceed ~50-100 files or "where is X?" recurs | Only if many queries are conceptual (not keywordable) |
| **Medium** | Skills with supporting files; hooks; auto memory discipline; optional `--add-dir` | If workflows are encoded as skills and rules prevent rediscovery | When retrieval latency or context bloat becomes a bottleneck | When you need both exact identifiers + concept retrieval; hybrid first |
| **Large** | Dedicated retrieval service via MCP; strict metadata; eval harness | Almost never (too much sprawl) | Always | Often, but only with strong evaluation + drift control |

**Stop signs indicating overengineering:**
- CLAUDE.md keeps growing -- move content to skills/hooks (see [failure-patterns.md](failure-patterns.md#4-context-pollution))
- MCP server/tool sprawl -- disable unused servers, prefer CLI tools, enable Tool Search (see [context-engineering.md](context-engineering.md#mcp-context-budget-rule-of-thumb))

*Source: deep-research-report-claudecodeknowledgelayer.md*
