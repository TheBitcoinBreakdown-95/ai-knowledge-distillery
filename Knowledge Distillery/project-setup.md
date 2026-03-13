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

Place `.mcp.json` at project root. Use `--mcp-debug` to troubleshoot. Document MCP usage guidance in `CLAUDE.md` so Claude knows *when* and *how* to use each server. (see [tools-and-integrations.md#mcp-servers-extending-capabilities](tools-and-integrations.md#mcp-servers-extending-capabilities))

### Local-First Development: Docker + Ollama Setup Pattern

- Beginner-documented path from zero to running local AI tools: enable VM/SVM in BIOS, install Docker, clone repo, configure API keys, compose containers, open ports
- Key lesson: the gap between "download this repo" and "it actually runs" involves BIOS settings, Docker networking, port configuration, and model pulling -- none in most README instructions
- Docker Compose as deployment unit: services in `docker-compose.yml`, env vars pointing to local Ollama (`http://host.docker.internal:11434`), persistent volumes
- Model setup is separate from app setup: `ollama pull [model]` + configure app to reference model names
- Same skills needed for MCP server configuration and local tool integration (see [project-setup.md](#step-4-set-up-mcp-servers))
*Source: Old Notes/Open Notebook.md*

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

