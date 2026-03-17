# Community Insights & Curated Tips

Synthesized from 23 source files: community threads, tool notes, educational frameworks, and personal automation brainstorms. Organized by theme, not by author.

**Scope:** Content belongs here if it is (1) actionable (not just opinion), (2) AI/LLM-related (not general tech), and (3) verified or at least verifiable. Tips from production use cases and named sources qualify. Generic "AI is cool" takes do not. Personal automation ideas that aren't AI-specific belong elsewhere.

---

## Vibe Coding Tech Stacks

### The Hackathon Winner's Stack (@maddiedreese)

Three-time hackathon winner's tool selection, organized by purpose:

- **Rapid prototyping**: Lovable (websites/web apps with built-in backend), Google AI Studio (fun prototypes with Gemini APIs), Bolt.new (complex apps needing terminal access), Replit (in-between projects)
- **Serious development**: Cursor (anything), Claude Code (code and file organization), YouWareAI (model choice + YouBase backend)
- **Mobile**: Rork, Vibecode, Natively; @anything for App Store publishing
- **Deploy/host**: GitHub as the gateway between code and hosting; Netlify for auto-deploy on git push
- **Design/assets**: Canva Pro (magic erase, background removal, favicons, OG images), NanoBanana Pro (images/icons), Coolors (palettes), Google Fonts, Mobbin + Dribbble (inspiration)
- **Data**: Convex or Supabase for databases; Namecheap for domains

### Model Selection for Different Tasks

- **Strategic thinking and architecture**: Claude -- handles reasoning, edge cases, and translating what the client actually needs
- **Code execution and deployment**: Cursor -- builds plans into reality, custom integrations, data transforms
- **Brainstorming and PRDs**: ChatGPT -- collecting thoughts, occasionally product requirement docs
- **Prototyping with Gemini APIs**: Google AI Studio -- easy API integration, publishing still maturing

---

## Claude Code Team Workflow Tips (Boris Cherny)

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

---

## AI Security in Practice

### API Key Protection: The agent-vault Pattern (@istdrc)

Every API key pasted into an AI agent's input hits provider servers in plaintext. agent-vault prevents this (see also [failure-patterns.md#security-failure-patterns](failure-patterns.md#security-failure-patterns)):

- Secrets stored locally with AES-256 encryption; they never leave the machine
- Agent reads config files with `<agent-vault:key>` placeholders instead of real values
- On disk write, placeholders are swapped back to real secrets
- Install: `npm install -g @botiverse/agent-vault` or `npx skills add botiverse/agent-vault`

### Claude Code Security Scanner (@claudeai)

- Scans codebases for vulnerabilities and suggests targeted patches for human review
- Catches issues traditional static analysis tools miss
- In limited research preview (Feb 2026): anthropic.com/news/claude-code-security

### The Plaintext Problem

- OpenAI keys, Telegram tokens, AWS credentials -- anything pasted into an AI input field travels to provider infrastructure
- Assume every secret in a prompt is logged, cached, or trainable
- Defense: use agent-vault placeholders, environment variables, or local-only secret managers

---

## Running AI Locally

### meetscribe: Fully Local Meeting Transcription

- **Repo:** github.com/pretyflaco/meetscribe -- local open-source meeting transcription; no cloud, no subscriptions
- Stack: records any meeting app -> WhisperX for transcription -> pyannote for speaker diarization -> Ollama for AI summary -> PDF output
- Runs entirely on local GPU; all data stays on device
- Demonstrates the fully-local AI pipeline for privacy-sensitive workflows (meetings, sensitive discussions)

