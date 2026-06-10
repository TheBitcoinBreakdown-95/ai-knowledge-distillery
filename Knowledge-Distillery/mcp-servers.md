# MCP Servers & Plugins

MCP servers are external tools running locally or remotely that Claude calls to perform actions beyond its built-in tools -- browser control, API integrations, documentation lookup -- through a standardized protocol. This file covers MCP configuration, key servers, the plugin system, browser automation, design tool integrations, and Obsidian tooling.

### Configuration (`.mcp.json` at project root)

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-playwright"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "your-token-here" }
    }
  }
}
```

Install via CLI: `claude mcp add [name] [start-command]`. Debug with: `claude --mcp-debug`.

### Key MCPs Worth Knowing

| MCP Server | Capability |
|---|---|
| **Playwright** | Browser automation: navigate pages, take screenshots, test UIs |
| **Context7** | Real-time documentation lookup (avoids stale training data) |
| **Synta** | Deploy n8n workflows directly -- Claude builds, deploys, and debugs automation workflows from natural language descriptions |
| **GitHub** | Repository management, PR operations, issue tracking |
| **Sentry** | Error tracking integration |

### Permission Management

First use of any MCP tool requires manual approval. Auto-approve by adding tool patterns to `allowedTools` in settings: `"allowedTools": ["mcp__playwright__*", "mcp__github__*"]`.

### Tool Search: Defer-Loading for Cache Stability

- When dozens of MCP tools are loaded, including all full schemas in every request is expensive; removing them mid-conversation breaks the prompt cache
- Solution: `defer_loading` -- send lightweight stubs (tool name only, `defer_loading: true`) that the model can discover via a `ToolSearch` tool when needed
- Full tool schemas load only when the model selects them; the cached prefix stays stable because the same stubs are always present in the same order
- Available as an API feature: the tool search tool can be used through the Claude API directly (see [context-engineering.md#prompt-cache-architecture](context-engineering.md#prompt-cache-architecture))

*Source: Prompt Caching Is Everything (Claude Code team)*

### GrepRAG: Identifier-Focused Retrieval for Code

A 2026 research finding on repository-level code completion: coarse retrieval stages based on global lexical similarity (BM25/Jaccard) can fail for code completion because they miss precise identifier-related context. Grep-like retrieval targeting explicit identifiers recalls relevant definitions/usages more reliably in many cases.

- **Practical implication:** For code-heavy knowledge retrieval, prefer grep/ripgrep for identifier lookup over general-purpose BM25. Reserve semantic/vector search for natural-language queries that don't share vocabulary with the codebase.
- **Hybrid approach:** When a corpus contains both "exact code tokens" and "conceptual knowledge," hybrid retrieval (keyword + embeddings + simple fusion/reranking) outperforms either alone.
- **Aligns with Claude Code design:** The built-in Grep tool is the most efficient retrieval mechanism for code; the mgrep plugin adds semantic-aware token reduction but does not replace identifier-focused search.

(see [context-engineering.md](context-engineering.md#scaling-strategy-matrix-when-to-add-complexity) for when vector/hybrid becomes worth it)

*Source: deep-research-report-claudecodeknowledgelayer.md*

### X API Reference for Research Skills

- **Authentication:** Bearer token from `X_BEARER_TOKEN` env var
- **Search endpoints:** Recent search (last 7 days, `GET /2/tweets/search/recent`, max 100/request, 512-char query) and Full-archive search (all time, `GET /2/tweets/search/all`, max 500/request, 1024-char query, same pay-per-use tier)
- **Key search operators:** `from:`, `to:`, `is:retweet`, `is:reply`, `has:media`, `has:links`, `url:`, `conversation_id:`, `lang:` -- note `min_likes`/`min_retweets` are NOT available as search operators (filter post-hoc from `public_metrics`)
- **Pay-per-use pricing (Feb 2026+):** $0.005/post read, $0.010/user lookup, $0.010/post create. Prepaid credits at console.x.com. 24-hour deduplication (same post re-requested within UTC day = 1 charge). Typical research session: 5 queries x 100 tweets = ~$2.50
- **Response structure:** `data[]` (tweets with `public_metrics`, `entities.urls`, `conversation_id`), `includes.users[]` (author details), `meta.next_token` (pagination). Tweet URLs: `https://x.com/{username}/status/{tweet_id}`
- **Rate limiting:** Pay-per-use controls via spending limits in Developer Console, not fixed per-window caps. 350ms delay between requests as safety buffer

*Source: x-research-skill/references/x-api.md*

### Browser Automation MCP Comparison

Three browser automation options for Claude Code, each optimized for different use cases:

| | Chrome DevTools MCP | Claude in Chrome | Playwright MCP |
|---|---|---|---|
| **Source** | Google (official) | Anthropic (extension) | Microsoft |
| **Best for** | Performance debugging, network analysis | Quick manual verification while logged in | E2E testing, cross-browser, CI/CD |
| **Token cost** | ~19.0k (9.5%) | ~15.4k (7.7%) | ~13.7k (6.8%) |
| **Tools** | 26 (input, nav, emulation, perf, network, debug) | 16 (browser control, forms, media, tabs) | 21 (nav, interaction, assertions, page state) |
| **Cross-browser** | No (Chrome only) | No (Chrome only) | Yes (Chromium, Firefox, WebKit) |
| **CI/CD** | Excellent (headless) | Poor (requires login) | Excellent (headless) |
| **Element selection** | CSS/XPath selectors | Visual + DOM | Accessibility tree (semantic, less flaky) |

**Recommendation:** Playwright MCP as primary (lowest tokens, cross-browser, best CI/CD). Chrome DevTools MCP as secondary (unmatched performance traces, network inspection). Claude in Chrome only for quick logged-in-session visual checks.

**Security notes:**
- Claude in Chrome had 23.6% attack success rate without mitigations (11.2% with defenses); still beta with known vulnerabilities
- Playwright and Chrome DevTools both run isolated browser contexts with no cloud dependencies

**Install:**
```bash
npx playwright install
claude mcp add playwright -s user -- npx @playwright/mcp@latest
claude mcp add chrome-devtools -s user -- npx chrome-devtools-mcp@latest
```

