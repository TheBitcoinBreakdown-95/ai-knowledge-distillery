# Learning Resources & Guides

Curated educational content, courses, roadmaps, and reference guides for AI/LLM development. Organized by skill level and topic. For hands-on workflow patterns, see [workflow-patterns.md](workflow-patterns.md). For tool-specific docs, see [tools-and-integrations.md](tools-and-integrations.md).

---

## Getting Started

### The Hackathon Winner's Stack (@maddiedreese)

Three-time hackathon winner's tool selection, organized by purpose:

- **Rapid prototyping**: Lovable (websites/web apps with built-in backend), Google AI Studio (fun prototypes with Gemini APIs), Bolt.new (complex apps needing terminal access), Replit (in-between projects)
- **Serious development**: Cursor (anything), Claude Code (code and file organization), YouWareAI (model choice + YouBase backend)
- **Mobile**: Rork, Vibecode, Natively; @anything for App Store publishing
- **Deploy/host**: GitHub as the gateway between code and hosting; Netlify for auto-deploy on git push
- **Design/assets**: Canva Pro (magic erase, background removal, favicons, OG images), NanoBanana Pro (images/icons), Coolors (palettes), Google Fonts, Mobbin + Dribbble (inspiration)
- **Data**: Convex or Supabase for databases; Namecheap for domains

*Source: Threads/maddiedreese - Vibe Coding Tech Stack.md*

### Model Selection for Different Tasks

- **Strategic thinking and architecture**: Claude -- handles reasoning, edge cases, and translating what the client actually needs
- **Code execution and deployment**: Cursor -- builds plans into reality, custom integrations, data transforms
- **Brainstorming and PRDs**: ChatGPT -- collecting thoughts, occasionally product requirement docs
- **Prototyping with Gemini APIs**: Google AI Studio -- easy API integration, publishing still maturing

*Source: Threads/maddiedreese - Vibe Coding Tech Stack.md*

### Claude Beginner's Guide March 2026: Models, Skills, and Cowork

- Model selection matrix (March 2026): Sonnet 4.6 = everyday workhorse (80% of use), Opus 4.6 = deep thinker for complex multi-step tasks, Haiku 4.5 = fast/cheap for quick lookups (free tier)
- Claude Skills turn repeated workflows into one-command automations; Claude can build its own skills when you describe the workflow
- Context management: use "compact" command when sessions slow down; use output restraints (word limits, bullet format) to preserve window space
- Research Mode: deep multi-source research taking 5-45 minutes, outputs cited reports

*Source: Twitter-Bookmarks/2026-03-04-aiedge-httpstcoyprrgbwqcu.md*

### Claude Managed Agents Beginner Guide
- Non-technical walkthrough of Claude Managed Agents: what it is, the 4 building blocks, and how to get started without engineering background
- Includes a Google Doc prompt template that walks Claude Code through deploying a first managed agent step by step (return-my-time.kit.com/2872b904f5)
- Business-oriented framing: identifies law firms, accounting practices, real estate agencies, medical offices as target clients who need agent builders

