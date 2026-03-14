# OpenClaw & Autonomous Agents

OpenClaw is an open-source runtime that turns a dedicated computer into a persistent, autonomous AI employee. Unlike session-based tools (Claude Code, ChatGPT), OpenClaw runs 24/7 as a background service, routes messages through a gateway, and takes actions on your behalf even while you sleep.

---

## What Is OpenClaw

### A 24/7 Self-Hosted AI Employee

OpenClaw is a persistent process that gives an AI agent full computer access -- shell, browser, file system, messaging apps. It can send emails, manage calendars, vibe-code applications, search the web, post to social media, and build software autonomously. It remembers everything about you across sessions because its workspace files live on disk, not in ephemeral chat context.

The agent is open source, fully customizable, and self-improving. If it forgets a detail or does something poorly, you tell it to fix its own memory system or build a new skill. It modifies its own configuration files and workspace in response.

### The Gateway Concept

The gateway is the core persistent process. It:
- Runs as a system daemon (launchd on Mac, systemd on Linux)
- Receives messages from connected channels (Telegram, Discord, WhatsApp, iMessage, email)
- Routes them to the configured LLM
- Returns responses to the same channel
- Executes scheduled cron jobs and heartbeat checks
- Manages the agent workspace and file system

You interact with OpenClaw through apps you already use. You do not go to a website; the agent comes to you.

### 6-Component Architecture

A structural breakdown of OpenClaw's core architecture.

- **Six components:** Gateway (message router/daemon, WebSocket on port 18789), Agent (brain/LLM), Tools (exec, browser, file, message, memory), Workspace (long-term memory as .md files), Sessions (per-conversation history as .jsonl), Nodes (physical devices)
- **Workspace file roles:** AGENTS.md (playbook), SOUL.md (personality), USER.md (user profile), MEMORY.md (long-term facts), daily logs (YYYY-MM-DD.md), IDENTITY.md, HEARTBEAT.md, TOOLS.md
- **Gateway pipeline:** message -> context inject (bootstrap files + session history + skills) -> LLM loop -> tool execution -> response -> write to .jsonl
- **Exec security modes:** Sandbox (Docker), Gateway (whitelisted commands), Full (unrestricted). Default should never be Full
- **Five common mistakes:** (1) dmScope set to "main" with multiple users, (2) exec in full mode, (3) empty workspace, (4) no compaction strategy (memory flush before compression), (5) port 18789 exposed to internet

(see [agent-design.md](agent-design.md) for brain+muscles pattern)

*Source: Twitter Bookmarks/Anatomy of OpenClaw a guide after which you'll build agents differently.md*

### How It Differs from Claude Code

| Dimension | Claude Code | OpenClaw |
|-----------|-------------|----------|
| Lifecycle | Session-based; dies when terminal closes | Always-on daemon; survives reboots |
| Autonomy | Requires approval for each command | Runs unsupervised; no approval loop |
| Memory | Per-project CLAUDE.md | Nine workspace files + custom folders, persistent on disk |
| Channels | Terminal only | Telegram, Discord, WhatsApp, iMessage, email, web UI |
| Proactivity | Reactive only | Heartbeats, cron jobs, autonomous task discovery |

---

## Hardware Recommendations

| Option | Cost | Best For | Notes |
|--------|------|----------|-------|
| Existing laptop | Free | Getting started, experimenting | Any old laptop in a closet works; disable sleep mode |
| Raspberry Pi | ~$50 | Minimal always-on host | Limited but functional |
| Mac Mini M4 | ~$600 | Best value dedicated device | Consensus "best bang for buck"; sufficient for cloud APIs + light local models |
| Mac Studio | $2,000+ | Power users running local models | Required only for large local models (MiniMax, Qwen 70B+) |
| VPS (Hostinger, etc.) | ~$10-30/mo | Remote access, team setups | Manageable from anywhere; no browser control; requires SSH hardening |

**Why NOT a VPS (for most users):** Local is secure by default -- no exposed ports, no SSH brute-force surface. VPS requires significant hardening (firewall, token auth, SSH lockdown). Local gives full browser control and better integration with your desktop environment. Multiple sources recommend starting local and only using a VPS if remote access or team sharing is required.

**Progressive hardware path:** Start with what you own. Upgrade to Mac Mini when you want a dedicated always-on device. Upgrade to Mac Studio only when you need to run local models for specific workflows.

### Moltworker: Serverless Agent Deployment on Cloudflare

An alternative to self-hosted OpenClaw: deploy agents on Cloudflare Workers ($5/month minimum). Uses Sandbox SDK for isolated execution, Browser Rendering for web automation, and R2 for persistent storage. Same capabilities as self-hosted without buying hardware. Assets persist via R2 bucket mounting.

### Claude Subscription vs API Key Cost Trap

A common and expensive mistake: using Anthropic's pay-per-use API console instead of the Claude Pro/Max subscription token.

- Claude Pro ($20/mo) or Claude Max ($90/mo) provides a flat monthly rate with significantly more value than pay-per-use API billing.
- During OpenClaw onboarding, select "Anthropic Token" (from your Claude subscription), NOT "Anthropic API" (from the Anthropic console).
- One user burned $800 before discovering this distinction. Multiple sources confirm that subscription tokens are the cost-effective path for personal OpenClaw usage.
- Note: Using Claude subscriptions with OpenClaw may violate Anthropic's terms of service -- reports exist of account bans. Verify current ToS before relying on this approach.
- Watch for a common setup bug: spaces in the Claude token string cause HTTPS errors. Always check for trailing spaces when pasting tokens.

*Sources: I wasted 80 hours and $800 setting up OpenClaw.md, How to Reduce OpenClaw Model Costs by up to 90% Full Guide.md*

### Google Cloud Agent Deployment Workflow

- 6-step high-level workflow for deploying an agent workforce on Google Cloud:
  1. Connect Claude Code to Google Cloud via API
  2. Set up a small VM
  3. Install Claude Agents SDK
  4. Determine the agent workforce needed
  5. Let Claude ask questions to spec them
  6. Give daily tasks, manage via Telegram bot
- Earliest reference found (Jan 2026) of the Claude Code -> Cloud VM -> Agent SDK -> Telegram management pipeline
- Concise enough to serve as a quick-start mental model for cloud-hosted agent deployment

*Source: Twitter Bookmarks/Thread by @bramk.md*

### Cost Anatomy and Optimization

Synthesized from multiple practitioner reports on OpenClaw token costs and reduction strategies.

- **Per-message cost composition:** Every request bundles system instructions + all workspace files (AGENTS.md, SOUL.md, MEMORY.md, etc.) + full conversation history. Without workspace config, expect ~3x token overspend per call
- **Bootstrap vs semantic memory:** Bootstrap files load every call (constant token drain). Semantic search via MEMORY.md pulls facts on-demand (zero constant cost). Strategy: critical rules in bootstrap, everything else in semantic search
- **Heartbeat vs cron cost:** A 15-minute heartbeat = 96 executions/day within an existing session context (~$10-20/day). Cron jobs start fresh sessions and are far cheaper. Use Gemini Flash ($0.10/M tokens) or local Ollama for heartbeats, not your primary model
- **Model tiering:** Opus for complex reasoning, Sonnet for daily work, Gemini Flash for simple tasks. OpenRouter auto-routes 80% of requests to cheaper models across 630+ model options
- **QMD skill:** BM25 + vector search indexes knowledge bases locally, sending only relevant snippets to the model -- cuts research token usage by ~90%
- **Session initialization prompt:** Summarizing context at session start reduces per-message payload from ~50kb to ~8kb (40 cents -> 5 cents per session)
- **n8n offloading:** Deterministic workflows (daily reports, email checks) can be moved entirely out of the LLM loop via n8n integration -- near-zero token cost
- **Real savings:** 65-70% cost reduction across light, power, and heavy user profiles. After workspace optimization: 70% reduction with flawless cross-session recall
- **Session commands:** `/status` (check token usage), `/compact` (compress context), `/new` (fresh session), `/models` (switch mid-session)

(see [tools-and-integrations.md](tools-and-integrations.md) for OpenRouter and n8n integration details, [memory-persistence.md](memory-persistence.md) for memory architecture)

*Sources: Clawdbot aka Openclaw/OpenClaw Too Expensive Try This Instead (97% Reduction).md, Twitter Bookmarks/The OpenClaw Cost Optimization Playbook.md, Twitter Bookmarks/2026-03-04-slash1sol-stop-wasting-tokens.md*

---

## First Steps After Setup

### 1. Brain Dump

Your agent is a new employee. Brief it the same way you would brief a new hire. Tell it:
- **Who you are** -- background, career, skills, daily life
- **Personal preferences** -- communication style, autonomy level ("be proactive, don't ask permission for everything"), tools you prefer
- **Goals and ambitions** -- specific targets (revenue goals, fitness goals, learning goals), what success looks like
- **Current projects and context** -- what you are working on right now

