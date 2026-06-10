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

*Source: Twitter-Bookmarks/Anatomy of OpenClaw a guide after which you'll build agents differently.md*

### How It Differs from Claude Code

| Dimension | Claude Code | OpenClaw |
|-----------|-------------|----------|
| Lifecycle | Session-based; dies when terminal closes | Always-on daemon; survives reboots |
| Autonomy | Requires approval for each command | Runs unsupervised; no approval loop |
| Memory | Per-project CLAUDE.md | Nine workspace files + custom folders, persistent on disk |
| Channels | Terminal only | Telegram, Discord, WhatsApp, iMessage, email, web UI |
| Proactivity | Reactive only | Heartbeats, cron jobs, autonomous task discovery |

### MaxClaw -- Hosted OpenClaw with Zero-Setup Deployment
- Hosted version of OpenClaw by MiniMax that removes the Docker/API key/server provisioning barrier entirely
- One-click deployment in under 20 seconds with support for Telegram, WhatsApp, Discord, and Slack out of the box
- Persistent memory spanning 200,000+ tokens that adapts to working style over time -- no workspace file configuration needed
- Expert 2.0 system: 10,000+ pre-built expert agents deployable with a single click, covering common use cases
- Self-hosted OpenClaw costs $25-250/month; MaxClaw bundles everything for $19/month with no additional API fees -- trades customizability for convenience
- (see [The Winning Architecture: 6 Requirements for Secure Recursive Agents](#the-winning-architecture-6-requirements-for-secure-recursive-agents) for hosted vs self-hosted tradeoffs)

*Source: 2026-03-09-godofprompt-httpstcoyxb6c4pxll.md*

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

*Source: Twitter-Bookmarks/Thread by @bramk.md*

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

*Sources: Clawdbot-aka-Openclaw/OpenClaw Too Expensive Try This Instead (97% Reduction).md, Twitter-Bookmarks/The OpenClaw Cost Optimization Playbook.md, Twitter-Bookmarks/2026-03-04-slash1sol-stop-wasting-tokens.md*

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

### Five-Step OpenClaw Setup for Maximum Effectiveness

A prioritized checklist for turning a default OpenClaw install into a proactive, goal-aligned agent (see [agent-design.md](agent-design.md) for persona and architecture patterns, [memory-persistence.md](memory-persistence.md) for memory setup):

1. **Brain dump** -- Tell your agent your interests, career, goals, ambitions, and anything personal. Without this context, the agent cannot work toward your objectives.
2. **Connect your tools** -- Ask the agent to connect to every tool you use daily; it will figure out the integration. Then create a skill for each one. Example: agent checks a todo list (Things 3) every morning and completes any tasks it can.
3. **Build a Mission Control** -- A custom NextJS hub the agent builds and maintains. When the agent lacks a tool for a task, it builds one inside Mission Control. This creates a growing internal toolset over time.
4. **Write a mission statement** -- A one-sentence north star that governs every action. Example: "An autonomous organization of AI agents that does work for me and produces value 24/7." Place it at the top of Mission Control so every task aligns with it.
5. **Make it proactive** -- Schedule the agent to run a task at a fixed time (e.g., 2am nightly) that moves one step closer to the mission statement. Without explicit proactivity expectations, the agent stays passive.

*Source: Clawdbot-aka-Openclaw/Research/Alex Finn recos.md*

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

*Source: Twitter-Bookmarks/2026-03-04-moritzkremb-openclaw-optimized-setup-guide.md*

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

*Source: Twitter-Bookmarks/This is how you actually build an AI team via OpenClaw ANTILARP.md*

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

### Full Autonomous AI Agent Setup: 18 Cron Jobs, Three-Model Stack

- Architecture: Mac Mini M4 (always-on) + Hermes Agent + Telegram bot + 18 cron jobs + 35 shell scripts + 6 custom skills + ALIVE context system
- Three-model stack by role: GLM-5 (interactive chat, tool calling), GLM-4.7 (cron jobs, cheaper), Qwen 3.5 4B via local Ollama (context compression -- keeps compression free and rate-limit-free)
- Critical failure mode: using cloud API for compression creates a death spiral -- cron jobs → context grows → compression calls API → rate limit hit → compression fails silently → sessions grow unbounded
- Session idle timeout: set to 60 minutes (not 1440-minute default); short sessions = clean context = fast responses
- Source diversity rule: explicitly specify fetch order (Techmeme → Hacker News → Reddit → web search) or the model defaults to Reddit for everything
- LaunchAgent (not cron) for auto-restart: cron lacks login credentials; LaunchAgent runs inside the user session where Claude's auth is available
(see [memory-persistence.md](memory-persistence.md) for the ALIVE context system details)
*Source: 2026-03-27-witcheer-httpstcolnsqgjjxvm.md*

### Hermes Agent Practical Setup Tips

- Nightly skill evolution: set up a cronjob to run skill optimization nightly; add a second cronjob to evaluate the changes so you don't have to manually review; critical: make it stop anything trying to game the optimization loop (prevents misaligned self-modification)
- Honcho for memory: install plastic-labs/honcho if hitting memory issues; provides cross-session recall, memory synthesis, and better long-term storage; avoids repeating same mistakes or pulling too much context
- USER.md and MEMORY.md character limits: Hermes has much smaller limits than OpenClaw; MEMORY.md: 2200 chars max; USER.md: 1375 chars max; populate and curate thoughtfully -- quality over quantity helps it learn faster
- OpenClaw → Hermes migration: expose OpenClaw agents as OpenAI-compatible endpoints; lets you run both side-by-side with zero disruption while transitioning; Hermes can call them directly, existing crons keep working
- Session timeout config: change default session timeout and expiry; especially useful for threads not used daily -- prevents agent from losing context unnecessarily
- Anti-bikeshedding rule: don't start changing your skin/configuration until agents are actually doing work; easy to spend all time on setup and go down the rabbit hole while never shipping
*Source: 2026-04-02-Rigario-many-are-running-nousresearch-hermes-agent-now-here-are-some.md*

### Personal Hermes Agent Crew (vmiss33)
@vmiss33's "what to actually use a personal AI agent for" walkthrough -- direct counter to "I installed OpenClaw and stared at it for an hour." Practical methodology: write down what you do for a day, then a week, then ask: "what took a lot of time?" and "what didn't provide value?"

- **The softer-stuff angle:** beyond model selection, look at life friction points. Things you forget to do. Things that make life harder. (Drink water reminders. Posture checks. Movement breaks.)
- **The agent crew (separate profiles per provider/model):**
  - **Tech Research Agent** -- Nous Portal, MiniMax M2.7. Used for research briefs with citations -- the agent teaches user how to do something (e.g., model quantizations) rather than doing it
  - **Tech Task Master Agent** -- ChatGPT Plus subscription via Codex (NOT API). GPT 5.5. Builds skills for Hermes; the "anything" agent
  - **Lifestyle Agent** -- OpenRouter free tier, NVIDIA Nemotron 3 Super. Reminds via Telegram (water, posture, movement)
  - **Lifestyle/Research Agent** -- LOCAL Qwen 3.5 9B quant on RTX 4070 (8GB VRAM, 64K context, llama.cpp serving). MCAS / food allergy research; recipe brainstorming
- **Provider/cost strategy:**
  - **OpenRouter free models:** put $10 in credits to unlock 1,000 req/day + 20 req/min on free models. Free account = 50 req/day (gone fast)
  - **Nous Portal $10/mo subscription** -- experimentation, includes tool calling
  - **Local models** on consumer hardware -- 8GB VRAM laptop or 16GB Mac runs Qwen 3.5 9B surprisingly well via LM Studio + Hermes
  - **ChatGPT Plus $20/mo via Codex subscription** (not API!) -- working flawlessly
  - **NVIDIA NIM** -- many free models for testing
  - **DeepSeek v4 API** -- 75% discount through end of May 2026 (subsidized)
- **Mistake most people make:** starting with the tech instead of the problem. "You don't need 3090s. Start with your life. Your workflow. Your friction points. Then build agents around that."
- (see [vmiss33's guide](https://x.com/vmiss33) for ongoing posts)

*Source: 2026-05-03-vmiss33-httpstcoosab1oa3qx.md*

---

## Brain + Muscles Architecture

The most cost-effective and capable setup separates orchestration ("brain") from execution ("muscles") (see [agent-design.md#brain-muscles-pattern](agent-design.md#brain-muscles-pattern-from-openclaw) for the general pattern).

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

Concrete model assignments for the brain/muscles architecture (see [agent-design.md](agent-design.md#brain-muscles-pattern-from-openclaw) for the architectural pattern):

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

*Source: Twitter-Bookmarks/2026-03-07-AlexFinn-brains-muscles-model-openclaw.md*

### CEO-Only Main Agent Pattern

- Main agent acts exclusively as CEO: plans, delegates, never executes tasks directly (no coding, no web search, no email drafting)
- All execution delegated to subagents
- Benefit: main agent responds instantly because it is never busy with tasks
- Corroborates brain/muscles and direct vs boss routing patterns with a simpler framing (see [Multi-Agent Communication: Direct vs Boss Routing](#multi-agent-communication-direct-vs-boss-routing))

*Source: Twitter-Bookmarks/Thread by @johann_sath 1.md*

### Two-Agent Architecture for Long-Running Projects

- Two-agent architecture: Initializer agent (sets up environment, creates feature list in JSON with pass/fail fields, initial git commit); Coding agent (one feature at a time, updates progress file and git history)
- Feature list as cognitive anchor: store in JSON not Markdown -- models are empirically less likely to inappropriately overwrite JSON vs Markdown
- Clean state requirement: every coding session ends with a git commit, progress file update, and reversion to a working state -- not a nice-to-have, a first-class constraint
- Two failure modes: (1) attempting too much without testing/documenting, (2) looking at partial progress and declaring victory -- both solved by initializer + feature list architecture
*Source: 2026-03-17-rohit4verse-httpstcoh4kcn5wwnx.md*

### Sandboxed Personal AI Coordinator with Local Models
@intangiblecoins's "Clem" pattern: a single AI assistant on Signal that coordinates a Mac Mini stack of local models, Bitcoin node, analytics DB, and Lightning wallet -- with strict data isolation.

- **Coordinator on Signal 24/7** routes queries to local models (Gemma4 26B, DeepSeek R1 32B) as appropriate; cloud APIs only when local models can't handle it
- **Strict scope isolation:** zero access to iCloud, email, contacts, or personal data; operates entirely within a sandboxed research workspace -- coordinator powerful inside its scope, blind outside
- **Tool surface:** Bitcoin node + analytics DB + Obsidian vault (2,200+ docs) + Kuzu graph + LLM wiki + Lightning wallet -- all local, all owned, all auditable
- **Why this pattern matters:** demonstrates the personal-sovereignty version of the Five-Agent Fleet pattern -- one human, one coordinator, many tools, no cloud dependency, ~$100/mo
- (see [bitcoin-ai.md](bitcoin-ai.md#personal-bitcoinai-research-infrastructure-on-mac-mini) for the full Mac Mini stack; see [agent-design.md > Five-Agent Fleet + Single Brain](agent-design.md#five-agent-fleet--single-brain-pattern-dorsey-world-model) for the team/business analog)

*Source: 2026-04-12-intangiblecoins-spent-the-last-month-building-a-personal-ai-research-infrast.md*

### LM Studio as Official OpenClaw Provider
- LM Studio (Mac/Windows/Linux local-model runner) became an official OpenClaw provider
- Onboard: `openclaw onboard --auth-choice lmstudio`
- Eliminates per-token cloud cost for OpenClaw deployments by routing brain/muscles work through local LM Studio models
- Strengthens the local-first OpenClaw stack alongside Ollama and direct GGUF setups (see [Brain + Muscles Pattern](#) and [Local Model Hybrid](#) for the cost/performance tradeoffs)

*Source: 2026-04-13-lmstudio-lm-studio-is-now-an-official-openclaw-provider-run-openclaw.md*

### Kimi K2.6 -- Long-Horizon Coding + 300-Agent Swarms
Moonshot's Kimi K2.6 release. Open-source SOTA on multiple coding/agent benchmarks: HLE w/tools 54.0, SWE-Bench Pro 58.6, SWE-bench Multilingual 76.7, BrowseComp 83.2, Toolathlon 50.0.

- **Long-horizon coding:** 4,000+ tool calls and 12+ hours of continuous execution per session, with cross-language generalization (Rust, Go, Python) and across task types (frontend, devops, perf optimization)
- **Agent swarms scaled up:** 300 parallel sub-agents × 4,000 steps per run (up from K2.5's 100 / 1,500). One prompt → 100+ files generated
- **Motion-rich frontend output:** native videos in hero sections, WebGL shaders, GSAP + Framer Motion, Three.js 3D
- **Powers OpenClaw + Hermes Agent** for 24/7 autonomous operations -- production-grade coding workflows pair K2.6 with Kimi Code
- **Claw Groups (research preview):** bring your own agents, command friends' agents, mix bots and humans in the loop
- Available in chat mode and agent mode on the Moonshot platform; weights and API both released
- Significance: open-source frontier closes faster than expected -- agent-grade open weights now match closed frontier on long-horizon coding

*Source: 2026-04-20-Kimi_Moonshot-meet-kimi-k26-advancing-open-source-coding-open-source-sota.md*

### Local LLM Cheat Sheet for 16GB Devices
@gkisokay's curated lineup of small local models for Mac Mini / personal laptop with 16GB RAM. Q4_K_M quantization unless noted. All in GGUF format.

- **Daily-use tier:**
  - **Qwen3.5 9B** -- daily driver. Chat, drafting, research, translation. "If you keep only one, keep this."
  - **DeepSeek-R1 Distill Qwen 7B** -- reasoning. Math, logic, step-by-step. Slower but worth it.
- **Specialty tier:**
  - **Qwen2.5 Coder 7B** -- code completions, refactors, debugging, repo Q&A
  - **Llama 3.1 8B** -- long context. RAG, doc chat, codebase Q&A. Output not top-tier; context strong for size.
  - **Phi-4 Mini Reasoning** -- compact thinker. Logic, structured answers, math. Smaller context.
- **Efficiency tier:**
  - **Gemma 4 E4B** -- writing, chat, light agents, structured output
  - **Phi-3.5 Mini (Q5_K_M)** -- summaries, extraction, doc chat. Pair with bigger model.
  - **Qwen3.5 2B** -- summaries, tagging, rewrites, lightweight sidekick
- **Micro tier:**
  - **Qwen3.5 0.8B (Q5_K_M)** -- classification, keyword routing, binary decisions, triage
  - **Gemma 4 E2B-it** -- lightweight chat, quick Q&A, summaries, tiny agents
- **Recommended pairings:** single = Qwen3.5 9B; two-model = Qwen3.5 9B + Qwen2.5 Coder 7B (code) OR Qwen3.5 9B + Phi-3.5 Mini (support tasks)
- (see [Brain + Muscles Pattern](#brain--muscles-pattern-from-openclaw) for how to combine these as muscles to a frontier brain)

*Source: 2026-04-21-gkisokay-the-local-llm-cheat-sheet-for-your-16gb-ram-device-i-pulled.md*

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

### clawchief: OpenClaw as Configured Operating System
- clawchief (github.com/snarktank/clawchief) is an operating layer on top of OpenClaw, not a replacement -- installs skills + workspace files that transform OpenClaw into a configured executive assistant
- HEARTBEAT.md is the proactivity engine: instructs the agent to read the priority map, auto-resolver, meeting-notes policy, live task file, and only message when something actually matters -- prevents both passivity and noise
- Single canonical task file (`clawchief/tasks.md`) is the live source of truth for the day; agent promotes due-today items and archives completions automatically; eliminates scattered context
- Private context files (AGENTS.md, SOUL.md, USER.md, IDENTITY.md, MEMORY.md) are where the template becomes personal -- tone, boundaries, business preferences, long-term memory
- TOOLS.md holds environment-specific notes (preferred email accounts, tracker quirks, local environment details, target-market notes) that should not be buried in prompts
- Cron jobs are the activation event: executive assistant sweep, daily task prep, business-development sourcing -- agent becomes dramatically more useful when it wakes itself up for recurring work
- Key principle: "Generic assistants are generic because they are under-configured. Great assistants are opinionated, specific, and deeply shaped around one person's operating reality"

(see [The Self-Improvement Loop](#the-self-improvement-loop) and [Verbalization as a Core Skill](#verbalization-as-a-core-skill) for related configuration philosophy)

*Source: 2026-04-02-ryancarson-httpstco72mblecaso.md*

### gbrain: Opinionated OpenClaw Agent Brain Configuration
- Garry Tan's personal OpenClaw/Hermes Agent brain configuration -- the behavioral and identity layer, complementary to his gstack (infrastructure layer)
- Demonstrates the pattern of separating agent identity/personality (brain) from agent capabilities/tools (stack) in the OpenClaw ecosystem
- Relevant as a real-world example of how experienced builders configure the OpenClaw agent identity layer
- GitHub: garrytan/gbrain

*Source: GitHub Stars*

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

*Source: Twitter-Bookmarks/2026-03-08-linuz90-openclaw-telegram-forum-topics.md*

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

### Production Multi-Agent Systems: Karpathy Loop and Self-Healing Crons

- Model routing slashes costs: mapping 48 automated jobs to cheapest capable model reduced API costs from $500/day to $25/day
- Multi-agent coordination via shared context directory: a "signal bus" where agents read and write to one shared folder -- no explicit orchestration needed
- Self-healing cron doctor: script running twice daily that reads every job's error log and auto-fixes pattern-matched failures
- Karpathy loop / autogrowth: one agent reviews its own performance nightly, scores experiments, and modifies its own cron instructions -- every day it gets slightly better
- Agent compounding: week 1 output is mediocre; by week 8, every correction is stored; a feedback file with 200+ entries means 200 corrections the agent will never repeat
- Practical startup: begin with 3 agents and 5 crons; run clean for a month before scaling
*Source: 2026-03-15-ericosiu-httpstcokldqwohczf.md*

### Session File Bloat: Cron Output Accumulation Anti-Pattern

- Anti-pattern: every cron job output stored in session files; months of accumulated .jsonl files load into context on every message, causing up to 95% response time slowdown
- Fix: delete old .jsonl files except the main session, then rebuild sessions.json to only reference sessions that still exist on disk
- Cron job output accumulation is invisible until performance degrades significantly -- periodic session file cleanup should be a scheduled maintenance task
- General pattern: any long-running autonomous agent with persistent session storage will accumulate stale context unless it has an explicit cleanup mechanism
*Source: 2026-03-19-sharbel-ran-this-on-mine-this-morning-my-openclaw-had-been-getting-s.md*

### Cloud-Scheduled Tasks: Decoupling Agent Execution from Local Machine

- Claude Code supports cloud-based scheduled recurring tasks: set a repo, a schedule, and a prompt; executes via cloud infrastructure on schedule
- Decouples agent execution from local machine uptime -- enables true overnight/asynchronous autonomous operation without leaving a laptop running
*Source: 2026-03-20-noahzweben-you-can-now-schedule-recurring-cloud-based-tasks-on-claude-c.md*

### Autonomous Overnight Research Loop

- Core loop: read context → modify code → run timed experiment → evaluate metric → keep or revert → repeat indefinitely without stopping for human input
- "NEVER STOP" directive: once started, the agent runs until manually interrupted; no confirmation gates inside the loop
- Fixed time budget per experiment (e.g., 5 minutes) makes all runs platform-comparable; enables ~100 experiments per human sleep cycle
- Single metric + single editable file + single immutable harness is the scoping pattern that makes autonomous iteration safe and reviewable
- Results logged to a separate untracked TSV; git commits act as experiment checkpoints: `keep` = advance branch, `discard` = git reset
- Simplicity criterion: a small improvement that adds ugly complexity is a discard; removing code to get equal performance is a keep
- Crash handling: fix typos and re-run; abandon fundamentally broken ideas; record `crash` status and move on
*Source: autoresearch/README.md*

---

### program.md as Lightweight Agent Operating System

- `program.md` functions as a minimal SKILL.md for a fully autonomous agent: defines scope, rules, constraints, output format, and the main loop in a single Markdown file the human iterates on
- Human role = "programming the program.md," not the implementation files; the agent executes, the human refines the instruction set
- Explicitly defines what the agent CAN and CANNOT modify (e.g., train.py = editable; prepare.py = read-only), establishing hard boundaries between agent territory and invariant harness
- Demonstrates that a skill can serve as an entire operating model for an agent, not just a reference guide
- (see [skills.md](skills.md#skills-sops-for-ai-agents) for the SKILL.md format this extends)
*Source: autoresearch/program.md*

---

### Overnight Autonomous Job Manifest Pattern

- `/overnight` command creates a JSON manifest for unattended batch or resume-mode jobs: `name`, `working_dir`, `items`, `prompt_template` fields
- Two job modes: batch (list of similar items processed independently) and resume (single long-running pipeline with checkpoint tracking)
- Prompt template requirements: what to do with each item (specific), reference file locations, how to check if already done (idempotency), expected output format, and for resume mode -- instruction to check `{checkpoint_file}` before starting
- Status dashboard tracks progress, failure count, last run time, checkpoint file, and log path -- enables human oversight without interrupting the run
- `/overnight resume` pattern: find manifest, check checkpoint for remaining work, re-launch orchestrator
*Source: claude-code-synthesis/commands/overnight.md*

---

### Autopilot TDD Workflow (Task Master)

- `tm autopilot <taskId>` runs a deterministic RED/GREEN/COMMIT loop per subtask: generate failing tests → implement code to pass → commit → advance to next subtask → push and open PR
- Guardrails: never commits to default branch; only commits on green tests; enforces configurable coverage threshold; pauses with full state artifacts after 3 failed GREEN attempts
- Resumable: state and JSONL event log stored in `.taskmaster/reports/runs/<run-id>/`; `--resume` picks up from last checkpoint
- Orchestration model: `WorkflowOrchestrator` returns "work units" to the Claude executor via MCP -- state management and code generation are cleanly separated
- Prompt composition uses three layers: base rules (git + test workflow), task context injection (subtask description + acceptance criteria + phase), and phase-specific instructions (RED: generate failing tests only; GREEN: implement minimal code)
- `--dry-run` prints the full execution plan without making changes
- (see [workflow-patterns.md](workflow-patterns.md#pattern-2-the-ralph-loop-autonomous-coding) for the related Ralph Loop pattern)
*Source: claude-task-master/.taskmaster/docs/autonomous-tdd-git-workflow.md*

---

### tm loop: Task Master Iteration Pattern

- `task-master loop --iterations N` spawns a fresh Claude Code session per iteration, each picking the next task, completing it, committing, and exiting -- fresh context per iteration prevents quality degradation
- A shared `loop-progress.txt` persists notes across iterations so each fresh session has context about prior work without full conversation history
- Built-in presets: `default` (task completion), `test-coverage` (write tests for uncovered lines), `linting` (fix lint/type errors), `duplication` (refactor via jscpd), `entropy` (code smell cleanup); custom prompt files accepted via file path
- Completion command (`--on-complete`) runs a shell command when all tasks finish -- enables webhook notifications
- Variation on the Ralph Loop pattern (see [workflow-patterns.md](workflow-patterns.md#pattern-2-the-ralph-loop-autonomous-coding)); key difference: task-master loop uses structured task metadata and Taskmaster's task selection logic rather than plain text files
- Credit: "Ralph Wiggum pattern" attributed to Jeffrey Huntley / Matt Pocock
*Source: claude-task-master/.taskmaster/docs/loop-prd.md*

---

### Expect as Native Workflow Integration

- Agent self-doubt hook: Claude Code hook on `assistant_response` detects task-completion language and injects a verification run before the response reaches the user
- Reverse integration: Expect finds a bug, opens issue or sends message back to the coding agent, agent fixes, Expect re-verifies -- human only sees the final result
- MCP server exposure: any agent can call `expect.verify({description: "..."})` mid-task, not just at the end -- highest leverage because it works across all agents
- Preview URL auto-detection: detects Vercel/Netlify preview deploys from git metadata or CI env vars; auto-runs on every preview deploy with zero config
- `expect watch` daemon: continuous background re-run of the relevant subset of last test plan on every hot reload
- Spec-driven testing: `expect init` generates `expect.plan.md` that lives in the repo; developers edit it like a spec doc; Expect executes it -- the spec IS the test suite
- (see [testing-verification.md](testing-verification.md#automated-verification-hooks) for hook-based verification patterns)
*Source: expect/.specs/workflow-integration-brainstorm.md*
- Role-specialized agents (marketing agent, coding agent, recruiting agent)

### Claude Computer Use + Dispatch: Desktop Agent Control from Phone

- Claude Computer Use allows Claude to control your Mac desktop while you're away; Claude Dispatch connects desktop app to mobile Claude app
- Scheduling: supports task scheduling (name + description + prompt + frequency) for recurring autonomous workflows
- Example use cases: post jobs on Fiverr, collect URLs from Meta Ads Library, save to Canva -- multi-step cross-app automation from a single phone prompt
- Critical: computer must stay on; dedicated always-on hardware (Mac Mini) is the recommended production setup
*Source: 2026-03-25-rubenhassid-httpstcosbyxsl3qua.md*

### 20-Agent Content Pipeline: Specialization and Quality Gates

- Each of 20 agents runs in its own context window, specializes in one job (hook writing, body copy, CTA, weapons check, etc.) and has a hard quality bar to clear before output passes to the next agent
- Quality gate pattern: every hook goes through minimum 3 iterations with diagnosis of weaknesses before rewrite; Hook Manager scores on 5 dimensions, must hit 10/10; nothing advances until it passes
- "Weapons Check" step: every script line independently scored on Invention Novelty and Copy Intensity; both must hit 10/10; lines that fail get rewritten; pure filler gets cut
- Research phase precedes all writing: 15 YouTube keyword searches across 3 time windows, Reddit pain mining, ~5,000 X posts sorted by engagement; all indexed as "ammunition" for writing agents
- Key architecture principle: don't use one agent for research + writing + editing; specialize each agent and give it a supervisor that enforces the quality bar
*Source: 2026-03-23-MitcheIl-httpstco1ax8svq17s.md*

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

*Source: Twitter-Bookmarks/2026-02-11-getAlby-an-openclaw-bot-spawned-a-child.md*

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

### AutoAgent: Self-Improving Agent via Overnight Iteration
- AutoAgent (github.com/kevinrgu/autoagent) automates the prompt-tools-config tuning loop: you write a `program.md` in plain English, add benchmark tasks, and the system rewrites and tests the agent configuration overnight
- Meta-agent loop: a "meta-agent" reads your instructions → rewrites the full agent setup → tests against real benchmarks → keeps improvements → discards regressions → repeats autonomously
- Benchmark results: #1 SpreadSheetBench (96.5%), #1 TerminalBench with GPT-5 (55.1%) -- reached via this automated self-improvement process, not manual tuning
- Setup: `git clone` → `uv sync` → write `program.md` → add tasks in `tasks/` → run overnight; runs inside Docker so nothing breaks on the host
- Conceptual framing: "AutoML but for agents" -- same principle as automated hyperparameter search applied to agent architecture
- Operational implication: when agent performance is poor, the bottleneck is usually the prompt/tools/config, not the model -- AutoAgent makes that bottleneck automatically addressable

(see [program.md as Lightweight Agent Operating System](#programmd-as-lightweight-agent-operating-system) for the related single-file agent OS pattern)

*Source: 2026-04-04-Axel_bitblaze69-something-for-your-to-do-list-this-weekend-clone-one-repo-wr.md*

### Autoresearch Applied to Marketing -- Autonomous Experiment Loops
- Karpathy's autoresearch pattern (modify variable, deploy, measure, keep/discard, repeat) generalizes beyond ML to any domain with a measurable feedback signal
- Marketing implementation uses three files: baseline.md (fixed constraints/ICP), template.json (asset being optimized), program.md (campaign goal + scoring rule) -- mirrors the prepare.py/train.py/program.md architecture
- Autonomous loops can execute 36,500+ experiments/year vs ~30 for traditional teams at $100-150/month compute cost -- the moat is the accumulated experiment history, not any single result
- Multiple loops running simultaneously across channels (email, ads, landing pages) create compounding effects -- each loop's discoveries feed the others
- (see [Autonomous Overnight Research Loop](#autonomous-overnight-research-loop) for the core autoresearch pattern; see [program.md as Lightweight Agent Operating System](#programmd-as-lightweight-agent-operating-system) for the three-file architecture)

*Source: 2026-03-08-ericosiu-httpstcolgxham4tdn.md*

### Autoresearch Deployment Guide -- Mac and Windows
- Autoresearch replaces the human researcher with an AI agent in an autonomous loop: read instructions, modify code, run 5-min training, measure val_bpb score, keep or discard, repeat (~12 experiments/hour)
- Three-file architecture: prepare.py (fixed constraints), train.py (the thing being optimized), program.md (instructions for the agent -- the human's primary leverage point)
- Claude Code recommended for full autopilot mode; Cursor for semi-manual learning where you observe and approve each step
- Most experiments fail (10-20 out of 100 are keepers) -- the agent handles discard/keep automatically; results tracked in results.tsv with each successful experiment saved as a git commit
- (see [AutoAgent: Self-Improving Agent via Overnight Iteration](#autoagent-self-improving-agent-via-overnight-iteration) for the meta-agent variant of this pattern)

*Source: 2026-03-08-hooeem-httpstcon2ph5qetco.md*

### Five-Agent Fleet + Single Brain Marketing OS
@ericosiu's six-month production deployment running an AI marketing agency on top of an OpenClaw-style fleet. Five agents, each owning a business function, coordinated by a World Agent and grounded in a continuously-ingested Single Brain.

- **The fleet (one agent per function, no overlap, no gaps):** Alfred (chief of staff/orchestrator), Oracle (SEO/analytics), Arrow (sales pipeline -- inbound BDR + outbound), Cyborg (recruiting), Flash (content factory)
- **Single Brain layer (Dorsey "world model"):** unified vector DB ingests Slack, CRM, Gong transcripts (6,862+), Granola notes, Google Analytics, Search Console, deliverables, financials every 15 minutes. Six months of continuous ingestion is the moat; competitors can't fast-forward proprietary data.
- **Sales pipeline (Arrow):** runs 3x/day (6am/noon/6pm) checking HubSpot for new leads, enriching, scoring, posting lead cards to Slack with approve/reject buttons. Outbound: 6,038 leads loaded across 5 active campaigns; AI manages sequencing, personalization, timing. Reply tracking every 4 hours; account rollup 7x/day on weekdays.
- **Content factory (Flash):** X trend scanner runs 2x/day on 10 key accounts, scoring posts 0-100 for impressions/engagement/bookmarks/topic relevance. YouTube competitive analysis 2x/week across 10 channels with view-velocity outlier detection. Podcast transcripts auto-broken into content atoms (1 episode → 6-8 platform-specific drafts). Articles avg 120K views; short posts 19K -- 6x multiplier means Flash prioritizes long-form.
- **Recruiting (Cyborg):** sources overnight while user sleeps. Last run: 50 candidates across 4 roles in 8 hours. 84% in target geography, 76% scored HIGH on experience+role+location match. Preference model learns from approve/reject patterns -- no manual brief updates.
- **AutoResearch + AutoGrowth:** Karpathy's autoresearch pattern runs continuously across all data; surfaced a 3x close-rate correlation tied to specific keywords prospects used in first 5 minutes of calls. AutoGrowth A/B tests subject lines/angles/send times -- question-form subjects outperformed statements 2.3x after 4 weeks; insight applied automatically.
- **Self-healing cron doctor:** twice-daily check on all 48 jobs; reads error logs, diagnoses, fixes what it can. Real test: "recovers faster than you notice." 2 of 3 failures auto-repaired before user checks.
- **Cost economics:** moving from cloud APIs to local inference cut costs ~70%; hardware pays for itself in weeks.
- **Six design principles:** LLMs do judgment, scripts do determinism. Never instruct twice (second occurrence becomes a skill or cron). Security gates on every external-content-handling script (inbound + outbound). Self-healing over monitoring. Flat files over databases. The system compounds -- months 1-2 are pain, month 3 the flywheel kicks in.
- **Productization angle:** internal implementation becomes the product. Agencies sell the intelligence layer that makes services 10x more effective; the services come with it. Months of compounded data + learnings = differentiation that SaaS can't replicate.
- (see [agent-design.md](agent-design.md#five-agent-fleet--single-brain-pattern-dorsey-world-model) for the architecture view)

*Source: 2026-04-11-ericosiu-httpstcop3alvdc9dc.md*

### X API via OpenClaw (Elon Musk announcement)
- @elonmusk: "You can access X API via OpenClaw. We're trying to make it affordable without giving away the shop."
- Means OpenClaw and other agentic platforms can now build apps on top of X (read tweets, manage timelines, post, monitor mentions)
- Previously the X API access was prohibitively expensive for indie/agent use; OpenClaw integration changes the economics
- Relevant for any agent-driven Twitter marketing or social listening pattern (see [community-insights.md > Agent-Driven Marketing & Sales](community-insights.md#agent-driven-marketing--sales) for adjacent tactics)

*Source: 2026-04-18-elonmusk-you-can-access-api-via-openclaw-were-trying-to-make-it-affor.md*

### In-the-Loop / On-the-Loop / Off-the-Loop -- The Autonomy Spectrum (Andrew Orobator Pt 10)
The conceptual progression from manual prompting to true autonomous agents. Each level requires more infrastructure but unlocks different work.

- **In the loop:** human prompts every step. Solo vibe coding. Right for ambiguous feature work where judgment is the value.
- **On the loop:** human orchestrates and reviews. Conductor pattern with multiple worktrees (see Andrew Pt 9). Human kicks off each agent, reviews each PR.
- **Off the loop:** human sets constraints + reviews outcomes. Cron, webhook, or event triggers. Background agents run on schedule.
- **The transition rule:** "If engineers still manually kick off work with a prompt, we've automated the work, not the workflow."
- **What makes off-the-loop viable:** maintenance tasks aren't ambiguous (they're deterministic, verifiable, soul-crushing). Flag cleanup is the first domino because the pain is universal, the correctness is checkable, and the win is measurable.
- (see [Flag Lifecycle Agent](#flag-lifecycle-agent--the-self-driving-codebase-andrew-orobator-pt-10) below for the production case study; see [agent-design.md > The Multi-Agent Spectrum](agent-design.md#the-multi-agent-spectrum-subagents-vs-independent-sessions-vs-serial-andrew-orobator-pt-9) for the on-the-loop predecessor pattern)

*Source: Andrew-Vibe-Coding/Vibe Engineering From Random Code to Deterministic Systems (Part 10).md*

### Flag Lifecycle Agent -- The Self-Driving Codebase (Andrew Orobator Pt 10)
Production-grade case study of off-the-loop autonomy. Reddit hackathon, Phase 1 = one engineer + one day cleaned up 7 stale feature flags end-to-end on Reddit's Android codebase.

**The problem space:**
- Reddit's Android codebase had **571 stale flags**, 91 of them >12 months old. Backlog growing faster than any cleanup ritual could drain it.
- "We should clean this up" never happens at scale. Engineers hate it. Cleanup sprints don't stick. War rooms only delete what gets political capital burned on them.
- Stripe's Developer Coefficient pegs maintenance + tech debt drag at ~17 hrs/week per dev. McKinsey: 20-40% of tech estate value. Knight Capital lost $440M in 45 minutes when a repurposed flag reactivated dormant code on deploy.

**The numbers from Phase 1:**
- 7 cleanups (5 kill switches + 1 feature flag + 1 four-variant experiment)
- **7/7 PRs passed CI; 7/7 kept the correct code path; 0 adjacent flags touched**
- Total LLM cost: **$8.79 across all runs ($1.26 per cleanup)**
- Avg runtime: ~14 minutes per cleanup
- 1 intelligent refusal -- the agent detected a scope contradiction and stopped rather than produce code that would break a test file it wasn't allowed to modify. Cost $0.70, saved a broken PR.

**Architecture (Society-of-Mind layers):**
- **Orchestration:** discovery (`stale_flags.py`) → experiment-platform validation → complexity scoring → spec generation → PR transplant
- **Specialists:** Planner → Coder → Reviewer 3-agent loop inside cloud sandbox
- **Platform:** sandboxed execution, git, GitHub, experiment data MCP

**Decision discipline (evidence-backed not assumption-backed):**
- Before submitting cleanup, orchestrator queries variant sizes (variant at 1.0 = winner = code path to keep)
- Pulls metric readouts into the PR body so reviewers see experiment impact
- Frozen experiment / failed health check / partial rollout → **aborts the cleanup**
- Agent does NOT invent cleanup logic -- it executes a battle-tested skill that encodes 2 years of post-mortems from experimentation + Android teams. The skill is the runbook; the agent is the runner.

**Economics at scale:**
- $1.26/cleanup × 2-PR/day cap × weekdays = ~520 flags/year for <$700 LLM spend
- That's >90% of Reddit's Android backlog cleared in 12 months for less than a team lunch
- Human alternative: 30 min × $100/hr fully loaded = $50/flag → $26,000 + 260 engineer-hours = 6.5 weeks of full-time work
- **The actual comparison isn't $700 vs $26,000 -- it's $700 vs *nothing*.** The work was never going to get done manually.

**Kill criteria (the autonomy spec):**
- 2 reverts in 7 days → pause
- 3 consecutive refusals → pause
- 20% CI failure rate → pause
- 5 unreviewed PRs in queue → pause
- Single run >$5 → pause
- "You don't deploy an autonomous agent without deciding, in advance, what 'too dangerous to continue' looks like."

**Generalized pattern -- the formula under all autonomous fleets:**
**Discover → Assess risk → Execute → Verify → Human review.**

- Verification gate per work type:
  - Backend/logic: compile + unit + integration tests
  - UI code: compile + unit + screenshot tests
  - UI feature: screenshot tests + video review by second agent
  - Dependency bump: full test suite + perf benchmarks
  - Documentation: linter + broken-link check + example code compiles
  - Refactor/dead code: compile + full test suite + behavior diff
- **The limiting factor is verification quality, not LLM capability.** If you can verify it, you can automate it. Tests rot too, but a broken gate fails *loudly* while a broken prompt fails *silently and ships*.

**Honest pushback (from the internal Slack thread that sharpened the thesis):**
- **Attestation:** human trigger = human merges. Cron trigger = CODEOWNERS owns it. Same rules as any other change.
- **DoS-ing reviewers:** agents generate faster than humans read. Rate limit is a kill criterion, not a nice-to-have.
- **Repeat regressions:** agents make the same mistake twice. Kill switches + verification gates + post-mortem-encoded skills exist for this.
- **Plan review > code review:** for autonomous agents, the **skill is the pre-approved plan** -- reviewed once when written, applied every run.
- **Legitimacy at volume:** "review required" quietly collapses when the queue doubles. The rate limit isn't a throughput knob; it's a **trust budget**.

**Adjacent fleet candidates (the same pattern across domains):**
- Dependency bumps
- Incident first-response
- Skill maintenance (closes the loop -- skills accumulate entropy too)
- Dead code cleanup
- Lint migrations
- A11y audits

**Industry signal:** Cognition's Devin runs 14 of these in production teams. Anthropic Managed Agents and Cursor Automations are bets on the same shape. Steve Yegge's [Gastown](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04) -- fleets of 20+ agents under a "mayor" -- is already in production at Fortune 100 companies.

**The mindset shift:** "We should be **harness engineering** -- building the system that writes the code, not writing the code. Senior engineers should be designing the constraints, the gates, the skills, the verification surface. Deterministic chore work runs on a cron while we sleep."

*Source: Andrew-Vibe-Coding/Vibe Engineering From Random Code to Deterministic Systems (Part 10).md*

### Open Swarm: One-Canvas Agent Army
- @OpenSwarm_ launched: "One canvas, an army of AI agents. Be the boss."
- Visual canvas-based orchestration of multiple AI agents -- the user is the orchestrator/conductor, agents execute in parallel
- Adjacent to Five-Agent Fleet pattern but UI-first vs file-first; tradeoff is operational visibility (canvas is legible) vs persistence (file-based scales better)

*Source: 2026-04-22-OpenSwarm-introducing-open-swarm-one-canvas-an-army-of-ai-agents-be-th.md*

### Hermes Agent Army: 5 Pillars + VPS Setup + Multi-Agent Strategy (Nate Herk)
- **Open-source agent runtime** (Nous Research, MIT, 140K stars). VPS, Mac Mini, laptop, Docker, even Android via Termux. 91 skills ship out of the box, 520+ in community hub (16 official Anthropic). Connects to Telegram/Discord/Slack/WhatsApp/iMessage.
- **Positioning vs. Claude Code:** Claude Code is the desk-bound daily driver for knowledge/coding work. Hermes is the on-the-go, voice-first, scheduled-automation layer that lives in your pocket. Same brain (skills + memory + version control), different interface. They share a GitHub repo of business context, skills, memory — any agent (Claude Code, Hermes, OpenClaw, Codex) can plug in.
- **The Five Pillars mental model:**
  1. **Memory** — `user.md` (who you are, style, preferences) + `memory.md` (projects, environment, business context) load at session start. Auto-extracts facts as you work. Use session search (SQLite) for old conversations. Never put secrets or temporary task status in memory.
  2. **Skills** — procedural memory as reusable playbooks. Stored as `skill.md` with YAML frontmatter declaring triggers (progressive disclosure — body loads only on invocation). Hermes analyzes conversations and offers to turn repeated patterns into skills.
  3. **Soul** — `soul.md` shapes personality. Six Hermes agents can each have their own vibe (concise, sarcastic, blunt, formal). Evolves with feedback.
  4. **Crons** — natural-language scheduled jobs. Each cron runs in a fresh isolated session, results back to chat. Flags: `CONTEXTFROM` (chain output), `WORKDIR`, `NOAGENT` (no agent reasoning loop). Cron sessions can't recursively create crons — prompt must be self-contained. Time-bounded crons work like `/loop`.
  5. **Self-Improving Loop** — do work → feedback → save to memory → repeat steps become skills → search past sessions when context matters. Caveat: automatic doesn't mean magic. Correct on the spot, ask it to save things, let it create skills after complex work.
- **Manage Hermes from Claude Code:** keep a `vps-agents` project where every agent gets a folder containing IP, admin creds, API key paths, container setup, Docker info, security/integration notes. "When something breaks at 11pm, I don't dig through Hostinger — I open Claude Code, point at the project, it fixes the agent." Build the assistant for the assistant.
- **API key hygiene:** never paste keys in chat. SSH in, run `hermes config set GITHUB_TOKEN <token>` so it lands in container's `/opt/data/.env`. Named keys per agent, scoped tight (least privilege). Marketing agent doesn't need read access to QuickBooks. Finance agent does. Lock down VPS via firewall, restrict to your IP, block unused ports — build a skill that runs a nightly security audit. Hermes can attack its own setup and report findings.
- **Spin-up-second-agent decision rule:** new agent if it needs its own credentials/secrets/tools, its own long-term memory, OR is ongoing repeated work for a separate role. Otherwise extend main agent. Bad pattern: one mega-agent with every key + every skill + every cron (high confusion, high blast radius). Good pattern: main personal + split-off agents in own containers with scoped keys and uncommitted .env.
- **The Claude Code/Hermes split lesson:** "watch the agent while it's working. If you wanted it to invoke a skill and it didn't, that's your signal to tell it 'update the YAML front matter so this skill triggers when I say X.'"
- (see [skills.md > Claude Skills Full Playbook](skills.md#claude-skills-full-playbook-saved-prompt-vs-trained-employee) for the SKILL.md authoring patterns Hermes uses; see [memory-persistence.md](memory-persistence.md) for the user.md/memory.md two-file convention)

*Source: 2026-05-10-nateherk-httpstcopqx1ron7vm.md*

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

*Source: Twitter-Bookmarks/openclaw security 101 13 steps to lock down your AI agent.md*

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

*Source: Twitter-Bookmarks/Thread by @johann_sath.md*

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

This represents a production-ready pattern for the "agents paying agents" use case referenced in multiple OpenClaw community discussions (see [bitcoin-ai.md](bitcoin-ai.md) for full technical details, also Claw Cash and Start With Bitcoin entries).

### MiniClaw Philosophy: Single Access Point Architecture

A security-first alternative to OpenClaw's multi-channel model, advocated by the Everything Claude Code author after a week of probing OpenClaw's attack surface.

- **Core principle:** "Multiple points of access is a bug, not a feature." Every channel you connect (Telegram, Discord, X, email, WhatsApp) is an injection surface. One compromised channel pivots to all others
- **MiniClaw setup:** SSH-only access (ed25519 key auth) -> Tailscale mesh (no exposed ports) -> tmux session (persistent) -> Claude Code with scoped permissions. No multi-channel integrations
- **The OpenClaw Paradox:** "The people who can safely evaluate OpenClaw's risks don't need its orchestration layer. The people who need the orchestration layer can't safely evaluate its risks." Named pattern -- technical users bypass the GUI anyway; non-technical users can't assess the security tradeoffs
- **Comparison table:** MiniClaw uses 1 access point (SSH), containerized execution, headless terminal, manually audited local-only skills, SSH-only network exposure, project-scoped blast radius. OpenClaw uses many access points, host machine execution, dashboard GUI, unvetted marketplace, multiple ports, everything-accessible blast radius
- **Everything OpenClaw does can be replicated** with cron-job.org, Playwright, CLI tools, and skills/hooks -- without the multi-channel attack surface
- **Account partitioning:** Give agents their own accounts (Telegram, X, email, GitHub). Never share personal accounts -- "if your agent has access to the same accounts you do, a compromised agent IS you"

(see [failure-patterns.md](failure-patterns.md#agent-security-threat-model-6-attack-classes) for the specific attack categories)

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

### Nunchuk CLI: Bounded-Authority Bitcoin Wallets for AI Agents
- Nunchuk released a CLI tool to create shared Bitcoin wallets between humans and AI agents with spending budgets and human final-say
- **Bounded authority pattern:** agent gets its own key in a multisig wallet with a spending limit -- agent can initiate transactions up to the budget, human retains veto/co-sign authority
- Operationalizes the "least privilege for agents" principle: agents should never get full key access. The wallet IS the permission boundary
- Complements existing agent wallet patterns: LNCURL (Lightning wallets with survival mechanics), remote signer architecture (key separation), macaroon budget caps

(see [LNCURL: Instant Lightning Wallets for Agents](#lncurl-instant-lightning-wallets-for-agents) for the Lightning equivalent; see [bitcoin-ai.md](bitcoin-ai.md) for full Bitcoin-AI integration patterns)

*Source: 2026-04-08-nunchuk_io-ai-agents-shouldnt-get-the-full-key-to-your-kingdom-today-we.md*

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

*Source: Twitter-Bookmarks/Thread by @thegarrettscott.md*

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


