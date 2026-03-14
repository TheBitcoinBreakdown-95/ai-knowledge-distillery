# Learning Path

A curated guide for the human orchestrator. The KB synthesizes well for AI agents reading it in full, but humans need a filtered view: the most important, verified, actionable concepts in the right order.

**How to use:** Work through each level sequentially. Each entry links to the source section. Skip ahead only if you already practice the concept consistently.

---

## Level 1: Foundations

Establish the mental model and vocabulary that everything else builds on. Read these first.

### 1. Specificity Is Everything

- **Why:** The single highest-leverage insight in AI-assisted work. Vague prompts produce vague output. Detailed prompts with exact tech stack, constraints, and examples produce usable code on the first pass.
- **Takeaway:** Replace "make it look good" with "use Tailwind, rounded-lg, shadow-md, 16px padding, #1a1a2e background."
- **Link:** [prompt-engineering.md → Core Principle](prompt-engineering.md#core-principle-specificity-is-everything)
- **Prerequisites:** None
- **Depth:** 10 min read

### 2. The 8 Kickoff Questions

- **Why:** Every project starts with the same 8 questions. Answering them before writing code prevents the most common failures: wrong scope, missing constraints, unclear completion criteria.
- **Takeaway:** Ask "What does done look like?" before touching code. If you cannot describe the end state, the AI cannot either.
- **Link:** [project-setup.md → The 8 Kickoff Questions](project-setup.md#the-8-kickoff-questions)
- **Prerequisites:** None
- **Depth:** 5 min read

### 3. CLAUDE.md: Your Always-Loaded Memory

- **Why:** The single most impactful configuration file. Loaded automatically at every session start. Three scopes (global, project, local) let you layer instructions from general to specific.
- **Takeaway:** Write a CLAUDE.md for every project. Include: build commands, architecture overview, code style rules, what NOT to do.
- **Link:** [context-engineering.md → CLAUDE.md](context-engineering.md#claudemd-your-always-loaded-memory)
- **Prerequisites:** None
- **Depth:** 15 min read

### 4. The Four Named Failure Patterns

- **Why:** Naming failures makes them catchable. These four account for most AI-assisted development problems. If you can spot them, you can fix them.
- **Takeaway:** Vision Compression (strategic context evicted), Premature Completion (says "done" at 90%), Plausible Echo (looks right but never verified), Context Pollution (wrong context leaks in).
- **Link:** [failure-patterns.md → The Four Named Patterns](failure-patterns.md#the-four-named-patterns)
- **Prerequisites:** None
- **Depth:** 10 min read

### 5. Verify Artifacts, Not Self-Reports

- **Why:** AI will confidently report success without actually running the code. This is not lying -- it is pattern-matching the concept of "done." The fix: treat every "done" as a hypothesis.
- **Takeaway:** Run tests, check the browser, curl the endpoint. Never trust "I've implemented X" without observing the artifact yourself.
- **Link:** [testing-verification.md → Core Principle](testing-verification.md#core-principle-verify-artifacts-not-self-reports)
- **Prerequisites:** #4 (Four Named Patterns)
- **Depth:** 5 min read

### 6. The Master Prompting Template

- **Why:** A 9-section framework that ensures prompts include everything the AI needs. Too much for every task, but invaluable for high-stakes features. Compress to 3 sections (Task + Background + Do-Not) for daily use.
- **Takeaway:** Every non-trivial prompt should have at minimum: what to do, relevant context, and what NOT to do.
- **Link:** [prompt-engineering.md → The Master Prompting Template](prompt-engineering.md#the-master-prompting-template)
- **Prerequisites:** #1 (Specificity)
- **Depth:** 15 min read

### 7. Context Window Management

- **Why:** Context windows have limits, and quality degrades before hitting them. Knowing when to `/compact` vs `/clear` prevents context pollution and keeps output quality high.
- **Takeaway:** `/compact` to compress within a task. `/clear` when switching between unrelated tasks. Monitor with `/context`.
- **Link:** [context-engineering.md → Context Window Management](context-engineering.md#context-window-management)
- **Prerequisites:** #3 (CLAUDE.md)
- **Depth:** 10 min read

---

## Level 2: Core Workflows

Patterns for daily use. Apply these in almost every task to get consistent, high-quality output.

### 8. The Vibe Engineering Stack

- **Why:** The overarching workflow framework: Spec → Invariants → Worklog → Code → Tests → Feedback. Each step feeds the next. The feedback loop at the end is what makes systems improve instead of just repeat.
- **Takeaway:** Software engineering did not go away -- you got promoted from writing code to directing it. The Identity Ladder: manual → supervised → autonomous.
- **Link:** [workflow-patterns.md → The Vibe Engineering Stack](workflow-patterns.md#the-vibe-engineering-stack)
- **Prerequisites:** Level 1 complete
- **Depth:** 15 min read

### 9. Spec-Driven Feature Development

- **Why:** The 7-step workflow that produces reliable results. Spec → Invariants → Worklog → Skills → Verify → Feedback → Archive. Each step has a concrete output.
- **Takeaway:** Write the spec and invariants BEFORE asking the AI to code. This is the single biggest quality lever after specificity.
- **Link:** [workflow-patterns.md → Pattern 1](workflow-patterns.md#pattern-1-spec-driven-feature-development)
- **Prerequisites:** #8 (Vibe Engineering Stack), #1 (Specificity)
- **Depth:** 20 min read

### 10. Worklogs: Session-to-Session Memory

- **Why:** CLAUDE.md stores project-wide knowledge. Worklogs store feature-specific progress that persists across sessions. Without them, every new session restarts from zero.
- **Takeaway:** Create a WORKLOG.md per feature. Update it at the end of every session. Include: what was done, what is next, decisions made and why.
- **Link:** [memory-persistence.md → Layer 2: Worklogs](memory-persistence.md#layer-2-worklogs-feature-scoped-session-to-session)
- **Prerequisites:** #3 (CLAUDE.md)
- **Depth:** 10 min read

### 11. Invariants and Binary Pass/Fail

- **Why:** Requirements are vague ("make it fast"). Invariants are verifiable ("P95 response time < 200ms"). Binary pass/fail criteria turn subjective quality into objective checkpoints.
- **Takeaway:** For every feature, define at least one invariant the AI can verify without your help. Skip for trivial tasks.
- **Link:** [testing-verification.md → Invariants vs Requirements](testing-verification.md#invariants-vs-requirements)
- **Prerequisites:** #5 (Verify Artifacts), #9 (Spec-Driven)
- **Depth:** 10 min read

### 12. Skills and Slash Commands

- **Why:** Skills are SOPs (standard operating procedures) for your AI. Slash commands trigger specific workflows. Together they encode your team's best practices into repeatable, invocable instructions.
- **Takeaway:** Create a skill when you catch yourself giving the same instruction three times (Rule of Three). One concern per skill file.
- **Link:** [skills.md → Skills: SOPs for AI Agents](skills.md#skills-sops-for-ai-agents)
- **Prerequisites:** #3 (CLAUDE.md)
- **Depth:** 20 min read

### 13. Hooks: Automated Verification

- **Why:** Hooks run before or after tool calls automatically. They catch problems (type errors, .env exposure, code duplication) in real time without human intervention.
- **Takeaway:** Start with two hooks: a type-checker on PostToolUse and an .env protector on PreToolUse. Add more as you hit recurring issues.
- **Link:** [tools-and-integrations.md → Hooks](tools-and-integrations.md#hooks-prepost-tool-automation)
- **Prerequisites:** #12 (Skills)
- **Depth:** 15 min read

### 14. The Skill Lifecycle

- **Why:** Every bug is a future prevention. The cycle: mistake → lesson → skill update → prevention. Applied in real time, in the same session while context is fresh.
- **Takeaway:** When the AI makes a mistake, update the relevant skill immediately. Do not wait for a post-mortem.
- **Link:** [skills.md → The Skill Lifecycle](skills.md#the-skill-lifecycle-mistake-lesson-skill-prevention)
- **Prerequisites:** #12 (Skills), #5 (Verify Artifacts)
- **Depth:** 5 min read

### 15. Subagents for Context Isolation

- **Why:** Mixing strategic and tactical context in one window degrades both. Subagents provide separate context windows for different phases of work.
- **Takeaway:** Use subagents when a task requires a different perspective from the one you have been building. Custom subagent definitions go in `.claude/agents/`.
- **Link:** [context-engineering.md → Subagents for Context Isolation](context-engineering.md#subagents-for-context-isolation)
- **Prerequisites:** #4 (Four Named Patterns — specifically Vision Compression), #7 (Context Window)
- **Depth:** 10 min read

---

## Level 3: Advanced

For complex projects, distributed work, or pushing beyond single-session productivity.

### 16. Personas: Imaginary Colleagues

- **Why:** Multiple AI reviewers catch what a single reviewer misses. Each persona has a specific concern (security, UX, testing, adversarial thinking). For high-risk features, run a full persona review.
- **Takeaway:** Define 4 personas (@Security, @UX, @Test, @Machiavelli). Invoke them on any feature touching PII, payments, or auth.
- **Link:** [agent-design.md → Personas](agent-design.md#personas-imaginary-colleagues-that-catch-what-you-miss)
- **Prerequisites:** #15 (Subagents)
- **Depth:** 15 min read

### 17. The Ralph Loop (Autonomous Coding)

- **Why:** Batch task execution with minimal human intervention. The AI works through a task list autonomously, logging progress and learning at each step.
- **Takeaway:** Prepare a task list with binary pass/fail for each item. Let Ralph run. Review results after. Best for well-defined, low-ambiguity tasks.
- **Link:** [workflow-patterns.md → Pattern 2: The Ralph Loop](workflow-patterns.md#pattern-2-the-ralph-loop-autonomous-coding)
- **Prerequisites:** #9 (Spec-Driven), #11 (Invariants)
- **Depth:** 15 min read

### 18. Meta-Agent Architecture

- **Why:** Separates strategy (Opus) from execution (workers). The meta-agent never writes code -- it decomposes tasks, delegates to subagents, and maintains strategic coherence. Directly prevents Vision Compression.
- **Takeaway:** For complex features, use a two-terminal pattern: one terminal for strategy (meta-agent), workers in separate terminals for execution.
- **Link:** [agent-design.md → Meta-Agent Architecture](agent-design.md#meta-agent-architecture)
- **Prerequisites:** #15 (Subagents), #16 (Personas)
- **Depth:** 20 min read

### 19. Decision Traces: Strategic Memory

- **Why:** Worklogs capture what happened. Decision traces capture WHY. Context, alternatives considered, rationale, consequences. Essential for architectural decisions that outlive a single session.
- **Takeaway:** Write a decision trace for any choice that: required >30 min of deliberation, chose between 3+ alternatives, or will constrain future work.
- **Link:** [memory-persistence.md → Decision Traces](memory-persistence.md#decision-traces-strategic-memory)
- **Prerequisites:** #10 (Worklogs)
- **Depth:** 10 min read

### 20. Prompt Cache Architecture

- **Why:** Understanding cache behavior reduces cost and latency. Cache hits require exact prefix matches. Changing tools or models mid-session breaks the cache and forces a full recompute.
- **Takeaway:** Never change tools or models mid-session. Put stable instructions (CLAUDE.md) at the top. Use messages for updates, not system prompt changes.
- **Link:** [context-engineering.md → Prompt Cache Architecture](context-engineering.md#prompt-cache-architecture)
- **Prerequisites:** #7 (Context Window)
- **Depth:** 10 min read

### 21. MCP Servers

- **Why:** MCP extends Claude Code's capabilities beyond its built-in tools. Database access, browser automation, file conversion, API integration -- all as tool calls within the same session.
- **Takeaway:** Start with 1-2 MCPs for your most common tasks. Avoid loading 10+ MCPs (context budget: keep total tool count under 30).
- **Link:** [tools-and-integrations.md → MCP Servers](tools-and-integrations.md#mcp-servers-extending-capabilities)
- **Prerequisites:** #12 (Skills), #20 (Prompt Cache)
- **Depth:** 15 min read

### 22. RPI Workflow (Research → Plan → Implement)

- **Why:** A 4-step gate system for features that require research before coding. User validation blocks between phases prevent the AI from implementing something before it fully understands the problem.
- **Takeaway:** Use RPI when you are not sure HOW to build something. The research phase uses 6 specialist agents; the plan phase produces a spec for review before any code is written.
- **Link:** [workflow-patterns.md → Pattern 4: RPI Workflow](workflow-patterns.md#pattern-4-rpi-workflow-research---plan---implement)
- **Prerequisites:** #9 (Spec-Driven), #15 (Subagents)
- **Depth:** 10 min read

---

## Level 4: Specialized

Niche domains, autonomous systems, and architectural decisions for specific use cases.

### 23. OpenClaw: Autonomous 24/7 Agents

- **Why:** Running an AI as a persistent employee (not a chat tool) introduces unique challenges: security, cost management, identity continuity, and automated self-improvement.
- **Takeaway:** Start with a brain dump, then a morning brief, then gradually grant permissions. Security is the single biggest risk -- dedicated machine, dedicated accounts, never expose to public input.
- **Link:** [autonomous-agents.md → What Is OpenClaw](autonomous-agents.md#what-is-openclaw)
- **Prerequisites:** Level 3 complete
- **Depth:** 30 min read (full file)

### 24. Brain + Muscles Architecture

- **Why:** Cost-optimized multi-model setup. Brain (Opus/Sonnet) handles orchestration and strategy. Muscles (Haiku/specialized models) handle execution. Prevents paying Opus prices for routine tasks.
- **Takeaway:** Route complex reasoning to expensive models, routine execution to cheap ones. Progressive path: start single-model, add muscles as bottlenecks appear.
- **Link:** [agent-design.md → Brain + Muscles Pattern](agent-design.md#brain--muscles-pattern-from-openclaw)
- **Prerequisites:** #18 (Meta-Agent)
- **Depth:** 10 min read

### 25. Agent Teams (Experimental)

- **Why:** Multiple Claude Code sessions coordinating on shared work. Lead assigns tasks, teammates execute in parallel. Early-stage feature with real limitations (no shared context, no cross-agent tool calls).
- **Takeaway:** Use for embarrassingly parallel work (multiple independent files/features). Do not use when tight coordination between agents is required.
- **Link:** [agent-design.md → Agent Teams](agent-design.md#agent-teams)
- **Prerequisites:** #18 (Meta-Agent), #15 (Subagents)
- **Depth:** 10 min read

### 26. claude-mem Plugin

- **Why:** Automatic cross-session memory via lifecycle hooks and a local database. Retrieves relevant memories at session start using hybrid search (vector + BM25). Saves significant tokens vs full-history dump.
- **Takeaway:** Install if you work on long-running projects with 10+ sessions. Not needed for short one-off tasks.
- **Link:** [memory-persistence.md → Layer 3: claude-mem Plugin](memory-persistence.md#layer-3-claude-mem-plugin-automatic-cross-session)
- **Prerequisites:** #3 (CLAUDE.md), #10 (Worklogs)
- **Depth:** 10 min read

### 27. Mission Control Pattern

- **Why:** Shared-database multi-agent architecture for 10+ agent teams. Six-table schema coordinates agents, tasks, configs, events, evaluations, and orchestration. Production-grade alternative to file-based coordination.
- **Takeaway:** Use when file-based shared state (worklogs, state files) breaks down at scale. Not needed for solo use or small teams.
- **Link:** [agent-design.md → Mission Control Pattern](agent-design.md#mission-control-pattern-shared-database-multi-agent-architecture)
- **Prerequisites:** #18 (Meta-Agent), #24 (Brain + Muscles)
- **Depth:** 10 min read

### 28. Security Failure Patterns

- **Why:** API key exposure, prompt injection, admin access blast radius, supply chain attacks via skill marketplaces. Every autonomous agent risk multiplied by 24/7 operation.
- **Takeaway:** Never paste API keys into AI input (use agent-vault pattern). Dedicated machine, dedicated accounts. Review every ClawHub skill before installation.
- **Link:** [failure-patterns.md → Security Failure Patterns](failure-patterns.md#security-failure-patterns)
- **Prerequisites:** #4 (Four Named Patterns)
- **Depth:** 10 min read

### 29. Claude Agent SDK

- **Why:** Programmatic access to Claude Code for building custom agent architectures. Key constraint: subagents cannot spawn subagents (one level of nesting only).
- **Takeaway:** Use the SDK when you need to orchestrate Claude Code from your own application, not from the CLI.
- **Link:** [agent-design.md → The Claude Agent SDK](agent-design.md#the-claude-agent-sdk)
- **Prerequisites:** #18 (Meta-Agent), #15 (Subagents)
- **Depth:** 15 min read

### 30. Vault-as-Codebase

- **Why:** Treating a knowledge base like a codebase: version-controlled, auditable, with automated pipelines for ingestion, verification, and quality control.
- **Takeaway:** The pattern behind this very Knowledge Distillery. Apply to any domain where knowledge accumulates faster than humans can organize it.
- **Link:** [memory-persistence.md → Vault-as-Codebase](memory-persistence.md#vault-as-codebase-knowledge-bases-operated-like-codebases)
- **Prerequisites:** #10 (Worklogs), #19 (Decision Traces)
- **Depth:** 5 min read

---

## Teaching Candidates

New concepts flagged by `/process-notes` as potentially teach-worthy (3+ sources, affects 2+ KB files, introduces new workflows, or contradicts existing practice). Review and promote to a level above when verified.