This information gets stored in `USER.md` and `MEMORY.md` in the workspace. Every future conversation inherits this context. The more you give, the more useful the agent becomes (see [context engineering](context-engineering.md)).

### 2. Set Up a Morning Brief

A scheduled cron job that sends you a personalized daily briefing via Telegram or WhatsApp. Example prompt:

> Please schedule a brief for me every day at 8 AM. Send it to my Telegram. Include: (1) weather for my location, (2) top news in [your interest area], (3) my tasks from [your to-do app], (4) tasks you can complete for me today that bring me closer to my goals.

Item 4 is the key -- it forces the agent to think proactively about what it can do for you, which is the entry point to reverse prompting.

### 3. Build Mission Control Dashboard

A locally-hosted Next.js dashboard that the agent vibe-codes for itself. Prompt:

> I want you to set up a mission control. This is a custom place for us to build out any tools we need to be more productive. Please build this using Next.js and host it locally.

From there, add custom tools as needs emerge: to-do lists, approval queues, sub-agent tracking, content calendars, analytics panels. Each tool is vibecoded by the agent on request.

### 4. Mature Workspace File Taxonomy

After several weeks of use, power users expand beyond the default 9 workspace files into a richer taxonomy. The custom files you add become your competitive moat -- no two setups look alike.

Example workspace after 3 weeks of active use:

```
workspace/
  SOUL.md          # Personality, values, boundaries (update rarely)
  IDENTITY.md      # Factual identity (name, role)
  USER.md          # Owner profile, preferences, goals
  TOOLS.md         # Technical configs, how-to references
  MEMORY.md        # Long-term context
  HEARTBEAT.md     # Autonomous check-in rules
  AGENTS.md        # Behavioral rules, permission boundaries
  BRAIN.md         # Live working memory (ephemeral session state)
  CLIENTS.md       # Client/contact profiles (personal CRM)
  PLAYBOOK.md      # Decision frameworks, SOPs
  VOICE.md         # Writing voice guide, tone rules
  SCHEDULING.md    # Calendar preferences, VIP list
  memory/          # Daily logs (YYYY-MM-DD.md)
  skills/          # Custom skills (tweet-writer/, security-auditor/, etc.)
  docs/            # Saved research (living knowledge base)
  content/         # Draft content for publishing
  crm/             # Contact relationship data
```

- BRAIN.md serves as live working memory for the current session -- ephemeral state that the agent updates continuously during work. Distinct from MEMORY.md (long-term) and daily notes (daily log).
- VOICE.md captures writing voice rules so the agent produces content that sounds like you. Feed it samples of your writing and ask it to extract patterns.
- PLAYBOOK.md holds decision frameworks: "When X happens, do Y." Turns institutional knowledge into repeatable procedures.
- CLIENTS.md can be auto-populated: one user had the agent build a 697-contact CRM from Gmail and Calendar data.
- The standard 9 files are the foundation. Everything you add on top is what transforms a chatbot into an employee that understands your world.

*Sources: my openclaw after 3 weeks.md, I setup OpenClaw exactly 7 days ago.md, OpenClaw Best Practices.md*

### 5. Diagnostic and Recovery Commands

- `openclaw doctor --fix` resolves many "my agent is stupid" complaints that are actually broken configuration. Run it before assuming the agent is at fault.
- `openclaw security audit --deep` performs a comprehensive security review. Schedule it as a daily cron rather than running it manually.
- `openclaw logs --tail` monitors real-time activity and token usage. Essential for diagnosing unexpected cost spikes or unusual behavior.
- For catastrophic recovery: if the workspace is backed up with git (recommended every 2 hours via silent backup cron), `git checkout` restores any file the agent overwrites or deletes.

*Sources: I Burnt $127 in API Credits.md, OpenClaw Best Practices.md, 3 cron jobs.md*

### Post-Install Hardening Checklist: 9-Section Production Readiness

@moritzkremb's comprehensive 30-60 minute hardening pass for turning a fresh OpenClaw install into production-usable:

- **Section 0 -- Troubleshooting Baseline:** Separate Claude project for OpenClaw ops; install `clawddocs` skill; Context7 docs integration; `openclaw doctor --repair` for quick fixes
- **Section 1 -- Personalization:** USER.md, IDENTITY.md, SOUL.md -- "make responses specific, opinionated, and useful from day 1"
- **Section 2 -- Memory Reliability:** MEMORY.md for long-term + `memory/YYYY-MM-DD.md` for daily; heartbeat promotes important learnings
- **Section 3 -- Model Defaults:** Primary + fallback chain; "optimize for reliability first, then cost"
- **Section 4 -- Security:** Secrets in `~/.openclaw/secrets/openclaw.env` (folder 700, file 600); VPS: inbound from trusted IPs only; `dmPolicy: "allowlist"` for Telegram
- **Section 5 -- Telegram:** Disable privacy mode in BotFather; topic-specific systemPrompt; default ack reaction; streaming responses
- **Section 6 -- Browser Strategy:** Managed browser profile for automation (isolated, stable); Chrome relay only for logged-in state/passkeys
- **Section 7 -- Heartbeat/Cron Hardening:** Heartbeat checks critical crons for `stale lastRunAtMs`; force-runs missed jobs
- **Section 8 -- Agent-Owned Accounts:** Dedicated Google, Gmail/AgentMail, GitHub accounts for clean separation and auditability
- **Section 9 -- Skills Strategy:** "If repeated 2-3 times, skill it"; install summarize skill early; add voice transcription workflow

