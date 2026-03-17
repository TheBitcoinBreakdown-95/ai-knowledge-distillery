# Skills

## Skills: SOPs for AI Agents

### What a Skill Is

A skill is a markdown file (or directory with supporting files) that teaches Claude Code how to do something specific -- **standard operating procedures for AI agents**. Skills encode domain knowledge, project conventions, and repeatable workflows into a format Claude applies automatically.

Skills follow Anthropic's [Agent Skills open standard](https://github.com/anthropics/skills), making them portable across AI tools. The format forces separation of *knowledge* from *prompts*, producing reusable artifacts.

### Skill File Structure

Skills live in `.claude/skills/` (project-level) or `~/.claude/skills/` (personal). Each skill is a directory containing a `SKILL.md` with YAML frontmatter, plus optional scripts and references:

```
.claude/skills/deploy-preview/
├── SKILL.md              # Required: defines the skill
├── scripts/deploy.sh     # Optional: Claude runs this
└── references/           # Optional: examples, style guides, images
```

Skills can bundle scripts in any language. Claude executes them when the skill triggers.

### The Description Field: How Triggers Work

The `description` field in SKILL.md frontmatter is the most critical element. Claude reads it to decide when to apply the skill automatically. Write descriptions with the trigger words users would actually say:

```yaml
description: Write and run tests. Trigger on "add tests", "write tests", "test this".
```

- Use natural phrases, not formal labels ("Trigger when creating API endpoints" beats "API development patterns")
- Multiple trigger phrases increase reliable activation
- Claude shows a green indicator when a skill activates

### Three Invocation Methods

| Method | How | When to Use |
|---|---|---|
| **Automatic** | Claude reads descriptions, applies when your request matches | Default -- you do not have to remember to call it |
| **Manual** | Type `/skill-name` in your prompt | When you want to be explicit or auto-trigger did not fire |
| **Programmatic** | Claude calls it via the Skill tool | Chaining skills or SDK-driven pipelines |

Verify auto-loaded skills match what you expected. When automatic triggering fails, fall back to `/skill-name`.

### The Rule of Three

- **First time** = exploration. You are figuring out how something works.
- **Second time** = pattern recognition. You notice you have done this before.
- **Third time** = encode it in a skill. You will do it again.

