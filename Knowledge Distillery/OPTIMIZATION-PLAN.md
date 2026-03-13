# Knowledge Distillery — Optimization Plan

**Last updated:** 2026-03-12
**Status:** Phases 1-3, 7-8, 9.1-9.2, 9.3a, 10-11, 15-17 complete. Phase 14 core shipped. Active: 9.3b, 9.3c, 9.4 (9.4b/c done), 13, 6. Parked: 4.2, 4.3, 5.

---

## Completed Phases (Archived)

| Phase | Summary | Session |
|-------|---------|---------|
| 1 | **Structural Fixes** — Renamed "Knowledge Base" to "Knowledge Distillery", fixed folder mismatches, added scan targets, created this plan | 3 |
| 2 | **New Commands** — Built `/consolidate-kb`, `/kb-status`, `/notes-transition`, `/verify-kb`, `/audit`. Created DISCREPANCIES.md. Enhanced `/process-notes` with contradiction detection + Concept Index updates. Added README "Why This Exists" | 4-5 |
| 3 | **Quality Pass** — Fixed 36 broken cross-refs across 11 files. First consolidation (50 entries merged). Tone review (consistent). Stub files marked permanently skipped. Documented 3-layer model in README | 5 |
| 7 | **Teaching Layer** — Created LEARNING-PATH.md (4 levels, 30 entries). Added Impact tiers to Concept Index (Foundational/Core/Enhancing/Reference). Enhanced `/process-notes` with teach-worthy flagging | 7 |
| 8 | **Source Ingestion** — Processed ~69 files across 3 new directories (claude-code-best-practice, x-research-skill, Twitter Bookmarks). ~90 new sections added. Post-ingestion consolidation merged 83 entries. Source count ~105 to ~160 | 6-7 |
| 9.1 | **Quick Wins** — Defined 5 KB health invariants. Added 5 "Don't" rules. Added frontmatter to 5 commands. Resolved 2 discrepancies. Added stale RA rule. Consolidated 6 remaining RAs | 12-14 |
| 9.2 | **Medium Effort** — Added dedup logging. Created DECISIONS.md (11 traces). Extracted audit + transition templates (thin skills pattern) | 15 |
| 10 | **Architecture Review** — Consolidated 59 RAs. Split skills-and-tools.md into skills.md + tools-and-integrations.md (11 to 12 files). Relocated 4 misplaced sections from context-engineering.md. Added scope rules, batch limits, spot-check. Raised consolidation threshold 3 to 5. Recorded 4 new decisions | 18-19 |
| 11 | **MCP Retrieval Layer** — Built hybrid BM25+vector search engine over KB. LanceDB + Ollama mxbai-embed-large embeddings. FastMCP server with 3 tools (search_kb, list_topics, get_section). 30-query eval harness. Reindex hook for automatic updates. Reciprocal Rank Fusion for result merging. Keyword-only fallback when Ollama unavailable | 42 |
| 15 | **Workflow Self-Optimization** — Restructured MEMORY.md (131 to 45 lines + 3 detail files). PreCompact hook. 3 subagents (kb-researcher, kb-processor, verify-claims). 3 rules (kb-editing path-scoped, session-save, no-emojis). Auto-verify in `/consolidate-kb` + `/process-notes`. Context monitor removed (VSCode-incompatible) | 27-32 |
| 16 | **Deterministic Enforcement** — PreToolUse hook blocks source file modifications. PostToolUse hook validates cross-refs after KB edits. Skill safety (disable-model-invocation) on `/process-notes` and `/consolidate-kb`. Dynamic context injection in both commands. Knowledge placement policy with 5-level enforcement ladder. Eval harness (30-query test set) shipped with Phase 11. SessionEnd hook not feasible (command-only, no agent/prompt type) | 30-32 |
| 17 | **Bookmark Export Modernization** — Replaced Bird CLI with browser console export (`export_bookmarks.js`) + Python parser (`parse_bookmarks.py`). fxtwitter enrichment for full text. --skip-existing for incremental runs. Bird CLI references retired across all docs | 39-42 |

*Full task-level detail: [OPTIMIZATION-ARCHIVE.md](_work-archive/OPTIMIZATION-ARCHIVE.md)*

---

