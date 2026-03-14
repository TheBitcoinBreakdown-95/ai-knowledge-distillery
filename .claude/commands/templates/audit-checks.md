# Audit Check Tables

Referenced by `/audit`. Contains all check definitions, report format, and adaptive rules.

---

## Category A: Foundation (CLAUDE.md & Project Identity)

| # | Check | How to Verify | Severity |
|---|-------|---------------|----------|
| A1 | CLAUDE.md exists | File exists at `[target]/CLAUDE.md` | Critical |
| A2 | CLAUDE.md is committed to git | `git ls-files CLAUDE.md` returns a result. N/A if not a git repo | Critical |
| A3 | Project description present | CLAUDE.md contains a one-line description, "About" section, or opening paragraph explaining what the project is | Critical |
| A4 | Build/dev/test commands listed | CLAUDE.md contains a "Commands" section or code blocks with runnable commands | Critical |
| A5 | Architecture or directory overview | CLAUDE.md mentions architecture, directory structure, data flow, or key directories | Recommended |
| A6 | Entry point or tech stack documented | CLAUDE.md mentions the main entry point, language, framework, or tech stack | Recommended |
| A7 | CLAUDE.md line count reasonable | PASS if <= 200 lines, WARN if 201-300, FAIL if > 300 (without referencing external docs) | Recommended |
| A8 | Documentation spine defined | CLAUDE.md references external docs in reading order, OR a `docs/` directory exists with clear navigation | Optional |
| A9 | Four-Pillar coverage | Score 0-4 for presence of: (1) The Why -- purpose/goals, (2) The Map -- directories/architecture, (3) The Rules -- standards/gotchas, (4) The Workflows -- build/test/deploy commands. PASS >= 3, WARN = 2, FAIL <= 1 | Recommended |
| A10 | Negation rules present | CLAUDE.md contains a "Do NOT" or "Don't" section with explicit prohibitions. PASS if present, WARN if absent | Recommended |
| A11 | CLAUDE.md freshness | Check last git commit date for CLAUDE.md. PASS if < 90 days, WARN if 90-180 days, FAIL if > 180 days. N/A if not git or file is new | Optional |
| A12 | CLAUDE.md quality score | Apply the 6-criterion rubric from `audit-scoring.md`. PASS if grade B or above, WARN if C, FAIL if D or below | Recommended |

**KB references:** `project-setup.md` (Day-Zero Workflow, CLAUDE.md Templates, First Session Checklist), `context-engineering.md` (CLAUDE.md: Your Always-Loaded Memory, What to Include, Four-Pillar Framework)

---

## Category B: Configuration (Settings & Tooling)

| # | Check | How to Verify | Severity |
|---|-------|---------------|----------|
| B1 | `.claude/settings.json` exists | File exists at `[target]/.claude/settings.json` | Recommended |
| B2 | `allowedTools` configured | `settings.json` contains `allowedTools` array with at least one entry | Recommended |
| B3 | `deny` patterns configured | `settings.json` contains a `deny` array (especially for `.env` files) | Recommended |
| B4 | `.mcp.json` exists (if applicable) | File exists at `[target]/.mcp.json`. Mark N/A if the project clearly has no external tool needs | Optional |
| B5 | Local config gitignored | `.gitignore` contains entries for `CLAUDE.local.md` and/or `.claude/settings.local.json`, OR those files do not exist. N/A if not git | Recommended |
| B6 | Hook coverage adequate | For typed languages: type-check hook exists. For projects with tests: test hook exists. Mark N/A if no typed lang and no test suite | Recommended |
| B7 | Permission model least-privilege | `allowedTools` does not contain `Bash(*)` (unrestricted). `deny` patterns cover `.env*` files. WARN if Bash is unrestricted, FAIL if no deny patterns on a project with secrets | Recommended |

**KB references:** `project-setup.md` (Step 3: Configure Settings, Settings.json Patterns, Permission Configuration), `context-engineering.md` (Enforcement Guarantee Ladder)

---

## Category C: Workflow Infrastructure (Commands, Skills, Hooks)

| # | Check | How to Verify | Severity |
|---|-------|---------------|----------|
| C1 | `.claude/commands/` directory exists | Directory exists and contains at least one `.md` file | Optional |
| C2 | Custom commands follow standard format | Each `.md` in `.claude/commands/` has a description line and structured instructions | Optional |
| C3 | Skills directory exists (if applicable) | `.claude/skills/` exists. Mark N/A for simple projects | Optional |
| C4 | Hooks are configured | `settings.json` contains a `hooks` section with at least one hook | Optional |
| C5 | Verification hooks present | Hooks include a PostToolUse hook for type-checking, linting, or test running. Mark N/A if project uses no typed language or build system | Recommended |
| C6 | Thin-skills compliance | Every `.md` in `.claude/commands/` and `.claude/skills/` is under 100 lines and has a single responsibility. WARN if any exceed 100 lines, FAIL if any exceed 200 lines | Recommended |
| C7 | Subagent definitions exist | If the project is complex (3+ directories, multiple languages, or CI/CD), check for agent definitions in `.claude/agents/` or subagent usage patterns in commands. Mark N/A for simple projects | Optional |
| C8 | Decision traces exist | A `DECISIONS.md` file or equivalent decision log exists documenting architectural choices with rationale. Mark N/A for simple/new projects | Optional |
| C9 | Invariants defined for critical features | If the project has auth, payments, or PII features, invariant rules are documented in CLAUDE.md, rules files, or a dedicated invariants file. Escalate to Critical if high-stakes keywords found with no invariants | Conditional |

