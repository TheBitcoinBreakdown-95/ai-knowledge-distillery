# Workflow Patterns

Three distinct workflows for AI-assisted development, each suited to different
situations. All share a common foundation: the human provides judgment and
constraints, the AI provides execution and memory.

---

## The Vibe Engineering Stack

### Architecture: Spec -> Invariants -> Worklog -> Code -> Tests -> Feedback

The complete cognitive architecture for AI-assisted development:

```
Human Judgment
             |
             v
 +---------------------------------+
 | Personas  ->  perspectives      |
 | Skills    ->  heuristics        |
 | Worklogs  ->  memory            |
 | Feedback  ->  learning          |
 +---------------------------------+
             |
             v
    Deterministic Gates
 (tests, compilers, invariants)
             |
             v
     Production Software
```

The feedback loop closes the circle. Without it, you have tools.
With it, you have a system that improves:

```
Spec -> Invariants -> Worklog -> Code -> Tests
           ^                       |
        Personas  <-- Feedback <-- Skills
```

Each primitive externalizes a different aspect of human judgment.
The gates filter out randomness. What ships is deterministic.

(see [memory-persistence.md#layer-2-worklogs-feature-scoped-session-to-session](memory-persistence.md#layer-2-worklogs-feature-scoped-session-to-session) for worklog format details)
(see [skills.md](skills.md) for skill encoding patterns)

### The Identity Ladder

- **Junior** writes code
- **Mid-level** refactors code
- **Senior** designs systems
- **Vibe Engineer** designs the constraints that machines write inside

The vibe engineer defines *what* needs to be built (spec), *what must always be
true* (invariants), and *who reviews the work* (agent personas). The AI writes
the code, tests, and docs. Deterministic gates reject anything that does not
pass. The engineer reviews and ships.

### "You've Been Promoted, Not Replaced"

AI coding is the baseline. Your job shifted from writing code to:

1. **Architecture** -- deciding how pieces fit together
2. **Scope** -- deciding what is and is not in the build
3. **Constraints** -- defining the rules machines write inside
4. **Review** -- verifying output against intent

The mental model: you are a senior engineer mentoring a brilliant college grad
who can code circles around most people, learns fast, and has zero real-world
judgment. LLMs are strong coders but lack context about your specific situation.
Your job is to provide that context. Their job is to execute within it.

When you invert this -- letting the AI make architectural decisions or define
scope -- you get technically impressive code that solves the wrong problem.

### CLAUDE.md 7-Section Operating Template

Comprehensive CLAUDE.md template covering operational behavior, not just project config:

1. **Plan Mode Default** -- enter plan mode for any non-trivial task (3+ steps or architectural decisions); re-plan immediately if something goes sideways
2. **Subagent Strategy** -- use subagents liberally to keep main context clean; one task per subagent for focused execution
3. **Self-Improvement Loop** -- after any user correction, update `tasks/lessons.md` with the pattern; write rules to prevent repeat mistakes; review lessons at session start
4. **Verification Before Done** -- never mark a task complete without proving it works; ask "would a staff engineer approve this?"
5. **Demand Elegance (Balanced)** -- for non-trivial changes, pause to ask "is there a more elegant way?"; skip for obvious fixes
6. **Autonomous Bug Fixing** -- given a bug report, just fix it; point at logs, errors, failing tests, then resolve
7. **Task Management** -- plan to `tasks/todo.md`, verify plan, track progress, explain changes, document results, capture lessons

Core principles: simplicity first, no temporary fixes, minimal impact changes.

*Source: Twitter Bookmarks/Thread by @EXM7777.md*

### Cowork Context Files Strategy: Better Files Beat Better Prompts

@heynavtoor's full Cowork setup guide centers on a mindset shift: "stop thinking about better prompts and start thinking about better files."

- **Three Core Context Files:** `about-me.md` (role, success criteria), `brand-voice.md` (communication style, phrases, examples), `working-style.md` (preferences for Claude's behavior, output format, question-first approach)
- **AskUserQuestion as Default:** Add "DO NOT start working yet. First, ask me clarifying questions" to every non-trivial prompt -- eliminates the "polished garbage" problem of AI guessing wrong
- **Key Quote:** "ChatGPT trained you to write better prompts. Cowork trains you to build better context. One is a skill that depreciates. The other compounds."
- **5 Cowork Features Ranked by Impact:** 1) File System Access, 2) AskUserQuestion, 3) Plugins, 4) Instructions (global + folder), 5) Connectors
- **Instructions as Persistent Memory:** Global instructions load every session; folder instructions are project-specific -- workaround for no cross-session memory
- **Connector Strategy:** Link tools once (Slack, Drive, Notion), then Claude references live data mid-conversation -- "most underused feature"