## Active Phases (Priority Order)

### Phase 9.3 — Audit Redesign

Current `/audit` checks file existence. A real audit should check substantive things: invariants defined, negation rules present, decision traces exist, verification loops closed, thin skills followed, dedup auditable.

This phase should be done first -- its findings will inform what the coaching layer (Phase 14) should prioritize and what the publishing cleanup (Phase 6) needs to address.

| # | Task | Status | Notes |
|---|------|--------|-------|
| 9.3a | Redesign /audit for substantive KB checks | Done | 28 to 42 checks, 6 to 8 categories (added G: Anti-Patterns, H: Workflow Maturity). Added MCP retrieval, project classification, CLAUDE.md quality rubric. Baseline audit run on all 4 projects. Session 51 |
| 9.3b | Add confidence/epistemic status checks | Pending | Audit should flag sections missing a status tag (Stable / Current best practice / Experimental / Disputed / Deprecated). Not every sentence -- section-level |
| 9.3c | Add freshness checks against decay cadences | Pending | Flag sections overdue for `/verify-kb` based on topic decay rate (see freshness table below) |

#### Freshness Decay Cadences

Not all KB content decays at the same rate. `/verify-kb` targeting and audit checks should respect these cadences.

| Decay rate | Topics | Verify cadence |
|---|---|---|
| Slow | prompt-engineering, workflow-patterns, agent-design, failure-patterns, memory-persistence | Every 6 months |
| Medium | context-engineering, skills, testing-verification, project-setup, autonomous-agents | Every 3 months |
| Fast | tools-and-integrations, community-insights | Every 6-8 weeks |

#### Enforcement Policy

Start soft. Confidence tags and freshness checks are flagged as recommendations ("preferred"), not failures. Promote to hard audit checks only after the standards prove useful across 3+ sessions.

#### Success Criteria

- Confidence tags: do they make sections easier to trust or challenge?
- Freshness cadence: does `/verify-kb` focus on the right places instead of rechecking timeless material?

#### Kill Criteria

- If freshness checks generate noise (false urgency on stable content), widen cadences or drop to advisory-only
- If confidence tagging feels awkward during consolidation, simplify to 3 levels (Stable / Experimental / Deprecated) or drop entirely

#### 9.3a Baseline Audit Results (Session 51)

| Project | Pass | Warn | Fail | Maturity | CLAUDE.md Grade |
|---------|------|------|------|----------|-----------------|
| Knowledge Distillery | 35 | 5 | 0 | Exemplary | A (88) |
| OpenClaw | 19 | 9 | 2 | Developing | A (87) |
| TBB | 31 | 9 | 3 | Developing | B (77) |
| FreedomLab | 26 | 7 | 7 | Starter | B (81) |

---

### Phase 9.4 — Workspace Issues from Baseline Audit

Cross-project issues discovered during the Phase 9.3a baseline audit. These are workspace-level fixes, not KB-specific.

| # | Task | Status | Severity | Notes |
|---|------|--------|----------|-------|
| 9.4a | Git-track OpenClaw, FreedomLab, and AI Notes | Pending | Critical | All three directories are entirely untracked (`??`). No version history, no backup. Add project-level `.gitignore` files first to exclude secrets and large dirs, then commit key files (CLAUDE.md, WORKLOG.md, commands, settings) |
| 9.4b | Secure FreedomLab OAuth client secret | Done | Critical | Relocated to `~/.config/google-drive-mcp/`. Added `client_secret_*.json`, `token*.json`, `credentials*.json` to workspace `.gitignore`. Updated 3 Python scripts + setup guide to new path. Session 53 |
| 9.4c | Fix workspace `.gitignore` for `.claude/` | Done | High | Replaced blanket `.claude/` with surgical entries: `settings.local.json`, `.tmp/`, `plans/`, `.claude-plugin/`, `.git/`, `skills/`. Commands, rules, hooks, agents, scripts, settings.json now trackable. Session 53 |
| 9.4d | Trim CLAUDE.md Part 2 bloat (3 projects) | Pending | Recommended | OpenClaw (292 lines), TBB (254), FreedomLab (330) all have duplicated workspace rules in Part 2 sections. Cut generic operating principles already covered by `.claude/rules/`. Target: all under 200 lines |
| 9.4e | Create TBB settings.json | Pending | Recommended | Only `settings.local.json` exists (gitignored). No committed config, no deny patterns at project level |
| 9.4f | Add verification hook for TBB | Pending | Recommended | No `npx astro check` hook on .ts/.astro edits. Workspace hooks are KB-specific only |
| 9.4g | Trim OpenClaw WORKLOG.md | Pending | Recommended | 174 lines -- sessions 57-61 should move to SESSION-ARCHIVE.md |
| 9.4h | Split process-notes.md | Pending | Recommended | 215 lines -- only kitchen-sink command. Delegate classification/routing to kb-processor agent. Target: under 100 lines |

