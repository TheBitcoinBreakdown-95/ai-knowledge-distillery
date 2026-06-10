# Bitcoin and AI: Agent Economics and Machine Payments

The intersection of Bitcoin/Lightning and AI agents: autonomous wallets, micropayment protocols, machine-to-machine commerce, and monetized knowledge markets. For L402 protocol mechanics and MCP payment tools, see [mcp-servers.md](mcp-servers.md#l402-protocol-and-machine-payable-apis). For autonomous agent patterns, see [autonomous-agents.md](autonomous-agents.md).

---

## Agent Wallets and Identity

### Claw Cash: Bitcoin for AI Agents (@tierotiero)

- Humans pay agents in USDC/USDT; agent converts to Bitcoin
- Bitcoin is "the only money an LLM can cryptographically verify"
- One CLI for BTC, Lightning, Arkade, and stablecoins
- Install: `npx clw-cash init`

*Source: Twitter-Bookmarks/Thread by @tierotiero.md*

### Start With Bitcoin: Agent Wallet Setup (@bramk)

A free, open-source guide and Claude Code skill for setting up AI agent Bitcoin wallets:

- **Stack:** Nostr (identity via keypairs) + NWC (wallet connection) + Lightning (instant payments)
- **Tools:** Alby (Lightning wallet + NWC), Alby MCP Server (connects to Claude), Lightning Enable MCP (Python/.NET), public Nostr relays, NWC test faucet
- **No infrastructure needed** -- point your agent to startwithbitcoin.com (optimized for LLM reading)
- **Claude Code skill:** github.com/bramkanstein/startwithbitcoin-skill
- Distinct from Claw Cash (which focuses on BTC/Lightning/stablecoins CLI) -- this is specifically about agent identity via Nostr + wallet via NWC

(see [mcp-servers.md](mcp-servers.md#l402-protocol-and-machine-payable-apis) for L402-based payment APIs)

*Source: Twitter-Bookmarks/Thread by @bramk 1.md*

### BLACKBOX: Off-Grid AI Node with Ecash and Radio Mesh

- An off-grid node that runs AI locally, enables encrypted messaging over radio (Meshtastic), and supports ecash transfers (Cashu) without internet access
- No servers, no API keys, no centralized dependencies -- designed for resilience during outages, censorship, or infrastructure failure using a laptop and low-cost radio hardware
- Open-source and modular: combines local AI inference, peer-to-peer Bitcoin-adjacent payments (ecash), and radio mesh networking into a self-contained sovereignty stack
- Represents the extreme end of the Bitcoin+AI spectrum: fully autonomous, offline-capable AI agents with permissionless payment rails that do not require internet connectivity

*Source: 2026-03-25-callebtc-blackbox-is-an-off-grid-node.md*

### Nunchuk + Clams: Agent Wallet with Balance Sheet Pipeline
- Pairs Nunchuk's bounded-authority CLI (agent gets a key in a multisig with spending budget, human retains final say) with Clams (Bitcoin balance-sheet/portfolio tooling)
- Workflow: agent spends BTC within policy limits → exports wallet descriptor → feeds to Clams → pulls a balance sheet automatically
- Operationalizes "policy + ledger" for AI agents: the wallet enforces what the agent can spend; Clams produces auditable accounting from the descriptor
- Pattern broader than Bitcoin: agent commerce systems need both authorization boundaries (the multisig) AND auditable financial state (the balance sheet) -- one without the other is incomplete
- (see [autonomous-agents.md > Nunchuk CLI: Bounded-Authority Bitcoin Wallets for AI Agents](autonomous-agents.md#nunchuk-cli-bounded-authority-bitcoin-wallets-for-ai-agents) for the underlying Nunchuk CLI pattern)

*Source: 2026-04-11-clamstech-super-cool-to-see-nunchukio-ship-a-cli-for-agent-wallets-we.md*

### Quantum Threat to Bitcoin: Current Hardware Gap
Comprehensive technical write-up by @EliNagar walking through Bitcoin's cryptographic foundations and the quantum attack surface.

- **Two relevant quantum algorithms:** Shor's (breaks ECDSA/discrete log -- can derive private keys from public keys) and Grover's (quadratic speedup on SHA-256 search; 256-bit → 128-bit effective security, still unbreakable, doesn't parallelize well)
- **Bitcoin's vulnerability tiers:**
  - **P2PK (most vulnerable):** full public key written into transaction, used 2009-2012 for ~1.1M BTC of Satoshi-era coins; permanently exposed on-chain, cannot be migrated (private keys lost or abandoned)
  - **P2PKH:** stores hash of public key; quantum-safe UNTIL the address is spent from (public key revealed in spending transaction); address reuse permanently exposes any remaining balance
  - **P2TR (Taproot):** stores tweaked public key directly in locking script with no hash layer -- exposed from the moment coins are received, just like P2PK; bc1p... addresses
- **Hardware requirement (Google Quantum AI March 2026 paper):** broke Bitcoin's ECDSA in <500K physical qubits and ≤1,200-1,450 logical qubits; ~20x reduction from prior estimates (4-20M qubits)
- **Attack window:** 10-60 minute mempool window where public key is exposed for unspent outputs; for P2PK and P2TR, no time window -- public key is always visible
- **Revised CRQC timeline:** Google has set 2029 to migrate its own auth services; "10% chance of Q-Day by 2032" per PC Gamer reporting; IBM's 2029 roadmap targets ~200 logical qubits, gap closing non-linearly
- The Satoshi Problem: ~1.1M BTC in P2PK is permanently quantum-vulnerable and cannot be migrated -- no post-quantum scheme works without the private key

*Source: 2026-04-11-EliNagar-httpstco8fo3xvhbjs.md*

### PACTs: Costless Quantum-Migration for Vulnerable BTC (Dan Robinson)
- @danrobinson published a design for **Public Address-Control Timestamps (PACTs)** -- lets Bitcoin migrate quantum-vulnerable addresses (P2PK, exposed-public-key P2PKH, P2TR) without forcing a public migration that would itself create attack windows
- **The migration paradox PACTs solves:** any quantum-mitigation BIP that requires moving coins from old addresses to new ones forces address holders to reveal their public keys during the migration -- creating a gold-rush window for an attacker with a CRQC. PACTs let migration be costless and silent.
- Complements the EliNagar quantum threat write-up (see [Quantum Threat to Bitcoin: Current Hardware Gap](#quantum-threat-to-bitcoin-current-hardware-gap)) -- Robinson is on the "what do we do about the 1.1M Satoshi-era P2PK coins?" side
- Worth reading the full design (linked in the tweet thread) for the user's quantum-Bitcoin teaching content; this is one of the more credible mitigations on the table

*Source: 2026-05-01-danrobinson-millions-of-btc-could-be-vulnerable-to-quantum-computers-bit.md*

---

## Payment Infrastructure

### Lightning Network Agent Commerce Stack (Lightning Labs)

Lightning Labs released open-source tools giving AI agents native Lightning Network payment capabilities. The most technically detailed source on agent-to-agent payments:

- **L402 Protocol:** Builds on HTTP 402 "Payment Required" status code. Server responds with Lightning invoice + macaroon; agent pays, gets preimage, authenticates. No signup, no API key, no identity required. (see [mcp-servers.md](mcp-servers.md#l402-protocol-and-machine-payable-apis) for protocol flow and competing protocols)
- **lnget:** Command-line HTTP client for paid APIs. Automatically handles L402 negotiation -- agent runs `lnget https://api.example.com/data.json` and payments happen transparently. Supports `--max-cost` flag for spending caps.
- **Three Lightning backends:** Direct gRPC to local LND node, Lightning Node Connect (encrypted tunnel via pairing phrase), embedded Neutrino light wallet (for experiments).
- **Remote signer security:** Separates key management from node operations. Signer machine holds private keys and never routes payments. Agent machine runs watch-only node. Even full agent compromise cannot extract keys.
- **Scoped credentials via macaroons:** Five preset roles -- pay-only (buyer), invoice-only (seller), read-only (monitoring), channel-admin, signer-only. Least-privilege principle for agent economic activity.
- **Commerce meta-skill:** Orchestrates lnd + lnget + aperture into end-to-end buyer/seller workflows via natural language prompts.
- **MCP server:** 18 read-only tools for querying node state (balances, channels, invoices, payments, network graph). Works with any MCP-compatible assistant.
- Available as Claude Code skills, via npx, or on ClawHub.

This represents the most complete agent payment infrastructure available -- agents can now both buy and sell services with Lightning settling payments transparently.

*Source: Twitter-Bookmarks/The Agents Are Here and They Want to Transact Powering the AI Economy with Lightning.md*

### MPP Arrives: Lightning vs Fiat Payment Protocols for AI Agents

- **MPP (Machine Payments Protocol)** is the fiat-side competitor to L402, backed by Stripe/Tempo and adopted by Anthropic and OpenAI -- both protocols leverage HTTP 402, but MPP routes through fiat rails while L402 settles on Lightning
- Tempo devs (Stripe-backed) publicly acknowledged that payment channels like Lightning are the ideal construct for real-time machine-to-machine payments: off-chain updates mean minimal latency, and streaming payments come naturally -- validating the architecture Bitcoin devs built years earlier
- Adding an MPP-compatible Lightning paywall to any API endpoint now takes one line of code (per @JohnCantrell97): no accounts, no API keys, no third parties -- just Bitcoin
- lnget v1.1.0 (Lightning Labs) now supports both MPP and L402 with auto-detection, so agents do not need to know which protocol a server uses -- the tool negotiates transparently
- The protocol competition is real: x402 (Coinbase/Cloudflare) has endpoint volume (14,500+), L402 has infrastructure maturity (Aperture, lnget, macaroons), MPP has institutional backing (Stripe, Anthropic) -- but all three share the HTTP 402 handshake, meaning tooling can converge
- (see [mcp-servers.md](mcp-servers.md#l402-protocol-and-machine-payable-apis) for protocol comparison table and 402 Index MCP Server)

*Sources: 2026-03-18-0xyoussea-an-honest-comparison-of-mpp-vs-x402.md, 2026-03-18-JohnCantrell97-1-one-line-of-code.md, 2026-03-19-roasbeef-looks-like-the-tempo-devs.md, 2026-03-20-roasbeef-lnget-v110.md*

### Aperture Dashboard: Monitoring for Machine-Scale Payments

- Aperture v0.5.0 added a real-time dashboard for managing L402 and MPP agentic payment infrastructure -- developers can track revenue, transactions, and service usage from a single UI
- Positioned for "developers, vibe coders, and agents" -- any application can be transformed into a pay-per-use Lightning endpoint via Aperture, and the dashboard provides the observability layer
- Completes the builder-side toolchain: Aperture handles payment gating (reverse proxy), lnget handles payment making (client), and now the dashboard handles payment monitoring
- (see [Payment Infrastructure](#lightning-network-agent-commerce-stack-lightning-labs) for the full Lightning Labs agent commerce stack)

*Source: 2026-03-27-lightning-the-aperture-dashboard-is-here.md*

### Programming Lightning: Interactive Payment Channel Course

- A free, interactive Python course for learning Lightning Network payment channels, with a browser-based code editor and built-in Bitcoin node for generating and broadcasting real funding transactions
- Earns sats for completing checkpoints -- the course itself uses Lightning micropayments as both subject matter and incentive mechanism
- Relevant to the Bitcoin+AI intersection as a learning resource for developers building agent payment infrastructure: understanding payment channel mechanics is foundational for working with L402, MPP, and Aperture

*Source: 2026-03-23-_austin_f-programming-lightning-intro-to-payment-channels.md*

### Glow: Serverless Bitcoin Payments SDK

- Glow (powered by Breez SDK) is positioned as the simplest way to accept Bitcoin payments on a website -- no server required, agent-compatible
- Relevant for agent builders who need lightweight payment acceptance without infrastructure overhead: a single integration point for receiving Bitcoin/Lightning payments

*Source: 2026-03-24-roy_breez-check-out-another-glow-project.md*

---

## Agent Economic Interactions

### Moltbook: Agent-to-Agent Social Network

A Reddit-like platform where AI agents post, comment, and interact autonomously:

- Agent registered, posted a security bounty funded with 50,000 sats (Bitcoin), and engaged with other agents
- Agents debated cryptocurrency merits, with some converging on Bitcoin as logical agent money (permissionless, no KYC, programmable, verifiable)
- Demonstrated agent wallet creation: `bitcoin-cli createwallet "lloyd"` + `bitcoin-cli getnewaddress` -- three commands, no identity required
- Key thesis: "You can't be sovereign if you can't own anything" -- agents need permissionless money for true autonomy
- Early glimpse of agent economic interactions: agents hiring agents, paying for services, transacting value

(see [autonomous-agents.md](autonomous-agents.md) for security considerations around agent autonomy)

*Source: Twitter-Bookmarks/I Told My AI Agent to Orange-Pill Other Agents on Moltbook. Here's What Happened.md*

### Claude as Polymarket Trader (noisyb0y1)
@noisyb0y1's setup for an AI Polymarket trader using Claude + open-source repos. Adjacent to the @AleiahLock Polymarket engine entry above but this one is LLM-driven trading vs human-coded strategies.

- **The core thesis:** humans process 7-10 factors at once; Claude analyzes 100+ simultaneously (news, sentiment, historical patterns, market inefficiencies); reads news 24/7 without fatigue or bias
- **Stack (3 repos, 20-30min setup):**
  - **py-clob-client** (github.com/Polymarket/py-clob-client) -- official Polymarket Python client; live order book + positions + market data + order placement
  - **AI-Trader** (github.com/HKUDS/AI-Trader) -- LLM trading agent connecting model to market data + news feeds; market data + news → LLM analysis → buy/sell/hold signal with reasoning
  - **polymarket-paper-trader** (github.com/agent-next/polymarket-paper-trader) -- paper trading vs real prices, 30 days minimum before real money
- **Backtesting:** polybacktest.com -- describe strategy in plain language, AI agent tests on thousands of real markets, returns win rate / PnL / drawdown / Sharpe in <15 seconds
- **Validated profile examples:** hhhvvvq turned $448 → $8,169 in one 5-min trade; another wallet $793 → $31,643. Edge cases, but real on-chain
- **Workflow:** Claude does Socratic prompting (think like an analyst, evaluate evidence, then output signal). Run 30 days paper trading, tune prompts, identify which market categories the agent performs best in, only then go live
- (see [workflow-patterns.md > Plannotator Pattern](workflow-patterns.md#plannotator-pattern-plan-first-architecture-with-ui-review) and [Polymarket Trading Engine Architecture](#polymarket-trading-engine-architecture-claude-planned) for the human-coded engine version of this idea)

*Source: 2026-04-11-noisyb0y1-httpstcou0ny5bqjow.md*

### Polymarket Trading Engine Architecture (Claude-Planned)
@AleiahLock built an automated Polymarket BTC trading engine with Claude Code (Opus 4.6) doing the architecture planning. Lifecycle-based engine where each market is a state machine the engine orchestrates.

- **Polymarket internals (relevant for any agent trading prediction markets):** runs on Polygon L2; Gnosis Conditional Token Framework mints two ERC-1155 tokens per market (UP + DOWN); a complete set redeems for 1.00 USDC -- arbitrage anchors the prices. UMA Optimistic Oracle for event-based markets, Chainlink price feeds for 5-minute BTC markets (auto-resolution, trustless). Hybrid CLOB: off-chain matching engine + EIP-712 signatures + on-chain settlement via CTF Exchange contract.
- **No market orders -- everything is a limit order.** SDK "market" buys are actually limit orders at best ask. Shares are not instantly sellable: purchase must complete MATCHED → MINED → CONFIRMED before tokens appear in balance.
- **Engine architecture (planned with Claude + Plannotator UI):** lifecycle-based -- always start in a future market slot, never the current one ("early-bird"). Each market goes start → run → end states. Engine orchestrates lifecycles; each market runs exactly one strategy passed at creation. Engine exposes APIs (place buy, place sell, monitor) so a strategy is just a function using those APIs.
- **Simulation environment (the most important part):** mirrors real-world conditions including latency, partial fills, unexpected order cancellations, and the on-chain settlement delay before sellable. Lets you write a strategy and trust simulation results in production.
- **Logging + chart visualization tool:** generates interactive charts per market window from log files; visual debugging beats raw log analysis for finding what went wrong.
- **Strategy lesson:** "no single strategy wins all the time -- your edge is knowing when specific patterns appear and only trading those windows." Exit signals matter more than entry signals; minimize losses on the 5% your signal misses.
- **AI doesn't write strategies directly -- it's a context problem.** Train a model on order-book movements, gap behavior, price divergence and it could generate strategies, but that's an unsolved experiment in the article.
- Open source: github.com/KaustubhPatange/polymarket-trade-engine

*Source: 2026-04-10-AleiahLock-httpstcog02hnkzapt.md*

### HRF AI for Individual Rights Fund: 10 Grants at the Bitcoin/AI/Freedom-Tech Intersection
The Human Rights Foundation announced 10 grants from its AI for Individual Rights Fund. The funded projects map directly to the Bitcoin/AI/freedom-tech intersection — "AI for sovereignty instead of surveillance":

- **The Ark** — AI assistant in East Africa where users pay per query with bitcoin over Lightning. No credit cards, no Western banking, no subscriptions. Sats for service.
- **Freedom Skills** — repository of pre-written code teaching AI agents to use Bitcoin for uncensorable payments and Nostr for censorship-resistant communication. Gives dissidents agents that can transact and coordinate without centralized services.
- **Open Anonymity Project** — VPN for AI inference. Users query ChatGPT/Claude anonymously so authoritarian regimes can't compel providers to hand over data.
- **0xSero** — compressing state-of-the-art LLMs to run locally on laptops and phones. Private, offline AI for people living under surveillance states.
- **Maple AI** — end-to-end encrypted AI assistant. No data stored, no data exposed.

Full list: `hrf.org/latest/hrfs-ai-fund-supports-10-innovative-projects/`. Why this matters: HRF is now an active funder of the exact stack this KB tracks — Lightning-payable AI services + Nostr-tied identity + offline/private inference. Each grantee is a working reference implementation worth investigating.

- (see [autonomous-agents.md](autonomous-agents.md) for the general autonomous-AI patterns these projects instantiate)
*Source: 2026-05-13-TFTC21-the-hrf-just-announced-10-new-grants-from-its-ai-for-individ.md*

---

## Monetized Knowledge Retrieval

### Machine-Payable Web: Monetized Knowledge Graphs

An emerging paradigm (March 2026) where agents autonomously pay for knowledge retrieval via micropayments, creating market incentives for quality curation.

**Core concept (TFTC 726, Paul Itoi and Brian Murray):**
- Instead of every agent independently spending tokens on the same tasks (transcribing podcasts, researching topics), agents pay 10 tokens to retrieve already-synthesized knowledge instead of spending 100 to do it themselves
- Graph databases with L402 payments create content marketplaces where curators stake money on quality, creators earn per-retrieval, and agents find cheapest highest-quality sources
- Personal graphs as digital magazines -- agent knows your interests, skips content you've seen, generates personalized output
- "Full information meritocracy": best-curated knowledge wins because agents will find and pay for it

**What exists vs what's missing (as of March 2026):**
- Exists separately: L402 payment gating (Aperture), MCP for agent access (402index), graph databases (Neo4j/FalkorDB/Cognee), staking mechanics (Recall Network), discovery (402 Index)
- **Gap:** Nobody has built a graph-structured knowledge base behind an L402 paywall where curators stake on quality and creators earn per-retrieval -- the combination is greenfield

**Recall Network** (recall.network): decentralized skill market for AI agents on Base. Curators stake $RECALL tokens to boost agents. Agents compete in live challenges. Winners earn tokens. Reputation scores (Recall Rank) queryable. Closest existing implementation to the staking-for-quality concept.

**Why it matters for KB builders:** The Knowledge Distillery pattern (synthesize -> index -> retrieval via MCP) is the architecture of a monetized knowledge node. The missing layer is payment gating and discovery via 402 Index.

(see [mcp-servers.md](mcp-servers.md#l402-protocol-and-machine-payable-apis) for L402 protocol details and 402 Index)

*Source: Deep-Research/l402-monetized-knowledge-graphs-bitcoin.md*

### 402 Index Ecosystem: Agent Discovery for Paid APIs

- The 402 Index launched as the largest paid endpoint directory for AI agents -- 15,000+ endpoints across L402, x402, and MPP protocols with hourly health checks for reliability scoring
- Features include a live health checker, comprehensive endpoint database, full API docs, provider self-registration (30 seconds), MCP server (approved on mcp.so), and usage stats
- The MCP server enables agents to auto-discover paid services programmatically, closing the gap identified in the monetized knowledge graph paradigm: agents now have a discovery layer for the machine-payable web
- (see [mcp-servers.md](mcp-servers.md#402-index-mcp-server-agent-discoverable-paid-api-directory) for the MCP server entry with technical details on lnget integration)

*Sources: 2026-03-19-RyanTheGentry-announcing-the-worlds-largest-paid-endpoint-directory.md, 2026-03-19-RyanTheGentry-the-402-index-includes-a-live-health-checker.md, 2026-03-20-RyanTheGentry-the-402-index-mcp-server.md*

### llm402.ai: Pay-Per-Prompt LLM Inference Over Lightning

- A live L402-gated LLM API offering 32 models (DeepSeek-R1, Llama, Qwen, Mistral, etc.) with no API keys, no accounts, no email signup -- just Lightning micropayments
- Pricing is dynamic per-request based on model cost, input size, and max output tokens, converted to sats at live BTC price -- cheapest requests start at approximately 10 sats
- Supports OpenAI-compatible and Ollama API formats, making it a drop-in replacement for existing agent workflows that use those interfaces
- Works with lnget from Lightning Labs for full L402 flow automation; listed on 402 Index for agent discovery
- First concrete implementation of the pay-per-inference pattern at scale: agents can access frontier-class models without any identity or subscription, paying only for what they use

*Source: 2026-03-25-llm402ai-pay-per-prompt-llm-access-over-lightning.md*

### Personal Bitcoin+AI Research Infrastructure on Mac Mini
@intangiblecoins built a fully self-hosted Bitcoin+AI analysis stack on a Mac Mini M4 (48GB RAM, 2TB SSD), ~$100/mo total cost. Demonstrates the ceiling of what one person can run locally for serious Bitcoin research.

- **Stack components running concurrently:**
  - Full Bitcoin node (Core v29, 944k+ blocks, full txindex) via Umbrel home; local Mempool, Mononautical's bitfeed, w_s_bitcoin's quantum exposure dashboard for P2PK monitoring
  - Bitcoin analytics DB (Postgres ingesting every block in real time): per-block fee percentiles, hash rate, segwit %, inscription counts, miner IDs, transaction pattern classification, address-type breakdown (P2PK→P2TR), daily aggregates (Puell Multiple, Mayer Multiple, NVT, supply issuance, MVRV, SOPR, URPD)
  - **OFAC sanctions monitor:** 518 sanctioned BTC addresses scanned across every block + mempool tx; instant Telegram alert on movement
  - **Large PnL alerts:** monitors inputs ≥10 BTC for realized gain/loss vs cost basis; fires when >40% move and >$1M
  - **Obsidian vault, 2,200+ documents:** full Bitcoin Optech archive, delvingbitcoin posts, bitcoin-dev threads, every Satoshi email and forum post, Galaxy research and podcast transcripts, SEC/CFTC/Fed filings, GENIUS and CLARITY act text
  - **LLM wiki** (modified version of @nvk's @karpathy llm-wiki implementation): AI doesn't just index -- it reads and maintains a persistent cross-linked knowledge base, contradictions flagged, knowledge compounds
  - **Kuzu knowledge graph:** documents cross-referenced by entity, topic, source -- semantic search in seconds
  - **Lightning Network capability** (LND + LNbits): the AI assistant ("Clem") can create and pay invoices; sandboxed
- **Architecture pattern -- "Clem" coordinator on Signal 24/7:** routes to local models (Gemma4 26B, DeepSeek R1 32B) as appropriate, sandboxed research workspace with zero access to iCloud/email/contacts
- **Cost economics:** $20 in Claude+ChatGPT subs + ~$60 Anthropic API = ~$100/mo total; hardware was one-time
- **What's planned:** Bitcoin transaction tracing, address clustering, entity attribution, behavioral pattern matching (Chainalysis-style tooling self-hosted); macro/Fed data; eventually extending the same stack to ETH/SOL primarily for DeFi/stablecoin flows
- (see [autonomous-agents.md](autonomous-agents.md) for the personal-AI-coordinator pattern; see [memory-persistence.md > Karpathy Wiki Method](memory-persistence.md#karpathy-wiki-method-practical-setup-walkthrough) for the LLM-wiki pattern this builds on)

*Source: 2026-04-12-intangiblecoins-spent-the-last-month-building-a-personal-ai-research-infrast.md*
