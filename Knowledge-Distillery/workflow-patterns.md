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

*Source: Twitter-Bookmarks/Thread by @EXM7777.md*

### Cowork Context Files Strategy: Better Files Beat Better Prompts

@heynavtoor's full Cowork setup guide centers on a mindset shift: "stop thinking about better prompts and start thinking about better files."

- **Three Core Context Files:** `about-me.md` (role, success criteria), `brand-voice.md` (communication style, phrases, examples), `working-style.md` (preferences for Claude's behavior, output format, question-first approach)
- **AskUserQuestion as Default:** Add "DO NOT start working yet. First, ask me clarifying questions" to every non-trivial prompt -- eliminates the "polished garbage" problem of AI guessing wrong
- **Key Quote:** "ChatGPT trained you to write better prompts. Cowork trains you to build better context. One is a skill that depreciates. The other compounds."
- **5 Cowork Features Ranked by Impact:** 1) File System Access, 2) AskUserQuestion, 3) Plugins, 4) Instructions (global + folder), 5) Connectors
- **Instructions as Persistent Memory:** Global instructions load every session; folder instructions are project-specific -- workaround for no cross-session memory
- **Connector Strategy:** Link tools once (Slack, Drive, Notion), then Claude references live data mid-conversation -- "most underused feature"

