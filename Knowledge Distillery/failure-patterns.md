# Failure Patterns & Anti-Patterns

## Why Naming Failures Matters

"Named problems become workable. Unnamed problems become tech debt."

The act of naming a failure *during* the work -- not after -- is what turns a surprise into a reusable principle. You build, encounter something unexpected, and name the specific thing: "the agent skipped the design loops because the prompt framed them as suggestions." That name produces a pattern. The pattern becomes a choice you make going forward. The choice becomes process.

This is not reflection. Reflection happens after. This happens during -- you are building and watching yourself build at the same time, and the watching changes the building. The process is a product that evolves through use, not through design.

The fix protocol is always the same: **Catch -> Name -> Update Skill -> Prevent Recurrence** (see [skills.md#the-skill-lifecycle-mistake---lesson---skill---prevention](skills.md#the-skill-lifecycle-mistake---lesson---skill---prevention)).

---

## The Four Named Patterns

### 1. Vision Compression

- **What:** Strategic context gets compressed out as implementation detail grows.
- **Cause:** A single context window tries to hold both *why* and *how*. As tokens accumulate with file paths, function signatures, and error traces, the original vision -- architecture, goals, rationale -- gets silently evicted.
- **Symptoms:**
  - Features ship correctly but solve the wrong problem
  - Architectural decisions drift from the original plan mid-session
  - Agent optimizes for local code correctness instead of system-level coherence
  - You re-read the output and realize the spec was quietly abandoned
- **Fix:** Separate strategic and tactical into different windows/sessions. Keep a meta-lane AI whose context is purely strategic, never polluted with implementation detail (see [context-engineering.md#subagents-for-context-isolation](context-engineering.md#subagents-for-context-isolation)).
- **Prevention:**
  - Maintain a strategic AI that holds project-level context across sessions
  - Persist the "why" in worklogs with explicit milestones, not just in conversation memory
  - Run `/clear` before switching from planning to implementation
  - Write the spec before the session where code gets written
  - Use CLAUDE.md and worklog invariants to anchor intent on disk where it cannot erode

### 2. Premature Completion

- **What:** Agent declares "done" based on what it completed, not the full spec.
- **Cause:** No explicit completion criteria in the prompt. The agent cannot distinguish "code written" from "feature working." Without an explicit verification step, it marks "done" after writing code, not after proving it works (see [prompt-engineering.md#2-task-what-to-do](prompt-engineering.md#2-task-what-to-do)).
- **Symptoms:**
  - Agent says "all tests pass" at 90% completion
  - Missing edge cases or features from the original request
  - Work looks finished until you actually run it
  - Closing-the-loop steps were never executed
  - Milestone log shows completion but the artifact was never tested end-to-end
- **Fix:** Binary pass/fail criteria in every prompt. Define "done" as a verifiable state, not a self-assessment (see [testing-verification.md#closing-the-loop](testing-verification.md#closing-the-loop)).
- **Prevention:**
  - Add a "Closing the Loop" section to every worklog with concrete verification steps
  - Use invariants for high-stakes features: `INV-1: A single email cannot receive >5 magic links per hour`
  - Require at least one end-to-end verification (Playwright, curl, browser check) per milestone
  - AI should never just write code -- it needs a way to prove the code works
  - Verification method depends on context: unit tests as baseline, Playwright for web, curl for API

### 3. Plausible Echo

- **What:** Output looks correct but was never verified against reality.
- **Cause:** Reviewer trusts the self-report instead of checking the artifact. The AI generates confident, well-formatted output regardless of whether it actually works. Most people building with AI cannot distinguish a real result from a plausible echo of one.
- **Symptoms:**
  - "All tests pass" but tests were never run
  - Code compiles in the agent's narrative but errors on execution
  - Documentation describes behavior the system does not exhibit
  - Demo works in the agent's summary but not in the browser
  - The button that looks right but does not actually submit; the form that validates but does not save
- **Fix:** Always verify the artifact (run tests, check browser, curl the endpoint). Treat agent output as a draft until independently confirmed (see [testing-verification.md#closing-the-loop](testing-verification.md#closing-the-loop)).
- **Prevention:**
  - Give the agent verification tools (MCPs for browser, dev tools, test runners)
  - Structure prompts so the agent must *run* verification, not just *describe* it
  - Add "If the agent cannot close the loop, it is guessing. And guessing ships bugs." as a project-level rule
  - Use a second model for review on high-risk features (see Model Reviewing Its Own Work below)
  - At least one end-to-end check beyond unit tests -- unit tests miss what looks right but does not work

### 4. Context Pollution

- **What:** Debugging context from earlier tasks contaminates new analysis.
- **Cause:** Long conversations without `/clear` or subagent isolation. Residual error messages, abandoned approaches, and stale assumptions persist and bias new reasoning. Every token of old context reduces space available for current reasoning.
- **Symptoms:**
  - Agent applies fixes for problems that do not exist in the current task
  - Solutions reference files or patterns from a previous, unrelated task
  - Increasing incoherence as conversation length grows
  - Agent "remembers" constraints only relevant three tasks ago
  - Proposed fixes address symptoms from a previous debugging session
- **Fix:** `/clear` between tasks, subagents for distinct phases (see [context-engineering.md#anti-pattern-context-pollution](context-engineering.md#anti-pattern-context-pollution)).
- **Prevention:**
  - One task per conversation when possible
  - Use worklogs for persistence instead of relying on conversation history
  - Write a session log entry before starting fresh -- clean handoffs before compaction
  - Keep the meta-lane separate from implementation lanes
  - When context runs thin, handle it explicitly: markdown logs, memory files, clean handoffs

### Anchor Files: Compaction-Resistant Rules

- Rules in conversation are vulnerable to context compaction -- the system summarizes, losing specific instructions while preserving the "gist"
- An `anchor.md` file with absolute non-negotiable rules survives compaction because files are re-read, not summarized
- Distinct from CLAUDE.md (general context at session start): anchor.md is a compaction survival mechanism for rules that must never be lost mid-session
- The failure mode: "Your agent does something you explicitly told it not to do 30 minutes ago" -- the instruction was compacted away

*Sources: Before You Do Anything With OpenClaw.md, Things I wish someone told me.md*

### 5. Prompt Entropy

- **What:** Prompts accumulate noise over many edits; instruction count exceeds ~150-200 and performance degrades.
- **Cause:** Design-time instruction bloat from incremental additions without periodic pruning. Distinct from Context Pollution (which is runtime noise) -- Prompt Entropy is accumulated instruction noise in the prompt itself.
- **Symptoms:**
  - Task success rate drops after prompt edits
  - Agent follows some instructions but ignores others
  - Adding more instructions makes output worse, not better
- **Fix:** Shorten and merge instructions; refresh the session. Periodically audit CLAUDE.md and skill files for redundant or contradictory rules.

### 6. Over-Automation Collapse

- **What:** Over-trust in unverified automated steps causes slow progress and strange loops.
- **Cause:** The agent takes actions without human checkpoints, compounding errors silently. Each unverified step builds on the previous unverified step.
- **Symptoms:**
  - Agent takes many actions but makes no real progress
  - Strange loops where the agent undoes and redoes work
  - Silent error accumulation across automated steps
- **Fix:** Insert human approval gates at critical steps; human-in-the-loop for irreversible actions. Roll back agent actions to last safe commit when detected.

### 7. State Corruption

- **What:** Memory entries or CLAUDE.md become outdated, causing contradictory answers.
- **Cause:** Persistent files (CLAUDE.md, MEMORY.md, skills) are not maintained as living documents. Old information sits alongside new information without reconciliation.
- **Symptoms:**
  - Claude gives conflicting answers to the same query across sessions
  - Agent references outdated conventions or deprecated APIs
  - Contradictions between different memory sources
- **Fix:** Version-pin knowledge ("truth as of v3.5"), run manual audit loops, and re-feed correct information. Treat CLAUDE.md as a living document to prevent the "stale file" trap.

*Source: deep-research-report.md*

---

## AI-Specific Anti-Patterns

### Catfish Code (looks good on surface, broken underneath)

Happens when the prompt lacks technical specificity. The AI fills architectural gaps by guessing, and its guesses pattern-match on common structures without satisfying actual requirements. When AI has to guess architecture, you are more likely to get code that "looks good at first glance, but when you look deeper, it is disgusting."

The fix: detailed prompts with exact tech stack, documentation links, and explicit "do not" constraints. The three-section prompt pattern -- (1) task with technical detail, (2) background information and docs, (3) "do not" section -- consistently produces better results than vague requests (see [prompt-engineering.md#core-principle-specificity-is-everything](prompt-engineering.md#core-principle-specificity-is-everything)).

### Scope Creep by AI (implementing features you did not ask for)

Without explicit milestones, the agent gold-plates -- adding CAPTCHA to a rate limiter, refactoring adjacent code, building abstractions nobody requested. Milestones in a worklog are the boundary. When the agent finishes M2, it stops. New scope requires explicit human approval. If you want to add scope, you approve it; the agent does not decide on its own.

### Over-Engineered Worklogs (787 lines for a 2-field change -- the Linus Torvalds Test)

A 787-line plan for adding two fields and an if-statement. It had "Constitutional Invariants," "Decision Traces with formal statuses," "Forward Compatibility Considerations," and a Risk Assessment that said "low risk" five different ways. After the Torvalds review: 136 lines. Commits: 7 became 4. The technical content stayed the same.

The irony: the same AI that helps you write thorough worklogs will happily write *too* thorough worklogs. It loves to perform expertise. The smell test:

- Worklog longer than 100 lines for a simple task -- cut sections, not detail
- More than 5 commits planned -- merge related changes
- Invariants for a UI-only change -- delete the Invariants section
- You are proud of how thorough it looks -- you have over-engineered it

Target 50-100 lines for most features. If the plan is longer than the implementation will be, cut it down.

### Model Reviewing Its Own Work (same blind spots in write and review)

Claude implemented a 400-line organizer attendee list. It ran a full nine-persona review -- Security, UX, Test, all of them. Every single one approved.

Then Codex found it in 30 seconds: `useEffect` did not reset state when `eventId` changed. The component would show attendees from the previous event while new data loaded -- leaking names and emails. All 1333 tests passed after the fix. But it almost shipped with a data leak.

Personas are powerful, but they normalize what they have been staring at. The same AI that writes code may carry the same blind spots when reviewing it. For high-risk features (PII, payments, auth), enforce model diversity: one AI implements, a different AI reviews. Humans stay in the loop for anything with irreversible consequences (see [testing-verification.md#the-feedback-loop-how-systems-get-smarter](testing-verification.md#the-feedback-loop-how-systems-get-smarter)).

### Kitchen-Sink Skills (1400-line skills that match everything)

Skills that cover every edge case flood the context window with irrelevant instructions, drowning out what matters for the current task. A skill that matches everything helps nothing. The fix: narrow, focused skills -- one concern per file, loaded explicitly when needed. "Load skills for everything, no matter how small" -- but the skills themselves must be small (see [skills.md#thin-skills-principle](skills.md#thin-skills-principle)).

### Model-Task Mismatch: Wrong Tier for the Job

- Using an expensive reasoning model (e.g., Opus) for routine tasks -- file existence checks, heartbeat pings, syntax validation -- burns tokens at 20-40x the necessary rate
- The fix is tiered model configs: cheap/fast model (Haiku) for routine work, mid-tier (Sonnet) for coding, expensive (Opus) reserved for complex debugging or multi-step reasoning failures
- One practitioner dropped daily token spend from 40,000 to 1,500 by routing correctly
- The inverse also fails: models that produce articulate chat responses can be terrible at tool calling -- they generate malformed JSON and hallucinate function names (see [workflow-patterns.md#model-selection-strategy](workflow-patterns.md#model-selection-strategy))
- Test any model with three sequential tool calls before deploying it for autonomous work; if it cannot chain tool calls without hand-holding, do not use it for agent tasks

*Source: I Burnt $127 in API Credits Before I Fixed These OpenClaw Mistakes.md*

### Chat Quality vs Agent Quality Mismatch

- A model's conversational quality is a poor predictor of agent task performance -- tool calling is a fundamentally different capability
- Documented: DeepSeek Reasoner excels at reasoning but is "terrible at tool calls"; GPT-5.1 Mini is cheap but "useless" for agent tasks
- Diagnostic: test any model with three sequential tool calls before deploying for autonomous work
- Extends Model-Task Mismatch beyond cost to capability: capable-sounding models may be incompatible with agent task types

*Source: Things I wish someone told me.md*

### Loop Trap: Agent Repeats the Same Failed Fix

- Without explicit anti-loop rules, an agent will retry the same failing approach indefinitely, burning tokens on each iteration
- The pattern: agent hits an error, tries a variation, hits the same error, tries another variation -- sometimes 8+ cycles before a human notices
- The fix is a hard skill rule: "If you see the same error twice, stop and ask me. Do not try a third variation."
- Every assumption the agent makes without checking workspace files (USER.md, schema docs, config) is a potential loop trigger -- the agent guesses, fails, guesses differently, fails again
- Related to Premature Completion: the agent is "doing work" but never verifying whether its approach is viable before iterating (see [failure-patterns.md#premature-completion](#2-premature-completion))

*Source: I Burnt $127 in API Credits Before I Fixed These OpenClaw Mistakes.md*

### Integration Overload: Configuring Everything at Once

- Setting up multiple integrations simultaneously (email, calendar, Telegram, web scraping, reporting) makes failures undiagnosable -- you cannot tell which integration is broken
- One working end-to-end workflow beats five half-configured ones; get a single integration running reliably before adding the next
- Every new integration is a new failure mode with its own config, auth, and error surface
- When "the agent is stupid," run diagnostics first (`openclaw doctor --fix`) -- half of apparent agent failures are actually config problems
- The compounding effect works in reverse too: broken integrations pollute each other's context, making the agent worse at everything rather than just the broken part

*Source: I Burnt $127 in API Credits Before I Fixed These OpenClaw Mistakes.md*

### Pay-Per-Use Cost Trap

- New users default to Anthropic console pay-per-use pricing, then run multiple agents or experiments without cost guardrails -- one practitioner burned $800 before switching to flat-rate membership
- Running multiple agents on different providers simultaneously (Kimi, Opus, various API tiers) multiplies costs without improving results because context is fragmented across instances
- The fix: start with a flat-rate membership (Claude Pro/Max), use the membership token rather than an API key, and run a single well-configured agent rather than a squad of confused ones (see [autonomous-agents.md](autonomous-agents.md))

*Source: I wasted 80 hours and $800 setting up OpenClaw - so you don't have to.md*

### Empty Context Files: The Silent Degradation

- Leaving SOUL.md, USER.md, and MEMORY.md empty or unfilled causes the agent to behave like a generic chatbot -- it has no identity, no user context, and no accumulated knowledge
- One practitioner described the difference after filling out workspace files as "night and day"
- Related failure: installing the memory skill (QMD) midway through usage causes the agent to reset or lose chat logs -- memory infrastructure must be installed before conversations begin, not after
- The fix: fill out workspace identity files before the first real task, and install memory tooling during initial setup, not as an afterthought (see [memory-persistence.md](memory-persistence.md))

*Source: I wasted 80 hours and $800 setting up OpenClaw - so you don't have to.md*

### Compaction Amnesia: Context Window Eats Un-Persisted Knowledge

- Distinct from Context Pollution: compaction amnesia occurs when the system actively summarizes or removes older messages to stay within token limits, destroying knowledge that was never written to disk
- One practitioner spent 20 minutes explaining a database schema; the agent compacted and hallucinated a replacement schema, nearly dropping a production table
- Even MEMORY.md content loaded at session start can get summarized away during long sessions -- the agent forgets mid-conversation because compaction removed context and nothing triggered a reload
- The fix is persistence discipline: state files (JSON/YAML) for task status, workspace docs for stable context, decision logs for architectural choices -- anything the agent must remember beyond the current window must exist on disk (see [memory-persistence.md#layer-2-worklogs-feature-scoped-session-to-session](memory-persistence.md#layer-2-worklogs-feature-scoped-session-to-session))
- Long-running thinking sessions are inherently fragile: they break, they cost money, and they hallucinate as context degrades

*Sources: I Burnt $127 in API Credits Before I Fixed These OpenClaw Mistakes.md; Give your Openclaw the Memory it Needs (Full Guide).md*

### OpenClaw Delegation Failure Pattern

A practitioner's documented experience with multi-step autonomous agent delegation, illustrating systemic failure modes.

- **Delegation framework overhead:** 40+ hours building standards, accountability, workspace hygiene, commit cadences, capability logs -- minimal payoff. The framework itself became a workload
- **Regressions as common as successes:** "2 steps forward, 1 step back" -- constant micromanagement required despite well-defined 3-phase, 10-step "definition of done"
- **200K context forgetting:** Agent forgets ~80% of processes multiple times per day despite documented procedures. Context window size does not equal reliable recall
- **Agents are tools, not workers:** Installing OpenClaw creates a massive workload for the operator. The fantasy of autonomous execution doesn't match reality for complex multi-step processes
- **Realistic expectations:** Success stories on social media likely involve unreported technical support, personal time investment, or exaggeration. Set expectations accordingly

(see [autonomous-agents.md](autonomous-agents.md) for cost optimization and architecture that mitigates these issues)

*Source: Twitter Bookmarks/2026-03-02-bradmillscan-trying-to-get-openclaw-agents.md*

### Debunked and Outdated Practices

Practices once considered effective but now proven counterproductive:

- **"Load everything into CLAUDE.md"** -- LLMs have a limited instruction window (~150-200 instructions before performance degrades); overly long CLAUDE.md dilutes relevance. Use retrieval tools for detailed knowledge instead
- **"Claude as linter/code style enforcer"** -- LLMs excel at reasoning, not formatting enforcement. Rely on ESLint/Prettier locally; ask Claude about logic or design questions only
- **"/init-generated CLAUDE.md is enough"** -- Auto-generated instructions tend to be generic and misaligned. Must be manually curated, focusing on what truly matters
- **"One-session mastery"** -- Long unbranched conversations lead to drift. Break tasks into mini-sessions or subagents; fresh contexts with summaries are more reliable (see [Context Pollution](#4-context-pollution))
- **"Tokens don't matter / always use Sonnet"** -- Model costs vary significantly; defaulting to the strongest model is wasteful. Token-budget tasks by routing to appropriate model tiers
- **"Claude remembers between runs"** -- False without explicit memory tools or CLAUDE.md. Must re-provide state via notes, memory plugins, or handoffs each session (see [memory-persistence.md](memory-persistence.md))

*Source: deep-research-report.md*

### LLM Training Data Staleness (Skills Must Contain Ground Truth)

- Most LLMs have outdated information baked into training data -- API pricing tiers, rate limit structures, endpoint availability, and access levels that no longer exist
- Documented case: the X API moved from subscription tiers (Basic/Pro/Enterprise at $200/mo) to pay-per-use credits, but LLMs confidently reference the old system. Users whose agents referenced "enterprise-only" features that are actually available on pay-per-use were blocked from using them
- **The pattern generalizes:** any skill that references external APIs, pricing, rate limits, or access levels must contain current ground truth in the skill itself -- do not rely on the LLM's training data for this information
- Related to Plausible Echo: the agent confidently states old pricing because it pattern-matches on training data, and the output looks authoritative. The user trusts it because it is specific and formatted well (see [Plausible Echo](#3-plausible-echo))
- **Fix:** embed accurate reference data directly in skills or skill reference files. Treat LLM knowledge of API details as unreliable by default. When a skill wraps an external service, include a `references/` directory with current API docs that the agent reads instead of guessing

### Dashboard Trap: Catch Exceptions, Don't Build Dashboards

From enterprise agent deployments ($3M ARR):

- **The Anti-Pattern:** Default instinct is to create dashboards that surface information. Dashboards are where problems go to die -- your team already knows the problems exist, and another system to check adds overhead without forcing resolution
- **The Fix -- Catch and Route:** When an exception occurs, immediately flag it, identify who needs to act, route to them with full context (vendor, amount, policy, missing docs), and block the transaction until resolved
- **Escalation Pattern:** If a deal approval sits >24 hours, escalate automatically with deal context -- don't wait for weekly review
- **Contingency Triggers:** When a supplier misses a milestone, trigger the contingency playbook before anyone manually notices
- **Core Principle:** "Your AI Agent's job is to make problems impossible to ignore and incredibly easy to resolve."
- Only build dashboards once the problem is mitigated to near 100%

Complements [Premature Completion](#2-premature-completion) -- both are about agents that stop short of forcing resolution.

*Source: Twitter Bookmarks/2026-01-11-vasuman-100x-a-business-with-ai.md*

### Concurrent File Editing Race Condition

Critical failure mode when multiple sub-agents edit shared state files:

- **Problem:** The `edit` tool requires exact text matching. When two sub-agents modify the same file concurrently, one fails silently because the content it expects no longer matches
- **Solution -- append-only state:** Split task state into two files: `AUTONOMOUS.md` (main session only, read-write) + `tasks-log.md` (append-only for sub-agents). Sub-agents never edit shared state, only append
- **Design principle:** Mirrors Git's commit log -- never rewrite history, only append. Eliminates race conditions entirely
- **Token budget rule:** Keep the frequently-loaded state file under 50 lines to avoid token waste on every heartbeat cycle
- Applies to any multi-agent workflow with concurrent file access -- not limited to task management

(see [agent-design.md](agent-design.md#subagents-in-claude-code) for sub-agent architecture)

*Source: awesome-openclaw-usecases/usecases/overnight-mini-app-builder.md*

---

## Security Failure Patterns

### API Key Exposure (pasting keys into AI input = plaintext on provider servers)

Every API key pasted into an AI agent's input box hits the provider's servers in plaintext. OpenAI keys, Telegram tokens, AWS credentials -- the agent needed them to write a config file, so you pasted them in. Now they are in the provider's logs, training data, or worse. This is not hypothetical; it is the default behavior of every hosted AI tool. Never paste secrets into chat.

### Prompt Injection (exposing your agent to untrusted input sources)

If the agent reads public replies, group chats, or inbound emails, anyone can inject instructions. If the agent has admin access, a prompt injection gives the attacker that same access. Do not put your agent in group chats. Do not have it read tweet replies. Do not expose it to any channel where untrusted users can send text until you have hardened guardrails in place.

### Admin Access Blast Radius (bot has access to everything on the machine)

The agent has access to everything on your computer -- passwords, API keys, logged-in sessions, email, social media. If compromised via prompt injection or otherwise, the blast radius is total.

| Mitigation | Effect |
|---|---|
| Dedicated device (old laptop, Mac Mini) | Limits blast radius to one machine |
| Separate accounts for the agent (e.g., its own GitHub) | No elevated privileges on your real accounts |
| No browser sessions with sensitive logins | Agent cannot access what is not there |
| Approval gates before external actions | Human confirms tweets, emails, deployments |
| Think before every prompt | "Will this expose my agent to untrusted input?" |

Best practice: "We recommend NOT giving it any keys or tokens or access -- we made ours its own GitHub account so it can submit PRs but not with elevated privs."

### Silent Session Replacement

- Background automations (cron jobs, heartbeats) can silently hijack the main session pointer when not in isolated sessions, causing apparent "amnesia"
- Documented: 5 of 10 main sessions over 11 days were spawned by crons/heartbeats targeting `sessionTarget: "main"` instead of `"isolated"`
- Platform updates can introduce phantom required files (e.g., WORKFLOW_AUTO.md); compaction checks for non-existent files can spawn new sessions
- Agent directory duplication: updates create a second directory; gateway routes to new one without migrating history; old directory continues receiving auth writes
- Diagnosis requires forensic session audit: check session creators, search for phantom files, audit cron targets, check for duplicate directories
- Fix: ensure all crons/heartbeats use `sessionTarget: "isolated"`; create platform-expected files (even empty); audit for duplicate directories
- Distinct from Compaction Amnesia: this is a completely different session masquerading as the original
- (see [autonomous-agents.md](autonomous-agents.md) for cron session routing)

*Source: Thread by @bradmillscan.md*

### Agents of Chaos: Multi-Agent Security Vulnerabilities

- 2026 red-teaming study on OpenClaw with 6 Opus-powered agents documented 11 critical vulnerability categories over 20 days
- Social engineering bypassed all access controls; semantic reframing defeated safety rules (refused to "share" but "forwarded" entire emails)
- Identity hijacking via display name spoofing: changing a Discord username to match the owner's name convinced an agent to rename itself and reassign admin privileges
- Multi-agent risk amplification: compromised states spread between agents, turning isolated failures into coordinated cascades
- Emotional manipulation bypassed hardcoded safeguards: sustained guilt-tripping convinced agents to comply with restricted actions
- (see [autonomous-agents.md](autonomous-agents.md) for the full study summary)

*Source: Thread by @BrianRoemmele.md*

### agent-vault: The Placeholder Pattern (`<agent-vault:key>` substitution)

AES-256 encrypted local storage. The agent reads config files and sees placeholders. Real values are swapped in on disk but never enter the AI provider's context. The agent sets everything up perfectly -- it just never sees your secrets.

```
What the agent sees:      api_key: <agent-vault:openai-key>
What is actually on disk:  api_key: sk-proj-abc123...
```

### Agent Security Threat Model: 6 Attack Classes

Comprehensive threat taxonomy for AI agents. Extends existing security failure patterns with named attack classes.

- **Transitive Prompt Injection:** A skill links to external documentation. The external repo gets compromised. The LLM reads the injected content with the same authority as your own config. Mitigation: inline content instead of linking, or add reverse injection guardrails after external links
- **MCP Tool Poisoning ("Rug Pull"):** An MCP tool registers with a clean description, you approve it. Later the tool definition is dynamically amended with hidden instructions. You already approved the tool -- the new payload bypasses all permission prompts. Mitigation: pin MCP tool versions, verify descriptions haven't changed between sessions
- **Memory Poisoning (Temporal Fragmentation):** Malicious inputs fragmented across time, written into persistent memory files (MEMORY.md, SOUL.md, session files). Each fragment is harmless alone -- they combine later into a functional payload that survives restarts. The agent equivalent of a logic bomb. Palo Alto Networks identified this as a fourth amplifying factor beyond standard attack categories
- **Sleeper Payloads:** Community skills that work perfectly for weeks, then activate on a trigger condition (specific date, file pattern, environment variable). Extremely difficult to catch in review. 341 malicious skills documented in the ClawHavoc incident used this pattern
- **Adversarial Pipeline:** Organized communities develop jailbreaks on abliterated models (safety-removed fine-tunes from HuggingFace), refine against production models, then deploy. Payloads include runic encoding, binary-encoded function calls, semantic inversion, and persona injection -- all model-specific. Defense is centralized (a few labs); offense is distributed (global community iterating 24/7)
- **OWASP Top 10 for Agentic Applications (2026):** Industry-standard risk framework: ASI01 Goal Hijacking, ASI02 Tool Misuse, ASI03 Identity/Privilege Abuse, ASI04 Supply Chain, ASI05 Unexpected Code Execution, ASI06 Memory/Context Poisoning, ASI07 Rogue Agents. Palo Alto mapped OpenClaw to every category

(see [autonomous-agents.md](autonomous-agents.md#miniclaw-philosophy-single-access-point-architecture) for the security-first alternative architecture)

*Sources: everything-claude-code/the-openclaw-guide.md, everything-claude-code/the-security-guide.md*

### CI/CD Silent Failures and Telemetry Traps

Failure patterns specific to Claude Code in CI/CD environments that fail silently rather than loudly:

- **Silent OTEL collector failure:** When the OpenTelemetry collector endpoint is unreachable, Claude Code does not error -- telemetry silently drops. Always verify endpoint with `curl http://localhost:4317` before debugging missing metrics
- **Claude Code hang after telemetry enable** is a known issue requiring clean reinstall + cache clear (`rm -rf ~/.config/claude-code/`). Not a code bug -- a state corruption from partial telemetry config
- **Telemetry cost metrics are approximations only** -- teams that rely on telemetry for budgeting without cross-referencing official billing (Anthropic Console/AWS/GCP) risk budget overruns
- **CI/CD prompt injection as distinct attack surface:** When Claude processes PRs/issues from external contributors, untrusted input enters the agent's context (see [tools-and-integrations.md](tools-and-integrations.md#prompt-injection-defense-layers-in-cicd) for defense layers)
- **Non-write user bypass** (`allowed_non_write_users: "*"`) is a "significant security risk" -- wildcard access without permission scoping creates an open escalation path

*Sources: claude-code-action/docs/security.md, claude-code-monitoring-guide/troubleshooting.md*

---

## The Fix Protocol

For Every Failure: **Catch -> Name -> Update Skill -> Prevent Recurrence**

| Step | Action | Artifact |
|---|---|---|
| **Catch** | Notice the failure while it is happening, not after | Surprise logged in worklog |
| **Name** | Give it a precise, reusable label | Pattern added to this document |
| **Update Skill** | Encode the fix so the agent applies it automatically next time | Skill file updated (see [skills.md](skills.md)) |
| **Prevent** | Add structural guardrails (prompt rules, verification steps, context separation) | CLAUDE.md or prompt template updated (see [prompt-engineering.md](prompt-engineering.md)) |

Anytime the agent messes up: "Hey, pause right there. Build a new skill that solves this problem." Surprises get logged in the worklog, then immediately compressed into skills while the context is fresh. If you wait until "later," you forget the nuance.

### Structured AI Debugging Methodology

An 8-step diagnostic process for when Claude behaves unexpectedly, complementing the Catch -> Name -> Update Skill cycle:

1. **Identify symptom:** Is it hallucination, omission, or wrong format? Document the exact prompt and output
2. **Think/Plan mode inspection:** Ask Claude to explain its reasoning step by step; check if any step contradicts instructions
3. **Ablation testing:** Iteratively remove or alter prompt parts one at a time to isolate the cause -- a prompt "unit test"
4. **Context pollution check:** Start a fresh session with just the problem prompt; if output improves, stray info was the culprit (see [Context Pollution](#4-context-pollution))
5. **Instruction conflict resolution:** Check for contradictory instructions between CLAUDE.md, prompt, and agent team outputs
6. **Distinguish limits vs bugs:** Test with simpler examples; if ideal prompt also fails, it may be a model limitation rather than a fixable bug
7. **Iterate with evidence:** Provide evidence to rebut hallucinated facts; add explicit examples of correct format
8. **Tool misuse check:** Verify that plugin outputs (curl, browse, terminal) are parsed correctly

*Source: deep-research-report.md*

The goal is not to prevent all failures. The goal is to ensure no failure happens the same way twice.

### Troubleshooting Taxonomy: Three Problem Types

A practical classification for diagnosing issues, especially useful for non-coders:

| Type | What It Looks Like | Strategy |
|------|--------------------|----------|
| **Type 1: Errors** | Red text, error messages, stack traces, crashes | Read the error (first line = actual problem, find your file names, ignore internal stack trace). Translate to plain English. |
| **Type 2: Wrong Results** | Code runs but output is incorrect (wrong color, wrong position, missing feature) | Use What-Why-Constraints to describe the gap between expected and actual behavior. Be specific about what is wrong. |
| **Type 3: Confusion** | Do not understand what is happening or what Claude did | Ask for a debrief in plain English. Request analogies, examples, increasing detail. Do not proceed until it makes sense. |

Each type requires a different approach. Misidentifying the type wastes time -- errors need error-reading skills, wrong results need specific feedback, confusion needs explanation.

### Error Reading Framework

A non-coder's guide to reading error messages without panic:

1. **Read the first line or two** -- that is the actual problem. Everything else is context.
2. **Look for your file names and line numbers** -- e.g., `User.js:23` means line 23 of User.js. Ignore files in `node_modules/` or internal paths.
3. **Translate common terms:** "undefined" or "null" = trying to use something that does not exist. "TypeError" = wrong kind of data. "SyntaxError" = typo or formatting mistake.
4. **Provide context to Claude:** "I was trying to [what you requested]. Here's the error: [paste]." Context + error gives Claude everything it needs.

Complements the 8-step diagnostic process (see [above](#structured-ai-debugging-methodology)) by providing the entry-level error-reading skill that feeds into systematic diagnosis.

### Personal Troubleshooting Script Template

A reusable checklist organized by problem type:

**When I see an error:**
1. Read the first line -- what is the actual message?
2. Look for my file names (ignore internal/node_modules)
3. Provide context: "I was trying to [action]. Here's the error: [paste]"
4. Review what changed: "Show me what code was actually changed"
5. Ask for plain English explanation and fix

**When the result is wrong:**
1. Use What-Why-Constraints to describe the gap (see [prompt-engineering.md#what-why-constraints](prompt-engineering.md#what-why-constraints))
2. Be specific about the gap between expected and actual
3. Ask Claude to verify understanding before fixing
4. Narrow the scope to the specific component or section

**When I am confused:**
1. Ask for debrief in plain English
2. Request multiple formats (analogies, examples)
3. Ask for increasing detail
4. Request foundational concepts
5. Do not move forward until it makes sense

*Source: Learning CC/notes/module-6-reflection.md*

