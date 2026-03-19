# /kickoff Command Guide

A comprehensive reference for the `/kickoff` slash command -- what it does, how to use it, how it works internally, and best practices.

---

## What It Is

`/kickoff` is a **read-only pre-work brief**. It queries the Knowledge Distillery before you start a task and presents everything the KB knows that could be relevant -- best practices, anti-patterns, failure modes, verification patterns, and tooling suggestions. Think of it as a senior colleague saying "here's what I'd keep in mind before starting this."

It does not create, modify, or delete any files. It only reads and reports.

---

## How to Use It

Three invocation patterns:

| Pattern | What happens |
|---------|-------------|
| `/kickoff build a contact form` | Briefs on the specified task |
| `/kickoff` (no argument) | Reads WORKLOG.md "What's Next" and briefs on the first item |
| `/kickoff` (no argument, no worklog) | Presents a "Ready Check" -- project health + open tracker items, then asks what you're working on |

---

## How It Works Internally

Here is what happens when you run `/kickoff` (steps with sub-variants for the 3 output formats):

### Step 1: Understand the Project

Reads the nearest CLAUDE.md and extracts:

- **Identity** -- what is this project? (website, course, tool, etc.)
- **Stack** -- technologies, frameworks, formats in use
- **Domain** -- subject matter (Bitcoin education, AI tooling, web dev, etc.)
- **Audience** -- who is this for? (developers, newcomers, educators, etc.)
- **Conventions** -- voice, style, structural rules already in place
- **What exists** -- infrastructure already in place (CLAUDE.md quality, rules, hooks, commands, task trackers, verification steps)

If no CLAUDE.md exists, the command shifts to **setup mode** instead of a task brief.

### Step 1b: Health Scan (initialized projects only)

Five fast checks (file reads and keyword greps only -- no MCP queries):

| Check | What to look for | KB source if issue found |
|-------|-----------------|--------------------------|
| Worklog freshness | WORKLOG.md missing, or last session >7 days old | memory-persistence.md > Layer 2 |
| CLAUDE.md Four Pillars | Coverage of: Why, Map, Rules, Workflows | context-engineering.md > Four-Pillar Framework |
| Task tracker state | Tracker exists and has open items | project-setup.md > First Session Checklist |
| Verification gap | Does CLAUDE.md mention how to confirm work? | testing-verification.md > Verify Artifacts |
| Commands defined | Build/dev/test commands present? | context-engineering.md > What to Include |

This is a 5-second glance, not an audit. For deep analysis, use `/audit`.

### Step 2: Determine the Task

1. If `$ARGUMENTS` is provided, use it as the task description
2. If empty, read the nearest WORKLOG.md and extract the first "What's Next" item
3. If no worklog or no next items: present the health scan, surface open tracker items, ask what the user is working on

### Step 3: Classify the Task

Tags the task as one or more of:

- **Code change** -- new feature, bug fix, refactoring
- **Content creation** -- docs, slides, markdown
- **Configuration** -- settings, hooks, rules, CI/CD
- **Debugging** -- investigating failures, logs, errors
- **Infrastructure** -- build system, tooling, MCP, commands

### Step 4: Query the KB (the core)

Generates **10-30 targeted queries** using `search_kb` across 14 dimensions:

| Dimension | What it surfaces |
|-----------|-----------------|
| Task mechanics | How to do this type of work well |
| Domain knowledge | Subject-matter practices |
| Anti-slop | Preventing low-quality AI output |
| Failure patterns | What goes wrong with this type of task |
| Verification | How to confirm the work is correct |
| Workflow | Patterns for structuring this work |
| Stack-specific | Practices for the specific tools/formats in use |
| Audience-specific | Tailoring for the target reader/user |
| Context management | Session and context risks |
| Scope risks | Scope creep and over-engineering risks |
| Tooling | Tools or integrations that could help |
| Skills | Relevant skill patterns |
| Similar work | Community examples of similar tasks |
| Meta-practices | Cross-cutting practices that apply broadly |

Results are deduplicated and filtered against practices already covered by the project's CLAUDE.md or rules files.

### Step 5: Check Invariants

Scans the workspace CLAUDE.md "Invariants" section and any project-specific CLAUDE.md for rules directly relevant to the task.

### Step 6: Compile the Brief

Outputs a structured brief with:

- **Project Health** -- observations from Step 1b (always present)
- **KB Practices** -- grouped by theme, every relevant practice the KB returned
- **Invariants in Scope** -- applicable rules
- **Verification Plan** -- how to confirm the task is done correctly
- **Teaching Queue** -- if a T1-T5 concept is relevant (optional)

### Step 7: Proceed

Asks: "Ready to start, or want to adjust the approach?"

---

## Three Output Formats

### 1. Task Brief (standard)

