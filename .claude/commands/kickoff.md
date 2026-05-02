---
description: KB-powered task brief. Retrieves relevant practices, anti-patterns, and verification patterns before work begins.
---

Retrieve comprehensive knowledge from the Knowledge Distillery and present a structured brief before starting work. Coaching (Rule 1) asks the user for missing context. Kickoff answers from the KB. They complement each other.

## Usage

`/kickoff $ARGUMENTS` -- Brief for the specified task. If no argument, read the nearest WORKLOG.md "What's Next" section and brief on the first item.

## Instructions

### Step 1: Understand the Project

Read the nearest CLAUDE.md. Extract: Identity, Stack, Domain, Audience, Conventions, existing infrastructure (CLAUDE.md quality, rules, hooks, commands, task trackers, verification). Also read WORKLOG.md if present.

**If uninitialized** (no CLAUDE.md or empty structure): produce a Setup Brief (see [kickoff-guide.md](kickoff-guide.md)). Ask only the kickoff questions the existing files can't answer.

**If initialized**, proceed to Step 1b.

### Step 1b: Quick Health Scan

Five fast checks — single file reads or keyword greps only. No MCP queries.

| Check | What to look for | If issue, cite |
|-------|-----------------|----------------|
| Worklog freshness | Missing or "Last Session" >7 days old | memory-persistence.md > Layer 2 |
| CLAUDE.md Four Pillars | Why, Map, Rules, Workflows all present | context-engineering.md > Four-Pillar Framework |
| Task tracker | Referenced file exists with open items | project-setup.md > First Session Checklist |
| Verification gap | Mentions testing or how to confirm work is correct | testing-verification.md > Verify Artifacts |
| Commands defined | Runnable commands present (N/A for non-code) | context-engineering.md > What to Include |

### Step 2: Determine the Task

a. If `$ARGUMENTS` is provided, use it.
b. If empty, read the nearest WORKLOG.md and extract the first "What's Next" item. Do not search parent directories.
c. If no worklog or no items: present health scan + open task tracker items, then ask. Use Ready Check format (see [kickoff-guide.md](kickoff-guide.md)).

### Step 3: Classify the Task

Code change / Content creation / Configuration / Debugging / Infrastructure

### Step 4: Query the KB Comprehensively

Generate 10–30 queries across these dimensions: Task mechanics, Domain knowledge, Anti-slop, Failure patterns, Verification, Workflow, Stack-specific, Audience-specific, Context management, Scope risks, Tooling, Skills, Similar work, Meta-practices.

Run in parallel batches via `search_kb` (top_k: 5+). Deduplicate. Filter out what's already in the project's CLAUDE.md. Group survivors by theme.

**If MCP unavailable**, note it and proceed to Step 6.

### Step 5: Check Workspace Invariants

Scan CLAUDE.md for invariants relevant to this task.

### Step 6: Compile the Brief

See [kickoff-guide.md](kickoff-guide.md) for full format templates. Output:
- Header: Type, Project (one line)
- Project Health (always present)
- KB Practices grouped by theme — comprehensive, don't pre-filter
- Invariants in Scope
- Verification Plan

### Step 7: Proceed

Ask: "Ready to start, or want to adjust the approach?"

## Important Rules

- **Read-only** — do not create, modify, or delete project files
- **Health scan is fast** — file reads and keyword greps only; no MCP queries. Use `/audit` for deep review
- **Comprehensive KB querying** — don't cap practice count; let the user decide what to skip
- Don't repeat information already covered by the project's CLAUDE.md or rules files
- Don't ask the 8 Kickoff Questions on initialized projects (that's coaching Rule 1's job)
- Cite KB sources with every practice and health observation
- If task is trivial (typo fix, single read), say "No brief needed" and stop
- Omit empty sections; Project Health always appears (even if "All clear")