(see [context-engineering.md](context-engineering.md#claudemd-your-always-loaded-memory) for the CLAUDE.md equivalent in Claude Code; see [prompt-engineering.md](prompt-engineering.md#core-principle-specificity-is-everything) for the specificity principle this builds on)

*Source: Twitter-Bookmarks/2026-02-25-heynavtoor-how-to-set-up-claude-cowork-the-right.md*

### Claude Cowork Starter Pack: Plugins, Context Files, and Morning Rituals

- Plugins are the power layer: Productivity (task/schedule/workflow), Marketing (draft/repurpose/campaign), Data (analyze CSV, SQL from English), Sales (account research, personalized outreach)
- Context files are what make plugins useful: about-me.md (identity, style, timezone), brand-voice.md (tone, vocabulary), current-projects.md (active work, deadlines, blockers) -- "the prompting game is over, the context game is everything"
- Morning dashboard workflow: reads calendar, priorities, and open tasks in 30 seconds; end-of-day shutdown workflow closes loops and preps tomorrow

*Source: Twitter-Bookmarks/2026-03-15-coreyganim-httpstcor60ja9ptkc.md*

### Obsidian + Claude Cowork as AI Employee: Persistent Business Operating System

- Three components: structured knowledge base (Obsidian vault with Memory file, Client Roster, Action Tracker), automatic memory loop (call transcripts → Drive → Claude processes and writes back to vault), intelligence layer (Claude Cowork + MCP connectors to Slack, Calendar, Drive)
- Memory file is the onboarding doc for an AI that never forgets -- write it once; every session starts fully briefed
- Compound effect: every processed call adds context; after 8 weeks, the AI catches things you missed, reminds you of commitments from forgotten calls
- One instruction in custom preferences: "Before answering, always search the Obsidian vault for relevant notes" -- this single line makes Claude context-aware without manual copy-paste

*Source: Twitter-Bookmarks/2026-03-21-sourfraser-httpstcoo5osbj933j.md*

### NotebookLM + Gemini + Obsidian: Learning Compression Workflow

- Three-layer stack: NotebookLM as "source brain" (PDFs, YouTube, articles), Gemini as "reasoning engine" (attaches to NotebookLM, reasons over sources + web), Obsidian as "long-term memory"
- Key step: prompt Gemini to split source material into Section A (basic/repeated) and Section B (new, counter-intuitive, high-leverage) -- only capture Section B; eliminates 80% of repeated content
- Repeatable weekly sprint: Collect → Compress in Gemini → Store in Obsidian → Revise from Obsidian only (never from raw sources)
- The "delta extraction" approach (only capturing what is genuinely new or non-obvious) is a valid pattern for any KB ingestion pipeline

*Source: Twitter-Bookmarks/2026-03-26-KanikaBK-httpstco9xrnfpthpu.md*

### Pixel-Perfect Website Reverse Engineering

- An AI-assisted workflow template for reverse-engineering websites to pixel-perfect reproductions is available as a GitHub resource (JCodesMore/ai-website-cloner-template)
- Useful reference for structured visual accuracy requirements in web development agent workflows

*Source: Twitter-Bookmarks/2026-03-27-tom_doerr-pixel-perfect-website-reverse-engineering-httpstcojhuudrs2ir.md*

### Claude Code CLI Power Flags: Scripting, Cost Control, Multi-Repo

- **`-p` flag (non-interactive mode):** processes prompt and exits; turns Claude Code into a CLI tool for scripts and pipelines; enables JSON output and schema validation; use for cron jobs, CI/CD, Unix pipes (e.g. `git diff main | claude -p "review for security issues"`)
- **`--max-budget-usd N`:** hard spending cap per session; Claude stops when it hits the cap; prevents runaway costs on stuck tasks; pair with `--max-turns` to limit back-and-forth iterations; both essential for CI/CD with predictable costs
- **`--add-dir`:** gives Claude visibility across multiple directories or repos simultaneously; Claude only scans specified directories, reducing noise and keeping context focused
- **`claude -w branch-name`:** creates isolated git worktree, does all work there, commits, optionally creates PR; main branch completely untouched; if something goes wrong, your main codebase was never touched
- **`--permission-mode auto`:** AI safety classifier reviews each action before it runs; checks for risky behavior and prompt injection while letting routine work proceed; middle ground between clicking "yes" every 30 seconds and `--dangerously-skip-permissions`
- **`-c` / `-r name` / `-n name`:** continue last session, resume by name, name current session; keep separate named sessions for separate work streams; context for each work stream stays clean
- **Pipe pattern:** `git diff main | claude -p "review for security issues"` replaces 90% of dedicated code review tools; `-p` flag is where Claude Code stops being a chat tool and becomes infrastructure

*Source: Twitter-Bookmarks/2026-03-31-zodchiii-httpstcofa9qn1cgf0.md*

### COMP System: Four-File Project Context Architecture

- Every project maintains four standardized files: CLAUDE.md (behavioral contract, agent-facing), ORIENT.md (orientation for humans returning after time away), MEMORY.md (cross-session decisions and gotchas), PLAN.md (roadmap with a refreshed `## Current State` section each session)
- ORIENT.md answers "what do I need to know after two weeks away?" -- written for humans, not agents: project description, mental model, common operations, known weirdness, key links; not a file index
- PLAN.md's `## Current State` section is refreshed every session; MEMORY.md captures durable knowledge; no duplication between them
- CLAUDE.md health check: quarterly, audit whether every instruction earns its place in always-loaded context; move stale rules to on-demand guides
- Corrective framing over reminders: when an agent keeps forgetting something, present a specific possibly-wrong claim that triggers corrective behavior rather than adding another "remember to X"
- (see [context-engineering.md](context-engineering.md#claudemd-your-always-loaded-memory) for CLAUDE.md design; [memory-persistence.md](memory-persistence.md) for MEMORY.md layer patterns)
*Source: claude-code-synthesis/CLAUDE.md*

### Tiered Session Start Command

- Three session modes: quick (PLAN.md current state + MEMORY.md only, start immediately), standard (PLAN + MEMORY + CLAUDE.md + brief dashboard), full (all 4 COMP files + detailed plan with scope estimate)
- Full mode applies scope discipline: if task is multi-session, say so and propose a first-session subset; if prerequisites are visible, flag them
- Micro-plan in standard mode: 3 steps max if task is provided; otherwise suggest next item from PLAN.md
- Pattern: session mode is a configurable dial, not a fixed startup sequence
*Source: claude-code-synthesis/commands/start.md*

### Compound Engineering Workflow Philosophy

- Core model: Brainstorm → Plan → Work → Review → Compound; each cycle compounds knowledge into the next
- 80/20 rule applied to AI-assisted development: 80% effort in planning and review, 20% in execution; planning is the primary leverage point
- Plans are decisions-first artifacts: file paths, dependencies, sequencing, risks, test scenarios -- no implementation code or shell commands
- Plans distinguish "resolved during planning" from "deferred to implementation-time discovery" -- open questions are intentional classification, not bugs
- Explicit handoff contracts: each phase produces an artifact the next phase consumes without re-inventing decisions
- "Enthusiastic junior engineer with poor taste, no judgment, and an aversion to testing" is the target audience for implementation plans -- plans must be explicit enough for that persona
*Source: compound-engineering-plugin/docs/brainstorms/2026-03-14-ce-plan-rewrite-requirements.md*

### Separation of Planning from Execution

- Plans must not contain implementation code, test-run results, or exact git commands -- these belong to the execution skill
- "Planning stops before execution" is a hard boundary: no code snippets, no fail/pass feedback loops, no commit choreography in plan artifacts
- Plans remain shareable as documents or issues without executor-specific litter (tool-call choreography, inline results)
- When requirements from upstream contain unresolved product blockers, planning must pause -- not proceed on assumptions
*Source: compound-engineering-plugin/docs/brainstorms/2026-03-14-ce-plan-rewrite-requirements.md*

### Red/Green TDD as the Highest-Leverage Agentic Pattern

- Simon Willison names "red/green TDD" as the single highest-leverage agentic engineering pattern: agent writes failing tests first, then implements code to pass them, then verifies green
- The five-word prompt "use red/green TDD" encodes the entire workflow because agents recognize the jargon and execute the full loop without further instruction
- Contrast with post-hoc testing: agents that write code first and tests after routinely claim tests pass before confirming; test-first removes this failure mode by construction
- Companion pattern -- "hoarding things you know how to do": maintain a repo of small proof-of-concept tools and experiments; when a new problem arrives, point the agent at past projects and say "combine these two approaches"
- Code is cheap now -- the bottleneck has shifted to deciding what to build, proving ideas work, and getting user feedback; building three prototype versions to explore the design space is now economically rational

(see [Pattern 1: Spec-Driven Feature Development](workflow-patterns.md#pattern-1-spec-driven-feature-development) for where test-first fits in the broader spec workflow; see [testing-verification.md](testing-verification.md) for verification patterns)

*Source: 2026-04-03-lennysan-my-biggest-takeaways-from-simonw-1-november-2025-was-an-infl.md*

### Idea File: Agent-Buildable Spec as Shareable Artifact

- In the era of LLM agents, the primary shareable artifact shifts from specific code/apps to the *idea* itself -- expressed as a concise, intentionally abstract spec that any agent can implement for its owner's specific needs
- Format: a brief markdown description (a "gist") of what the system should do, kept deliberately vague to leave room for each agent to customize; users give it to their own agent which then builds and guides configuration
- Operational implication: sharing an idea file is more valuable than sharing the code because the code has one implementation; the idea file generates N implementations each optimized for the recipient's context
- Apply to this KB: any workflow pattern can be captured as an idea file rather than a prescriptive implementation, making it agent-portable
- Concrete example: Karpathy's "LLM wiki" -- a personal knowledge base where LLMs build and maintain structured topic wikis from research inputs. The gist describes what the system should do; each user's agent builds their own version customized to their workflow. A large fraction of his recent token throughput goes into manipulating knowledge, not code
- Pattern shift: LLMs as knowledge infrastructure, not just code tools -- the same agent that writes your code can curate, structure, and maintain your research (see [memory-persistence.md](memory-persistence.md) for related knowledge management patterns)

(see [skills.md](skills.md) for how skills encode similar concepts in a more structured format)

*Source: 2026-04-04-karpathy-wow-this-tweet-went-very-viral-i-wanted-share-a-possibly-sli.md, 2026-04-06-NickSpisak-httpstco2ano3c1ubq.md*

### AI Distribution Strategies for Vibe Coders: Distribution > Code

- AI commoditized code; distribution is the new scarce skill; "the people who understand how to get customers, build audiences, and earn attention are at the top of the stack" (Peter Levels: $3M+ revenue, zero employees, 750K followers = the moat)
- **MCP servers as distribution channel:** build an MCP server for your product's core value; zero customer acquisition cost; AI assistant discovers it and returns it as the answer; early movers own registries (Smithery, MCPT, OpenTools); "building an MCP server in 2026 is like building for mobile in 2010"
- **AEO (Answer Engine Optimization):** optimize to be cited by ChatGPT and Perplexity instead of Google; write structured, direct, citation-worthy answers for the top 20 questions your customer asks; add schema markup and FAQ blocks; Peter Levels reported AI referrals jumped from 4% to 20% in a single month
- **AI content repurposing engine:** one 30-minute voice memo -> transcribe -> Claude generates: 5-10 tweets, 3-5 LinkedIn posts, 2-3 short videos, 1 newsletter, 5-10 quote graphics; shots-on-net strategy; optimize for your voice not default AI slop; repeat weekly
- **Viral artifacts:** identify what output your user wants to screenshot and brag about; make it beautiful and shareable; add pre-filled share button; every share = free impressions to exact target audience
- Core principle: "AI cannot build distribution for you. It can help you scale it. But the trust, the audience, the SEO authority: those take real effort and compound over time."

*Source: Twitter-Bookmarks/2026-03-30-startupideaspod-httpstco3nhxfqbsdf.md*

### Full Lead Gen Pipeline Vibe-Coded in 2 Weeks

- One developer used Claude Code to build a complete lead generation + outreach system: scrapes every business from Google Maps with 30+ data fields, visits actual websites for verified emails/phone/social profiles (live, not from a database), reads up to 50 Google reviews to find pain points, cross-references your offer with those pain points to write personalized cold emails per business, sends one-by-one (not bulk) for primary inbox deliverability
- GPS-mapped CRM with territory routing, optimized driving routes, team activity tracking, voice note transcription built in; works in 200+ countries
- Illustrates what is now achievable by a solo developer in two weeks with AI coding assistance; the entire sales pipeline -- from lead discovery to personalized outreach to CRM -- collapsed into one tool

*Source: 2026-04-04-om_patel5-someone-vibe-coded-a-tool-that-finds-businesses-reads-their.md, 2026-04-05-RoundtableSpace-someone-vibe-coded-a-full-lead-gen-tool-with-claude-code-in.md*

### Claude+Gamma Workflow for Professional Presentations

- Three methods ranked by output quality: Claude alone (3/10 -- generic, no brand), Gamma alone (8/10 -- polished but shallow), Claude+Gamma combined (best results)
- Optimal workflow: Research phase (Claude deep research for substance) -> Brief phase (structured outline with key points) -> Generate phase (Gamma turns brief into polished slides) -> Edit phase (human refinement, 10-15 min)
- Brand consistency at scale: extract brand guidelines into a markdown file, then create a Gamma theme from an existing brand template -- AI-generated decks match corporate identity without per-deck styling
- "Vague prompt = pretty slides that say nothing" -- the research and briefing stages determine output quality, not the generation tool; this mirrors the spec-driven pattern where upstream clarity eliminates downstream waste (see [Pattern 1: Spec-Driven Feature Development](#pattern-1-spec-driven-feature-development))

*Source: Twitter-Bookmarks/2026-03-09-rubenhassid-httpstcodah90zdxmt.md*

### Obsidian + AI Agent Shared Folder Pattern

- Core pattern: point both Obsidian and an AI agent terminal at the same folder so both read and write the same markdown files
- AGENTS.md in the folder root serves the same function as CLAUDE.md: persistent instructions the agent reads before every response (see [context-engineering.md#claudemd-your-always-loaded-memory](context-engineering.md#claudemd-your-always-loaded-memory))
- Store everything as Markdown -- Obsidian's native format and the cleanest format for LLM consumption; non-markdown formats (PDFs, DOCX) break the shared-folder pattern
- Graph-powered exploration: the agent can follow Obsidian backlinks (`[[wikilinks]]`) to synthesize across the knowledge base, surfacing connections across notes
- Three mistakes that break the setup: (1) no AGENTS.md giving the agent instructions, (2) storing content in non-markdown formats the agent cannot parse, (3) keeping the agent workspace and notes in different folders so they cannot see each other

*Source: Twitter-Bookmarks/2026-03-13-Atenov_D-httpstcoicy5hmqxgi.md*

### Six AI Skills That Create Income Premiums

- Context engineering as a distinct high-value skill: setting up AI environments that already know your work, processes, voice, and historical decisions before you start prompting (see [context-engineering.md](context-engineering.md))
- Designing AI into workflows: knowing where human-agent handoffs happen, what triggers escalation, when the agent should be autonomous vs ask for help -- the workflow design skill underlying every pattern in this file
- Systematic quality control: building frameworks and checklists that catch AI errors at scale rather than relying on manual review of every output (see [testing-verification.md](testing-verification.md))
- Knowing what NOT to automate is as valuable as knowing what to automate -- some tasks lose value when automated (relationship-building, judgment calls, creative direction)
- The gap between "using AI" and "integrating AI" is the income gap: practitioners who integrate AI into workflows command $40-60K salary premiums and $150-250/hr consulting rates over those who merely use AI tools

*Source: Twitter-Bookmarks/2026-03-10-Zephyr_hg-httpstcobzqotxnhzt.md*

### Red-Green Commit Discipline at AI Scale

The 7-commit rhythm that shipped a 5-bug payment fix without regressions. Each commit followed identical discipline:
**Write a failing test → commit it red → implement the fix → run the suite → commit it green.**

- Commit 1: Remove jarring auto-redirect → green
- Commit 2: Failing test for duplicate init under React StrictMode → red
- Commit 3: Add `initCalledRef` guard → green
- Commit 4: Failing test -- calling finalize twice should succeed both times → red
- Commit 5: Make finalize endpoint idempotent → green
- Commits 6-7: Stop polling in terminal states + re-read `stateRef.current` after the await -- preventive guards from same root-cause analysis (no separate failing tests because they hardened against the failure mode, not a specific regression) → green
- After EACH commit: full suite ran (1,014 Next.js tests + 393 invoice-svc tests + TypeScript compilation). All had to pass before next milestone.
- After all commits: Playwright on the full payment flow confirmed "You're Going!" persists even when late poll fires.

**The principle:** **"The AI is random. The gate is deterministic. Spin until green."**

7 commits = 7 trips through the gate. The code that shipped is the code that survived. Each commit small enough to review in <1 minute. Each touched ~2 files. The structure forced understanding.

**Generalizes to:** any AI-driven multi-bug fix where the temptation is to do "everything at once." Discipline = artifacts at every state transition.

*Source: Andrew-Vibe-Coding/Vibe Engineering From Random Code to Deterministic Systems (Part 6).md*

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

### Implementation Behavior Rules

- Surface assumptions as a numbered list before any non-trivial task: "Correct me now or I'll proceed with these"
- Three-fix escalation rule: if a fix has been attempted 3 times and the problem persists, STOP -- don't try a fourth; escalate with what was tried and why it's not working
- Red flag language: "should work," "probably fine," "seems to handle," "Done!," "Perfect!" -- treat as signal that completion is being claimed without verification
- Compaction-safe artifacts: write important outputs to files immediately; during complex work, periodically write a 3-5 line session state summary
- Naive-then-optimize: implement the obviously-correct naive version first, verify correctness, then optimize while preserving behavior
- Prefer structured over prose for rules agents MUST follow: XML tags, numbered steps -- Claude processes tagged content differently
*Source: claude-code-synthesis/CLAUDE.md*

### AI Infinite Surface Area Trap -- Do Less, Not More

- AI creates an "infinite surface area" trap: every new tool and capability invites expanding what you do, distributing attention ever thinner across more projects, more automations, more workflows
- Attention is the only input that does not scale -- you can automate output but not care; stretching across too many things produces shallow results everywhere
- Counterintuitive advice: use AI to go deep on one thing rather than wide across many; AI works best as a force multiplier for depth, not a license for breadth
- Directly relevant to scope discipline throughout this file: the "NOT in MVP" list (see [Step 1: Write the Spec](#step-1-write-the-spec)), minimum viable parallelization limits (see [Parallelization Patterns](#parallelization-patterns-cascade-and-two-instance-kickoff)), and the focus principle behind "choose one goal, delete the rest"

*Source: Twitter-Bookmarks/2026-03-12-lucas__crespo-httpstcooblvzlq3yq.md*

### Constitutional Invariants -- INV-1 Through INV-N as Test Cases

After multi-persona diagnosis (see agent-design.md), define invariants BEFORE writing code. Each invariant becomes a verification test.

**Sparkpass payment-bug example -- 5 invariants:**
- **INV-1:** Lightning payment is the source of truth for payment status
- **INV-2:** Never display an invoice without verifying it via NWC first
- **INV-3:** Audit/logging failures must never block user-facing operations
- **INV-4:** Users always receive actionable guidance, even during degradation
- **INV-5:** Graceful degradation over total failure -- partial information beats no information

**Why INV-1 is load-bearing:** if Lightning says "paid," the user paid -- regardless of database state. Recovery flows directly from this: status endpoint calls `getInvoiceStatus()` via NWC for each invoice *before* returning. NWC takes precedence over DB. Database sync is fire-and-forget. **Without INV-1, would have built retry logic against the database; with it, built verification against Lightning.** The invariant didn't add time -- it removed the wrong solution from the search space.

**Each invariant translates directly to a verification step:**
- INV-1 → Test: When DB is down but NWC confirms payment, UI shows success
- INV-3 → Test: When FundsFlow creation fails, payment acknowledgment continues
- INV-4 → Test: When status is unknown, UI shows guidance message (not blank, not spinner)
- INV-5 → Test: When audit logging fails, payment flow continues

**INV-5 prevented over-engineering.** Initial instinct: full event-driven architecture with message queues + guaranteed delivery. INV-5 said: show the user what you know, even if incomplete. Degraded experience that communicates beats perfect system that goes silent.

**Pattern: invariants are reusable across projects.** Constitutional rules ("X is the source of truth," "Y must never block Z") tend to recur. Encode them at the project level for the AI to apply.

*Source: Andrew-Vibe-Coding/Vibe Engineering From Random Code to Deterministic Systems (Part 6).md*

### Worklog Milestones with Explicit Deferral Rationale

The worklog discipline that prevents AI scope creep on complex bugs.

**The Sparkpass example:** 6 milestones planned. **2 shipped. 4 deferred -- intentionally.**

- **Shipped (M1-M2):**
  - NWC-first status verification
  - Error detection + graceful UX degradation
- **Deferred (M3-M6):**
  - Event-driven architecture with message queues
  - Circuit breaker for database connections
  - Comprehensive monitoring dashboard
  - Automatic retry queue for failed database writes

**Why deferral matters:** all 4 deferred items were good ideas. They were also pre-launch MVP scope creep. @Founder-Agent flagged it: "M1-M2 fix the user-facing problem. M3-M6 are infrastructure hardening for a product with zero users. Ship, launch, harden later."

**Without explicit milestones with deferral rationale,** Claude would have happily implemented all 6 -- the worklog gave permission to STOP. The pattern is **don't just list what to do; list what NOT to do and why.**

*Source: Andrew-Vibe-Coding/Vibe Engineering From Random Code to Deterministic Systems (Part 6).md*

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

*Source: Twitter-Bookmarks/2026-03-01-mustang_akin-beginner-vibe-coder.md*

### The Director Mental Model (Non-Programmer Framing)

A practical mental model for non-coders using Claude Code, drawn from a 20-hour "Claude Code for Non-Programmers" curriculum:

- **Core analogy:** You are a film director, not a camera operator. Directors communicate vision, understand enough craft for productive conversations, recognize when something is wrong, and know how to course-correct -- but never operate the equipment themselves
- **Key mindset shift:** Tell Claude WHAT you want to accomplish, not HOW to do it. "Add an interactive quote randomizer with smooth animations" outperforms "Create a div with class 'quote-box' containing a p tag..."
- **Specificity spectrum:** Neither vague ("make it better") nor hyper-precise (exact pixel values) is always correct. The sweet spot: specific about WHAT and CONSTRAINTS, flexible on HOW
- **When to direct vs delegate:** Direct explicitly on user-facing text, visual design, business logic, and integration points. Delegate to Claude on implementation details, best practices, code organization, and tool/library choices
- **Iteration is a feature, not a bug:** The revision cycle (instruct -> review -> specific feedback -> repeat) is a legitimate workflow, not a failure of initial instruction. Good feedback acknowledges what works, specifies exactly what to change, and provides clear direction

*Source: Learning-CC/notes/module-1-reflection.md, module-3-reflection.md, module-5-reflection.md*

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

*Source: Learning-CC/new-project-key-steps.md, Learning-CC/notes/module-7-reflection.md*

### Bug Fix: 5-Step Workflow

A systematic bug-fixing workflow that prevents random guessing:

1. **Reproduce** -- Make the bug happen reliably. Cannot fix what you cannot see. Document exact steps.
2. **Locate** -- Find the responsible file and function. "What part of the code is likely responsible?"
3. **Understand** -- Why is this happening? "Explain what the current code is doing and why that causes the bug."
4. **Fix** -- Choose the safest fix. "What's the safest way to fix this without breaking anything else?"
5. **Test** -- Verify: original bug is gone, no new bugs introduced, related functionality still works, edge cases handled.

Complementary to the troubleshooting taxonomy in failure-patterns.md (see [failure-patterns.md#troubleshooting-taxonomy](failure-patterns.md#troubleshooting-taxonomy-three-problem-types)).

*Source: Learning-CC/new-project-key-steps.md, Learning-CC/notes/module-6-reflection.md*

### Director-Level Version Control

Git concepts framed for non-programmers who direct Claude through git operations:

- **Branches as risk-free innovation:** Create a branch before risky work, experiment freely, merge if successful, delete if not. "I don't need to be afraid to experiment. Git has my back."
- **Two levels of recovery:** Uncommitted changes -> `git restore` (undo before saving). Bad commit -> `git reset --hard HEAD~1` (undo a save). Two states of change need two different tools.
- **Director language for git:** Never say "do a hard commit reset." Instead: "That last commit broke things. Can you help me undo it and get back to the previous working state?" Your value is knowing what is possible, not memorizing commands.
- **Commit philosophy:** Each commit represents one logical change with a clear descriptive message. Git commit is a checkpoint, not a ceremony.

*Source: Learning-CC/notes/module-8-reflection.md*

### 50 Claude Code Tips: Two-Session Review and Context Management

- /clear between unrelated tasks: context from earlier tasks actively drowns out current instructions
- Two-session review pattern: first Claude implements, second Claude reviews from fresh context -- different from just asking the same session to review its own work
- Guide /compact with explicit guidance ("focus on API changes and modified files") to preserve critical context; re-inject key context automatically via a Notification hook post-compaction

*Source: Twitter-Bookmarks/2026-03-19-CodevolutionWeb-httpstcotxmjpjngdo.md*

### Anime.js Site Build Recipe with Claude
- Minimal four-step workflow: (1) Ask Claude to plan a minimal interactive website with smooth motion. (2) `npm i animejs`. (3) Use Claude to generate timelines, staggered text, hover animations. (4) Add smooth SVG, scroll, and cursor effects. Small but valid template for AI-assisted creative-web work.

*Source: 2026-05-09-Oluwaphilemon1-how-i-built-an-animejs-style-site-with-claude-ask-claude-to.md*

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

### Human Gate Pattern in Automated Pipelines

- A pipeline step can be a "human gate": the automated pipeline detects a condition (e.g., uncategorized records), reports the count, and pauses; the human runs agents externally, then resumes
- Skip flags (`--skip-enrich`, `--skip-categories`) enable partial re-runs so later pipeline stages can resume without re-running completed steps
- Separation of concerns: automated pipeline (deterministic transforms) vs. LLM agent steps (non-deterministic, require oversight) -- gate at the boundary
- "Known Weirdness" section in ORIENT.md as a design element: documents encoding quirks, API oddities, workarounds that would otherwise cost debugging time on return
*Source: claude-code-synthesis/examples/data-pipeline/guides/pipeline-steps.md*

### PRD-to-Task Pipeline (Task Master)

- Parse a PRD into a structured task list with `parse_prd`, then immediately run complexity analysis and `expand --all --research` to size and decompose every task before coding begins
- Task IDs are hierarchical (1, 1.1, 1.1.1); each task carries title, description, status, dependencies, priority, details, and testStrategy
- The `next` command selects the highest-priority pending task with all dependencies satisfied -- use it to start every session rather than picking tasks manually
- Use `update --from=<id>` when implementation drift requires revising future tasks; use `update-subtask --id=<id>` to log timestamped implementation notes inside a task (creates an auditable plan log)
- Tiered MCP tool loading (core = 7 tools, standard = 14, all = 42+) keeps context window lean for daily workflow -- upgrade only when needed
*Source: claude-task-master/.taskmaster/CLAUDE.md*

### Tagged Task Lists for Multi-Context Development

- Tags create isolated task namespaces (`master`, `feature-auth`, `experiment-zustand`); changes in one tag never affect others
- Agent-trigger patterns: create a tag when user opens a feature branch, mentions a teammate, or describes a large PRD-driven initiative
- The `master` tag holds only high-level milestones and release-blocking items; implementation subtasks live inside feature-specific tags
- `task-master add-tag --from-branch` auto-creates a tag matching the current git branch name, keeping tasks and branches in sync
*Source: claude-task-master/.kiro/steering/dev_workflow.md*

### Iterative Subtask Implementation Protocol

- Seven-step loop per subtask: (1) understand goal, (2) explore and plan, (3) log plan with `update-subtask` (file paths, line numbers, proposed diffs), (4) verify plan was saved, (5) set in-progress, (6) implement and log what worked/what didn't after each attempt, (7) mark done + commit
- "What didn't work and why" logging is as important as "what worked" -- prevents repeating mistakes across iterations
- Each `update-subtask` call appends a timestamped entry; review existing entries before adding new ones to avoid redundancy
*Source: claude-task-master/.kiro/steering/dev_workflow.md*

### Harness Engineering: Automated Code Write-and-Review Loop

A control-plane pattern for repos where agents write 100% of the code and review agents validate every PR. The specific reviewer can be Greptile, CodeRabbit, CodeQL, or a custom LLM -- the pattern stays the same (see [Pattern 2: The Ralph Loop](#pattern-2-the-ralph-loop-autonomous-coding) for related orchestration concepts).

**The Loop**
1. Coding agent writes code
2. Repo enforces risk-aware checks before merge
3. Code review agent validates the PR
4. Evidence (tests + browser + review) is machine-verifiable
5. Findings feed back as repeatable harness cases

**Key Principles**

| Principle | Why It Matters |
|---|---|
| Single machine-readable contract | Defines risk tiers by path, required checks by tier, docs-drift rules, evidence requirements. Removes ambiguity and prevents silent drift between scripts and policy docs. |
| Preflight gate before expensive CI | Run `risk-policy-gate` first; only start test/build/security fanout if policy passes. Saves CI minutes on blocked PRs. |
| Current-head SHA discipline | Review state is valid only when it matches the current PR head commit. Ignore stale summary comments tied to older SHAs. Require reruns after every push. Without this, stale "clean" evidence can slip through. |
| Single rerun-comment writer with SHA dedup | One canonical workflow requests reruns; dedup by marker + `sha:<head>`. Prevents duplicate bot comments and race conditions. |
| Automated remediation loop | Review findings trigger a coding agent to read context, patch code, run local validation, push a fix commit to the same PR branch. Pin model + effort for reproducibility. Never bypass policy gates. |
| Auto-resolve bot-only threads after clean rerun | After a clean current-head rerun, auto-resolve unresolved threads where all comments are from the review bot. Never auto-resolve human-participated threads. |
| Browser evidence as first-class proof | For UI/flow changes, require evidence manifests and assertions in CI -- not just screenshots in PR text. Validate required flows, entrypoints, account identity, artifact freshness. |
| Harness-gap loop for incident memory | `production regression -> harness gap issue -> case added -> SLA tracked`. Converts one-off patches into long-term coverage. |

**Concrete Implementation Example**
- Code review agent: Greptile
- Remediation agent: Codex Action
- Workflows: `greptile-rerun.yml`, `greptile-auto-resolve-threads.yml`, `risk-policy-gate.yml`

*Source: Clawdbot-aka-Openclaw/Research/Code Factory How to setup your repo so your agent can auto write and review 100% of your code.md*

### "Money Printer" Autonomous Outbound: URL-to-Customer Pipeline

- Pattern: paste a website URL -> AI reads the site, infers ideal customer profile -> finds companies matching that profile that are actively looking -> identifies decision-maker contacts -> writes personalized outreach -> starts sending and even calls them
- No list building, no forms, no manual filters; starts from a URL and generates outbound pipeline automatically
- Extends the lead gen vibe-coding pattern (see [The Vibe Engineering Stack](#the-vibe-engineering-stack)) but frames it from the customer's perspective: the product understands your offer first, then finds buyers

*Source: 2026-04-06-heynavtoor-breaking-someone-built-a-money-printer-you-paste-a-website-a.md*

### Codex /goal + Hermes Agent + Telegram Kanban Pattern
- Hermes Agent skill that gives Codex a goal on-the-fly via Telegram and tracks each goal in a Kanban board. Short demo of the delegation-via-messaging-app pattern: trigger autonomous coding work from anywhere on your phone, watch progress on a board.

*Source: 2026-05-10-Saboo_Shubham-codex-goal-with-hermes-agent-is-life-changing-i-updated-my-h.md*

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

*Sources: Twitter-Bookmarks/The Longform Guide to Everything Claude Code.md, Twitter-Bookmarks/Best Practices for Claude Code (Use these to make Claude Code 100x Powerful).md*

### Chief of Staff Pattern: Non-Programmer Builds Full Autonomous Workflow

Non-programmer (@jimprosser) built a complete "Chief of Staff" system with Claude Code in 36 hours. Key patterns:

- **4-Color Task Triage:** AM Sweep classifies every task as Green (AI handles fully), Yellow (AI gets 80% done, human finishes), Red (needs human brain/presence), Gray (not actionable today)
- **Stream Deck as Agent Trigger:** Two physical buttons -- AM Sweep (triage + 6 parallel agents) and Time Block (schedule remaining tasks geographically)
- **6 Parallel Specialized Agents:** Each with scoped tool access and own context window -- email drafter (never sends, only drafts), Obsidian updater, meeting scheduler, background researcher, etc.
- **Overnight Automation:** Two cron jobs pre-6:15 AM scan calendar for drive times (Google Maps API) and triage email into Todoist with priorities/durations
- **Time Block Intelligence:** Batches errands geographically, knows home vs office vs location-specific tasks, schedules gym, defers overflow to lowest-load future day
- Build happened in "layers of functionality" over a year of tinkering, not a one-shot -- parallelized subagents were the unlock

(see [autonomous-agents.md](autonomous-agents.md#ceo-only-main-agent-pattern) for the delegation pattern; see [context-engineering.md](context-engineering.md#knowledge-type-placement-matrix) for how to structure the context files that make this work)

*Source: Twitter-Bookmarks/2026-03-05-jimprosser-chief-of-staff-claude-code.md*

### Channel-Isolated Parallel Agent Chains

Multi-agent content production pipeline using channel isolation for parallelization:

- **Pattern:** Research agent (trends) -> writing agent (scripts) -> thumbnail agent (images), each in its own Discord channel
- **Key insight:** Agents don't need to be aware of each other; channels handle routing. Output from one feeds visibly to the next
- **Advantage over sequential handoffs:** Creates transparency, allows feedback at each stage without blocking the pipeline
- Discord topics as a coordination primitive for multi-agent workflows -- simpler than explicit orchestration

(see [autonomous-agents.md](autonomous-agents.md#multi-agent-communication-direct-vs-boss-routing) for direct vs boss routing alternatives)

*Source: awesome-openclaw-usecases/usecases/content-factory.md*

### Hybrid Human-AI QA and Cross-System Integration

Emerging patterns combining Claude with non-LLM tools for higher quality:

- **Static analyzer pairing:** Run automated static analyzers or formal verifiers in tandem with Claude's outputs. Cross-system integration catches issues Claude misses (e.g., formal verification of state machine logic, SAST tools for security)
- **Cross-language agent glue:** Link multiple LLMs via orchestration scripts -- e.g., GPT-4 for certain code generation steps and Claude for others, leveraging each model's strengths. Under-documented but some teams report benefits from model-diverse pipelines
- **Meta-reinforcement via failure feedback:** Nascent idea -- track when Claude hallucinates and feed that as a penalty in prompt ranking. Early experiment: ask "What would you do differently next time?" after a mistake and use the answer to tune the next prompt
- These patterns are experimental and under-documented; watch community forums for maturation

*Source: deep-research-report.md*

### Production Case Study: 6-Agent Website Sales Pipeline

- Six sequential agents: Scout (Google Places API), Intel (website audit), Builder (demo site + UGC), Outreach (email + SMS), Closer (call prep), Growth (monitoring + upsell)
- Only human step is the actual sales call; everything else autonomous
- UGC stack: ElevenLabs voice, Nano Banana Pro talking head, Kling video, Puppeteer + ffmpeg walkthrough
- SMS as attention driver: no links, just heads-up to check email -- 40% open rates

*Source: how I use OpenClaw to sell websites on autopilot.md*

### Hermes Clipping Agent: Phone-Based Agent Army

- A 19-year-old built an entire content clipping agent system controlled from a phone via Telegram: one text with a YouTube link triggers the agent to extract high-performing clips, schedule them, and post -- no desktop required
- Hermes Agent runs 24/7 as the runtime; agent army architecture enables parallel clip processing and scheduling without human coordination
- Pattern: Telegram as the human-agent interface + Hermes as the background runtime + specialized clipping skill = fully autonomous content pipeline accessible from mobile

(see [autonomous-agents.md](autonomous-agents.md#discord-multi-channel-pipeline) for related multi-channel orchestration; NousResearch/hermes-agent in github-repos.md)

*Source: 2026-04-06-VadimStrizheus-this-19yo-built-an-entire-clipping-agent-army-from-his-phone.md*

### Planner Agent Before Builder: Anthropic's Internal Method

- Root cause of Claude's mediocre 70% outputs: Claude silently fills in decisions you didn't specify (audience, emotional arc, key objection) and defaults to the middle ground
- Anthropic's internal method: run a planner agent before any build; the planner expands a one-sentence prompt into a full scope/dependency/audience spec; the builder executes from the spec
- Demonstrated: "Create a 2D retro game maker" (one sentence) → planner produced a 16-feature spec → polished playable app; without planner = broken, unplayable
- Adaptation for non-code outputs: the-interviewer skill -- expands prompt into most ambitious outline, identifies gaps and asks with recommended answers, assembles a creative brief and executes
- 2 minutes of upfront interviewing eliminates the full back-and-forth editing cycle

*Source: Twitter-Bookmarks/2026-03-27-itsolelehmann-httpstcowemnpj6xem.md*

### Superpowers: 7-Phase Structured Agentic Pipeline

- Framework (obra/superpowers) enforces structured workflow over raw prompting; 125K+ stars; works with Claude Code, Cursor, Codex, Gemini CLI
- **Phase 1 — Brainstorm:** 9-step workflow before any code: explore project context → ask clarifying questions one at a time → propose 2-3 approaches with trade-offs → present design in sections with approval after each → write design doc → self-review for gaps/contradictions/ambiguity → wait for explicit approval; one exit: moving to planning; zero implementation until design approved
- **Phase 2 — Plan:** structured plan with dependencies, acceptance criteria, exact file paths, and order of operations; iron rule: no placeholders allowed ("TBD", "TODO", "implement later", "similar to task above"); every task must have complete copy-pasteable instructions; assumption is that executor has zero familiarity with your codebase
- **Phase 3 — Subagent-driven development:** dispatches independent tasks to parallel subagents, each with fresh context; main Claude session never writes code itself, only orchestrates: dispatch → review → track progress
- **Phase 4 — TDD:** iron law: no production code without a failing test first; if code gets written before its test, it gets deleted; write failing test → write simplest code that passes → refactor
- **Phase 5 — Two-stage code review:** two separate reviewer agents; first checks spec compliance; second checks code quality; both must pass; run separately to prevent first review biasing second
- **Phase 6 — Systematic debugging:** reproduce → isolate → form one hypothesis (not three) → smallest possible change → verify; 3-strike rule: if 3 fixes fail, stop patching symptoms and question the architecture
- **Phase 7 — Branch completion:** merge, PR, cleanup
- Trade-off: skills consume context window; on large tasks with lots of existing code, brainstorming prompts can eat into implementation context; shines on multi-file features, not single-file fixes

*Source: Twitter-Bookmarks/2026-03-30-shannholmberg-httpstcopbvno37xvs.md*

### Conductor Pattern -- Orchestrator Stays on develop, Worktrees Execute

The on-the-loop pattern for parallel agent work where one main editor window orchestrates and N worktree windows execute.

**The structure:**
- **Main editor window stays on `develop`.** Never implements. Plans + coordinates.
- **Each execution window opens in its own git worktree** -- separate working copies sharing git history but with own files on disk + own branch
- Main creates worktrees, writes worklogs, delegates
- Each execution window follows its assigned worklog: TDD plan + verification plan + invariants + checklist
- Each commits, pushes, opens its own PR (independent, not stacked)

**The orchestrator agent upgrade -- ask it instead of deciding yourself:**
"Look at the work remaining and the worktrees already running. What should the next agent pick up?" Agent considers file overlap + module boundaries + dependency chains. **It might tell you everything remaining is serial. That's fine.**

**Verification gate per worklog (TDD discipline):**
- Write the test → watch it fail → write the implementation → watch it pass → commit at each transition
- Without closing this loop, the AI pushes slop
- Worklog structure separates "parallel execution" from "parallel chaos"

**Worklog survives compaction.** When long-running agent hits context limits and conversation gets compressed, worklog on disk is intact. Agent re-reads it and restores full context. **This is what makes parallel agents viable for complex PRs, not just trivial ones.**

**Code review at AI scale -- decompose into mechanical + judgment layers:**
- AI handles mechanical layer: missing imports, type inconsistencies, test coverage gaps. Different models have different blind spots; using a second model for review catches what the first missed.
- Humans handle slow-judgment layer: architecture, product decisions
- **Stacked PRs:** AI generates 10x code; humans read at the same speed. Massive PRs that nobody reads carefully = how bugs ship. "LGTM" on a 50-file diff means "I trust you" not "I verified." **The only thing that scales with AI output is smaller PRs, not faster reviews.**

**Tools:** Greptile for confidence scoring (a 2/5 score has consistently flagged real problems); CodeRabbit for deep static analysis + auto-generated sequence diagrams. Specific tools matter less than the pattern.

**Workflow:** agent writes → push to branch → open PR → AI reviewer scores + flags mechanical issues → CI passes → human reviews with mechanical analysis already done.

*Source: Andrew-Vibe-Coding/Vibe Engineering From Random Code to Deterministic Systems (Part 9).md*

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

### Cross-Invocation PR Feedback Clustering

- Volume gate alone misses recurring patterns: reviewer posts 1-2 feedback items per round across 3 rounds -- each is below threshold, but the pattern is a single concern class
- Detection: check the skill's own prior reply comments on PR threads as evidence of previous resolution rounds -- GitHub is the source of truth, no persistent state files required
- Three resolver modes on cross-invocation clusters: (1) band-aid fixes -- prior fixes addressed symptoms, redo holistically; (2) correct but incomplete -- keep prior fixes, investigate sibling code proactively; (3) sound and independent -- use prior context for awareness only
- "Correct but incomplete" is the highest-value mode: "three rounds of the same concern in different files means more files with the same issue exist"
- Two-tier cost control: lightweight overlap check first, promote to full clustering only when overlap is confirmed
*Source: compound-engineering-plugin/docs/brainstorms/2026-04-01-cross-invocation-cluster-analysis-requirements.md*

### Address-Feedback: Structured PR Review Resolution

- Five-step PR review response workflow: gather comments (including full thread for context) → triage → fix → present summary to user → reply and resolve threads
- Key nuance: read full thread before acting -- a maintainer may have already explained why a suggestion should NOT be applied; acting on an already-resolved discussion is a common agent mistake
- Automated reviewer comments (bots) receive equal weight to human comments -- evaluate each suggestion on its merits; automated reviewers can also be wrong
- User approval gate before replying and resolving threads -- changes are staged and reviewed before any GitHub mutations
*Source: pydantic-ai/.claude/skills/address-feedback/SKILL.md*

### Plannotator Pattern: Plan-First Architecture with UI Review

@AleiahLock used Claude Code (Opus 4.6) plus the Plannotator plugin to architect a Polymarket BTC trading engine before any code was written. The pattern is broadly applicable to any system where extensibility and simulation matter more than first-version speed.

- **Step 1: plan with Claude in Plannotator UI.** Plannotator presents the plan in a clean reviewable interface where the human gives feedback on the plan itself, not on generated code. Several rounds of back-and-forth converge on a final architecture before implementation.
- **Step 2: ask Claude for an initial skeleton matching the agreed plan.** This includes the simulation harness alongside the production code -- not as an afterthought.
- **Step 3: build logging + visualization in the same pass.** AleiahLock added a chart-visualization tool that takes existing log files and generates interactive charts per execution window. Visual debugging is materially faster than raw-log analysis when the system is event-driven.
- **Why this matters for trading/financial agents specifically:** without a simulation environment that mirrors real-world latency, partial fills, and settlement delays, you cannot iterate on strategies without losing money. Build the simulation FIRST, validate strategies in simulation, then deploy.
- **Generalization:** any system that depends on subtle external behavior (order books, market data, real-world APIs) benefits from the "plan + simulate + visualize first" sequence. The plan is the spec; the simulation is the test harness; the visualization is the debugger.
- (see [bitcoin-ai.md > Polymarket Trading Engine Architecture](bitcoin-ai.md#polymarket-trading-engine-architecture-claude-planned) for the specific implementation)

*Source: 2026-04-10-AleiahLock-httpstcog02hnkzapt.md*

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

### Claude Code as Executive Assistant: Markdown-Based Organizational OS

- Open a fresh directory and prompt Claude to self-organize a markdown-based system for your role; Claude figures out folder structure without explicit design
- Maintain at least one Claude Code session open at all times; run multiple concurrent sessions for parallel workstreams (meeting prep, candidate research, writing simultaneously)
- MCP/tool integrations (calendar, Slack, Linear) are essential -- "post to Slack" without context switching is the real multiplier, not just Q&A
- Meeting transcripts pasted to Claude auto-produce notes, action items, and context file updates with no explicit instruction on where things go
- Decision logging: "log decision about X" creates structured records with alternatives considered -- weeks later you have full rationale, not just the outcome
- System compounds over time: 11,579 lines of institutional knowledge captured in 3 weeks including 82 meeting notes, 18 1:1s, 23 team members with 264 lines of context each

(see [memory-persistence.md](memory-persistence.md) for the memory layer patterns behind this)

*Source: Twitter-Bookmarks/2026-01-21-obie-httpstcokqfccopmdv.md*

### Skill Systems: From Standalone Skills to Autonomous Pipelines

- A skill is a unit (does one thing); a plugin/skill system is an architecture (multiple skills sharing context, passing output between each other, producing compound results)
- Three connective patterns: (1) shared context files (brand-voice.md loaded by every skill), (2) output-as-input chaining (Skill A writes to file; Skill B reads it), (3) scheduled orchestration (skills run on cron schedules)
- Build skills individually and test each connection manually before adding scheduling; design the whole system upfront leads to rebuilds
- Log every handoff: each skill writes to a run log (what it read, what it produced, any issues) -- without logs you debug blind across a multi-step pipeline
- Skills that naturally chain: scanner (trending topics) → creator (daily drafts) → reviewer -- each reads the previous skill's output directory

(see [skills.md](skills.md) for individual skill design patterns)

*Source: Twitter-Bookmarks/2026-03-09-NickSpisak-httpstcowp3gidzlka.md*

### Emerging Plugin Patterns

Novel workflow patterns from the Claude Code plugin ecosystem:

- **`/conductor` pattern:** A structured loop of context -> spec -> plan -> implement with persistent context across steps. Stateful, gate-driven workflow similar to RPI (see [Pattern 4: RPI Workflow](#pattern-4-rpi-workflow-research---plan---implement)) but plugin-based
- **Semantic reversion:** Plugin-assisted ability to revert not just code changes but semantic intent, understanding what a change was trying to achieve and undoing it at the concept level rather than the diff level
- **Agent Teams presets:** Community plugins providing preset team configurations like `/team-review` (parallel code review team) and `/team-debug` (debugging team) that configure agent roles, models, and communication patterns automatically

*Source: deep-research-report.md*

### Paperclip + Skills: Agentic Marketing Automation in Practice

- Practical workflow: install Postiz skill (social media posting), agent-media (UGC picture generation), Larry skill (TikTok slideshows), Virlo (trend discovery), GStack (human-sounding prose); chain them to automate TikTok content creation, scheduling, and feedback loops
- Skills as capability modules: "it's like the way Neo learned Kung Fu in the Matrix -- a simple Markdown file that you give to the agent and they know how to do some stuff"
- Retention automation via GitHub commits: hook GitHub skill -> read commits -> generate changelog posts -> distribute to Discord/Telegram/Slack/newsletter via Postiz; schedule as draft so you can review before posting
- Every video/piece of content should have an issue tracking it; if not, AI will have memory problems and won't know what constitutes a good video
- Key insight: agents + specialized skills + a cross-agent orchestrator (Paperclip, OpenClaw) = agentic business process automation available to solo founders

*Source: Twitter-Bookmarks/2026-04-01-wickedguro-httpstcorkuac6qdtu.md*

### Production Case Study: $70K/mo B2C Growth with OpenClaw

- 11 apps / $73K/mo; OpenClaw agent automates 5 workflows for Prayer Lock app
- Faceless content pipeline: 4 TikTok/IG accounts via "Larry" skill, replacing $30K/mo agency
- Influencer outreach: 1000 emails + 100 DMs/day, replacing $400/mo VA at 10x volume
- Automated support with Telegram escalation; daily KPI reporting; X/YouTube content automation
- Key: "Before you give OpenClaw a system to automate, you must first have the system built out for yourself"

*Source: How our OpenClaw agent Eddie helps us make $70kmo.md*

### RedditVideoMakerBot: One-Script Faceless YouTube Pipeline

- One Python script + one Reddit link = finished YouTube video, ready to upload
- Pipeline: finds Reddit thread -> screenshots post and top comments -> narrates with AI voice -> overlays on Minecraft/GTA gameplay background -> renders MP4
- Powers channels with 500K-2M subscribers making $10K/month in ad revenue; operators never record a single second of footage
- 7.7K GitHub stars, free, open source (elebumm/RedditVideoMakerBot)
- Typical content: AITA threads, "what job pays insanely well" threads -- high-engagement Reddit formats that translate directly to YouTube watch time
- Pattern: the entire creator economy middle layer (recording, editing, voiceover, thumbnails) collapses to a single script execution; the remaining skill is topic selection and upload cadence

*Source: Twitter-Bookmarks/2026-04-05-socialwithaayan-breaking-someone-just-open-sourced-the-exact-tool-powering-t.md*

### Instagram Growth Playbook with AI Automation

@erichustls step-by-step faceless Instagram page growth strategy:

- Stack: Namelix (naming), Nano Banana (logo), ChatGPT (bio/content), ViralFindr (viral content discovery), Canva AI (post creation), Later.com (scheduling)
- Progression: 10K followers in 60 days -> brand deals -> digital products -> $20K/month -> scale to 6-8 pages -> hire team -> $50K+/month
- Minimal AI content -- primarily a social media growth playbook that uses AI for content creation acceleration
- 30 minutes/day claim for maintenance once automated

*Source: Twitter-Bookmarks/How to use AI to become a millionaire in 2026 (step-by-step).md*

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

*Source: Twitter-Bookmarks/Thread by @simplifyinAI 1.md*

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

### Bookmark-to-Knowledge-Graph Pipeline Built with Claude Code

- Five-stage autonomous pipeline: (1) thread expansion (fetch full tweet threads, not just tweet 1), (2) article extraction (fetch linked URLs via Defuddle → clean markdown inside the note, not behind a dead link), (3) keyword tagging, (4) wikilink enrichment (150 known entities auto-linked, creating graph connectivity in Obsidian), (5) hub page generation (per-author, per-entity, per-tag)
- Built entirely via natural language description to Claude Code: "scaffolded project, wrote all 6 modules, debugged parser crashes, ran autonomously across 3,330 bookmarks" -- no manual coding
- The wikilink layer is the value: tags and frontmatter don't create graph edges; `[[Author]]` `[[Entity]]` `[[Tag]]` wikilinks in the footer do
- Pattern generalizes to any URL type (GitHub repos, research papers, newsletters); the pipeline is the template
- Stack: TypeScript, Bun, SQLite, Defuddle; runs locally, no cloud APIs beyond Claude Max

*Source: Twitter-Bookmarks/2026-03-24-Dogwiz-httpstcomzjnnikuvt.md*

### Scrapling + OpenClaw: Production Scraping with Cloudflare Bypass

Dedicated @simplifyinAI thread with concrete Scrapling performance data and community validation:

- **Performance:** 774x faster than BeautifulSoup. Zero bot detection. Bypasses ALL Cloudflare protections natively. 100% open source (GitHub: D4Vinci/Scrapling)
- **Key Value (community consensus):** "The actually useful part is selectors that survive site updates without you babysitting them" -- selector drift + Cloudflare blocks are where most automations die in production
- **Confirmed Running:** User reports running Scrapling on Picoclaw for a week
- **Community Pushback:**
  - "Not exclusive to OpenClaw -- any AI agent can use GitHub tools via CLI"
  - "Most unblockable scrapers get patched within weeks" -- Cloudflare may adapt
  - "Scraping websites is a fragile workaround, not a scalable solution"
- **Production Takeaway:** Cloudflare Turnstile specifically is the real test, not raw speed. Reliability against Turnstile determines workflow viability

*Source: Twitter-Bookmarks/Thread by @simplifyinAI 1 1.md*

### Claude Code Scraping: API Endpoint Reverse-Engineering as Key Nudge

@aniketapanjwani on 9 ways to scrape data with Claude Code (partial -- 2 of 9 shown):

- **Way 1 (Direct):** Just ask Claude Code to scrape a site; it writes a Python script, runs it, may write unit tests, outputs to CSV/SQLite
- **Way 2 (Endpoint Nudge):** Many sites load data via API calls. Sometimes Claude reverse-engineers the endpoint itself, but explicitly saying "look for an API endpoint" as a nudge dramatically improves results
- Remaining 7 methods require X premium article access

*Source: Twitter-Bookmarks/2026-03-04-aniketapanjwani-nine-ways-scrape-data-claude-code.md*

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

### YouTube Video Script Forensic Analysis (@alex_prompter)

Extract a viral video's entire playbook. Workflow: find viral video, extract transcript with ytscribe.ai, then run the 11-section analysis prompt:

1. **Hook Architecture** -- primary hook type (curiosity gap, pattern interrupt, bold claim), secondary hooks with timestamps, fill-in-blank templates
2. **Structural Blueprint** -- macro-structure (Problem-Agitate-Solve, etc.), beat map, pacing, time allocation
3. **Retention Mechanics** -- open loops, pattern interrupts, curiosity gaps, payoff points
4. **Emotional Engineering** -- emotional arc, trigger words, identity hooks, us-vs-them dynamics
5. **Storytelling Elements** -- narrative framework, character positioning, specificity anchors
6. **Linguistic Patterns** -- power phrases, sentence rhythm, repetition, conversational triggers
7. **Algorithm Signals** -- watch time optimizers, engagement bait, share/save triggers
8. **CTA Architecture** -- primary/soft CTAs, timing, value exchange
9. **Viral Coefficient** -- shareability score (1-10), controversy calibration, niche crossover
10. **Reusable Template** -- complete fill-in-blank script with opening variations and transition library
11. **Implementation Playbook** -- top 10 steal-this elements, adaptation guide, A/B test suggestions

*Source: Threads/alex_prompter - YouTube Video Script Hack.md*

### Voice Cloning via Prompt Engineering (@alex_prompter)

Three-step process to clone any writing voice using Claude Sonnet 4.5 (94% pass rate in blind tests):

1. **Extract Voice DNA:** Feed 2-3 writing samples and extract sentence structure patterns, vocabulary preferences, rhetorical devices, tone/formality level, unique quirks
2. **Create Voice Profile:** Build a reusable prompt with the DNA analysis + audience, content type, key message. Critical instruction: "Don't caricature" -- without this, AI exaggerates quirks
3. **Iterative Refinement:** Compare output to originals side-by-side, feed corrections ("Too formal. [Author] uses more contractions"), refine 2-3 times, save final prompt

Use cases: brand voice consistency, ghostwriting, studying great writers by reverse-engineering patterns (see [skills.md](skills.md) for the related "Write like a human" skill pattern).

*Source: Twitter-Bookmarks/Thread by @alex_prompter 1.md*

### Content OS: Bookmarkable Posts via Run-Folder Per Content Object (Shann Holmberg)
- **The system in one diagram:** every piece of content is an object that carries its own state from idea to published. Each post = one `runs/active/YYYY-MM-DD-{slug}/` folder containing `content-object.md` (id, status, format, pillar) + `brief.md` (writer context packet). When it ships, it gets archived with feedback.
- **Two context layers:** signal layer (external — bookmarks saved this week, content from watch-list creators, articles you liked) and knowledge graph (internal — your personal OS, notes, journals, voice memos, archive of shipped content). The route decides which feeds the brief.
- **Four content routes, each with its own brief and gates:** ORIGINAL (drawn from you/second brain, no external source), REPURPOSE (extend owned content — thread spun from article, self-QRT, tweet extracted from piece), REWRITE (external source translated through your POV/voice with explicit "what to keep / what to credit / which voice rules apply"), RESEARCH + IDEATE (explore topic before any drafting, output is sharpened idea/angle list, not a post).
- **The bookmarkability rubric** (0/1/2 points each, threshold 8/12): saves the reader a future task; includes proof (numbers, screenshot, named example); gives reusable takeaway (template, checklist, frame); has specific audience and job-to-be-done; can be applied without you being in the room; has strong visual.
- **Bookmarkable post shapes (the filter):** before shipping ask "does this draft resemble one of these — checklist, blueprint, folder structure, template, framework, step-by-step workflow, proof screenshot with takeaway, before/after, reusable mental model?" If no, usually shouldn't be published.
- **Master avoid-slop document:** 54 patterns broken into severity tiers, with concrete rewrites for each. Loaded by writer agent before drafting AND by verifier agent before approval. Difference between "AI wrote this" and "a person who happens to use AI wrote this."
- **Writer/orchestrator role split:** writer (Opus 4.7) handles taste/rhythm/compression/voice/actual draft. Orchestrator (GPT-5.5) handles routing between layers, packaging context, deciding what gets passed, running verifier, handoff to publish layer. Different models for different jobs.
- **Earlier 4-agent system → leaner version lesson:** "the agent count was not the lever. the knowledge layer feeding the writer was." Fewer agents, more workflows, same loop, sharper output.
- (see [4-Agent Content Production Team](agent-design.md#4-agent-content-production-team-researchproductionqualitydistribution) for a complementary but more agent-heavy approach to the same content production problem; see [Fat Skills + Thin Harness](skills.md#fat-skills--thin-harness--skillify-meta-skill-garry-tan) for the "knowledge layer beats agent count" insight)

*Source: 2026-05-08-shannholmberg-httpstcowarqpgs5ft.md*

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

*Source: Twitter-Bookmarks/2026-03-08-shannholmberg-claude-workflow-audit-prompt.md*

### 10 Repeatable Claude Workflows That Save Time

- A "workflow" means a repeatable prompt + fixed input/output structure -- not a one-off prompt; the value is consistency, not speed
- Critical prompt pattern for research: always add "If data is insufficient, say so." Without this, Claude confidently invents numbers
- Code review prompt: add "be harsh." Without it, Claude defaults to polite, low-signal feedback ("well-structured, perhaps consider...")
- Email prompt: include "does not sound like ChatGPT" -- removes the AI-generated opener pattern
- Batch content repurposing: one article → 1 TG post + 3 tweets + 2 quote-tweet captions + thread hook in one prompt
- Weekly review as highest-ROI workflow: dump the week's notes/bookmarks into Claude on Sunday; it surfaces connections you missed because you're too close to your own work

*Source: Twitter-Bookmarks/2026-03-26-zodchiii-httpstcovddldgl4nk.md*

### Claude Code Team Workflow Tips (Boris Cherny)

Tips from the Claude Code creator and team:

- **Voice dictation for prompts:** You speak 3x faster than you type, and prompts get way more detailed as a result. On macOS, hit fn twice to activate.
- **"Use subagents" as a prompt suffix:** Append "use subagents" to any request where you want Claude to throw more compute at the problem. Offload individual tasks to subagents to keep the main context window clean.
- **Two-Claude plan-review pattern:** One Claude writes the plan, then a second Claude reviews it as a staff engineer. Catches issues the planner misses.
- **Slack MCP for bug fixing:** Enable the Slack MCP, paste a bug thread, say "fix." Zero context switching. Also works: "Go fix the failing CI tests" without specifying how.
- **BigQuery/database analytics via CLI:** Build a database skill checked into the codebase. The team uses it for analytics queries directly in Claude Code via the `bq` CLI. Works for any database with a CLI, MCP, or API.
- **Spaced-repetition learning skill:** You explain your understanding, Claude asks follow-ups to fill gaps, stores the result. Builds a personal knowledge base over time.
- **Hooks for permission routing:** Route permission requests to Opus 4.5 via a hook -- it scans for attacks and auto-approves the safe ones (see [tools-and-integrations.md](tools-and-integrations.md)).
- **Plan mode for verification, not just building:** Use plan mode explicitly for verification steps. When something goes sideways, switch back to plan mode and re-plan immediately -- don't keep pushing.
- **Explanatory output style for learning:** Enable "Explanatory" or "Learning" output style in `/config` to have Claude explain the *why* behind its changes.

*Source: Twitter-Bookmarks/Thread by @bcherny.md*

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
| Autonomous lead gen / outbound pipeline | Full Lead Gen Pipeline or "Money Printer" |
| Faceless content production | RedditVideoMakerBot / Hermes Clipping Agent |
| Agentic marketing automation | Paperclip + Skills / Instagram Growth Playbook |

