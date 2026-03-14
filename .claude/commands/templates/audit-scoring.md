# CLAUDE.md Quality Rubric

Used by audit check A12. Scores a project's CLAUDE.md on 6 criteria for a letter grade A-F.

---

## Criteria

| # | Criterion | Weight | Description |
|---|-----------|--------|-------------|
| 1 | Commands | 20 pt | Build, test, lint, dev commands present and runnable. Full marks: all common commands listed with exact invocations. Zero: no commands section. |
| 2 | Architecture | 20 pt | Directory structure, key files, data flow, or system diagram. Full marks: someone unfamiliar could navigate the codebase. Zero: no structural info. |
| 3 | Non-obvious patterns | 20 pt | Gotchas, warnings, edge cases, "Do NOT" rules -- things Claude would get wrong without being told. Full marks: multiple project-specific warnings. Zero: only generic content. |
| 4 | Conciseness | 15 pt | Information density. Full marks: every line prevents a specific mistake, no filler, under 150 lines. Deduct for: prose walls, redundant sections, content that belongs in external docs. |
| 5 | Currency | 15 pt | Content matches the actual project state. Full marks: commands work, referenced files exist, tech stack is accurate. Deduct for: stale references, outdated commands, missing new features. |
| 6 | Actionability | 10 pt | A new Claude session could start productive work immediately. Full marks: first task could begin without asking clarifying questions. Zero: requires significant exploration first. |

**Total: 100 points**

---

## Scoring

Evaluate each criterion on its full point scale. Sum for total score.

| Grade | Score | Meaning |
|-------|-------|---------|
| A | 85-100 | Excellent -- minimal improvements possible |
| B | 70-84 | Good -- a few gaps but functional |
| C | 55-69 | Adequate -- covers basics, missing depth |
| D | 40-54 | Weak -- significant gaps affect productivity |
| F | 0-39 | Poor -- CLAUDE.md provides little useful guidance |

---

## Report Format

When triggered by audit check A12, include this in the detailed findings:

```
### A12: CLAUDE.md Quality Score -- [PASS/WARN/FAIL]

| Criterion | Score | Notes |
|-----------|-------|-------|
| Commands (20) | /20 | |
| Architecture (20) | /20 | |
| Non-obvious patterns (20) | /20 | |
| Conciseness (15) | /15 | |
| Currency (15) | /15 | |
| Actionability (10) | /10 | |
| **Total** | **/100** | **Grade: [A-F]** |
```

---

## KB References

- `context-engineering.md` > What to Include (and What NOT to Include)
- `context-engineering.md` > Four-Pillar Framework
- `project-setup.md` > CLAUDE.md Templates
- `failure-patterns.md` > Prompt Entropy
