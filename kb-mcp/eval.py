"""
Evaluation harness for KB retrieval quality.

Imports the LIVE server pipeline from kb_mcp_server (query expansion, FTS,
vector, RRF merge) so the eval measures exactly what the MCP server serves --
no reimplemented search (audit M2-8). Run after /consolidate-kb; consolidation
renames H2 sections, which is what breaks fixtures.

Baseline ratified per Decision Gate G8 (2026-06-10): thresholds are floors set
from the first honest run of the real pipeline, not aspirations. The gate is
the HYBRID mode (the deployed path); BM25-only is reported as the Ollama-down
fallback path.
"""

import sys

from kb_mcp_server import (embed_query, expand_query, get_table, rrf_merge,
                           search_fts, search_vector)

# G8 ratified floors. First honest run of the real pipeline (2026-06-10):
# hybrid Recall@5 93.3%, P@1 63.3%, MRR 0.747. Floors sit at/just under that
# baseline; a future run below them is a real regression, not noise. The old
# aspirational P@1 70% was never measured against the deployed path.
RECALL_FLOOR = 0.90
P1_FLOOR = 0.60
MRR_FLOOR = 0.70

# Known-answer test cases: (query, expected_chunk_ids)
# Each query should find at least one of the expected chunks in top-5
TEST_CASES = [
    # Exact match / keyword queries
    ("context pollution", ["context-engineering__anti-pattern-context-pollution"]),
    ("CLAUDE.md", ["context-engineering__claudemd-your-always-loaded-memory"]),
    ("plausible echo", ["testing-verification__the-plausible-echo-problem"]),
    ("Ralph loop", ["workflow-patterns__pattern-2-the-ralph-loop-autonomous-coding"]),
    ("kickoff questions", ["project-setup__the-8-kickoff-questions"]),
    ("PostToolUse hooks", ["tools-and-integrations__hooks-prepost-tool-automation"]),
    ("anti-slop controls", ["prompt-engineering__anti-slop-controls"]),
    ("brain muscles pattern", ["agent-design__brain-muscles-pattern-from-openclaw",
                               "autonomous-agents__brain-muscles-architecture"]),
    ("MCP servers", ["tools-and-integrations__mcp-servers-plugins"]),
    ("worklogs session continuity", ["memory-persistence__the-memory-problem-every-session-starts-at-zero",
                                     "memory-persistence__the-four-layer-memory-model"]),

    # Conceptual queries (no exact keyword match expected)
    ("how to prevent AI from making stuff up", ["failure-patterns__the-four-named-patterns",
                                                 "testing-verification__the-plausible-echo-problem"]),
    ("what should go in my project instructions file", ["context-engineering__claudemd-your-always-loaded-memory",
                                                         "project-setup__the-8-kickoff-questions"]),
    ("running autonomous agents safely", ["autonomous-agents__security-rules-non-negotiable"]),
    ("how to structure a prompt", ["prompt-engineering__the-master-prompting-template",
                                    "prompt-engineering__core-principle-specificity-is-everything"]),
    ("verifying AI outputs", ["testing-verification__core-principle-verify-artifacts-not-self-reports"]),
    ("when to use subagents vs skills", ["agent-design__skills-vs-subagents-same-brain-or-separate-invocation",
                                          "agent-design__when-to-use-which-architecture"]),

    # Cross-topic queries
    ("context window management and caching", ["context-engineering__context-window-management",
                                                "context-engineering__prompt-cache-architecture"]),
    ("CI/CD with Claude Code", ["tools-and-integrations__cicd-integration"]),
    ("vibe coding workflow", ["workflow-patterns__the-vibe-engineering-stack"]),
    ("OpenClaw setup", ["autonomous-agents__what-is-openclaw",
                        "autonomous-agents__first-steps-after-setup"]),

    # KB-specific terms
    ("Enforcement Guarantee Ladder", ["context-engineering__knowledge-type-placement-matrix"]),
    ("GSD framework", ["workflow-patterns__pattern-6-gsd-get-shit-done-execution-framework"]),
    ("spec driven development", ["workflow-patterns__pattern-1-spec-driven-feature-development",
                                  "prompt-engineering__spec-driven-development"]),
    ("compound effect skills hooks MCP", ["tools-and-integrations__the-compound-effect-skills-hooks-mcp-together"]),
    ("invariants vs requirements", ["testing-verification__invariants-vs-requirements"]),

    # Negative/edge cases (should still find something reasonable)
    ("settings.json configuration", ["project-setup__settingsjson-patterns"]),
    ("meta-agent orchestration", ["workflow-patterns__pattern-3-meta-agent-orchestration",
                                   "agent-design__meta-agent-architecture"]),
    ("local LLM embedding models", ["community-insights__running-ai-locally"]),
    ("memory persistence across sessions", ["memory-persistence__the-memory-problem-every-session-starts-at-zero",
                                             "memory-persistence__the-four-layer-memory-model"]),
    ("SDK programmatic access", ["tools-and-integrations__claude-code-sdk-programmatic-access"]),
]