Project is initialized, task is known. Full KB-backed brief with practices, anti-patterns, verification plan.

### 2. Setup Brief (uninitialized projects)

Project has no CLAUDE.md or meaningful structure. Instead of a task brief, outputs:

- **What's Here** -- inventory of existing files/folders
- **What's Missing** -- gaps and why they matter (with KB sources)
- **Kickoff Questions** -- relevant questions from the 8 Kickoff Questions (see [project-setup.md](project-setup.md#the-8-kickoff-questions)) that existing files cannot answer
- **Recommended Setup Steps** -- ordered plan to create missing infrastructure

### 3. Ready Check (no task determined)

Project is initialized but no task was specified and no worklog items exist. Shows health scan results, open tracker items, and asks what the user wants to work on.

---

## The 8 Kickoff Questions

These come from [project-setup.md](project-setup.md#the-8-kickoff-questions) and are used in Setup Briefs (uninitialized projects):

**Understanding the Project:**
1. What does this project do in one sentence?
2. Who uses this, and what do they need?
3. What technologies is it built with?
4. Where is the main entry point?

**Understanding the Work:**
5. What needs to be done?
6. What does "done" look like?
7. What constraints do I need to work within?
8. What could go wrong?

On initialized projects, `/kickoff` does NOT ask these questions -- that is Coaching Rule 1's job if needed.

---

## How /kickoff Interacts with Coaching Rule 1

This is the most important design detail. `/kickoff` and Coaching Rule 1 (Adaptive Kickoff) are **complementary, not redundant**:

| | Coaching Rule 1 | /kickoff command |
|---|---|---|
| **Purpose** | Asks the user for missing context | Answers from the KB |
| **Trigger** | Automatic on ambiguous requests | Manual invocation |
| **Output** | Clarifying questions | Structured brief with practices |
| **On uninitialized projects** | They merge -- coaching asks questions, kickoff provides KB knowledge, both feed into a setup plan |

On initialized projects with a clear task, `/kickoff` does not ask the 8 Kickoff Questions. Coaching asks. Kickoff answers. They serve different functions and remain separate.

(see [DECISIONS.md](DECISIONS.md#decision-kickoff-command-not-expanded-coaching) for the architectural reasoning behind this separation)

---

## Best Practices

1. **Use it at the start of non-trivial tasks.** A typo fix does not need a brief. Building a new feature, setting up a project, or debugging a complex issue does.

2. **Provide specific task descriptions.** `/kickoff add OAuth login to the API` gives better KB results than `/kickoff work on auth`. The more specific your argument, the more targeted the 10-30 queries become. (see [prompt-engineering.md](prompt-engineering.md#core-principle-specificity-is-everything))

3. **Keep your WORKLOG.md current.** If you use `/kickoff` with no argument, it reads "What's Next" from the worklog. A stale worklog means a stale brief.

4. **Do not skip the Verification Plan.** The brief always includes a verification section. Use it as your "done" checklist -- this directly feeds Coaching Rule 3 (Verification Before Done).

5. **Scan, do not read every line.** The brief is intentionally comprehensive. It surfaces everything the KB has. You decide what is relevant -- the command does not pre-filter.

6. **Use it on new projects.** Running `/kickoff` in a directory with no CLAUDE.md triggers the setup brief, which walks you through initializing the project properly. This is one of the fastest ways to bootstrap a new project with KB-backed infrastructure.

7. **Pair with `/audit` for depth.** The health scan in kickoff is a 5-second glance (file reads only, no MCP). If it flags issues, `/audit` gives the deep analysis.

---

## What It Does NOT Do

- Does not modify any files (read-only)
- Does not run builds, tests, or commands
- Does not ask the 8 Kickoff Questions on initialized projects (that is coaching's job)
- Does not replace thinking -- it is information, not a plan
- Does not work well for trivial tasks (will explicitly say "No brief needed")

---

## When to Skip It

- Typo fixes, single-line edits, "read this file"
- Tasks where you already know the full context and just need execution
- When you say "just do it" to coaching -- that same energy applies here

---

## Command Source

The command definition lives at `.claude/commands/kickoff.md`. It is a Claude Code slash command loaded automatically when working in this workspace.

Related files:
- `.claude/rules/coaching.md` -- Coaching Rule 1 (Adaptive Kickoff) that complements this command
- `.claude/rules/teaching-queue.md` -- T1-T5 concepts that may appear in kickoff briefs
- [project-setup.md](project-setup.md) -- Source of the 8 Kickoff Questions and First Session Checklist
- [context-engineering.md](context-engineering.md) -- Enforcement Guarantee Ladder (kickoff sits on the "on-demand" tier)
- [DECISIONS.md](../../../DECISIONS.md) -- Decision trace for why this is a command, not an expanded coaching rule
