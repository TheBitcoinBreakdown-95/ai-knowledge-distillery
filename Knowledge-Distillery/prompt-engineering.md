# Prompt Engineering

A synthesized guide to getting consistently high-quality output from language models. Drawn from 500+ hours of AI-assisted programming, spec-driven engineering workflows, and hands-on Claude Code usage.

---

## Core Principle: Specificity Is Everything

The single highest-leverage insight across every source: **output quality is directly proportional to input specificity.** This is a communication skill, not a technical skill.

### The 3-Level Hierarchy (demonstrated with a Google Docs clone)

| Level | Prompt Style | Result |
|-------|-------------|--------|
| **1 -- Smooth Brain** | "Build Google Docs." | Nothing useful. A good tool will ask for more info; a bad one will vomit out garbage code. |
| **2 -- Average Person** | Non-technical feature description with some detail but no tech-stack info, no architecture, no screenshots. | Runs after manual fixes. Features mostly present, but zero styling, multiple errors, and "catfish code" -- looks OK at first glance, disgusting underneath. |
| **3 -- The Ideal** | Full technical context: exact tech stack, terminal commands, documentation links, design screenshots, file references. | Runs first try. Features work. Styling matches intent. Code is idiomatic because the AI had the same references a human would use. |

The gap between "AI is useless" and "AI is incredible" is almost never the model. It is almost always the prompt.

### Specificity Experiment: 500+ Hours of AI Programming

An empirical demonstration across 500+ hours confirming that prompt specificity is the primary quality lever.

- **Three levels tested building a Google Docs clone:** Smooth brain ("make a Google Docs clone"), Average (some structure), Ideal (detailed task + background/docs + do-not section) -- ideal produced working features on first try
- **Task decomposition mandate:** Break into small independent steps and identify risks before writing code -- not optional
- **Key insight:** "LLMs are multipliers, not replacements" -- AI amplifies both good and bad engineering habits equally. Specificity beats cleverness
- **Verification is non-optional:** Tests, CLI commands, CI checks, or manual steps must accompany every output

(see [testing-verification.md](testing-verification.md) for verification patterns)

*Sources: I Have Spent 500+ Hours.../Best Practices Extracted.md, I Have Spent 500+ Hours.../I Have Spent 500+ Hours Programming With AI.md*

Another concrete comparison from workflow automation:

| Vague | Specific |
|-------|----------|
| "Build me something that handles leads" | "Build a workflow that scrapes Google Maps for dentists within 50 miles of Austin, enriches with Apollo, validates emails through NeverBounce, scores by practice size and Google rating, filters for >4.2 stars and <5 years in business, and pushes qualified leads to HubSpot with a confidence score" |
| Mediocre, generic result | Exactly what was wanted |

---

## The Master Prompting Template

A 9-section framework that gives an LLM the same inputs a senior engineer would need. Use every section for complex tasks; trim to sections 2, 3, and 5 for quick iterations.

### 1. Role and Expectations

- Assign a specific role: Senior Software Engineer, Architect, Reviewer, etc.
- State goals: correct, maintainable, idiomatic solutions; clarity over cleverness.
- Set constraints: work within provided context only; if information is missing, pause and ask; do not hallucinate APIs, libraries, or behaviors.

### 2. Task (What To Do)

- **Primary objective** -- one clear, specific sentence.
- **Scope** -- what IS included and what IS NOT included.
- **Success criteria** -- what "done" looks like and how you will verify it.

> If this were handed to a human engineer, they should not need to ask for clarification.

### 3. Background and Context

Provide the ground-truth references the AI should prefer over its general training data:

- **Project overview**: purpose, target users, non-goals.
- **Tech stack**: language, framework, runtime, tooling, package manager, deployment target.
- **Codebase / files**: relevant files, existing patterns, architectural decisions already made.
- **References**: official docs, internal docs, example repos, design screenshots or Figma links.

(see [project-setup.md](project-setup.md) for the CLAUDE.md template that keeps project context persistent across sessions)

### 4. Requirements (Functional + Non-Functional)

- **Functional**: features, edge cases, error handling expectations.
- **Non-functional**: performance constraints, accessibility, security, browser/platform support.