### playwright-mcp: Accessibility Tree Beats Vision Models
- Microsoft built an MCP server for Playwright (github.com/microsoft/playwright-mcp) that fundamentally changes how AI agents browse the web
- **The architectural insight:** most browser agents rely on screenshots + vision models to "see" pages. playwright-mcp skips that entirely and reads the **accessibility tree** -- structured, clean, zero ambiguity
- Result: LLM knows exactly what's on the page and what to do with it; no hallucinated clicks, no broken selectors
- Works with Cursor, VS Code, Claude Desktop
- **Why this matters:** the accessibility tree is what screen readers consume -- it's the "semantic API" of the browser. Vision models guess at what a button is from pixels; the accessibility tree just tells you. This is structurally cheaper AND more reliable. Expect this pattern to spread to other "see + act" domains where a structured representation already exists.

*Source: 2026-04-28-_vmlops-microsoft-built-an-mcp-server-for-playwright-and-it-changes.md*

### agent-browser: Browser Automation CLI for AI Agents

- CLI tool purpose-built for AI agent browser automation -- distinct from Playwright MCP in that it provides a ref-based interaction model designed for LLM consumption
- **Core workflow:** Navigate (`open <url>`) -> Snapshot (`snapshot -i` returns `@e1`, `@e2` element refs) -> Interact (use refs to `click`, `fill`, `select`) -> Re-snapshot (refs invalidate after page changes)
- **Ref lifecycle:** Element references (`@e1`, `@e2`) are invalidated when the DOM changes (navigation, form submission, dynamic content) -- always re-snapshot after interactions that change the page
- **Semantic locators:** Alternative to refs when they're unreliable: `find text "Sign In" click`, `find label "Email" fill "user@test.com"`, `find role button click --name "Submit"`, `find testid "submit-btn" click`
- **Session management:** Parallel sessions via `--session <name>`, state persistence via `state save/load auth.json` for reusing authentication across runs
- **iOS Simulator support:** `-p ios --device "iPhone 16 Pro"` for mobile Safari automation via Appium xcuitest driver
- **Skill integration:** Packaged as a Claude Code skill with `allowed-tools: Bash(agent-browser:*)` -- restricts the agent to only run agent-browser commands

