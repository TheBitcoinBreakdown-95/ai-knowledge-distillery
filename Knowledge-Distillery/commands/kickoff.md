---
description: KB-powered task brief. Retrieves relevant practices, anti-patterns, and verification patterns before work begins.
---

Retrieve comprehensive knowledge from the Knowledge Distillery and present a structured brief before starting work. Coaching (Rule 1) asks the user for missing context. Kickoff answers from the KB. They complement each other.

## Usage

`/kickoff $ARGUMENTS` -- Brief for the specified task. If no argument, read the nearest WORKLOG.md "What's Next" section and brief on the first item.

## Instructions

### Step 1: Understand the Project

Read the nearest CLAUDE.md and extract the project context. You need this before you can query the KB intelligently.

Extract:
- **Identity** -- what is this project? (website, course, tool, content workspace, etc.)
- **Stack** -- what technologies, frameworks, or formats are in use?
- **Domain** -- what subject matter? (Bitcoin education, AI tooling, web dev, etc.)
- **Audience** -- who is this for? (developers, newcomers, educators, etc.)
- **Conventions** -- what voice, style, or structural rules already exist?
- **What exists** -- what infrastructure is already in place? (CLAUDE.md quality, rules, hooks, commands, task trackers, verification steps)

Also scan for:
- `WORKLOG.md` -- is there session continuity?
- Basic project structure -- are there files, an outline, any existing content?

**If the project is uninitialized** (missing CLAUDE.md or has no meaningful structure), shift to a **setup-oriented brief**:
- Flag what's missing and why it matters (cite KB sources)
- Query the KB for `project-setup.md > First Session Checklist` and `context-engineering.md > CLAUDE.md` best practices
- Present a setup brief instead of a task brief (see Step 6b)
- Ask the relevant Kickoff Questions (from project-setup.md) that can't be answered from existing files -- skip questions that the codebase already answers
- Propose a plan to create the missing infrastructure

**If initialized**, proceed to Step 1b.

### Step 1b: Quick Health Scan (initialized projects only)

Before determining the task, run 5 fast checks against the project. Each check is a single file read or keyword grep -- no MCP queries, no content analysis. This is a 5-second glance, not an audit.

| Check | What to look for | If issue found, cite |
|-------|-----------------|----------------------|
| Worklog freshness | WORKLOG.md missing, or "Last Session" date >7 days old | memory-persistence.md > Layer 2 |
| CLAUDE.md Four Pillars | Scan for coverage of: Why (purpose/goals), Map (directories/architecture), Rules (standards/gotchas), Workflows (commands/processes). Flag any missing pillar | context-engineering.md > Four-Pillar Framework |
| Task tracker state | If CLAUDE.md references a task file, check if it exists and has open items | project-setup.md > First Session Checklist |
| Verification gap | Does CLAUDE.md mention verification, testing, or how to confirm work is correct? | testing-verification.md > Verify Artifacts |
| Commands defined | Does CLAUDE.md include runnable commands (build, dev, test, etc.)? N/A for non-code projects | context-engineering.md > What to Include |

Record observations for inclusion in the brief. If all checks pass, note "All clear" and move on.

### Step 2: Determine the Task

a. If `$ARGUMENTS` is provided, use it as the task description.
b. If empty, read the nearest `WORKLOG.md` (must be within or below the current working directory -- do not search parent directories) and extract the first item from "What's Next".
c. If no worklog, no next items, or worklog is empty: present the health scan results (from Step 1b), surface open items from the task tracker if found, then ask the user what they're working on. Do not stop with nothing to show -- use the Ready Check brief (Step 6c).

### Step 3: Classify the Task

Categorize the task into one or more types:

- **Code change** -- new feature, bug fix, refactoring
- **Content creation** -- docs, slides, markdown
- **Configuration** -- settings, hooks, rules, CI/CD
- **Debugging** -- investigating failures, logs, errors
- **Infrastructure** -- build system, tooling, MCP, commands

### Step 4: Query the KB Comprehensively

This is the core of kickoff. Use the project context from Step 1 and the task from Step 2 to generate **10-30 targeted KB queries**. The goal is to surface everything in the KB that could be relevant -- practices, anti-patterns, failure modes, verification patterns, workflow patterns, tool recommendations, and domain-specific insights.

**How to generate queries:**

Use the project identity (stack, domain, audience) and the specific task to create queries across these dimensions. Not every dimension applies to every task -- skip dimensions that clearly don't fit, but err on the side of inclusion.

| Dimension | What to query | Example for "review Node SSH content for voice consistency" |
|-----------|--------------|-------------------------------------------------------------|
| **Task mechanics** | How to do this type of work well | "content review editorial process", "voice consistency writing" |
| **Domain knowledge** | Subject-matter practices | "educational content best practices", "technical writing tutorials" |
| **Anti-slop** | Preventing low-quality AI output | "anti-slop controls writing", "voice DNA style matching" |
| **Failure patterns** | What goes wrong with this type of task | "failure patterns content creation", "premature completion" |
| **Verification** | How to confirm the work is correct | "verification patterns content review", "artifact verification checklist" |
| **Workflow** | Patterns for structuring this work | "workflow patterns review process", "iterative refinement" |
| **Stack-specific** | Practices for the specific tools/formats in use | "markdown content conventions", "Obsidian formatting" |
| **Audience-specific** | Tailoring for the target reader/user | "technical hobbyist audience", "accessibility non-technical users" |
| **Context management** | Session and context risks for this task | "context window management long review", "context pollution" |
| **Scope risks** | Scope creep and over-engineering risks | "scope creep AI content", "over-engineering prevention" |
| **Tooling** | Tools or integrations that could help | "MCP tools for content", "hooks automation" |
| **Skills** | Relevant skill patterns | "writing skills patterns", "review skill examples" |
| **Similar work** | Community examples of similar tasks | "community insights content creation", "voice cloning prompt engineering" |
| **Meta-practices** | Cross-cutting practices that apply broadly | "specificity prompting", "closing the loop verification" |