(see [agent-design.md](agent-design.md#claude-managed-agents-production-agent-infrastructure-2026-04-08) for the technical details)

*Source: 2026-04-09-coreyganim-httpstco3dxtbhbgwu.md*

### Claude Power User in 30 Days -- 10-Hour Path
@cyrilXBT's 30-day skill-up plan. Now charges $1,500-2,000/half-day to train teams; 14-company waitlist.

- **Week 1 (days 1-7) -- Context and Roles:** every prompt starts with a role. "Senior content strategist with 10 years in crypto media" beats "write me a tweet" by ~40% output quality. Single most-impactful habit.
- **Week 2 (days 8-14) -- Iteration:** treat every session as a working relationship. First output is never final. Brief → review → specific feedback note → improve. Three rounds produces output you couldn't write yourself. Keep one long conversation per project, not fresh sessions.
- **Week 3 (days 15-21) -- Repeatable Systems:** stop one-off tasks; build prompt templates with consistent structure (one for content, one for research, one for editing). Refine until predictable.
- **Week 4 (days 22-30) -- Persistence:** Projects for memory, skill files that load only when needed, workflows that run without babysitting.
- **The 10 power-user skills:** role assignment, constraint setting (what NOT to do), iteration loops, context preservation, persona training (paste your best work, "write in this style"), output formatting (table/bullets/headers, never unspecified), chain of thought (think step-by-step), Projects + Memory, Skill files, failure analysis ("ask Claude why" when output fails).
- **What companies pay $2K/day to teach:** the same 6 transitions -- Ask-and-hope → Role+Context+Constraint+Format; Accept first draft → 3-round iteration; Fresh sessions → Projects with persistent context; One-off tasks → Reusable templates; Generic output → Persona training; Start over on failure → Failure analysis + system update.
- **Day 8-14 is where most people quit.** Initial excitement fades, outputs are inconsistent, learning curve doing its job. Push through; this is normal. Every system that runs flawlessly went through a broken phase.

*Source: 2026-04-15-cyrilXBT-httpstcorsgtj55u8s.md*

---

## Core Frameworks

### AI Fluency Framework (4Ds)

From Anthropic's free course for educators (Dakan, Feller, and Anthropic, CC BY-NC-SA 4.0):

#### Delegation: Choose the Right Tasks for AI

- **Problem awareness**: get clear on what you are trying to do before opening an AI assistant
- **Platform awareness**: different AI systems have different strengths -- match the tool to the job
- **Task delegation**: divide work to leverage human creativity/judgment and AI speed/consistency

#### Description: Build Rich Context

- **Product description**: specify format, length, audience, style of the final output
- **Process description**: tell AI how to approach the task ("think step-by-step," "consider multiple perspectives")
- **Performance description**: define how the AI should behave ("be a critical editor," "brainstorm supportively")
- The transformation from generic assistant to thinking partner happens through rich context-building

#### Discernment: Evaluate AI Output Critically

- **Product discernment**: is the output accurate? Did it surface something you had not considered?
- **Process discernment**: did the AI follow logical steps and make reasonable assumptions?
- **Performance discernment**: did it stay in role and push back when appropriate?
- Description and Discernment form a continuous feedback loop -- each round deepens collaboration

#### Diligence: Document and Share Your AI Process

- **Creation diligence**: choose AI systems thoughtfully (privacy, security, context)
- **Transparency diligence**: be honest about how AI helped -- showcase fluent collaboration
- **Deployment diligence**: verify accuracy, take responsibility for final outputs

#### Teaching Application: AI as Your Students

- Ask AI to role-play as your students: "Where will they get confused?" "What scaffolding is needed at this transition?"
- Build a reusable Teaching Context Document through AI interview -- share it at the start of every future collaboration
- Augmentation (working with AI to enhance) beats automation (having AI do it for you), especially in learning contexts

*Source: Claude-Code/AI Fluency for educators/ (Anthropic Academy)*

### How to Learn AI the Right Way: Zero-to-Advanced Roadmap

- Start with a needs assessment before touching any tools: use Claude to identify your specific use cases and workflow gaps, then get tool recommendations tailored to those needs
- Three core fundamentals before tools: (1) AI-style thinking -- AI as thinking partner not replacement; (2) prompt engineering; (3) iteration loops -- treat every output as a first draft, re-prompt at least 3x
- Three-bucket tool stack: Daily Driver (Claude/GPT/Gemini), Agentic Tool (Manus/Runable), Learning Tool (NotebookLM); do not add a fourth bucket until you've mastered three
- Personal learning system: use Claude Opus to vibe-code a personalized 30-day learning roadmap app; complete the roadmap before expanding the stack
- Staying current: daily X scan of curated AI creator list + weekly time-blocked experimentation block (1-2 hrs) to action bookmarked workflows

*Source: Twitter-Bookmarks/2026-03-23-aiedge-httpstco7g5qsypm7m.md*

### $200/hr AI Freelancer Playbook -- Five-Phase Path
@eng_khairallah1's complete guide to AI freelancing positioning -- relevant to anyone treating freelance AI work as a career path or transition vehicle.

- **Market reality:** AI agent dev = $175-300/hr; RAG implementation = $150-250/hr; LLM integration = $125-200/hr. Demand-supply imbalance: traditional devs can write Python but not design reliable prompt architectures; AI researchers understand models but can't ship; the both-skills overlap is rare.
- **Phase 1 -- Pick ONE niche:** specialists earn more than generalists. High-demand pairs: AI agents for SaaS, AI workflow automation for professional services (law/accounting/consulting/recruiting), AI content systems for marketing teams, AI data analysis for e-commerce, custom Claude Skill development.
- **Phase 2 -- Build credibility proof (weeks 1-3):** three portfolio projects in your niche (each with live demo + write-up + architecture decisions); weekly published content on the niche; at least one testimonial (do reduced-rate or free work to get the first one).
- **Phase 3 -- Pricing:** start at $150/hr minimum (NOT $50-75). After 3-5 clients raise to $200; after 10 with testimonials consider $250. Price per project when possible, not hourly -- "$4,000 for a system saving $12,000/yr" is an easy yes; "$200/hr for undefined hours" creates anxiety.
- **Phase 4 -- Land clients:** outreach with a sample built using their actual business data (proves you understand their problem); inbound via consistent content (every piece is a permanent lead asset); referrals -- after every client ask for testimonial AND introductions.
- **Phase 5 -- Scale:** clear scope document per project (prevents scope creep, the #1 profitability killer); overdeliver on first project with a new client; offer monthly retainers; build reusable templates so the 5th customer-support agent takes half the time of the 1st.
- **Realistic timeline:** Month 1 first client; Month 2 $3-5K revenue + testimonial; Month 3 raise to $175 ($5-8K revenue); Month 4-6 hit $200/hr ($8-15K/mo); Month 6-12 established at $200+ ($15-25K/mo).
- **Window argument:** in 2-3 years supply will catch up to demand and rates will normalize; people who establish reputation now will retain client relationships newcomers can't replicate.

*Source: 2026-04-10-eng_khairallah1-httpstcobbsbrmvjug.md*

### 6-Month AI Automation Builder Roadmap (DeRonin_)
A 10,000+ word freelancer roadmap structured month-by-month, with two parallel tracks (non-technical n8n path = default; developer path = optional Python add-on). One rule: pick a lane, stop switching.

- **Month 1 -- First workflow in n8n:** master one no-code platform (n8n recommended), API/webhook/JSON vocabulary (use Postman to call api.github.com/users/torvalds, recreate in n8n), reading API docs without panicking, basic prompt engineering (system vs user, structured JSON output), what LLMs are good vs bad at. Milestone: 3-5 step workflow solving a real problem in your own life.
- **Month 2 -- Embed AI:** stop using ChatGPT manually. n8n AI Agent node, Trigger → AI Decision → Action → Output skeleton (covers 80% of real automations), error handling + Retry On Fail (the difference between 90% and 99.9% reliability), token cost awareness (input cheap, output 4-5x expensive). Practice: Gmail trigger → AI classify {support, sales, personal, spam} → route. Milestone: 3-5 workflows + clear idea of first paid gig.
- **Early Monetization (Month 2-3):** Don't wait until Month 6. Take the gig before you feel ready. Productized offers ($300-500): Lead qualification bot, Email triage assistant, Meeting notes to CRM ($400-700), Content repurposer ($250-400). Channels: Upwork ($30-50/hr first 2-3 jobs), Fiverr (productized fixed price), Contra ($500-2K projects), n8n Template Marketplace (free leads), own X/LinkedIn. Always deliver: workflow JSON + 3-5min Loom + 1-page Notion runbook + 7 days free support.
- **Month 3 -- Repeatable services:** Build 1-2 polished workflows you can resell. Six in-demand use cases with sellable price points: Lead Gen Pipeline ($1,500 + $500/mo), Personalized Outreach ($2,000 + $1,000/mo), CRM Autopilot ($1,500 + $750/mo), AI Content Engine ($2,500 + $1,000/mo), Meeting Autopilot ($1,200 + $600/mo), Internal Knowledge Bot ($2,500 + $500/mo). Don't build all six -- pick 1-2.
- **Month 4 -- Agents (carefully):** 70% of the time an agent is the wrong choice. Single LLM call vs Fixed chain vs Agent decision framework: only use an agent when number of steps is genuinely unknown and depends on input. Build inside n8n's AI Agent node (max 3-5 tools, max 10-15 iterations, human-in-the-loop on irreversible actions). Mandatory reading: Anthropic's Building Effective Agents.
- **Month 5 -- Production-ready:** Railway 1-click n8n deploy with custom domain + HTTPS (skip Docker until 5+ clients). Better Stack monitoring + Langfuse for LLM observability. Prompt versioning (Notion DB or Langfuse). Security: never paste keys into nodes -- use n8n credentials vault. OWASP Top 10 for LLM Apps. Documentation = the difference between $500 and $5,000 projects.
- **Month 6 -- Direction:** Pick ONE: Freelance Automation Builder (fastest income, $500-2K projects + $1-3K/mo retainers), In-House Automation Builder (salary $75-280K, ROI metrics), AI Automation Agency (E-Myth/Built to Sell, niche down by industry, hire after 3+ paying clients).
- Realistic targets: junior $75-110K, mid-level $125-180K, senior $180-280K+; freelance $500-5K/project + $1-3K/mo retainer + $100-250/hr; agency $500-5K setup + $1-5K/mo managed + $3-15K full custom + $10-50K enterprise.

*Source: 2026-04-13-DeRonin-httpstcopouik6acsd.md*

### Lunour Brand Playbook -- Four Pillars of B2B Branding
@scott_bair (Lunour co-founder) on building B2B brands as a business strategy, not a design project. Substantive enough to function as a reference doc.

- **Four pillars (skip one and the whole structure wobbles):** Positioning (where you stand and why) → Messaging (how you say it) → Visual Identity (how you look) → Brand System (toolkit that scales)
- **Positioning trap:** "Full-service technology solutions provider" or "We help businesses grow" communicates nothing. Narrow positioning creates power. Like New Kind: "No agency in the world has more experience branding open source companies." Verifiable, narrow, owns the category.
- **Five-step positioning exercise (April Dunford framework):** (1) list competitive alternatives including doing nothing -- inertia is the real competitor in B2B; (2) identify unique attributes (be ruthless); (3) define the value those attributes create; (4) describe best-fit customer specifically (industry, stage, trigger event, pain); (5) name your category (the frame -- "revenue intelligence platform" hits differently than "sales analytics software")
- **Messaging hierarchy (4 levels):** Level 1 one-liner (7-12 words, outcome-focused, no jargon); Level 2 elevator pitch (3-4 sentences); Level 3 proof narrative (2-3min, case studies); Level 4 deep dive (full methodology, blog/podcasts/whitepapers)
- **Voice and tone:** define 3-4 voice attributes; for each define what it IS and what it ISN'T; write 10 sample sentences in your brand voice across contexts to validate. Tone shifts with context; voice stays constant.
- **Visual identity components:** logo (overrated alone), typography (most underrated -- does more heavy lifting than anything), color (90ms emotional response), photography/illustration style (most B2B brands fall apart here), iconography. Distinctive over decorative; ownable territory; system thinking from day one.
- **Brand system (the part most companies skip):** logo guidelines, type system, color system, grid/layout, photography guidelines, icon library, component library, templates (deck/social/email/proposals), motion guidelines. Test: can a non-designer team member create on-brand collateral? If no, you don't have a system, you have a logo and colors.
- **Tiered build approach:** Tier 1 essentials (Day 1) -- logo guidelines, color, typography, quick reference card; Tier 2 working system (Month 1) -- grid, photo direction, deck/social/email templates; Tier 3 comprehensive (Q1) -- component library, icons, motion, full templates, voice guide.
- **Investment benchmarks:** pre-seed $2-5K DIY; Series A $15-40K strategy + core identity; Series B+ $50K+ comprehensive. Common rule: 5-10% of first-year revenue target. Big-name studios (Pentagram, Collins, Wolff Olins) $200K-$1M+; mid-tier studios $30-100K produce comparable transformation.
- **Five common branding mistakes:** start with visuals before strategy; design by committee (great brands are opinionated); chase trends instead of longevity (IBM logo, 1972, untouched); inconsistency across touchpoints (system problem, not design problem); treating launch as finish line (it's a starting line).

*Source: 2026-04-13-scott_bair-httpstcoc6jjyn6a9u.md*

### $2M Digital Product Playbook -- Niching to Niche-Within-Niche
@dickiebush's playbook from $20M+ in digital product sales. Relevant to the user's coaching/teaching side path -- product-creation framework rather than "build a course."

- **Lesson from "Podcast Compendium" first product ($400 flop):** you don't need a huge audience to launch. Your first product should be work you've already done. People pay for organized thinking. But: positioning must come first; otherwise the product disappoints buyers and they warn others.
- **Lesson from "Ship 30 for 30" ($2M+ scale):** a tweet asking if anyone wanted accountability for daily writing. 50+ people paid to join the first cohort. 12 months → 7 figures.
- **The 4-step framework (creates a sellable product anyone can run):**
  1. **Mega-category → niche → niche-within-niche.** Don't say "I help all writers." Say "I help beginner writers start writing online." The narrower, the higher the conversion.
  2. **List 10 biggest problems** the niche-within-niche faces (distractions, perfectionism, imposter syndrome, finding time, etc.). Game isn't every possible problem -- top 10.
  3. **List 10 most desirable outcomes** for the same audience. Ideally outcomes you yourself have wanted/achieved. Write as "I" statements: "If I wasn't distracted, I would be so much more productive."
  4. **Pick the most painful/expensive problem** and create the product around it. **Lead with ONE problem** in positioning, even if the product solves all 10.
- **Three pro tips:**
  - Tip 1: outcomes you market should be outcomes YOU have wanted/achieved -- otherwise why are you selling a solution to your own unsolved problem
  - Tip 2: shortcut -- take the 10 problems list and write the desirable outcome next to each
  - Tip 3: write outcomes as "I" statements (puts you in the customer's mind)
- **Action-oriented learning:** people don't want random information; they want learning that helps them ACT, because action increases the likelihood of achieving the desired outcome. Learning for its own sake doesn't sell.
- **Anti-pattern called out:** "creating a digital product" by recording rambling slides + slapping into a bonus PDF + rushing to sell. Without product-creation work, marketing/launch/tech stack don't matter.

*Source: 2026-04-20-dickiebush-httpstcootjwhn6qu8.md*

### Postiz + One Niche -- AI Social Media Productized Service (Greg Isenberg)
@gregisenberg's startup recipe using open-source Postiz (see [tools-and-integrations.md > Postiz](tools-and-integrations.md#postiz-open-source-social-media-scheduling-stack)) as the engine + niche-down focus + AI captions as the hook.

- **Pattern:** "Open source is the new wholesale. The code is free. The customer relationship is where the margin lives."
- **Steps:**
  1. Self-host Postiz (figure out via Codex/Claude Code in an afternoon)
  2. Pick ONE niche -- not just "lawyers" but "family law attorneys"; not just "dentists" but "orthodontists"
  3. Wrap in their language -- "AI social media for dental practices"
  4. **The hook:** "we write your captions with AI" -- that's what they're actually paying for
  5. Plug into n8n / Make / Zapier so posting + scheduling + approvals run on autopilot; client approves with one tap
  6. Charge $50-100/seat/mo -- compares against $2,000/mo social media freelancer; you're 25x cheaper, 10x more reliable
  7. One landing page + one onboarding call = the entire sales motion
  8. Build niche-specific media presence (X, TikTok, YouTube) -- become "the social media for dentists" person
  9. Reinvest profits to layer adjacent tools for the same niche (scheduling, reviews, patient intake) -- own the vertical
- **The market intuition:** these businesses know they need to post, hate doing it, will never find Postiz on GitHub themselves. They Google "someone please handle my social media" -- that's you.
- Replicable as a one-person or two-person business -- no funding, no office, just a laptop + a niche + willingness to start.

*Source: 2026-04-25-gregisenberg-startup-idea-for-you-use-postiz-20k-github-stars-project-to.md*

### The Five Levels of Claude (Nate Herk)
A leveling ladder from "Claude as search bar" to "Claude as infrastructure," with the friction point and cheat code that gets you to the next level. After 400+ hours across Chat, Cowork, and Claude Code.

- **Level 1: The Enthusiast** — Open Claude, ask question, close tab. ~30 min/day saved. Stall: treating Claude as stateless search. **Cheat code → Level 2:** create your first Project (drop reference docs, write a system prompt, every chat starts pre-loaded).
- **Level 2: The Beginner** — Projects + memory + connectors + real Excel/PPT/Word/PDF file creation + Office add-ons (April 2026 cross-app context: analyze in Excel → switch to PowerPoint → Claude builds deck with that analysis). Inline visuals + persistent artifacts that can call Claude's API. Save 5+ hours/week. **Stall:** Claude can't do anything ON your machine. **Cheat code → Level 3:** open the Claude Desktop "cowork" tab.
- **Level 3: The Intermediate** — Cowork runs on your machine with filesystem access, runs code in an isolated VM, real read/write on granted folders. Skills (over 100 published, 16+ official), scheduled tasks (`/schedule`), mobile control (dispatch + phone), Cloud Design (separate Anthropic Labs product, reads codebase/brand to design from your fonts/colors and packages handoff bundles for Claude Code/Canva). 10+ hours/week saved — minimum bar for selling automation as a service. **Stall:** "scared of anything technical" OR "cowork ceiling — safe but less precise than what comes next." **Cheat code → Level 4:** folder structure cowork can rely on (about-me file, templates folder, projects folder, outputs folder + "never edit templates, always deliver to outputs").
- **Level 4: The Advanced User** — Claude Code with parallel sessions. Boris Cherny (built Claude Code) runs 5 numbered terminal tabs daily. `claude.md` at project root (keep under 200 lines; push detail to separate files referenced with `@filename`); the level-4 move = "every time Claude makes a mistake, say 'update your claude.md so you don't make that mistake again.'" Plan mode (shift+tab twice; hidden Opus Plan setting = Opus plans + Sonnet executes = cost cut in half). Sub-agents (specialized contexts, parallel, communicate via main session). Worktrees (`claude-worktree feature-name` for isolated git branches, 3-4 in parallel comfortable). MCP with a big asterisk — when a CLI exists, use it: CLIs use 60-70% fewer tokens than equivalent MCP because nothing loads until you run it. **Power moves:** `/compact` proactively (not when warnings fire — too late); `/context`, prompt caching → 60-90% cost cut; auto mode + `/focus`; **the verification loop** (Boris: "give Claude a way to check its own work" via Chrome extension that opens a browser, tests UI, iterates — "2-3x quality"); custom slash commands at `.claude/commands/` (Boris uses `/commit-push-pr` dozens of times/day); `/rewind` (drops failed attempt out of context), `/btw` (mid-task question without polluting), `/branch` (fork conversation), `/insights` (past-month usage report), `/output-style new` (swap Claude Code personality). $5K-$15K freelance project tier.
- **Level 5: The Architect** — **Cloud routines** (saved configs running on Anthropic's cloud; scheduled, API-triggered, or GitHub-event-triggered; laptop closed and work still happens). **Hooks** (pre-tool-use blocks dangerous commands; post-edit auto-formats; stop hooks ping Slack). **Channels** (Discord/Telegram/iMessage/webhooks; one-way calendar booking → research agent; two-way text from phone against your codebase). **Headless mode + Agent SDK** (Python/TypeScript libs to build your own product on Claude Code's engine). **Remote control** (bridge Claude Code session to mobile app via QR). **Memory consolidation (autodream)** — background sub-agent prunes memory files between sessions (deletes contradicted facts, merges duplicates, converts "yesterday" to actual dates). **Task budgets** (Opus 4.7 beta: give the agent a token target, it self-regulates and wraps up gracefully — API only right now). **Agent teams** (still experimental; multiple specialized Claudes message each other via shared task list; A2A protocol for agent-to-agent).
- **The real stall is trust, not technical.** "Almost anyone can set up a cloud routine. They won't. Because handing the steering wheel to a system that runs while you're asleep feels reckless." The fix: empty parking lot, not the highway. Pick a low-stakes routine (daily stand-up that only goes to you), watch it run for weeks, don't touch it. Once you trust it, you'll trust the next ten.

*Source: 2026-05-12-nateherk-httpstcouhjtuzcqef.md*

---

## Technical Deep Dives

### LLM Quantization Explained: Interactive Guide from First Principles

- Quantization converts model weights from 32-bit floats to lower-precision integers (8-bit, 4-bit, 2-bit), shrinking model size and increasing inference speed
- Empirical results on Qwen 3.5 9B: 8-bit = near-zero quality loss + 66% speed gain; 4-bit = ~5-10% accuracy loss + 2-3x speed; 2-bit = unusable
- Key insight: quality doesn't degrade linearly -- 8-bit is the sweet spot for most local model deployments
- Interactive essay at ngrok.com/blog/quantization for anyone choosing quantization settings for local models

*Source: Twitter-Bookmarks/2026-03-25-ngrokHQ-quantization-can-make-an-llm-4x-smaller-and-2x-faster-with-b.md*

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

*Source: Twitter-Bookmarks/the 2026 ai engineer roadmap.md*

### 6-Month Claude Architect Learning Path

- Month 1-2: master prompt engineering and production-ready prompts; go API-native (streaming, conversation history, chaining, error handling)
- Month 3: tool use -- writing tool descriptions Claude interprets correctly, handling outputs, chaining multi-step tool use
- Month 5: multi-agent systems, vector databases for long-term memory, evaluation suites that test prompts against expected outputs
- The real dividing line is architecture, not intelligence: architects work in the API; practitioners work in the chat interface

*Source: Twitter-Bookmarks/2026-03-19-cyrilXBT-httpstcoe1lw0c8xkf.md*

---

## Platform References

### Everything Claude Shipped in 2026: Complete Feature Guide

- Model matrix: Opus 4.6 (1M context, $5/$25/M tokens, 128K output, 14.5hr task window), Sonnet 4.6 (1M context, $3/$15/M tokens, 64K output, 30-50% faster than Sonnet 4.5), Haiku 4.5 (fast/cheap, zero prompt injection protection -- risky for untrusted input in agentic setups)
- 1M context now at standard pricing (was premium >200K): as of March 13, no surcharge; media limit jumped to 600 images/PDF pages per request (was 100)
- Four Claude modes: Chat (browser/mobile, conversation), Cowork (desktop agent, autonomous file/task execution), Code (terminal, codebase-aware), Projects (saved workspaces with stable context)
- Memory: available to all users including free since March 2; can view/edit/delete in Settings > Capabilities; import/export supported; Cowork sessions don't persist memory -- use context files as workaround
- Rule of thumb: Chat for quick questions, Cowork for delegated work on your files, Code for development, Projects for recurring work with stable context

*Source: Twitter-Bookmarks/2026-03-24-kloss_xyz-httpstcop2ldwjt7kj.md*

### Timeline of Claude 2026 Launches

- Comprehensive chronological timeline of every Claude product launch from January through March 2026, including Cowork, Sonnet 4.6, Opus 4.6, memory, auto mode, and integrations
- Useful reference for orienting new users or catching up after time away from the Claude ecosystem

*Source: Twitter-Bookmarks/2026-03-24-TawohAwa-every-new-claude-launch-since-the-beginning-of-2026-jan-2026.md*

### OpenMAIC: Multi-Agent AI Classroom Platform
- Open-source platform from Tsinghua University that generates interactive courses from a single prompt -- not slides or chatbots but a live classroom with AI teacher, AI classmates, and real-time discussion
- Architecture: LangGraph-based Director-Generator-Director DAG loop coordinates multiple agent personas (Mentor, TA, Peer) that interact, interrupt, and challenge each other during lessons
- Four auto-generated course components: voice-guided interactive slides with synchronized teaching actions, auto-graded quizzes integrated into session flow, scenario-based GenUI interactive web pages (exportable as static HTML), and project-based collaborative learning modules
- Multimodal input support (speech, images, video, web content); LLM provider configurable via BYOK; fully self-hostable with no cloud dependency
- Distinct from typical AI education tools: starts from learning goals rather than existing content; agents participate in discussion rather than just delivering information

(see [agent-design.md](agent-design.md) for multi-agent coordination patterns used in the underlying architecture)

*Source: 2026-03-15-heyshrutimishra-httpstcoqhdo5z8pus.md*

---

## Free Courses and Guides

### Google Skills Hub (@aaditsh)

- 3,000 free technical modules replacing "prompting" fluff with actual DeepMind research workflows
- Same curriculum used to train Google's internal teams on transformer architecture
- Launched quietly; access at skills.google.com

### Anthropic's AI Fluency Courses (Free)

- **AI Fluency: Framework & Foundations** -- the core 4D framework course
- **AI Fluency for Educators** -- applying 4Ds to course design, material creation, and assessment
- **AI Fluency for Students** -- companion course designed for learners directly
- All available on Anthropic Academy (anthropic.skilljar.com)

### Anthropic Academy: 13+ Free Official Courses with Certificates

- Anthropic Academy (anthropic.skilljar.com) offers 13+ official free courses with certificates, no subscription required
- Key courses: Claude 101, Claude Code in Action, Building with the Claude API (8+ hours), Intro to MCP + Advanced MCP, Agent Skills, Claude on AWS Bedrock and Google Vertex AI

*Source: Twitter-Bookmarks/2026-03-14-RoundtableSpace-anthropic-just-launched-anthropic-academy-totally-free-13-of.md*

### Visual Guide to Master Claude Code

- A curated visual/illustrated guide for mastering Claude Code, published as a GitHub resource (luongnv89/claude-howto)
- Useful as a reference/onboarding resource for new Claude Code users

*Source: Twitter-Bookmarks/2026-03-26-tom_doerr-visual-guide-to-master-claude-code-httpstcowxryizmwvk-httpst.md*

### Curated Free Resource List for Building AI Agents
- Seven essential papers for agent foundations: ReAct (reasoning + acting loop), Generative Agents (Stanford believable simulacra), Toolformer (self-learning tool use), Chain-of-Thought (step-by-step reasoning), Tree of Thoughts (deliberate search over reasoning paths), Reflexion (self-critique feedback loops), and a comprehensive RAG Survey
- Key frameworks to study hands-on: LangChain (composable chains), AutoGen (Microsoft multi-agent conversations), CrewAI (role-based agent teams), OpenAI Swarm (lightweight handoff orchestration), AgentGPT (autonomous browser agent)
- Two must-read guides that synthesize the field: Lilian Weng's "LLM Powered Autonomous Agents" (comprehensive taxonomy) and Anthropic's "Building Effective Agents" (practical patterns over frameworks)
- Recommended 4-week self-study path: Week 1 (Weng guide + ReAct paper + Karpathy intro lectures), Week 2 (LangGraph hands-on), Week 3 (Anthropic guide + build a working agent), Week 4 (deeper papers and advanced patterns)
- Newsletters for staying current: The Rundown AI, TLDR AI, Import AI (Jack Clark), The Batch (Andrew Ng), Last Week in AI

(see [agent-design.md](agent-design.md) for synthesized agent architecture patterns; see [Anthropic Academy](#anthropic-academy-13-free-official-courses-with-certificates) for structured courses)

*Source: 2026-03-12-mayorxbt-httpstcocevntfha7b.md*

### Awesome Open-Source AI: Curated Project Directory
- Curated list of the best truly open-source AI projects covering agents, RAG, machine learning, MLOps, tools, and infrastructure
- Useful as a discovery layer for open-source alternatives to commercial AI tools and for finding reference implementations of agent patterns
- GitHub: alvinreal/awesome-opensource-ai

*Source: GitHub Stars*

### 40 No-Code AI Automations You Can Build This Weekend
@eng_khairallah1's catalog of 40 automations for non-technical builders using Claude + Cowork + MCP servers + free tools. Grouped by domain.

- **Content & Writing (1-10):** Weekly newsletter draft, social repurposer (1 article → 10 tweets + 3 LinkedIn + 2 IG + 1 email), blog post from voice notes, content calendar, SEO article writer (Tavily research + structured output), email sequence builder, YouTube script generator, thread expander, comment response bank, headline tester (20 variations across 5 frameworks)
- **Research & Analysis (11-20):** Competitor tracker, industry news digest, market research report, trend spotter, book summary system, meeting research prep, patent/product scanner, pricing analyzer, audience research engine, investment research brief
- **Productivity & Organization (21-30):** Inbox zero processor, file organizer, meeting notes → action items, weekly review generator, SOPs from your brain, invoice processor, travel planner, habit tracker review, personal CRM updater, daily briefing
- **Business & Revenue (31-40):** Proposal generator, client onboarding docs, product description writer, review response system, sales email personalizer, financial report formatter, contract summarizer, knowledge base builder, testimonial collector, workflow audit report
- **The 4-step build process:** Define task (in/out) → write skill file → add your context → test and refine
- Pick 3 highest-leverage automations first; build those; come back for more. People building these save 10-20 hours/week not because they're technical but because they took one afternoon to set up something that runs forever.

*Source: 2026-04-12-eng_khairallah1-httpstcorg0hlv0uc3.md*