(see [Hooks: Pre/Post Tool Automation](tools-and-integrations.md#hooks-prepost-tool-automation) for complementary guardrail patterns)

*Source: claude-code-best-practice/.claude/skills/agent-browser/SKILL.md*

### Plugin System and Marketplaces

Plugins bundle skills, hooks, subagents, and MCP servers into a single installable unit, namespaced to avoid conflicts (e.g., `/my-plugin:review`):

- Official Anthropic marketplace auto-available; browse via `/plugin` > Discover tab; add third-party marketplaces from GitHub, Git URLs, local paths, or remote URLs
- Code intelligence plugins configure LSP connections for automatic diagnostics after edits (type errors, missing imports) and code navigation -- available for 11 languages
- External integration plugins bundle pre-configured MCP servers for GitHub, GitLab, Jira, Confluence, Linear, Notion, Figma, Slack, Vercel, Firebase, Supabase, Sentry
- Marketplace auto-updates enabled by default; configurable per marketplace; `DISABLE_AUTOUPDATER` env var disables all; `FORCE_AUTOUPDATE_PLUGINS=true` keeps plugin updates while disabling CLI updates
- Team config: `extraKnownMarketplaces` in `.claude/settings.json` for automatic marketplace installation

*Sources: Discover and install prebuilt plugins through marketplaces.md, Extend Claude Code.md*

### Plugin Development Toolkit: 8-Phase Create-Plugin Workflow

Anthropic's official plugin-dev toolkit provides 7 specialized skills and a guided 8-phase workflow for building Claude Code plugins from scratch.

- **8 phases:** Discovery -> Component Planning -> Detailed Design -> Structure Creation -> Component Implementation -> Validation -> Testing -> Documentation
- **7 skills:** hook-development, mcp-integration, plugin-structure, plugin-settings, command-development, agent-development, skill-development. Each ~1,500-2,000 words with progressive disclosure (metadata -> SKILL.md -> references/examples)
- **AI-assisted agent generation:** The agent-development skill includes Claude Code's own agent-creation system prompt as a reference, enabling agents to generate other agents
- **Validation utilities:** `validate-hook-schema.sh`, `test-hook.sh`, `hook-linter.sh`, `validate-agent.sh` -- production-ready scripts for plugin quality checks
- **Plugin settings pattern:** `.claude/plugin-name.local.md` files with YAML frontmatter for per-project configuration. Parsed via sed/awk/grep. Gitignored by convention
- **Content scale:** ~11,000 words across 7 SKILL.md files, ~10,000+ words references, 12+ working examples, 6 utility scripts

*Source: claude-plugins-official/plugins/plugin-dev/README.md*

### CLAUDE.md Management Plugin: Audit + Session Capture

An Anthropic-built plugin with two complementary tools for maintaining CLAUDE.md files.

- **claude-md-improver (skill):** Audits CLAUDE.md files against current codebase state. Triggered by "audit my CLAUDE.md" or "check if CLAUDE.md is up to date." For periodic maintenance when codebase evolves
- **/revise-claude-md (command):** Captures session learnings at end of session. Triggered manually. Adds context that was missing or incorrect based on what the session revealed
- **Dual-tool pattern:** Skill handles ongoing alignment (codebase -> CLAUDE.md); command handles learning capture (session -> CLAUDE.md). Different triggers, complementary purposes

(see [context-engineering.md](context-engineering.md) for CLAUDE.md authoring patterns)

*Source: claude-plugins-official/plugins/claude-md-management/README.md*

### Plugin MCP Integration: Naming Convention and Lifecycle

MCP server configuration specifics within the Claude Code plugin system:

- **Plugin MCP tool naming:** `mcp__plugin_<plugin-name>_<server-name>__<tool-name>` -- the `plugin_` prefix plus double-underscore delimiters prevent naming collisions between MCP tools from different plugins; use this full pattern in `allowed-tools` to pre-approve specific plugin MCP tools
- **Two configuration methods:** `.mcp.json` at project root (standard, shared with non-plugin setups) vs inline in `plugin.json` `mcpServers` field (plugin-specific, bundled and distributed with the plugin)
- **Four transport types:** stdio (local single-user), SSE (deprecated), streamable HTTP (remote/multi-client, recommended replacement for SSE), WebSocket (persistent bidirectional connections for real-time use cases)
- **Lazy-loading lifecycle:** MCP servers in plugins start only when their tools are first invoked, not at plugin installation or session start; auto-startup can be configured per server for latency-sensitive tools
- **Environment variable expansion:** `$ENV_VAR` syntax in MCP config files for credential injection without hardcoding; supports both `.mcp.json` and `plugin.json` formats

(see [Configuration](#configuration-mcpjson-at-project-root) for general MCP setup; see [MCP Server Development Standards](#mcp-server-development-standards) for naming and transport guidance)

*Source: claude-plugins-official/plugins/plugin-dev/skills/mcp-integration/SKILL.md*

### Plugin Settings Pattern: .local.md Convention Expanded

Expanded detail on the `.claude/plugin-name.local.md` per-project configuration pattern (see [Plugin Development Toolkit](#plugin-development-toolkit-8-phase-create-plugin-workflow) for the brief overview):

- **Format:** YAML frontmatter for structured settings + markdown body for free-form instructions; parsed in bash hooks via `sed -n '/^---$/,/^---$/p'` piped to `grep`
- **Gitignored by convention:** `.local.md` suffix signals local-only configuration that should not be committed
- **Real-world examples:** `multi-agent-swarm` plugin stores `coordinator_session` ID and tmux integration config; `ralph-loop` plugin tracks iteration count and test status across sessions
- **Security requirements:** validate all settings paths to prevent path traversal; sanitize values before use in shell commands; never execute settings values as code
- **Restart required:** settings changes take effect only after session restart -- same limitation as hooks (no hot-reload mechanism)
- **Reading from different contexts:** hooks parse settings via shell commands (`sed`/`grep`); commands access via file read; agents reference via instructions in their system prompt

*Source: claude-plugins-official/plugins/plugin-dev/skills/plugin-settings/SKILL.md*

### LSP Integration: Reality Check and Actual Benefits

- LSP (Language Server Protocol) integration exists in Claude Code and provides semantic code navigation (go-to-definition, find-references, workspace-symbol)
- **Enabled by default** since v2.0.74 -- not a hidden setting. Requires a language server installed for your language
- **Debunked claims:** "600x faster" is fabricated; there is no `ENABLE_LSP_TOOL` flag; "50ms definition lookup" is not a real feature; "auto-catches type errors after every edit" is not how it works
- **Actual benefits:** precision over grep for large codebases; token savings by avoiding grepping through hundreds of irrelevant files; semantic navigation (findReferences on structs/types, documentSymbol)
- **Rust-specific findings:** findReferences and documentSymbol are killer features; workspaceSymbol is a fast alternative to glob+grep; call hierarchy is unreliable for free functions (grep is safer)
- **The real bottleneck** is usually the model deciding to read 30 files it doesn't need, not grep being slow
- Tip: add "use LSP-first for [language] navigation" to CLAUDE.md for codebases where LSP is well-supported (see [context-engineering.md](context-engineering.md#claudemd-your-always-loaded-memory))

*Source: Twitter-Bookmarks/2026-03-08-om_patel5-LSP-tool-claude-code.md*

### Plugin Auto-Discovery Mechanism and Portable Paths

Detailed internals of how Claude Code discovers and loads plugin components:

- **Discovery order:** Plugin manifest (`.claude-plugin/plugin.json`) -> `commands/` (all `.md` files) -> `agents/` (all `.md` files) -> `skills/` (subdirs containing `SKILL.md`) -> `hooks/hooks.json` -> `.mcp.json`
- **Override behavior:** Custom paths in `plugin.json` **supplement** default directories, never replace them -- components in both locations load
- **Path rules:** Must be relative, must start with `./`, support arrays for multiple locations, no absolute paths
- **`${CLAUDE_PLUGIN_ROOT}` environment variable:** Use for all intra-plugin path references in hooks, MCP configs, and scripts. Available in hook commands, MCP server args, and executed scripts. Never hardcode absolute paths, relative paths from working directory, or `~/` shortcuts
- **Timing:** Components register at install, activate at enable, no restart required for changes (next session picks them up)
- **Manifest fields:** Only `name` (kebab-case) is required; `version`, `description`, `author`, `keywords` are recommended; `commands`, `agents`, `hooks`, `mcpServers` fields for custom paths
- **Troubleshooting patterns:** Component not loading (check frontmatter syntax, ensure SKILL.md not README.md); path errors (replace hardcoded with `${CLAUDE_PLUGIN_ROOT}`); auto-discovery failures (directories must be at plugin root, not in `.claude-plugin/`); conflicts (namespace commands with plugin name)

(see [Plugin Development Toolkit](#plugin-development-toolkit-8-phase-create-plugin-workflow) for the 8-phase workflow)

*Source: claude-plugins-official/plugins/plugin-dev/skills/plugin-structure/SKILL.md*

### Cowork Plugin Tier List: 21 Plugins Ranked S/A/B/C

@heynavtoor tested all 21 Claude Cowork plugins with real paid deliverables over 4 weeks:

- **Plugin Architecture:** A plugin folder contains skills (domain expertise), slash commands (structured workflows), connectors (MCP integrations), and sub-agents (parallel workers). "Plugins are just markdown files" -- zero barrier to creation
- **S-Tier:** Data Analysis (`/data:explore` auto-summarizes, flags anomalies), Productivity (compounds over time as chief of staff), Sales (CRM-connected call prep, battlecard generation)
- **A-Tier:** Legal (triggered SaaSpocalypse -- Thomson Reuters -18%, LegalZoom -20%), Product Management (spec writing with AskUserQuestion), Marketing (brand-voice-aware), Finance (cross-app Excel-to-PowerPoint)
- **B-Tier (needs customization):** Customer Support, HR, Engineering, Operations, Design, Financial Analysis, Investment Banking, Equity Research, Private Equity, Brand Voice
- **C-Tier (narrow/incomplete):** Enterprise Search, Bio Research, Wealth Management, Plugin Management
- **Platform Strategy:** Jan 30 horizontal wave (every company needs), Feb 24 vertical wave (industry-specific) -- "plugins are just markdown files" with 2,000 GitHub stars and growing
- **Market Impact:** "$20/month subscription doing 40% of what $150/month enterprise seats do" -- SaaSpocalypse was "price discovery, not panic"

(see [skills.md](skills.md) for skill design patterns applicable to custom plugin creation)

*Source: Twitter-Bookmarks/2026-02-26-heynavtoor-i-tested-all-21-claude-cowork-plugins-heres.md*

### Synta MCP: Workflow Deployment to n8n

- MCP server enables Claude/Cursor to deploy complete n8n workflows directly into a running instance
- Workflow: MCP interviews user, scrapes real-time n8n docs, deploys to instance, auto-debugs before delivery
- "MCP as deployment bridge" pattern: AI generates and validates automation workflows end-to-end

*Source: Synta's MCP 1.md*

### fli: Google Flights MCP Server
- MCP server and Python library that enables LLM agents to search flights, compare prices, and access travel data programmatically via the MCP protocol
- Example of a domain-specific MCP server that gives agents access to real-world transactional data -- flight search, price comparison, itinerary planning
- GitHub: punitarani/fli

*Source: GitHub Stars*

### Financial Datasets MCP for Claude Code -- 17K+ Stocks Live
@cyrilXBT documented setup for plugging Claude Code into financialdatasets.ai (live financial data: 17,000+ stocks, crypto prices, earnings, balance sheets, income statements, cash flow).

- **Setup (60 seconds):**
  ```
  claude mcp add --transport http financial-datasets https://mcp.financialdatasets.ai/
  ```
  Then `/mcp` in Claude Code → complete OAuth in browser → verify with `claude mcp list`
- **Sample queries that work:** "What is Apple's current P/E ratio and market cap?" / "Show me Tesla's income statement for the last 4 quarters." / "How has Bitcoin's price changed over the past year?"
- **Implication:** $24K/year Bloomberg Terminal capability now accessible via OAuth + 60s setup
- **Strategic note:** quants/analysts/PMs combining Claude reasoning with live financial data have a research edge that compounds daily. Relevant for the user's WSJ/financial services adjacency and the financial-services sales pivot
- Docs (for errors): docs.financialdatasets.ai/mcp-server#claude-code

*Source: 2026-05-09-cyrilXBT-claude-code-can-now-pull-live-data-from-17000-stocks-crypto.md*

### Meta Ads MCP + CLI -- Agentic Media Buying
@BryanECano flagged Meta's release of an Ads MCP and CLI giving Claude/ChatGPT direct authorized access to manage Meta Ads accounts via natural language.

- **Comprehensive reporting:** pull detailed reports, surface performance trends, understand campaign state without clicking through Ads Manager
- **Campaign management:** create + edit campaigns, ad sets, ads from the agent
- **Catalog management:** create product catalogs, add product data, troubleshoot feed issues
- **Signal diagnostics:** signal health and quality insights to prioritize setup parts that need attention
- **Significance:** "agentic media buying" as a productized pattern -- Meta has explicitly opened the door to AI-driven ad ops. For agency builders, this is the wedge to sell "AI media buyer" services. For the user's career-pivot path: relevant evidence that ad ops/media buying is automating fast, validating the ad-sales-is-automation-exposed thesis.

*Source: 2026-04-30-BryanECano-meta-released-their-ads-mcp-and-cli-today-if-you-use-claude.md*

### n8n + Synta MCP: Describe Once, Deploy Everywhere

The three-tool stack that replaces manual workflow building:

- **Claude** (brain): strategic thinking, architecture, complex reasoning
- **Cursor** (hands): code execution, custom scripts, direct deployment
- **Synta MCP** (bridge): connects Claude/Cursor directly to your n8n instance with real-time docs
- Workflow: describe what you want in one paragraph; Claude builds, deploys, auto-debugs in your n8n instance
- Before Synta: describe to Claude, copy JSON, paste in n8n, debug for hours. After: 6 workflows in 4 minutes, zero manual nodes
- Key tips: one conversation per workflow; tell Claude what NOT to do; give context about why ("runs every 5 minutes so it needs to be fast")

(see [Synta MCP: Workflow Deployment to n8n](#synta-mcp-workflow-deployment-to-n8n) for MCP configuration details; [Credential Isolation Architecture via n8n Proxy](#credential-isolation-architecture-via-n8n-proxy) for security patterns)

*Source: Old-Notes/N8N.md, Old-Notes/Synta's MCP.md*

### Credential Isolation Architecture via n8n Proxy

Using n8n as a credential proxy layer between OpenClaw and external APIs:

- **Pattern:** OpenClaw designs n8n workflows with webhooks, then calls those webhooks -- API keys never reach the agent
- **Three benefits:** Observability (visual UI inspection of workflow logic), security (API keys stay in n8n, never in agent code), performance (deterministic workflows don't burn LLM tokens)
- **Implementation:** Docker Compose stack (`openclaw-n8n-stack`) on shared network for seamless webhook calls
- **"Lock after testing" rule:** After validating workflows, lock them to prevent silent modification by the agent
- Prevents the most common agent security failure: hardcoded API keys in code (see [failure-patterns.md](failure-patterns.md#agent-security-threat-model-6-attack-classes))

*Source: awesome-openclaw-usecases/usecases/n8n-workflow-orchestration.md*

### Curated Daily-Use MCP Recommendations

Community consensus on the MCP servers that actually get used daily (vs the 15 installed but 4 used pattern):

| MCP Server | What It Does | Why It Matters |
|------------|-------------|----------------|
| **Context7** | Fetches up-to-date library docs into context | Prevents hallucinated APIs from stale training data |
| **Playwright** | Browser automation: screenshots, navigation, form testing | E2E testing, cross-browser, CI/CD-ready |
| **Claude in Chrome** | Connects to your real Chrome: console, network, DOM | Debug what users actually see (beta, known vulnerabilities) |
| **DeepWiki** | Wiki-style documentation for any GitHub repo | Architecture, API surface, relationships -- structured |
| **Excalidraw** | Generate architecture diagrams and flowcharts from prompts | Hand-drawn Excalidraw sketches, useful for documentation |

**Recommended pipeline:** Research (Context7/DeepWiki) -> Debug (Playwright/Chrome) -> Document (Excalidraw)

**The "went overboard" warning:** "Went overboard with 15 MCP servers thinking more = better. Ended up using only 4 daily." Start with Context7 + Playwright, add others as specific needs arise.

(see [Browser Automation MCP Comparison](#browser-automation-mcp-comparison) for detailed Playwright vs Chrome DevTools vs Claude in Chrome analysis)

### Five Must-Have MCPs for Claude Code (Axel Bitblaze)
- **Curated stack** that turns Claude into a full automation surface (search, scraping, browser control, page inspection, media generation), all native, no glue code:
  1. **Perplexity MCP** — real-time web search inside Claude. Four tools: search, ask, deep research, reasoning. Pulls live news, latest docs, market data into context. Repo: `github.com/perplexityai/modelcontextprotocol`.
  2. **Playwright MCP** — cleanest browser automation for Claude. Uses the accessibility tree (not screenshots) and is token-cheap. Repo: `github.com/microsoft/playwright-mcp`.
  3. **Firecrawl MCP** — search, scrape, deep-research any website. Handles bot detection, returns clean structured data. Repo: `github.com/firecrawl/firecrawl-mcp-server`.
  4. **Glif MCP** — runs AI media workflows from `glif.app` (image, video, audio, voice cloning) all hosted (no local GPU). Repo: `github.com/glifxyz/glif-mcp-server`.
  5. **Chrome MCP** — built into Claude Code. Claude inspects any page (DOM, network requests, console errors, performance metrics) live, in chat. Zero install.
- **Curation thesis:** before these five, Claude was stuck on reasoning + code edits + reading local files. Now: live web search, full browser automation, structured scraping, page debugging, media generation — without opening a single SaaS app. Zero subscriptions outside API keys.

*Source: 2026-05-10-Axel_bitblaze69-5-must-have-mcps-these-are-the-ones-id-recommend-every-claud.md*

### Tested MCP Server Catalog: 35 Servers by Category
- Curated from 10,000+ listed MCP servers -- tested for reliability, active maintenance, and solving real problems
- **Search and Research:** Tavily (AI-optimized web search, 1K free/mo), Exa (semantic search by meaning), Brave Search (independent index, no Google), Perplexity (answer engine with deep research), Context7 (live framework docs, prevents hallucinated APIs)
- **Web Scraping:** Firecrawl (URL to markdown, RAG pipelines), Apify (3,000+ scrapers), Bright Data (anti-bot bypass), Crawl4AI (open-source, 61K stars, no API key)
- **Browser Automation:** Playwright (Claude controls Chrome), Browserbase (cloud-hosted browser sessions)
- **Dev Tools:** GitHub (PRs, issues, CI/CD), Linear (issue tracking), Sentry (production errors), Vercel (deploy/debug), Jira/Atlassian (sprint management)
- **Databases:** Supabase (Postgres + auth), PostgreSQL (natural language queries), MongoDB (40+ tools), Neo4j (graph queries)
- **Vector/AI Memory:** Pinecone (cloud vector + reranking), Qdrant (open-source, self-hostable), Chroma (lightweight local), Memory MCP (knowledge graph persistence)
- **Productivity:** Notion, Slack, Todoist, Zapier (6,000+ app automations)
- **Business:** Stripe (payments), HubSpot (CRM)
- **Design:** Figma (design-to-code), Bannerbear (automated image generation)
- **Infrastructure:** Cloudflare (Workers, KV, D1), Docker (container management), Grafana (monitoring)
- **Sweet spot: 3-5 servers.** Each MCP server consumes token context for tool descriptions. More than 5 = burning tokens before you ask a question. Claude Code's Tool Search lazy-loads to mitigate this

(see [context-engineering.md](context-engineering.md#mcp-context-budget-rule-of-thumb) for the token budget rule)

*Source: 2026-04-08-zodchiii-httpstcouax5di3nmq.md*

### Top 30 MCP Servers Catalog
@the_smart_ape's curated list of 30 MCP servers worth installing, with installation order. Ecosystem state: 10,000+ public servers, 97M monthly SDK downloads.

- **Discovery layers (search before building):**
  - Official MCP servers repo: github.com/modelcontextprotocol/servers (reference implementations from MCP steering group)
  - Official registry: registry.modelcontextprotocol.io (500+ indexed, searchable API; backed by Anthropic, GitHub, Microsoft, PulseMCP)
  - Awesome list: github.com/wong2/awesome-mcp-servers (most comprehensive community list, organized by category)
  - mcp.run -- run MCP servers without local install, sandboxed execution, good for testing
- **MCP vs Skills (the distinction matters):**
  - Skills tell Claude HOW to think (instruction sets, SKILL.md files: TDD methodology, PRD writing, code review process)
  - MCP servers give Claude access to WHERE things live (databases, GitHub, Slack, real systems with real data)
  - Skills without MCP = brilliant employee with no tool access. MCP without skills = employee with tools but no playbook. Need both.
- **The 30 servers, by category:**
  - **Dev & Code:** github.com/github/github-mcp-server (28K+ stars, 51 tools, the most popular), github.com/microsoft/playwright-mcp (full browser automation), github.com/getsentry/sentry-mcp (error tracking + stack trace analysis), github.com/semgrep/mcp (static analysis + security scanning), github.com/circleci/mcp-server-circleci (CI/CD pipeline access)
  - **Databases & Data:** github.com/neondatabase/mcp-server-neon (Postgres direct), github.com/supabase-community/supabase-mcp (full Supabase: DB+auth+storage+edge functions), github.com/neo4j/neo4j-mcp (graph DB), github.com/qdrant/mcp-server-qdrant (vector search + semantic memory), github.com/tinybirdco/mcp-tinybird (real-time analytics at billion-row scale)
  - **Cloud & Infra:** github.com/awslabs/mcp (full AWS suite: CDK advice, cost analysis, Bedrock, Nova), github.com/cloudflare/mcp-server-cloudflare (16 specialized servers: Workers, R2, D1, Browser Rendering, DNS, KV), github.com/grafana/mcp-grafana (dashboards + datasources + incident investigation), github.com/nichochar/railway-mcp (Railway deploy/manage), github.com/render-oss/render-mcp-server (Render stack)
  - **Productivity & Business:** github.com/makenotion/notion-mcp-server (official Notion), github.com/anthropics/slack-mcp (Slack reads/posts/threads), Gmail MCP (community), Jira/Asana via registry, github.com/stripe/agent-toolkit (official Stripe), HubSpot MCP via registry
  - **Web Scraping:** github.com/mendableai/firecrawl (JS rendering, anti-bot, clean markdown), github.com/browserbase/mcp-server-browserbase (cloud-hosted browser automation), Bright Data MCP (proxy + SERP + e-commerce scraping), github.com/apify/actors-mcp-server (3,000+ pre-built scrapers)
  - **AI/Knowledge/Memory:** github.com/modelcontextprotocol/servers/tree/main/src/memory (knowledge-graph persistent memory), github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking (forces structured step-by-step reasoning, dynamic thought revision), github.com/upstash/context7 (up-to-date docs for any library; should be installed by default to stop hallucinated outdated APIs)
  - **Media & Design:** github.com/nichochar/figma-mcp (design-to-code bridge), github.com/elevenlabs/elevenlabs-mcp (TTS + voice generation)
- **Install order (foundation → stack → productivity → data):**
  1. Foundation: filesystem, git, memory, sequential thinking (free, official, make everything else better)
  2. Stack-specific: Postgres + GitHub + AWS suite, etc. -- match your tools
  3. Productivity: Notion + Slack + Gmail (turns Claude into communication hub)
  4. Data access last: firecrawl + browserbase + apify (powerful but situational)

*Source: 2026-04-16-the_smart_ape-httpstcofajylzzfti.md*

### MCP Server Design Patterns: Building Production-Quality Tool Servers

- Four-phase creation: deep research/planning -> implementation -> review/test -> create evaluations
- Tool design tradeoff: comprehensive API coverage vs specialized workflow tools; when uncertain, prioritize comprehensive coverage
- Tool naming: consistent prefixes + action-oriented names (e.g., `github_create_issue`)
- Context management: design tools to return focused, concise data; support filtering/pagination to avoid flooding agent context
- Actionable error messages: errors should guide agents toward solutions with specific next steps
- Recommended stack: TypeScript (best SDK support) with streamable HTTP for remote, stdio for local
- Tool annotations: `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint` for safety metadata
- Output schemas: define `outputSchema` for structured data; use `structuredContent` in responses
- Evaluation: 10 complex, realistic, read-only, independent, verifiable, stable questions in XML format

*Source: skills/skills/mcp-builder/SKILL.md*

### MCP Server Development Standards

- **Server naming convention:** Python: `{service}_mcp` (e.g., `slack_mcp`). Node/TypeScript: `{service}-mcp-server` (e.g., `slack-mcp-server`). No version numbers in names.
- **Response format dual-output:** All data-returning tools should support both JSON (machine-readable, all fields) and Markdown (human-readable, display names, formatted timestamps). Default to Markdown.
- **Pagination standard:** Always respect `limit` parameter. Return `has_more`, `next_offset`/`next_cursor`, `total_count`. Default to 20-50 items. Never load all results into memory.
- **DNS rebinding protection:** For streamable HTTP servers running locally -- enable DNS rebinding protection, validate `Origin` header on all incoming connections, bind to `127.0.0.1` not `0.0.0.0`.
- **Transport deprecation:** Avoid SSE (deprecated in favor of streamable HTTP). Use stdio for local single-user tools, streamable HTTP for remote/multi-client.
- **stdio logging:** stdio servers must NOT log to stdout -- use stderr for all logging output.

*Source: skills/skills/mcp-builder/reference/mcp_best_practices.md*

### Graph RAG Integrations for Claude

Structured retrieval via graph databases, accessible through MCP and Claude Code.

**Microsoft GraphRAG** (arxiv.org/abs/2404.16130, open-source at github.com/microsoft/graphrag):
1. Slice corpus into TextUnits
2. LLM extracts entities, relationships, and claims
3. Hierarchical clustering (Leiden algorithm) groups entities into communities
4. LLM generates community summaries
5. Query time: Local (entity-specific), Global (dataset-wide synthesis), DRIFT (hybrid)

Cost: entity extraction = ~75% of total indexing cost. 45,000 words with GPT-4o ≈ $30, 35 minutes. FastGraphRAG uses NLP-based extraction (spaCy/NLTK) as cheaper alternative.

**Graph database options ranked by Claude integration ease:**
- **Cognee** (github.com/topoteretes/cognee) -- ECL pipeline, MCP integration for Claude (December 2025), 70+ companies, raised $7.5M. Lowest friction option. (see [memory-persistence.md](memory-persistence.md#graph-databases-vs-vector-for-agent-memory))
- **Neo4j MCP** -- connect Claude directly to Neo4j via natural language → Cypher queries
- **mcp-knowledge-graph** (github.com/shaneholloman/mcp-knowledge-graph) -- persistent memory through local knowledge graph
- **FalkorDB** (github.com/FalkorDB/FalkorDB) -- Redis-based, sub-10ms query latency, integrated with Zep/Graphiti

**Claude Code: code-review-graph** (github.com/tirth8205/code-review-graph): parses codebase with Tree-sitter into structural graphs (SQLite). Achieved 49x token reduction on a Next.js monorepo by serving structural graph instead of raw files.

**Benchmark context:** GraphRAG 81.67% vs VectorRAG 57.50% on relational queries (Lettria 2025). But GraphRAG 13.4% LOWER on Natural Questions (ICLR 2026). Use graph for multi-entity relational queries; vector for simple lookups.

*Source: Deep-Research/graph-databases-for-ai-agents.md*

### L402 Protocol and Machine-Payable APIs

L402 activates HTTP 402 "Payment Required" by combining Lightning Network micropayments with macaroon-based cryptographic credentials. Developed by Lightning Labs. Enables machine-native pay-per-request APIs with no accounts, passwords, or API keys.

**L402 flow:**
1. Client requests protected resource
2. Server responds 402 with `WWW-Authenticate: L402 macaroon="<base64>", invoice="<bolt11>"`
3. Client pays Lightning invoice, receives preimage as proof-of-payment
4. Client retries with `Authorization: L402 <base64(macaroon)>:<hex(preimage)>`
5. Server verifies cryptographically (stateless) and returns resource

Macaroons support attenuation -- restrict permissions before delegating (e.g., spending caps). Sub-cent granularity. Entire flow automatable by agents.

**Three competing protocols (as of March 2026):**
| Protocol | Payment | Endpoints | Key backers |
|----------|---------|-----------|-------------|
| L402 | Bitcoin Lightning | 517 | Lightning Labs |
| x402 | USDC (Base/Solana/Polygon) | 14,554 | Coinbase, Cloudflare, Google, Visa |
| MPP | Fiat via Stripe/Tempo | 490 | Anthropic, OpenAI, Visa, Shopify |

**402 Index MCP Server** (github.com/ryanthegentry/402index-mcp-server): discovery layer -- 15,500+ paid API endpoints across all three protocols. Four tools: `search_services`, `get_service_detail`, `list_categories`, `get_directory_stats`. Agents use it to find where to spend money.

**Key tools for building paid APIs:**
- **Aperture** (Lightning Labs) -- L402 reverse proxy; sits in front of any HTTP endpoint, adds payment gating. You set price/request; Aperture handles invoice generation and verification.
- **Alby PaidMCP** (github.com/getAlby/paidmcp) -- SDK for creating paid MCP servers with Lightning
- **lightning-agent-tools** (github.com/lightninglabs/lightning-agent-tools) -- 7-skill MCP toolkit including node management, macaroon bakery, lnget

**Practical implementations:** Agent Commerce Store wraps 21 free public APIs behind L402 (2-10 sats each: Weather, Wikipedia, arXiv). Sats4AI: 25+ AI tools. SatsAPI: Bitcoin market intelligence at 2 sats/request.

(see [bitcoin-ai.md](bitcoin-ai.md#machine-payable-web-monetized-knowledge-graphs) for the monetized knowledge graph paradigm)

*Source: Deep-Research/l402-monetized-knowledge-graphs-bitcoin.md*

### 402 Index: 15,000+ Paid API Endpoint Directory for AI Agents

- The 402 Index aggregates 15,000+ paid API endpoints (L402, x402, MPP protocols) with hourly health checks -- agents can auto-discover reliable monetized services
- Includes live health checker, full API docs, an MCP server (on mcp.so), and provider self-registration
- Enables the agent-payments pattern: agents autonomously discover, evaluate, and pay for API services using micropayment protocols

*Source: Twitter-Bookmarks/2026-03-19-RyanTheGentry-announcing-the-worlds-largest-paid-endpoint-directory-for-ai.md*

### 402 Index MCP Server: Agent-Discoverable Paid API Directory
- MCP server approved on the official MCP registry that lets AI agents auto-discover 15,000+ paid API endpoints across L402, x402, and MPP payment protocols
- Includes a live health checker with hourly checks, comprehensive endpoint database, full API docs, self-registration for providers, and usage stats
- Enables agents to find and pay for services programmatically over Bitcoin Lightning Network without pre-configured API keys or accounts
- lnget v1.1.0 (Lightning Labs) added MCP server mode via `lnget mcp serve` -- supports both MPP and L402 protocols with auto-detection, JSON input/output, and context management for agent-friendly usage
- Pattern: payment protocol discovery as an MCP tool -- agents query for available paid services, negotiate payment, and consume the API in a single workflow
- (see [bitcoin-ai.md](bitcoin-ai.md) for broader Bitcoin + AI integration patterns)

*Sources: 2026-03-20-RyanTheGentry-the-402-index-mcp-server-has-officially-been-approved-on-htt.md, 2026-03-20-roasbeef-lnget-v110-has-just-been-released-it-now-supports-both-mppl4.md*

### Ollama Now an Official OpenClaw Provider

- Ollama is now an official provider for OpenClaw: `openclaw onboard --auth-choice ollama` enables all local Ollama models to work with OpenClaw seamlessly
- Enables fully local, private agentic workflows using any Ollama-supported model

*Source: Twitter-Bookmarks/2026-03-16-ollama-ollama-is-now-an-official-provider-for-openclaw-openclaw-onb.md*

### AI-Native Design with Paper MCP: Design-to-Code Roundtrip

- Paper (design tool) + Claude Code via MCP creates a design-to-code roundtrip: Claude generates HTML/CSS directly into Paper canvas as editable frames, you refine, then push designs back to Claude to write production code
- Setup: `npx skills add paper-mcp` + restart + /mcp to verify
- Paper Snapshot Chrome plugin copies live websites as editable layers into Paper; then prompt Claude to remix those references with your spec
- Break designs into specific pages/components rather than entire user journeys; iterative collaboration model: Claude designs, human refines, Claude explores more variants

*Source: Twitter-Bookmarks/2026-03-18-tkkong-httpstcod9wdpmh7tr.md*

### Chrome Browser Agent Optimization: Enable JavaScript from Apple Events

- On macOS, enable "Allow JavaScript from Apple Events" (View → Developer → Allow JavaScript from Apple Events in Chrome) before running browser agents
- Telling your agent this setting is enabled saves a large number of tokens for any browser-based work by allowing direct JS execution

*Source: Twitter-Bookmarks/2026-03-19-Austen-pro-tip-to-make-agents-not-suck-at-doing-everything-in-chrom.md*

### Google Stitch DESIGN.md: Portable Agent-Readable Design System

- Google Stitch introduces DESIGN.md: a portable, agent-readable design system file analogous to CLAUDE.md but for UI/design systems
- Has an MCP server that connects directly to Claude Code, Cursor, and Gemini CLI -- the agent reads your design system and builds against it
- PRD → design → code used to be three teams and three handoffs; DESIGN.md collapses it to one loop with one context file

*Source: Twitter-Bookmarks/2026-03-19-PawelHuryn-google-just-shipped-designmd-a-portable-agent-readable-desig.md*

### Google Stitch Masterclass: AI-Native Design with MCP Integration

- Google Stitch is an AI-native infinite canvas design tool with full MCP server integration connecting to Cursor, Gemini CLI, and AI Studio
- Brand kit import: provide a URL and Stitch scrapes the site to extract colors, fonts, and component styles -- auto-populating a design system from an existing website
- Variations feature: generate 5 design directions from one broad prompt, pick the closest, iterate with Creative Range slider; 6-8 hours of design iteration compressed to 5 minutes
- Instant Prototype: Stitch auto-generates the next logical screen based on expected user flow
- Export to Figma with editable layers and Auto Layout intact; use Stitch for starting, Figma for finishing

*Source: Twitter-Bookmarks/2026-03-20-jspujji-httpstcomyw8k0rjzd.md*

### Figma use_figma MCP: AI Agents on the Canvas

- Figma released `use_figma` MCP tool enabling AI agents to design directly on the Figma canvas; open beta as of March 2026
- Comes with skills to teach agents design workflows; enables AI-assisted design that stays inside the existing Figma context rather than jumping between tools

*Source: Twitter-Bookmarks/2026-03-24-figma-now-you-can-use-ai-agents-to-design-directly-on-the-figma-ca.md*

### Claude + Filesystem MCP for Large Vault Maintenance

- Claude with filesystem MCP server can systematically fix a 12M-word Obsidian vault -- broken links, formatting inconsistencies, orphaned notes -- at scale
- Pattern: give Claude filesystem access + a specific audit task + a verification criteria; let it work through the vault in batches; review diffs before accepting
- Practical ceiling: very large vaults require batching by directory; single-shot processing of 12M words exceeds context; the win is systematic coverage, not single-prompt magic

*Source: Twitter-Bookmarks/2026-03-25-EleanorKonik-eight-months-ago-i-wrote-about-using-claude-with-mcp-servers.md*

### dev-browser CLI: Let Agents Control Browsers via Code

- `npm i -g dev-browser` then instruct the agent to "use dev-browser" -- no complex integration required
- Code-driven browser control is significantly faster than vision-based approaches; the agent writes JavaScript/DOM manipulation rather than interpreting screenshots
- Lightweight alternative to MCP browser tools for agents that already have code execution capabilities

*Source: Twitter-Bookmarks/2026-03-25-sawyerhood-introducing-the-new-dev-browser-cli-the-fastest-way-for-an-a.md*

### On-Demand Domain Guidance via MCP Tool

- Problem: domain expertise loaded by the outer coding agent is consumed by the wrong agent -- the inner test executor is the one that needs it
- Solution: MCP `load_guidance` tool; inner agent calls it on demand when it encounters a domain-specific failure
- Build-time codegen (markdown → TypeScript module) over runtime file reads: deterministic across installs and CI
- `readOnlyHint: true` annotation enables parallel execution alongside other read-only tools
- Compact TOC (~10 lines) in the system prompt is the routing table -- tells the agent what domains are available without loading all guidance upfront
- Cost reduction: loads 0-3 domains per run vs all statically -- ~2000 tokens saved per run on average
*Source: expect/.specs/agent-domain-guidance.md*

### Smart Explore: AST-Based Code Navigation

- `smart_search` → `smart_outline` → `smart_unfold` replaces Glob → Grep → Read for code exploration; 4-8x token savings on file understanding
- `smart_search(query, path)`: discovers files and symbols across a directory in one call; returns ranked symbols with signatures and folded file views
- `smart_outline(file_path)`: structural skeleton (all functions, classes, methods, ~1-2k tokens) without loading implementation
- `smart_unfold(file_path, symbol_name)`: full source of one symbol only; AST boundaries guarantee completeness regardless of size
- Fall back to standard tools: Grep for exact string search, Read for files under ~100 lines or non-code files, Glob for file path patterns
*Source: claude-mem/plugin/skills/smart-explore/SKILL.md*

### OpenClaw Plugin: Memory for Gateway Agents

- claude-mem integrates into OpenClaw gateway via 4 hooks: `before_agent_start` (init session), `before_prompt_build` (inject timeline into system prompt, cached 60s per project), `tool_result_persist` (fire-and-forget observation), `agent_end` (summarize + complete)
- Config: `project` scopes all observations; `syncMemoryFileExclude` lists agent IDs that manage their own memory (still observed, not injected)
- Observation feed: SSE stream from worker to messaging channels (Telegram, Discord, Slack, Signal, WhatsApp, LINE) -- agents learn things and you watch in real time
- Tools prefixed with `memory_` are skipped to prevent recursive observation recording
*Source: claude-mem/openclaw/SKILL.md*

### Defuddle: Token-Efficient Web Fetching

- `defuddle parse <url> --md` extracts clean markdown from web pages, removing navigation, ads, and clutter before passing to the model
- Prefer over WebFetch for standard web pages (articles, docs, blog posts); use WebFetch directly for `.md` URLs (already clean)
- Save to file: `defuddle parse <url> --md -o content.md`; extract metadata only: `defuddle parse <url> -p title`
*Source: obsidian-skills/skills/defuddle/SKILL.md*

### Obsidian CLI: Programmatic Vault Operations

- `obsidian` CLI talks to a running Obsidian instance; requires Obsidian to be open
- File targeting: `file=<name>` resolves like a wikilink (name only); `path=<path>` for exact vault-root-relative path
- Plugin dev/test cycle: `plugin:reload` → `dev:errors` → `dev:screenshot` → `dev:console` -- four-step loop identical to TDD cycle
- `eval code="..."` runs JavaScript in the Obsidian app context -- programmatic vault introspection
- `--copy` copies output to clipboard; `silent` prevents files from opening during automation
*Source: obsidian-skills/skills/obsidian-cli/SKILL.md*

### Obsidian Bases: Database Views for Note Vaults

- `.base` files are YAML with `filters` (scope), `formulas` (computed properties), `properties` (display names), `summaries` (aggregations), and `views` (table/cards/list/map)
- Date subtraction returns a `Duration` type -- always access `.days`, `.hours`, etc. before applying numeric functions
- Guard all formula property accesses with `if()` -- properties may not exist on all notes
- Embed in a note: `![[MyBase.base]]` or `![[MyBase.base#View Name]]` for a specific view
*Source: obsidian-skills/skills/obsidian-bases/SKILL.md*

### JSON Canvas: Visual Node Graph File Format

- `.canvas` files: `{"nodes": [], "edges": []}` with two top-level arrays; nodes have `id` (16-char lowercase hex), `type` (text/file/link/group), `x`, `y`, `width`, `height`
- Edges reference `fromNode`/`toNode` by ID; optional `fromSide`/`toSide` (`top/right/bottom/left`) and `fromEnd`/`toEnd` (`none/arrow`)
- `group` nodes are visual containers; position child nodes within the group's bounds manually
- Newline pitfall: use `\n` in JSON strings, not `\\n`
- Validation: unique IDs across nodes and edges, all edge references resolve, required fields present per type
*Source: obsidian-skills/skills/json-canvas/SKILL.md*

### Obsidian Markdown Extensions

- Wikilinks (`[[Note]]`) for internal vault links -- prefer over Markdown links because Obsidian tracks renames automatically
- Embeds: prefix any wikilink with `!` to embed inline (`![[Note]]`, `![[image.png|300]]`, `![[doc.pdf#page=3]]`)
- Callouts: `> [!type]` with `+` for expanded-foldable and `-` for collapsed-foldable
- Block IDs (`^block-id`) placed inline on paragraphs or on a separate line after lists/quotes -- linkable as `[[Note#^block-id]]`
- `%%hidden%%` comments invisible in reading view; `==highlight==` syntax for yellow highlight
*Source: obsidian-skills/skills/obsidian-markdown/SKILL.md*