**Execution:**

1. Generate the full list of queries based on the dimensions above.
2. Run them in parallel batches using `search_kb` (use `top_k: 5` or higher per query to cast a wide net).
3. Deduplicate results -- many queries will return overlapping sections. Keep each practice once.
4. Filter out practices already covered by the project's CLAUDE.md or rules files -- don't tell the user what they already have in place.
5. Group the surviving practices by theme for the brief.

**If MCP is unavailable**, note it and skip to Step 6.

### Step 5: Check Workspace Invariants

Scan the workspace CLAUDE.md "Invariants" section and any project-specific CLAUDE.md for rules that apply to this task. Include only invariants that are directly relevant.

### Step 6: Compile the Brief

Output the brief in this format:

```
## Kickoff: [task summary, 5-10 words]

**Type:** [classification from Step 3]
**Project:** [one-line project identity from Step 1 -- what it is, who it's for]

### Project Health
- [observation 1] -- [KB source]
- [observation 2] -- [KB source]
- [or "All clear -- no issues found"]

### KB Practices
[Group by theme. Include everything relevant from the KB query results. Each practice gets a one-line summary and its source. Use sub-headings if there are many practices across distinct themes.]

#### [Theme 1, e.g., "Voice and Style"]
- [Practice] -- [source-file.md > Section]
- [Practice] -- [source-file.md > Section]

#### [Theme 2, e.g., "Verification"]
- [Practice] -- [source-file.md > Section]

#### [Theme 3, e.g., "Failure Patterns to Watch"]
- [Practice] -- [source-file.md > Section]

[Continue with as many themes and practices as the KB surfaced. Do not cap the count artificially.]

### Invariants in Scope
- [Invariant, if any apply] -- [where defined]
- [or "None in scope"]

### Verification Plan
- [How to verify the task is done correctly]
- [What to check before marking complete]

### Teaching Queue
[If a Teaching Queue concept (T1-T5) from coaching.md is relevant to this task, mention it in one line. Otherwise omit this section entirely.]
```

Be comprehensive. Include every relevant practice the KB returned. The user will scan and decide what matters -- don't pre-filter for them. Omit sections with no findings (except Project Health, which always appears).

### Step 6b: Setup Brief (uninitialized projects only)

When Step 1 detected a missing CLAUDE.md or uninitialized project, use this format instead:

```
## Setup: [project/directory name]

### What's Here
- [Brief inventory of existing files/folders]

### What's Missing
- [Missing item 1] -- [why it matters, KB source]
- [Missing item 2] -- [why it matters, KB source]

### Kickoff Questions
[Ask only the questions from project-setup.md > 8 Kickoff Questions that can't be answered from existing files. Skip obvious ones. Frame them conversationally, not as a numbered interrogation.]

### Recommended Setup Steps
1. [Step 1 -- what to create first]
2. [Step 2]
3. [Step 3, if needed]
```

After presenting, ask what the user wants to tackle first. Do not assume all steps are wanted.

### Step 6c: Ready Check Brief (initialized project, no task determined)

When Step 2c applies -- the project is initialized but no task was determined (no argument, no worklog items):

```
## Kickoff: [project name] -- Ready Check

### Project Health
- [observations from Step 1b, or "All clear"]

### Open Items
- [top 1-2 items from task tracker, if found]
- [or "No task tracker found -- consider adding one"]

### Teaching Queue
[if relevant, one line. Otherwise omit.]
```

After presenting, ask what the user wants to work on. This replaces the dead-end "ask and stop" behavior.

### Step 7: Proceed

After presenting the brief, ask: "Ready to start, or want to adjust the approach?"

## Important Rules

- **Read-only** -- Do not create, modify, or delete any project files
- **Health scan is fast** -- file reads and keyword greps only. No MCP queries, no content analysis. For deep project review, use `/audit`
- **Comprehensive KB querying** -- Do not artificially limit the number of queries or practices. The goal is to surface everything relevant, not to be brief. Let the user decide what to skip.
- Do not repeat information already covered by the project's CLAUDE.md or rules files -- the brief should add value, not echo what's already in place
- Do not ask the 8 Kickoff Questions on initialized projects -- that is coaching Rule 1's job. Exception: uninitialized projects (Step 6b) should include relevant questions as part of the setup brief
- Cite KB sources with every practice and health observation
- If the task is trivial (typo fix, single-line edit, "read this file"), say "No brief needed for this task" and stop
- Omit empty sections -- if no anti-patterns found, skip that section. Exception: Project Health always appears (even if "All clear")
