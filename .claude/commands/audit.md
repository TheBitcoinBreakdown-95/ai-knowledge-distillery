---
description: Audit a project directory against AI/LLM development best practices from the Knowledge Distillery.
---

Audit a project directory against AI/LLM development best practices from the Knowledge Distillery. Read-only -- reports findings, does not modify the target project.

## Usage

`/audit $ARGUMENTS` -- Audit the specified project directory. If no path is given, audit the current working directory's project root.

## Instructions

### Step 0: Resolve Target Directory

a. If `$ARGUMENTS` is provided, resolve it relative to the current working directory or as absolute path.
b. If empty, walk up from cwd to find nearest project root (`.git/`, `package.json`, `CLAUDE.md`).
c. Verify it exists. If not, report error and stop.
d. Detect git repo. Count files -- if fewer than 5, run only Category F checks.

### Step 1: Load Context

Read these files:

- `.claude/commands/templates/audit-checks.md` -- all check definitions (Categories A-H), report format, adaptive rules
- `.claude/commands/templates/audit-scoring.md` -- CLAUDE.md quality rubric (for check A12)

### Step 1.5: Classify Project

Before running checks, classify the target:

- **Type:** Code project (has package manifest, source files) or Content project (markdown, docs, config only)
- **Complexity:** Simple (< 500 LOC, single directory), Medium (multi-directory, one language), Complex (multi-language, CI/CD, multiple services)
- **Tech stack:** Languages, frameworks, build tools detected
- **Workspace context:** Standalone repo or part of a multi-project workspace

Record this classification in the report header. It determines which adaptive rules apply.

### Step 2: Retrieve KB Best Practices

Use the `search_kb` MCP tool to pull relevant best practices based on the project classification:

- For code projects: search for the detected framework/language patterns
- For all projects: search for "CLAUDE.md best practices", "security configuration", "verification patterns"
- Use retrieved KB content to enrich the "Best practice" field in detailed findings

If MCP is unavailable, fall back to the static KB references listed in each category of audit-checks.md.

### Step 3: Run Checks

Run all checks from Categories A-H in the audit-checks template. Record PASS / WARN / FAIL / N/A for each. Apply the adaptive rules (non-git, non-code, monorepo, stub project, simple project).

### Step 4: Compile Report

Follow the report format in the audit-checks template: summary scorecard (8 categories), detailed findings (WARN/FAIL only), top 3 recommendations, CLAUDE.md starter if A1 failed, quality score if A12 triggered.

## Important Rules

- **Read-only** -- Do not create, modify, or delete any files anywhere
- Credential scanning (F1-F3): false positives acceptable, false negatives are not
- N/A means not applicable, not FAIL -- do not penalize for inapplicable checks
- If target path is ambiguous, ask the user to clarify
- All KB references use paths relative to `Knowledge Distillery/`
- Do not audit the Knowledge Distillery itself -- use `/kb-status` and `/verify-kb` instead
- UIGen is a test project -- skip it entirely if encountered