**KB references:** `skills.md` (Skill File Structure, Thin Skills Principle), `testing-verification.md` (Automated Verification Hooks, Invariants vs Requirements), `agent-design.md` (Subagents in Claude Code)

---

## Category D: Memory & Persistence

| # | Check | How to Verify | Severity |
|---|-------|---------------|----------|
| D1 | Memory persistence strategy exists | At least one of: `WORKLOG*.md`, `TRANSITION-PROMPT.md`, `memory/` directory, session log files, or `.claude/CLAUDE.md` (personal notes) exists | Recommended |
| D2 | Session handoff mechanism | A transition prompt, handoff doc, or `/transition`-style command exists | Optional |
| D3 | Worklogs reasonable length | If `WORKLOG*.md` files exist, check line counts. PASS if all <= 100 lines. WARN 101-200. FAIL if any > 200 | Recommended |
| D4 | Memory layer completeness | Score against the Four-Layer Memory Model: (1) CLAUDE.md, (2) Worklogs, (3) Auto-memory/persistent notes, (4) External knowledge (MCP, docs). PASS >= 3 layers, WARN = 2, FAIL <= 1 | Recommended |
| D5 | Self-modification rules defined | CLAUDE.md or rules files specify when/how the AI should update its own instructions (e.g., "update WORKLOG on save", self-improvement loops). Mark N/A for simple projects | Optional |
| D6 | Lessons capture mechanism exists | A pattern for converting debugging insights into persistent knowledge: lessons file, memory notes, or bug-to-lesson workflow. Mark N/A for new projects | Optional |

**KB references:** `memory-persistence.md` (The Four-Layer Memory Model, Self-Improvement Loop), `failure-patterns.md` (Over-Engineered Worklogs)

---

## Category E: Verification & Testing

| # | Check | How to Verify | Severity |
|---|-------|---------------|----------|
| E1 | Test infrastructure exists | Test config files (`vitest.config.*`, `jest.config.*`, `pytest.ini`, etc.) or test directories (`__tests__/`, `tests/`, `*.test.*` files) exist. Mark N/A for non-code projects | Recommended |
| E2 | Test command in CLAUDE.md | CLAUDE.md mentions a test command (search for "test" in Commands section) | Recommended |
| E3 | Invariants for high-stakes domains | If the project touches auth/payments/PII (search source files for: `password`, `token`, `payment`, `stripe`, `jwt`, `auth`, `session`, `encrypt`, `secret`, `credit`), check if invariant definitions exist in CLAUDE.md, WORKLOG, or a dedicated file. Escalate to Critical if high-stakes keywords found | Conditional |
| E4 | Verification hooks wired | PostToolUse hooks exist for type-check, lint, or test on relevant file types. Score: 0 = none, 1 = one hook, 2+ = comprehensive. PASS >= 1, WARN = 0 for code projects. N/A for non-code | Recommended |
| E5 | Closing-the-loop pattern documented | CLAUDE.md or workflow docs describe a verify-after-change pattern (run tests after edits, check build after changes). Mark N/A for non-code projects | Optional |

**KB references:** `testing-verification.md` (Invariants vs Requirements, Binary Pass/Fail Criteria, Closing the Loop, Automated Verification Hooks)

---

## Category F: Security

| # | Check | How to Verify | Severity |
|---|-------|---------------|----------|
| F1 | No credentials in CLAUDE.md | Scan for patterns: `sk-`, `ghp_`, `xoxb-`, `AKIA`, `Bearer `, `token:`, connection strings, base64 strings > 40 chars. PASS if clean | Critical |
| F2 | No credentials in settings.json | Same scan on `.claude/settings.json` | Critical |
| F3 | No credentials in .mcp.json | If `.mcp.json` exists, scan for hardcoded tokens in `env` values (vs. env var references like `$VAR_NAME`) | Critical |
| F4 | `.env` files protected | `.env` is in `.gitignore`, OR `settings.json` has a deny pattern for `.env`, OR no `.env` files exist | Critical |
| F5 | `.env` files not committed | `git ls-files .env .env.*` returns empty. N/A if not git | Critical |

**KB references:** `failure-patterns.md` (Security Failure Patterns), `project-setup.md` (Environment Variables)

---

## Category G: Anti-Pattern Detection