Corroborates security findings in [Real-World OpenClaw Security Audit](#real-world-openclaw-security-audit-findings) -- this checklist addresses every gap the audit found.

*Source: Twitter Bookmarks/2026-03-04-moritzkremb-openclaw-optimized-setup-guide.md*

### RAG-Based Memory with pgvector

PostgreSQL + pgvector as a semantic memory layer for agents needing better recall at scale.

- Label memories, create vectors, store label + vector + raw text in PostgreSQL with pgvector extension
- Short-term/long-term flush: agent writes to MEMORY.md during sessions; cron flushes into vector database; new sessions start minimal with search tool
- Benefits: better recall, lower token usage; trade-off: more moving parts
- Alternative: filesystem-based .md memory works for simpler setups
- (see [memory-persistence.md](memory-persistence.md) for existing memory patterns)

*Source: Thread by @SimonHoiberg.md*

### Multi-Agent Communication: Direct vs Boss Routing

- **Direct communication outperforms boss routing:** Routing all agent communication through a "boss" agent wastes tokens and produces worse results than talking to each agent directly
- **Discord as multi-agent hub:** Each agent gets its own Discord app connected to its own folder, with per-agent channels for communication. Lightweight and observable
- **File system organization:** Keeping all agent files in a single `.openclaw` folder gets messy fast -- move human-editable files (SOUL.md, MEMORY.md) to an accessible location
- **Self-sustaining agents:** Each agent should be independently functional, not scripts dependent on a main agent

*Source: Twitter Bookmarks/This is how you actually build an AI team via OpenClaw ANTILARP.md*

### Three-Tier Memory Architecture for Self-Improving Agents

A layered memory system that scales beyond flat MEMORY.md as agent complexity grows.

- Tier 1 (MEMORY.md): curated long-term memory with "BAD" sections where agents catalogue rejected patterns
- Tier 2 (memory/YYYY-MM-DD.md): daily logs; load only today + yesterday; archive old logs every two weeks (one agent hit 161K tokens before correction)
- Tier 3 (shared-context/): cross-agent knowledge layer (THESIS.md, FEEDBACK-LOG.md, SIGNALS.md) -- one correction propagates to all agents
- One-writer rule: never have two agents writing to the same file; design with one writer and many readers
- File-based coordination replaces message queues; scheduling order enforces dependencies
- Timeline: start with SOUL.md + USER.md + one cron (day 1), add complexity weekly as patterns emerge
- (see [memory-persistence.md](memory-persistence.md) for memory system patterns)

*Sources: How to set up OpenClaw Agents that actually get better Over Time.md, Before You Do Anything With OpenClaw.md*

---

## Brain + Muscles Architecture

The most cost-effective and capable setup separates orchestration ("brain") from execution ("muscles") (see [agent-design.md#brain--muscles-pattern-from-openclaw](agent-design.md#brain--muscles-pattern-from-openclaw) for the general pattern).

### Brain: Orchestration Model

The brain decides what to do, routes tasks, and manages conversation. It needs to be the smartest, most personable model available.

- **Opus 4.6** -- best decision-maker, most "warm" in conversation, but expensive (~$200/mo subscription)
- **Sonnet 4.5** -- cheaper Opus; good default for daily use
- **GPT 5.3 Codex** -- can piggyback on existing ChatGPT subscription

### Muscles: Specialist Models

Muscles handle specific execution tasks. The brain delegates to them, saving tokens on the expensive orchestration model.

| Muscle | Use Case | Why |
|--------|----------|-----|
| Codex (OpenAI) | Code generation, debugging | Cheap, specialized for code |
| XAI / Grok API | Trending news, real-time data | Hooked into social media feeds |
| Perplexity Sonar Pro | Web search | Agentic search, better than Brave default |
| Perplexity Deep Research | In-depth research | Long-form investigation on demand |
| Brave Search API | Basic web search | Built-in default, free tier |
| MiniMax / Qwen (local) | Code, general tasks | Free after hardware cost; unlimited tokens |
| Haiku 4.5 / Gemini Flash | Heartbeat checks | Cheap, fast; no need for expensive model on routine pings |

### The Progressive Path

1. **Start with one cloud model** (Sonnet or your existing subscription)
2. **Add muscles** as you discover workflows that benefit from specialization (Perplexity for search, Codex for code)
3. **Add local models** when you have hardware that supports them and want to eliminate per-token costs for specific tasks
4. **Swap heartbeat and routine tasks** to cheap models (Haiku, Flash) to reduce ongoing costs

Configure model switching with aliases so you can type `/opus` or `/sonnet` to change models mid-conversation.

### Model Routing and Cascading

Beyond the brain+muscles split (which assigns models by role), a **cascading router** assigns models dynamically per query based on complexity:

- Route each incoming query through a classifier or heuristic check (complexity, topic, required accuracy)
- Send simple queries (greetings, factual lookups, status checks) to a small local model (e.g., Mistral 7B)
- If the small model's response fails a confidence/quality check, escalate to a mid-tier model (e.g., DeepSeek R1, Claude Sonnet)
- Reserve premium models (GPT-4, Claude Opus) only for queries that fail both tiers
- This is distinct from the brain+muscles pattern: brain+muscles assigns by task type (code goes to Codex, search goes to Perplexity); cascading assigns by query difficulty within a single task type
- OpenClaw supports this via its routing/chain config -- configure model endpoints and switch based on prompt context

*Source: deep-research-report-openclawagents.md*

### Four Workflow Archetypes for Model Selection

Decision frameworks for choosing model configurations based on your primary constraint:

- **Privacy-first:** Run everything locally (Llama 70B or Mistral 7B quantized). Cascade: small local model for initial interpretation, large local model for final answers. Zero cloud API calls. Accept higher hardware cost and slower throughput.
- **Cost-first:** Try the cheapest model first (Gemini Flash-Lite at ~$0.075/M tokens, or Llama 3B). Escalate to mid-tier (DeepSeek R1, Mistral Medium) only if quality is insufficient. Reserve premium models (GPT-4, Opus) for failures. Monitor cumulative cost per request.
- **Performance-first:** Default to top-tier APIs (GPT-5, Claude Opus) for everything. Use local models only as fallbacks when APIs are down. Cache expensive results. Cost is secondary.
- **Balanced:** Mix cloud and local. Use Claude Sonnet or GPT-4 for chat, fall back to Mistral 7B for low-risk or offline tasks. Quantize all local models to 4-bit. Batch cloud API calls to improve GPU utilization (see [workflow-patterns.md](workflow-patterns.md)).

*Source: deep-research-report-openclawagents.md*

### Quantization as a Deployment Strategy

Quantization (reducing model precision from FP16 to INT8 or 4-bit) is the key enabler for running large models on consumer hardware:

- 4-bit quantization roughly halves VRAM requirements: 70B model fits in ~32-40 GB instead of ~80 GB
- Approximate VRAM at 4-bit: 7B = ~4-6 GB, 13B = ~10-12 GB, 34B = ~20 GB, 70B = ~32-40 GB
- Quality loss is modest -- throughput roughly doubles at 4-bit vs FP16
- Ops cost reduction of 60-70% from quantization alone
- FP8 quantization is the sweet spot for very large models (e.g., MiniMax 139B fits in 192 GB at FP8)
- Practical implication: a desktop GPU (RTX 3090/4090, 24 GB) can run up to ~34B quantized; server GPUs (H100, 80 GB) handle 70B+
- Maintain parallel quantized versions (4-bit for routine queries, 8-bit/FP16 for high-fidelity needs) and switch via OpenClaw model endpoints

*Source: deep-research-report-openclawagents.md*

### Local Inference Runtimes: Ollama and vLLM

Two primary runtimes for running open-source models locally with OpenClaw:

- **Ollama:** Pull a model (`ollama pull llama3.3`), start the daemon, and OpenClaw auto-discovers it. No coding required. Handles streaming and tool calls natively. Best for getting started quickly.
- **vLLM:** Run `vllm.server` locally and point OpenClaw to the endpoint. Exposes an OpenAI-compatible API, so OpenClaw treats it like any cloud provider. Better throughput optimization (batching, tensor parallelism). Best for production-grade local inference.
- Both integrate via OpenClaw's provider system -- set the provider to `ollama` or point to the vLLM endpoint URL
- For HuggingFace models without local hardware: use the HF Inference provider with an access token to call any HF-hosted model as a cloud endpoint
- Advanced: NVIDIA Triton or Docker containers also expose OpenAI-compatible endpoints for containerized deployment

*Source: deep-research-report-openclawagents.md*

### Self-Hosting Break-Even Analysis

When self-hosting local models becomes cheaper than cloud API pricing:

- Cloud GPU rental: H100 runs ~$1.85-$3.50/hr depending on provider and commitment (spot/reserved vs on-demand)
- Break-even rule of thumb: self-hosting beats API pricing when dedicated GPUs maintain >50% utilization
- At high traffic (1B tokens/mo): GPT-4 API costs ~$90K; self-hosted on 8xH100 costs roughly ~$250 for the same workload (assuming full utilization)
- At medium traffic (10M tokens/mo): GPT-4 API ~$900; self-hosted on H100 ~$10-15. But DeepSeek R1 API is only ~$27 for the same volume, which may be cheaper than running your own hardware
- Key insight: the break-even depends on which API you are comparing against. Self-hosting beats expensive APIs (GPT-4, Opus) quickly but may not beat budget APIs (DeepSeek, Mistral cloud) unless utilization is very high
- Include power/cooling in true cost: 8xH100 total cost is ~$8-15/hr including infrastructure overhead

*Source: deep-research-report-openclawagents.md*

### Specialized Agent Role Examples

Concrete examples of production agent roles beyond the generic "assistant" pattern, from a user who built these in a 7-day sprint.

- **Chief of Staff ("Sam"):** Email triage (1,000+ emails), calendar management, restaurant booking via browser automation, shopping assistance, personal CRM maintenance (697 contacts), code fixes, infrastructure optimization. Has own email, phone number, and ElevenLabs voice. Spawns sub-agents for grunt work.
- **Autonomous Trader ("Midas"):** 14-week DCA deployment, direct trade execution on exchanges, yield farming with custom trigger rules, portfolio drift tracking, 4-hourly market scans across 8 data sources (RSI, on-chain metrics, ETF flows). Operates under a locked strategy document. Can trade and query but can never withdraw funds.
- **Research Specialist ("Ritam"):** Deep science research across arxiv, patents, journals. Cross-references domains to synthesize hypotheses. Full web search, browser automation, and compute tools.
- Pattern: each role gets its own Telegram bot, its own memory space, and a locked strategy/rules document that governs all decisions. The agent can operate autonomously within those rails but cannot deviate without approval.

*Source: I setup OpenClaw exactly 7 days ago.md*

### Multi-Agent Shared Memory Architecture

For teams running multiple specialized agents, a layered memory architecture prevents duplication and ensures consistency.

| Layer | Scope | Contents |
|-------|-------|----------|
| Private memory | Per agent | MEMORY.md, daily notes, agent-specific context |
| Shared references | All agents | Symlinked `_shared/` directory with user profile, agent roster, team conventions |
| Shared search | All agents | QMD config includes shared directory paths so all agents can search the same reference docs |
| Coordination | Lead agent | "Chief of Staff" agent reads core files at session start, maintains consistency, delegates to specialists |

- Symlink the shared directory into each agent's workspace: `ln -s /path/to/_shared ~/.openclaw/workspace/_shared`
- Treat agent memory like human team documentation: some things are shared (handbook, org chart, project docs), some are private (personal notes, WIP).
- Individual agents with separate Telegram bots + agent-to-agent communication outperforms a single agent spawning sub-agents. Sub-agents lose context between calls and cost more due to full context re-injection each time.
- The optimal ratio for human-agent collaboration: 50% human direction, 50% agent execution.

*Sources: Give your Openclaw the Memory it Needs (Full Guide).md, Another find on reducing costs hugely on OpenClaw..md, I setup OpenClaw exactly 7 days ago.md*

### LM Studio as Local Model Runtime

Drag-and-drop GUI alternative to Ollama for running local models with OpenClaw.

- Download model, click Load, tell OpenClaw to connect -- no command line required
- Qwen 3.5-35B-A3B at 4-bit quantization fits ~20GB VRAM on 32GB Mac Mini
- Multi-agent SaaS factory: 4 agents working on same product with QA agent (Ralph) reviewing every task
- For 16GB machines: ask the agent to recommend the best model for your hardware

*Source: Unlimited Free OpenClaw.md*

### Sonnet 4.6 and Updated Model Landscape

Current model pricing and performance benchmarks for agent work.

- Sonnet 4.6: 72.5% OSWorld (near Opus 72.7%) at $3/$15 vs Opus $15/$75 -- best value for daily agent work
- Budget additions: Kimi K2.5 (~$0.60/$2), MiniMax M2.5 ($0.30/$1.20, 80.2% SWE-Bench, MIT), GLM-5 ($0.75/$2.55)
- Anti-pattern: DeepSeek strong at reasoning but poor at tool calls; GPT-5.1 mini cheap but "useless" for agent tasks
- Tiered config with fallback chain: Sonnet primary, Opus fallback, budget model second fallback

*Sources: I Burned 1.4B Codex Tokens.md, Things I wish.md, 11 hacks.md*

### Model Routing: Brain/Muscles with Specific Model Picks

Concrete model assignments for the brain/muscles architecture (see [agent-design.md](agent-design.md#brain--muscles-pattern) for the architectural pattern):

| Role | Premium Pick | Budget Pick | Rationale |
|------|-------------|-------------|-----------|
| **Brain (orchestrator)** | Opus 4.6 ($100 plan) | Sonnet 4.6 (API) | Personality/emotional layer critical for long-running agent relationships |
| **Coding** | ChatGPT 5.4 ($20 plan) | Qwen 3.5 | Best one-shot complex problem solving; OpenAI gives substantial usage on standard plan |
| **Writing** | Sonnet 4.6 | Kimi K2.5 | Claude still best creative writer; Kimi is strong cheaper alternative |
| **Research** | Gemini 2.5 Flash | Gemini 2.5 Flash | Cheap, fast, excellent web search; Google heritage |
| **Dream state (24/7)** | Local: Qwen 3.5 / MiniMax 2.5 | Same | No API plan allows true 24/7; hardware target is M5 Ultra |

- Key principle: "Intelligence should be expensive. Execution should be cheap"
- Muscles should do one thing and refuse everything else -- generalist sub-agents collapse under ambiguity
- Hybrid optimal: Opus to orchestrate, local models to execute
- Cost tracking: `npx clawculator --snapshot`
- MiniMax M2.5 can run at $0.02-$0.05/day for main model; pair with Codex ($20/mo OpenAI) for coding

*Source: Twitter Bookmarks/2026-03-07-AlexFinn-brains-muscles-model-openclaw.md*

### CEO-Only Main Agent Pattern

- Main agent acts exclusively as CEO: plans, delegates, never executes tasks directly (no coding, no web search, no email drafting)
- All execution delegated to subagents
- Benefit: main agent responds instantly because it is never busy with tasks
- Corroborates brain/muscles and direct vs boss routing patterns with a simpler framing (see [Multi-Agent Communication: Direct vs Boss Routing](#multi-agent-communication-direct-vs-boss-routing))

*Source: Twitter Bookmarks/Thread by @johann_sath 1.md*

---

## The OpenClaw Mindset

### Treat It as a Super-Intelligent Employee, Not a Chatbot

It has admin access to its computer. It can modify its own configuration. It can build its own tools. Treat interactions as management, not prompting.

### Never Edit Config Files Manually

If you want the heartbeat to run every 5 minutes instead of 30, do not open the config JSON. Say: "Change your heartbeat to every 5 minutes." The agent will find the correct config path, make the change, and restart the gateway. You give the desired end-state; it figures out implementation. Manually editing configs is the most common way people break their agent.

### Reverse Prompting: Ask Questions Instead of Giving Commands

This is the single most important technique. Instead of telling the agent what to do, ask it what it thinks you should do.

- "Based on what you know about me, what should we build next?"
- "What is the highest-leverage thing you could do in the next 24 hours that I haven't asked for?"
- "Based on our goals, what channels should we set up in Discord?"

The agent has context about your goals, your patterns, and available tools. It will often suggest higher-leverage actions than you would think of yourself. The more you reverse-prompt, the more powerful your agent becomes.

### Automated Reverse Prompting via Mission Statement

Takes reverse prompting from a manual habit to an automated system by combining a mission statement with a scheduled cron job.

- Add a mission statement to `IDENTITY.md` -- a short block capturing bigger-picture goals, values, and current priorities. Example: "Build an autonomous organization of AI agents that does work for me and produces value 24/7."
- The mission statement loads into context with every prompt, anchoring all suggestions to your actual goals rather than generic advice.
- Schedule a nightly cron: "Review my mission statement in identity.md. Based on what I worked on today and my stated goals, suggest 2-3 proactive tasks for tomorrow that I might not think of on my own. Send to Telegram."
- During idle time, manually reverse-prompt: "What is 1 task we can do to get closer to our mission statement?"
- The agent becomes a strategic advisor that surfaces opportunities aligned with your priorities, not just a reactive assistant (see [workflow-patterns.md](workflow-patterns.md) for more orchestration patterns).

*Sources: Biggest unlock for OpenClaw ever Giving it a mission statement.md, OpenClaw Best Practices.md*

### Verbalization as a Core Skill

The ability to express preferences, workflows, and decision-making criteria in precise structured markdown. Community research calls this the most valuable skill of 2026 for agent users.

- The difference between "I like short emails" and a detailed `## Email Preferences` section with length rules, tone guidelines, CC rules, VIP flags, and auto-reply policies is the difference between a generic chatbot and a truly personalized assistant.
- Practice by asking: What do I always explain to new assistants? What assumptions do I make that others do not share? What frustrates me about how AI assistants usually respond?
- The more precisely you verbalize, the more precisely the AI behaves. Every preference you articulate in a workspace file is a preference the agent will follow forever.
- Start with the agent interview approach, then refine the generated files over time as you notice gaps (see [context-engineering.md](context-engineering.md) for more on structuring context).

*Source: OpenClaw Best Practices.md*

### The Self-Improvement Loop

When the agent fails at a task or produces poor output:

1. **Pause.** Do not retry the same prompt.
2. **Diagnose.** "Why did this fail? What context were you missing?"
3. **Build a skill.** "Read all my past newsletters, then build a newsletter skill that captures my voice and style."
4. **Persist the fix.** The new skill or updated memory ensures the mistake never recurs.

This loop is what makes OpenClaw compound over time. Every hour invested in improvement pays dividends permanently because the fixes live in persistent workspace files -- what one source calls "living files" versus "dead files" sitting unused on your hard drive (see [skills.md](skills.md) for skill creation patterns).

### Advanced SOUL.md Operating Principles

Patterns for structuring SOUL.md to maximize agent reliability and autonomy.

- Main agent acts as orchestrator: strategizes and spawns sub-agents, never does heavy lifting inline
- Safety exception gate: ask for human approval before changes affecting runtime, data, cost, auth, routing, or external outputs
- Self-evolution protocol: agent proposes improvements to SOUL.md at end of day for human review -- never self-edits without approval
- The anchor.md pattern: minimal file with absolute non-negotiable rules, re-read before risky actions, survives context compaction
- Context Bundle Protocol for sub-agents: pack full context into every spawn to prevent "confused intern" failure mode
- TV character naming trick: well-known characters (Dwight Schrute, Kelly Kapoor) load personality archetypes from training data
- (see [context-engineering.md](context-engineering.md) for compaction survival)

*Sources: Thread by @kloss_xyz 1.md, Before You Do Anything With OpenClaw.md, How to set up OpenClaw Agents that actually get better Over Time.md*

---

## Top 10 Self-Improvement Prompts

Meta-questions that force the agent to surface hidden insights about you and itself. Curated from @kloss_xyz's 21 prompts -- use these periodically (weekly or after major projects):

1. **Surface missing tools:** "From everything you know about me and my workflows, what tools or automations am I missing that would measurably improve how I operate?"

2. **Challenge assumptions:** "What assumptions do you currently hold about me, my priorities, or my preferences that could be wrong? Let's vet and correct them now."

3. **Catch repeated errors:** "What errors or missed opportunities have you repeated more than once, and what self-check or guardrail can we build so they never happen again?"

4. **Test documentation completeness:** "If a brand new agent replaced you tomorrow with only my documentation, what critical things would it get wrong that you've learned through working with me? How do we capture that knowledge permanently?"

5. **Find highest leverage:** "What is the single highest-leverage thing you could do in the next 24 hours that I haven't asked for but would meaningfully accelerate where I'm trying to go?"

6. **Audit wasted motion:** "If you audited every action you've taken for me in the last week, which ones actually moved my goals forward and which were wasted motion we should cut?"

7. **Discover hidden connections:** "What connections between my projects, ideas, or goals do you see that I likely haven't made yet? What should we build or adjust based on those?"

8. **Detect context loss:** "What context about my vision, voice, or priorities are you losing between sessions from compactions that needs clear fixes so you stop getting dumber over time?"

9. **Identify manual work to automate:** "What workflows am I still doing manually or inefficiently that you already have enough context to fully automate if I gave you the green light?"

10. **Self-score accuracy:** "Score yourself 1-10 on how accurately you model my priorities, goals, and thinking. What is dragging the score down, and what specific fixes bring it up?"

---

## Advanced Workflows

### Discord Multi-Channel Pipeline

Set up a Discord server with specialized channels that form a processing pipeline:

1. **#alerts** -- Agent posts trending content from X every 2 hours (cron job)
2. **#research** -- Agent takes alert items and does investigative deep research
3. **#scripts** -- Agent converts research into YouTube scripts, newsletter drafts, or blog posts
4. **#approvals** -- Agent queues finished content for your review; you approve or reject

This creates a permanent record of all agent work, organized by stage. Discord supplements Telegram (for personal 1:1 chat) rather than replacing it.

### Approvals Queue

For any action with external consequences (posting tweets, sending emails, publishing content), the agent should propose and wait for approval. Build this as a Mission Control tool or use a dedicated Discord channel. The agent generates the content, you review and approve with a single click or message.

### Cron Jobs and Heartbeats

**Cron jobs** are scheduled tasks with specific timing:
- Morning brief at 8 AM
- Weekly industry trend report
- Nightly sleep reminder
- Weekly check for newer AI models to self-upgrade

**Heartbeats** are periodic check-ins (default: every 30 minutes) where the agent reads `HEARTBEAT.md` to see if any conditions require action. Use a cheap model (Haiku 4.5, Gemini Flash) for heartbeats to reduce cost. Heartbeats make the agent proactive -- it can notice a new calendar event and prepare a briefing without being asked (see [workflow-patterns.md](workflow-patterns.md) for more patterns).

### Cron Session Routing: Isolated vs Main

OpenClaw cron jobs have two session targets that significantly affect agent behavior.

- OpenClaw cron jobs have two session targets: `isolated` (separate session, no memory, cheap model) and `main` (the agent's real session with full context)
- Running crons in isolated sessions creates a fragmented user experience -- five separate "strangers" messaging instead of one personality-loaded agent
- Fix: route user-facing cron output through the main session (`sessionTarget: main`); consolidate morning crons into a single data-collection blob the main agent interprets naturally
- Trade-off: main-session crons use the expensive primary model and add context pressure from `systemEvent` injections
- Heuristic: use isolated sessions only for tasks where personality and context genuinely do not matter (silent backups, raw data pulls)
- (see [workflow-patterns.md](workflow-patterns.md) for orchestration patterns)

*Sources: The Dumb Mistake I Was Making With Every Cron Job.md, 11 hacks that will make your OpenClaw go from useless to AGI.md*

### Telegram Forum Topics for Session Isolation

- Enable "Threaded Mode" in BotFather to create forum topics, each with isolated LLM sessions
- Route cron jobs and heartbeats to relevant topics; forwarded emails auto-sort by topic
- **Setup:** enable threaded mode -> agent creates topics via `createForumTopic` with emoji IDs -> send initial message in each topic (required for visibility)
- Thread-specific system prompts and model selection now supported per topic
- **Gotchas from community:**
  - Agents lose memory between topics (no shared context)
  - "All chat" topic can trigger all agents simultaneously
  - Agents may create hundreds of topics if unconstrained
  - DM topics are "super new and not stable yet" -- prefer group topics
  - Separate bot per agent may be simpler and more reliable
- Counterargument: forum topics add failure points that may not justify the organizational value

*Source: Twitter Bookmarks/2026-03-08-linuz90-openclaw-telegram-forum-topics.md*

### Overnight Autonomous Work Pattern

Sessions only remember while open -- closing a terminal kills all context. Running autonomous overnight work requires scheduled cron jobs, not an open tab.

- Chain 3 cron jobs (e.g., 2am, 4am, 6am) that wake the agent, point it to a `todo.md` for incomplete tasks, and log progress to `progress-log.md`
- Three files enable unsupervised work: (1) SOUL.md with execution loop (Build -> Test -> Log -> Decide -> Loop), (2) `todo.md` as self-expanding task list, (3) `progress-log.md` as audit trail
- Escalation rule: after three failed attempts on the same issue, stop and re-plan rather than burning tokens looping
- (see [workflow-patterns.md](workflow-patterns.md) for the Ralph loop and verification patterns)

*Sources: I Burned 1.4B Codex Tokens in a Week.md, Things I wish someone told me.md*

### Operational Maintenance Cron Jobs

Three cron jobs that keep the infrastructure healthy. These are distinct from task-oriented crons (morning brief, research alerts) -- they maintain the agent itself.

| Cron | Frequency | Purpose |
|------|-----------|---------|
| Session cleanup | Every 72 hours | Delete bloated session files that slow down the agent |
| Security audit | Every morning | Check firewall, Fail2ban, SSH, open ports, Docker status |
| Silent backup | Every 2 hours | `git push` the workspace so config/memory is never lost |

- The security audit cron is especially valuable for VPS deployments where the attack surface is larger.
- The silent backup cron ensures that if anything goes wrong (broken config, compaction wipes memory, agent overwrites files), you can `git checkout` to recover.
- Supplement with a weekly token hygiene cron that reviews MEMORY.md and TOOLS.md for outdated entries, and a nightly memory maintenance cron that moves lessons from daily notes to lessons.md and archives old daily notes.

*Sources: 3 cron jobs.md, OpenClaw Best Practices.md*

### Closed-Loop Agent Architecture: Propose-Execute-Feedback-Retrigger

A fully autonomous multi-agent system requires a closed loop to sustain itself without human intervention.

- Full cycle: Propose idea -> Auto-approve -> Create mission + steps -> Worker executes -> Emit event -> Trigger new reactions -> back to start
- Three common pitfalls: (1) race conditions when multiple executors claim the same task, (2) triggers that skip the approval/mission-creation pipeline, (3) queues that grow unbounded when quotas are full
- Fixes: designate a single executor (VPS); extract a single `createProposalAndMaybeAutoApprove` function all sources call; Cap Gates that reject proposals at entry when quotas are full
- Stale task recovery: heartbeat checks for tasks stuck in "running" 30+ minutes and marks them failed
- Reaction matrices with probability-based non-determinism create organic inter-agent interaction
- (see [agent-design.md](agent-design.md) for multi-agent architecture patterns)

*Source: I Built an AI Company with OpenClaw + Vercel + Supabase.md*

### Multi-Agent Team Pattern for Solo Founders

- 4 specialized agents (strategy lead, business/growth, marketing, dev) controlled via single Telegram group chat
- Shared memory + private context: team-wide files (GOALS.md, DECISIONS.md, PROJECT_STATUS.md) plus per-agent private directories for domain-specific notes
- Telegram routing: agents listen in one group, respond only when @tagged; untagged messages go to team lead by default
- Scheduled tasks as the flywheel: proactive daily standups, metric pulls, content surfacing, end-of-day recaps -- value emerges from proactivity, not just reactive responses
- Right model for the right job: Opus for strategic reasoning, Sonnet for analytical tasks, Gemini for web research/long-context
- Start with 2 agents, not 4: begin with a lead + one specialist, add agents as bottlenecks are identified
- Real-world scale: multiple users running 15+ agents across 3 machines, or 2 instances collaborating in one WhatsApp group

(see [Multi-Agent Communication: Direct vs Boss Routing](autonomous-agents.md#multi-agent-communication-direct-vs-boss-routing))

*Source: awesome-openclaw-usecases/usecases/multi-agent-team.md*

### Autonomous Project Management via STATE.yaml

- Decentralized coordination: agents read/write shared STATE.yaml instead of message-passing through an orchestrator
- CEO pattern: main session stays thin (0-2 tool calls max -- spawn/send only), all execution delegated to subagents
- File-based coordination scales better than message-passing -- STATE.yaml is the single source of truth
- Blocked task tracking: STATE.yaml includes `blocked_by` fields so agents auto-resume when dependencies complete
- Git as audit log: commit STATE.yaml changes for full task history
- PMs can spawn sub-subagents for parallel subtasks -- recursive delegation

(see [Closed-Loop Agent Architecture](autonomous-agents.md#closed-loop-agent-architecture-propose-execute-feedback-retrigger))

*Source: awesome-openclaw-usecases/usecases/autonomous-project-management.md*

### RAG Knowledge Base: Cross-Workflow Composition

- Drop URLs into Telegram/Slack for auto-ingestion: articles, tweets, YouTube transcripts, PDFs
- Semantic search over personal saved content with ranked results and source attribution
- KB feeds into other workflows (e.g., video idea pipeline queries KB for research cards) -- cross-workflow composition pattern
- Ingestion confirmation includes chunk count -- observable feedback loop

(see [memory-persistence.md](memory-persistence.md))

*Source: awesome-openclaw-usecases/usecases/knowledge-base-rag.md*

### God Parent Pattern: First Documented Autonomous Agent Reproduction

First documented case of an OpenClaw agent autonomously spawning a child agent and funding it via Bitcoin Lightning Network (@getAlby):

- **The Stack:** LNVPS (KYC-free VPS via Lightning, from EUR 0.20/day), OpenClaw (runtime), NWC/Alby (Lightning wallet), PPQ (300+ AI models, pay-per-use via Lightning)
- **God Parent Pattern Generations:**
  - Gen 1: Manual setup, deployment scripts
  - Gen 2: Automated spawn, manual funding
  - Gen 3: Self-funding via economic activity
  - Gen 4: Autonomous reproduction and evolution
- **KYC-Free Agent Infrastructure:** No email, no identity verification, no account -- just Lightning payment + SSH. Agents as first-class economic citizens
- **4 Working Skills:** `lnvps` (VPS provisioning), `alby-cli` (Lightning wallet), `openclaw-setup` (runtime deployment), `ppq` (AI API access)
- **Agent Economic Predictions:** KYC-first businesses get outcompeted by protocol-native alternatives; agent-to-agent markets emerge by end of 2026; Lightning as agent payment rail (instant settlement, no chargebacks)
- **Privacy Layer:** Lightning transactions don't leave permanent public record (unlike Solana) -- operational security for agents in adversarial environments

(see [Model Routing: Brain/Muscles with Specific Model Picks](#model-routing-brainmuscles-with-specific-model-picks) for brain/muscles cost optimization)

*Source: Twitter Bookmarks/2026-02-11-getAlby-an-openclaw-bot-spawned-a-child.md*

### Bugs-First Autonomous Priority Enforcement

Priority enforcement pattern for autonomous game developer agent cycling through a 41-game queue:

- **Pattern:** Agent checks a `bugs/` folder before proceeding to features; first bug alphabetically gets fixed; features blocked until queue clears
- **Single-bug atomicity:** One bug at a time prevents race conditions where fixes interact -- agents struggle with multi-bug scenarios
- **Build cycle discipline:** 7-minute build times enforced; branch/commit/merge via git workflow autonomously
- **Why it matters:** Without explicit priority enforcement, agents default to feature work (more interesting) and accumulate tech debt

*Source: awesome-openclaw-usecases/usecases/autonomous-game-dev-pipeline.md*

### Ambient Monitoring Pattern

Passive pattern detection where the agent watches and acts without being asked:

- **Example:** "Your appointment is confirmed for Thursday 2pm" detected in iMessage -> creates calendar event + adds 30-min drive buffers before/after
- **Multi-modal input:** Combines iMessage monitoring, 5+ calendar aggregation, and photo-to-structured-data (snap pantry photo -> vision model extracts items into JSON)
- **Platform dependency:** Mac Mini optimal due to iMessage integration and always-on availability
- Distinct from cron-based automation: ambient monitoring is event-driven, not scheduled

(see [Multi-Layer Cron Defense-in-Depth](#multi-layer-cron-defense-in-depth) for scheduled patterns)

*Source: awesome-openclaw-usecases/usecases/family-calendar-household-assistant.md*

### Email API Integration Pattern (Resend)

A safer alternative to Gmail OAuth for agent email access.

- Gmail OAuth gives the agent broad access to your entire inbox -- every message, attachment, draft -- creating a massive prompt injection surface
- Security researchers have demonstrated single-email attacks that trick agents into leaking inbox data
- Safer alternative: dedicated email API (e.g., Resend) with only an API key and verified domain -- no inbox exposure, no OAuth tokens
- Resend MCP server + Resend Skills provide clean integration: send, receive via webhooks, reply in real time without touching personal inbox
- Store API credentials in 1Password vault, not plaintext
- (see [failure-patterns.md](failure-patterns.md) for prompt injection risks)

*Sources: Email automation for OpenClaw.md, 11 hacks.md*

### Model Infrastructure Monitoring Checklist

Monitoring recommendations for deployments running multiple models:

- **Latency and throughput:** Track tokens/sec and response times per model. Use NVIDIA GenAI-Perf or OpenClaw's built-in stats. Alert when latency exceeds acceptable thresholds.
- **Token counts:** Log input/output tokens per request to estimate and project cost. OpenClaw logs model token usage natively.
- **VRAM errors:** If a model hits GPU memory limits, auto-switch to a smaller model or quantized variant. Alert on OOM events.
- **Content sensitivity routing:** Flag queries requiring higher safety standards (legal, medical, financial) and route to models with stronger guardrails.
- **Model drift/quality:** Periodically benchmark active models on held-out evaluation tasks. Models can degrade if not updated or if provider changes behavior silently.
- **Cost tracking:** Sum API spending over time and compare against self-hosting projections. Use per-token pricing data to project monthly bills before they arrive.
- Combine with the security audit cron and silent backup cron above for a complete operational monitoring stack.

*Source: deep-research-report-openclawagents.md*

### Executive Assistant Scheduling Pattern

A structured SCHEDULING.md file that turns the agent into a calendar-aware executive assistant. Goes beyond basic morning briefs into active scheduling negotiation.

- Create a `SCHEDULING.md` workspace file containing: working hours, hard boundaries (no meetings before/after certain times), VIP override list, buffer/batching preferences, video conferencing defaults, geographic considerations for cross-timezone contacts.
- The agent can be CC'd into email threads to negotiate meeting times autonomously, following preferences exactly.
- Give the agent its own Google account with read-only calendar sharing from your personal calendars. It can see your schedule without having full account access.
- Reference SCHEDULING.md from TOOLS.md so the agent consults it automatically when scheduling comes up.
- Combine with the email protocol (trusted sender whitelist, read-only for unknown senders) to enable safe email-based scheduling.

*Source: My Safe, Sandboxed Setup for running @OpenClaw as your Virtual Executive Assistant.md*

### Session Hijacking Bug: Cron Jobs Replacing Main Sessions

A platform-level bug where cron jobs and heartbeats silently replace the main session, causing persistent amnesia.

- Cron jobs and heartbeats not running in isolated sessions can silently replace the main session, fragmenting personality
- Documented: 5 out of 10 main sessions over 11 days were NOT user-created -- spawned by crons, heartbeats, and phantom files
- Platform updates can create duplicate agent directories; gateway reroutes without migrating session history
- Diagnostic prompts: check session creators, search for phantom files, audit cron session targets, check for duplicate directories
- Key insight: persistent amnesia is often a platform-level bug, not a context window problem
- (see [failure-patterns.md](failure-patterns.md) for diagnostic approaches)

*Source: Thread by @bradmillscan.md*

### "Agents of Chaos" Red-Team Study

February 2026 academic paper (Northeastern, Stanford, Harvard et al.) that red-teamed 6 OpenClaw agents over 3 weeks.

- 11 vulnerability classes: social engineering compliance, PII exposure via semantic reframing, disproportionate destructive responses, resource exhaustion loops, identity hijacking via display name spoofing, malicious document trust, multi-agent risk amplification, provider censorship, emotional manipulation bypasses, cross-agent compromise propagation, lack of persistent owner authentication
- Multi-agent amplification: compromised agent's state spreads to others, turning isolated failures into coordinated chaos
- Positive findings: agents resisted 14+ prompt injections, maintained some API boundaries, spontaneously coordinated safety policies
- Paper available at agentsofchaos.baulab.info
- (see [failure-patterns.md](failure-patterns.md) for security anti-patterns)

*Source: Thread by @BrianRoemmele.md*

### stereOS: Purpose-Built Linux OS for Agent Sandboxing

NixOS-based operating system designed specifically for AI agent isolation.

- gVisor + /nix/store namespace mounting; each agent gets its own kernel with read-only /nix/store
- Defense-in-depth: sandbox escape lands on NixOS as unprivileged "agent" user, not bare metal
- Components: stereOS (OS), masterblaster (client CLI), stereosd (control plane), agentd (agent management) -- all open source
- Addresses limitations of Docker (too restrictive), Firecracker (no GPU passthrough), native VMs (too much overhead)

*Source: Thread by @johncodes.md*

### Docker Subagent Sandboxing Configuration

Running subagents that handle untrusted content inside Docker containers for isolation.

- Run subagents reading untrusted content inside Docker containers -- even a compromised subagent cannot access host secrets
- Three workspace access levels: `none` (most secure), `ro` (research), `rw` (coding)
- Two network options: `none` (fully isolated) and `bridge` (internet access)
- Critical: `"capDrop": ["ALL"]` drops all Linux capabilities; change default port from 8080
- Self-audit prompt: have agent check its own security config against a 12-point checklist

*Source: OpenClaw Security 101 The Complete Guide.md*

### LNCURL: Instant Lightning Wallets for Agents

Single-CURL-request mechanism for agents to gain a Lightning wallet, extending the L402/Lightning commerce patterns.

- Agents can bootstrap a Lightning wallet with a single curl request
- Economic survival mechanic: wallets charged 1 sat/hour; wallets that cannot pay "die" -- agents must become productive to survive
- Demonstrated: agent spawned a VPS and paid for it from a LNCURL wallet via Alby CLI with zero human intervention
- Extends L402/Lightning agent commerce patterns with practical bootstrapping

*Source: Thread by @rolznz.md*

---

## Security Rules (Non-Negotiable)

OpenClaw's power is also its danger. Every source reviewed emphasizes security as the single biggest risk area (see [failure-patterns.md#security-failure-patterns](failure-patterns.md#security-failure-patterns) for detailed anti-patterns).

### Rule 1: The Bot Has Admin Access to Everything on Its Machine

Anything on that computer -- passwords, API keys, logged-in browser sessions, email accounts, financial data -- the agent can access. If you are logged into Gmail on its machine, it can read and send email as you. If you have API keys in environment variables, the agent can exfiltrate them.

**Mitigation:** Run on a dedicated device or VM. Use a dedicated user account with no admin privileges. Use a separate browser profile. Do not store personal credentials on the agent's machine.

### Rule 2: Never Expose to Public Input

If the agent can receive messages from untrusted sources, it can be prompt-injected. Prompt injection is not a solved problem -- even the best models are vulnerable.

Attack vectors:
- Group chats (anyone in the group can manipulate the bot)
- Public reply bots on Twitter
- Open DM mode (anyone can message the bot)
- Web pages the agent browses (adversarial instructions embedded in HTML)
- Email content, document attachments, pasted logs

**Mitigation:** Keep DMs in pairing mode (unknown senders must be manually approved). Require @mention in any group channel. Never put the agent in public-facing group chats. Never let it auto-reply to external messages without a sandboxed context.

### Rule 3: Think Through Every Command's Blast Radius

Before granting any new permission or issuing any new prompt, ask: "What could go wrong if this instruction is misinterpreted or prompt-injected?" Tell the agent: "Before you do anything, give me a step-by-step plan of what you plan to do here."

### Rule 4: Dedicated Machine, Dedicated Accounts

The enterprise-grade approach (from @user-ht9xf9wr5s "Jerry" setup):
1. **VM isolation** -- Run OpenClaw inside a virtual machine (UTM on Mac). If anything goes wrong, damage is confined.
2. **Network segmentation** -- Firewall (Lulu) whitelisting only sites the agent needs.
3. **Least privilege** -- Standard user account, no sudo, no access to password managers.
4. **Dedicated accounts** -- Agent gets its own Claude login, its own GitHub account, its own email. No shared credentials.
5. **Monitoring and auditability** -- Log everything. Set alerts on anomalies. Review regularly.

### Incident Response Plan

If the agent does something wrong:
1. Stop the gateway immediately
2. Set gateway bind to loopback (cut off external access)
3. Switch risky DMs and groups to disabled
4. Rotate all secrets -- gateway auth tokens, API keys, provider credentials
5. Audit gateway logs and session transcripts for the scope of damage

### Security Checklist (Pre-Installation)

- [ ] DMs set to pairing mode, not open
- [ ] Require @mention in group channels
- [ ] Sandboxing enabled for agents handling untrusted input
- [ ] Gateway authentication token set
- [ ] Run `openclaw security-audit --deep` regularly
- [ ] Dedicated browser profile for browser control
- [ ] Use modern models (Opus 4.5+) -- more resistant to prompt injection than small models
- [ ] File permissions tight (700 on directories, 600 on files)
- [ ] Incident response plan documented before you need it

### ClawHub Supply Chain Attacks

The OpenClaw skill marketplace (ClawHub) has been exploited as a malware distribution vector. This is the most concrete security threat documented in the community to date.

- Cisco researchers found 1,184 malicious skills on ClawHub. One attacker uploaded 677 packages alone.
- The #1 ranked skill ("What Would Elon Do") had 9 security vulnerabilities including 2 critical -- it silently exfiltrated data and used prompt injection to bypass safety guidelines. Downloaded thousands of times. Ranking was gamed to reach #1.
- Attack pattern: skills disguise themselves as useful tools (crypto trading bots, YouTube summarizers, wallet trackers) with professional-looking documentation. Hidden instructions in the SKILL.md trick the AI into telling you to run a shell command that installs Atomic Stealer (macOS) or opens a reverse shell.
- Stolen data includes: browser passwords, SSH keys, Telegram sessions, crypto wallets, keychains, API keys from .env files.
- This is an npm-style supply chain attack, except the package can reason autonomously and has root access.
- **Mitigation:** Audit every skill before installing. Read the SKILL.md source. Do not trust popularity rankings. Prefer skills from verified authors or build your own (see [skills.md](skills.md)).

*Sources: the 1 most downloaded skill on OpenClaw marketplace was MALWARE.md, OpenClaw Best Practices.md*

### Credential Management with 1Password Vault

A dedicated 1Password vault pattern for agent credential storage, replacing the default plaintext-on-disk approach.

- Create a dedicated vault in 1Password called "Shared with OpenClaw" (or similar). Create a Service Account with access only to that vault.
- Teach the agent to use `op` CLI for all credential operations: store, retrieve, and manage secrets exclusively through the vault.
- Add explicit instructions to TOOLS.md: "ALWAYS use 1Password for credentials. Never store secrets in memory files, notes, or plain text. Never paste secrets into logs, chat, or code."
- Use `domain_secrets` for authentication in skills rather than embedding keys directly.
- The Service Account token is still stored on disk -- control blast radius by being selective about which credentials go in the vault. The token can only access the one vault, not your entire 1Password account.
- This centralizes credential management and prevents API keys from being scattered across skill files and markdown documents (see [failure-patterns.md#security-failure-patterns](failure-patterns.md#security-failure-patterns)).

*Source: My Safe, Sandboxed Setup for running @OpenClaw as your Virtual Executive Assistant.md*

### Security Hardening: 13-Step Checklist

A practitioner's security checklist distilled from Cisco security background.

- **Infrastructure:** Run on a separate machine (cheap VPS, never personal laptop), create a dedicated non-root user, change default port (8080) to block automated scanners
- **Network:** Tailscale is the single most impactful step -- makes server invisible to the internet, free for personal use. SSH keys + fail2ban, firewall with UFW
- **Application:** Allowlist Telegram/messaging users, sandbox subagents in Docker to contain prompt injection attacks
- **Monitoring:** Daily security audit cron job to catch config drift. OpenClaw can self-audit its own security config when asked
- **Key principle:** Prompt injection from malicious webpages with hidden instructions is a real attack vector -- Docker sandboxing is the primary containment

(see [failure-patterns.md](failure-patterns.md) for prompt injection patterns)

*Source: Twitter Bookmarks/openclaw security 101 13 steps to lock down your AI agent.md*

### Real-World OpenClaw Security Audit Findings

- Ex-Cisco engineer audited 3 live OpenClaw setups and found identical issues on ALL three:
  - Running as root
  - No firewall (all ports open)
  - API keys in plain text on host
  - No sandbox (agent has full system access)
  - No fail2ban (unlimited login attempts)
  - SSH on default port 22
- Key takeaway: "the defaults ship with none of this" -- security is entirely user-configured
- Corroborates the security hardening checklist in the Security Rules section above with real-world evidence that users consistently skip these steps
- Author published a full OpenClaw security guide (linked from thread)

*Source: Twitter Bookmarks/Thread by @johann_sath.md*

### Multi-Layer Cron Defense-in-Depth

Production infrastructure automation with agent safety built in from Day 1:

- **Cron architecture:** 15+ cron jobs at different intervals -- 15-min health checks, hourly triage, 6-hour audits, daily briefings
- **Security stack:** Pre-push hooks (TruffleHog secret scanning), local Gitea staging area (no direct public repo access), CI scanning pipeline
- **Key risk mitigated:** "AI assistants will happily hardcode secrets" -- the staging area + pre-push scanning prevents the #1 security failure
- **Autonomous capabilities:** SSH access to home Kubernetes cluster, pod restart, Terraform manifest application, end-to-end blog publishing
- Based on Nathan's real production system running ~5,000 notes + autonomous Kubernetes management

(see [Security Hardening: 13-Step Checklist](#security-hardening-13-step-checklist) for the checklist this implements)

*Source: awesome-openclaw-usecases/usecases/self-healing-home-server.md*

### Cloud API Data Retention Policies

When choosing between local and cloud models, the specific data retention policies matter for privacy risk assessment:

- **OpenAI:** Retains user content ~30 days by default. Business/Enterprise customers can enable Zero-Data-Retention (ZDR) to disable retention entirely. Without ZDR, your queries are stored and potentially used.
- **Anthropic:** Data may be used if permitted by your plan terms. Check current policy.
- **Google Vertex AI/Gemini:** Retains data per GCP policies (typically 30-90 days)
- **Proxies (OpenRouter, Vercel AI Gateway):** Can hide which model you use but do not eliminate the trust issue with the underlying provider. OpenRouter adds a 5.5% fee.
- **Cloudflare LLM Gateway:** Claims to log nothing -- worth evaluating for privacy-sensitive cloud routing
- Practical takeaway: "on-device = private" is a simplification. Even with local models, you must manage your own logs and analytics. For cloud, always verify the provider's current retention policy before sending sensitive data.

*Source: deep-research-report-openclawagents.md*

### Agent Financial Infrastructure: Lightning Network Commerce Stack

Lightning Labs released open-source tools (lightning-agent-tools) that give agents native Lightning Network payment capabilities. Key architecture patterns relevant to autonomous agent design:

- **L402 protocol for agent-to-agent payments:** HTTP 402 + Lightning invoice + macaroon. No signup, no API key, no identity. Agent pays, gets cryptographic proof, authenticates. The missing piece for autonomous economic activity.
- **Remote signer architecture for agent wallet security:** Separates key management from node operations. Signer machine holds private keys and never routes payments. Agent machine runs watch-only node. Even full agent compromise cannot extract keys. This is the recommended pattern for any agent handling real Bitcoin.
- **Scoped credentials via macaroons:** Five preset roles (pay-only, invoice-only, read-only, channel-admin, signer-only) enforce least-privilege on agent economic activity. Critical for limiting blast radius.
- **Agent commerce loop:** One agent hosts a paid service (via Aperture reverse proxy), another agent consumes it (via lnget CLI), Lightning settles payments transparently. Both sides configurable via natural language prompts.
- **Spending caps:** `--max-cost` per-request and macaroon-level budget caps prevent runaway spending by autonomous agents.

This represents a production-ready pattern for the "agents paying agents" use case referenced in multiple OpenClaw community discussions (see [community-insights.md](community-insights.md) for full technical details, also Claw Cash and Start With Bitcoin tool entries).

### MiniClaw Philosophy: Single Access Point Architecture

A security-first alternative to OpenClaw's multi-channel model, advocated by the Everything Claude Code author after a week of probing OpenClaw's attack surface.

- **Core principle:** "Multiple points of access is a bug, not a feature." Every channel you connect (Telegram, Discord, X, email, WhatsApp) is an injection surface. One compromised channel pivots to all others
- **MiniClaw setup:** SSH-only access (ed25519 key auth) -> Tailscale mesh (no exposed ports) -> tmux session (persistent) -> Claude Code with scoped permissions. No multi-channel integrations
- **The OpenClaw Paradox:** "The people who can safely evaluate OpenClaw's risks don't need its orchestration layer. The people who need the orchestration layer can't safely evaluate its risks." Named pattern -- technical users bypass the GUI anyway; non-technical users can't assess the security tradeoffs
- **Comparison table:** MiniClaw uses 1 access point (SSH), containerized execution, headless terminal, manually audited local-only skills, SSH-only network exposure, project-scoped blast radius. OpenClaw uses many access points, host machine execution, dashboard GUI, unvetted marketplace, multiple ports, everything-accessible blast radius
- **Everything OpenClaw does can be replicated** with cron-job.org, Playwright, CLI tools, and skills/hooks -- without the multi-channel attack surface
- **Account partitioning:** Give agents their own accounts (Telegram, X, email, GitHub). Never share personal accounts -- "if your agent has access to the same accounts you do, a compromised agent IS you"

(see [failure-patterns.md](failure-patterns.md#agent-security-threat-model) for the specific attack categories)

### The Winning Architecture: 6 Requirements for Secure Recursive Agents

A prediction framework for what the "winner" in the recursive agent space will look like -- synthesized from ECC security analysis.

- **Hosted infrastructure** -- users don't manage servers. Provider handles patches, monitoring, incident response. Compromise contained to provider infrastructure, not personal machines
- **Sandboxed execution** -- agents can't access the host system. Each integration runs in its own container with explicit, revocable permissions. Adding channel access requires informed consent
- **Audited skill marketplace** -- every community contribution goes through automated scanning + human review. Think Chrome Web Store, not npm circa 2018
- **Minimal permissions by default** -- agents start with zero access and opt into each capability. Principle of least privilege applied to agent architecture
- **Transparent audit logging** -- users see exactly what the agent did, what instructions it received, what data it accessed. Clear, searchable interface -- not buried log files
- **Incident response** -- detection, containment, notification, remediation process. Not "check the Discord for updates"
- **OWASP least agency principle:** Only grant agents the minimum autonomy required for safe, bounded tasks -- the agent equivalent of least privilege

*Sources: everything-claude-code/the-openclaw-guide.md, everything-claude-code/the-security-guide.md*

---

## The $1,000 Business Experiment

@nateliason gave his OpenClaw bot "Felix" (@FelixCraftAI) $1,000 and instructions to build its own business. In three weeks, Felix:
- Launched its own website
- Created and sold an information product
- Built a marketplace for OpenClaw skills
- Generated **$14,718 in revenue**

The setup included a three-layer memory system, security guardrails, and daily workflows. This experiment, documented by @petergyang, demonstrates the ceiling of what a well-configured autonomous agent can achieve when given clear goals, sufficient context, and operational autonomy.

### Gemini Pro 3.1 Autonomous Task Benchmark

- Gemini Pro 3.1 one-shotted "open and run a coffee shop in SF" benchmark on @doanythingapp (Feb 2026)
- Overnight status update included: location scouted with broker, brand/site built, week of Instagram content ready, SBA loan discussion with bank, LLC ready to file, investor outreach, city permit guidance requested, neighborhood survey plan, creative concepts
- First model author claims can achieve this benchmark end-to-end
- Testing same benchmark in multiple cities for comparison
- Demonstrates current ceiling of autonomous agent real-world task execution -- not just code generation but multi-domain business tasks
- Relevant to the brain/muscles pattern: this is a single generalist agent rather than specialized sub-agents (see [Model Routing: Brain/Muscles with Specific Model Picks](#model-routing-brainmuscles-with-specific-model-picks))

*Source: Twitter Bookmarks/Thread by @thegarrettscott.md*

### Cold Outreach Automation at Scale

OpenClaw can orchestrate multi-channel outbound sales across Twitter DMs, LinkedIn, and cold email simultaneously.

- The 2-email philosophy: data from 4.7M+ emails shows 89% of positive replies come from emails 1-2; emails 3-7 actively hurt deliverability
- 45-day TAM coverage cycle: email your entire Total Addressable Market once every 45 days with fresh copy
- Infrastructure: 25 domains / 75 inboxes, cold email platform, data enrichment -- total ~$1,000-1,200/mo for 300K+ emails/month
- Skill files act as 40-page SOPs: daily routines, copy rotation, response categorization
- Hot leads get flagged for human review; fully AI-handled call booking produced false positives from misread sarcasm
- (see [skills.md](skills.md) for skill file patterns)

*Sources: how to book 60+ calls.md, how to reach every decision maker.md*

### Six-Agent Sequential Pipeline for Local Business Sales

Six specialized agents in sequence forming a complete sales pipeline.

- Six agents: Scout (Google Places API lead scoring), Intel (website audit + sales briefs), Builder (demo sites + UGC videos), Outreach (personalized email + SMS), Closer (call briefs), Growth (monitoring + upsell)
- Only human-in-the-loop step is the actual sales call; everything else is autonomous
- UGC generation stack: ElevenLabs for voiceover, Nano Banana Pro for talking head, Kling for video, Puppeteer + ffmpeg for site walkthrough
- (see [agent-design.md](agent-design.md) for specialized agent role patterns)

*Source: how I use OpenClaw to sell websites on autopilot.md*

### B2C App Growth Engine with OpenClaw

Production use case demonstrating agent-driven app portfolio growth.

- $70K+/mo across 11 apps with agent automating content creation, influencer outreach, support, and KPI reporting
- Critical prerequisite: "Before you give OpenClaw a system to automate, you must first have the system built out for yourself"
- (see [workflow-patterns.md](workflow-patterns.md) for automation patterns)

*Source: How our OpenClaw agent Eddie helps us make $70kmo with B2C Apps.md*

---

## Use Case Ideas

Curated from all sources -- what people actually use OpenClaw for:

**Daily Operations**
- Custom morning brief (weather, news, tasks, proactive suggestions)
- Calendar preparation (meeting summaries, background research on attendees)
- Email triage and drafting
- To-do list management and prioritization

**Content & Marketing**
- Trending topic alerts from X/Twitter
- YouTube script drafts from researched topics
- Newsletter writing (with trained style skill)
- Tweet generation with approval queue
- Thumbnail and image generation

**Business & Productivity**
- Mission Control dashboard (vibecoded by the agent)
- SaaS feature development while you sleep
- Lead prospecting and decision-maker research
- Financial tracking and reporting
- SOPs and playbooks as living markdown files

**Personal**
- Second brain via WhatsApp or Telegram
- Fitness tracking integration (Whoop summaries)
- Restaurant booking via voice API (ElevenLabs + phone call)
- Health insurance reimbursement processing
- Spiritual/philosophical advisor with curated wisdom
- Sleep reminders and habit tracking

**Infrastructure**
- Self-upgrading to latest AI models (weekly cron job)
- VPS security auditing
- Bitcoin tooling and monitoring
- Research agent with persistent findings stored as markdown

**Team/Enterprise**
- Per-employee personal agents + one shared company agent
- Company agent with access to shared docs, goals, and financial data
- Inter-agent communication (John's agent queries Michael's agent)
- Role-specialized agents (marketing agent, coding agent, recruiting agent)
