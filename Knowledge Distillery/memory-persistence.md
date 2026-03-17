# Memory & Persistence

## The Memory Problem: Every Session Starts at Zero

AI agents have no memory between sessions by default. When a context window closes, everything learned -- architecture discovered, bugs diagnosed, decisions made -- vanishes. Your job is to build the external memory system that makes each session smarter than the last. Without deliberate memory infrastructure, you repeat yourself endlessly and the agent never compounds knowledge.

The solution is not one mechanism but four complementary layers, each with different scope, persistence, and automation characteristics.

### Three Named Memory Failure Modes

Understanding how memory fails is prerequisite to fixing it. There are three distinct failure modes, each requiring a different mitigation:

- **Memory Never Saved:** The LLM decides in real-time whether information is worth storing -- it is a judgment call, not a guarantee. Important context slips through constantly because the model deemed it not worth writing to disk. Like an employee who decides on their own which meeting notes to keep.
- **Saved But Never Retrieved:** Even when facts make it to disk, the agent has to decide to call `memory_search`. In practice, it frequently answers from its current context window instead of searching stored memory. From the user's perspective it "forgot," but it never looked.
- **Compaction Destroys Knowledge:** When the context window fills, older messages get summarized or removed. Any information that only existed in conversation (not yet persisted to disk) is destroyed. Even MEMORY.md content loaded at session start can get summarized away during a long session. (see [failure-patterns.md#compaction-amnesia-context-window-eats-un-persisted-knowledge](failure-patterns.md#compaction-amnesia-context-window-eats-un-persisted-knowledge))

The core insight: agents treat memory as a suggestion, not a requirement. You must configure them to be reliable.

*Source: Give your Openclaw the Memory it Needs (Full Guide).md*

## The Four-Layer Memory Model

| Layer | Mechanism | Scope | Persistence | Automation | Best For |
|-------|-----------|-------|-------------|------------|----------|
| 1 | `CLAUDE.md` | Project / user / global | Permanent (git-tracked) | Manual + `#` shortcut | Architecture, commands, conventions, warnings |
| 2 | `WORKLOG.md` | Feature / task | Multi-session | Human-steered, AI-written | Context restoration, scope control, decision audit |
| 3 | claude-mem plugin | Project-wide | Automatic (SQLite) | Fully automatic via hooks | Cross-session recall, search over history |
| 4 | SDK session persistence | Agent orchestration | Session-resumable | Programmatic | Meta-agent state, forking explorations |

---

### Layer 1: CLAUDE.md (Always-Loaded, Project-Wide)

CLAUDE.md is loaded into the system prompt on every conversation. It is the single most impactful memory mechanism because it requires zero recall effort -- the agent reads it automatically.

**What it remembers:**
- Project architecture and key directories
- Build/test/deploy commands
- Code style rules and conventions
- Warnings about footguns or sensitive areas
- Tool configuration (MCP servers, custom CLI utilities)
- Standard workflows (plan-before-code, TDD, commit conventions)

**The `#` shortcut:** Press `#` mid-session in Claude Code to add a memory. This appends to your CLAUDE.md without breaking flow -- use it every time you catch yourself repeating an instruction. (see [context-engineering.md#claudemd-your-always-loaded-memory](context-engineering.md#claudemd-your-always-loaded-memory))

**Three scopes:**

| File Location | Scope | Typical Content |
|---|---|---|
| `~/.claude/CLAUDE.md` | All projects (global) | Personal style, universal rules |
| `./CLAUDE.md` (repo root) | This project (shared) | Architecture, commands, team conventions |
| `./.claude/CLAUDE.md` | This project (local) | Personal scratch, local overrides |

**Limitation:** Because it loads every session, keep it concise. If your CLAUDE.md exceeds ~200 lines, break content into separate markdown files and reference them. Prefer summary docs over raw code dumps (see the "Documentation Spine" pattern in the Sample CLAUDE.md).

**Self-modification rule:** CLAUDE.md should evolve. When a mistake reveals a missing rule, update the file immediately. Require the agent to state what changed and why.

---

### Layer 2: Worklogs (Feature-Scoped, Session-to-Session)

A worklog is a living document that combines plan, decisions, session log, and surprises. Unlike a plan (a prediction), a worklog is a record that starts with one and evolves during execution.

**Key insight:** The AI writes the worklog. You steer it. Say something like: *"Create a worklog for adding rate limiting to user registration. Load the `/api-patterns` and `/rate-limiting` skills."* Then review and adjust.

**What worklogs solve:**
- **Context restoration** -- new session reads the worklog and resumes without re-explanation
- **Auditability** -- what decisions were made and why
- **Scope control** -- explicit milestones prevent gold-plating

#### WORKLOG.md Format Template

```markdown
# Feature: [Feature Name]

## Skills Loaded
- `/skill-name` -- why it matters for this feature

## Milestones
- [ ] M1: [First deliverable]
- [ ] M2: [Second deliverable]

## Invariants (high-stakes features only)
- **INV-1:** [Verifiable constraint, e.g., "A single IP cannot request >10 magic links per hour"]

## Closing the Loop
- [ ] Run `npm test` -- all new tests pass
- [ ] [End-to-end verification step, e.g., Playwright, curl, manual check]
- [ ] Edge case: [specific scenario]

## Session Log
### Session 1 (YYYY-MM-DD)
- Completed M1
- **Next:** [What to do next]

## Surprises
- [What you learned that was unexpected -- update the relevant skill immediately]
```

**Naming convention:** `WORKLOG_feature-name_YYYY-MM-DD.md` for multi-feature work.

#### The Worklog Smell Test

Before starting, calibrate. Most features need 50-100 lines, not 787.

- Worklog longer than 100 lines for a simple task --> cut sections, not detail
- More than 5 commits planned --> merge related changes
- Invariants for a UI-only change --> delete that section
- You are proud of how thorough it looks --> you have over-engineered it

The same AI that writes thorough worklogs will happily write too-thorough worklogs. Tell it when to stop. (see [failure-patterns.md#1-vision-compression](failure-patterns.md#1-vision-compression))

#### Automating Context Restoration

Use a session-start hook to detect worklogs automatically:

```bash
# .claude/hooks/session-start-worklog-check.sh
if [ -f "WORKLOG.md" ]; then
  echo "WORKLOG.md detected. Read it to restore context."
fi
```

```json
{
  "hooks": {
    "SessionStart": [{
      "type": "command",
      "command": "bash .claude/hooks/session-start-worklog-check.sh"
    }]
  }
}
```

Now "continue" is all you need to say. The agent reads the worklog and picks up where the last session left off.

#### Archiving Strategy

When a feature ships, do not delete the worklog or rely on git history alone.

| Approach | Pros | Cons |
|---|---|---|
| `docs/worklogs/` (git-tracked) | Teammates learn; agent finds context | Repo noise over time |
| `.worklogs/` (gitignored) | Clean repo; agent still reads locally | Lost on machine switch |

**The real preservation question:** If you update skills when surprises happen, the important knowledge compresses into skills -- which persist permanently. The worklog was scaffolding; the skill is the building. (see [skills.md](skills.md))

---

### Four-File Memory Split (Extending Worklogs to Daily Operation)

The default single-MEMORY.md approach degrades as the file grows -- the agent struggles to parse a monolithic memory file over time. This pattern extends the Layer 2 worklog concept beyond feature-scoped work into general agent operation.

Split memory into four files by lifecycle stage:

| File | Purpose | When Read |
|---|---|---|
| **MEMORY.md** | Long-term context | Every session start |
| **memory/YYYY-MM-DD.md** | Daily notes | Written immediately, read when relevant |
| **memory/active-tasks.md** | In-progress work | Checked on startup |
| **memory/lessons.md** | Mistakes worth remembering | Session start, periodic review |

**Session start protocol:** (1) read MEMORY.md, (2) check active-tasks.md for interrupted work, (3) read today's daily notes if they exist.

**During-session rule:** Write to daily notes immediately when completing something, learning a preference, making a decision, or encountering something important.

*Source: Give Your OpenClaw Agent Memory that Actually Works.md*

---

### Layer 3: claude-mem Plugin (Automatic, Cross-Session)

claude-mem is a third-party Claude Code plugin that captures tool usage observations automatically via lifecycle hooks, compresses them with AI, and injects relevant context into future sessions.

**How it works:**
1. **5 lifecycle hooks** (SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd) observe everything Claude does
2. **Worker service** on port 37777 stores observations in SQLite with FTS5 full-text search
3. **Chroma vector database** enables hybrid semantic + keyword search
4. **Session start injection** primes the new session with compressed context from prior sessions

#### 3-Layer Retrieval Workflow (Token-Efficient)

```
1. search(query="auth bug", type="bugfix", limit=10)   --> compact index (~50-100 tokens/result)
2. timeline(around=observation_id)                       --> chronological context
3. get_observations(ids=[123, 456])                      --> full details (~500-1000 tokens/result)
```

This progressive disclosure pattern yields roughly 10x token savings compared to dumping full history upfront.

#### Hybrid Search and Session Indexing

claude-mem supports two built-in search enhancements that significantly improve retrieval quality:

- **Hybrid search** combines vector similarity (conceptual matching, weight 0.7) with BM25 keyword search (exact token matching, weight 0.3) -- leaving BM25 off means missing exact matches on error codes, project names, and technical terms
- **Session transcript indexing** (`experimental.sessionMemory: true`) chunks and indexes past conversations alongside memory files, making queries like "What did we decide about X last Tuesday?" answerable
- Both are built-in config options, not external tools -- enable them in `memorySearch` settings

*Source: Give your Openclaw the Memory it Needs (Full Guide).md*

#### Memory Flush and Pre-Compaction Persistence

The single most impactful configuration change for memory reliability is the **memory flush**: a silent turn triggered before compaction that prompts the agent to write durable memories to disk.

- Customize the flush prompt to specify exactly what to capture: decisions, state changes, lessons, blockers
- Raise `softThresholdTokens` to ~40,000 to trigger flushes earlier, before valuable context gets compacted
- **Context pruning with TTL mode** (`cache-ttl` with 6h window, `keepLastAssistants: 3`) eliminates the problem of having to repeat recent messages after a context flush
- These are config-level fixes that require no external tools -- most "my agent forgets everything" complaints come from running default config without these optimizations

*Source: Give your Openclaw the Memory it Needs (Full Guide).md*

#### Memory Persistence via Hooks and Continuous Learning

A pattern using Claude Code hooks to create continuous memory without manual intervention:

- **Three hook types for memory:** PreCompact (save state before context compaction), SessionStart (load prior context from .tmp files), Stop (persist learnings at session end)
- **Continuous learning pattern:** Stop hook analyzes completed sessions for non-trivial patterns (debugging techniques, workarounds, architectural insights) and auto-saves them as reusable skills -- not just memory entries but executable knowledge
- **Session memory via .tmp files:** Store summaries in `.claude/.tmp/` -- what worked, what failed, what's untried. Next session loads these for continuity without bloating CLAUDE.md
- **Dynamic system prompt injection:** `--system-prompt` flag gives higher instruction authority than @file references or `.claude/rules/` -- useful for strict behavioral rules that must override other context

(see [tools-and-integrations.md](tools-and-integrations.md#hooks-prepost-tool-automation) for hook mechanics, [context-engineering.md](context-engineering.md) for context hierarchy)

*Source: Twitter Bookmarks/The Longform Guide to Everything Claude Code.md*

#### OpenClaw Memory Lifecycle: Defense-in-Depth Configuration

Production-grade memory configuration for OpenClaw agents, extending the flush/compaction patterns above with diagnostics and a layered defense model:

- **`/context list` as first-step diagnostic:** Run `/context list` in any OpenClaw session to see loaded workspace files, character counts, and truncation status. Check: Is MEMORY.md loading? Is anything TRUNCATED (per-file limit `bootstrapMaxChars` default 20,000 chars, aggregate `bootstrapTotalMaxChars` default 150,000 chars)? Do injected chars equal raw chars?
- **Three-layer defense model:** (1) Pre-compaction memory flush (automated safety net), (2) Manual memory discipline (relevance-based "save this to memory"), (3) File architecture (bootstrap files survive compaction because they reload from disk). No single layer is sufficient alone.
- **Compaction vs pruning -- explicitly differentiated:** Compaction rewrites conversation history (lossy, permanent, affects all message types, triggered by context window overflow). Pruning trims old tool results in-memory only (lossless, temporary, on-disk transcript untouched, only affects `toolResult` messages). Pruning is safe; compaction is the dangerous one.
- **Pre-compaction flush config:** `reserveTokensFloor: 40000` (headroom for flush + summary; default 20K is too tight -- a single large tool output can jump past threshold). `memoryFlush.enabled: true` triggers a silent agentic turn before compaction. The `NO_REPLY` token suppresses user-visible output.
- **Manual `/compact` timing trick:** (1) Save context to memory files, (2) Send `/compact`, (3) Give new instructions. New instructions land in post-compaction context with maximum lifespan. Can focus compaction with `/compact Focus on decisions and open questions`.
- **Sub-agent injection filtering:** Sub-agent sessions only inject AGENTS.md and TOOLS.md -- other bootstrap files (SOUL.md, USER.md, MEMORY.md) are filtered out. If sub-agents lack personality or preferences, this is why.
- **Memory hygiene cadence:** Daily: append to daily log (automated). Weekly: promote durable rules and decisions from daily logs into MEMORY.md. Keep MEMORY.md under 100 lines -- it's a cheat sheet, not a journal.
- **Defense-in-depth summary:** 9 layers -- workspace files (permanent identity), pre-compaction flush (automated safety net), manual saves (relevance-based), strategic `/compact` (controlled reset), session pruning (cache-ttl delays compaction), hybrid search (meaning + keyword), extra paths (index external docs), QMD (full knowledge base search), git backup (history + rollback).
- **7 troubleshooting patterns** with diagnostic prompts: preferences not remembered (check MEMORY.md loading), memory_search empty (check embedding model download), tool results forgotten (session pruning -- re-run tool or save to memory), overflow errors (compact proactively, raise reserveTokensFloor), flush didn't run (large token jump bypassed threshold), agent forgets tools (known compaction bug -- `/new` to reset), overnight amnesia (daily session reset is expected -- bootstrap + search carry over).

(see [Memory Flush and Pre-Compaction Persistence](#memory-flush-and-pre-compaction-persistence))

*Source: Twitter Bookmarks/OpenClaw Memory Masterclass The complete guide to agent memory that survives.md*

#### Endless Mode (Beta)

- Up to 95% fewer tokens per session
- Approximately 20x more tool calls before hitting context limits
- Enabled from the beta channel in the web viewer UI

#### Privacy Controls

- `<private>` tags exclude sensitive content from storage
- All data stored locally in SQLite -- no cloud sync
- Configurable context injection via `~/.claude-mem/settings.json`

#### Caveat

This is a third-party plugin. Watch for context bloat in large projects -- at least one practitioner reported degraded agent performance, likely from excessive context injection. If the agent seems confused, disable and compare. Keep injection lean.

---

### QMD: External Retrieval Backend

QMD (by Tobi Lutke / Shopify) is an opt-in replacement for the built-in SQLite indexer, running as a local sidecar combining BM25 + vectors + reranking for noticeably better retrieval quality.

**Killer feature:** Indexes external document collections (Obsidian vaults, project docs, Notion exports) making them searchable via `memory_search`.

**Usage:**
- `qmd query "search terms"` to search across all memory files
- `qmd get <file>:<line> -l N` to pull specific sections
- Save the QMD default preference in the agent's TOOLS.md file so it persists across sessions

**Installation timing matters:** Install QMD before loading the agent with conversations -- installing memory infrastructure midway causes resets and lost chat logs. (see [failure-patterns.md#empty-context-files-the-silent-degradation](failure-patterns.md#empty-context-files-the-silent-degradation))

*Sources: Give your Openclaw the Memory it Needs (Full Guide).md; Give Your OpenClaw Agent Memory that Actually Works.md*

#### qmd + Obsidian: Local Hybrid Search Stack

- **qmd** (github.com/tobi/qmd): CLI tool by Shopify CEO Tobi Lutke for searching local markdown files; 14.5k stars
- Three search modes running entirely on-device: BM25 full-text, vector semantic search (300MB local embedding model), and LLM re-ranking for final relevance
- Stack: Obsidian for note storage (all files are local .md, no lock-in) + qmd for retrieval + Claude Code as the query interface
- `qmd embed` indexes the entire collection once; Claude Code calls `qmd query "..."` during sessions to pull relevant context automatically
- **Compounding effect:** each new note increases future session quality without extra setup effort; eliminates manual context-pasting at session start
- No data leaves the machine -- full privacy, works offline

(see [memory-persistence.md#layer-3-claude-mem-plugin-automatic-cross-session](memory-persistence.md#layer-3-claude-mem-plugin-automatic-cross-session) for related cross-session memory patterns)

*Source: Twitter Bookmarks/2026-03-12-nurijanian-if-youre-a-pm-who-uses-claude-codecursor-to-build-and-execut.md (@nurijanian)*

---

### Mem0 and Cognee: External Memory Layers

Two external tools that complement rather than replace the built-in memory system:

- **Mem0** (YC-backed) stores memories outside the context window entirely, making them compaction-proof. Two processes per turn: auto-capture (stores without depending on LLM judgment) and auto-recall (injects relevant memories before the agent responds). Solves the "never saved" and "compaction destroys" failure modes completely. Installs as an OpenClaw plug-in.
- **Cognee** builds a knowledge graph from memory files, representing entities and relationships as nodes and edges (e.g., "Alice owns the auth module"). Useful for multi-agent teams or enterprise settings where relationship queries matter. Requires Docker; overkill for basic setups.

*Source: Give your Openclaw the Memory it Needs (Full Guide).md*

### Supermemory: Hybrid Memory Plugin for Claude Code

A Claude Code plugin (distinct from MCP) that gives Claude persistent cross-session memory via a hybrid architecture that goes beyond simple RAG:

**Architecture:**
- **User profiles** combine episodic content (what you worked on, how you fixed things) with static information (role, preferences, style)
- **Three memory dimensions:** Episodic (where you left off), Stylistic (coding preferences, patterns you favor), Personal (role, project context) -- each dimension is tracked and updated independently
- **Fact extraction** -- not just similarity retrieval; the system extracts discrete facts, tracks how they evolve over time, and keeps the profile current
- **Context injection at session start** -- user profile is automatically injected (not dependent on the model choosing to call a tool)
- **Automatic conversation capture** -- conversation turns are stored without relying on LLM judgment about what is worth saving
- **Compounding effect:** Learns how you fixed specific errors, which patterns you prefer, what debugging approaches worked -- each session makes future sessions more calibrated

**Why a plugin instead of MCP:** The MCP version cannot control when Claude Code chooses to run memory tools. The plugin adds two capabilities MCP cannot:
1. Guaranteed context injection on session start (no tool-call dependency)
2. Automatic capture of conversation turns (no LLM judgment dependency)

This directly addresses two of the three named memory failure modes (see [Memory Never Saved and Saved But Never Retrieved](#three-named-memory-failure-modes)) -- the plugin removes LLM judgment from both the save and retrieve paths.

**Benchmark:** LongMemEval score of 81.6% (most RAG systems score 40-60% on memory-specific tasks). The gap comes from understanding that "the auth bug" means the specific issue from three days ago, and that preferences evolve over time (used to like classes, now prefers functions).

**Key distinction from claude-mem:** claude-mem observes tool usage via lifecycle hooks and compresses observations. Supermemory builds a persistent user profile from conversation history and injects it proactively. Both are complementary -- claude-mem indexes what happened, supermemory remembers who you are.

### Claudie-Memory: Raw Chat Log Indexing

A community tool that indexes raw chat logs (JSONL) in SQLite with FTS search and injects them into new sessions. Distinct from claude-mem (which observes tool actions) -- Claudie-memory captures raw conversational context, enabling one agent to pick up exactly where another left off by key terms. Achieves real-time cross-session memory without costly vector embeddings.

Novel approach: FTS over raw chat transcripts rather than summarized/compressed observations. Where claude-mem compresses before storing, Claudie-memory stores verbatim and searches full-text -- trading storage for fidelity.

*Source: deep-research-report.md*

### lossless-claw: Compaction-Resistant Memory Plugin

- **lossless-claw** (github.com/martian-engineering/lossless-claw): OpenClaw memory plugin targeting the compaction forgetfulness problem
- Context compaction discards detail to fit within the window; lossless-claw preserves key memory across compaction events
- Positioned as an alternative to Claude Code's built-in memory feature when that feature is insufficient
- Complements qmd (retrieval) -- lossless-claw focuses on in-session continuity, qmd on cross-session retrieval

(see [memory-persistence.md#layer-2-worklogs-feature-scoped-session-to-session](memory-persistence.md#layer-2-worklogs-feature-scoped-session-to-session) for manual continuity approaches)

*Source: Twitter Bookmarks/2026-03-14-steipete-theres-a-lot-of-cool-stuff-being-built-around-openclaw-if-th.md (@steipete)*

---

### Auto Memory: Built-In Cross-Session Learning

- Built-in feature (rolled out Feb 2026) where Claude saves notes for itself across sessions without user intervention
- Storage: `~/.claude/projects/<project>/memory/MEMORY.md` + topic files; first 200 lines injected at session start; topic files read on demand
- Relationship to the Four-Layer Model: occupies a space between Layer 1 (CLAUDE.md, manual) and Layer 3 (claude-mem, automatic plugin) -- built-in and automatic but simpler than claude-mem's observation/compression/search pipeline
- Toggle: `/memory` command, `autoMemoryEnabled` setting, or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` env var
- Concern: creates vendor lock-in proportional to accumulated context; risk of "black box" memories from other projects interfering
- (see [context-engineering.md](context-engineering.md) for CLAUDE.md vs MEMORY.md distinction)
*Sources: Thread by @trq212.md, How Claude remembers your project.md*

---

### Layer 4: SDK Session Persistence (Meta-Agent Pattern)

The Claude Agent SDK provides programmatic session management for orchestration-level memory.

**Core mechanism:** `resume: sessionId` picks up exactly where the agent left off, restoring full conversation history.

```typescript
for await (const message of query({
  prompt: "continue",
  options: {
    resume: savedSessionId,   // restore previous session
    // forkSession: true,     // or fork to explore without polluting main
  }
})) { ... }
```

**Two-layer persistence in the meta-agent pattern:**
- **Layer A (automatic):** SDK session resume restores conversation state
- **Layer B (explicit):** State files (`workstreams.md`, `patterns.md`, `decisions.md`, `session-log.md`) are human-readable markdown that both agent and human can edit between sessions

**Fork sessions** to explore alternatives without polluting the main session. If the fork yields good results, merge the learning back into state files.

State files survive even if the SDK session is lost. They are the durable layer. (see [workflow-patterns.md](workflow-patterns.md))

---

### Layer 5: Agent Memory -- Per-Agent Persistent Knowledge (v2.1.33+)

A fifth memory mechanism distinct from CLAUDE.md, auto-memory, `/memory`, and the four-layer model. The `memory` frontmatter field gives each subagent its own persistent markdown-based knowledge store.

**How it works:**
- On startup, first 200 lines of the agent's `MEMORY.md` are injected into its system prompt
- `Read`, `Write`, `Edit` tools are auto-enabled so the agent can manage its own memory files
- If `MEMORY.md` exceeds 200 lines, the agent moves details into topic-specific files (e.g., `react-patterns.md`, `security-checklist.md`)

**Three scopes:**

| Scope | Storage Location | Version Controlled | Shared | Best For |
|-------|-----------------|-------------------|--------|----------|
| `user` | `~/.claude/agent-memory/<agent-name>/` | No | No | Cross-project knowledge (recommended default) |
| `project` | `.claude/agent-memory/<agent-name>/` | Yes | Yes | Project-specific knowledge the team should share |
| `local` | `.claude/agent-memory-local/<agent-name>/` | No | No | Project-specific knowledge that's personal |

These scopes mirror the settings hierarchy (`~/.claude/settings.json` > `.claude/settings.json` > `.claude/settings.local.json`).

**Comparison with other memory systems:**

| System | Who Writes | Who Reads | Scope |
|--------|-----------|-----------|-------|
| CLAUDE.md | You (manually) | Main Claude + all agents | Project |
| Auto-memory | Main Claude (auto) | Main Claude only | Per-project per-user |
| `/memory` command | You (via editor) | Main Claude only | Per-project per-user |
| Agent memory | The agent itself | That specific agent only | Configurable (user/project/local) |

These systems are complementary -- an agent reads both CLAUDE.md (project context) and its own memory (agent-specific knowledge).

**Tips:**
- Prompt memory usage explicitly: "Before starting, review your memory. After completing, update your memory with what you learned."
- Combine `skills` (static knowledge at startup) with `memory` (dynamic knowledge built over time) for maximum effectiveness (see [agent-design.md](agent-design.md))
- Choose scope intentionally: `user` for cross-project patterns, `project` for team-shared conventions, `local` for personal project notes

### RAG-Based Agent Memory with Vector Database

- PostgreSQL + pgvector as dedicated memory backend: label the memory, create a vector, store label + vector + raw text; search vector store on unknown queries
- Short-term/long-term flush pattern: agent writes to memory file during sessions; cron flushes into vector database; new sessions start minimal with search tool
- Benefits: better recall, lower token usage; trade-off: more moving parts, complex for non-developers
- Recommended production stack: agent framework + PostgreSQL/pgvector + n8n (for API proxies and security)
- Simpler alternative: filesystem-based .md memory reported as "almost 100% effective" for non-vector-search use cases
- (see [autonomous-agents.md](autonomous-agents.md) for agent-specific memory implementations)
*Source: Thread by @SimonHoiberg.md*

---

### Multi-Agent Memory Architecture

For teams of specialized agents, the four-layer model extends to a shared architecture with four layers of its own:

1. **Private memory per agent** -- each agent maintains its own MEMORY.md and daily notes
2. **Shared reference files** via symlinked `_shared/` directory (user profile, agent roster, team conventions)
3. **QMD with shared paths** so all agents search the same reference docs while maintaining private memory
4. **Coordination agent** ("Chief of Staff") that reads core files at session start and maintains consistency

Treat agent memory like a human team's documentation: some things shared (handbook, org chart, project docs), some things private (personal notes, work in progress).

**Obsidian integration at scale:** Symlink the memory folder so daily notes appear in Obsidian on all devices, or index the Obsidian vault via QMD so everything captured becomes searchable by all agents. Obsidian 1.12 CLI enables metadata/property queries instead of reading entire files, reducing token cost for memory lookups.

*Source: Give your Openclaw the Memory it Needs (Full Guide).md*

---

## Decision Traces: Strategic Memory

Decision traces record *why* you chose path A over path B. They are strategic memory -- slower to write, higher value over time.

### When to Write One

- Architectural choices (database selection, framework migration, API design)
- Production incidents and post-mortems
- Any decision that a future developer will question

### Format

```markdown
## Decision: [Title]
- **Context:** What prompted this decision
- **Alternatives Considered:** What else was on the table
- **Rationale:** Why this option won
- **Consequences:** What this commits us to and what it rules out
- **Linked Skill:** `/skill-name` if a skill was created or updated
```

### When a Skill Update Is Enough vs. a Full Trace

- **Tactical** (how to do X correctly) --> update the skill
- **Strategic** (why we chose X over Y) --> write a decision trace
- If you are not sure, write the trace. It takes 5 minutes and prevents a 2-hour re-debate later.

---

## The Memory Lifecycle

Knowledge flows through a predictable lifecycle. Understanding it prevents both under-documentation and over-documentation.

### Bug --> Lesson --> Skill --> Prevention

```
Bug discovered
  --> Log in Surprises section of worklog
    --> Extract lesson: what went wrong and the fix
      --> Encode as skill: pattern the agent follows next time
        --> Prevention: the bug category stops recurring
```

### Surprise --> Worklog Entry --> Decision Trace or Skill Update

```
Unexpected behavior observed
  --> Document in worklog Surprises section (immediate)
    --> Is it strategic (architectural, cross-cutting)?
        YES --> Write a decision trace
        NO  --> Update the relevant skill
```

The context is freshest right after you hit the issue. If you wait until "later," you lose the nuance.

---

## Self-Improvement Loop

After every correction, close the loop:

1. **Update `tasks/lessons.md`** with what went wrong and the specific fix
2. **Write a rule** that prevents recurrence -- prefer specific rules over vague advice
3. **Review lessons at session start** for the relevant project
4. **Iterate ruthlessly** until the mistake rate measurably drops

This pattern comes from treating CLAUDE.md as a living document. When a mistake reveals a missing rule:
- Update CLAUDE.md or the relevant skill immediately
- State what changed and why
- The correction becomes permanent prevention

### Periodic Memory Maintenance via Cron

Without maintenance, memory files accumulate outdated context that degrades retrieval quality and wastes tokens. Set up periodic cron jobs for three hygiene tasks:

1. **Review memory for misplaced items** -- entries that are actually tool configs belong in TOOLS.md, not MEMORY.md
2. **Extract key lessons** from daily notes and memory into lessons.md
3. **Remove outdated context** -- stale entries waste tokens and pollute retrieval

The principle: "Text beats brain. If you want to remember it, write it down" -- but written-down text also needs pruning. Memory systems that are not actively maintained decay rather than compound.

*Sources: Give Your OpenClaw Agent Memory that Actually Works.md; memory protocol.md*

The goal: every mistake makes the system smarter. A bug fixed without updating the memory system is a bug that will recur. (see [workflow-patterns.md#step-7-archive-and-compress](workflow-patterns.md#step-7-archive-and-compress))

### Single-Rule Compounding Memory for OpenClaw

- One rule produces compounding agent memory: "Every time you learn something about how I work or what I need, write it down immediately. Never make me teach you the same thing twice."
- Agent self-maintains a `lessons.md` file, updating after every mistake
- Progression: Week 1 = basic context (timezone). Week 4 = deep personalization (calendar, clients, writing style, CRM, schedule)
- Key insight: most people reset AI context every conversation; this pattern makes it compound instead
- Lighter-weight alternative to full instinct-based learning pipelines (see [skills.md](skills.md#instinct-based-learning-continuous-learning-v2)) -- single file, single rule, no observer architecture needed

*Source: Twitter Bookmarks/2026-03-09-johann_sath-i-gave-my-openclaw-one-rule-every-time-you-learn-something-a.md*

### Agent Sleep Architecture: Automated Memory Consolidation

A maintenance framework that treats agent infrastructure (skills, rules, memory files) as accumulating entropy that needs periodic consolidation -- the agent equivalent of sleep.

- **Three-tier file hierarchy:** Genome (core identity -- never changes during sleep), Epigenetic (skills, configs -- auto-maintainable), Transient (working context -- discarded between sessions)
- **Two maintenance phases:** NREM = consolidation (deduplicate, compress, prune overlapping skills), REM = abstraction (detect contradictions, merge skills, extract general principles from specific patterns)
- **Episodic-to-semantic transfer:** Raw session logs get compressed into actionable rules, then abstracted into general principles. Example: 5 debugging sessions -> 1 debugging skill -> 1 general principle about error isolation
- **Shelf-life tagging:** Canned goods (stable -- core patterns), Fresh produce (API-dependent -- check weekly), Sandwich (use-once -- auto-expire)
- **Fleet sleep:** For multi-agent teams, nightly scans compare shared skills for contradictions, stale references, and bloat across agents
- **Implementation:** Scheduled nightly job (2 AM cron) with scan -> auto-patch -> synaptic homeostasis (graduated decay of low-use entries) -> memory consolidation -> morning brief

(see [autonomous-agents.md](autonomous-agents.md) for cron/heartbeat scheduling, [workflow-patterns.md](workflow-patterns.md) for maintenance automation)

*Source: Andrew Vibe Coding/Your Agent Needs a Bedtime.md*

### Knowledge Distillation Pipeline Reference Architecture

A two-tier architecture for automated knowledge distillation, extending the four-layer model with automated extraction, dedup, and confidence scoring:

- **Tier 1 (briefing):** A concise, auto-updated CLAUDE.md containing only top-N facts by confidence x access frequency, with budgeted lines per section
- **Tier 2 (full store):** Complete memory store (SQLite/JSON) queried on demand via `memory_search` or `memory_ask`; ~50-80% of sessions need only Tier 1
- **Extraction protocol:** Break conversation/code diffs into chunks, feed to a secondary LLM to generate structured entries (e.g., "Edited src/auth.ts: changed JWT secret to env var")
- **Deduplication logic:** On write, compare each new entry to existing via Jaccard token overlap; >60% overlap means the new entry replaces the old. Periodically run LLM-driven consolidation to merge near-duplicates and resolve contradictions
- **Confidence decay:** Assign each entry a confidence score (0-1) that decays over time; only high-confidence, recently-accessed facts make it into Tier 1. Critical facts (architecture decisions) never drop below a floor threshold
- **Audit loop:** Scheduled consolidation prompt (e.g., "List memory entries older than 60 days with confidence <0.5") catches stale or conflicting entries
- **Standard entry format:** `TIMESTAMP | TYPE | Summary | Source` for queryable, versioned entries

*Source: deep-research-report.md*

---

## Vault-as-Codebase: Knowledge Bases Operated Like Codebases

A paradigm shift for knowledge management: treat an Obsidian vault (or any markdown-based knowledge base) the same way you treat a codebase -- both are folders of text files with relationships, conventions, and patterns that benefit from agents that can navigate and operate them.

**Core insight:** "You don't take notes anymore. You operate a system that takes notes." The human role shifts from writer to editor, from creator to curator. The same shift that vibe coding brought to software development applies to knowledge work (see [workflow-patterns.md](workflow-patterns.md)).

**Agent orientation layers (progressive disclosure for vaults):**
1. **Folder structure** -- a SessionStart hook runs `tree -L 3` so the agent sees what exists without reading every file
2. **Vault index** -- a single file listing every note with a one-sentence description; the agent scans 50+ notes in seconds without opening them
3. **Topic pages (MOCs)** -- maps of content linking to related notes; act as tables of contents per subject

**Agent breadcrumbs:** When Claude discovers something useful about navigating a topic, it records that insight in the topic page. Future sessions read those notes and learn from past navigation -- the vault remembers how to think through itself.

**Claim-based note naming:** Instead of naming notes like topics ("Thoughts on AI slop"), name them like claims ("Quality is the hard part"). When you link to it, the title becomes part of your sentence naturally. Forces the agent to understand the claim when building references, not just categorize.

**Composability principle:** Each note should stand alone -- if linking to it forces you to explain three other things first, split it up. Notes are lego blocks: complete individually, connectable into larger structures.

**Philosophy-per-vault:** Every vault needs its own CLAUDE.md with its own rules. A thinking vault emphasizes depth over breadth. A work vault emphasizes capture-first, project tracking, client context. Same pattern (markdown + links + CLAUDE.md + conventions), different rules.

**Relationship to the four-layer model:** Vaults serve as a Layer 1 mechanism (always-loaded context via CLAUDE.md) combined with Layer 2 characteristics (living documents updated across sessions). The vault index + MOC pattern is an alternative to worklogs for knowledge-oriented rather than feature-oriented work.

### Zero-Friction Capture: Conversation as Interface

- Zero-friction capture principle: "capture should be as easy as texting, and retrieval should be as easy as searching" -- no folders, no tags, no organization
- Every note-taking app fails because organizing friction exceeds forgetting friction -- remove the organizing step entirely
- OpenClaw's built-in memory is cumulative -- remembers everything ever told, grows more powerful over time
- Text from phone triggers actions on computer -- the conversation IS the interface
- Custom Next.js dashboard with global search (Cmd+K) across all memories, conversations, and notes -- agent builds the UI autonomously

(see [Agent Sleep Architecture](#agent-sleep-architecture-automated-memory-consolidation))

*Source: awesome-openclaw-usecases/usecases/second-brain.md*

### Event Sourcing for Project State (2026-03-08)

Immutable event-driven project state management replacing static Kanban boards:

- **Pattern:** User speaks conversationally ("Finished auth, blocked on dashboard") -> agent logs events to database with full context -> preserves complete decision history
- **Event sourcing principle:** Every state change is an immutable event, not a mutation. Enables time-travel queries ("Why did we decide X?")
- **Automatic standups:** Daily standups generated from git commits + project events -- no manual status updates
- **Git-event linkage:** Commits mapped to project events for traceability across code and process
- Applies Martin Fowler's Event Sourcing pattern to project management -- the full audit trail IS the database

(see [workflow-patterns.md](workflow-patterns.md#gsd-context-aware-spec-driven-execution) for phase-based project management alternative)

*Source: awesome-openclaw-usecases/usecases/project-state-management.md*

---