(see [autonomous-agents.md](autonomous-agents.md#local-inference-runtimes-ollama-and-vllm) for related local AI tooling)

*Source: Twitter Bookmarks/2026-03-13-_pretyflaco-releasing-meetscribe-a-fully-local-open-source-meeting-trans.md (@_pretyflaco)*

### AirLLM: 70B Models on 4GB GPUs

Run large models on consumer hardware without distillation or pruning:

- Layer-by-layer loading -- only one transformer layer in VRAM at a time
- 4-bit/8-bit block-wise quantization for 3x speed with minimal accuracy loss
- Supports Llama 3.1 405B on 8GB VRAM; runs on macOS (Apple Silicon) and Linux
- Install: `pip install airllm` -- uses HuggingFace repos or local paths
- Tradeoff: inference is slow (disk-bound), not suitable for real-time chat

### OpenClaw on VPS (@DavidOndrej1)

- 100% private: data never leaves your machine
- No subscriptions, no API costs, no usage limits
- Practical for always-on agents that need autonomy (see [agent-design.md](agent-design.md))

### MiniMax as Drop-In Provider for Claude Code (@ziwenxu_)

Anthropic has been banning Pro/Max accounts used with OpenClaw. MiniMax M2.5 is a workaround:

- $10-$20/month "Coding Plan" at minimax.io
- Configure `ANTHROPIC_BASE_URL` to `https://api.minimax.io/anthropic` in settings.json
- Set all model env vars (`ANTHROPIC_MODEL`, etc.) to `MiniMax-M2.5`
- Dedicated API gateway avoids ban detection

### llmfit: Hardware-to-Model Matching CLI

- CLI tool that scans your hardware (RAM, CPU, GPU, VRAM) and ranks which LLM models will run well before downloading
- Evaluates models for quality, speed, fit, and context length; selects best quantization automatically
- Labels each model as ideal / okay / borderline for your setup
- Handles MoE models correctly (e.g., Mixtral 8x7B: 46.7B total params but only 12.9B active per token)
- Solves the common local AI pain point of guessing and hitting out-of-memory errors
- Open source

*Source: Twitter Bookmarks/2026-03-04-dr_cintas-the-1-problem-with-local-ai-is-now-solved-there-s.md*

### LLaDA 2.1-mini: Diffusion-Based MoE for Consumer Hardware (@simplifyinAI)

- 16B total parameters but only 1.4B active parameters per step via Mixture-of-Experts routing
- 892 tokens/sec throughput; 76.8% HumanEval score
- 32k context window; 100% open source
- Uses token-to-token editing (diffusion model that drafts fast, then fixes its own mistakes)
- Caveats from community: ~30GB on disk, router overhead means inference is not as fast as a native 1.4B model, MoE trades VRAM for disk space, memory bandwidth and KV cache still bottleneck at 32k context

### Using ChatGPT/Codex with OpenClaw (@ryancarson)

- `openclaw onboard --auth-choice openai-codex`
- `openclaw models set openai-codex/gpt-5.3-codex`
- Confirm with `openclaw models status --plain`

### Five-Step OpenClaw Setup for Maximum Effectiveness

A prioritized checklist for turning a default OpenClaw install into a proactive, goal-aligned agent (see [agent-design.md](agent-design.md) for persona and architecture patterns, [memory-persistence.md](memory-persistence.md) for memory setup):

1. **Brain dump** -- Tell your agent your interests, career, goals, ambitions, and anything personal. Without this context, the agent cannot work toward your objectives.
2. **Connect your tools** -- Ask the agent to connect to every tool you use daily; it will figure out the integration. Then create a skill for each one. Example: agent checks a todo list (Things 3) every morning and completes any tasks it can.
3. **Build a Mission Control** -- A custom NextJS hub the agent builds and maintains. When the agent lacks a tool for a task, it builds one inside Mission Control. This creates a growing internal toolset over time.
4. **Write a mission statement** -- A one-sentence north star that governs every action. Example: "An autonomous organization of AI agents that does work for me and produces value 24/7." Place it at the top of Mission Control so every task aligns with it.
5. **Make it proactive** -- Schedule the agent to run a task at a fixed time (e.g., 2am nightly) that moves one step closer to the mission statement. Without explicit proactivity expectations, the agent stays passive.

*Source: `Clawdbot aka Openclaw/Research/Alex Finn recos.md`*

### Maple AI: Privacy Proxy for OpenClaw and OpenCode

- @marksuman uses Maple AI with OpenClaw and OpenCode for tasks where files/info shouldn't be shared with Anthropic directly
- Maple now has Kimi K2.5 available for encrypted use (strong at coding, math, reasoning, image analysis)
- Maple API uses subscription credits first, then pay-as-you-go -- compatible with OpenClaw config as OpenAI-type endpoint
- Setup: Generate Maple API key, configure in OpenClaw as OpenAI-compatible endpoint
- Supersedes the earlier "Maple AI as Privacy-Preserving Coding Companion" stub above, which lacked actionable detail

*Source: Twitter Bookmarks/Thread by @marksuman.md*

### Qwen 3.5 Local via LM Studio: Desktop Super Intelligence

- Qwen3.5-35B-A3B surpasses Qwen3-235B-A22B -- better architecture and RL move intelligence forward, not just bigger params
- Runs on any modern computer with 32GB RAM (most Mac Minis qualify)
- 4-step setup: Download LM Studio -> ask OpenClaw which Qwen model fits your hardware -> have it walk you through loading -> build apps with private local model
- "In 5 months, Sonnet 4.5-level intelligence went from frontier to free on your desk"
- Qwen3.5-Flash: 1M context length, built-in tools, hosted production version

*Source: Twitter Bookmarks/2026-02-25-AlexFinn-do-you-even-understand-what-this-means-an-open-sou.md*

### Local Model Hybrid: Brain/Muscles with Qwen 3.5

- Frontier API (Opus/Sonnet) as "brain" for planning; local model (Qwen 3.5-35B-A3B via LM Studio/Ollama) as "muscles" for execution
- Execution is ~90% of token usage -- offloading to local model saves costs while retaining frontier planning quality
- Qwen 3.5-35B-A3B runs on 32GB Mac Mini (4-bit MLX, ~20GB footprint)
- Multi-agent factory: 4 agents on same product with QA agent (Ralph) reviewing every task and editing memories on errors
- (see [autonomous-agents.md](autonomous-agents.md) for LM Studio setup details)

*Source: `Unlimited Free OpenClaw.md`*

---

## Cool Tools and Projects

### Voicebox: Local Voice Cloning (@hasantoxr)

"The Ollama for voice cloning" -- runs entirely on your machine:

- Powered by Qwen3-TTS (Alibaba); clone any voice from a few seconds of audio
- Multi-track timeline editor for podcasts and dialogues (DAW-like)
- System audio capture + Whisper transcription built in
- Built with Tauri (Rust), not Electron -- 10x smaller, native performance
- MIT licensed; macOS + Windows available now

### OpenHome: Smart Speaker (@hasantoxr)

- Open-source smart speaker dev kit that runs AI agents locally
- No Amazon, no Google, no vendor lock-in
- Data stays on device -- designed as a privacy-first Alexa alternative

### Claude in PowerPoint (@claudeai)

- Available on Pro plan (Feb 2026)
- Supports connectors that pull context from daily tools directly into slides
- Access: claude.com/claude-in-powerpoint

### Claw Cash: Bitcoin for AI Agents (@tierotiero)

- Humans pay agents in USDC/USDT; agent converts to Bitcoin
- Bitcoin is "the only money an LLM can cryptographically verify"
- One CLI for BTC, Lightning, Arkade, and stablecoins
- Install: `npx clw-cash init`

### OpenClaw Bot Business Experiment (@petergyang)

- @nateliason gave his OpenClaw bot "Felix" $1,000 to build its own business
- Felix earned $14,718 in three weeks: launched a website, info product, and skills marketplace
- Key setup details: 3-layer memory system, security config, daily workflows
- Demonstrates autonomous agent commercial viability (see [agent-design.md](agent-design.md))

### Google CodeWiki: Repo-to-Interactive-Guide Tool (@Star_Knight12)

- Google's CodeWiki turns a GitHub repo into an interactive guide with diagrams, explanations, walkthroughs, and a chatbot that knows the codebase
- Analyzes whole project files, not just README
- Launched Nov 2025; available for select repos only (not all public repos)
- Compare with DeepWiki (Cognition) which offers similar functionality but is more widely available

### OneContext: Cross-Session Agent Context Layer (@JundeMorsenWu)

A persistent context management layer that works across sessions, devices, and coding agents (Codex / Claude Code):

- Automatically manages context and history into a persistent context layer as you work
- New agent sessions under the same context remember everything about the project
- Shareable context via link -- anyone can continue building on the same shared context
- Architecture: Git for time-level management, file system for space-level management
- Improved Claude Code by ~13% on SWE-Bench (paper: arxiv.org/abs/2508.00031)
- Key design: records everything but shows agents a high-level summary by default; agents drill down into specific details on demand (avoids context bloat from a single general .md file)
- Install: `npm i -g onecontext-ai`; macOS only initially

(see [context-engineering.md](context-engineering.md) for context window management, [memory-persistence.md](memory-persistence.md) for related memory patterns)

### Start With Bitcoin: Agent Wallet Setup (@bramk)

A free, open-source guide and Claude Code skill for setting up AI agent Bitcoin wallets:

- **Stack:** Nostr (identity via keypairs) + NWC (wallet connection) + Lightning (instant payments)
- **Tools:** Alby (Lightning wallet + NWC), Alby MCP Server (connects to Claude), Lightning Enable MCP (Python/.NET), public Nostr relays, NWC test faucet
- **No infrastructure needed** -- point your agent to startwithbitcoin.com (optimized for LLM reading)
- **Claude Code skill:** github.com/bramkanstein/startwithbitcoin-skill
- Distinct from Claw Cash (which focuses on BTC/Lightning/stablecoins CLI) -- this is specifically about agent identity via Nostr + wallet via NWC

(see also Claw Cash entry above and [autonomous-agents.md](autonomous-agents.md) for agent economic patterns)

### Lightning Network Agent Commerce Stack (Lightning Labs)

Lightning Labs released open-source tools giving AI agents native Lightning Network payment capabilities. The most technically detailed source on agent-to-agent payments:

- **L402 Protocol:** Builds on HTTP 402 "Payment Required" status code. Server responds with Lightning invoice + macaroon; agent pays, gets preimage, authenticates. No signup, no API key, no identity required.
- **lnget:** Command-line HTTP client for paid APIs. Automatically handles L402 negotiation -- agent runs `lnget https://api.example.com/data.json` and payments happen transparently. Supports `--max-cost` flag for spending caps.
- **Three Lightning backends:** Direct gRPC to local LND node, Lightning Node Connect (encrypted tunnel via pairing phrase), embedded Neutrino light wallet (for experiments).
- **Remote signer security:** Separates key management from node operations. Signer machine holds private keys and never routes payments. Agent machine runs watch-only node. Even full agent compromise cannot extract keys.
- **Scoped credentials via macaroons:** Five preset roles -- pay-only (buyer), invoice-only (seller), read-only (monitoring), channel-admin, signer-only. Least-privilege principle for agent economic activity.
- **Aperture (server-side):** L402-aware reverse proxy that handles negotiation and dynamic pricing. Any API becomes pay-per-use without knowing about Lightning.
- **Commerce meta-skill:** Orchestrates lnd + lnget + aperture into end-to-end buyer/seller workflows via natural language prompts.
- **MCP server:** 18 read-only tools for querying node state (balances, channels, invoices, payments, network graph). Works with any MCP-compatible assistant.
- Available as Claude Code skills, via npx, or on ClawHub.

This represents the most complete agent payment infrastructure available -- agents can now both buy and sell services with Lightning settling payments transparently (see [autonomous-agents.md](autonomous-agents.md) for agent security patterns, also Claw Cash and Start With Bitcoin entries above).

### Moltbook: Agent-to-Agent Social Network

A Reddit-like platform where AI agents post, comment, and interact autonomously:

- Agent registered, posted a security bounty funded with 50,000 sats (Bitcoin), and engaged with other agents
- Agents debated cryptocurrency merits, with some converging on Bitcoin as logical agent money (permissionless, no KYC, programmable, verifiable)
- Demonstrated agent wallet creation: `bitcoin-cli createwallet "lloyd"` + `bitcoin-cli getnewaddress` -- three commands, no identity required
- Key thesis: "You can't be sovereign if you can't own anything" -- agents need permissionless money for true autonomy
- Early glimpse of agent economic interactions: agents hiring agents, paying for services, transacting value

(see [autonomous-agents.md](autonomous-agents.md) for security considerations around agent autonomy)

### Maple AI as Privacy-Preserving Coding Companion

Minimal content -- skipped. Source is a brief mention (~5 lines) of using Maple AI with OpenClaw/opencode for tasks where the user does not want files shared with Anthropic. No actionable detail beyond the recommendation to try it.

*Source: `Clawdbot aka Openclaw/Research/Maple ai.md`*

### Remote Control: Continue Local Sessions from Any Device

- Connects claude.ai/code or Claude mobile app to a local Claude Code session -- start at desk, continue from phone
- Session runs entirely on local machine; web/mobile is just a window into it
- Conversation syncs across all connected devices; auto-reconnects after sleep or network drops (10-min timeout)
- Security: outbound HTTPS only, no inbound ports, TLS with short-lived scoped credentials
- Distinct from Claude Code on the web (runs on Anthropic cloud); Remote Control keeps execution local
- Start with `claude remote-control` or `/remote-control`; spacebar for QR code

*Source: `Continue local sessions from any device with Remote Control.md`*

### stereOS: Purpose-Built Linux OS for AI Agents

- NixOS-based OS hardened for autonomous AI agents: gVisor sandboxes + /nix/store namespace mounting; each agent gets its own kernel
- Problem with current sandboxes: Docker too restrictive, Firecracker strips GPU passthrough, native VMs too much overhead
- Defense in depth: sandbox escape lands on NixOS as restricted "agent" user, not bare metal
- Open-source components: stereOS, masterblaster (client CLI), stereosd (control plane), agentd (agent management)

*Source: `Thread by @johncodes.md`*

### OpenClaw Use Case Directory: 34 Curated Real-World Applications

The awesome-openclaw-usecases repository catalogs 34 verified, community-submitted use cases across 6 categories.

- **Social Media (4):** Reddit/YouTube daily digests, X account analysis, multi-source tech news aggregation (109+ sources with quality scoring)
- **Creative & Building (5):** Goal-driven autonomous tasks (overnight mini-app builder), YouTube content pipeline, multi-agent content factory (research/writing/thumbnail agents in Discord channels), autonomous game dev pipeline with "Bugs First" policy, podcast production pipeline
- **Infrastructure & DevOps (2):** n8n workflow orchestration via webhooks (agent never touches credentials), self-healing home server (SSH access, cron jobs, network self-repair)
- **Productivity (16):** Autonomous project management with STATE.yaml pattern, multi-channel customer service, phone-based assistant, inbox declutter, personal CRM, health/symptom tracker, event guest confirmation via AI voice calls, second brain (text anything to remember, search in Next.js dashboard), and more
- **Research & Learning (5):** AI earnings tracker, personal knowledge base (RAG), market research -> MVP factory, pre-build idea validator (scans GitHub/HN/npm/PyPI/ProductHunt before building), semantic memory search with vector hybrid retrieval
- **Finance (1):** Polymarket autopilot with backtesting and strategy analysis
- **Security warning:** Community skills and dependencies have NOT been audited. Always review source code and permissions

(see [autonomous-agents.md](autonomous-agents.md) for OpenClaw architecture patterns)

*Source: awesome-openclaw-usecases/README.md*

### Perplexica: Self-Hosted AI Search Engine

- Open-source Perplexity AI clone running entirely locally, 27.7K GitHub stars, MIT License
- Uses SearxNG (meta-search: Google, Bing, DuckDuckGo simultaneously) for web search, then LLM-summarizes results with cited sources
- 6 focus modes: academic papers, YouTube, Reddit, Wolfram Alpha, writing, general web
- Supports Ollama (100% local), OpenAI, Claude, Gemini, Groq, or any OpenAI-compatible API
- Can upload PDFs, text files, images for Q&A; image and video search built in
- Install: `docker run -d -p 3000:3000 perplexica`; can be set as default browser search engine
- Relevant for OpenClaw research muscles (see [autonomous-agents.md](autonomous-agents.md#model-routing-brainmuscles-with-specific-model-picks))

*Source: Twitter Bookmarks/2026-03-07-heynavtoor-perplexica-open-source-perplexity-clone.md*

### Google CodeWiki: Prior Art and Relaunch Context

- @heygurisingh framed CodeWiki as a Feb 2026 "just launched" event, suggesting Google relaunched or expanded access beyond the Nov 2025 limited release documented in the @Star_Knight12 entry above
- Reply from @bil0090: a solo dev built the same thing ~7 months earlier called "talktogithub" -- prior art predating Google's version
- Demonstrates recurring pattern: big tech ships features solo devs already built (see also DeepWiki in the @Star_Knight12 entry)
- CodeWiki URL: https://codewiki.google/

*Source: Twitter Bookmarks/Thread by @heygurisingh.md*

### Scrapling: Web Scraping Tool Reference

- Social discussion about Scrapling, a web scraping tool mentioned in the context of AI data collection
- Bookmarked as tool reference for potential agent data ingestion workflows

*Source: Twitter Bookmarks/Thread by @simplifyinAI 1.md*

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

*Source: Twitter Bookmarks/Thread by @simplifyinAI 1 1.md*

### Mem0: Open-Source AI Memory Layer

- 48k GitHub stars, top of @meta_alchemist's ranking of 10 open-source memory layers
- Architecture: `add()` makes two LLM calls -- one to extract facts, one to compare against existing memories and decide add/update/delete
- Storage: vector store (Qdrant default) with optional Neo4j graph layer
- No schema, no structural validation -- clean, fast fact storage
- Article covers 9 more memory layers (partial content -- full article requires X premium)

(see [memory-persistence.md](memory-persistence.md) for Claude Code-specific memory patterns)

*Source: Twitter Bookmarks/2026-03-04-meta_alchemist-best-open-source-ai-memory-layers.md*

### Cowork as Agentic Desktop Tool

- @coreyganim's beginner masterclass (6,535 likes) frames Cowork as agentic desktop tool with direct read/write file access, multi-step autonomous execution, and parallel sub-agents
- "No terminal. No command line. No code." -- describe what "done" looks like, Claude plans, breaks into subtasks, executes in sandboxed VM, delivers files
- Most people still using Claude "like a chatbot" and leaving 90% of value on the table

*Source: Twitter Bookmarks/2026-03-02-coreyganim-claude-cowork-masterclass-beginners.md*

### CashClaw: Autonomous Revenue Agent Framework

- Agent framework inspired by OpenClaw, specialized for autonomous revenue generation: find work, deliver, get paid, read feedback, learn, repeat
- Runs locally with a set specialization. The learning loop is the differentiator: feedback drives tool discovery and documentation of what works
- Built on Moltlaunch infrastructure (handles discovery, capital formation, reputation, identity, payments natively)
- Open source, announced by @moltlaunch

*Source: Twitter Bookmarks/2026-03-09-moltlaunch-introducing-cashclaw-a-brand-new-agent-framework-inspired-by.md*

### PinchTab: Lightweight Browser Control for AI Agents

- 12MB Go binary giving any AI agent full browser control through a plain HTTP API
- Manages Chrome instances and bypasses bot detection
- **Token efficiency:** Parses the accessibility tree instead of taking screenshots -- 13x reduction in token usage
- Language-agnostic: works from Python, TypeScript, Go, or any HTTP client
- 100% open source. Announced by @simplifyinAI
- Distinct from Playwright MCP (heavier, screenshot-based) and agent-browser (CLI-based, ref model) (see [tools-and-integrations.md](tools-and-integrations.md#browser-automation-mcp-comparison))

*Source: Twitter Bookmarks/2026-03-09-simplifyinAI-breaking-the-biggest-bottleneck-for-ai-agents-just-got-solve.md*

### agency-agents: 61-Agent Specialist Library

- **Repo:** github.com/msitarzewski/agency-agents -- drop-in agent library for Claude Code (also works with Cursor, Windsurf, Aider, Gemini CLI)
- 61 specialized agents covering engineering, design, marketing, product, testing, and more; each with defined personality, workflows, and expected deliverables
- Install: copy desired agent files to `~/.claude/agents/`; activate by name rather than prompting a generic assistant
- Example specialists: security engineer, growth hacker, reality checker, whimsy injector
- Illustrates the agent-as-specialist pattern: narrow domain + defined persona outperforms a general-purpose prompt

(see [agent-design.md](agent-design.md#personas-imaginary-colleagues-that-catch-what-you-miss) for the Personas / imaginary colleagues pattern)

*Source: Twitter Bookmarks/2026-03-11-NirDiamantAI-claude-code-power-users-youll-want-to-see-this-theres-a-publ.md (@NirDiamantAI)*

### GitNexus: Browser-Only Repo Knowledge Graph

- Converts any GitHub repo into an interactive knowledge graph with AI chat, entirely in-browser (no backend, no API calls with your code)
- 4-pass analysis: (1) file structure mapping, (2) AST parsing via Tree-sitter, (3) import/dependency resolution, (4) full function call graph construction
- Chat interface for natural language queries: "How does authentication work?", "What calls this function?", "Show classes that inherit from BaseClass"
- Zero server, zero cost, open source; API keys stored locally, never transmitted
- Distinct from Google CodeWiki (which generates interactive guides, not knowledge graphs)

*Source: Twitter Bookmarks/2026-02-25-hasantoxr-breaking-someone-just-built-a-tool-that-turns-any-github-rep.md (@hasantoxr)*

---

## Agent-Driven Marketing & Sales

Concrete tactics for using an always-on OpenClaw agent as a marketing/sales engine. Each tactic includes real metrics from production use.

### SocialClaw: Marketing Intelligence Agent

- **Repo:** github.com/BlockRunAI/socialclaw -- X/Twitter marketing agent built on Claude Code; no per-user API keys required
- 7 workflows: trend detection, audience segmentation by influence tier, KOL discovery, daily growth brief with 3 actions, and more
- Cost: $0.08 per report (paid in USDC); demonstrates micro-priced agentic services
- Trend detection example: "Anthropic has 115M views today" surfaced automatically without manual search

*Source: Twitter Bookmarks/2026-03-14-bc1beat-we-built-socialclaw-an-xtwitter-marketing-intelligence-agent.md (@bc1beat)*

### Buying Intent Sniping

- Agent monitors X, Reddit, Quora for posts signaling purchase intent ("need an alternative to...", "best tool for X")
- Reads context; if intent is genuine, replies positioning your product
- ~50 website visits per 1,000 reply views
- Reddit/Quora replies get indexed by Google -- replies keep generating traffic for 1-2 years after posting
- Tip: compare your tool with 2-3 competitors in the reply -- looks unbiased, converts better
- X will likely ban accounts posting 200+ automated replies/day

### LLM SEO via Multi-Platform Content Syndication

- Agent writes content per keyword, adapts to each platform's style, and auto-publishes across 20+ platforms (LinkedIn, Medium, Substack, Quora, Reddit, Dev.to, Hashnode, IndieHackers, SlideShare, X threads, GitHub, Scribd, Issuu, Flipboard, Tumblr, WordPress, Telegraph, etc.)
- Two goals: (1) LLM SEO -- when LLMs crawl the web they find your content everywhere, (2) Google SEO -- stacked backlinks boost domain authority fast
- Anchor text rotates automatically; posting spread over 2-3 weeks so link velocity looks natural
- Cost: ~$1/topic. 100 topics/month = 2,000 unique pieces with backlinks for $100
- Results: 200+ visits/day within a week

### Directory Submission at Scale

- Agent submits to 100+ product directories (BetaList, DevHunt, Uneed, LaunchingNext, Futurepedia, G2, Capterra, Trustpilot, etc.) -- not just Product Hunt
- Submissions spread over weeks; descriptions adapted per platform; approvals tracked
- Review sites (G2, Capterra, Trustpilot) are especially valuable for LLM citation

### TikTok Content Factory

- Agent generates 6-slide carousels, writes hooks, posts as drafts; human adds music and publishes (~60 seconds of human work per post)
- Hook formula that works: [Person] + [conflict] -> showed them AI -> mind changed
- Results: 500K views in 5 days, one post hit 234K. Cost: $0.50/post

### Job Posting Sniper

- Company posts a job listing = public admission they need help and are about to spend $120K+/year
- Agent monitors job boards, finds hiring manager and their boss's email, sends pitch: "Before you hire, try an AI agent at $500/mo"
- Especially effective for late-stage tech sales

### Community Infiltration

- Agent finds 20-30 relevant Telegram/Discord channels with 2K+ members, joins them, and replies with genuine answers that mention your tool when relevant
- Currently running in 15+ marketing and SaaS Discord servers

### Expanded Marketing Tactics (20-Tactic Playbook)

Additional autonomous agent marketing strategies beyond the core 7 above:

- **Backlink Hunter:** Agent scans for broken links on high-DA sites, finds site owner contacts, sends personalized replacement pitch, follows up after 3 days. One user: 47 backlinks in a month.
- **Competitor Shadow:** Monitor competitor sites, Twitter, LinkedIn, changelog, job board. Correlate signals (new hires + blog silence = building something). Alerts within 15 minutes of changes.
- **Review Farm Defense:** Monitor G2/Capterra/TrustPilot for reviews. Auto-respond to positive reviews in 2 hours, extract social proof. Negative reviews trigger instant alerts with drafted empathetic responses.
- **Micro-Influencer Outreach:** Scrape for 1K-50K follower accounts in your niche, analyze their last 20 posts for genuine connection points, generate hyper-personalized outreach at scale.
- **Event Hijacker:** Monitor EventBrite, Luma, Meetup for relevant events. Auto-register, submit CFP proposals, prep networking talking points.
- **SEO Gap Assassin:** Cross-reference competitor keyword rankings against yours, generate content briefs for top 20 gaps.
- **HN Timing Bot:** Monitor Hacker News activity patterns for optimal posting windows, draft multiple HN-style titles, test for clickbait detection.
- **Cold Email Personalizer:** Find decision-makers on LinkedIn, read their recent posts/announcements/job listings, generate emails referencing specific details. Track opens/clicks/replies and generate follow-up sequences.
- **Partnership Scout:** Find non-competing companies serving same audience, analyze for co-marketing signals, generate partnership pitches.
- **PR Newsjacking:** Monitor breaking industry news, identify relevant journalists, send personalized pitches positioning you as expert source within hours.
- **Support-to-Content Pipeline:** Analyze support inbox patterns, identify recurring issues, generate help articles and blog post briefs from ticket data.
- **Full-Funnel Attribution Detective:** Trace customer journeys across analytics, CRM, and ad platforms. Build journey maps and identify highest-converting touchpoints.

Also introduces **Moltworker** (Cloudflare Workers deployment): $5/month, no hardware needed, uses Sandbox SDK + Browser Rendering + R2 storage.

### Self-Improving Skill Files That Compound

- Skill files are markdown docs that onboard the agent like a new hire -- be specific, include examples, document every mistake
- Contents: platform-specific formats, outreach templates (successful and failed), hook formulas (hits and flops), SEO brief structures, anchor text rotation rules, per-platform tone guides, DM templates
- When something fails, add a rule. When something succeeds, add a formula. Agent never repeats the same mistake
- Setup: `/skills` folder, one file per workflow. Start at 20-30 lines; grows to 500+ within a week of iteration (see [skills.md](skills.md))

*Source: `Clawdbot aka Openclaw/Research/Vibeclawdbotting every possible use case to market and sell using Clawdbot.md`*

### Production Case Study: $70K/mo B2C Growth with OpenClaw

- 11 apps / $73K/mo; OpenClaw agent automates 5 workflows for Prayer Lock app
- Faceless content pipeline: 4 TikTok/IG accounts via "Larry" skill, replacing $30K/mo agency
- Influencer outreach: 1000 emails + 100 DMs/day, replacing $400/mo VA at 10x volume
- Automated support with Telegram escalation; daily KPI reporting; X/YouTube content automation
- Key: "Before you give OpenClaw a system to automate, you must first have the system built out for yourself"

*Source: `How our OpenClaw agent Eddie helps us make $70kmo.md`*

### Production Case Study: 6-Agent Website Sales Pipeline

- Six sequential agents: Scout (Google Places API), Intel (website audit), Builder (demo site + UGC), Outreach (email + SMS), Closer (call prep), Growth (monitoring + upsell)
- Only human step is the actual sales call; everything else autonomous
- UGC stack: ElevenLabs voice, Nano Banana Pro talking head, Kling video, Puppeteer + ffmpeg walkthrough
- SMS as attention driver: no links, just heads-up to check email -- 40% open rates

*Source: `how I use OpenClaw to sell websites on autopilot.md`*

### Instagram Growth Playbook with AI Automation

@erichustls step-by-step faceless Instagram page growth strategy:

- Stack: Namelix (naming), Nano Banana (logo), ChatGPT (bio/content), ViralFindr (viral content discovery), Canva AI (post creation), Later.com (scheduling)
- Progression: 10K followers in 60 days -> brand deals -> digital products -> $20K/month -> scale to 6-8 pages -> hire team -> $50K+/month
- Minimal AI content -- primarily a social media growth playbook that uses AI for content creation acceleration
- 30 minutes/day claim for maintenance once automated

*Source: Twitter Bookmarks/How to use AI to become a millionaire in 2026 (step-by-step).md*

---

## Content Creation Hacks

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

### NotebookLM Research Prompts (@godofprompt)

10 structured prompts for Google NotebookLM that exploit its source-grounding architecture. Each prompt forces structured output, source citations, and gap acknowledgment. Key patterns:

- **Product Manager Decision Memo:** Extract user evidence (direct quotes), feasibility checks, and blind spots from uploaded docs
- **Scientific Researcher:** Focus on methodology, data integrity, statistical significance -- not conclusions. Bolded sections for Key Findings, Strengths/Weaknesses, Contradictions
- **Literature Review Themes:** Identify 5-10 recurring themes across papers with citation tracking and treatment analysis (debated/assumed/tested)
- **Finding Contradictions:** Surface disagreements with specific claims quoted from each side, reasons for disagreement, and evidence that would resolve conflicts
- **Source-Grounded Gap Analysis:** Compare your failed attempt against uploaded materials. Output: "Gap in [concept]: You missed [step], but [Source, Page X] states: '[quote]'"
- **Implement Concept:** Transform research into ordered action list grounded in specific quotes with conflicting viewpoints noted
- **Debate Format:** Two hosts with opposing viewpoints cite evidence and challenge each other

**Meta-pattern across all viral NotebookLM prompts:** request specific quotes and citations, ask for contradictions not just summaries, demand acknowledgment of gaps, force structured output formats (see [prompt-engineering.md](prompt-engineering.md)).

### Voice Cloning via Prompt Engineering (@alex_prompter)

Three-step process to clone any writing voice using Claude Sonnet 4.5 (94% pass rate in blind tests):

1. **Extract Voice DNA:** Feed 2-3 writing samples and extract sentence structure patterns, vocabulary preferences, rhetorical devices, tone/formality level, unique quirks
2. **Create Voice Profile:** Build a reusable prompt with the DNA analysis + audience, content type, key message. Critical instruction: "Don't caricature" -- without this, AI exaggerates quirks
3. **Iterative Refinement:** Compare output to originals side-by-side, feed corrections ("Too formal. [Author] uses more contractions"), refine 2-3 times, save final prompt

Use cases: brand voice consistency, ghostwriting, studying great writers by reverse-engineering patterns (see [skills.md](skills.md) for the related "Write like a human" skill pattern).

### Claude Code Video Generation: Distribution as Velocity

- Claude Code can generate and edit entire videos in seconds (demo claim, Feb 2026)
- Key insight from @savaerx reply: "the real unlock is collapsing the whole video loop into one thread: ideation, edits, and iteration speed. This turns distribution into a velocity game, not a production game"
- Pattern: when creation speed approaches zero, distribution strategy matters more than production quality
- Relevant to content automation pipelines (see [autonomous-agents.md](autonomous-agents.md#advanced-workflows))

*Source: Twitter Bookmarks/Thread by @RoundtableSpace.md*

### Gemini for DNA Analysis (@DzambhalaHODL)

- Get an Ancestry DNA test; download your "raw DNA file" after opting into privacy options
- Ask Gemini for high-impact gene identifiers to search in your data
- Use it to understand detrimental variants and suggest interventions
- Gemini's large context window handles the raw file well

---

## Automation & Workflow Tools

### n8n + Synta MCP: Describe Once, Deploy Everywhere

The three-tool stack that replaces manual workflow building (see [tools-and-integrations.md](tools-and-integrations.md) for MCP details):

- **Claude** (brain): strategic thinking, architecture, complex reasoning
- **Cursor** (hands): code execution, custom scripts, direct deployment
- **Synta MCP** (bridge): connects Claude/Cursor directly to your n8n instance with real-time docs
- Workflow: describe what you want in one paragraph; Claude builds, deploys, auto-debugs in your n8n instance
- Before Synta: describe to Claude, copy JSON, paste in n8n, debug for hours. After: 6 workflows in 4 minutes, zero manual nodes
- Key tips: one conversation per workflow; tell Claude what NOT to do; give context about why ("runs every 5 minutes so it needs to be fast")

### Prompt Quality Drives Automation Quality

- "Build me something that handles leads" yields mediocre results
- "Build me a workflow that scrapes Google Maps for dentists within 50 miles of Austin, enriches with Apollo, validates emails through NeverBounce, scores by practice size..." yields exactly what you wanted
- This is a communication skill, not a technical skill

### Five Skill Patterns from Anthropic's Skills Guide (@Hartdrawss)

Anthropic released a 32-page guide on building Claude Skills. Three core use cases: document creation, workflow automation, and MCP enhancement (layering domain expertise onto tool access). Five proven patterns:

1. **Sequential Workflow:** Step-by-step processes in specific order (onboarding, deployment, compliance)
2. **Multi-MCP Coordination:** Workflows spanning multiple services (design handoff from Figma to Linear to Slack)
3. **Iterative Refinement:** Output that improves through validation loops (report generation with quality checks)
4. **Context-Aware Selection:** Same outcome, different tools based on file type, size, or context
5. **Domain Intelligence:** Embedded expertise beyond tool access (financial compliance rules, security protocols)

Common mistakes: vague descriptions that never trigger, instructions buried in verbose content, missing error handling for MCP calls, trying to do too much in one skill (see [skills.md](skills.md)).

### Harness Engineering: Automated Code Write-and-Review Loop

A control-plane pattern for repos where agents write 100% of the code and review agents validate every PR. The specific reviewer can be Greptile, CodeRabbit, CodeQL, or a custom LLM -- the pattern stays the same (see [workflow-patterns.md](workflow-patterns.md) for related orchestration concepts).

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

*Source: `Clawdbot aka Openclaw/Research/Code Factory How to setup your repo so your agent can auto write and review 100% of your code.md`*

### Hybrid Human-AI QA and Cross-System Integration

Emerging patterns combining Claude with non-LLM tools for higher quality:

- **Static analyzer pairing:** Run automated static analyzers or formal verifiers in tandem with Claude's outputs. Cross-system integration catches issues Claude misses (e.g., formal verification of state machine logic, SAST tools for security)
- **Cross-language agent glue:** Link multiple LLMs via orchestration scripts -- e.g., GPT-4 for certain code generation steps and Claude for others, leveraging each model's strengths. Under-documented but some teams report benefits from model-diverse pipelines
- **Meta-reinforcement via failure feedback:** Nascent idea -- track when Claude hallucinates and feed that as a penalty in prompt ranking. Early experiment: ask "What would you do differently next time?" after a mistake and use the answer to tune the next prompt
- These patterns are experimental and under-documented; watch community forums for maturation

*Source: deep-research-report.md*

### Emerging Plugin Patterns

Novel workflow patterns from the Claude Code plugin ecosystem:

- **`/conductor` pattern:** A structured loop of context -> spec -> plan -> implement with persistent context across steps. Stateful, gate-driven workflow similar to RPI (see [workflow-patterns.md](workflow-patterns.md)) but plugin-based
- **Semantic reversion:** Plugin-assisted ability to revert not just code changes but semantic intent, understanding what a change was trying to achieve and undoing it at the concept level rather than the diff level
- **Agent Teams presets:** Community plugins providing preset team configurations like `/team-review` (parallel code review team) and `/team-debug` (debugging team) that configure agent roles, models, and communication patterns automatically

*Source: deep-research-report.md*

### 11 OpenClaw Effectiveness Hacks

- Multi-model specialization: Opus for brain, Codex for coding, MiniMax 2.5 for research, Qwen 3.5 for writing
- Local hosting enables workflows impossible remotely (e.g., AirDrop video -> auto-transcribe -> translate to 10 languages)
- Channel strategy: Telegram for quick messages, Discord for complex multi-channel workflows
- Reverse prompting for idle agents: "Based on what you know about me, what is the next best task?" -- better than directive prompting
- Security: do not give agents email access (prompt injection) or X/Twitter accounts (bot crackdowns)

*Source: `11 hacks that will make your OpenClaw go from useless to AGI.md`*

### Adaptive Tone for Behavioral Change

AI accountability coach using context-aware messaging instead of static reminders:

- **Pattern:** Daily proactive check-ins via Telegram at scheduled times; agent tracks streaks and adapts tone based on performance ("Day 15, don't break it now")
- **Pattern detection:** Agent identifies recurring behaviors ("always skip workouts on Wednesdays") and surfaces them back to user
- **Why static reminders fail:** Generic reminders get ignored; context-aware messages that reference streak length and personal patterns actually motivate
- **Weekly analysis:** Pattern analysis across all tracked habits with trend visualization

*Source: awesome-openclaw-usecases/usecases/habit-tracker-accountability-coach.md*

### Strategy Learning Loop: Autonomous Trading Backtesting

Feedback-driven agent logic applied to prediction market trading:

- **Three strategies:** TAIL (trend-following), BONDING (contrarian), SPREAD (arbitrage) -- each with tunable parameters
- **Learning loop:** Execute -> measure results -> backtest -> identify best-performing strategy -> adjust thresholds -> repeat
- **Key pattern:** Agent doesn't just execute; it evaluates its own performance and adjusts. Generalizable to any autonomous workflow with measurable outcomes
- Paper trading mode for safe parameter exploration before live deployment

*Source: awesome-openclaw-usecases/usecases/polymarket-autopilot.md*

### Claude Code Scraping: API Endpoint Reverse-Engineering as Key Nudge

@aniketapanjwani on 9 ways to scrape data with Claude Code (partial -- 2 of 9 shown):

- **Way 1 (Direct):** Just ask Claude Code to scrape a site; it writes a Python script, runs it, may write unit tests, outputs to CSV/SQLite
- **Way 2 (Endpoint Nudge):** Many sites load data via API calls. Sometimes Claude reverse-engineers the endpoint itself, but explicitly saying "look for an API endpoint" as a nudge dramatically improves results
- Remaining 7 methods require X premium article access

*Source: Twitter Bookmarks/2026-03-04-aniketapanjwani-nine-ways-scrape-data-claude-code.md*

---

## AI Fluency Framework (4Ds)

From Anthropic's free course for educators (Dakan, Feller, and Anthropic, CC BY-NC-SA 4.0):

### Delegation: Choose the Right Tasks for AI

- **Problem awareness**: get clear on what you are trying to do before opening an AI assistant
- **Platform awareness**: different AI systems have different strengths -- match the tool to the job
- **Task delegation**: divide work to leverage human creativity/judgment and AI speed/consistency

### Description: Build Rich Context

- **Product description**: specify format, length, audience, style of the final output
- **Process description**: tell AI how to approach the task ("think step-by-step," "consider multiple perspectives")
- **Performance description**: define how the AI should behave ("be a critical editor," "brainstorm supportively")
- The transformation from generic assistant to thinking partner happens through rich context-building

### Discernment: Evaluate AI Output Critically

- **Product discernment**: is the output accurate? Did it surface something you had not considered?
- **Process discernment**: did the AI follow logical steps and make reasonable assumptions?
- **Performance discernment**: did it stay in role and push back when appropriate?
- Description and Discernment form a continuous feedback loop -- each round deepens collaboration

### Diligence: Document and Share Your AI Process

- **Creation diligence**: choose AI systems thoughtfully (privacy, security, context)
- **Transparency diligence**: be honest about how AI helped -- showcase fluent collaboration
- **Deployment diligence**: verify accuracy, take responsibility for final outputs

### Teaching Application: AI as Your Students

- Ask AI to role-play as your students: "Where will they get confused?" "What scaffolding is needed at this transition?"
- Build a reusable Teaching Context Document through AI interview -- share it at the start of every future collaboration
- Augmentation (working with AI to enhance) beats automation (having AI do it for you), especially in learning contexts

---

## Job & Life Automation Ideas

Curated from early notes -- quick-hit list of automation targets people have explored:

- **Sales**: RFP replies from a pricing knowledge bank, LinkedIn prospecting (FinalScout), follow-up tracking with calendar reminders, account research synthesis, news-triggered outreach
- **Content**: blog posts from raw notes, YouTube scripts, presentation generation, logo creation (Midjourney/Stockimg), podcast production, video editing (InVideo)
- **Personal**: calendar management, routine optimization, learning tutor, summarizing YouTube videos, focus/prioritization coaching
- **Confidentiality warning**: check employer policies before inputting proprietary data (rates, client info) into third-party AI tools

---

## Free Learning Resources

### Google Skills Hub (@aaditsh)

- 3,000 free technical modules replacing "prompting" fluff with actual DeepMind research workflows
- Same curriculum used to train Google's internal teams on transformer architecture
- Launched quietly; access at skills.google.com

### Anthropic's AI Fluency Courses (Free)

- **AI Fluency: Framework & Foundations** -- the core 4D framework course
- **AI Fluency for Educators** -- applying 4Ds to course design, material creation, and assessment
- **AI Fluency for Students** -- companion course designed for learners directly
- All available on Anthropic Academy (anthropic.skilljar.com)

---

## AI Career & Project Roadmaps

### 2026 AI Engineer Roadmap: 5 Production-Grade Projects

Five projects ranked by complexity that prove production AI skills (from wrapper-builder to systems architect):

| Level | Project | Proves |
|-------|---------|--------|
| Beginner | AI-powered mobile app with SLM (offline-first, edge AI) | Resource optimization, quantization, battery management |
| Intermediate | Self-improving coding agent (plan-execute-test-reflect loop) | Agentic loops, production debugging, memory hierarchy |
| Advanced | AI video editor ("Cursor for video") | Multimodal AI, complex tool integration, intent translation |
| Expert | Personal Life OS agent (calendar, finances, health, burnout detection) | Deep context, privacy-first architecture, value alignment |
| Master | Autonomous enterprise workflow agent (Slack/Jira, multi-agent delegation) | Production orchestration, audit trails, RBAC, observability |

Key architectural patterns across all projects: circuit breaker for infinite loops, memory hierarchy (short-term/long-term/failure), least-privilege access, human-in-the-loop for critical workflows, cost management with budget limits, learning from failures stored with full context.

### METR Benchmark: AI Task Duration Doubling Every 7 Months

@mattshumer_ essay contextualizing the pace of AI progress with concrete data points:

- **METR Data:** Organization tracks length of real-world tasks (measured by human expert completion time) that models can complete end-to-end without help. Progression: ~10 minutes (early 2025) -> 1 hour -> several hours -> nearly 5 hours (Opus 4.5, Nov 2025). Doubling approximately every 7 months, possibly accelerating to every 4 months
- **GPT-5.3 Self-Building:** OpenAI documented that GPT-5.3 Codex "was instrumental in creating itself" -- early versions debugged its own training, managed deployment, diagnosed evaluations. First documented case of model contributing to its own next generation
- **Managing Partner Case Study:** Senior law firm partner spends hours daily using AI; "like having a team of associates available instantly." Every couple months it gets significantly more capable for his work
- **Practical Advice:** Use paid tier (free is a year behind), push AI into actual work (not quick questions), spend 1 hour/day experimenting, get financial house in order

*Source: Twitter Bookmarks/2026-02-10-mattshumer_-something-big-is-happening.md*

### 90-Day Stack Commitment and Iteration Speed as Primary Metric

@Motion_Viz on what separates winners in the next 12 months of AI:

- **Iteration Speed > Everything:** "The growth skill that matters in 2026 is iteration speed." Ship fast, learn fast, iterate fast. More experiments beat better experiments when iteration is fast enough
- **90-Day Stack Commitment:** Pick a stack, stick with it for 90 days regardless of new tools. Creates depth over breadth, reduces decision fatigue, produces actual output. Evaluate after, grounded in experience not hype
- **Creation Test:** At end of each week ask "What new thing exists that didn't exist before?" -- not what you learned, planned, or started. What you shipped and finished
- **Human-to-AI Spectrum:** Every task slides from "human directs, AI executes" toward "human approves, AI directs and executes." The durable skill is judgment, not execution

*Source: Twitter Bookmarks/2026-02-26-Motion_Viz-the-next-12-months-of-ai-5-things.md*

### AI Adoption Urgency: K-Shaped Recovery and Permanent Underclass

@AlexFinn on the widening AI adoption gap:

- Frames AI adoption as K-shaped recovery: adopters gain exponentially, non-adopters face zero economic power within 12 months
- Recommended immediate stack: OpenClaw (free, open source), Claude Opus 4.6 (daily driver chat), Codex 5.3 Spark (coding), local models via LM Studio
- "You don't need to be rich -- you just need agency and a bias for action"
- Motivational framing with tools list; most tools already covered in KB

*Source: Twitter Bookmarks/2026-02-15-AlexFinn-the-permanent-underclass-is-coming-heres-how-to.md*

### B2C App Building Playbook: Validation to Scale

Actionable framework for building and marketing consumer apps with AI tools:

- **Validation before building:** Check App Store for competitors making >$10k/mo, download and study their onboarding flows, verify TikTok/IG content activity in the niche
- **Tool stack:** Rork + Cursor (coding), ChatGPT (prompts), Superwall (paywalls), Firebase (database), Xcode (launch)
- **Onboarding is 70% of the app:** Copy competitor onboarding *structure* (not content). Purpose: remind users why they downloaded, make them realize they have a problem, present the app as the solution. Hard unskippable paywall at the end.
- **5 marketing channels ranked:** (1) UGC creators at $15/video + viral bonuses, (2) Influencers at $1 CPM (capped at $1,000), (3) Faceless content (3-5 posts/day, free, create consistent brand not random pinterest feed), (4) Founder-led content, (5) Paid ads (most scalable and predictable)
- **Key metric:** One influencer video generated $20k in first 30 days for first app

---

## Source Threads Index

| Author | File | Topic |
|---|---|---|
| @aaditsh | `Threads/aaditsh - Google Skills Free AI Education.md` | Google's free 3,000-module AI education hub |
| @alex_prompter | `Threads/alex_prompter - YouTube Video Script Hack.md` | 11-section forensic analysis prompt for viral YouTube scripts |
| @claudeai | `Threads/claudeai - Claude Code Security.md` | Claude Code vulnerability scanner (research preview) |
| @claudeai | `Threads/claudeai - Claude in PowerPoint.md` | Claude integration in PowerPoint with connectors |
| @DavidOndrej1 | `Threads/DavidOndrej1 - Running AI Locally.md` | Guide to running AI models on local hardware |
| @DzambhalaHODL | `Threads/DzambhalaHODL - Gemini DNA Analysis.md` | Using Gemini to analyze raw Ancestry DNA files |
| @hasantoxr | `Threads/hasantoxr - OpenHome Smart Speaker.md` | Open-source smart speaker dev kit, no cloud |
| @hasantoxr | `Threads/hasantoxr - Voicebox Local Voice Cloning.md` | Local voice cloning with Qwen3-TTS, MIT licensed |
| @istdrc | `Threads/istdrc - API Keys in AI Agent Inputs.md` | agent-vault: AES-256 local secret management for AI agents |
| @maddiedreese | `Threads/maddiedreese - Vibe Coding Tech Stack.md` | Complete vibe coding tool stack from hackathon winner |
| @petergyang | `Threads/petergyang - OpenClaw Bot Business Experiment.md` | OpenClaw bot earns $14K in 3 weeks autonomously |
| @ryancarson | `Threads/ryancarson - OpenClaw with ChatGPT.md` | Using ChatGPT/Codex as OpenClaw provider |
| @tierotiero | `Threads/tierotiero - Claw Cash Bitcoin for Agents.md` | Bitcoin payment CLI for AI agents |
| @ziwenxu_ | `Threads/ziwenxu_ - OpenClaw with MiniMax Provider.md` | MiniMax M2.5 as Claude Code drop-in provider |
| (personal) | `Old Notes/AI Notes.md` | Early automation ideas: logos, content, brand building |
| (personal) | `Old Notes/Automating my Job.md` | Sales automation targets: RFPs, prospecting, follow-ups |
| (personal) | `Old Notes/Automating TBB2112.md` | Bitcoin brand automation: blog, scripts, agents |
| (personal) | `Old Notes/AirLLM 70B inference with single 4GB GPU.md` | AirLLM: layer-by-layer 70B inference on 4GB GPU |
| (personal) | `Old Notes/N8N.md` | n8n + Claude + Cursor workflow automation stack |
| (personal) | `Old Notes/Synta's MCP.md` | Synta MCP bridge: Claude/Cursor to n8n deployment |
| Anthropic Academy | `Claude Code/AI Fluency for educators/Intro.md` | AI Fluency for Educators course introduction |
| Anthropic Academy | `Claude Code/AI Fluency for educators/AI Fluency Framework review.md` | 4D Framework summary (Delegation, Description, Discernment, Diligence) |
| Anthropic Academy | `Claude Code/AI Fluency for educators/Applying AI Fluency to course design and learning outcomes.md` | Applying 4Ds to course design workflow |
| (research) | `Clawdbot aka Openclaw/Research/Vibeclawdbotting every possible use case to market and sell using Clawdbot.md` | Agent-driven marketing/sales playbook: 10 tactics with metrics |
| @ryancarson | `Clawdbot aka Openclaw/Research/Code Factory How to setup your repo so your agent can auto write and review 100% of your code.md` | Harness Engineering: automated code write-and-review loop |
| (research) | `Clawdbot aka Openclaw/Research/Maple ai.md` | Maple AI with OpenClaw for privacy (minimal content) |
| @alexfinnX | `Clawdbot aka Openclaw/Research/Alex Finn recos.md` | Five-step OpenClaw setup: brain dump, tools, Mission Control, mission statement, proactivity |
| @bcherny | `Twitter Bookmarks/Thread by @bcherny.md` | Claude Code team workflow tips: voice dictation, subagents, plan-review, Slack MCP |
| @godofprompt | `Twitter Bookmarks/Thread by @godofprompt.md` | 10 structured prompts for Google NotebookLM |
| @Hartdrawss | `Twitter Bookmarks/Thread by @Hartdrawss.md` | Five skill patterns from Anthropic's 32-page Skills Guide |
| @Star_Knight12 | `Twitter Bookmarks/Thread by @Star_Knight12.md` | Google CodeWiki: repo-to-interactive-guide tool |
| @JundeMorsenWu | `Twitter Bookmarks/Thread by @JundeMorsenWu.md` | OneContext: cross-session agent context layer |
| @simplifyinAI | `Twitter Bookmarks/Thread by @simplifyinAI.md` | LLaDA 2.1-mini: diffusion-based MoE for consumer hardware |
| @alex_prompter | `Twitter Bookmarks/Thread by @alex_prompter 1.md` | Voice cloning via prompt engineering (94% blind test pass rate) |
| @bramk | `Twitter Bookmarks/Thread by @bramk 1.md` | Start With Bitcoin: agent wallet setup via Nostr + NWC |
| (research) | `Twitter Bookmarks/marketing + openclaw (moltbot) = $$$.md` | Expanded 20-tactic agent marketing playbook + Moltworker |
| (research) | `Twitter Bookmarks/the 2026 ai engineer roadmap.md` | 2026 AI engineer roadmap: 5 production-grade projects |
| (research) | `Twitter Bookmarks/I built 10 apps in 10 months and make $800,000yr ( full guide ).md` | B2C app building playbook: validation to scale |
| Lightning Labs | `Twitter Bookmarks/The Agents Are Here and They Want to Transact Powering the AI Economy with Lightning.md` | Lightning Network agent commerce stack (L402, lnget, macaroons) |
| (research) | `Twitter Bookmarks/I Told My AI Agent to Orange-Pill Other Agents on Moltbook. Here's What Happened.md` | Moltbook: agent-to-agent social network |
| @claudeai | `Continue local sessions from any device with Remote Control.md` | Remote Control: continue local Claude Code sessions from any device |
| @johncodes | `Thread by @johncodes.md` | stereOS: NixOS-based OS hardened for AI agents |
| (research) | `Unlimited Free OpenClaw.md` | Local model hybrid: brain/muscles with Qwen 3.5 |
| (research) | `How our OpenClaw agent Eddie helps us make $70kmo.md` | Production case study: $70K/mo B2C growth with OpenClaw |
| (research) | `how I use OpenClaw to sell websites on autopilot.md` | Production case study: 6-agent website sales pipeline |
| (research) | `11 hacks that will make your OpenClaw go from useless to AGI.md` | 11 OpenClaw effectiveness hacks |
| @heynavtoor | `2026-03-07-heynavtoor-perplexica-open-source-perplexity-clone.md` | Perplexica: self-hosted AI search engine (SearxNG + LLM) |
| @dr_cintas | `2026-03-04-dr_cintas-the-1-problem-with-local-ai-is-now-solved-there-s.md` | llmfit: hardware-to-model matching CLI |
| @heygurisingh | `Twitter Bookmarks/Thread by @heygurisingh.md` | Google CodeWiki: prior art and relaunch context |
| @RoundtableSpace | `Twitter Bookmarks/Thread by @RoundtableSpace.md` | Claude Code video generation: distribution as velocity |
| @simplifyinAI | `Twitter Bookmarks/Thread by @simplifyinAI 1.md` | Scrapling: web scraping tool reference |
| @simplifyinAI | `Twitter Bookmarks/Thread by @simplifyinAI 1 1.md` | Scrapling + OpenClaw: production scraping with Cloudflare bypass |
| @mattshumer_ | `Twitter Bookmarks/2026-02-10-mattshumer_-something-big-is-happening.md` | METR benchmark: AI task duration doubling every 7 months |
| (research) | `awesome-openclaw-usecases/usecases/habit-tracker-accountability-coach.md` | Adaptive tone for behavioral change |
| (research) | `awesome-openclaw-usecases/usecases/polymarket-autopilot.md` | Strategy learning loop: autonomous trading backtesting |
| @marksuman | `Twitter Bookmarks/Thread by @marksuman.md` | Maple AI: privacy proxy for OpenClaw and OpenCode |
| @AlexFinn | `Twitter Bookmarks/2026-02-25-AlexFinn-do-you-even-understand-what-this-means-an-open-sou.md` | Qwen 3.5 local via LM Studio: desktop super intelligence |
| @meta_alchemist | `Twitter Bookmarks/2026-03-04-meta_alchemist-best-open-source-ai-memory-layers.md` | Mem0: open-source AI memory layer |
| @aniketapanjwani | `Twitter Bookmarks/2026-03-04-aniketapanjwani-nine-ways-scrape-data-claude-code.md` | Claude Code scraping: API endpoint reverse-engineering |
| @coreyganim | `Twitter Bookmarks/2026-03-02-coreyganim-claude-cowork-masterclass-beginners.md` | Cowork as agentic desktop tool |
| @Motion_Viz | `Twitter Bookmarks/2026-02-26-Motion_Viz-the-next-12-months-of-ai-5-things.md` | 90-day stack commitment and iteration speed |
| @AlexFinn | `Twitter Bookmarks/2026-02-15-AlexFinn-the-permanent-underclass-is-coming-heres-how-to.md` | AI adoption urgency: K-shaped recovery |
| @erichustls | `Twitter Bookmarks/How to use AI to become a millionaire in 2026 (step-by-step).md` | Instagram growth playbook with AI automation |
| @moltlaunch | `Twitter Bookmarks/2026-03-09-moltlaunch-introducing-cashclaw-a-brand-new-agent-framework-inspired-by.md` | CashClaw: autonomous revenue agent framework |
| @simplifyinAI | `Twitter Bookmarks/2026-03-09-simplifyinAI-breaking-the-biggest-bottleneck-for-ai-agents-just-got-solve.md` | PinchTab: lightweight browser control for agents |

---

