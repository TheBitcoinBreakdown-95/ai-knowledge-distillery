---
description: Compare a new article, URL, or text against the Knowledge Distillery. Identifies gaps, suggests KB placement, and proposes workspace actions.
---

Process a new insight against the Knowledge Distillery. Compares new content with existing KB, identifies genuine gaps, and suggests concrete actions.

## Usage

`/process-insight $ARGUMENTS` -- Pass a URL, file path, or inline text to analyze.

## Instructions

### Step 1: Extract Content

a. If `$ARGUMENTS` is a URL, fetch it with WebFetch and extract the main content.
b. If it is a file path, read the file.
c. If it is inline text, use it directly.
d. Summarize the key claims and practices in 3-5 bullets.

### Step 2: Compare Against KB

a. Use `search_kb` (MCP tool) to find related existing content for each key claim.
b. For each claim, classify as:
   - **Already covered:** KB has this. Note the file and section.
   - **Extends existing:** KB covers the topic but this adds new detail. Note the gap.
   - **New concept:** KB does not cover this at all.
   - **Contradicts KB:** This disagrees with existing KB content. Note the conflict.

### Step 3: Report Findings

Present a table:

| # | Claim | Status | KB Location | Action |
|---|-------|--------|-------------|--------|

### Step 4: Suggest Actions

For each non-"Already covered" item, suggest one of:
- **Add to [topic-file.md]** -- with a draft entry for `## Recent Additions`
- **Log to DISCREPANCIES.md** -- if it contradicts existing content
- **New topic file** -- if it does not fit any existing file (rare -- ask user first)
- **Update workspace rule/hook/command** -- if the insight has framework implications

### Step 5: Apply on Approval

Do not make changes automatically. Present all suggestions, then ask: "Apply these? (all / pick numbers / skip)"

## Constraints

- Read-only until Step 5 approval
- Do not force-fit content into community-insights.md -- if it does not belong in any existing file, say so
- Always attribute the source (URL, file path, or "user-provided text")
- Keep draft entries under 10 lines each
