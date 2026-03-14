---
description: Deep-research verification of Knowledge Distillery claims against current web sources. Flags outd...
---

Deep-research verification of Knowledge Distillery claims against current web sources. Flags outdated, wrong, or unverifiable content to DISCREPANCIES.md.

## Usage

`/verify-kb [topic-file]` — Verify a specific topic file (e.g., `/verify-kb agent-design.md`)

If no file is specified, ask the user which file to verify.

## Instructions

1. **Read the target topic file** from `Knowledge Distillery/`.

2. **Identify verifiable claims** — Extract specific factual claims, recommendations, tool names, version-specific details, and "best practice" assertions. Skip subjective opinions and general principles.

3. **For each verifiable claim, deep-research it:**
   - Search the web for current documentation, changelogs, and community discussions
   - Check if the claim is still accurate as of today
   - Check if tools/features mentioned still exist, have been renamed, or deprecated
   - Check if recommended practices have been superseded

4. **Classify each finding:**
   - **Confirmed** — Claim matches current sources. No action needed.
   - **Outdated** — Claim was true but is no longer accurate (e.g., API changed, tool deprecated, feature renamed)
   - **Wrong** — Claim appears to be factually incorrect based on current sources
   - **Unverifiable** — Cannot find authoritative sources to confirm or deny
   - **Contradicted** — Current sources directly contradict the claim

5. **For anything not Confirmed**, append to `Knowledge Distillery/DISCREPANCIES.md` using this format:

   ```
   ### [Claim summary] — [Outdated/Wrong/Unverifiable/Contradicted]

   **File:** [topic-file.md]
   **Section:** [section heading]
   **Current claim:** [what the KB says]
   **Finding:** [what research found]
   **Source:** [URL or source name]
   **Date checked:** [today]
   **Status:** Open
   ```

6. **Report summary:**
   - Total claims checked
   - Confirmed / Outdated / Wrong / Unverifiable / Contradicted counts
   - List of items added to DISCREPANCIES.md

## Important Rules
- Do NOT modify any topic files — only write to DISCREPANCIES.md
- The user decides what to update. This command flags; the user fixes.
- Be conservative — only flag things where you have a concrete source showing the claim is wrong or outdated
- Prioritize checking: tool names/versions, API details, specific workflows, feature availability
- General principles ("test your code", "keep context small") rarely go stale — skip them