---

### Phase 14 — Coaching Layer (includes Teaching Queue)

The AI proactively applies KB best practices, pushes back on suboptimal requests, and surfaces workflow optimizations in real time. Includes the former Phase 12 teaching queue -- five KB concepts the user hasn't adopted yet, taught in dependency order.

**Origin:** User insight -- the KB is passive reference material. The AI should internalize best practices and actively apply them. Teaching queue originated from Session 19 when user asked about Agent Teams and tmux.

**Core Principles:**
- Push, don't pull
- Intervene only when expected value of interruption is high
- Biggest risk is premature doctrine, not missing information

#### 14.0 — Framework Design

Four components:

**1. Behavioral Instructions** — Rules that make AI proactively apply KB practices:
- Request lacks constraints -> apply Specificity principle, ask for details
- Starting a feature -> adaptive kickoff (simple task = 0-1 questions, complex/ambiguous = structured kickoff)
- Completing work -> verify artifacts, don't trust self-reports
- Project gets complex -> suggest subagents, personas, context isolation
- Architectural decision -> suggest decision trace
- Coaching is gentle (suggest, don't block) with escape hatch ("just do it")
- Always cite the source principle
- High stakes / complexity / repeated mistake -> coach proactively. Low stakes / simple execution / user optimizing for speed -> stay quiet

**2. Insight Processing Pipeline** — Compare new articles against KB + current setup, identify genuine gaps, suggest actions, log to KB.

**3. Personal Context Foundation** — `about-me.md` + `working-style.md` in global memory. Compound over time.

**4. Post-Task Optimization Habit** — `*Idea:* what if we did ___` (gentle, skippable). Draw from unused KB practices.

#### 14.1 — Teaching Queue (formerly Phase 12)

Five KB concepts the user hasn't adopted yet. Teach in dependency order.

| # | Concept | KB Source | Status | Notes |
|---|---------|-----------|--------|-------|
| 14.1-T1 | Personas: Imaginary Colleagues | agent-design.md > Personas | Pending | @Security, @UX, @Test, @Machiavelli reviewers |
| 14.1-T2 | Prompt Cache Architecture | context-engineering.md > Prompt Cache Architecture | Pending | Never change tools/models mid-session |
| 14.1-T3 | Meta-Agent Architecture | agent-design.md > Meta-Agent Architecture | Pending | Two-terminal pattern |
| 14.1-T4 | claude-mem Plugin | memory-persistence.md > Layer 3 | Pending | Automatic cross-session memory via hooks + local DB |
| 14.1-T5 | Agent Teams | agent-design.md > Agent Teams | Pending | Parallel Claude Code sessions with tmux split panes |

**Teaching order:** T1 -> T2 -> T3 -> T4 -> T5
**Teaching rule:** Surface when relevant to current work, not on a schedule. Skip on fast execution tasks. Opportunity, not obligation.

#### Success Criteria

- Adaptive kickoff: reduces friction without lowering task quality
- Post-task coaching: surfaces ideas that are actually adopted (not just acknowledged)
- Teaching queue: concepts get used in real work, not just explained
- Coaching overall: user says "that was helpful" more than "just do it"

#### Kill Criteria

- If coaching interrupts too often, reduce to top 3 triggers only
- If teaching suggestions are ignored repeatedly, make them less frequent or remove the concept from the queue
- If post-task ideas are consistently skipped, reduce frequency or make them session-end only
- If the coaching layer adds friction to simple tasks despite the "stay quiet" rule, tighten the intervention threshold

#### 14.2 — Implementation

| # | Task | Status | Notes |
|---|------|--------|-------|
| 14.2a | Create about-me.md in global memory | Done | Placeholder sections for user to fill in. Session 53 |
| 14.2b | Create working-style.md in global memory | Done | Collaboration prefs, escape hatches ("just do it", "stop coaching"). Session 53 |
| 14.2c | Draft behavioral instruction set | Done | 3 active rules (adaptive kickoff, specificity nudge, verification before done) + 7 queued. Placed in `.claude/rules/coaching.md`. Session 53 |
| 14.2d | Determine instruction placement | Done | Rules folder (`coaching.md`, `teaching-queue.md`). Auto-loaded by Claude Code. Session 53 |
| 14.2e | Build insight processing checklist | Done | `/process-insight` command: fetch/read content, compare via MCP search_kb, classify as covered/extends/new/contradicts, suggest actions. Session 53 |
| 14.2f | Define post-task optimization format | Done | Embedded in coaching rule #8 (queued). Format: `*Idea: [suggestion]. See [KB-file.md] > [section].* (say 'skip' to dismiss)`. Session 53 |
| 14.2g | Test with a real project task | Pending | Evaluate if it helps or annoys |

#### 14.3 — Validation

| # | Task | Status | Notes |
|---|------|--------|-------|
| 14.3a | Verify no conflicts with project CLAUDE.md files | Pending | |
| 14.3b | Test escape hatch | Pending | |
| 14.3c | Confirm coaching cites KB sources correctly | Pending | |
| 14.3d | User feedback after 3 sessions | Pending | |

#### 14.4 — Article Triage Gap

KB covers CLAUDE.md scopes and progressive disclosure but NOT tiered file prioritization within working folders. The 3-tier manifest (Canonical/Domain/Archival) is a distinct concept.

---

### Phase 13 — Image-Aware Processing

Enrich `/process-notes` with vision-based image descriptions. Images are transient enrichment, not standalone knowledge items.

**Origin:** 401 image references across 113 source files. ~265 are content images containing knowledge not in surrounding text.

**Constraints:** Source files never modified. Descriptions are transient. Per-file cap: 10 images. Per-batch cap: 40 images.

#### 13.1 — Implementation

| # | Task | Status | Notes |
|---|------|--------|-------|
| 13.1a | Add step 5a-ii to `/process-notes` | Pending | Detect `![alt](path)` refs, skip badges/logos/GIF/SVG, read/fetch images, generate descriptions |
| 13.1b | Add skip rules | Pending | shields.io, logos, GIF, SVG, video thumbnails |
| 13.1c | Add failure handling | Pending | `[image-missing]`, `[image-unavailable]`, `[image-unsupported]`. All logged, none fatal |
| 13.1d | Add per-file cap (10) and per-batch cap (40) | Pending | Prevents image-heavy files from consuming session capacity |
| 13.1e | Add Image Processing Summary to step 8 report | Pending | Counts: found, described, skipped, failed |

#### 13.2 — Validation

| # | Task | Status | Notes |
|---|------|--------|-------|
| 13.2a | Test with local-image file | Pending | `everything-claude-code/the-shortform-guide.md` (10 local images) |
| 13.2b | Test with remote-image file | Pending | Twitter Bookmarks thread with pbs.twimg.com images |
| 13.2c | Test with badge-heavy file | Pending | README with shields.io badges |
| 13.2d | Test with missing local refs | Pending | Old Notes file with orphaned image refs |
| 13.2e | Verify source files unmodified | Pending | Confirm no source `.md` files changed |

#### 13.3 — Siftly-Inspired Enhancements

Borrowable ideas from Siftly's vision pipeline: structured vision output (OCR, tags, classification) instead of free-text, image type classification for smarter skip rules, OCR extraction for screenshots of code/terminal/architecture diagrams.

| # | Task | Status | Notes |
|---|------|--------|-------|
| 13.3a | Evaluate structured vs free-text vision prompts | Pending | Test both on 5 sample images, compare synthesis utility |
| 13.3b | Add image type classification to skip rules | Pending | meme/reaction/selfie = skip; chart/code/diagram/architecture = priority |

---

### Phase 6 — Publish & Market

**Key decision:** Publish the SYSTEM, not the personal notes. (See DECISIONS.md)

#### 6.1B — Pre-Publication Cleanup

**6.1B-i: Move internal files to `_work-archive/`**

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.1b-1 | Create `Knowledge Distillery/_work-archive/` | Done | Added to `.gitignore` |
| 6.1b-2 | Move optimization docs | Partial | `OPTIMIZATION-ARCHIVE.md` moved. `OPTIMIZATION-PLAN.md` stays (active workflow) |
| 6.1b-3 | Move session history | Partial | `SESSION-ARCHIVE.md` moved. `SESSION-HISTORY.md` + `WORKLOG.md` stay (active workflow) |
| 6.1b-4 | Move research scratch | Done | `RESEARCH-retrieval-layer.md`, `Phase 11 plan`, `new_files_triage.txt` moved |
| 6.1b-5 | Move deep research reports | Done | 3 `deep-research-report*.md` files moved |
| 6.1b-6 | Move Coaching Layer brainstorm | Done | `Coaching Layer/` moved |
| 6.1b-7 | Move ingestion tracking | Deferred | `sources/ingested-files.md`, `ingested-paths.txt`, `processing-log.md` still needed by `/process-notes`. Move at publish time |
| 6.1b-8 | Move bookmark tooling | Partial | `refresh_bird_cookies.py` moved (retired). `export_bookmarks.js` + `parse_bookmarks.py` stay (active pipeline) |
| 6.1b-9 | Move KD-level `.claude/` | Done | `Knowledge Distillery/.claude/` moved to archive |

**6.1B-ii: Scrub published files of internal language**

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.1b-10 | Clean README.md | Pending | Remove "Built 2026-02-27", session numbers, "Phase X" references, optimization plan links. Keep structure, pipeline diagram, Concept Index, Retrieval Layer docs |
| 6.1b-11 | Clean DECISIONS.md | Pending | Remove "(Session N)" from all decision traces. Decisions are valuable for outsiders; session numbers are not |
| 6.1b-12 | Clean CLAUDE.md | Pending | Remove optimization tracker references, session continuity section, internal phase numbers. Keep commands, conventions, don't rules, health invariants |
| 6.1b-13 | Clean LEARNING-PATH.md | Pending | Review for internal references |
| 6.1b-14 | Clean DISCREPANCIES.md | Pending | Remove session-specific resolution notes |
| 6.1b-15 | Clean KB-PROCESS.md | Pending | Review for internal language |
| 6.1b-16 | Audit topic files for leftover internal refs | Pending | Grep all 12 topic files for "Session", "Phase", "OPTIMIZATION", "WORKLOG" references |

**6.1B-iii: Folder structure cleanup**

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.1b-17 | Gitignore all source note directories | Pending | `Andrew Vibe Coding/`, `Claude Code/`, `Threads/`, `Twitter Bookmarks/`, `Old Notes/`, `Ralph Wiggum/`, `Scrapling/`, etc. Source notes are private inputs, not published |
| 6.1b-18 | Gitignore cloned repos | Pending | `anthropic-courses/`, `awesome-openclaw-usecases/`, `claude-agent-sdk-*`, `claude-code-*`, `claude-cookbooks/`, `claude-plugins-official/`, `claude-quickstarts/`, `everything-claude-code/`, `get-shit-done/`, `langextract/` |
| 6.1b-19 | Decide on `.claude/commands/` placement | Pending | Currently in parent `AI Notes/.claude/commands/`. For publishing, commands should ship inside `Knowledge Distillery/` or be clearly documented |
| 6.1b-20 | Decide on `kb-mcp/` placement | Pending | Currently at `AI Notes/kb-mcp/`. Should it move inside `Knowledge Distillery/` for a self-contained published folder? |
| 6.1b-21 | Final structure review | Pending | Verify the published folder is self-contained: topic files, README, commands, search engine, provenance -- nothing depends on private files |

**What the published folder looks like after cleanup:**

```
Knowledge Distillery/
  README.md                    # Project overview, pipeline, Concept Index
  CLAUDE.md                    # Instructions for Claude Code users
  LEARNING-PATH.md             # Curated learning progression
  DECISIONS.md                 # Architectural decision traces
  DISCREPANCIES.md             # Review queue
  KB-PROCESS.md                # Pipeline internals
  prompt-engineering.md        # 12 topic files...
  context-engineering.md
  workflow-patterns.md
  agent-design.md
  memory-persistence.md
  skills.md
  tools-and-integrations.md
  testing-verification.md
  failure-patterns.md
  project-setup.md
  autonomous-agents.md
  community-insights.md
  sources/
    source-index.md            # Provenance mapping (public)
  kb-mcp/                      # Local search engine
    chunker.py
    indexer.py
    kb_mcp_server.py
    eval.py
    requirements.txt
  .claude/commands/             # Slash commands (/process-notes, etc.)
  _work-archive/                # Gitignored: optimization docs, session history, research
```

#### 6.2A — Repository Setup (Infrastructure)

What to include: slash commands, KB structure templates, README, LEARNING-PATH template, CLAUDE.md template, kb-mcp search engine.
What to exclude: source notes, synthesized personal content, `_work-archive/`, MEMORY.md.

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.2a | Create public GitHub repo | Pending | Name candidates: `ai-knowledge-distillery`, `knowledge-distillery`, `ai-distillery` |
| 6.2b | Scaffold repo structure | Pending | Clean folder structure with template files, commands, kb-mcp, example CLAUDE.md |
| 6.2c | Add LICENSE | Pending | MIT for commands/tooling, CC-BY-4.0 for content templates |
| 6.2d | Write repo-level README | Pending | What it is, quickstart, screenshot of /audit output, link to LEARNING-PATH |
| 6.2e | Add CONTRIBUTING.md | Pending | How to submit improvements to commands, pipeline docs, quality standards |

#### 6.2B — Verified Starter Content (Future)

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.2f | Execute deep-research-prompt.md | Pending | Comprehensive meta-workflow research |
| 6.2g | Verify starter content claims | Pending | Run /verify-kb on all starter files before publishing |
| 6.2h | Write starter topic files | Pending | Subset: prompt-engineering, context-engineering, project-setup, failure-patterns |

#### 6.3 — Content Marketing

| # | Task | Status | Notes |
|---|------|--------|-------|
| 6.3a | Write launch thread (Twitter/X) | Pending | Hook: "I built a system that synthesizes AI knowledge instead of just accumulating it." |
| 6.3b | Write long-form post | Pending | Blog post or Substack |
| 6.3c | Record demo video | Pending | Full loop: drop note -> /process-notes -> /audit -> fix CLAUDE.md |
| 6.3d | Post to relevant communities | Pending | r/ClaudeAI, r/LocalLLaMA, HN, Claude Code Discord, OpenClaw |

#### 6.4 — Positioning & Messaging

**One-liner:** "A knowledge system that synthesizes AI best practices and audits your projects against them."

**Key differentiators:** Synthesis over retrieval, contradiction detection, provenance tracking, verification pipeline, actionable audit loop, local search engine, compounding value.

**Target audiences:** Claude Code users (primary), OpenClaw builders, PKM community, AI educators.

**Comparisons:** vs Obsidian ("stores vs synthesizes"), vs RAG ("5 results vs 1 answer"), vs agent memory ("decays vs compounds").

---

## Parked Ideas

| # | Idea | Status | Notes |
|---|------|--------|-------|
| 4.2 | Coverage blind spots | Parked | Thin areas: non-Anthropic ecosystems, RAG, evals. Address by ingesting new sources |
| 4.3 | KB as shared infrastructure | Parked | Mechanism for other projects to pull Distillery context |

---

## Phase 5 — Workspace-Wide Scope (Future Vision)

The Distillery methodology generalizes beyond AI Notes.

**Target directories:** `FreedomLab/`, `TBB/`, `Learning CC/`, `FL/`, `SkillsTest/`

**Reusable primitives:** `/process-notes` pattern, topic file structure, source tracking dedup

**Future command:** `/init-distillery [path]` -- scaffold a new Knowledge Distillery at any target path.

---

*Session history: [SESSION-HISTORY.md](../SESSION-HISTORY.md) (Sessions 9-23) | [SESSION-ARCHIVE.md](_work-archive/SESSION-ARCHIVE.md) (Sessions 1-8)*