Edge cases matter disproportionately. AI tends to nail the happy path but miss failure modes unless you enumerate them explicitly. (see [failure-patterns.md](failure-patterns.md#catfish-code-looks-good-on-surface-broken-underneath) for what happens when you skip this)

### 5. Do-Not Section (Anti-Slop Control)

Explicit exclusion list. Example:

```
Do NOT:
- Refactor unrelated files
- Change existing APIs
- Introduce new dependencies unless approved
- Simplify logic at the expense of correctness
- Invent features I did not ask for

Do NOT touch:
- src/auth/* (stable, audited)
- The database schema
```

> If something seems wrong but is outside scope -- call it out, do not change it.

### 6. Task Decomposition (Mandatory)

Before writing final code:

1. Break the task into small, independent steps.
2. Explain the approach briefly.
3. Identify potential risks or unknowns.
4. Proceed one step at a time.

If the task cannot be broken down, state why. (If you truly cannot decompose it, you do not yet understand the problem well enough.)

### 7. Verification and Proof

Require at least one of:

- Unit / integration / e2e tests (must fail before, pass after)
- CLI commands to verify
- Manual verification steps
- CI checks
- Runtime validation

Never accept unverified output. Always verify AI-generated tests are not trivially passing.

### 8. Output Format

Deliver in order:

1. Brief explanation (what and why)
2. Step-by-step plan
3. Implementation
4. Verification steps
5. Known limitations or follow-ups

Use clear headings. Minimal verbosity. No filler.

### Structured Output Format Requests

Explicitly request the output format: outline, bullets, mind map, persuasive essay, character-limited chunks, or a specific structure. Format requests are a cheap, high-leverage lever -- same content repackaged for different platforms in a single prompt. JSON as a prompt format: structuring prompts as JSON rather than prose improves LLM parsing and reduces ambiguity for complex multi-part requests.

*Sources: Old-Notes/Mastering GPT.md, Old-Notes/Prompt Engineering.md*

### 9. Prompt Self-Improvement

After completing the task, the AI should:

- Suggest how the prompt could be improved.
- Identify missing context that would improve accuracy.
- Recommend future task breakdowns.

This creates a feedback loop where each prompt teaches you to write the next one better.

### Quick-Reference: Fast Mode Template

When speed matters, compress to a single block:

```
Role: Senior engineer in [stack]
Task: [Specific task]
Context:
  - Tech stack: [...]
  - Files: [...]
  - Docs: [...]
Requirements:
  - Must: [...]
  - Must not: [...]
Do NOT: [list]
Verify with: [tests / commands]
If anything is unclear, ask before proceeding.
```

This is the minimum viable prompt for non-trivial tasks. Anything shorter risks slop.

### Top 30 Prompt Techniques for Claude 4.6

- XML tags are Claude's native language -- wrap content in `<instructions>`, `<context>`, `<examples>`, `<output>`; Anthropic tests show 30%+ output quality improvement vs. unstructured prompts
- Context before instructions: place long documents/data ABOVE the query, not after; Anthropic's own testing shows up to 30% quality improvement
- Few-shot beats adjectives: one good example is worth ten descriptions; 3-5 diverse examples covering edge cases is the sweet spot
- Explain WHY not just WHAT: "avoid ellipses since the TTS engine won't know how to pronounce them" outperforms "never use ellipses"; motivated rules generalize better
- Give permission to say "I don't know": add "If the data is insufficient to draw conclusions, say so" to every research prompt; eliminates confident hallucination
- Negative constraints: "Does NOT sound like generic AI, corporate jargon, LinkedIn influencer" is faster than describing what you do want
- Multi-Persona Debate: make Claude argue from 3 perspectives (optimistic founder / cautious CFO / customer) then synthesize; produces dramatically better analysis than single-perspective
- Self-Evaluation Loop: "Rate your answer 1-10 on accuracy, completeness, clarity. Then improve it based on your rating. Show improved version only." -- reliable error catcher
- Extended thinking trigger: "Think through this step by step before giving your final answer. Consider edge cases and potential issues." -- transforms output quality for complex problems
- 1M context tip: put longest content at TOP; use `<document index="1">` XML tags; ask Claude to quote relevant sections before analyzing; don't dump -- curate
*Source: 2026-03-23-zodchiii-httpstcogw0rshzvea.md*

---

## Quick-Use Frameworks

The full 9-section template is overkill for focused tasks. Use these lighter structures when speed matters.

### What-Why-Constraints

A minimal 3-part shorthand for organizing your thoughts before any prompt:

| Part | Purpose | Example |
|------|---------|---------|
| **What** | The specific task | "Add pagination to the /users endpoint" |
| **Why** | Business or technical reason that changes tradeoffs | "The endpoint returns 50k rows and crashes the browser" |
| **Constraints** | Guardrails and scope limits | "Use cursor-based pagination, not offset. Do not change the response schema." |

Takes 30 seconds. Prevents the most common failure mode: ambiguity. Best used when the AI already has project context via memory files and you just need to direct a focused change.

### The Three-Section Pattern (Task + Background + Do-Not)

A battle-tested middle ground between the full template and the shorthand. Covers 80% of use cases.

```
## Task
[Detailed description of what to build. Be as specific as possible.]

## Background
[Documentation links, relevant files, screenshots showing desired UI/UX flow.]

## Do Not
[What not to touch. What not to change. The only files the AI should modify.]
```

Demonstrated result: a commenting feature matching Google Docs behavior, implemented correctly in ~3 minutes of prompting versus 30-60 minutes of manual coding. The key was that each section provided a different type of constraint -- the Task said what to do, the Background removed guesswork, and the Do-Not prevented scope creep.

### First Principles Decomposition

A framework that overrides LLM pattern-matching by demanding decomposition into base truths before generating solutions:

1. What are the absolute fundamental truths here? (No assumptions)
2. What am I assuming that might be habit rather than fact?
3. If I had to explain this problem using only elementary concepts, how would I describe it?
4. What would a solution look like if built from scratch with zero legacy constraints?

Without first principles, "Create a content strategy for my SaaS" yields generic advice ("Post 3x/week, use hashtags"). With first principles, the model questions why content exists for SaaS at all, producing novel strategic insights rather than recombined templates.

Works because LLMs naturally pattern-match to training data. Explicit decomposition prompts override this default with genuine reasoning.

### Claude Code Conversation Patterns

Four interaction patterns for effective Claude Code sessions, applicable beyond prompting to session-level communication:

- **Pattern 1: Explore First** -- Ask Claude to examine existing code before making changes. "Can you look at the contact form and tell me how it works?" Prevents blind modifications.
- **Pattern 2: Specify What You Don't Want** -- Set boundaries to protect existing functionality. "Add dark mode but don't change existing light mode colors." Defensive scoping.
- **Pattern 3: Ask for Options** -- Get multiple approaches with trade-offs before committing. "What are 2-3 approaches for user authentication?" Prevents premature commitment.
- **Pattern 4: Incremental Steps** -- Break complex tasks into stages with checkpoints. "First show me what files you'd need to modify. Don't change anything yet." Maintains control.

These patterns complement the What-Why-Constraints framework (see [above](#what-why-constraints)) by addressing session flow rather than individual prompt structure.

---

## Spec-Driven Development

Write the spec before writing code. Without a clear spec, the AI hallucinates requirements -- garbage in, garbage out, but now the garbage arrives faster and with more confidence.

(see [workflow-patterns.md](workflow-patterns.md) for the full spec-driven development workflow)

### Product Specs (Happy Path / Sad Path / Edge Cases / NOT-in-MVP)

Maintain a `PRODUCT_SPEC.md` (or equivalent) containing:

- **User flows** -- step-by-step walkthroughs of every feature.
- **Happy paths** -- what happens when everything works.
- **Sad paths** -- what happens when things fail.
- **Edge cases** -- unusual scenarios ("user closes browser mid-payment").
- **Business logic** -- calculations, rate limits, capacity rules.
- **NOT in MVP** -- explicit list of deferred features.

Example:

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
- Token storage: SHA256 hash (never store plaintext)
- Session: HTTP-only cookie, 7-day expiry

### NOT in MVP
- Social auth (Google, GitHub)
- SMS-based magic links
```

The "NOT in MVP" section is critical. Half of AI productivity gains get consumed by scope creep. The AI will happily implement features you did not ask for if they seem related. An explicit exclusion list gives both you and the AI a reference point for saying no.

### System Specs (API contracts, CI definitions)

The same spec-driven approach applies to infrastructure and architecture:

- **API specs** -- define request/response shapes, error codes, and edge-case behavior before writing a single line of implementation code.
- **CI specs** -- document what each CI job checks, why it exists, what failure modes it catches, and how to fix common failures. Link each job back to a decision trace or post-mortem.
- **Invariants** -- statements that must always be true ("tokens are never stored in plaintext," "every invoice has exactly one payment request").

When the AI has a complete system spec, it implements rather than invents. The spec also becomes a conversation artifact: instead of re-explaining the payment flow every session, say "check INVOICE_SVC_SPEC.md section 4" and the AI has full context.

### Prompt-as-Spec: Gamification with Dopamine Mechanics

A detailed example of the Level 3 "Ideal" prompt style taken to its extreme -- the entire prompt is a structured specification document rather than a conversational request.

**Demonstrated with an RPG quest system (gamified task manager):**

- **Intermittent Reward Design:** Variable ratio reinforcement (slot machine psychology) -- base 70% reward chance, 30% nothing. Difficulty modifiers: Trivial -20%, Legendary guaranteed. Exploits uncertainty-before-reward for maximum engagement
- **Structured Spec Format:** Complete app specification with sections for Visual Design (color palettes, typography), Character System (stats, talent trees), Quest System (difficulty tiers with XP values), Reward Tiers (Common 50% through Legendary 1%), and Micro-Interactions
- **Behavioral Hooks:** Streak bonuses (+10% per consecutive day, caps +100%), category combos (+25% XP for 3+ same-category quests), Perfect Day guarantee (all due quests = guaranteed Rare+ reward)

The key takeaway: rather than describing what to build conversationally, structure the prompt as a specification document with headers, tables, and exact values. The AI implements a spec more faithfully than it interprets a description.

*Source: Twitter-Bookmarks/Cure Procrastination by Gamifying your life with AI (Prompt Included).md*

### Planner Agent as Prompt Architecture: Specificity Before Production

- Underlying principle: specificity of input determines quality of output; the planner step forces specificity before any production begins
- One-sentence prompt → planner expands to full scope/dependency/audience spec → builder executes from spec; eliminates silent assumption-filling
- The-interviewer pattern: (1) expand prompt into most ambitious version outline; (2) identify gaps, ask directly with proposed answers; (3) assemble brief and execute; 2 minutes upfront eliminates editing cycles
*Source: 2026-03-27-itsolelehmann-httpstcowemnpj6xem.md*

### Prompt Formatting as a Skill Layer

- Three depth levels: light (format only), standard (format + assumptions/rationale block), deep (format + research/compare/verify block)
- Tool-routing check before execution: check whether another tool would serve the task better; flag but don't block
- Two-pass audit for refinement: substance checklist first (depth calibration, self-verification, best-practice grounding, specificity), then structure checklist -- substance gaps take priority
- Anti-patterns to fix: vague thoroughness language ("be meticulous") → specific action verbs; over-prompting ("YOU MUST", "CRITICAL") → calm specific directives; buried lede → core task at top
- Pattern: a `/prompt` command that parses intent, calibrates depth, formats to structured prompt, injects depth directives, then executes
*Source: claude-code-synthesis/commands/prompt.md*

---

## Anti-Slop Controls

"Slop" is plausible-looking output that is wrong, bloated, or off-target. Every AI user encounters it. These techniques reduce it.

### Tell AI What NOT To Do (explicit exclusion list)

The Do-Not section is disproportionately effective. LLMs have tendencies: they overengineer, add unnecessary branches, create "flexibility" nobody asked for, and invent adjacent features.

Counter this with explicit constraints:

- "Keep this simple. Do not add error handling I did not ask for."
- "Linear flow, no branches unless absolutely necessary."
- "Do not create separate workflows for this."
- "Do not build admin interfaces I did not request."

LLMs respond better to explicit constraints than to open-ended requests.

### Scope Boundaries (what is in/out of this task)

- One conversation per workflow or feature. Do not reuse a conversation to build unrelated systems -- contexts bleed together and the AI loses focus.
- When switching tasks, start a fresh context or compact the conversation history.
- Use explicit "in scope / out of scope" lists in each prompt.
- Enforce the "NOT in MVP" section from your product spec.

The smaller the task, the better the result. This is not an AI trick; it is fundamental engineering. (see [failure-patterns.md](failure-patterns.md#scope-creep-by-ai-implementing-features-you-did-not-ask-for) for what happens when scope boundaries are ignored)

### The "Enhance My Prompt" Technique

A shortcut for when you have the technical information but not the patience to structure it:

1. Write a rough prompt containing all the technical details but minimal polish.
2. Tell the AI: "Enhance this prompt with LLM best practices before executing it."
3. The AI restructures your prompt -- adding sections, surfacing edge cases, clarifying ambiguities.
4. Use the enhanced version as your actual prompt.

This works because the AI knows what information it needs; it just cannot ask for it unprompted. Letting it restructure your input surfaces gaps you did not think to fill.

### Reverse Prompting: Example-to-Prompt Extraction

Show the model a finished output and ask: "What prompt would generate content exactly like this?" The model reverse-engineers hidden structure -- sentence patterns, rhetorical devices, formatting, tone -- producing a reusable template.

- Useful when you have a successful artifact but cannot articulate why it works
- Complements the "Enhance My Prompt" technique (see [above](#the-enhance-my-prompt-technique)): Enhance improves a draft prompt; Reverse Prompting creates one from an output
- Also applicable to voice/tone cloning: feed writing samples, extract style DNA, generate a reusable voice profile

*Sources: Old-Notes/Prompt Engineering.md, Old-Notes/Emails.md*

### Negation-Based Prompting for Code Quality ("Code Field")

Research showing that **inhibition shapes LLM behavior more reliably than instruction** for code generation. Negation-based prompts dramatically improved code quality:

- Bug detection: 39% to 89%
- Severity recognition: 0% to 100%
- Assumptions stated: 0% to 100%

**Atomic version (4 lines):**
```
Do not write code before stating assumptions.
Do not claim correctness you haven't verified.
Do not handle only the happy path.
Under what conditions does this work?
```

The full "Code Field" prompt adds metacognitive framing: notice the completion reflex, the pattern-match urge, the assumption that compiling equals correctness. It asks "What would a malicious caller do?" and "What would a tired maintainer misunderstand?" before any code is written.

**Key distinction:** Negation works for code because it targets premature action, not content avoidance. For non-code writing, positive framing generally outperforms negative framing (see [Positive Framing below](#positive-framing-vs-negative-framing)).

### Positive Framing vs Negative Framing

Telling Claude what NOT to do can backfire for non-code tasks. The attention mechanism highlights the forbidden concept, increasing the likelihood the model focuses on it.

| Approach | Example |
|----------|---------|
| Bad (negative) | "Do not write long, fluffy introductions" |
| Good (positive) | "Start directly with the core argument" |

**Exception:** Code Field / negation-based prompting (see [above](#negation-based-prompting-for-code-quality-code-field)) deliberately uses negation because it targets premature action, not content avoidance -- a different mechanism.

Rule of thumb: reframe every negative as a positive command for writing tasks. Reserve negation for code tasks where inhibiting action is the goal.

### Voice DNA: Persistent Writing Style Matching

A single context file that makes AI output match the user's natural writing voice.

- **Structure:** Writing rules (contractions, short paragraphs, physical verbs), formatting rules, comprehensive banned phrases list, and user writing samples at the bottom
- **Banned phrase categories:** Dead AI language ("delve," "harness," "landscape"), dead transitions ("furthermore," "moreover"), engagement bait ("let that sink in"), AI cringe ("supercharge," "10x"), and the fatal pattern: "This isn't X. This is Y." -- all negation-then-correction variants
- **Writing sample source:** Use pre-AI writing (Google Docs, reports, emails, Slack) -- writing produced after AI adoption already blends with model defaults
- **Physical verbs over abstract:** "sanded down" not "improved," "bolted on" not "added," "stripped back" not "simplified"
- **Placement:** Save as `voice-dna.md` in cowork context folder or global rules. Setup takes ~10 minutes; persists across all sessions

(see [context-engineering.md](context-engineering.md) for context file placement hierarchy)

*Source: Twitter-Bookmarks/2026-03-02-itsolelehmann-i-got-claude-to-actually-sound-like-me.md*

### Memory Files as Standing Anti-Slop Rules

Use project-level instruction files (CLAUDE.md, guidelines.md, rules files) to encode persistent rules that prevent repeated mistakes:

- Project overview and tech stack.
- Important commands and workflows.
- Project-specific conventions (naming, file structure, import patterns).
- Critical file references (e.g., database schemas) that should always be available.
- Per-technology rule files for specific frameworks or libraries.

These act as standing instructions across all sessions. The trade-off is context window: every persistent document consumes tokens. Right-size your context -- enough to prevent guessing, not so much that the AI drowns in irrelevant information.

(see [project-setup.md](project-setup.md#claudemd-templates) for the CLAUDE.md template)

### Prompting for Code Review: Unlocking Signal with "Be Harsh"

- Code review prompt: add "be harsh" -- without it, Claude defaults to polite, low-signal feedback; harsh instruction unlocks actually useful critique
- "Does not sound like ChatGPT" instruction removes the AI-generated opener pattern and produces more human-sounding writing output
- Always add "If data is insufficient, say so" to research prompts -- without this, Claude confidently invents numbers
*Source: 2026-03-26-zodchiii-httpstcovddldgl4nk.md*

### Prompt Engineering Applied to Agent System Prompts

- Peripheral position rule is the highest-leverage single optimization: move mandatory checklists and status markers to the end; identity/framing to the beginning
- Adversarial identity framing ("find bugs the developer missed") is more effective than procedural framing ("executing a browser regression test") -- framing influences every downstream decision
- Strip inline code samples from behavioral instructions: behavioral directives drive compliance; code examples burn budget without improving compliance
- Remove hedging ("when relevant," "take your time") -- replace with concrete directives; hedged language is an agent escape hatch
- Positive framing over negative: "a thorough run that catches real issues is the goal" paired with "do not rush to completion"
- Dynamic effort parameter: `medium` for local runs, `high` for CI where thoroughness matters more
- Domain tagging on failure reports (`domain=animation`, `domain=accessibility`) enables routing failures to the correct sub-skill
*Source: expect/.specs/prompt-optimization.md*

### Verbalized Sampling: Sampling From the Tails
Stanford research technique (Zhang, Manning, et al. -- arxiv 2510.01171) that counters mode collapse caused by alignment training (RLHF, DPO).

- **The mode collapse problem:** after alignment, LLMs converge on safe, typical, "most likely" responses. Creative, unusual, high-value insights get suppressed because the model learned that familiar = preferred. When you ask any AI for analysis, you're getting the most TYPICAL analysis, not the most INSIGHTFUL one. The tails of the distribution -- where the genuinely surprising insights live -- get cut off.
- **The technique:** instead of asking the model for one answer, ask it to generate multiple responses AND assign probability scores to each. Then explicitly tell it to sample from the tails -- responses with probability less than 0.10.
- **Result:** 1.6-2.1x diversity improvement in creative tasks while maintaining quality. Training-free. Works on any model. **Orthogonal to temperature** -- it stacks on top of temperature settings, doesn't replace them.
- **Why it matters for council/multi-perspective workflows:** without VS, each model gives its most typical response; with VS, each model explores its own distribution more broadly, surfacing insights it would otherwise suppress (see [agent-design.md](agent-design.md#three-layer-llm-council-multi-model--custom-lenses--verbalized-sampling) for the LLM Council application).
- **Practical prompt shape:** "Generate 5 responses to [question]. Assign each a probability score reflecting how typical/expected it is. Then give me the response with probability < 0.10 -- the tail-distribution insight."
- Real example surfaced: "should I paywall my newsletter at 99K subscribers?" -- the typical response analyzes free vs paid revenue. The tail-distribution insight reframed the question entirely: "the newsletter is the trust asset, not the revenue product. Monetization should sit ABOVE the newsletter (courses, consulting), not inside it."

*Source: 2026-04-11-alex_prompter-httpstcoyhwxqinusq.md*

### Self-Preference Bias in LLM-as-Judge
Three peer-reviewed papers documenting why single-model peer-review steps are weaker than they look:

- **NeurIPS 2024 (arxiv 2404.13076):** LLMs score their own outputs higher than other models' outputs even when humans rate them equal. Linear correlation: the better a model recognizes its own output → the stronger the self-preference bias.
- **ICLR 2025 (arxiv 2410.21819):** the mechanism is stylistic familiarity (measured via perplexity). Outputs closer to the model's own style get higher scores.
- **arXiv 2026 (arxiv 2604.06996):** the bias persists even with entirely objective criteria. Judges were up to 50% more likely to incorrectly mark outputs as correct when the output was their own.
- **Practical implication:** persona prompting (Contrarian, Expansionist, etc.) on a single model DOES generate genuinely different outputs. The weakness is in the peer-review step -- one model can't meaningfully critique five of its own outputs because they all "feel" equally familiar. Fix: use different models for evaluation/peer-review than for generation.
- (see [agent-design.md](agent-design.md#three-layer-llm-council-multi-model--custom-lenses--verbalized-sampling) for the multi-model council pattern that addresses this)

*Source: 2026-04-11-alex_prompter-httpstcoyhwxqinusq.md*

---

## Meta-Principles

| Principle | Why It Matters |
|-----------|---------------|
| **LLMs are multipliers, not replacements** | They multiply what you already know. Zero times any multiplier is still zero. You must know how to program to get programming value from AI. |
| **Specificity beats cleverness** | A detailed, boring prompt outperforms a clever, vague one every time. Communication skill is now a core engineering skill. |
| **Small tasks = better output** | Break big tasks into smaller ones. If AI is good at small tasks and bad at big ones, use that to your advantage. |
| **Typing can be outsourced; thinking cannot** | Let AI handle implementation. Keep architecture, scope, constraints, and review as your job. The moment you let AI think for you, you are useless. |
| **If you cannot break it down, you do not understand it yet** | Decomposition is not an AI technique. It is problem solving. AI just makes the penalty for skipping it more visible. |
| **Bad habits scale as well as good ones** | Skip tests, ignore edge cases, avoid documentation -- AI will amplify all of it. The developers who benefit most already had good fundamentals. |
| **Your judgment becomes code** | Specs, personas, memory files, constraints -- all are ways of externalizing your experience into machine-readable artifacts. The AI executes within them. |
| **Specs are not optional** | Without a clear spec, AI amplifies confusion. With a clear spec, AI amplifies execution. |
| **Always give AI a way to verify its work** | Tests, CLI commands, CI pipelines, browser screenshots -- any mechanism that proves the code works. Never accept unverified output. |

### Claude 4.5+ Literal Interpretation Shift

Claude 4.5+ takes instructions literally -- previous versions inferred intent and expanded on vague requests; current versions do exactly what you ask, nothing more. This requires explicitly requesting thoroughness:

- Use "Go above and beyond" or "Be thorough and comprehensive" when you want expansive output
- Without explicit requests, Claude may produce minimal responses that technically satisfy the prompt but miss your intent
- This is a feature, not a bug -- it increases precision but requires more deliberate prompting

(see [Anti-Slop Controls](#anti-slop-controls) -- this shift makes the Do-Not section less necessary for scope control but more necessary for quality control)

### Instruction Budget: ~150-200 Instructions Max

LLMs can reliably follow approximately 150-200 instructions per interaction. Claude's system prompt alone consumes ~50 instructions, leaving ~100-150 for user prompts.

Implications:
- Prioritize ruthlessly -- not every rule matters equally
- Combine related instructions into single statements
- Remove instructions that do not measurably impact output quality
- Test what happens when you remove instructions (often: nothing changes)

This creates a direct tension with comprehensive CLAUDE.md files (see [context-engineering.md](context-engineering.md)) -- every persistent instruction consumes budget. Right-size your always-loaded context.

### Model-Specific Instruction Placement

Where you place instructions relative to content matters differently per model:

| Model | Optimal Placement | Why |
|-------|-------------------|-----|
| **Claude** | Instructions at TOP, documents below | Claude processes from the beginning |
| **Gemini** | Instructions AFTER long documents (end of prompt) | 30% quality improvement when instructions follow content |
| **GPT** | Instructions at TOP and BOTTOM of documents | Sandwich pattern for best recall |

Related to the "Lost in the Middle" problem: at 32K tokens, 10/12 models in the NoLiMa benchmark dropped below 50% of short-context baseline performance on information placed in the middle.

### The "Prompt Architect" Meta-Prompt

A self-contained system prompt that turns an LLM into a prompt engineering assistant: extract intent, structure inputs, anticipate ambiguities, inject domain terminology, output modular/reusable templates.

- Protocol: define objective, understand domain, choose format, inject constraints, build few-shot examples, simulate test run, refine
- Quality gate: "Would this prompt produce the best result for a non-expert user? If not, revise."
- Distinct from "Enhance My Prompt" (starts from rough user prompt); this is a standing persona that designs prompts from scratch

*Source: Old-Notes/Prompt Engineering.md*

### The Revision Cycle as Workflow

Iteration is a feature, not a bug. The revision cycle is a legitimate workflow, not a failure of initial instruction:

1. **Initial instruction** -- Claude produces output
2. **Review** -- Identify what is right and what is wrong
3. **Specific feedback** -- "The layout is good, but change X to Y because Z"
4. **Repeat** until satisfied

**Good feedback:** Acknowledges what works, specifies exactly what to change, provides clear direction. **Bad feedback:** "It's not quite right," "Make it more professional," "This isn't what I wanted." Each round should build on what works and change one specific thing.

Key insight: you do not need to specify everything upfront. A clear initial specification + 2-3 focused revision rounds often produces better results than trying to anticipate every detail in a single prompt.

*Source: Learning-CC/notes/module-3-reflection.md, module-5-reflection.md*

### Prompting as Project Management

- Prompt as project manager, not engineer: describe the end result ("a clean landing page with big headline, 4 services, booking link") not the steps; give the brief, let Claude be the developer
- Screenshot-driven debugging: paste a visual bug screenshot and say "this section overlaps on mobile -- fix it"; faster than text descriptions
- Loop-breaking pattern: when Claude enters a fix-creates-bug spiral, type "Stop. Explain what's going wrong. Give me 2 different approaches." Forces diagnosis before the next attempt
*Source: 2026-03-19-rubenhassid-httpstcolmdv0axswg.md*

### Role-Based Prompting: Role = Context = Quality

- Role assignment is the highest-leverage single prompt change: "act as a CMO with 20 years of Fortune 500 experience" vs. "explain marketing" produces radically different output from the same model
- A good prompt does four things: assigns a role, provides context, defines the output format, and sets constraints; most prompts do only one of these
- Debate Partner and Devil's Advocate roles are useful for stress-testing ideas before committing -- structured adversarial prompting, not just asking for feedback
*Source: 2026-03-20-qwerty_ytrevvq-httpstco7izbrzyeto.md*

### Intent Parsing Before Tool Invocation

- Parse user input into structured variables (`TOPIC`, `TARGET_TOOL`, `QUERY_TYPE`, `DEPTH`) before any tool call -- intent extraction as a pre-processing step rather than mid-execution inference
- Query type taxonomy drives completely different search patterns, synthesis formats, and output structures: PROMPTING / RECOMMENDATIONS / NEWS / GENERAL
- "Use the user's exact terminology -- do not substitute or add tech names based on your knowledge. Your knowledge may be outdated -- trust the user's terminology."
- Quantity of community mentions as a primary credibility signal: "count mentions across sources" vs qualitative synthesis for recommendations queries
*Source: last30days-skill/SKILL-original.md*

---

## See Also

- [failure-patterns.md](failure-patterns.md) -- what goes wrong when prompts are vague or tasks are too large
- [workflow-patterns.md](workflow-patterns.md) -- how prompts fit into larger development workflows
- [project-setup.md](project-setup.md) -- the CLAUDE.md template and project-level context setup