def ids_bm25(table, query: str, top_k: int = 5) -> list[str]:
    """Server fallback path: expanded query, FTS only (Ollama down)."""
    expanded = expand_query(query)
    return [r["id"] for r in search_fts(table, expanded, top_k)]


def ids_hybrid(table, query: str, top_k: int = 5) -> list[str]:
    """The deployed search_kb path: expansion, FTS@15 + vector@15, RRF."""
    expanded = expand_query(query)
    fts_results = search_fts(table, expanded, top_k=15)
    query_vec = embed_query(expanded)
    if query_vec is None:
        merged = fts_results
    else:
        merged = rrf_merge([fts_results, search_vector(table, query_vec, top_k=15)])
    return [r["id"] for r in merged[:top_k]]


def evaluate(table, search_fn, label: str, top_k: int = 5) -> dict:
    """Run all test cases against a search function."""
    recall_hits = 0
    p1_hits = 0
    rr_sum = 0.0
    total = len(TEST_CASES)
    failures = []

    for query, expected_ids in TEST_CASES:
        results = search_fn(table, query, top_k)
        hit = any(eid in results for eid in expected_ids)
        if hit:
            recall_hits += 1
        else:
            failures.append((query, expected_ids, results))

        if results and results[0] in expected_ids:
            p1_hits += 1

        for rank, rid in enumerate(results):
            if rid in expected_ids:
                rr_sum += 1.0 / (rank + 1)
                break

    return {
        "label": label,
        "recall_at_k": recall_hits / total,
        "p_at_1": p1_hits / total,
        "mrr": rr_sum / total,
        "total": total,
        "recall_hits": recall_hits,
        "p1_hits": p1_hits,
        "failures": failures,
    }


def print_results(res: dict, gated: bool, verbose: bool = False) -> None:
    label = res["label"]
    r, p, m = res["recall_at_k"], res["p_at_1"], res["mrr"]
    total = res["total"]
    suffix = "" if gated else "  (informational, not gated)"

    print(f"\n{'='*60}")
    print(f"  {label}{suffix}")
    print(f"{'='*60}")
    print(f"  Recall@5:  {r:.1%} ({res['recall_hits']}/{total})  (floor >= {RECALL_FLOOR:.0%})")
    print(f"  P@1:       {p:.1%} ({res['p1_hits']}/{total})  (floor >= {P1_FLOOR:.0%})")
    print(f"  MRR:       {m:.3f}             (floor >= {MRR_FLOOR:.2f})")

    if verbose and res["failures"]:
        print(f"\n  Failures ({len(res['failures'])}):")
        for query, expected, got in res["failures"]:
            print(f"    Q: {query}")
            print(f"    Expected: {expected}")
            print(f"    Got top-5: {got[:5]}")
            print()


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, help="Debug a single query")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show failures")
    args = parser.parse_args()

    table = get_table()

    if args.query:
        print(f"Query: {args.query}\n")
        print("BM25 (server fallback) results:")
        for i, rid in enumerate(ids_bm25(table, args.query, 5)):
            print(f"  {i+1}. {rid}")
        print("\nHybrid (deployed path) results:")
        for i, rid in enumerate(ids_hybrid(table, args.query, 5)):
            print(f"  {i+1}. {rid}")
        return

    print("Running evaluation against the live server pipeline...")
    bm25_res = evaluate(table, ids_bm25, "Server BM25 fallback")
    hybrid_res = evaluate(table, ids_hybrid, "Server hybrid (search_kb path)")

    print_results(bm25_res, gated=False, verbose=args.verbose)
    print_results(hybrid_res, gated=True, verbose=args.verbose)

    print(f"\n{'='*60}")
    hybrid_pass = (hybrid_res["recall_at_k"] >= RECALL_FLOOR
                   and hybrid_res["p_at_1"] >= P1_FLOOR
                   and hybrid_res["mrr"] >= MRR_FLOOR)
    if hybrid_pass:
        print("  OVERALL: PASS -- hybrid pipeline meets the ratified G8 floors")
    else:
        print("  OVERALL: FAIL -- hybrid pipeline regressed below the G8 floors")
    print(f"{'='*60}")

    sys.exit(0 if hybrid_pass else 1)


if __name__ == "__main__":
    main()