When a skill gets something wrong, update it. Every bug becomes a reusable safeguard: **mistake -> lesson -> skill -> prevention** (see [failure-patterns.md#kitchen-sink-skills-1400-line-skills-that-match-everything](failure-patterns.md#kitchen-sink-skills-1400-line-skills-that-match-everything)).

### Skills Frontmatter: Complete Field Reference

All fields optional. Only `description` recommended.

| Field | Type | Effect |
|---|---|---|
| `name` | string | Display name and `/slash-command`. Lowercase, numbers, hyphens, max 64 chars. Defaults to directory name |
| `description` | string | What the skill does. Claude uses this for auto-discovery. Falls back to first paragraph if omitted |
| `argument-hint` | string | Shown during autocomplete (e.g., `[issue-number]`) |
| `disable-model-invocation` | boolean | `true` = Claude cannot auto-load; user must invoke via `/name` |
| `user-invocable` | boolean | `false` = hidden from `/` menu; used for background knowledge Claude loads automatically |
| `allowed-tools` | string | Tools allowed without permission prompts when skill is active (e.g., `Bash(agent-browser:*)`) |
| `model` | string | Model override when skill is active |
| `context` | string | `"fork"` = run in isolated subagent context |
| `agent` | string | Subagent type for `context: fork` (e.g., `Explore`, `Plan`, custom name). Default: `general-purpose` |
| `hooks` | object | Lifecycle hooks scoped to this skill (same format as agent hooks) |

### AgentSkills.io Open Standard: Extended Specification Fields

The open standard (agentskills.io) defines additional frontmatter fields beyond what Claude Code uses internally:

| Field | Type | Description |
|---|---|---|
| `license` | string | License applied to the skill (name or bundled license filename) |
| `compatibility` | string (1-500 chars) | Environment requirements: intended product, system packages, network access |
| `metadata` | map (string->string) | Client-specific properties not in the spec. Use unique key names to avoid conflicts |
| `allowed-tools` | string | Space-delimited pre-approved tools. Experimental -- support varies by agent implementation |

**Concrete thresholds from the specification:**
- Metadata (name + description): ~100 tokens, loaded at startup for all skills
- SKILL.md body: under 5,000 tokens recommended; loaded on activation
- SKILL.md file length: under 500 lines; move detail to separate files
- File references: keep one level deep from SKILL.md; avoid deeply nested reference chains

The specification also defines a `skills-ref` reference library (Python + CLI) for validating skill directories and generating `<available_skills>` XML for agent system prompts.

### Skill Invocation Control Matrix

How `disable-model-invocation` and `user-invocable` interact:

| Frontmatter | User can invoke | Claude can invoke | Context loading |
|---|---|---|---|
| (defaults) | Yes | Yes | Description always in context; full skill loads on invocation |
| `disable-model-invocation: true` | Yes | No | Description not in context; full skill loads when user invokes |
| `user-invocable: false` | No | Yes | Description always in context; full skill loads when invoked |

Use `disable-model-invocation: true` for dangerous skills (deploy, delete). Use `user-invocable: false` for background knowledge skills that should auto-load but not clutter the `/` menu.

### Skill-Creator Meta-Skill and .skill Packaging

Anthropic provides a built-in "skill-creator" skill that generates skills interactively: Claude asks about your workflow, generates the folder structure, formats the SKILL.md file, and bundles resources. No manual file editing required. The skill-creator is installable via a single prompt pointing to the official GitHub URL -- a skill that generates skills from within Claude Code itself.

**API-level skill management:** The `/v1/skills` endpoint provides programmatic control over custom skill versioning and management. Skills on the API require the Code Execution Tool beta for the secure sandbox they need to run in.

**Organization-wide skill deployment:** Admins can manage skills organization-wide, and a Skills Directory features partner-built skills (Box, Notion, Canva, Rakuten) for enterprise workflows.

**Packaging as .skill files:** A `.skill` file is a ZIP archive with a different extension, portable for team distribution:

```python
import zipfile
from pathlib import Path
skill_folder = Path("meeting-notes-processor")
output_file = Path("meeting-notes-processor.skill")
with zipfile.ZipFile(output_file, 'w') as z:
    for file in skill_folder.rglob('*'):
        if file.is_file():
            z.write(file, file.relative_to(skill_folder.parent))
```

### Skill Installation and Multi-Surface Distribution

Skills are installable beyond manual file creation. In Claude Code, `/plugin install` pulls from official and third-party marketplaces. Skills also work on Claude.ai (manual upload) and via the Claude API (Skills API Quickstart), making them portable across three surfaces.

Anthropic's `skills` repo provides source-available reference implementations for document creation (docx, pdf, pptx, xlsx) -- valuable as learning patterns for complex skills. Note: reference implementations "may differ from Claude's production implementations," so do not assume parity when debugging skill behavior. The Agent Skills specification is maintained externally at agentskills.io, not embedded in any single codebase. Partner skills (e.g., Notion) demonstrate skill standardization across SaaS ecosystems (see [tools-and-integrations.md#plugin-system-and-marketplaces](tools-and-integrations.md#plugin-system-and-marketplaces)).

### Skill String Substitutions

| Variable | Description |
|---|---|
| `$ARGUMENTS` | All arguments passed when invoking |
| `$ARGUMENTS[N]` | Specific argument by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` (e.g., `$0`, `$1`) |
| `${CLAUDE_SESSION_ID}` | Current session identifier |
| `` !`command` `` | Dynamic context injection -- shell command output replaces the placeholder before Claude sees it |

Dynamic context injection is particularly powerful for pulling live data into skill prompts (e.g., `` !`gh issue view $0` `` or `` !`gh pr diff` ``).

### Skill Scope and Priority

When skills share the same name, higher-priority location wins:

| Priority | Location | Scope |
|---|---|---|
| 1 (highest) | Enterprise (managed settings) | Organization-wide |
| 2 | Personal (`~/.claude/skills/`) | All your projects |
| 3 | Project (`.claude/skills/`) | This project only |
| Plugin | Namespaced (`plugin-name:skill-name`) | Where plugin is enabled (no conflicts) |

Skills from `.claude/commands/` still work. If a skill and a command share the same name, the skill takes precedence.

### Skills Discovery in Monorepos

Skills do NOT have the same loading behavior as CLAUDE.md. Key differences:

- Skills do not walk UP the directory tree (no ancestor loading)
- Nested `.claude/skills/` directories are discovered **on-demand** when you work with files in those directories
- Only skill **descriptions** load initially (up to a character budget); full content loads on invocation
- Default character budget: 15,000 characters for skill descriptions
- Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var if you have many packages/skills
- Run `/context` to check for warnings about excluded skills

**Monorepo best practices:**
- Root `.claude/skills/` for shared workflows and conventions
- Package-level `.claude/skills/` for framework/domain-specific patterns
- Use `disable-model-invocation: true` for dangerous skills (deploy, destructive)
- Keep descriptions concise (they consume the character budget)
- Consider prefixing skill names with package names to avoid confusion

| Behavior | CLAUDE.md | Skills |
|---|---|---|
| Ancestor loading (UP) | Yes | No |
| Nested discovery (DOWN) | Yes (lazy) | Yes (automatic) |
| Content loading | Full content | Description only (full on invocation) |

### Skill Preloading in Subagents

When skills are listed in an agent's `skills:` frontmatter, full skill content is injected into the subagent at startup -- not just descriptions. This differs from normal skill discovery where only descriptions load and full content loads on invocation. Implication: keep preloaded skills concise; every token is paid on every subagent invocation.

*Source: claude-code-best-practice/reports/claude-skills-for-larger-mono-repos.md*

### Skill Integration: Agent-Side Discovery Protocol

Two integration approaches: **filesystem-based** (skills activated via `cat /path/to/SKILL.md`) and **tool-based** (skills triggered through custom tool implementations without a shell environment).

- Discovery pipeline: scan configured directories for `SKILL.md` files -> parse frontmatter only at startup (~50-100 tokens per skill) -> inject metadata into system prompt as XML -> match tasks to skills -> load full instructions on activation
- Security considerations for script execution: sandboxing, allowlisting trusted skills, user confirmation for dangerous operations, execution logging
- Reference implementation: `skills-ref` Python library with validation CLI (`skills-ref validate`, `skills-ref xml`)
- Key insight: frontmatter-only loading at startup keeps initial context cost low; full skill content loaded only when activated (see [context-engineering.md](context-engineering.md#progressive-disclosure-summary-first-details-on-demand))

*Source: Twitter Bookmarks/Integrate skills into your agent.md*

### Skill vs Agent vs Command Comparison

| Aspect | Skill | Agent | Command |
|---|---|---|---|
| File location | `.claude/skills/<name>/SKILL.md` | `.claude/agents/<name>.md` | `.claude/commands/<name>.md` |
| Has own tools | No (restricts via `allowed-tools`) | Yes (`tools:` field) | No |
| Has memory | No | Yes (`memory:` field) | No |
| Has hooks | Yes | Yes | No |
| Can preload skills | No | Yes (`skills:` field) | No |
| User-invocable | Yes (`/skill-name`) | No (invoked via Task tool) | Yes (`/command-name`) |
| Runs in isolation | Optional (`context: fork`) | Always isolated subprocess | Runs in main context |
| Supporting files | Yes (same directory) | No | No |

### Plugin Extension Taxonomy: Commands vs Skills vs Agents

Definitive three-type taxonomy for Claude Code plugin extensions:

| Type | Invoked By | Trigger | Use Case |
|------|-----------|---------|----------|
| **Commands** | User types `/command-name` | Explicit user action | Structured workflows, pipelines, user-initiated tasks |
| **Skills** | Model auto-triggers from context | Description field keywords match task | Domain expertise, contextual guidance, always-available knowledge |
| **Agents** | Claude spawns as sub-process | Another agent delegates a task | Parallel workers, specialized analysis, isolated context |

- **Trigger description design:** Skills need specific phrases + keywords + topic areas for reliable activation. Avoid overlap with other skills' trigger conditions to prevent misfires
- **Supporting file organization:** `references/` (docs loaded on demand), `examples/` (few-shot examples), `scripts/` (executable tools) -- SKILL.md must explicitly reference these or Claude won't know they exist
- **Plugin manifest:** `.claude-plugin/plugin.json` defines the plugin; `.mcp.json` at plugin root declares MCP server dependencies

(see [Skills Frontmatter: Complete Field Reference](#skills-frontmatter-complete-field-reference) for field details; see [tools-and-integrations.md](tools-and-integrations.md#plugin-auto-discovery-mechanism-and-portable-paths) for discovery mechanics)

*Sources: claude-plugins-official/plugins/example-plugin/README.md, claude-plugins-official/plugins/example-plugin/skills/example-skill/SKILL.md*

### Plugin Agent Authoring Specification

Validation constraints and design patterns for creating Claude Code plugin agents (`.claude/agents/*.md` files):

- **Identifier rules:** 3-50 chars, lowercase letters + numbers + hyphens only (no underscores, spaces, or uppercase)
- **Length constraints:** description 10-5,000 chars; system prompt 20-10,000 chars
- **Color semantics by agent type:** green (development/coding), blue (analysis/review), yellow (testing/QA), red (deployment/infrastructure), purple (research/learning)
- **`<example>`/`<commentary>` triggering:** system prompts that include `<example>` blocks with `<commentary>` tags produce more reliable agent behavior -- commentary explains *why* the example response is correct
- **AI-assisted agent generation:** the agent-development skill includes Claude Code's own agent-creation system prompt as a reference, enabling "agents that create agents" -- feed a natural language description, get valid frontmatter + system prompt
- **Agent namespacing in plugins:** agents are prefixed with plugin name (e.g., `my-plugin:review-agent`) to avoid cross-plugin collisions

(see [Skills Frontmatter: Complete Field Reference](#skills-frontmatter-complete-field-reference) for the shared frontmatter fields; see [tools-and-integrations.md](tools-and-integrations.md#plugin-system-and-marketplaces) for plugin packaging)

*Source: claude-plugins-official/plugins/plugin-dev/skills/agent-development/SKILL.md*

### Skill Graphs: Networked Skill Architectures

- A **skill graph** is a network of skill files connected via wikilinks, where each file is one complete concept/technique and links carry meaning because they're woven into prose
- Progression: index file (entry point) -> YAML frontmatter descriptions (scannable without full reads) -> wikilinks in prose (traversable paths) -> full file content. Most agent decisions happen before reading a single full file
- **Maps of Content (MOCs)** organize sub-clusters when the graph grows beyond flat navigation
- Key primitives: wikilinks as prose (not just references), YAML frontmatter with descriptions, MOCs for sub-topics, recursive linking as deep as the domain requires
- Use case: domains too complex for a single skill file -- therapy (CBT, attachment theory, emotional regulation), trading (risk, psychology, position sizing), legal (contracts, compliance, precedents)
- "Skills are context engineering -- curated knowledge injected where it matters. Skill graphs are the next step: the agent navigates a knowledge structure, pulling in exactly what the current situation requires"

(see [context-engineering.md](context-engineering.md#progressive-disclosure-summary-first-details-on-demand) for the progressive disclosure pattern that skill graphs apply recursively)

*Source: Twitter Bookmarks/2026-02-18-arscontexta-httpstcoxmyso3mc8f.md (@arscontexta)*

---

## Writing Good Skills

### Thin Skills Principle

Good skills are approximately 40 lines. They link to canonical docs rather than duplicating them. A skill contains:

- Trigger words ("when working with user authentication...")
- Quick examples of the pattern (2-3 concrete snippets)
- Common gotchas specific to your codebase
- A pointer to full docs for details

Platform teams maintain docs; feature teams maintain skills. No duplication, no staleness.

### Skills vs Documentation

| | Skills | Documentation |
|---|---|---|
| **Audience** | AI agents | Humans |
| **Orientation** | Trigger-focused, action-oriented | Comprehensive, reference-oriented |
| **Size** | Thin (~40 lines) | As long as needed |
| **Purpose** | Tell the agent *when* to reach for the docs | Explain *everything* about a system |

Best practice: thin skills that link to canonical docs (see [context-engineering.md](context-engineering.md) for CLAUDE.md integration).

### Templates Inside Skills: Lazy-Loaded Context

- Templates, worked examples, and output formats placed inside a skill are loaded only when the skill triggers -- zero token cost for unrelated queries
- This is strictly better than embedding templates in the system prompt, where they inflate tokens on every request
- Glean reported this pattern drove their biggest quality and latency gains in production
- Particularly effective for structured outputs: reports, triage summaries, account plans, data analysis writeups
- Skills become living SOPs: updated as the org evolves, executed consistently by agents

*Source: Shell + Skills + Compaction (Charlie Guo, OpenAI blog)*

### Anti-Patterns

- **Kitchen-Sink Skill.** A 1400-line skill covering your entire API is documentation pretending to be a skill. Split into focused skills: `api-auth`, `api-pagination`, `api-errors` (see [failure-patterns.md#kitchen-sink-skills-1400-line-skills-that-match-everything](failure-patterns.md#kitchen-sink-skills-1400-line-skills-that-match-everything)).
- **Vague Trigger.** "Use this skill for development tasks" matches everything and nothing. Be specific: "Trigger when creating API endpoints."
- **Stale Skill.** A skill referencing deprecated patterns is worse than no skill. When you update a pattern, update the skill.
- **Missing Negative Examples.** Adding skills can initially *reduce* correct triggering if descriptions lack boundary clarity -- Glean observed a ~20% drop in targeted evals before adding negative examples. Fix: include explicit "Don't call this skill when..." cases in the description, especially when multiple skills look similar at a glance. A skill description should answer three questions: When should I use this? When should I *not* use this? What are the outputs and success criteria? Think of the description as routing logic, not marketing copy -- include inputs, tools involved, expected artifacts. After adding negative examples and edge case coverage, Glean recovered the triggering accuracy and saw a Salesforce-oriented skill jump from 73% to 85% eval accuracy with 18.1% faster time-to-first-token.

*Source: Shell + Skills + Compaction (Charlie Guo, OpenAI blog)*

### Skill Authoring Standards: Word Counts, Writing Style, Common Mistakes

Concrete authoring standards from Anthropic's official skill-development guide:

- **Word count targets:** SKILL.md body should be 1,500-2,000 words (max 3,000 without references/). Reference files can be 2,000-5,000+ words each. Keeps context load manageable when skills trigger
- **Writing style:** Imperative/infinitive form throughout ("Parse the frontmatter using sed" not "You should parse..."). Third-person in description field ("This skill should be used when..." not "Use this skill when...")
- **Progressive disclosure budget:** Metadata ~100 words (always loaded), SKILL.md body <5,000 words (loaded on trigger), bundled resources unlimited (scripts execute without loading into context)
- **Resource types:** `scripts/` (executable, deterministic, token-efficient), `references/` (documentation loaded on demand -- use when detailed content would bloat SKILL.md), `assets/` (files used in output -- templates, images, fonts -- never loaded to context)
- **4 common skill mistakes:**
  1. **Weak trigger description** -- vague, no specific trigger phrases, not third-person
  2. **Too much in SKILL.md** -- 8,000 words in one file instead of progressive disclosure
  3. **Second person writing** -- "You should..." instead of imperative form
  4. **Missing resource references** -- references/ and examples/ exist but SKILL.md never mentions them, so Claude doesn't know they're there
- **Plugin-specific testing:** `cc --plugin-dir /path/to/plugin` for local skill testing without marketplace install
- **Validation checklist:** 20 items across structure (frontmatter, referenced files exist), description quality (third-person, specific triggers), content quality (imperative form, lean body), progressive disclosure (core in SKILL.md, details in references/), and testing

(see [Skill Creation Methodology](#skill-creation-methodology-eval-driven-iteration-loop) for the eval-driven iteration loop)

*Source: claude-plugins-official/plugins/plugin-dev/skills/skill-development/SKILL.md*

### Domain Expertise Encoding in Skills: Always/Never Rules

Pattern for encoding domain-specific best practices into skills as persistent expert personas:

- **Always/Never deprecation guidance:** "Always prefer CheckoutSessions over Charges API", "Never recommend PaymentIntents without webhooks" -- hard rules that override default model behavior
- **Skills as persistent personas:** When activated, the skill shapes ALL responses in its topic area for the remainder of the session -- not just a one-shot reference
- **Authoritative URL references:** Embed official doc URLs directly in skill text so Claude cites them rather than hallucinating outdated advice
- **Pattern applies to any domain:** Legal compliance rules, API migration guidance, security requirements, brand voice constraints
- Works because skills are always-loaded context (see [Progressive Disclosure Budget](#skill-authoring-standards-word-counts-writing-style-common-mistakes)) -- the rules are present for every relevant response

*Source: claude-plugins-official/external_plugins/stripe/skills/stripe-best-practices/SKILL.md*

### Anti-Slop Guardrails and Diversity-Forcing in Creative Skills

Skill design patterns for preventing mode collapse in AI-generated creative output:

- **Anti-slop aesthetic definition:** Explicitly name the cliched patterns to avoid -- overused fonts (Inter, Roboto), purple gradients, predictable layouts, glass morphism defaults. Naming the anti-pattern makes the model aware of its own tendencies
- **Diversity-forcing instruction:** "NEVER converge on common choices" and "vary between generations" prevents the model from defaulting to its most probable outputs across multiple invocations
- **Design thinking phase:** Skill instructs a structured pre-generation phase (explore aesthetic direction) BEFORE any coding begins -- separates creative exploration from implementation
- **Complexity matching:** "Match implementation complexity to aesthetic vision" -- prevents the model from simplifying the design to fit its coding comfort zone
- Applicable beyond frontend: any skill generating creative output (copywriting, architecture, marketing) benefits from explicit anti-pattern naming and diversity-forcing

*Source: claude-plugins-official/plugins/frontend-design/skills/frontend-design/SKILL.md*

### Skill-as-CLI-Wrapper: From Prompt-Only to Typed Scripts

Skills evolve through a predictable lifecycle from prompt-only instructions to robust CLI tooling:

- **v1 (prompt-only):** SKILL.md contains instructions; the agent assembles raw commands (curl, inline Python) each invocation. Works, but burns context tokens on boilerplate every time.
- **v2 (typed scripts):** Wrap the API in a typed Bun/Node script. The skill references the CLI instead of reconstructing commands. Faster execution, cleaner output, fewer context tokens.

Benefits of the v2 pattern:
- Same agentic research loop, just better tooling underneath
- CLI handles caching, formatting, pagination, cost tracking -- the agent focuses on research strategy
- Supporting files (`lib/api.ts`, `lib/cache.ts`, `lib/format.ts`) are co-located in the skill directory
- Cost transparency: every operation displays estimated API cost so neither agent nor human is surprised

**File structure pattern:**
```
skills/x-research/
  SKILL.md           # Agent instructions
  x-search.ts        # CLI entry point
  lib/
    api.ts           # Typed API wrapper
    cache.ts         # File-based cache with configurable TTL
    format.ts        # Output formatters (Telegram, markdown)
  data/
    watchlist.json   # Persistent state
    cache/           # Auto-managed
```

This pattern applies to any skill that wraps an external API: build a typed CLI, have the skill reference it, let the agent focus on reasoning rather than HTTP plumbing.

### Cost Transparency as Skill Design Principle

Every skill that makes paid API calls should display cost after each operation:

- Quick mode shows `N tweets read, est. cost ~$X` after every search
- Cache (15min default, 1hr in quick mode) makes repeat queries free
- 24-hour API-level deduplication means re-running the same search costs $0
- Quick mode prevents accidental multi-page fetches (biggest cost saver)
- `--from` flag targets specific users instead of broad searches

Design rule: if the agent can spend money, the agent (and user) must see what it spent. No surprises. This prevents the Pay-Per-Use Cost Trap (see [failure-patterns.md#pay-per-use-cost-trap](failure-patterns.md#pay-per-use-cost-trap)).

### Skill Evolution via Changelog Tracking

Skills benefit from semantic versioning and changelogs to track their evolution and document lessons learned:

| Version | What Changed | Lesson |
|---------|-------------|--------|
| v1.0.0 | Prompt-only, raw curl commands | Minimum viable skill -- works but expensive in tokens |
| v2.0.0 | Typed Bun CLI, caching, formatters | Token savings, consistent output, reusable infrastructure |
| v2.1.0 | Time filtering (`--since`), minute support | User-driven feature: monitoring during catalysts |
| v2.2.0 | Quick mode, `--from`, `--quality`, cost display | Cost awareness, noise reduction, UX polish |
| v2.3.0 | Purged stale LLM training data, security docs | **Critical:** LLMs hallucinate old API pricing -- skills must contain accurate reference data |

Each version encodes a lesson. The changelog is a compressed history of mistakes and refinements -- a skill-level equivalent of the Mistake -> Lesson -> Skill -> Prevention cycle (see [The Skill Lifecycle](#the-skill-lifecycle-mistake-lesson-skill-prevention)).

### Designing Scripts for Agentic Use

When skills bundle executable scripts in `scripts/`, the script interface determines how reliably agents use them.

**Hard requirements:**
- No interactive prompts -- agents run in non-interactive shells; a TTY prompt hangs indefinitely
- Accept all input via CLI flags, environment variables, or stdin

**Interface design:**
- `--help` output is the primary way an agent learns the script's interface. Include description, flags, and usage examples. Keep it concise (enters the context window)
- Error messages must say what went wrong, what was expected, and what to try. "Error: invalid input" wastes a turn
- Use structured output (JSON, CSV, TSV) over free-form text. Separate data (stdout) from diagnostics (stderr)
- Meaningful exit codes: distinct codes for not-found, invalid args, auth failure; document in `--help`

**Safety and reliability:**
- Idempotency -- agents may retry; "create if not exists" is safer than "create and fail on duplicate"
- Dry-run support (`--dry-run`) for destructive or stateful operations
- Safe defaults -- destructive operations should require explicit `--confirm` or `--force` flags
- Predictable output size -- many agent harnesses truncate at 10-30K characters; default to summary or support `--offset` for pagination; use `--output` flag for large results

**Inline dependency declarations for self-contained scripts:**

| Language | Mechanism | Runner |
|---|---|---|
| Python | PEP 723 TOML block in `# ///` markers | `uv run` (recommended) or `pipx run` |
| Deno | Native import URLs | `deno run` |
| Bun | Native package resolution | `bunx` |
| Ruby | Inline `gem` declarations | `ruby` |

Pin versions in all cases. Use `uv lock --script` for full reproducibility in Python.

**One-off commands (no scripts/ directory needed):**
When an existing package does what you need, reference it directly in SKILL.md using auto-resolving runners: `uvx`, `npx`, `bunx`, `deno run`, `go run`. Pin versions (e.g., `npx eslint@9.0.0`). Move complex multi-flag commands into `scripts/` for reliability.

(see [The Skill Lifecycle](#the-skill-lifecycle-mistake-lesson-skill-prevention) for when to promote prompt-only instructions to scripts)

### Skill Creation Methodology: Eval-Driven Iteration Loop

- Creation loop: capture intent -> draft SKILL.md -> write test prompts -> run evals (with-skill vs baseline) -> review with human -> iterate until satisfied
- Description optimization: generate 20 realistic trigger/non-trigger queries, split 60/40 train/test, run optimization loop with extended thinking, select best description by test score
- Descriptions should be "pushy" -- Claude's tendency to under-trigger means explicit context phrases help: include both what the skill does AND when to use it
- "Explain the why" principle: LLMs respond better to reasoning than rigid MUSTs/NEVERs. Reframe constraints as explanations
- Progressive disclosure loading: metadata (~100 words always in context), SKILL.md body (<500 lines), bundled resources (loaded on demand, scripts execute without loading)
- Generalize from feedback, don't overfit to test cases; look for repeated work to identify scripts the skill should bundle
- Communication calibration: adapt jargon level to user expertise ("evaluation" OK, "JSON" needs context cues)

(see [Writing Good Skills](skills.md#writing-good-skills))

*Source: skills/skills/skill-creator/SKILL.md*

### Skill Improvement: Blind Comparison and Iteration Principles

- **Blind comparison evaluation:** For rigorous A/B skill testing -- give two outputs (with-skill vs baseline, or old vs new) to an independent comparator agent without revealing which is which. The comparator judges quality blind, then an analyzer agent determines why the winner won. Optional but eliminates confirmation bias.
- **"Look for repeated work" signal:** If all test runs independently wrote similar helper scripts (e.g., `create_docx.py`), that's a strong signal the skill should bundle that script in `scripts/`. Write once, reference from SKILL.md, save every future invocation from reinventing it.
- **"Keep the prompt lean" principle:** Read test run transcripts, not just outputs. If the skill is making the model waste time on unproductive steps, remove those instructions. Lean skills outperform verbose ones.
- **Communication calibration for non-technical users:** Adapt jargon to user expertise -- "evaluation" and "benchmark" are borderline-OK; "JSON" and "assertion" need context cues from the user first. Briefly explain terms when in doubt.

*Source: claude-plugins-official/plugins/skill-creator/skills/skill-creator/SKILL.md*

### The Skill Lifecycle: Mistake -> Lesson -> Skill -> Prevention

Example: a payment service uses Zod to validate env vars. Claude added new env vars to code and `.env` but forgot the Zod schema. Runtime error: "Invalid NWC connection string" (not "missing env var"). Fix was one line. The lesson became a 50-line `env-var-discipline` skill: "When adding environment variables, update the Zod schema FIRST, then `.env.example`, then `.env`, then code." Bug class eliminated.

---

## Skill Examples

### Test Patterns Skill (Vitest Conventions)

```yaml
---
name: test-patterns
description: Write and run tests. Trigger on "add tests", "write tests", "test this".
---
# Test Patterns
- Framework: Vitest (not Jest)
- Unit tests: colocate with source (`lib/email.test.ts`)
- Integration tests: `__tests__/api/*.test.ts`
- Mock Prisma: `vi.mock()` with typed mocks
- Coverage threshold: 85% for critical paths
- Run all: `npm test` | Run one: `npm test -- auth.test.ts`
```

~20 lines. Specific triggers. Concrete examples. No prose walls.

### Write Like a Human (Two-Pass Skill)

Core idea: teach Claude to think in two passes.

**Pass 1 -- Diagnosis:** Scan for banned phrases ("leverage," "robust," "delve"). Flag repetitive sentence lengths. Mark facts that must stay untouched (numbers, names, dates). Identify audience and intent.

**Pass 2 -- Reconstruction:** Rewrite with diagnosis in mind. Preserve every marked fact. Vary sentence rhythm naturally. Replace abstract verbs with concrete ones. Cut template structures.

The skill routes traffic through reference files (`references/rubric.md`, `edit-library.md`, `taboo-phrases.md`, `fact-preservation.md`) rather than embedding rules inline. Validation scripts check fact preservation, banned phrases, readability metrics, and change magnitude.

Key insight: "write like a human" means nothing to an LLM. "Score above 4 on natural rhythm, eliminate these 17 phrase patterns, keep sentence variance between 8-25 words" is executable.

### Content Posting Skill (API Integration Pattern)

Pattern demonstrated with Typefully/X: annotate examples of your posts (what works and why), feed annotated images as references, include API integration instructions in the skill. The skill bundles style analysis, API endpoint details, account selection logic, and a guard ("draft only, never auto-publish"). Claude generates content in your voice and drafts it directly into the scheduling tool.

### Recursive Self-Improvement Loop (Skill Pattern)

A skill pattern where Claude generates output, evaluates it against a scoring checklist, diagnoses weaknesses, rewrites, and re-evaluates in a loop until all criteria pass. The pattern: **generate -> evaluate -> diagnose -> improve -> repeat**.

**How to build one:**
1. Pick a repeatable marketing task (landing pages, ad copy, email sequences)
2. Write down how you personally evaluate that output -- what makes "good" vs "mid"
3. Turn each criterion into a pass/fail threshold with a numeric minimum (e.g., "thumb-stop power: 9/10 minimum")
4. Build the loop: generate, score against checklist, diagnose failures, rewrite, re-score; do not stop until every criterion passes
5. Add adversarial pressure: give Claude a persona that attacks the output (skeptical customer, competitor, distracted buyer). If the output survives the attack, it ships
6. Save as a reusable skill

**Demonstrated applications:** image ad concepts (scored against 10 criteria), email drip sequences, video hooks (retention psychology), positioning (competitive stress-test), SEO content (competitive gap analysis).

This extends the two-pass pattern (see [Write Like a Human](#write-like-a-human-two-pass-skill)) into an N-pass loop with explicit quality gates and adversarial testing.

### Obsidian Skills Pack

- Community skill pack (`github.com/kepano/obsidian-skills`) teaching Obsidian-specific formats: Obsidian Flavored Markdown (wikilinks, callouts, embeds), JSON Canvas (.canvas), Obsidian Bases (.base database views)
- Installation: clone into `.claude/` at vault root; Claude auto-detects on session start
- Key distinction: MCP tools = file operations; skills = domain expertise and workflows

*Source: Obsidian Skills Pack.md*

### Marketing SOP Skills: Domain-Specific Skill Library

- Conversion Factory published 25 marketing skills on GitHub: copywriting, programmatic SEO, email sequences, A/B testing, analytics, competitor analysis, pricing strategy, referral programs
- Pattern: professional SOPs refined over years converted into reusable Claude Code skills, reducing execution from weeks to minutes

*Source: Opus 4.6 Replaces a $120K Marketing Agency.md*

### /humanizer Skill: AI Writing Detection Removal

- Open-source Claude Code skill that removes signs of AI-generated writing from text
- Uses 24 detection patterns to identify and rewrite AI tells
- Usage: type `/humanizer` and paste text
- GitHub: https://github.com/blader/humanizer
- Relevant for any workflow where AI-generated content needs to pass as human-written (marketing copy, blog posts, client communications)
- Author: @dr_cintas (also publishes daily AI tutorials at simplifyingai.co)

*Source: Twitter Bookmarks/Thread by @dr_cintas.md*

*Source: Twitter Bookmarks/2026-03-07-bcherny-loop-skill-release.md*

### GSD Command Suite: Spec-Driven Development Lifecycle

Get Shit Done (GSD) is a 30+ command reference implementation of spec-driven development lifecycle management, installable via `npx get-shit-done-cc@latest` and compatible with Claude Code, OpenCode, Gemini CLI, and Codex.

**Core workflow:** `/gsd:new-project` (init with questions, research, requirements, roadmap), `/gsd:discuss-phase` (capture implementation preferences before planning), `/gsd:plan-phase` (research + plan + verify loop), `/gsd:execute-phase` (parallel wave execution), `/gsd:verify-work` (manual UAT with auto-diagnosis).

**Model profile system:** Three profiles (quality/balanced/budget) assign per-agent model tiers across 11 specialized agents. Planning gets Opus; execution gets Sonnet; verification gets Haiku on budget. Quick switch via `/gsd:set-profile`.

**Brownfield support:** `/gsd:map-codebase` spawns parallel agents to analyze stack, architecture, conventions, and concerns before project init.

**Session management:** `/gsd:pause-work` and `/gsd:resume-work` for explicit context handoff. `/gsd:progress` for status checks. `/gsd:quick` handles ad-hoc tasks with GSD guarantees (atomic commits, state tracking) but without research/plan-checker overhead.

**Phase management:** Add, insert, remove phases mid-milestone. `/gsd:plan-milestone-gaps` creates phases for audit-discovered gaps. Plans are structured as XML optimized for Claude (`<task type="auto">` with name, files, action, verify, done fields).

(see [workflow-patterns.md](workflow-patterns.md) for the GSD wave execution pattern)

---

## Slash Commands

### Built-In Commands Quick Reference

| Command | What It Does |
|---|---|
| `/help` | List all available slash commands |
| `/init` | Analyze codebase, generate or update CLAUDE.md |
| `/clear` | Reset conversation and context completely |
| `/compact [topic]` | Compress conversation history; optional topic focus |
| `/config` | Open settings interface |
| `/model` | Switch between Opus, Sonnet, Haiku |
| `/permissions` | View and update tool permissions |
| `/output-style` | Configure response formatting verbosity |
| `/privacy-settings` | Control data sharing |
| `/export [filename]` | Export conversation to file or clipboard |
| `/rewind` | Go back to an earlier conversation point |
| `/context` | Check context window usage |
| `/todos` | View tracked action items |
| `/review` | Review recent code changes (quality, security, tests) |
| `/hooks` | Configure lifecycle hooks interactively |
| `/cost` | Show token usage and estimated cost |
| `/memory` | Quick-add notes to CLAUDE.md (`#` shortcut does the same) |
| `/install-github-app` | Set up automatic PR reviews by Claude |

### Creating Custom Commands

Custom commands are markdown files in `.claude/commands/` (project) or `~/.claude/commands/` (personal). The filename becomes the command name.

```
.claude/commands/
├── audit.md           # Creates /audit
├── frontend/
│   └── test.md        # Creates /test (project:frontend)
└── backend/
    └── test.md        # Creates /test (project:backend)
```

### Arguments

Use `$ARGUMENTS` for all arguments, or `$1`, `$2` for positional params:

```markdown
<!-- .claude/commands/fix-issue.md -->
---
allowed-tools: Read, Grep, Glob, Bash(git diff:*)
description: Fix a GitHub issue
argument-hint: <issue-number>
---
Fix issue #$1 following our coding standards. Verify the fix with tests.
```

Usage: `/fix-issue 123`

### Commands Frontmatter Reference

Commands (`.claude/commands/<name>.md`) have minimal frontmatter:

| Field | Type | Required | Description |
|---|---|---|---|
| `description` | string | Recommended | Short description shown in autocomplete |
| `model` | string | No | Model override for this command |

Template variables: `${ARGUMENTS}`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_PROJECT_DIR}`.

Commands are lightweight entry points. For complex workflows, delegate to agents with skills (see [Skill vs Agent vs Command Comparison](#skill-vs-agent-vs-command-comparison)).

### Extended Command Frontmatter and Dynamic Patterns

Command-specific frontmatter fields and dynamic patterns beyond the basic `description`/`model` documented in the [Commands Frontmatter Reference](#commands-frontmatter-reference):

- **`allowed-tools`** in commands: same tool scoping syntax as skills -- `Bash(git:*)` allows only git subcommands; `Bash(npm run *)` allows npm scripts; `Edit(/docs/**)` restricts edits to docs directory (see also [Practical Workflow Tips](tools-and-integrations.md#practical-workflow-tips-from-production-use) for `/permissions` wildcard syntax)
- **`disable-model-invocation`** for commands: prevents Claude from auto-triggering the command; user must explicitly type `/command-name`
- **`@$1` file reference:** `@` prefix combined with positional args injects file content into the command prompt -- `@$1` reads the file path from the first argument
- **`$IF()` conditional:** conditionally include command sections based on whether arguments or environment variables are present
- **`${CLAUDE_PLUGIN_ROOT}`:** resolves to the plugin's installation directory at runtime, enabling portable file references across different machines
- **Multi-component orchestration:** commands can chain to agents with preloaded skills for sophisticated workflows -- the command handles user interaction and setup, then delegates execution to a specialized agent

*Source: claude-plugins-official/plugins/plugin-dev/skills/command-development/SKILL.md*

### AskUserQuestion Tool: Interactive Command Input

Commands can gather structured user input via the `AskUserQuestion` tool before proceeding:

- **JSON schema:** `{ "questions": [{ "header": "Section Title", "multiSelect": true, "options": [{ "label": "Option Name", "description": "What it does" }] }] }`
- **Use case:** bootstrap commands that create configuration files (e.g., `.claude/plugin.local.md`) based on user selections
- **Pattern:** present options -> collect selections -> generate file content from selections -> write configuration
- Enables non-linear command flows where user input determines subsequent behavior, replacing the "ask one question at a time" approach with a structured multi-select interface

*Source: claude-plugins-official/plugins/plugin-dev/skills/plugin-settings/examples/create-settings-command.md*

### Pre-Command Bash Execution

Commands can run shell commands before Claude processes the prompt. Use `!` backtick syntax after the `---` separator:

```markdown
---
description: Review recent changes
---
!`git diff --name-only HEAD~1`
!`git diff HEAD~1`

Review the above changes for code quality and security issues.
```

### Expanded Slash Commands Reference

**Session management:** `/rename`, `/resume`, `/fork`, `/teleport` (resume remote session from claude.ai)

**Context & cost:** `/context` (visualize context usage as colored grid), `/usage` (plan limits, subscription only), `/stats` (daily usage, streaks, model preferences)

**Model & planning:** `/plan` (read-only planning mode), `/fast` (same Opus 4.6 with faster output)

**Extensions:** `/agents` (manage subagents), `/skills` (view available skills), `/hooks` (interactive hook management), `/mcp` (manage MCP servers), `/plugin` (manage plugins, browse marketplaces), `/ide` (connect to IDE)

**Configuration:** `/keybindings` (customize keyboard shortcuts), `/terminal-setup` (shift+enter for newlines), `/vim` (vim editing mode), `/statusline` (status line UI), `/sandbox` (configure sandboxing)

**Diagnostics:** `/doctor` (health check), `/debug [description]` (troubleshoot via debug log), `/tasks` (background tasks), `/feedback` (generate GitHub issue URL)

**Input prefixes:** `!` (bash mode -- run shell commands directly), `@` (file path autocomplete)

**Dynamic commands:** MCP prompts appear as `/mcp__<server>__<prompt>`, plugins as `/plugin-name:command-name`, skills as `/skill-name`.

### /simplify and /batch: Built-in PR Lifecycle Skills

Two official Claude Code skills (announced by Boris Cherny, Anthropic) targeting the gap between writing code and shipping code.

- **/simplify** uses parallel agents to improve code quality, tune efficiency, and ensure CLAUDE.md compliance. Designed to run after every coding task. Can be triggered automatically via PostToolUse hooks after code changes -- structural coaching without manual invocation
- **/batch** enables parallel code migrations across isolated git worktrees. Each subagent gets a folder, tests its work, then puts up a PR. Designed for highly parallelizable tasks without file conflicts. If tasks overlap files, the main agent must resolve conflicts manually after subagents complete

(see [workflow-patterns.md](workflow-patterns.md) for parallel execution patterns)

### /loop Skill: Built-in Recurring Task Scheduling

- Built-in skill (not a command or plugin) for scheduling recurring tasks up to 3 days
- Examples: PR babysitting with auto-fix, Slack morning briefings via MCP, periodic performance monitoring
- Available in v2.1.71+; works on desktop app
- 3-day limit is intentional design constraint -- context management, cost control, and failure recovery all get exponentially harder beyond that window
- Power users chain multiple skills within a loop: `/posthog` -> `/vercel-analysis` -> `/simplify` -> `/batch` -> `/ship`
- Replaces manual cron + orchestration glue (one user: "I can kill 300 lines of orchestration glue and get retry logic for free")
- Related: agents move closer to continuous background workers rather than one-off assistants (see [workflow-patterns.md](workflow-patterns.md#pattern-2-the-ralph-loop-autonomous-coding))

*Source: Twitter Bookmarks/2026-03-07-bcherny-loop-skill-release.md*

### /btw: Side Questions During Active Work

- Built-in Claude Code command for quick questions without adding to conversation history
- Available while Claude is working -- runs independently, does not interrupt the main turn
- **No tool access:** Answers only from what is already in context (cannot read files, run commands, or search)
- Single response, no follow-ups. Low cost -- reuses parent conversation's prompt cache
- `/btw` is the inverse of a subagent: it sees your full conversation but has no tools, while a subagent has full tools but starts with empty context (see [agent-design.md](agent-design.md#subagents-in-claude-code) for subagent mechanics)
- Built by @ErikSchluntz at Anthropic as a side project

*Sources: Twitter Bookmarks/2026-03-10-trq212-a-bit-more-on-the-technical-details-this-cannot-do-any-tool.md, Twitter Bookmarks/2026-03-10-trq212-we-just-added-btw-to-claude-code-use-it-to-have-side-chain-c.md*

### Instinct-Based Learning: Continuous Learning v2

A next-generation learning system replacing session-level skill extraction with atomic "instincts" -- small learned behaviors with confidence scoring and an evolution pipeline.

**Instinct model:** Each instinct has one trigger, one action, a confidence score (0.3-0.9), a domain tag (code-style, testing, git, workflow), and an evidence trail. Atomic by design -- no compound behaviors.

**Confidence scoring:**

| Score | Behavior |
|---|---|
| 0.3 | Tentative -- suggested only |
| 0.5 | Moderate -- applied when relevant |
| 0.7 | Strong -- auto-approved |
| 0.9 | Near-certain -- core behavior |

Confidence increases with repeated observation, decreases on user correction or inactivity. Configurable decay rate.

**Hooks over skills for observation:** v1 relied on skills (~50-80% fire rate based on Claude's judgment). v2 uses PreToolUse/PostToolUse hooks -- 100% deterministic, every tool call observed, no patterns missed (see [tools-and-integrations.md](tools-and-integrations.md#hooks-prepost-tool-automation) for hook types).

**Observer architecture:** A background agent (Haiku) reads `observations.jsonl`, detects patterns (user corrections, error resolutions, repeated workflows, tool preferences), and creates/updates instincts on a configurable interval (default 5 min).

**Evolution pipeline:** `/evolve` clusters related instincts (threshold: 3+) into full skills, commands, or agents stored in `~/.claude/homunculus/evolved/`. Instincts are the raw material; skills are the refined output. `/instinct-export` and `/instinct-import` enable team knowledge transfer (only patterns are shared -- no code or conversation content).

**Directory structure:** `~/.claude/homunculus/` with `instincts/personal/`, `instincts/inherited/`, `evolved/{agents,skills,commands}`, `observations.jsonl`. Backward compatible with existing `~/.claude/skills/learned/` from v1.

(see [context-engineering.md](context-engineering.md#dynamic-system-prompt-injection-via-cli-aliases) for hook-based learning rationale)

---


