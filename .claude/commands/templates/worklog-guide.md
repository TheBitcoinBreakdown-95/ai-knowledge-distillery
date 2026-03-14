# Session Continuity Guide

A simple system for maintaining project state across Claude Code sessions. Copy this pattern to any project.

---

## The Workflow

### During a session

Work normally. When something important happens (a decision, a surprise, a convention change), type `#` followed by a note:

```
# We chose Gemini Flash over Qwen because of rate limit reductions
# The rebuild script must be run with --force after logo changes
```

This saves instantly to persistent memory. No waiting until end of session.

### End of session

Say **"save progress"**. Claude will:
1. Read the current WORKLOG.md
2. Update it with what was done, what's next, and any decisions
3. Show you the updated content

That's it. Two words.

### Start of next session

**Option A — Resume recent session:**
`claude -c` picks up right where you left off. Full conversation history restored (automatically compacted if needed). Best when you stopped mid-task.

**Option B — Fresh start:**
Start a new session and say "read WORKLOG.md and continue." Best for long-running projects or after several sessions have passed. Gives you a clean context window.

**When to use which:**
- Same task, recent break: `claude -c`
- Different task, or it's been a while: fresh start + WORKLOG.md
- Context feels sluggish after compacting: fresh start + WORKLOG.md

---

## Setup for a New Project

### 1. Create WORKLOG.md in the project root

```markdown
# WORKLOG

**Last saved:** YYYY-MM-DD
**Status:** [One-line project state]

## Current State
- [What's built/done]
- [Where things stand]

## Last Session
[Brief summary of most recent work. Overwritten each save.]

## Next
1. [Priority item]
2. [Second item]
3. [Third item]

## Decisions
[Only when decisions were made this session. Remove section when empty.]

## Blockers
[Only when blockers exist. Remove section when empty.]
```

### 2. Add this to the project's CLAUDE.md

```markdown
## Session Continuity
- At session start, read WORKLOG.md if it exists
- When the user says "save progress": read WORKLOG.md, update with work done,
  what's next, and any decisions. Keep concise -- replace content, don't append.
```

### 3. Done

No commands to install. No hooks to configure. No slash commands.

---

## Rules

- **Overwrite, not append.** Each "save progress" replaces the worklog content. No session numbering, no growing history.
- **Under 40 lines.** If it's getting longer, information belongs in project-specific trackers (TODO.md, OPTIMIZATION-PLAN.md, etc.). The worklog just points to them.
- **No duplicate tracking.** Don't reproduce task lists that live elsewhere. Reference them: "Next: Phase 9.3a in OPTIMIZATION-PLAN.md."

---

## What This Replaces

If you previously used any of these, this system replaces them:
- `/transition` slash commands (multi-document update ceremonies)
- TRANSITION-PROMPT.md files (growing session-by-session logs)
- Multi-file handoff protocols
- Proactive transition trigger rules

The built-in Claude Code features that do the heavy lifting:
- **Auto-memory** — Claude writes its own notes between sessions (automatic)
- **CLAUDE.md** — persistent project instructions (loaded every session)
- **`claude -c`** — conversation resume (automatic context restoration)
- **`#` shortcut** — instant saves during a session
- **WORKLOG.md** — structured state you control (this guide)