| # | Check | How to Verify | Severity |
|---|-------|---------------|----------|
| G1 | No kitchen-sink skills | All files in `.claude/commands/` and `.claude/skills/` are under 200 lines. WARN if any 200-400 lines, FAIL if any > 400 lines | Recommended |
| G2 | No prompt entropy | Combined line count of CLAUDE.md + all `.claude/rules/*.md` files is under 500 lines. WARN 500-700, FAIL > 700 | Recommended |
| G3 | No over-engineered worklogs | All `WORKLOG*.md` files are under 100 lines. WARN 100-150, FAIL > 150 | Recommended |
| G4 | Context pollution prevention documented | CLAUDE.md or rules mention clearing context, `/clear`, or session boundaries between unrelated tasks | Optional |
| G5 | Loop trap prevention | CLAUDE.md or rules mention stopping after repeated failures, retry limits, or escalation patterns | Optional |

**KB references:** `failure-patterns.md` (Kitchen-Sink Skills, Prompt Entropy, Loop Trap: Agent Repeats the Same Failed Fix, Context Pollution)

---

## Category H: Workflow Maturity

| # | Check | How to Verify | Severity |
|---|-------|---------------|----------|
| H1 | End-to-end workflow documented | At least one complete workflow is documented (build-test-deploy, feature development, or content pipeline) showing the full sequence of steps | Optional |
| H2 | Enforcement ladder compliance | Check ratio of advisory (CLAUDE.md, rules) vs deterministic (hooks, CI) enforcement. PASS if at least one deterministic mechanism exists alongside advisory rules. WARN if all enforcement is advisory only | Optional |
| H3 | Cross-project awareness | If part of a multi-project workspace, the workspace-level CLAUDE.md references this project. Mark N/A for standalone repos | Optional |

**KB references:** `workflow-patterns.md` (Vibe Engineering), `context-engineering.md` (Enforcement Guarantee Ladder)

---

## Report Format

### Summary Scorecard

```
## Project Audit -- [target directory name] -- [date]

### Summary

| Category | Pass | Warn | Fail | N/A |
|----------|------|------|------|-----|
| A: Foundation | | | | |
| B: Configuration | | | | |
| C: Workflow | | | | |
| D: Memory | | | | |
| E: Verification | | | | |
| F: Security | | | | |
| G: Anti-Patterns | | | | |
| H: Workflow Maturity | | | | |
| **Total** | | | | |

**Maturity:** [Starter / Developing / Established / Optimized / Exemplary]
```

Maturity levels:
- **Starter** -- Any Critical FAIL
- **Developing** -- Zero Critical FAILs, but 3+ Recommended FAILs
- **Established** -- Zero Critical FAILs, fewer than 3 Recommended FAILs
- **Optimized** -- Zero FAILs of any severity
- **Exemplary** -- Zero FAILs, zero WARNs, at least one deterministic enforcement mechanism (hook or CI)

### Detailed Findings (WARN/FAIL only)

```
### [#]: [Check Name] -- [WARN/FAIL]

**Severity:** [Critical / Recommended / Optional / Conditional]
**Found:** [Specific observation]
**Best practice:** [One-sentence summary from KB]
**KB reference:** [topic-file.md] > [Section Heading]
**Suggested fix:** [Concrete action to take]
```

### Top 3 Recommendations

Prioritized by: (1) Critical severity, (2) quick wins, (3) compounding benefit.

```
### Top Recommendations

1. **[Action]** -- [Why]. See [KB file] > [Section].
2. **[Action]** -- [Why]. See [KB file] > [Section].
3. **[Action]** -- [Why]. See [KB file] > [Section].
```

### CLAUDE.md Starter (if A1 FAILED)

```markdown
# [Project Name]

## About
[One sentence: what this project is and does.]

## Tech Stack
[Language, framework, database, key libraries.]

## Commands
[Build, test, lint, dev server -- the commands you actually run.]

## Key Directories
- `src/` -- [what lives here]
- `tests/` -- [test framework and conventions]

## Notes
[One or two gotchas a new developer would hit.]
```

If A1 PASSED but A5 or A6 FAILED, list the specific sections to add with a reference to the full template in `project-setup.md` > CLAUDE.md Templates.

### CLAUDE.md Quality Score (if A12 triggered)

Include the scoring breakdown from `audit-scoring.md` with the letter grade and per-criterion scores.

---

## Adaptive Rules

- **Non-git directories** -- Skip checks A2, A11, B5, F5. Note: "Not a git repository -- git-dependent checks skipped."
- **Non-code projects** (no `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `Makefile`, etc.) -- Skip B6, C5, C6, E1, E4, E5. Note: "No package manifest detected -- build-tool checks skipped."
- **Monorepo detection** -- If a parent directory also has CLAUDE.md, note: "Parent CLAUDE.md detected at [path]. This audit covers the target directory scope only."
- **Stub projects** (fewer than 5 files) -- Report: "This appears to be an empty or stub project. Most checks are not applicable yet." Only run Category F checks.
- **Simple projects** (no CI, single directory, < 500 LOC) -- Mark C7, C8, D5, D6, H1 as N/A. Note: "Simple project -- advanced workflow checks skipped."
