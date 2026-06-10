# Testing & Verification

## Core Principle: Verify Artifacts, Not Self-Reports

An AI saying "done" means nothing. The artifact is the proof.

When an agent reports "all tests pass," that is a prediction, not evidence. It may have hallucinated output, skipped edge cases, or tested the wrong thing. The only way to know is to run the test, check the browser, curl the endpoint, or read the log yourself.

**Treat every "done" as a hypothesis until you observe the result yourself** (see [failure-patterns.md#2-premature-completion](failure-patterns.md#2-premature-completion)).

The standard: "Would a staff engineer approve this without seeing proof?" If not, the agent has not finished.

### Four-Level Verification Hierarchy: Exists -> Substantive -> Wired -> Functional

Four levels of artifact verification, each building on the previous: Exists (file present) -> Substantive (real implementation, not placeholder) -> Wired (connected to rest of system) -> Functional (actually works). Levels 1-3 are programmatic; level 4 often requires human.

- **Universal stub detection:** comment-based stubs (TODO/FIXME/placeholder), empty implementations (return null/undefined/{}), hardcoded values where dynamic expected, log-only functions
- **Wiring verification:** Component->API (fetch call exists and uses response), API->Database (query exists and result returned), Form->Handler (onSubmit calls API), State->Render (state vars in JSX)
- **Per-artifact-type checklists:** React components, API routes, database schemas, hooks/utilities, environment variables -- each with existence, substantive, stub, and wiring checks
- **Human verification triggers:** visual appearance, user flow completion, real-time behavior (WebSocket/SSE), external service integration, error message clarity
- **Red flag patterns:** React stubs (`return <div>Component</div>`), API stubs (Response.json with no DB query), schema stubs (models with only id field)

*Source: get-shit-done/get-shit-done/references/verification-patterns.md*

### Context Window as Verification Risk Factor

- LLM performance degrades as context fills -- verification steps added late in a session may execute less reliably
- "Kitchen sink session" anti-pattern: mixing unrelated tasks fills context with irrelevant information, degrading verification quality
- After two failed corrections on the same issue, clear context and restart -- accumulated failed approaches pollute verification signal
- Subagents for verification: run verification in a separate context window so verifier is not biased by implementer's context
- (see [Core Principle](#core-principle-verify-artifacts-not-self-reports) -- self-reports become less reliable in degraded context)

*Source: Best Practices for Claude Code.md*

### Three-Tier Artifact Checks and Wiring Verification (GSD)

Implementation-level verification patterns extending the four-level hierarchy above:

| Tier | Check | Catches |
|------|-------|---------|
| EXISTS | File present at expected path | Missing files, wrong directory |
| SUBSTANTIVE | Has real implementation: `min_lines`, expected `exports`, `contains` regex | Placeholder files, stub implementations, TODO-only files |
| WIRED | Components connected to each other with line-level evidence | Files exist independently but are never imported/called |

- **Key Link Verification:** Checks that components are actually connected (e.g., "Line 23: `fetch('/api/chat')` with response handling") -- not just that both files exist. The most common AI failure mode is creating files that work in isolation but are never wired together
- **No 3 consecutive tasks without automated verification** -- practical application of the Nyquist principle
- **Wave 0 concept:** Test scaffolding tasks that must complete before any implementation, ensuring feedback mechanisms exist before code is written

**UAT Diagnosis Pipeline:**
- **Severity inference from natural language:** System never asks user to rate severity -- infers from word choice ("crash" = blocker, "works but..." = minor)
- **Gap YAML feeds into planning:** `plan-phase --gaps` consumes structured gap data to create targeted fix plans -- closed loop from failure through diagnosis to remediation

**Anti-Pattern Detection Table:**
- Specific targets for AI-generated code: TODO comments, placeholder divs, missing files referenced in imports, empty function bodies
- **"Looks Done But Isn't" checklist:** Verification pattern targeting the gap between demo-ready and production-ready
- Verification report outputs structured fix plan recommendations ready for the planner agent to consume

(see [workflow-patterns.md](workflow-patterns.md#gsd-planning-templates-must-haves-contract-and-wave-orchestration) for the must-haves contract these verify against)

*Sources: get-shit-done/templates/VALIDATION.md, get-shit-done/templates/UAT.md, get-shit-done/templates/verification-report.md*

### Mandatory Completion Verification via Subagent

- Hard enforcement: "If you haven't run the verification tool in this message, you cannot claim the change works"
- Verification tools that take 1-30 minutes: spawn in a subagent; main thread must never idle while it runs -- always continue working on other tasks
- Spawn one subagent per feature concurrently when testing multiple features
- Re-run is always a new subagent spawn -- never block the main thread on re-verification
- Write test instructions adversarially: think like a user trying to break the feature, not confirming it renders
- Completion checklist at end of skill (peripheral position) -- the last thing read before acting
- (see [testing-verification.md](testing-verification.md#core-principle-verify-artifacts-not-self-reports) for the foundational verification principle)
*Source: expect/.agents/skills/expect/SKILL.md*

---

## The Plausible Echo Problem

### What It Is

AI output that looks correct but was never executed. The code compiles in your head. The function names make sense. But it was never run. Most people "cannot distinguish a real result from a plausible echo of one, because they're looking at the self-report instead of the artifact" (see [failure-patterns.md#3-plausible-echo](failure-patterns.md#3-plausible-echo)).

### Why It Fools You

- Pattern-matching on surface correctness. The code *looks* like code that works.
- AI models are trained to produce plausible output, not verified output.
- "Catfish code" -- code that looks good at first glance but is broken underneath.
- The longer the context, the more confidently the agent asserts completion.

### The Fix: At Least One End-to-End Verification Per Feature

Do not trust static reading. Execute the artifact. One happy-path E2E test plus one edge case is the minimum bar. If the feature touches payments, auth, or data integrity, raise the bar.

---

## Invariants vs Requirements

### Requirements Are Vague

"Must handle rate limiting properly." -- This tells the agent nothing testable. "Properly" is not a verifiable condition.

### Invariants Are Verifiable

```
INV-1: A single email cannot receive >5 magic links per hour.
INV-2: A single IP cannot request >10 magic links per hour.
```

An invariant has a specific number, a specific condition, and a binary outcome. Either the system enforces it or it does not. No judgment call required.

### When to Write Invariants

Write them for any domain where "almost right" ships a bug:
- **Payments** -- charge amounts, refund windows, duplicate transaction guards
- **Authentication** -- session lifetimes, token expiration, rate limits
- **PII** -- what data leaves the system, who can access what
- **Rate limiting** -- per-user, per-IP, per-endpoint thresholds
- **Data integrity** -- foreign key constraints, uniqueness guarantees, cascade behavior

### When to Skip

- UI-only changes (color, layout, copy)
- Simple CRUD with no business logic
- Refactors that do not change external behavior

### Pre-Implementation Validation Mapping (Nyquist Layer)

A verification pattern that maps automated test coverage to requirements BEFORE any code is written, closing the gap between "code was written" and "code works."

- **Pre-implementation mapping:** During planning/research, detect existing test infrastructure, map each requirement to a specific test command, and identify scaffolding that must be created before implementation begins (Wave 0 tasks)
- **Validation contract:** Output a specification of the feedback mechanism for each requirement -- what test to run, expected pass criteria, how to verify. Store as `VALIDATION.md` alongside implementation plans
- **Plan enforcement:** Treat validation coverage as a mandatory planning dimension. Plans where tasks lack automated verify commands should not be approved
- **Purpose:** Ensures that when a task is committed, a feedback mechanism already exists to verify it within seconds
- **Toggle for prototyping:** Disable for rapid prototyping phases where test infrastructure is not the focus; re-enable before shipping

(see [workflow-patterns.md](workflow-patterns.md) for the GSD wave execution pattern)

*Source: get-shit-done/docs/USER-GUIDE.md*

### Template

```
INV-[number]: [verifiable statement with specific numbers/conditions]
```

Examples:
- `INV-3: A deleted user's PII is purged from all tables within 24 hours.`
- `INV-4: No API response includes a user's email unless the requester owns the account.`
- `INV-5: Payment webhook retries stop after 5 attempts with exponential backoff.`

### Goal-Backward Plan Verification: 8-Dimension Framework

Goal-backward verification works backwards from the phase outcome to verify plans achieve it -- "plan completeness does not equal goal achievement."

- Eight verification dimensions: requirement coverage, task completeness, dependency correctness, key links planned, scope sanity, verification derivation, context compliance, Nyquist compliance
- Scope thresholds: 2-3 tasks/plan target (4 warning, 5+ blocker); 5-8 files/plan target (10 warning, 15+ blocker)
- Key links verification: checks that artifacts are wired together (component calls API, API queries DB), not just created in isolation
- Must-haves must be user-observable truths ("user can log in"), not implementation details ("bcrypt installed")
- Anti-patterns: don't check code existence (that's the verifier's job), don't accept vague tasks, don't skip dependency analysis

(see [Pre-Implementation Validation Mapping](testing-verification.md#pre-implementation-validation-mapping-nyquist-layer))

*Source: get-shit-done/agents/gsd-plan-checker.md*

---

## Binary Pass/Fail Criteria

### Good

```
"User sees dropdown with options: all, high, medium, low."
"Clicking filter 'high' shows only high-priority tasks."
"Hitting the endpoint 6 times returns 429 on the 6th request."
```

### Bad

```
"Make it look good."
"Handle errors properly."
"It should work well on mobile."
```

### The Test

Could a different AI evaluate this criterion without asking you a question? If the success condition requires human taste or subjective judgment, it is not a pass/fail criterion. Rewrite it until a machine can check it.

### How Ralph Uses This

Each atomic task in the Ralph loop has a binary pass/fail test. The agent builds, checks, and saves only if the test passes. If it fails, the agent logs what went wrong and moves on. No ambiguity, no partial credit (see [workflow-patterns.md#pattern-2-the-ralph-loop-autonomous-coding](workflow-patterns.md#pattern-2-the-ralph-loop-autonomous-coding)).

The insight: vague success criteria cause the agent to guess when it is done. Binary criteria eliminate that guessing.

### Eval Metrics: pass@k vs pass^k

Two complementary metrics for measuring agent task success across multiple attempts, useful for quantifying reliability beyond simple pass/fail.

- **pass@k** -- at least ONE of k attempts succeeds. Example: k=1 yields 70%, k=3 yields 91%, k=5 yields 97%. Use when you just need the task to work (most development tasks, exploratory coding)
- **pass^k** -- ALL k attempts must succeed. Example: k=1 yields 70%, k=3 yields 34%, k=5 yields 17%. Use when consistency is essential (CI/CD pipelines, production automation, deterministic outputs)
- **Checkpoint-based evals:** Set explicit checkpoints within a task, verify against defined criteria, fix before proceeding to the next checkpoint
- **Continuous evals:** Run every N minutes or after major changes; full test suite plus lint
- **Skill benchmarking technique:** Fork a conversation, run one instance with a skill and one without (using a worktree), diff outputs to measure skill impact

(see [workflow-patterns.md](workflow-patterns.md) for verification gate patterns)

*Source: everything-claude-code/the-longform-guide.md*

### Pre-Build Validation Gate with Real Data Sources

Validation gate that prevents building solutions to already-solved problems:

- **Tool:** `idea-reality-mcp` MCP server queries GitHub, Hacker News, npm, PyPI, Product Hunt in real time
- **Output:** `reality_signal` score (0-100) based on repository counts, star distributions, HN discussion volume
- **Decision thresholds:** >70 = STOP and discuss pivot directions; <30 = proceed; 30-70 = investigate further
- **Key value:** Score is based on real metrics, not LLM guessing -- prevents the most expensive agent mistake: "solving a problem that's already been solved"
- Pattern applies to any autonomous system: validate assumptions with external data before committing resources

(see [workflow-patterns.md](workflow-patterns.md#requirements-driven-phase-derivation) for how validated ideas flow into phase planning)

*Source: awesome-openclaw-usecases/usecases/pre-build-idea-validator.md*

### Testing Addressed Gate: Deliberation at the Point of Action

- "All tests pass" is vacuously true when no tests exist -- the gate must be: "testing addressed -- new/changed behavior has coverage OR explicit justification for why tests are not needed"
- Deliberate omission is a first-class valid outcome -- the goal is intentional decisions, not forced ceremony
- Three-layer approach: plan-time annotation (annotate why a unit has no test scenarios) → execution-time deliberation ("did this task change behavior? if yes, were tests written?") → review-time detection (flag behavioral diffs with zero test changes)
- "Did you address testing for this task?" is far more targeted than "tests pass"
- Contract tests that verify skills/agents contain required language are a concrete pattern for enforcing workflow correctness
*Source: compound-engineering-plugin/docs/brainstorms/2026-03-29-testing-addressed-gate-requirements.md*

---

## Knowledge Layer Evaluation Framework

A framework for measuring whether your Claude Code knowledge infrastructure (CLAUDE.md, rules, skills, hooks, auto memory, MCP) is actually helping. Distinct from code quality evals (see [EDD](#eval-driven-development-edd)) -- this evaluates the knowledge system itself.

| Metric | What to Measure | Why It Matters |
|---|---|---|
| **Retrieval quality** | Build a 20-50 query known-answer test set spanning build commands, conventions, gotchas, architecture decisions. Validate the right canonical doc is cited (not a stale note). | Conflicts between instruction sources cause arbitrary behavior. |
| **Planning quality** | Track wrong-problem implementations, rewinds per feature, whether plans identify correct files early. | Plan Mode separates exploration from execution -- measure if it's working. |
| **Coding quality** | Patch audits: test pass rate, lint pass rate, code style adherence. | Verification criteria are the highest-leverage improvement to Claude output. |
| **Debugging usefulness** | Median time from first failing test/log to verified fix. | Offloading logs through hooks/subagents should reduce time-to-fix measurably. |
| **Workflow adherence** | Count violations: forgot typecheck, wrong test command, edited protected directory. | Hooks and permissions make adherence deterministic rather than hope-based. |
| **Prompting reduction** | How often you restate build/test instructions or project conventions. | Sessions start fresh -- persistence must come from instruction/memory artifacts. |
| **Maintenance burden** | Track "doc drift" incidents: how often outdated notes cause wrong actions. | Treat CLAUDE.md like code -- review when things go wrong, prune ruthlessly. |

Most teams measure code output quality but never measure whether their knowledge infrastructure is effective. A knowledge layer that decays unnoticed is worse than no knowledge layer -- it creates false confidence.

(see [context-engineering.md](context-engineering.md#scaling-strategy-matrix-when-to-add-complexity) for when to add infrastructure, [failure-patterns.md](failure-patterns.md#4-context-pollution) for what goes wrong)

*Source: deep-research-report-claudecodeknowledgelayer.md*

---

## Closing the Loop

### The Principle

Writing code is not done. Passing a linter is not done. The feature functioning end-to-end in its real environment is done. The worklog's "Closing the Loop" section lists concrete verification steps per milestone; the agent checks each one before advancing.

### Verification Methods by Domain

| Domain | Method |
|--------|--------|
| Web app | Playwright MCP / Browser MCP -- navigate, screenshot, assert |
| API | curl / httpie / test scripts hitting real endpoints |
| CLI tool | Run the command, check stdout/stderr against expected output |
| Mobile | Mobile MCP (iOS + Android) or ADB MCP (Android) |
| Any | Unit tests as baseline (necessary but not sufficient) |

### The Minimum

One happy-path E2E plus one edge case per feature. Unit tests are the floor, not the ceiling. The button that "looks right" but does not submit, the form that validates but does not save -- caught by E2E, not unit tests.

### Web Application Testing: Server Lifecycle and Reconnaissance Pattern

- **with_server.py helper:** Manages server lifecycle for Playwright tests -- starts server(s), waits for port readiness, runs automation script, then tears down. Supports multiple servers (e.g., backend + frontend on different ports). Keeps test scripts focused on Playwright logic only.
- **Decision tree for test approach:** Static HTML -> read HTML directly, identify selectors, write Playwright script. Dynamic webapp (server not running) -> use with_server.py helper. Dynamic webapp (server running) -> reconnaissance-then-action pattern.
- **Reconnaissance-then-action pattern:** (1) Navigate and wait for `networkidle`, (2) Take screenshot or inspect DOM, (3) Identify selectors from rendered state, (4) Execute actions with discovered selectors. Critical: never inspect DOM before `networkidle` on dynamic apps -- you'll get incomplete/wrong selectors.
- **Black-box script usage:** Run helper scripts with `--help` first, invoke as black boxes. Do NOT read source code into context -- these scripts can be large and pollute the context window. They exist to be called, not ingested.

(see [TDD Methodology](testing-verification.md#tdd-methodology-decision-heuristic-and-execution-protocol))

*Source: skills/skills/webapp-testing/SKILL.md*

### Plan Review with Fresh-Context Subagent

- Stress-test plans using a subagent with fresh context to avoid planner bias -- if you helped write the plan, you carry bias that makes gap-finding harder; a fresh reviewer sees it cold
- Six review dimensions: pre-mortem ("it failed 3 months later -- why?"), completeness, feasibility, best-practice alignment, sequencing, specificity
- Red/Yellow/Green classification: Red = critical, will likely cause failure; Yellow = creates risk but can proceed; Green = nice-to-have
- Expert role is inferred from plan content and announced so the user can override
- Web research depth levels: quick (0 searches), standard (2), deep (3-4); distilled into 3-5 relevant principles
*Source: claude-code-synthesis/commands/review-plan.md*

---

## Automated Verification Hooks

Hooks run before or after tool calls to catch problems in real time, without human intervention (see [tools-and-integrations.md#hooks-prepost-tool-automation](tools-and-integrations.md#hooks-prepost-tool-automation) for implementation details).

### TypeScript Type-Checker (PostToolUse)

Runs `tsc --no-emit` after every TypeScript file edit. Catches broken call sites when function signatures change. Adaptable to any typed language; for untyped languages, substitute a test runner.

```json
{ "PostToolUse": [{ "matcher": "edit|write", "command": "npx tsc --no-emit 2>&1 | head -20" }] }
```

### Duplicate Code Prevention (PostToolUse)

Launches a second Claude instance via the SDK to scan a watched directory for duplication after edits. Trade-off: extra time/cost vs. cleaner codebase. Only watch critical directories (`queries/`, `lib/`).

```json
{ "PostToolUse": [{ "matcher": "edit|write", "command": "node ./hooks/dedup-check.js" }] }
```

### .env Protection (PreToolUse)

Blocks reads/writes to sensitive files. Parses incoming JSON for `file_path`; if it includes `.env`, exits with code 2 (block) plus stderr feedback.

```json
{ "PreToolUse": [{ "matcher": "read|grep", "command": "node ./hooks/read_hook.js" }] }
```

### CLAUDE.md as Verification Lever

- Treat CLAUDE.md like code: when things go wrong, review it, prune it, test changes by observing behavior shifts
- Over-specified CLAUDE.md causes Claude to ignore rules -- verification instructions get lost in noise
- Diagnostic: if Claude keeps violating a rule in CLAUDE.md, the file is too long; if Claude asks questions answered in CLAUDE.md, phrasing is ambiguous
- Convert always-needed verification behaviors to hooks (deterministic enforcement) rather than advisory CLAUDE.md
- Emphasis tuning ("IMPORTANT", "YOU MUST") can improve adherence to critical rules
- (see [prompt-engineering.md](prompt-engineering.md) for Instruction Budget ~150-200 max)

*Source: Best Practices for Claude Code.md*

### Production Deployment Patterns for AI-Generated Code

Practices for shipping AI-augmented code safely:

- **Trust boundaries:** Define what AI can do autonomously vs what requires human approval. Example policy: "Claude may update docstrings and tests, but all logic changes require peer review." Label AI-generated PRs so reviewers know to scrutinize
- **Rollback protocol:** Keep full audit logs via git (every Claude change is a commit). Maintain a state file (e.g., `claude-progress.txt`) tracking what each agent decided. Use `git revert` for agent commits when drift occurs
- **Regulated environments:** Require Claude to output explicit reasoning ("Explain why this change is needed") and log justifications. Freeze model versions (e.g., "Use Sonnet 4.5 only"). Rerun privacy/hallucination checks on outputs
- **CI integration template:** PR-triggered Claude review -> apply patch -> run tests -> halt on failure -> audit for security issues. Quality gates auto-fail if Claude's code does not meet style or logic standards
- Extends the Harness Engineering pattern (see [workflow-patterns.md](workflow-patterns.md#harness-engineering-automated-code-write-and-review-loop)) with regulated-environment and trust-boundary guidance

*Source: deep-research-report.md*

### Agent Verification Patterns from Production Use

- "Agents hallucinate paths, invent file names, tell you something worked when it didn't" -- reinforces Plausible Echo in agent workflows
- Build verification into every agent workflow: agent runs task, then runs a check. Extra 30 seconds prevents hours of debugging.
- Agents that seem "reliable" catch their own mistakes before you see them -- verification is baked in, not bolted on
- Model selection affects verification reliability: models good at chat are not necessarily good at tool calls (the verification mechanism)
- Incremental trust: start with narrow permissions, verify behavior at each scope level before expanding

*Source: Things I wish someone told me.md*

### Tiered Skill Testing: Free/Cheap/Expensive Separation

A three-tier testing architecture for Claude Code skills that separates cost-free static checks from expensive LLM/E2E evaluations.

**Tier 1 -- Static Validation (free, <1s):** Validate skill file structure, required fields, format compliance. Run on every change -- no API cost.

**Tier 2 -- E2E via `claude -p` (~$3.85/run):** Full end-to-end skill execution through real Claude sessions. Stream progress in real-time with `--output-format stream-json --verbose`. Run on demand or pre-merge, not on every commit. Ground truth: fixture-based expected outputs stored in `test/fixtures/`.

**Tier 3 -- LLM-as-Judge (~$0.15/run):** LLM evaluates quality of skill output (not just correctness). Cheaper than E2E but still paid -- run selectively. Useful for subjective output quality (writing style, analysis depth).

**Eval persistence and comparison:** Persist all eval results; compare against the previous run (not a fixed baseline) to catch regressions introduced by the last change. `eval:summary` aggregates stats across all runs for trend analysis.

**SKILL.md template generation:** SKILL.md files are generated from `.tmpl` templates, never edited directly. Edit the template, run `gen:skill-docs`, commit both. Prevents drift between implementation and documentation.

*Source: gstack/CLAUDE.md*

### Expect: Browser-Based Agent Testing with Video Evidence

- Expect lets AI agents test code in a real browser and records a video of every bug found; the video is the verification artifact
- Workflow: write test spec → agent executes in browser → watch video of what went wrong → fix → re-run until passing; the video eliminates the "works on my machine" problem for UI bugs
- Available as CLI (`npx -y expect-cli`) or Claude Code skill; designed to slot into existing agent loops as the verification step
*Source: 2026-03-25-aidenybai-introducing-expect-let-agents-test-your-code-in-a-real-brows.md*

### Hook-Driven Task Completion

- Hooks replace manual status updates: `Test Success Task Completer` detects passing tests and prompts for completion; `Code Change Task Tracker` monitors file saves; `Task Dependency Auto-Progression` auto-starts dependent tasks
- AI assistant rule: implement first, save frequently, let hooks detect completion from observable evidence -- manual status overrides reserved for documentation-only tasks and emergencies
- This is evidence-based task completion: tasks are marked done only when observable criteria (passing tests, file saves) are met, not when the agent self-reports
- (see [testing-verification.md](testing-verification.md#core-principle-verify-artifacts-not-self-reports) for the verification principle this implements)
*Source: claude-task-master/.kiro/steering/taskmaster_hooks_workflow.md*

---

## Eval-Driven Development (EDD)

A formal evaluation framework that treats evals as "the unit tests of AI development" -- define expected behavior before implementation, run evals continuously, track regressions. Analogous to TDD but for AI-assisted workflows where outputs are probabilistic.

### Core Workflow

1. **Define** -- Write evals BEFORE coding. Forces clear thinking about success criteria. Evals are first-class artifacts versioned with code
2. **Implement** -- Build to pass the defined evals
3. **Evaluate** -- Run checks against the implementation
4. **Report** -- Generate pass@k metrics and status summaries (see [Eval Metrics: pass@k vs pass^k](#eval-metrics-passk-vs-passk) for the reliability metrics)

### Eval Types

- **Capability evals:** Can Claude do something new? Validates that a new feature or behavior works as specified
- **Regression evals:** Did changes break existing functionality? Tracked per feature to catch regressions early

### Three Grader Types

| Grader | When to Use | Example |
|--------|-------------|---------|
| Code-based | Deterministic checks possible | `grep -q "pattern" file && echo PASS` |
| Model-based | Open-ended or subjective output | Claude scores 1-5 with reasoning |
| Human | Security-sensitive changes | Flag for manual review with risk level (LOW/MEDIUM/HIGH) |

Prefer code-based graders when possible -- deterministic beats probabilistic. Reserve human review for security; never fully automate security-sensitive evaluations.

### Eval Storage

- `.claude/evals/feature-name.md` -- eval definition
- `.claude/evals/feature-name.log` -- run history
- `.claude/evals/baseline.json` -- regression baselines

### Best Practices

- Keep evals fast -- slow evals do not get run
- Track pass@k over time to surface reliability trends
- Integration commands: `/eval define feature-name`, `/eval check feature-name`, `/eval report feature-name`

(see [workflow-patterns.md](workflow-patterns.md) for verification gate patterns)

*Source: everything-claude-code/skills/eval-harness/SKILL.md*

### Evals-Before-Specs Pattern

- Define how you'll evaluate success BEFORE writing the spec -- clear evaluation criteria constrain the solution space and produce better specs
- Formal progression: evals → spec → plan → implement → verify against evals
- Artifact frontmatter for scripts: include purpose (one line), inputs (file paths or data sources), outputs (file paths produced), last_run (date) -- makes pipeline dependencies explicit and debuggable
*Source: claude-code-synthesis/CLAUDE.md*

### Evaluation and Tracing Integration for RAG

- Production RAG systems should have both offline evaluation (quality) and online tracing (behavior) -- RAGAS for evaluation, Langfuse for tracing
- API returns retrieved contexts alongside query results specifically to support context precision metrics -- design for evaluability from the start
- Test marker system: `offline`, `integration`, `requires_db`, `requires_api` -- default run excludes integration tests; opt-in flag for when external services are available
- `--keep-artifacts` flag on tests preserves temp files for debugging failed runs -- useful pattern for any test suite that produces intermediate artifacts
*Source: LightRAG/README.md, LightRAG/CLAUDE.md*

---

## The Feedback Loop: How Systems Get Smarter

### Real-Time Skill Updates

Update the skill the moment you catch the mistake. Same conversation, while context is fresh.

The pattern:
1. Agent makes a mistake.
2. You catch it.
3. You say: "Create/update the `[name]` skill. Document [what went wrong] and [the safe pattern]."
4. The skill is better for next time.

One sentence. No ceremony.

### Why This Beats Batched Post-Mortems

- **Context is fresh** -- the update happens while the agent knows exactly what went wrong.
- **Zero friction** -- "update the skill" is one sentence, not a meeting.
- **Surprises get captured when they happen** -- API contract drift, connection limits, malformed secrets. If you wait, you forget the nuance.

### What Gets Updated

- **Skills** -- patterns, gotchas, conventions (e.g., "always re-read refs after await")
- **Persona definitions** -- new checks for specific agent roles
- **Worklog templates** -- additional verification steps in Closing the Loop sections
- **Invariant lists** -- new invariants discovered during implementation

### Recursive Critique Loop

A self-improving workflow where Claude iterates on its own output until stable:

- **Draft:** Claude generates output
- **Critique:** Claude (or a second instance) reviews against requirements, listing issues
- **Revise:** Claude re-generates with improvements
- **Check convergence:** If output changed significantly, repeat; if stable, accept
- Can be embedded as a skill or loop prompt (e.g., "Write the code, critique it for security, then revise to fix issues")
- Early evidence shows Claude can often spot issues it missed on first pass when explicitly asked to audit itself

*Source: deep-research-report.md*

### Prompt Evaluation and Benchmarking

Methods for measuring workflow quality:

- **Prompt regression testing:** Define expected outputs for fixed inputs; after each prompt change or model upgrade, re-run baseline prompts and diff results. Treat like software regression tests but for LLM behavior
- **A/B prompt testing:** Run multiple prompt variants on a representative workload; measure error count, tokens used, and answer quality score. Even random sampling reveals trends
- **Prompt scorecards:** Maintain a spreadsheet tracking average correctness (by human rating or test pass rate), consistency (variance in output), and cost (tokens/time). Update after each prompt change; adopt variants that improve the scorecard
- **Drift detection:** Track output quality over time via daily regression tests. If a new model or prompt change yields significantly different answers to a saved query set, flag it as "prompt entropy"
- **Benchmark reference:** SWE-bench coding tasks -- Claude Sonnet 4.5 at 77.2% (state of art) vs ~54% for GPT-4.1, useful for model selection decisions
- **Qualitative vs quantitative:** Use automated tests for objectively checkable correctness; use peer review or rubric scoring for subjective outputs. Lean more on automated evaluation as scale grows

*Source: deep-research-report.md*

### Productivity Telemetry as Verification Signal

Production telemetry data reveals verification patterns and coaching opportunities that manual observation misses:

- **Tool usage distribution:** Read operations dominate (~53.5% of all calls), confirming most Claude Code work is analysis and review, not generation. Verification-heavy workflows are the norm
- **Acceptance rates by tool:** MultiEdit (92%) outperforms Edit (81%), suggesting batch operations with clearer semantics inspire more trust. Write has the lowest acceptance (65%), indicating generation quality or prompt clarity gaps -- a training opportunity
- **Session shape:** Bimodal distribution of 5-minute quick checks and 30-minute deep work sessions, not continuous use. Verification workflows should account for both patterns
- **Team-level impact:** Pre/post productivity deltas from teams using Claude Code show -12% PR review cycles, -16% merge time, +17% commit velocity
- **Anti-pattern detection:** Telemetry catches "stuck developer" sessions (long duration, low output) and enables coaching interventions before time is wasted
- **Cost caveat:** Telemetry-based cost metrics are approximations only; official billing comes from Anthropic Console/AWS/GCP Billing (see [tools-and-integrations.md#claude-code-roi-and-monitoring-via-opentelemetry](tools-and-integrations.md#claude-code-roi-and-monitoring-via-opentelemetry))

*Sources: claude-code-monitoring-guide/claude_code_roi_full.md, sample-report-output.md*

### Autoresearch: Automated Skill Improvement via Scoring Loops

- Agent tests a skill, scores output against a 3-6 item yes/no checklist, makes one small change, keeps if score improves, reverts if not, repeats until 95%+ three times in a row
- Checklist design is the only human input required; more than 6 items causes the skill to game the checklist
- The changelog from autoresearch is the most valuable artifact: a complete record of what works and what doesn't, usable by future models to pick up exactly where this one left off
- Method generalizes beyond skills to any repeated prompt that can be scored objectively
(see [skills.md](skills.md) for the full autoresearch workflow)
*Source: 2026-03-17-itsolelehmann-httpstcokgo8wnoidv.md*

### Three Gulfs Framework: Why Automated Evals Fail Without Manual Comprehension

- Three Gulfs of AI evals: Gulf of Comprehension (gap between what you think your system does and what it actually does), Gulf of Specification (gap between what you want to measure and what your judges measure), Gulf of Generalization (gap between test performance and real-world performance)
- They must be closed in order -- you cannot skip Comprehension; machine-generated test inputs + machine-generated judges without manually reading any outputs = optimizing against a fantasy
- Error analysis protocol: (1) open coding -- read every output, write freeform failure notes; (2) axial coding -- group into binary failure taxonomy; (3) write judges grounded in the taxonomy; (4) validate judges on 15-20 manually scored outputs before running autonomously
- "If you are not willing to look at some data manually on a regular cadence, you are wasting your time with evals"
- autoresearch/eval optimization loops are powerful ONLY after the first two gulfs are closed; run the optimization loop last, not first
*Source: 2026-03-21-nurijanian-httpstcothbioerfj7.md*

### CLI Agent-Readiness as a Conditional Review Persona

- Agent-readiness issues (prose-only output, missing `--json`, interactive prompts without bypass, unbounded list output) are a distinct code quality concern that generic review misses
- Conditional persona pattern: activate based on diff content (CLI command definitions, argument parsing), not always-on
- Severity ceiling for agent-readiness findings is P1 -- they don't crash software but make it harder for agents to use
- All findings are advisory with human owner -- CLI design decisions are not auto-fixable
- Persona self-scopes after dispatch: identifies framework, detects changed commands, evaluates against principles
*Source: compound-engineering-plugin/docs/brainstorms/2026-03-30-cli-readiness-review-persona-requirements.md*

---

## TDD Methodology: Decision Heuristic and Execution Protocol

When to use TDD: "Can you write `expect(fn(input)).toBe(output)` before writing `fn`?" Yes = TDD. No = standard plan with post-hoc tests.

- **TDD candidates:** business logic, API endpoints, data transformations, validation rules, algorithms, state machines, utility functions. Skip: UI/styling, config changes, glue code, CRUD, prototyping
- **Context budget:** TDD is heavier -- target ~40% context budget (vs 50% for standard plans) due to 2-3 execution cycles per feature
- **One feature per TDD plan** -- if features are trivial enough to batch, they're trivial enough to skip TDD
- **Commit convention:** `test(phase-plan):` (RED), `feat(phase-plan):` (GREEN), `refactor(phase-plan):` (REFACTOR) -- 2-3 atomic commits per feature
- **Test quality:** test behavior not implementation, one concept per test, descriptive names, no mocking internals or testing private methods
- **Error handling:** test passes in RED = investigate (feature exists or test wrong); tests fail in REFACTOR = undo and refactor smaller

(see [Eval-Driven Development](testing-verification.md#eval-driven-development-edd))

*Source: get-shit-done/get-shit-done/references/tdd.md*

---

## Decision Traces for Strategic Learning

Real-time skill updates handle tactical lessons. Decision traces handle strategic ones -- *why* the system is shaped the way it is (see [memory-persistence.md#decision-traces-strategic-memory](memory-persistence.md#decision-traces-strategic-memory) for the full format).

### When to Write One

- Choosing between architectural approaches (in-memory vs. Redis, monolith vs. microservice)
- Post-mortems on production incidents
- Any decision whose reasoning you will forget within 30 days
- When you almost shipped a bug and the near-miss reveals a systemic gap

### Format

```
---
id: DT-YYYYMMDD-NNN
title: [Decision title]
date: YYYY-MM-DD
status: accepted
---

## Decision
[What you decided]

## Context
[Why this came up, what problem you were solving]

## Alternatives
[What else you considered and why you rejected it]

## Consequences
- [Impact on the system]
- Skill updated: `[skill-name]` now includes "[new rule]"
```

The last line is the key: the trace links to the skill it updated. *Why* lives in the trace. *What to do* lives in the skill. Together they prevent future agents from "simplifying away" a rule whose purpose they do not understand.

### When a Skill Update Is Enough vs. When You Need a Full Trace

**Skill update only:**
- Bug fixes with a clear pattern ("always re-read refs after await")
- Process corrections ("commit failing tests before implementing")
- The lesson is tactical, not strategic

**Full decision trace:**
- The decision affects more than one feature
- Multiple viable alternatives existed and you need to record why you chose this one
- A production incident revealed a systemic issue
- Someone will ask "why did we do it this way?" in six months