(see [context-engineering.md](context-engineering.md#claudemd-your-always-loaded-memory) for the CLAUDE.md equivalent in Claude Code; see [prompt-engineering.md](prompt-engineering.md#core-principle-specificity-is-everything) for the specificity principle this builds on)

*Source: Twitter Bookmarks/2026-02-25-heynavtoor-how-to-set-up-claude-cowork-the-right.md*

---

## Pattern 1: Spec-Driven Feature Development

The day-to-day workflow for any feature. This is hands-on, synchronous work
where you guide the AI through a structured process.

### Step 1: Write the Spec

Create a `PRODUCT_SPEC.md` with these sections:

| Section | Purpose |
|---------|---------|
| User flows | Step-by-step walkthroughs of every feature |
| Happy paths | What happens when everything works |
| Sad paths | What happens when things fail |
| Edge cases | The weird stuff ("user closes browser mid-payment") |
| Business logic | Fee calculations, rate limits, capacity rules |
| NOT in MVP | Explicit list of features you are deferring |

The "NOT in MVP" section is critical. Half of AI productivity gains get eaten
by scope creep. The AI will happily implement features you did not ask for if
they seem related. An explicit exclusion list gives you a reference for saying no.

**Concrete example -- User Registration Flow:**

```markdown
## User Registration Flow

### Happy Path
1. User enters email on /login
2. System sends magic link email
3. User clicks link within 24 hours
4. System creates session, redirects to /dashboard

### Sad Paths
- Invalid email format -> Show inline validation error
- Email send fails -> Show error, suggest retry
- Link expired -> Redirect to /login?error=expired
- Link already used -> Redirect to /login?error=used

### Constraints
- Rate limit: 5 magic links per email per hour
- Rate limit: 10 magic links per IP per hour
- Token storage: SHA256 hash (never store plaintext)
- Session: HTTP-only cookie, 7-day expiry
```

Without a clear spec, the AI hallucinates requirements. Garbage in, garbage out
-- but now the garbage comes out faster and with more confidence.

(see [prompt-engineering.md#spec-driven-development](prompt-engineering.md#spec-driven-development) for spec writing techniques)

### Interview-First Spec Discovery

For larger features, invert the usual workflow: instead of writing the spec yourself, start with a minimal prompt and let Claude interview you via AskUserQuestion. The model surfaces considerations you have not thought of through structured questioning.

- Once the spec is complete, start a fresh session to execute it -- clean context focused entirely on implementation
- Combine with the two-correction rule: after two failed corrections, `/clear` and restart with a better prompt

*Source: Best Practices for Claude Code.md*

### Step 2: Define Invariants

Invariants are statements that must *always* be true. They are verifiable, not
vague. Binary pass/fail, not "seems about right."

| Bad (vague) | Good (verifiable) |
|-------------|-------------------|
| "Login should be secure" | "Tokens are SHA256 hashed; plaintext never stored" |
| "System should be fast" | "API response < 200ms at p95" |
| "Handle errors gracefully" | "Every error path returns a specific HTTP status code" |

Start with three. Write them before any code exists.

(see [testing-verification.md](testing-verification.md) for verification protocols)

### Step 3: Create the Worklog

A worklog is a scoped task list: 50-100 lines, not 787. Each entry has:

- A concrete task description
- Binary completion criteria (done or not done)
- Dependencies on other tasks

The worklog is the AI's memory across sessions. When you start a new context
window, the AI reads the worklog and knows exactly where things stand.

(see [memory-persistence.md#layer-2-worklogs-feature-scoped-session-to-session](memory-persistence.md#layer-2-worklogs-feature-scoped-session-to-session) for worklog templates)

### Step 4: Load Skills, Begin Coding

Point the AI at relevant skills before starting. Skills are reusable prompts
that encode hard-won lessons -- patterns, gotchas, conventions extracted from
previous work. Example: a `react-async-patterns` skill that documents stale
closure bugs so every session touching async React gets the safe pattern
automatically.

### Step 5: Verify at Each Milestone

At every milestone checkpoint:

- Run the tests (deterministic gate)
- Check invariants (binary pass/fail)
- Compare output to spec (does it match the happy path? the sad paths?)

Do not batch verification to the end. Verify continuously.

### Step 6: Close the Loop

The agent must verify its own work against the spec, not just report completion.
"All tests pass" when the agent is 90% done is a common failure. Verify
artifacts, not self-reports.

(see [failure-patterns.md](failure-patterns.md) for the "Premature Completion" and "Plausible Echo" anti-patterns)

### Step 7: Archive and Compress

After a feature ships:

1. **Update skills** -- capture any new patterns immediately, while context is
   fresh. Do not wait for a formal post-mortem. "Update the skill" is one
   sentence, not a ceremony.
2. **Write decision traces** -- for strategic decisions (architectural choices,
   post-mortems). Each trace links to the skill it updated.
3. **Compress the worklog** -- completed worklogs become reference material,
   not active documents.

The feedback loop: Claude makes a mistake -> you catch it -> you tell Claude to
update the relevant skill right now -> the skill is better next time. Each
mistake makes the system smarter.

---

## Beginner Entry Points

### The Milestone Loop

A distilled entry-level workflow for AI-assisted development, applicable whether using a code editor (Cursor, Antigravity) or a no-code platform (Replit, Lovable):

**Step 1: Plan first (most important step).** Create a README with: what the app does (2-3 sentences), tech stack, and 5 testable milestones. If the plan feels too complex: "Simplify this. What's the absolute minimum I need to build first?"

**Step 2: Plan before code for each milestone.** "Tell me your plan for milestone 1. Don't code yet. Just explain your approach." Go back and forth until the plan is simple. Then: "Ok, now code it."

**Step 3: Test after every single change.** Run the app, try the feature. Broken? Screenshot and paste: "Here's what happened. Fix it." This is the loop: build, test, iterate.

**Step 4: Commit after each working milestone.** Git commit is a checkpoint, not a ceremony.

**Common mistakes that kill momentum:**
- Asking for the entire app at once (AI loses context, produces broken output)
- Not testing after changes (bugs compound into debugging nightmares)
- Being vague ("make a signup page" vs "signup page with email field, password field, blue button saying 'Sign Up'")
- Trusting AI output blindly (always review, always test)
- Hardcoding secrets (use environment variables)
- Skipping version control (no safety net when things break)

The core techniques -- plan first, one feature at a time, test immediately, revert when stuck, ask for explanations -- are identical to Pattern 1 (Spec-Driven) but stripped to their beginner-accessible minimum. The milestone loop is the training-wheels version of the full spec-driven workflow.

### Dual-AI Planner/Executor Workflow

A lightweight version of the Two-Terminal Pattern (see [Pattern 3](#pattern-3-meta-agent-orchestration)) accessible to beginners using an IDE with two AI models:

| Role | Model | Where | What It Does |
|------|-------|-------|-------------|
| **Planner** | Gemini (or any free/cheap model) | IDE sidebar chat | Creates implementation plans, answers questions, handles trivial changes |
| **Executor** | Claude Code | Terminal | Reads the plan, writes code, runs tests, executes |

**Workflow:**
1. Describe the app to the planner with all detail, links, docs, APIs
2. Ask the planner to create a detailed implementation plan in a folder (explicitly say "do not write code, just tasks")
3. Tell Claude Code: "Read the plan in folder X, understand it, execute it"
4. Use the planner for trivial iterations (color changes, simple updates) to conserve Claude Code credits
5. Reserve Claude Code for complex tasks where quality matters

**Credit optimization trick:** Ask the planner to write code changes as comments rather than modifying files, then have Claude Code read and execute those comments. Reduces Claude Code token consumption on routine changes.

This pattern embodies the same principle as the meta-agent architecture -- separation of planning from execution -- but requires zero setup, no SDK, no configuration. It works in any IDE that supports multiple AI integrations (Antigravity, Cursor, VS Code with extensions).

(see [prompt-engineering.md](prompt-engineering.md) for the spec-writing techniques that make the planner's output useful)

### Beginner vs Advanced Vibe Coder Setup Flow

A practitioner's comparison of beginner vs experienced setup workflows.

- **Beginner pattern:** Install tool -> think about what to build -> prompt -> begin -> generate AI slop -> debug endlessly
- **Advanced pattern:** Install tool -> set up preferences and agent memory -> set up skills and rules -> integrate connectors and MCP servers -> test agent -> think about what to build -> brainstorm in Claude project -> generate PRD -> plan and delegate -> begin -> generate 70% MVP -> debug to full functionality
- **Key insight:** The setup phase (memory, skills, rules, MCPs) before any building is what separates productive from unproductive vibe coding. "Vibe coding is a skill that's being slept on"

(see [project-setup.md](project-setup.md) for day-zero workflow)

*Source: Twitter Bookmarks/2026-03-01-mustang_akin-beginner-vibe-coder.md*

### The Director Mental Model (Non-Programmer Framing)

A practical mental model for non-coders using Claude Code, drawn from a 20-hour "Claude Code for Non-Programmers" curriculum:

- **Core analogy:** You are a film director, not a camera operator. Directors communicate vision, understand enough craft for productive conversations, recognize when something is wrong, and know how to course-correct -- but never operate the equipment themselves
- **Key mindset shift:** Tell Claude WHAT you want to accomplish, not HOW to do it. "Add an interactive quote randomizer with smooth animations" outperforms "Create a div with class 'quote-box' containing a p tag..."
- **Specificity spectrum:** Neither vague ("make it better") nor hyper-precise (exact pixel values) is always correct. The sweet spot: specific about WHAT and CONSTRAINTS, flexible on HOW
- **When to direct vs delegate:** Direct explicitly on user-facing text, visual design, business logic, and integration points. Delegate to Claude on implementation details, best practices, code organization, and tool/library choices
- **Iteration is a feature, not a bug:** The revision cycle (instruct -> review -> specific feedback -> repeat) is a legitimate workflow, not a failure of initial instruction. Good feedback acknowledges what works, specifies exactly what to change, and provides clear direction

*Source: Learning CC/notes/module-1-reflection.md, module-3-reflection.md, module-5-reflection.md*

### Feature Addition: 5-Phase Workflow

A structured workflow for adding features, more granular than the Milestone Loop:

| Phase | Action | Prompt Template |
|-------|--------|----------------|
| **1. Understand** | Explore how similar features work, identify files to modify, flag complications | "Before we implement [feature], explain how similar features work, identify files we'll modify, flag complications" |
| **2. Plan** | Decide approach, order, and what to build first to validate | "Based on that, let's plan. What order should we tackle this? What should we build first?" |
| **3. Implement** | Build step by step, starting with first piece only | "Let's start with [first piece]. Just this part for now." |
| **4. Verify** | Visual check, functional check, interaction check, responsive check, error handling | "How can I test that this works correctly? Walk me through checking it." |
| **5. Integrate** | Ensure consistency with existing patterns, styling, and no regressions | "Now let's make sure this integrates smoothly with the rest of the application." |

Complements the Milestone Loop (see [above](#the-milestone-loop)) by providing phase-level structure within each milestone.

*Source: Learning CC/new-project-key-steps.md, Learning CC/notes/module-7-reflection.md*

### Bug Fix: 5-Step Workflow

A systematic bug-fixing workflow that prevents random guessing:

1. **Reproduce** -- Make the bug happen reliably. Cannot fix what you cannot see. Document exact steps.
2. **Locate** -- Find the responsible file and function. "What part of the code is likely responsible?"
3. **Understand** -- Why is this happening? "Explain what the current code is doing and why that causes the bug."
4. **Fix** -- Choose the safest fix. "What's the safest way to fix this without breaking anything else?"
5. **Test** -- Verify: original bug is gone, no new bugs introduced, related functionality still works, edge cases handled.

Complementary to the troubleshooting taxonomy in failure-patterns.md (see [failure-patterns.md#troubleshooting-taxonomy](failure-patterns.md#troubleshooting-taxonomy-three-problem-types)).

*Source: Learning CC/new-project-key-steps.md, Learning CC/notes/module-6-reflection.md*

### Director-Level Version Control

Git concepts framed for non-programmers who direct Claude through git operations:

- **Branches as risk-free innovation:** Create a branch before risky work, experiment freely, merge if successful, delete if not. "I don't need to be afraid to experiment. Git has my back."
- **Two levels of recovery:** Uncommitted changes -> `git restore` (undo before saving). Bad commit -> `git reset --hard HEAD~1` (undo a save). Two states of change need two different tools.
- **Director language for git:** Never say "do a hard commit reset." Instead: "That last commit broke things. Can you help me undo it and get back to the previous working state?" Your value is knowing what is possible, not memorizing commands.
- **Commit philosophy:** Each commit represents one logical change with a clear descriptive message. Git commit is a checkpoint, not a ceremony.

*Source: Learning CC/notes/module-8-reflection.md*

---

## Pattern 2: The Ralph Loop (Autonomous Coding)

Ralph is an open-source autonomous coding agent that works while you are away.
Named after the Simpsons character known for naive, relentless persistence.

Repository: [github.com/snark-tank/ralph](https://github.com/snark-tank/ralph)

### How It Works

1. **Describe the full feature in detail** (spend serious time here -- vague
   descriptions produce garbage)
2. **Break into atomic tasks**, each with binary pass/fail criteria
3. Ralph picks task 1, codes it, tests it, saves if it passes, picks the next
4. **Each round starts fresh** -- no accumulated context confusion
5. **Knowledge compounds**: every round logs what it learned, next round reads
   those logs

The insight: engineering teams have worked this way for decades. Sticky notes on
a board. Pull one, complete it, put it back, grab the next. Ralph is the AI
version of that workflow.

### Writing Good Task Descriptions

Your description is the contract. The AI needs to know when it is done without
asking you.

| Quality | Example |
|---------|---------|
| Good | "Add a priority column that defaults to medium" |
| Good | "Dropdown shows options: all, high, medium, low" |
| Bad | "Make it good" |
| Bad | "Make it pretty" |

Workflow:
1. Open your AI coding tool and talk for 2-3 minutes describing everything you want
2. Tell the AI to turn your rambling into a formal list of requirements
3. Each requirement needs a clear pass/fail check

An hour on requirements saves ten hours of fixing.

### AFK Mode vs Hands-On Mode

| Mode | How | Best For |
|------|-----|----------|
| AFK Ralph | Set it running overnight, wake up to finished features | Straightforward tasks with clear requirements |
| Hands-On Ralph | Run one round at a time, review each update, steer when needed | Complex features where you want more control |

Typical result: Ralph gets 90% there, you spend an hour fixing the last 10%.
The win is turning a full day of focused work into an hour of cleanup.

### Cost Profile

Typical run: 10 rounds, roughly $30 total. One builder delivered, reviewed, and
tested an entire app for under $300 -- work that would have cost $50,000 to
hire out.

### When To Use Ralph vs Manual Vibe Engineering

| Situation | Use |
|-----------|-----|
| Overnight batch of well-defined tasks | Ralph (AFK) |
| Complex feature needing architectural judgment | Manual (Pattern 1) |
| Exploratory prototyping where requirements evolve | Manual (Pattern 1) |
| Large volume of independent, scoped tasks | Ralph (AFK or Hands-On) |
| Tasks requiring cross-system coordination | Meta-Agent (Pattern 3) |

### Fan-Out Batch Processing Pattern

For large migrations or batch operations: loop through tasks calling `claude -p` for each item in parallel with scoped `--allowedTools`.

- Unix-style piping: `cat data.json | claude -p "transform this" --output-format json`
- Structured output via `--json-schema` enforces response conformance; result in `structured_output` field
- Streaming: `--output-format stream-json --verbose --include-partial-messages` for real-time pipeline integration
- Session continuation in scripts: capture session ID, then `--resume {sessionId}` for follow-up prompts
- (see [agent-design.md](agent-design.md) for the SDK-level equivalent)

*Sources: Run Claude Code programmatically.md, Best Practices for Claude Code.md*

### Immutable Test List Pattern

Anthropic's official autonomous coding quickstart demonstrates a two-agent multi-session pattern for building complete applications.

- **Initializer agent (session 1):** Reads `app_spec.txt`, generates `feature_list.json` with 200+ detailed end-to-end test cases (both "functional" and "style" categories), creates `init.sh` for environment setup, initializes git
- **Immutable feature list:** Feature entries can ONLY have `"passes"` changed from false to true. Descriptions, steps, and ordering are NEVER modified. This prevents scope drift and ensures no functionality is silently dropped across sessions
- **Coding agent (sessions 2-N):** Each session starts from scratch (fresh context). 10-step cycle: orient (read spec + progress + git log) -> start servers -> regression verify (test 1-2 previously passing features) -> choose one feature -> implement -> verify via browser automation -> update feature_list.json -> commit -> update progress notes -> end cleanly
- **Regression verification mandate:** Before implementing new work, the coding agent MUST verify that previously passing features still pass. Any regression immediately marks the feature as failing and gets fixed before new work
- **Multi-session persistence:** Git commits + `claude-progress.txt` as handoff state. No memory between sessions; all context reconstructed from files
- **Quality bar:** Zero console errors, polished UI matching spec, all features verified end-to-end through actual UI (no curl shortcuts), screenshots as evidence

*Source: claude-quickstarts/autonomous-coding/prompts/initializer_prompt.md, coding_prompt.md*

---

## Pattern 3: Meta-Agent Orchestration

When the cognitive load shifts from coding to orchestrating -- when you are
managing multiple parallel workstreams and the state exceeds human working
memory -- you need a meta-layer.

(see [agent-design.md](agent-design.md) for full meta-agent architecture)

### The Two-Terminal Pattern

| Terminal 1 (persistent) | Terminal 2 (ephemeral) |
|--------------------------|------------------------|
| Meta-agent REPL (Opus) | Claude Code CLI (Sonnet) |
| Strategic: planning, tracking, patterns | Tactical: writing code, running tests |
| Never sees implementation code | Only sees code |

Separation is mandatory. When implementation context grows in a single window,
strategic context gets compressed out -- a failure mode called **Vision
Compression**. Intent erodes into implementation, token by token.

### How It Works: Meta-Agent Thinks, Workers Execute

1. Human describes goal to meta-agent
2. Meta-agent decomposes into workstreams, drafts implementation prompt
3. Human copies prompt into Claude Code session (or subagent executes it)
4. Claude Code does the implementation
5. Human reports results back to meta-agent
6. Meta-agent updates state, captures patterns, suggests next move

The meta-agent's system prompt forbids code and implementation. It thinks only
in goals, constraints, dependencies, and patterns.

### State Files as Shared Memory

Plain markdown files that both human and agent read and write:

| File | Contents |
|------|----------|
| `workstreams.md` | Active workstreams with status (PROPOSED -> ACTIVE -> REVIEW -> SHIPPED) |
| `decisions.md` | Decision log with context, alternatives, rationale |
| `patterns.md` | Named pattern journal (observed -> named -> implication) |
| `session-log.md` | Session history (append-only) |
| `handoff.md` | Bridge prompts for implementation sessions |

State files survive session boundaries. Even if the SDK session is lost, the
markdown state persists. The human can edit between sessions.

(see [memory-persistence.md](memory-persistence.md) for state file formats)

### Handoff Prompts Between Sessions

Each handoff prompt contains:

- **Context**: what the project is and where it stands
- **Goal**: what this session should accomplish
- **Scope**: what is in bounds and out of bounds
- **Constraints**: technical and process constraints
- **Verification criteria**: how to confirm the work is done

This prevents the meta-agent's understanding from degrading across session
boundaries.

### Writer/Reviewer Parallel Pattern

A fresh Claude Code session reviewing code it did not write avoids "same blind spots" -- the reviewer has no anchoring bias from implementation context.

- Patterns: one session writes code, another reviews; one session writes tests, another writes code to pass them
- Git worktrees enable parallel sessions: `claude -w feature-name` creates isolated worktree at `<repo>/.claude/worktrees/<name>`
- Subagents can also use `isolation: worktree` frontmatter -- auto-cleaned if no changes made
- (see [agent-design.md](agent-design.md) for the failure pattern this addresses)

*Sources: Best Practices for Claude Code.md, Common workflows.md*

### Parallelization Patterns: Cascade and Two-Instance Kickoff

Practical parallelization techniques for Claude Code sessions from experienced practitioners.

- **Cascade method:** Open newest tabs to the right, sweep left-to-right. Each instance works on a separate scope. Limit to 3-4 concurrent tasks -- beyond that, coordination overhead exceeds time saved ("minimum viable parallelization")
- **Git worktrees per instance:** Each parallel Claude Code instance gets its own worktree for isolated file changes. Prevents merge conflicts during parallel work
- **Two-instance kickoff:** One Claude scaffolds the project structure while another does deep research / PRD / architecture -- then merge results. Splits the "thinking" and "building" phases
- **Parallel via /fork:** For non-overlapping tasks within a session, `/fork` creates a new session branch. For overlapping changes, use git worktrees instead

(see [skills.md](skills.md) for /batch parallel migrations)

*Sources: Twitter Bookmarks/The Longform Guide to Everything Claude Code.md, Twitter Bookmarks/Best Practices for Claude Code (Use these to make Claude Code 100x Powerful).md*

### Chief of Staff Pattern: Non-Programmer Builds Full Autonomous Workflow

Non-programmer (@jimprosser) built a complete "Chief of Staff" system with Claude Code in 36 hours. Key patterns:

- **4-Color Task Triage:** AM Sweep classifies every task as Green (AI handles fully), Yellow (AI gets 80% done, human finishes), Red (needs human brain/presence), Gray (not actionable today)
- **Stream Deck as Agent Trigger:** Two physical buttons -- AM Sweep (triage + 6 parallel agents) and Time Block (schedule remaining tasks geographically)
- **6 Parallel Specialized Agents:** Each with scoped tool access and own context window -- email drafter (never sends, only drafts), Obsidian updater, meeting scheduler, background researcher, etc.
- **Overnight Automation:** Two cron jobs pre-6:15 AM scan calendar for drive times (Google Maps API) and triage email into Todoist with priorities/durations
- **Time Block Intelligence:** Batches errands geographically, knows home vs office vs location-specific tasks, schedules gym, defers overflow to lowest-load future day
- Build happened in "layers of functionality" over a year of tinkering, not a one-shot -- parallelized subagents were the unlock

(see [autonomous-agents.md](autonomous-agents.md#ceo-only-main-agent-pattern) for the delegation pattern; see [context-engineering.md](context-engineering.md#knowledge-type-placement-matrix) for how to structure the context files that make this work)

*Source: Twitter Bookmarks/2026-03-05-jimprosser-chief-of-staff-claude-code.md*

### Channel-Isolated Parallel Agent Chains

Multi-agent content production pipeline using channel isolation for parallelization:

- **Pattern:** Research agent (trends) -> writing agent (scripts) -> thumbnail agent (images), each in its own Discord channel
- **Key insight:** Agents don't need to be aware of each other; channels handle routing. Output from one feeds visibly to the next
- **Advantage over sequential handoffs:** Creates transparency, allows feedback at each stage without blocking the pipeline
- Discord topics as a coordination primitive for multi-agent workflows -- simpler than explicit orchestration

(see [autonomous-agents.md](autonomous-agents.md#multi-agent-communication-direct-vs-boss-routing) for direct vs boss routing alternatives)

*Source: awesome-openclaw-usecases/usecases/content-factory.md*

---

## Pattern 4: RPI Workflow (Research -> Plan -> Implement)

A systematic four-step development workflow that prevents wasted effort on non-viable features:

**Step 1 -- Describe:** Write feature description in `rpi/{feature-slug}/REQUEST.md`

**Step 2 -- Research (`/rpi:research`):** GO/NO-GO gate using 6 specialist agents in sequence:
1. requirement-parser: extract structured requirements
2. product-manager: product viability, strategic alignment
3. Explore (built-in): deep code exploration grounding analysis in code reality
4. senior-software-engineer: technical feasibility informed by actual codebase
5. technical-cto-advisor: strategic synthesis, go/no-go recommendation
6. documentation-analyst-writer: generates research report

Output: `rpi/{feature-slug}/research/RESEARCH.md` with GO, NO-GO, CONDITIONAL GO, or DEFER verdict.

**Step 3 -- Plan (`/rpi:plan`):** Generates four documents from research:
- `pm.md` (product requirements, user stories)
- `ux.md` (UI flows, accessibility)
- `eng.md` (technical architecture, API contracts)
- `PLAN.md` (phased implementation roadmap with task breakdown)

**Step 4 -- Implement (`/rpi:implement`):** Per-phase loop with validation gates:
1. Code Discovery (Explore agent) -- understand before changing
2. Implementation (senior-software-engineer) -- build phase deliverables
3. Self-Validation -- lint, test, build
4. Code Review (code-reviewer agent) -- security, correctness, maintainability
5. User Validation Gate -- STOP and require human PASS/CONDITIONAL PASS/FAIL
6. Documentation Update -- update PLAN.md and IMPLEMENT.md

**Critical design decisions:**
- Phase 2.5 (Technical Discovery) grounds feasibility in **actual code reality**, not assumptions -- prevents plans that look good on paper but conflict with existing architecture
- Every phase prompts `/compact` after completion to manage context window (see [context-engineering.md](context-engineering.md))
- User validation gate is mandatory and blocking -- the agent cannot proceed without human approval
- Implementation supports `--phase N` (resume from specific phase) and `--validate-only` (dry-run)
- When NOT to use: bug fixes, simple changes (<30 min), exploratory prototyping, docs-only changes

(see [agent-design.md#subagents-in-claude-code](agent-design.md#subagents-in-claude-code) for agent definition patterns)
(see [testing-verification.md](testing-verification.md) for validation gate design)

### Feature-Dev: 7-Phase Multi-Perspective Workflow

Anthropic's official feature-dev plugin implements a structured 7-phase workflow with parallel multi-perspective agents.

- **Phase 1 (Discovery):** Clarify the feature request -- problem, constraints, requirements
- **Phase 2 (Codebase Exploration):** Launch 2-3 `code-explorer` agents in parallel to trace similar features, map architecture, and analyze related implementations. Returns file:line references for deep reading
- **Phase 3 (Clarifying Questions):** Identify underspecified aspects (edge cases, error handling, integration points, backward compatibility). All questions presented at once; waits for answers before proceeding
- **Phase 4 (Architecture Design):** Launch 2-3 `code-architect` agents with different design philosophies: minimal changes, clean architecture, pragmatic balance. Presents comparison with trade-offs and recommendation. User chooses
- **Phase 5 (Implementation):** Only starts after explicit approval. Follows codebase conventions discovered in Phase 2 and architecture chosen in Phase 4
- **Phase 6 (Quality Review):** Launch 3 `code-reviewer` agents in parallel with different focuses: simplicity/DRY/elegance, bugs/correctness, conventions/abstractions. Confidence scoring (0-100). User decides: fix now, fix later, or proceed
- **Phase 7 (Summary):** Documents what was built, key decisions, files modified, suggested next steps
- **Key insight:** Each phase builds on the previous. Clarifying questions prevent design ambiguity; design prevents implementation drift; review prevents quality debt

*Source: claude-plugins-official/plugins/feature-dev/README.md*

### Multi-Agent Parallel Discovery with Human Checkpoints

7-phase feature development workflow using parallel agents with explicit approval gates:

- **Phase 2 (Discovery):** Launch 2-3 `code-explorer` agents in parallel on different aspects of the codebase
- **Phase 3 (Questions):** Explicit clarifying questions phase -- marked CRITICAL, don't skip. Eliminates the "polished garbage" problem
- **Phase 4 (Design):** Launch 2-3 `code-architect` agents with different focuses (minimal vs clean vs pragmatic)
- **Phase 5 (Approval):** Explicit user approval before any implementation begins
- **Phase 6 (Review):** 3 parallel reviewers on different aspects post-implementation
- **TodoWrite throughout:** Session tracking ensures no phase is skipped or merged
- Combines the parallelization pattern with mandatory human checkpoints at each phase transition

(see [agent-design.md](agent-design.md#subagents-in-claude-code) for subagent design patterns)

*Source: claude-plugins-official/plugins/feature-dev/commands/feature-dev.md*

---

## Pattern 5: Command -> Agent -> Skills Architecture

A three-tier orchestration pattern for multi-step workflows with clean separation of concerns:

| Layer | Role | Example |
|-------|------|---------|
| **Command** | Entry point, user interaction, initiates workflow | `/weather-orchestrator` |
| **Agent** | Orchestrates execution with preloaded skills | `weather` agent (model: haiku, tools: WebFetch, Read, Write) |
| **Skills** | Domain knowledge injected into agent context at startup | `weather-fetcher`, `weather-transformer` |

**Key design principles:**
- Skills are **preloaded as knowledge**, not dynamically invoked -- full skill content is injected into the agent's context at startup
- Single execution context: all work happens within one agent's agentic loop
- Sequential execution: the agent follows skill instructions in order
- Command invokes agent via `Task` tool, not bash (subagents cannot invoke other subagents via bash -- use Task tool exclusively)
- Configurable I/O: transformation rules and results live in external files, not hardcoded

**When to use:** multi-step workflows, domain-specific knowledge injection, sequential tasks requiring different knowledge domains, reusable workflow components.

**Why it works:** progressive disclosure (skills load only what the agent needs), clean separation (command/agent/skill boundaries), single context (no inter-agent communication overhead), reusability (same skills across different agents/commands).

(see [agent-design.md](agent-design.md) for subagent frontmatter including the `skills:` field)
(see [skills.md#skill-vs-agent-vs-command-comparison](skills.md#skill-vs-agent-vs-command-comparison) for invocation differences)

---

## Pattern 6: GSD (Get Shit Done) Execution Framework

Get Shit Done (GSD) is a meta-prompting and context engineering system for Claude Code that solves "context rot" -- quality degradation as the context window fills.

- **Wave execution model:** Plans grouped into dependency-based waves. Independent plans run in parallel within a wave; waves run sequentially. Vertical slices (end-to-end per feature) parallelize better than horizontal layers (all models, then all APIs)
- **Fresh context per executor:** Each subagent executor gets a clean 200K context window. The orchestrator stays at 30-40% utilization while thousands of lines of code are written across parallel executors
- **Model profiles per agent:** Three profiles (quality/balanced/budget) assign different model tiers to each of 11 agents. Planning agents get Opus by default; execution gets Sonnet; verification gets Haiku on budget. Configurable via `/gsd:set-profile`
- **Workflow agent toggles:** Research, plan_check, verifier, and nyquist_validation agents can be disabled per-invocation (`--skip-research`, `--skip-verify`) or globally via config -- balancing quality vs token spend
- **Lifecycle:** `/gsd:new-project` (questions -> research -> requirements -> roadmap) -> `/gsd:discuss-phase` (lock preferences) -> `/gsd:plan-phase` (research + plan + verify loop, up to 3x) -> `/gsd:execute-phase` (wave execution + atomic git commits) -> `/gsd:verify-work` (manual UAT with auto-diagnosis)
- **Brownfield support:** `/gsd:map-codebase` spawns parallel agents to map stack, architecture, conventions, and concerns before project init -- questions then focus on what you're adding, not what exists
- **Session management:** `/gsd:pause-work` saves handoff state; `/gsd:resume-work` restores. STATE.md tracks decisions, blockers, and position across sessions

### GSD Executor: Deviation Rules and Analysis Paralysis Guard

- Deviation rules hierarchy: Rule 1 (auto-fix bugs), Rule 2 (auto-add missing critical functionality), Rule 3 (auto-fix blocking issues), Rule 4 (ask about architectural changes). Rules 1-3 need no user permission; Rule 4 stops for user decision
- Analysis paralysis guard: if 5+ consecutive Read/Grep/Glob calls with no Edit/Write/Bash action, STOP -- either write code or report "blocked." Analysis without action is a stuck signal
- Fix attempt limit: after 3 auto-fix attempts on a single task, stop fixing, document issues, continue to next task. Prevents infinite repair loops
- Scope boundary: only auto-fix issues directly caused by current task's changes; pre-existing warnings are out of scope, logged to `deferred-items.md`
- Checkpoint protocol: three types -- human-verify (90%), decision (9%), human-action (1%); auto-mode can auto-approve verifications and auto-select first option
- Self-check: verify all claimed files and commits exist before proceeding -- prevents plausible echo in status reports

*Source: get-shit-done/agents/gsd-executor.md*

(see [testing-verification.md](testing-verification.md) for the Nyquist validation layer that pre-maps test coverage)

*Source: get-shit-done/README.md, get-shit-done/docs/USER-GUIDE.md*

### GSD Open Source Announcement Context

- @simplifyinAI framed Get-Shit-Done as solving "AI context rot" -- the accumulated garbage problem in long sessions
- Core pitch: breaks projects into phases, clears context between them, uses parallel agents for zero-drift execution
- Works with both Claude Code and Gemini CLI
- 100% open source
- Complements the detailed GSD coverage above with the community framing of what problem it solves

*Source: Twitter Bookmarks/Thread by @simplifyinAI 1.md*

### Requirements-Driven Phase Derivation

Phase structure derived from requirements, never imposed:

- **Core rule:** Never decide number or scope of phases first -- let the work's natural boundaries determine structure
- **Coverage validation:** 100% requirement-to-phase mapping with zero orphans (every requirement traced to a phase)
- **Goal-backward at phase level:** Success criteria phrased as "What must be TRUE?" with observable user behaviors, not implementation tasks
- **Depth calibration:** Quick/Standard/Comprehensive modes with different levels of detail per mode
- **Traceability updates:** Maps requirements to phases, enabling downstream verification that implementation matches intent

(see [testing-verification.md](testing-verification.md#goal-backward-plan-verification-8-dimension-framework) for the 8-dimension verification this feeds into)

*Source: get-shit-done/agents/gsd-roadmapper.md*

### GSD State Management Templates: Section Mutation Rules and Session Handoff

Implementation-level patterns from GSD templates for managing persistent state across context resets:

**Section Mutation Rules (DEBUG.md pattern):**
- Each section in a persistent file has a declared mutation type: OVERWRITE (replace entirely), IMMUTABLE (never change after initial population), or APPEND-only (grow but never delete)
- **Eliminated section (APPEND-only):** Prevents the agent from re-investigating dead-end hypotheses after `/clear` -- once eliminated, always eliminated
- **Self-monitoring trigger:** "If evidence grows very large (10+ entries), consider whether you're going in circles. Check Eliminated."
- **`awaiting_human_verify` status:** Distinct state where agent does NOT mark resolved until user explicitly confirms -- prevents premature closure

**STATE.md Digest Principle:**
- Hard 100-line constraint -- STATE.md is the single entry point for every workflow, so brevity is enforced
- Tracks: current position (phase/plan/status with progress bar), velocity trends (improving/stable/degrading), accumulated decisions, and session pointer
- Lifecycle contract: specifies exactly when STATE.md is read vs written, and by which workflows

**Context.md Emergent Categories:**
- Categories are NOT predefined -- they emerge from what was discussed. A CLI phase has CLI sections; a UI phase has UI sections
- **Claude's Discretion zones:** Explicitly marks areas where the agent has freedom vs locked decisions
- Structured for downstream machine consumption by researcher and planner agents
- Good content: "Card-based layout, not timeline." Bad content: "Should feel modern and clean."

**Continue-Here Ephemeral Handoff:**
- `.continue-here.md` with YAML frontmatter (phase, task progress, status) and mental context/"vibe" section
- `<next_action>` must be actionable without reading anything else -- single entry point for resumption
- Ephemeral by design: file is deleted after resume, not permanent storage

*Sources: get-shit-done/templates/DEBUG.md, get-shit-done/templates/state.md, get-shit-done/templates/context.md, get-shit-done/templates/continue-here.md*

### GSD Research Pipeline Templates: Source Confidence and Negative Research

Research methodology patterns from GSD templates:

**Three-Tier Source Priority with Confidence:**

| Source | Confidence | Notes |
|--------|-----------|-------|
| Context7 MCP | HIGH | Curated, version-specific |
| Official docs + WebFetch | MEDIUM | Authoritative but may be stale |
| WebSearch alone | LOW | Requires cross-validation |

- **Negative claim verification:** Claims like "X is not possible" must be verified with official documentation before accepting
- **Session initialization:** Agent verifies today's date before searching, preventing stale date references in queries
- **Research validity expiration:** 30 days for stable tech, 7 days for fast-moving -- research output includes its own shelf life

**Negative Research Patterns:**
- **"Don't Hand-Roll" section:** Explicitly identifies problems that look simple but have existing solutions. Includes WHY column explaining hidden edge cases/complexity that make hand-rolling dangerous
- **Anti-Features category:** Explicitly research features that seem good but create problems, with alternatives. Prevents scope creep through negative research
- **Discovery vs Research distinction:** Discovery = shallow "which library?" question; Research = deep ecosystem knowledge. Explicit routing criteria prevent over-researching simple choices

**Requirements-as-Hypotheses Lifecycle:**
- Active requirements are treated as hypotheses -> Validated (shipped and confirmed user value) or Out of Scope (with reasoning to prevent re-adding)
- Key Decisions table with outcome tracking: Good / Revisit / Pending -- decisions treated as experiments, not commitments
- Success criteria flow: defined at roadmap level as observable behaviors -> flow downstream to `must_haves` in PLAN.md -> verified by verify-phase

*Sources: get-shit-done/templates/discovery.md, get-shit-done/templates/research.md, get-shit-done/templates/project.md, get-shit-done/templates/roadmap.md*

### GSD Planning Templates: Must-Haves Contract and Wave Orchestration

Executable plan format (PLAN.md) implementation patterns:

**Must-Haves Goal-Backward Verification:**
- Three verification types:
  - `truths`: Observable behaviors ("user can log in and see dashboard")
  - `artifacts`: Files with real implementation verified by `min_lines`, `exports`, and `contains` regex patterns
  - `key_links`: Connections between artifacts verified by regex (e.g., Chat.tsx actually calls `/api/chat`)
- Verification-by-contract rather than verification-by-testing -- can verify without running the app

**Wave Pre-Computation:**
- `wave` field in frontmatter pre-computed at plan time -- execute-phase reads directly, no runtime dependency analysis needed
- Anti-pattern: reflexive dependency chaining ("Plan 02 refs 01 just because 01 comes before 02")
- Vertical slices preferred over horizontal layer grouping

**Checkpoint Orchestration:**
- Task types: `auto`, `checkpoint:decision`, `checkpoint:human-verify`, `checkpoint:human-action`
- In parallel execution: plan runs until checkpoint, returns to orchestrator with `agent_id`, user responds, orchestrator resumes with `resume: agent_id`
- `user_setup` schema with automation-first rule: only includes what Claude literally cannot do (account creation, secret retrieval)

**Machine-Readable Summary Frontmatter:**
- `requires` (prior phases), `provides` (what this built), `affects` (future phases) -- enables automatic context assembly by scanning first 25 lines of all summaries
- Auto-fix deviation records with rule references (Rule 2 - Missing Critical, Rule 3 - Blocking) -- deviations classified and documented, not hidden
- `requirements-completed` field linking execution back to requirements traceability

*Sources: get-shit-done/templates/phase-prompt.md, get-shit-done/templates/summary.md, get-shit-done/templates/planner-subagent-prompt.md*

---

## Agentic Research Loop

A six-step pattern for deep research over any data source (demonstrated with X/Twitter but applicable broadly):

1. **Decompose** the question into 3-5 targeted queries using source-specific operators (core query, expert voices via `from:`, pain points, positive signals, link filtering, noise reduction)
2. **Search and extract** -- run each query, assess signal vs noise after each, adjust operators
3. **Follow threads** -- when a result has high engagement or is a thread starter, pull the full conversation
4. **Deep-dive linked content** -- fetch resources linked from high-engagement results (prioritize multiply-referenced links, technical resources)
5. **Synthesize** -- group findings by theme, not by query; include attributed quotes and linked resources
6. **Save** -- persist research output to a standard location for later reference

**Refinement heuristics:**
- Too much noise? Add exclusion operators, sort by engagement, narrow keywords
- Too few results? Broaden with OR, remove restrictive operators
- Expert takes only? Filter by author or minimum engagement threshold
- Substance over hot takes? Filter for posts with links

The loop is iterative -- each search informs the next query. Key accounts discovered during research can be added to a watchlist for ongoing monitoring via heartbeat/cron integration (see [tools-and-integrations.md](tools-and-integrations.md)).

---

## Transcript-to-Advisor Pipeline

A three-step workflow for turning publicly available expert knowledge (YouTube transcripts, podcast recordings, books) into callable AI advisor skills:

**Step 1 -- Scrape:** Use an agent (e.g., OpenClaw) to bulk-scrape YouTube channel transcripts and guest appearance transcripts. Save each as a separate text file named after the video title. One channel can yield 200+ pages of transcripts in under an hour.

**Step 2 -- Extract:** Feed all transcripts to Claude with an extraction CLAUDE.md:
- "Your job is to extract, not summarize"
- For every distinct framework, mental model, or repeatable principle: name it using the thinker's own terminology, state the core principle in one sentence, include a direct quote, explain the underlying psychology, and show how to apply it to your specific business context
- Note cross-connections between frameworks

**Step 3 -- Build advisor skills:** Convert extracted frameworks into a reusable advisor prompt:
- "You are a strategic advisor trained on [Thinker]'s complete body of work"
- Score work against their methodology (1-10 per dimension)
- Identify the weakest element using their reasoning, not generic advice
- Push back when the user makes a mistake the thinker has explicitly warned against
- Every recommendation must reference something the thinker actually taught

**The compounding effect:** Each advisor is a different lens. Run the same artifact (landing page, pricing strategy, positioning) through multiple advisors for multi-perspective stress-testing. The system is trained on actual teachings structured around your specific business, not generic AI output.

Create one CLAUDE.md per thinker, one Claude Project per advisor, upload transcripts into Project Knowledge. Can be combined with the recursive self-improvement loop pattern (see [skills.md#recursive-self-improvement-loop-skill-pattern](skills.md#recursive-self-improvement-loop-skill-pattern)) for scoring-based iteration.

---

## Choosing Your Workflow

### Plan Mode vs Think Mode

Two distinct modes for expanding AI reasoning, drawn from Claude Code's
Shift+Tab interface:

| Mode | Trigger | What It Does | Use When |
|------|---------|--------------|----------|
| Plan | Shift+Tab x2 | Breadth: research more files, explore options, create detailed plans before executing | Multi-step tasks requiring wide codebase understanding |
| Think | "Ultra think" in prompt | Depth: extended reasoning budget for complex logic | Tricky debugging, intricate logic, subtle architectural decisions |

These can be combined for complex tasks. Both consume additional tokens.

### Model Selection Strategy

| Task Type | Model | Why |
|-----------|-------|-----|
| Strategic planning, architecture, pattern naming | Opus | Deep reasoning, holds complex context |
| Day-to-day feature development | Sonnet | Balance of speed, quality, and cost |
| Fast simple tasks, large batches, state file updates | Haiku | Speed and cost efficiency |

Practical rule: **Get a plan from Opus, do 80-90% of the work with Sonnet.**

In the meta-agent architecture, Opus runs the strategic layer while Sonnet
subagents handle implementation. Haiku handles cheap mechanical tasks like
surgical markdown edits to state files.

### Session Audit Pattern: Self-Analyzing Workflow Efficiency

- Prompt Claude Code to analyze all local sessions and surface usage patterns
- Key prompt: "Analyze my usage patterns. What I do most frequently, what should become skills, plugins, agents, what belongs in CLAUDE.md"
- Outputs categorized recommendations with frequency, priority, time-saved estimates, and build-order
- Related: `/insights` skill already exists for similar session analysis
- Value: surfaces workflow inefficiencies and repetitive patterns that users don't notice when building command-by-command
- Extended version categorizes into 4 buckets: top 10 skills, top 5 tools/plugins, top 5 agents, missing CLAUDE.md sections (see [context-engineering.md](context-engineering.md#claudemd-your-always-loaded-memory))

*Source: Twitter Bookmarks/2026-03-08-shannholmberg-claude-workflow-audit-prompt.md*

---

## The Meta-Skill: Naming Patterns in Real Time

### "The Process Is a Product"

The most important skill in AI-assisted development is not prompt engineering.
It is the ability to extract process from practice in real time, while the
practice is happening.

This is not reflection. Reflection happens after. This happens during. You are
building and watching yourself build at the same time, and the watching changes
the building.

### The Extraction Cycle

```
Build -> Surprise -> Name -> Principle -> Process
  ^                                         |
  +------ apply and observe ----------------+
```

Concrete examples of the cycle in action:

1. **Build**: An agent says "all tests pass" at 90% completion.
   **Name**: "Premature Completion."
   **Principle**: Agents declare success based on what they completed, not the
   full spec. Verify artifacts, not self-reports.

2. **Build**: A single context window cannot hold the why and the how without
   one compressing the other.
   **Name**: "Vision Compression."
   **Principle**: Strategic and implementation context must live in separate
   windows.

3. **Build**: An agent produces output that looks correct but is not.
   **Name**: "Plausible Echo."
   **Principle**: Most people cannot distinguish a real result from a plausible
   echo because they inspect the self-report instead of the artifact.

4. **Build**: A bug gets fixed but the system learns nothing.
   **Name**: "Dead-end fix."
   **Principle**: Every fix must update a skill or it will recur.

(see [failure-patterns.md](failure-patterns.md) for the full catalog of named failure modes)

### Named Problems Become Workable

The act of naming a pattern makes it actionable. Once you call something
"Vision Compression," you can design against it (separate context windows).
Once you call something "Premature Completion," you can guard against it
(explicit completion criteria). Unnamed problems become technical debt with
philosophical implications.

The difference between building with AI and being built by AI is whether you
can name what is happening while it is happening. That naming is only possible
when something -- a meta-agent, a pattern journal, a disciplined practice --
is holding the context you cannot.

Hold your patterns loosely. The next round of contact with reality will reshape
them. The process evolves through use, not through design.

---

## Quick Reference

| I need to... | Use |
|--------------|-----|
| Build a well-defined feature with architectural judgment | Pattern 1: Spec-Driven |
| Ship a batch of independent tasks overnight | Pattern 2: Ralph Loop (AFK) |
| Manage multiple parallel workstreams | Pattern 3: Meta-Agent |
| Debug a tricky issue requiring deep reasoning | Think Mode (any pattern) |
| Explore a codebase before deciding on approach | Plan Mode (any pattern) |
| Extract a lesson from a mistake | Feedback Loop (Step 7 of Pattern 1) |
| Hand off context between sessions | State files + handoff prompts (Pattern 3) |
| Deep research from social/web sources | Agentic Research Loop |
| Structured feature development with gates | RPI Workflow |
| Multi-skill orchestration via agents | Command -> Agent -> Skills |
| Beginner-friendly AI development | Milestone Loop or Dual-AI Planner/Executor |
| Context-aware execution with fresh subagent windows | Pattern 6: GSD |
| Multi-phase feature development with parallel agents | Feature-Dev (Pattern 4 variant) |
| Autonomous multi-session app building | Immutable Test List (Pattern 2 variant) |
| Parallel Claude Code instances | Parallelization: Cascade / Worktrees / /fork |
| Turn expert knowledge into callable AI advisors | Transcript-to-Advisor Pipeline |
| Self-audit Claude Code usage for optimization | Session Audit Pattern |
| Non-programmer mental model for AI-assisted dev | Director Mental Model |
| Add features methodically | Feature Addition: 5-Phase Workflow |
| Fix bugs systematically | Bug Fix: 5-Step Workflow |
| Git operations as a non-programmer | Director-Level Version Control |

