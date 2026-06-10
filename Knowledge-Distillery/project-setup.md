# Project Setup & Configuration

How to go from zero to a fully configured Claude Code project. Covers the thinking you do before touching code, the files Claude reads on every session, and the directory conventions that keep everything organized.

---

## The 8 Kickoff Questions

Before writing a line of code or a single prompt, answer these. They form the spec that every later decision traces back to.

### Understanding the Project

1. **What does this project do in one sentence?** -- Forces clarity. If you cannot say it in one sentence, the scope is not defined yet.
2. **Who uses this, and what do they need?** -- Identifies the audience and their core requirements.
3. **What technologies is it built with?** -- Tech stack dictates file structure, tooling, and which MCP servers matter.
4. **Where is the main entry point?** -- The file or command where execution begins. Claude needs this to orient itself.

### Understanding the Work

5. **What needs to be done?** -- The task list, feature set, or bug report.
6. **What does "done" look like?** -- Acceptance criteria, test conditions, or a visual reference. Without this you cannot verify. (see [prompt-engineering.md#spec-driven-development](prompt-engineering.md#spec-driven-development))
7. **What constraints do I need to work within?** -- Deadlines, backward compatibility, performance budgets, forbidden dependencies.
8. **What could go wrong?** -- Failure modes, security concerns, data loss risks. Name them now so Claude can avoid them.

### After the Questions: Plan

Decide on approach and execution order before implementation. What should we build first to validate the approach? Break work into manageable steps. Prompt to use: *"Based on that, let's plan the implementation. What order should we tackle this?"*

---

## Day-Zero Workflow

### Step 1: Run /init

```bash
cd your-project && claude
/init
```

`/init` scans package files, config, docs, and code structure, then generates a starter `CLAUDE.md` with detected build commands, architecture, key directories, and conventions. If one already exists, it suggests improvements instead. Treat the output as a draft -- it captures obvious patterns but misses team-specific nuance.

### Step 2: Review and Customize CLAUDE.md

After `/init`, immediately: verify commands are correct, add workflow instructions Claude could not infer (branch naming, deployment, review requirements), remove generic guidance that does not apply, and reference critical files explicitly (schemas, API contracts). Commit to version control so the team benefits.

Use the `#` shortcut inside a session to append notes to `CLAUDE.md` in natural language. Over time these accumulate into a file that reflects how the team actually works. (see [context-engineering.md#claudemd-your-always-loaded-memory](context-engineering.md#claudemd-your-always-loaded-memory))

### Step 3: Configure Settings (settings.json)

Create or edit `.claude/settings.json` for project-level config shared with the team. Use `.claude/settings.local.json` for personal overrides.

```json
{
  "permissions": {
    "allowedTools": ["Read", "Write", "Bash(git *)", "Bash(npm *)"],
    "deny": ["Read(./.env)", "Read(./.env.*)", "Write(./production.config.*)"]
  }
}
```

Key patterns: **allowedTools** whitelists tools/command prefixes so Claude does not prompt on routine operations. **deny** blacklists sensitive files. **hooks** automate post-edit checks like formatters or type checkers. (see [tools-and-integrations.md#hooks-prepost-tool-automation](tools-and-integrations.md#hooks-prepost-tool-automation))

### Step 4: Set Up MCP Servers (.mcp.json)

MCP (Model Context Protocol) servers extend Claude with external capabilities: browser automation, error tracking, GitHub operations, databases.

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "your-token-here" }
    }
  }
}
```

Place `.mcp.json` at project root. Use `--mcp-debug` to troubleshoot. Document MCP usage guidance in `CLAUDE.md` so Claude knows *when* and *how* to use each server. (see [mcp-servers.md](mcp-servers.md))

### Local-First Development: Docker + Ollama Setup Pattern

- Beginner-documented path from zero to running local AI tools: enable VM/SVM in BIOS, install Docker, clone repo, configure API keys, compose containers, open ports
- Key lesson: the gap between "download this repo" and "it actually runs" involves BIOS settings, Docker networking, port configuration, and model pulling -- none in most README instructions
- Docker Compose as deployment unit: services in `docker-compose.yml`, env vars pointing to local Ollama (`http://host.docker.internal:11434`), persistent volumes
- Model setup is separate from app setup: `ollama pull [model]` + configure app to reference model names
- Same skills needed for MCP server configuration and local tool integration (see [project-setup.md](#step-4-set-up-mcp-servers-mcpjson))
*Source: Old-Notes/Open Notebook.md*

### Claude Code Setup for Non-Technical Users

- CLAUDE.md as "memory file": after a first session, prompt Claude to "create a CLAUDE.md file and write down everything you've learned about this project: folder structure, design choices, preferences"
- Prompt as project manager, not engineer: describe the end result, not the steps; give the brief, let Claude be the developer
- Loop-breaking pattern: when Claude enters a fix-creates-bug spiral, type "Stop. Explain what's going wrong. Give me 2 different approaches." Forces diagnosis before the next attempt
- Start small, iterate: one deliverable per prompt, one screen at a time
*Source: 2026-03-19-rubenhassid-httpstcolmdv0axswg.md*

### Step 5: Create First Custom Commands (.claude/commands/)

Identify prompts you repeat and convert them to slash commands stored as markdown files.

```bash
mkdir -p .claude/commands
```

Example -- `.claude/commands/review.md`:
```markdown
---
allowed-tools: Read, Grep, Glob, Bash(git diff:*)
description: Review recent changes
---
!`git diff --name-only HEAD~1`
!`git diff HEAD~1`

Review the above changes for code quality, security issues, and performance concerns.
```

Commands support `$ARGUMENTS` for freeform input or `$1`, `$2` for positional args. Available in `/` autocomplete after restart.

---

## CLAUDE.md Templates

### Minimal Starter (~10 lines)

For simple projects or early prototypes. Cover the essentials and nothing more.

```markdown
# Project: [name]
[One-sentence description]

## Tech Stack
[Language, framework, database, key libraries]

## Commands
[build, dev, test, lint -- one code block]

## Entry Point
[Main file or startup command]

## Notes
[One or two project-specific gotchas]
```

### Full Operating Manual (~18 sections)

For production codebases that benefit from comprehensive guardrails. Each section header below is a slot -- fill only the ones that matter to your project.

| # | Section | What goes in it |
|---|---------|-----------------|
| 1 | Workflow Orchestration | When to use plan mode, thinking mode, or both |
| 2 | Parallelism & Isolation | Subagent strategy, git worktree patterns |
| 3 | Verification Before Done | Required proof steps: tests, logs, diffs |
| 4 | Demand Elegance | When to pause and ask for a better solution |
| 5 | Autonomous Bug Fixing | Expectations for end-to-end bug resolution |
| 6 | Self-Improvement Loop | How to capture lessons from corrections |
| 7 | Task Management Protocol | Checklist-driven execution order |
| 8 | Prompting Standards | Challenge/review mode, specification quality |
| 9 | Skills & Reuse | When to promote repeated tasks to commands/skills |
| 10 | Data & Analytics | How to use available CLIs, MCPs, or APIs |
| 11 | Learning & Explanation Mode | Output style preferences (diagrams, walkthroughs) |
| 12 | Terminal & Environment Awareness | Branch display, shell conventions |
| 13 | Documentation Spine | Required summary docs and navigation order |
| 14 | Self-Modification Rules | When Claude may edit CLAUDE.md itself |
| 15 | Tests, CI & Databases | Do not assume they exist; ask before introducing |
| 16 | Hooks & Automation | Recommended hooks and when they apply |
| 17 | Pull Request Behavior | Auto-PR rules, summary requirements, merge gating |
| 18 | Final Principles | Simplicity first, no laziness, minimal impact |

### CLAUDE.md Discipline: Core Principles

- CLAUDE.md should be a logical nested directory of IF-ELSE pointers to context files, not a giant rules dump; keep it barebones: "if doing X, read rules/X.md"
- Separate research from implementation in distinct agent sessions: give a fresh-context agent the specific implementation rather than "build an auth system"
- Define task completion explicitly: agents know how to start but not stop; tests are ideal endpoints (deterministic pass/fail); TASK_CONTRACT.md specifying required tests, screenshots, and verifications prevents premature termination
- New session per contract beats 24-hour running sessions: long sessions force context bloat from unrelated contracts
- Rules and Skills are the core primitives: rules encode preferences/prohibitions, skills encode recipes; periodically have the agent consolidate and remove contradictions from both
*Source: 2026-03-03-systematicls-httpstcowbakpai5vl.md*

### CLAUDE.md as Collaboration Contract

- CLAUDE.md is a collaboration contract: include build/test/lint commands, key directory structure, NEVER list, and Compact Instructions; exclude vague principles and large background materials
- Treat CLAUDE.md as starting empty: add entries only when you catch yourself repeating the same instruction; after correcting a mistake, immediately add "update your CLAUDE.md so you don't make that mistake again"
- Context cost reality: 5 MCP servers at ~200 tokens/tool definition = ~25k tokens consumed in fixed overhead before any task work
- Skills frequency rule: >1/session = keep auto-invoke + optimize descriptor; <1/session = disable auto-invoke; <1/month = remove and document in AGENTS.md
- HANDOFF.md pattern: before ending a session, have Claude record what it tried, what worked, what failed, and what comes next
- Verification test: "if you can't clearly articulate what 'done' looks like, the task is not ready for autonomous execution"
(see [context-engineering.md](context-engineering.md) for context window budgeting)
*Source: 2026-03-15-HiTw93-httpstcopec3y6sswl.md*

### CLAUDE.md Hierarchy: Project vs User vs Directory Level

- CLAUDE.md hierarchy: user-level (~/.claude/CLAUDE.md, NOT version-controlled), project-level (.claude/CLAUDE.md), directory-level (subdirectory files)
- Common trap: instructions in user-level config are not shared with team members -- anything team-wide must be at project level
- Path-specific rules (.claude/rules/ with YAML frontmatter glob patterns) apply conventions across the entire codebase; directory-level CLAUDE.md cannot do this because it is directory-bound
*Source: 2026-03-15-hooeem-httpstco4tchgza4oc.md*

### COMP System: Four-File Project Architecture

- COMP system: 4 project files -- CLAUDE.md (AI behavior), ORIENT.md (human onboarding), MEMORY.md (accumulated decisions/gotchas), PLAN.md (roadmap/progress); each has different audience and update frequency
- Orchestrator-first pattern: the session agent decides whether to handle directly, delegate to subagent, or route to MCP; never start coding before this decision
- Dialectic review pattern: spawn opposing agents (Hunter argues FOR, Skeptic argues AGAINST, Referee synthesizes) instead of asking one agent for pros/cons; anti-sycophancy by design
- Evals before specs: the progression is evals → spec → plan → implement → verify; define success measurement before writing the spec
- Structured over prose for mandatory rules: use XML and JSON in CLAUDE.md, not markdown paragraphs; Claude processes tagged content differently from prose
- Test-first bug fixing: write a test that reproduces the bug before any fix; operationalize every fix (write tests for the whole class, check for other instances, update CLAUDE.md if a gap is revealed)
- Progressive disclosure in CLAUDE.md: keep it lean with trigger rules ("when X happens, read guide Y"); guides load on-demand rather than all upfront
*Source: 2026-03-24-GriffinHilly-httpstcohwymfzk7ob.md*

### CLAUDE.md Size and Subagent Template Practices

- Keep CLAUDE.md under 200 lines; overflow into `.claude/rules/` with YAML frontmatter for path-matched loading; CLAUDE.md hierarchy (priority): managed/enterprise → project → user → rules/; array-valued settings (permissions) MERGE across scopes rather than replace
- Three subagent templates: explorer (read-only, no file writes), planner (read-only), executor (full capabilities) -- explicit tool allowlists required; a "read-only description" does not restrict tool access
- 6-persona subagent testing: Skeptical Staff Engineer, Security Reviewer, New Maintainer, Heavy CLI User, Operator/SRE, Docs-First Newcomer -- spin up all 6 before shipping; found 5 critical issues in 15 minutes that 2 weeks of personal use missed
- MCP overhead is real: each server adds 100-500+ tokens to context; run 2-3 max per project, disable when not needed
- Hooks enforce rules as code, not suggestions: PreToolUse can block; PostToolUse cannot (already ran); auto-inject important instructions after /compact via hook to prevent loss
- Auto-learning rules: nightly cron extracts behavioral patterns into CLAUDE.md; only style preferences can be automated; core safety rules must be handwritten and human-reviewed
- Plan Mode + Ctrl+G: edit the plan in your editor before execution; changing a plan takes one sentence, changing half-written code takes 10x longer
- Git worktrees for zero-risk experiments: each branch gets its own working directory; Claude can do anything in the experiment worktree, main stays untouched
*Source: 2026-03-25-Voxyz_ai-httpstcobjkuc3rtsc.md*

### Onboarding Document Generator Pattern

- Five-section structure for new contributor onboarding: What is this? How is it organized? Key concepts/abstractions? Primary flow? Where do I start?
- Always regenerate from scratch -- reading old doc to update it means doing two jobs (understand codebase + fact-check old doc); slower and more error-prone than regenerating
- Human-first writing -- clear prose, not agent-formatted structured data; agent utility is a side effect of clear prose
- No design rationale inference -- the creator may not know, and presenting guesses as fact is worse than silence
- Inline linking to existing docs within relevant sections, not a references appendix
*Source: compound-engineering-plugin/docs/brainstorms/2026-03-25-vonboarding-skill-requirements.md*

### Self-Improving Rules Pattern

- After completing each subtask, review code changes and chat history to identify new patterns; create or update rules files when a pattern appears in 3+ files or when code reviews repeat the same feedback
- Rule triggers: new technology used consistently, common bugs that could be prevented, emerging conventions, deprecated patterns to retire
- Rule quality checks: actionable and specific, examples from actual codebase, references current, patterns consistently enforced
- Deprecation: mark outdated patterns, document migration paths, remove rules that no longer apply
*Source: claude-task-master/.kiro/steering/self_improve.md*

### Rules-Extracted Coding Standards as AGENTS.md Topic Guides

- Store distilled coding rules in `agent_docs/` topic files (api-design, code-simplification, documentation, index) referenced from AGENTS.md -- rules are tagged with IDs for traceability to PRs
- Rules are extracted from PR review patterns and annotated with reasoning: what to do, why it prevents a problem, what the alternative looks like
- Three-tier knowledge structure: AGENTS.md (entry point) → agent_docs/index.md (coding guidelines) → agent_docs/topic-guides (domain-specific rules) -- hierarchical, load-on-demand
- AGENTS.md declares which sub-AGENTS.md files to load per directory -- directory-scoped instructions prevent context bloat
*Source: pydantic-ai/AGENTS.md, pydantic-ai/agent_docs/index.md*

### AGENTS.md Multi-Layer Instructions Pattern

- Root-level CLAUDE.md for project overview + directory-specific AGENTS.md files for each submodule -- instructions scoped to the code context being edited
- AGENTS.md explicitly specifies preferred tools: e.g., prefer `rg` for searches (faster under CLI harness), use `apply_patch` for single-file edits
- Makefile as canonical entry point: all setup stages invoked via `make` targets -- resolves platform compatibility issues (e.g., Bash 4+) that bare scripts would expose
- For automation: prefer wrapper scripts over bare tool invocations -- scripts have fallback chains through multiple Python installations
- Never use destructive git commands without explicit user confirmation -- state this as an invariant in AGENTS.md
*Source: LightRAG/AGENTS.md*

---

## File Locations Quick Reference

| File / Directory | Purpose | Scope |
|------------------|---------|-------|
| `CLAUDE.md` | Project memory and behavioral constitution | Project (shared, committed) |
| `CLAUDE.local.md` | Personal project notes | Project (personal, gitignored) |
| `~/.claude/CLAUDE.md` | Global context for all projects | User-wide |
| `.claude/settings.json` | Project configuration (permissions, hooks) | Project (shared, committed) |
| `.claude/settings.local.json` | Personal config overrides | Project (personal, gitignored) |
| `~/.claude/settings.json` | User-wide configuration | User-wide |
| `.claude/commands/` | Custom slash commands | Project (shared) |
| `~/.claude/commands/` | Personal slash commands | User-wide |
| `.claude/agents/` | Subagent definitions | Project |
| `~/.claude/skills/` | Skill bundles (prompt + scripts) | User-wide |
| `.mcp.json` | MCP server configuration | Project |

In monorepos, parent-directory `CLAUDE.md` files load automatically; child-directory files are pulled on demand.

---

## Settings.json Patterns

### Settings Precedence: Five-Level Override Hierarchy

User-writable settings apply in this override order (highest to lowest):

| Priority | Location | Scope | Version Controlled |
|----------|----------|-------|-------------------|
| 1 | Command line flags | Session | N/A |
| 2 | `.claude/settings.local.json` | Project | No (git-ignored) |
| 3 | `.claude/settings.json` | Project | Yes (committed) |
| 4 | `~/.claude/settings.local.json` | User | N/A |
| 5 | `~/.claude/settings.json` | User | N/A |

Policy layer: `managed-settings.json` is organization-enforced and cannot be overridden. `deny` rules have highest safety precedence -- they cannot be overridden by lower-priority allow/ask rules. (see [context-engineering.md](context-engineering.md))

### Permission Configuration

```json
{
  "permissions": {
    "allowedTools": ["Read", "Write", "Bash(git *)", "Bash(npm test *)"],
    "deny": ["Read(./.env)", "Read(./.env.*)"]
  }
}
```

- Wildcards supported: `Bash(npm *)` allows any npm command.
- `deny` overrides `allowedTools` -- use it for secrets and production configs.
- MCP tool auto-approve: add `MCP__[servername]` entries to `allowedTools`.

### Permission System: Full Structure

The complete permission structure:

```json
{
  "permissions": {
    "allow": [],
    "ask": [],
    "deny": [],
    "additionalDirectories": [],
    "defaultMode": "acceptEdits",
    "disableBypassPermissionsMode": "disable"
  }
}
```

**Permission modes:** `default`, `acceptEdits`, `askEdits`, `viewOnly`, `bypassPermissions`, `plan`.

**Tool permission syntax (comprehensive):**

| Tool | Syntax | Examples |
|---|---|---|
| `Bash` | `Bash(pattern)` | `Bash(npm run *)`, `Bash(* install)`, `Bash(git * main)` |
| `Read` | `Read(path)` | `Read(.env)`, `Read(./secrets/**)` |
| `Edit`/`Write` | `Edit(path)` | `Edit(src/**)`, `Write(*.md)` |
| `WebFetch` | `WebFetch(domain:pattern)` | `WebFetch(domain:example.com)` |
| `Task` | `Task(agent-name)` | `Task(Explore)`, `Task(my-agent)` |
| `Skill` | `Skill(skill-name)` | `Skill(weather-fetcher)` |
| `MCP` | `mcp__server__tool` | `mcp__memory__*` |

Wildcard `*` works at any position. `Bash(*)` = `Bash` (matches all). Rules support output redirections.

### Environment Variables

Set `env` inside `.mcp.json` per server. Never put API keys in `CLAUDE.md` or `settings.json` -- those files are committed to source control.

### Model Override

Use `"model": "claude-sonnet-4-20250514"` in settings, or switch interactively with `/model`. Opus for complex reasoning, Sonnet for everyday dev, Haiku for fast simple tasks.

### Complete Settings Reference

Additional settings groups beyond the hierarchy and permissions documented above:

**Core settings:**

| Key | Type | Default | Description |
|---|---|---|---|
| `model` | string | `"default"` | Model override. Aliases: `sonnet`, `opus`, `haiku`, `sonnet[1m]`, `opusplan` |
| `agent` | string | - | Default agent for main conversation (also `--agent` CLI flag) |
| `language` | string | `"english"` | Claude's response language |
| `cleanupPeriodDays` | number | `30` | Session cleanup threshold |
| `autoUpdatesChannel` | string | `"latest"` | `"stable"` or `"latest"` |
| `alwaysThinkingEnabled` | boolean | `false` | Extended thinking by default |
| `skipWebFetchPreflight` | boolean | `false` | Skip WebFetch blocklist check |
| `plansDirectory` | string | `.claude/plans/` | Where `/plan` outputs are stored |

**Attribution:** `attribution.commit` and `attribution.pr` customize commit/PR messages. Set to `""` to hide entirely. `includeCoAuthoredBy` is deprecated.

**Auth helpers:** `apiKeyHelper` (script outputting auth token), `forceLoginMethod` (`"claudeai"` or `"console"`), `forceLoginOrgUUID` (auto-select org during login).

**Company announcements:** `companyAnnouncements` array of strings cycled randomly at startup.

### Model Configuration: Effort Level

Opus 4.6 exposes an effort level via `/model` (arrow keys) or `CLAUDE_CODE_EFFORT_LEVEL` env var:

| Level | Description |
|---|---|
| High (default) | Full reasoning, complex tasks |
| Medium | Balanced, everyday tasks |
| Low | Minimal reasoning, fastest |

Only available for Opus 4.6; other models do not expose this control.

### Sandbox Configuration

| Key | Type | Default | Description |
|---|---|---|---|
| `sandbox.enabled` | boolean | `false` | Enable bash sandboxing |
| `sandbox.autoAllowBashIfSandboxed` | boolean | `true` | Auto-approve bash when sandboxed |
| `sandbox.excludedCommands` | array | `[]` | Commands outside sandbox |
| `sandbox.network.allowedDomains` | array | `[]` | Network domain allowlist |
| `sandbox.network.deniedDomains` | array | `[]` | Network domain denylist |
| `sandbox.network.allowLocalBinding` | boolean | `false` | Bind to localhost (macOS) |
| `sandbox.network.allowUnixSockets` | array | `[]` | Specific Unix socket paths |

Additional: `ignoreViolations` (suppress specific violations), `enableWeakerNestedSandbox` (Docker), `httpProxyPort`/`socksProxyPort` (custom proxy).

### Three-Level Claude Code Security Hardening Ladder
- **Level 1 (15 min, covers 90%):** `/sandbox` + `~/.claude/settings.json` with deny rules + `claude update`. Without sandbox, deny rules only block built-in tools -- bash commands bypass them entirely. Sandbox enables OS-level enforcement (Seatbelt on Mac, bubblewrap on Linux)
- **Level 2 (30 min):** Trail of Bits open-sourced their exact Claude Code security config: `github.com/trailofbits/claude-code-config`. Install via `claude plugin marketplace add trailofbits/skills`, then `/trailofbits:config`. Adds security checklists, workflow hooks, and forces plan-before-code + verify-before-ship discipline
- **Level 3 (1 hr, full isolation):** Trail of Bits devcontainer (`github.com/trailofbits/claude-code-devcontainer`). Claude runs inside a container with zero access to host machine -- no SSH keys, no cloud credentials, no filesystem outside the project. `bypassPermissions` enabled inside the container because the container IS the sandbox
- Key setting: `"enableAllProjectMcpServers": false` prevents cloned repos from auto-loading their MCP configs -- blocks the MCP config hijack attack vector
- Sample deny patterns: `Read(~/.ssh/**)`, `Read(~/.aws/**)`, `Read(~/.git-credentials)`, `Bash(curl *)`, `Bash(wget *)`, `Bash(ssh *)`, `Bash(git push *)`, `Read(*.env)`, `Read(.env.*)`
- Versions before 2.0.65 had two unpatched critical vulnerabilities -- run `claude update` monthly

(see [failure-patterns.md](failure-patterns.md#security-failure-patterns) for the attack vectors these settings defend against; see [Sandbox Configuration](#sandbox-configuration) for the full settings reference)

*Sources: 2026-04-08-noisyb0y1-httpstcoyvurya7dji.md, 2026-04-10-Axel_bitblaze69-some-important-claude-code-security-settings-you-need-to-tak.md*

### Display & UX Settings

| Key | Type | Description |
|---|---|---|
| `statusLine` | object | Custom status line (`type: "command"`, `command`, `padding`) |
| `spinnerVerbs` | object | Custom verbs with `mode` ("append"/"replace") and `verbs` array |
| `spinnerTipsOverride` | object | Custom tips array with optional `excludeDefault` |
| `outputStyle` | string | Response style (e.g., `"Explanatory"`) |
| `showTurnDuration` | boolean | Show turn duration |
| `respectGitignore` | boolean | Respect .gitignore in file picker |
| `fileSuggestion` | object | Custom file suggestion command |

Status line input fields: `workspace.added_dirs`, `context_window.used_percentage`, `current_usage`, `exceeds_200k_tokens`.

### Plugin and MCP Server Settings

**Plugins:** `enabledPlugins` (object), `extraKnownMarketplaces` (object), `strictKnownMarketplaces` (managed allowlist), `pluginConfigs` (per-plugin MCP configs keyed by `plugin@marketplace`).

**MCP servers:** `enableAllProjectMcpServers` (auto-approve all), `enabledMcpjsonServers` (allowlist), `disabledMcpjsonServers` (blocklist), `allowedMcpServers` / `deniedMcpServers` (managed, with name/command/URL matching).

### Claude Code Starter Settings and Memory Bank

- A published starter configuration with settings.json defaults and a structured memory bank for persisting context across Claude Code sessions is available as a reference implementation
- Covers the settings + memory bank setup pattern for bootstrapping new projects with persistent context from session one
*Source: 2026-03-27-tom_doerr-claude-code-starter-settings-and-memory-bank-system-httpstco.md*

---

## Directory Conventions

### .claude/commands/ (project slash commands)

Markdown files that become `/command-name` in the autocomplete menu. Shared via version control. Support front matter for tool restrictions, descriptions, and argument hints. Namespace with subdirectories (e.g., `frontend/test.md` and `backend/test.md`).

### .claude/agents/ (subagent definitions)

Markdown files defining specialized agents with specific roles, tools, and models. Claude invokes them automatically when tasks match their description, or you can request them explicitly.

### ~/.claude/ (personal/global config)

- `CLAUDE.md` -- instructions applied to every project.
- `settings.json` -- global permissions and preferences.
- `commands/` -- personal slash commands available everywhere.
- `skills/[skill-name]/SKILL.md` -- skill bundles pairing a prompt with helper scripts and templates. Unlike commands (invoked explicitly), skills are matched and invoked automatically based on task context. (see [skills.md#three-invocation-methods](skills.md#three-invocation-methods))

### Global-Only Features: What Cannot Live in .claude/

Several features exist only at `~/.claude/` and cannot be project-scoped:
- **Tasks** (`~/.claude/tasks/`) -- cross-session task lists, replacing old TodoWrite
- **Agent Teams** (`~/.claude/teams/`) -- multi-agent coordination configs (experimental)
- **Auto-memory** (`~/.claude/projects/<hash>/memory/`) -- Claude's self-written learnings per project (personal, never shared)
- **Credentials/OAuth** -- system keychain + `~/.claude.json`
- **Keybindings** (`~/.claude/keybindings.json`)

Design principle: coordination state, security state, and personal learning live globally. Configuration and workflow definitions live at both levels. Auto-memory is a notable hybrid: it is about a specific project but stored globally because it represents personal learning rather than team-shareable config.

### Anatomy of the .claude/ Folder

- Two .claude directories: project-level (.claude/ committed to git, team-shared) and global (~/.claude/ for personal preferences); settings.local.json auto-gitignored
- Hook exit codes: 0 = success, 1 = error but non-blocking (the most common mistake -- security hooks using exit 1 do nothing), 2 = blocks execution and sends stderr to Claude for self-correction. Always use exit 2 for security gates
- Stop hook infinite loop prevention: always check the stop_hook_active flag in the JSON payload; without this check, the hook blocks Claude indefinitely
- .claude/agents/ subagent personas: each has its own system prompt, tool access restrictions, and model preference; a security auditor needs only Read/Grep/Glob -- no Write access
- ~/.claude/projects/ stores session transcripts and auto-memory per project, browsable via /memory
*Source: 2026-03-21-akshay_pachaar-httpstcosssik3bx4z.md*

### Repo Documentation Taxonomy: Brainstorms/Plans/Solutions/Specs

- Layered documentation taxonomy: brainstorms (requirements exploration), plans (implementation plans + progress), solutions (documented decisions and patterns), specs (format specifications)
- Solution categories from the end-user perspective: developer-experience (local dev), integrations (cross-platform bugs), workflow/skill-design (plugin behavior)
- Pattern: keep these directories at `docs/brainstorms/`, `docs/plans/`, `docs/solutions/`, `docs/specs/` -- each has a clearly defined lifecycle and audience
*Source: compound-engineering-plugin/AGENTS.md*

### Context Scratch Space Convention

- Use `.context/<plugin-name>/<workflow-or-skill-name>/` for ephemeral collaboration artifacts (in-progress work, scratch space)
- Add per-run subdirectory when concurrent runs are plausible
- Clean scratch artifacts after successful completion unless user asked to inspect them or another agent still needs them
- Durable outputs (plans, specs, learnings, docs) do not belong in `.context/`
- `.context/` is gitignored; namespace under the plugin/tool identifier prevents collisions
*Source: compound-engineering-plugin/AGENTS.md*

---

## First Session Checklist

A repeatable routine for every new project:

- [ ] Answer the 8 kickoff questions
- [ ] `cd` into project root, run `claude`, then `/init`
- [ ] Review generated `CLAUDE.md` -- fix commands, add architecture notes, remove noise
- [ ] Reference critical files (schema, API contracts) explicitly in `CLAUDE.md`
- [ ] Create `.claude/settings.json` with `allowedTools` and `deny` patterns
- [ ] Create `.mcp.json` if external tools are needed (GitHub, Playwright, Sentry)
- [ ] Create `.claude/commands/` files for your most repeated prompts
- [ ] Commit `CLAUDE.md`, `.claude/settings.json`, `.mcp.json`, and commands to git
- [ ] Add `CLAUDE.local.md` and `.claude/settings.local.json` to `.gitignore`
- [ ] Start your first real task -- let friction surface what to add next

CLAUDE.md is a living document. Update it when you repeat instructions, when Claude makes a preventable mistake, or when the project structure changes.

### Terminal and Workflow Customization

Items to configure during project setup:
- `/config` for theme (light/dark)
- `/terminal-setup` for shift+enter newlines in IDE terminals, Apple Terminal, Warp, or Alacritty
- `/model` to set effort level (Low/Medium/High; High recommended)
- `/permissions` to pre-approve common tools; wildcard syntax supported (e.g., `Bash(bun run *)`, `Edit(/docs/**)`)
- `/sandbox` to enable file and network isolation
- `/statusline` to generate a custom status line from your shell config
- `/keybindings` to customize key mappings (live reload)
- Output styles via `/config`: Explanatory (learning a codebase), Learning (coaching mode), or Custom

### 50 Claude Code Configuration Tips

- CLAUDE.md has ~150-200 instruction budget before compliance degrades; every line must earn its place. Litmus test: "Would Claude make a mistake without this?" If no, delete it
- Use CLAUDE.md for suggestions, hooks for requirements -- CLAUDE.md compliance is ~80%, hooks are 100% deterministic
- After Claude makes a mistake, say "Update your CLAUDE.md so this doesn't happen again" -- Claude writes its own rule
- Two-session review pattern: first Claude implements, second Claude reviews from fresh context like a staff engineer who has no knowledge of implementation shortcuts
- /branch (/fork) creates a live copy of a conversation so both the risky and safe paths stay alive simultaneously
*Source: 2026-03-19-CodevolutionWeb-httpstcotxmjpjngdo.md*

### 40 Claude Code Best Practices: The Configuration Gap

- The gap between casual and power Claude Code users is configuration, not skill; properly configured saves 4-6 hours/week
- Three signal-to-noise improvements: /clear between unrelated tasks, after 2 failed corrections start fresh rather than correcting a third time, guide /compact with explicit preservation instructions
- ultrathink keyword on Opus 4.6 triggers adaptive reasoning budget allocation based on problem complexity
- /loop for background monitoring: /loop 5m check if deploy succeeded runs while session stays open; /permissions allowlist eliminates the per-command approval tax
- /sandbox provides OS-level isolation (Seatbelt/bubblewrap) for unsupervised experimental work
*Source: 2026-03-22-Suryanshti777-httpstcomhu0dgktzx.md*

### Compound Engineering Workflow

- /ce:plan before everything: run Compound Engineering's plan command at session start to force structured decomposition before any code is written
- 4-6 parallel sessions is the sweet spot for Compound Engineering; fewer than 4 leaves parallelism on the table; more than 6 creates coordination overhead
- bypassPermissions in settings.json: set for trusted projects to eliminate the per-command approval tax; use sparingly and only in projects you fully control
- Voice workflow: dictate tasks to Claude Code while doing other work; voice input with auto-transcription removes the typing bottleneck for longer task descriptions
- Compound Engineering plugin: EveryInc/compound-engineering-plugin -- extends Claude Code with /ce:plan, /ce:review, and related workflow commands
*Source: 2026-03-22-mvanhorn-httpstcoawabazttdp.md*

### Eight Claude Code Customizations for Power Users
- Shell alias `cc` with `--dangerously-skip-permissions` eliminates the per-command approval tax for experienced users who trust their project; additional aliases streamline common launch patterns
- Auto-compact threshold tuning: the default 95% triggers compaction too late, causing context loss at critical moments; set `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` to 60-75% for most tasks, 85% for context-heavy work where you need maximum window
- Compaction preservation instructions: add explicit notes to CLAUDE.md about what to maintain during compaction (active branch name, key decisions, current task state) so the agent doesn't lose critical context when the window compresses
- CLAUDE.md compliance is rule-dependent: specific, concise, actionable rules ("always run tests before committing") achieve ~89% compliance; vague instructions ("write clean code") hover around ~35%. This reinforces the existing CLAUDE.md ~150-200 instruction budget -- it is not just length that matters but specificity per rule
- Status line via shell script: displays current directory, git branch, and context usage color-coded by fill level (green/yellow/red), giving continuous visibility into how much context window remains
- PostToolUse hooks for auto-formatting: run Prettier or a linter automatically after every Edit/Write tool call; chain linters after formatter for consistent code quality without manual intervention

(see [50 Claude Code Configuration Tips](#50-claude-code-configuration-tips) for complementary settings; see [Key Environment Variables](#key-environment-variables) for `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` reference)

*Source: 2026-03-12-CodevolutionWeb-httpstcoqxb5hmsok3.md*

---

## CLI Startup Flags

Beyond the basic flags, the full set includes:

**Session:** `--continue` (`-c`), `--resume` (`-r`), `--from-pr`, `--fork-session`, `--session-id`, `--no-session-persistence`, `--remote`, `--teleport`

**Model:** `--model`, `--fallback-model` (auto-fallback when overloaded, print mode), `--betas` (beta headers)

**Permissions:** `--dangerously-skip-permissions`, `--allow-dangerously-skip-permissions`, `--permission-mode` (default/plan/acceptEdits/bypassPermissions), `--allowedTools`, `--disallowedTools`, `--tools` (restrict built-in tools; `""` disables all), `--permission-prompt-tool` (MCP tool for non-interactive permissions)

**Output:** `--print` (`-p`), `--output-format` (text/json/stream-json), `--input-format`, `--json-schema`, `--include-partial-messages`, `--verbose`

**System prompt:** `--system-prompt`, `--system-prompt-file`, `--append-system-prompt`, `--append-system-prompt-file`

**Agent:** `--agent`, `--agents` (JSON), `--teammate-mode` (auto/in-process/tmux)

**MCP/plugins:** `--mcp-config`, `--strict-mcp-config`, `--plugin-dir`

**Directory:** `--add-dir`, `--worktree` (`-w`)

**Budget (print mode):** `--max-budget-usd`, `--max-turns`

**Integration:** `--chrome` / `--no-chrome`, `--ide`

**Init:** `--init`, `--init-only`, `--maintenance`

**Debug:** `--debug` (category filter: `"api,hooks"`)

**Settings:** `--settings` (JSON file/string), `--setting-sources` (user/project/local), `--disable-slash-commands`

---

## Key Environment Variables

Notable env vars beyond the basics (`ANTHROPIC_API_KEY`, `ANTHROPIC_BASE_URL`, cloud flags):

| Variable | Description |
|---|---|
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | Auto-compact threshold (1-100). Default ~95%. Lower = earlier compaction |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` | Keep cwd between bash calls (`1`) |
| `CLAUDE_CODE_EFFORT_LEVEL` | Thinking depth: `low`, `medium`, `high` |
| `CLAUDE_CODE_SIMPLE` | Simple mode (Bash + Edit tools only) |
| `CLAUDE_BASH_NO_LOGIN` | Skip login shell for BashTool (`1`) |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` | Enable agent teams (`1`) |
| `CLAUDE_CODE_TMPDIR` | Override temp directory |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | Enable additional directory CLAUDE.md loading (`1`) |
| `MAX_THINKING_TOKENS` | Thinking token budget (`0` to disable) |
| `USE_BUILTIN_RIPGREP` | Set `0` to use system ripgrep (Alpine Linux) |
| `DISABLE_PROMPT_CACHING` | Disable all prompt caching (`1`). Model-specific variants also available |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` | Override file read token limit |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY` | Auto-exit SDK mode after idle duration (ms) |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET` | Override skill description char budget (see [skills.md](skills.md)) |

---

## Running Claude Code Locally with Open-Source Models

Claude Code can run entirely locally using Ollama as the model backend -- no API costs, no cloud data transmission, full privacy.

**Setup (4 steps):**
1. Install Ollama (runs quietly in background on Mac/Windows)
2. Pull a coding-focused model: `ollama run qwen2.5-coder:7b` (low RAM) or `qwen3-coder:30b` (high performance)
3. Set environment variables:
   - `ANTHROPIC_BASE_URL="http://localhost:11434"` (redirect to local Ollama)
   - `ANTHROPIC_AUTH_TOKEN="ollama"` (dummy API key)
   - `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` (opt out of telemetry)
4. Launch: `claude --model qwen2.5-coder:7b`

Claude Code reads files, edits code, and runs terminal commands using the local model. If previously logged into Anthropic, log out first so Claude switches to local mode.

**Use case:** developers wanting private/offline AI coding agents, open-source experimentation, environments where data cannot leave the machine.

---

## Usage, Rate Limits, and Extra Usage

- **`/usage`** -- check plan limits and rate limit status (Pro, Max 5x, Max 20x)
- **`/extra-usage`** -- configure pay-as-you-go overflow billing; Claude continues at standard API rates when you hit rate limits (reset every 5 hours)
- **`/cost`** -- session spending breakdown (API key users only)
- `/fast` mode is always billed to extra usage from the first token, even if plan limits remain; requires extra usage enabled and funded
- Daily redemption limit: $2,000/day
- Setup via CLI (`/extra-usage`) or web (claude.ai Settings > Usage)
- CLI budget flags: `--max-budget-usd` and `--max-turns` (print mode, API key users)

---

## Staged Implementation Roadmap

A 4-stage gate-based approach to building a Claude Code knowledge layer. Each stage has explicit "move on when" criteria and "do not overbuild" guardrails.

**Stage 0 -- Minimal Baseline:**
- Generate `CLAUDE.md` with `/init`, prune aggressively, add compaction preservation instructions, commit
- Enable and inspect auto memory via `/memory`
- Do NOT add: vector DB, custom retrieval, MCP servers
- Move on when: you still repeat the same workflow explanations weekly

**Stage 1 -- Usable Practical Setup:**
- Add `.claude/rules/` and path-scope anything non-universal
- Create 3-6 skills for repeat workflows; use supporting files for large references; use `disable-model-invocation` for side-effectful actions
- Add 1-2 high-value hooks (format-on-edit, block protected paths)
- Do NOT add: MCP servers you rarely use
- Move on when: MCP/tool overhead or external-doc retrieval becomes your bottleneck

**Stage 2 -- Stronger Retrieval:**
- Introduce MCP for external systems; use MCP resources (`@server:...`) for precise retrieval
- Tune MCP Tool Search thresholds; disable unused servers; prefer CLI tools
- Add lightweight retrieval index if local knowledge corpus is large (start with lexical/FTS; hybrid only if needed)
- Move on when: lexical retrieval fails routinely for conceptual queries and you can demonstrate it with evals

**Stage 3 -- Advanced Scaling (rarely needed):**
- Add hybrid retrieval + reranking/metadata and formal eval harness
- Integrate via an MCP retrieval server
- Formalize archival/deprecation: move stale notes out of active rotation

Most teams never need to leave Stage 1. The stop sign for overengineering is when CLAUDE.md keeps growing or MCP servers pile up unused (see [context-engineering.md](context-engineering.md#scaling-strategy-matrix-when-to-add-complexity), [failure-patterns.md](failure-patterns.md#4-context-pollution)).

*Source: deep-research-report-claudecodeknowledgelayer.md*

