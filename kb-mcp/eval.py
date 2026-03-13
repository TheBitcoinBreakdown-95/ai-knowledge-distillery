"""
Evaluation harness for KB retrieval quality.
Tests BM25, vector, and hybrid search against known-answer queries.
Must pass thresholds before MCP server is deployed.

Thresholds: Recall@5 >= 90%, P@1 >= 70%, MRR >= 0.7
"""

import json
import sys
from pathlib import Path

import httpx
import lancedb

OLLAMA_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "mxbai-embed-large"
TABLE_NAME = "kb_chunks"

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
    ("MCP servers", ["tools-and-integrations__mcp-servers-extending-capabilities"]),
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
    ("Enforcement Guarantee Ladder", ["context-engineering__recent-additions"]),
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


def get_kb_dir() -> Path:
    return Path(__file__).parent.parent / "Knowledge Distillery"


def embed_query(query: str) -> list[float]:
    resp = httpx.post(
        OLLAMA_URL,
        json={"model": EMBED_MODEL, "input": query},
        timeout=60.0,
    )
    resp.raise_for_status()
    return resp.json()["embeddings"][0]


def search_fts(table, query: str, top_k: int = 5) -> list[str]:
    """BM25 full-text search, return chunk IDs."""
    try:
        results = table.search(query, query_type="fts").limit(top_k).to_list()
        return [r["id"] for r in results]
    except Exception:
        return []


def search_vector(table, query: str, top_k: int = 5) -> list[str]:
    """Vector search, return chunk IDs."""
    vec = embed_query(query)
    results = table.search(vec).limit(top_k).to_list()
    return [r["id"] for r in results]


def rrf_merge(lists: list[list[str]], k: int = 60) -> list[str]:
    """Reciprocal Rank Fusion merge of multiple ranked lists."""
    scores = {}
    for result_list in lists:
        for rank, chunk_id in enumerate(result_list):
            scores[chunk_id] = scores.get(chunk_id, 0) + 1.0 / (k + rank + 1)
    return sorted(scores, key=scores.get, reverse=True)


def search_hybrid(table, query: str, top_k: int = 5) -> list[str]:
    """Hybrid BM25 + vector with RRF merge."""
    fts_results = search_fts(table, query, top_k=10)
    vec_results = search_vector(table, query, top_k=10)
    merged = rrf_merge([fts_results, vec_results])
    return merged[:top_k]


def evaluate(table, search_fn, label: str, top_k: int = 5) -> dict:
    """Run all test cases against a search function."""
    recall_hits = 0
    p1_hits = 0
    rr_sum = 0.0
    total = len(TEST_CASES)
    failures = []

    for query, expected_ids in TEST_CASES:
        results = search_fn(table, query, top_k)
        # Recall@k: did any expected chunk appear in top-k?
        hit = any(eid in results for eid in expected_ids)
        if hit:
            recall_hits += 1
        else:
            failures.append((query, expected_ids, results))

        # P@1: is top result one of the expected?
        if results and results[0] in expected_ids:
            p1_hits += 1

        # MRR: reciprocal rank of first expected hit
        for rank, rid in enumerate(results):
            if rid in expected_ids:
                rr_sum += 1.0 / (rank + 1)
                break

    recall = recall_hits / total
    p1 = p1_hits / total
    mrr = rr_sum / total

    return {
        "label": label,
        "recall_at_k": recall,
        "p_at_1": p1,
        "mrr": mrr,
        "total": total,
        "recall_hits": recall_hits,
        "p1_hits": p1_hits,
        "failures": failures,
    }


def print_results(res: dict, verbose: bool = False) -> None:
    label = res["label"]
    r = res["recall_at_k"]
    p = res["p_at_1"]
    m = res["mrr"]
    total = res["total"]
    r_pass = "PASS" if r >= 0.90 else "FAIL"
    p_pass = "PASS" if p >= 0.70 else "FAIL"
    m_pass = "PASS" if m >= 0.70 else "FAIL"

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(f"  Recall@5:  {r:.1%} ({res['recall_hits']}/{total})  [{r_pass}]  (target >= 90%)")
    print(f"  P@1:       {p:.1%} ({res['p1_hits']}/{total})  [{p_pass}]  (target >= 70%)")
    print(f"  MRR:       {m:.3f}             [{m_pass}]  (target >= 0.70)")

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
    parser.add_argument("--full", action="store_true", help="Run full eval suite")
    parser.add_argument("--query", type=str, help="Debug a single query")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show failures")
    args = parser.parse_args()

    kb_dir = get_kb_dir()
    db = lancedb.connect(str(kb_dir / ".vectordb"))
    table = db.open_table(TABLE_NAME)

    if args.query:
        print(f"Query: {args.query}\n")
        print("FTS results:")
        for i, rid in enumerate(search_fts(table, args.query, 5)):
            print(f"  {i+1}. {rid}")
        print("\nVector results:")
        for i, rid in enumerate(search_vector(table, args.query, 5)):
            print(f"  {i+1}. {rid}")
        print("\nHybrid (RRF) results:")
        for i, rid in enumerate(search_hybrid(table, args.query, 5)):
            print(f"  {i+1}. {rid}")
        return

    # Run eval for all three search modes
    print("Running evaluation...")
    fts_res = evaluate(table, search_fts, "BM25 (FTS)")
    vec_res = evaluate(table, search_vector, "Vector")
    hybrid_res = evaluate(table, search_hybrid, "Hybrid (RRF)")

    verbose = args.verbose or args.full
    for res in [fts_res, vec_res, hybrid_res]:
        print_results(res, verbose=verbose)

    # Overall pass/fail
    print(f"\n{'='*60}")
    hybrid_pass = (hybrid_res["recall_at_k"] >= 0.90
                   and hybrid_res["p_at_1"] >= 0.70
                   and hybrid_res["mrr"] >= 0.70)
    if hybrid_pass:
        print("  OVERALL: PASS -- Hybrid search meets all thresholds")
    else:
        print("  OVERALL: FAIL -- Hybrid search below thresholds")
    print(f"{'='*60}")

    sys.exit(0 if hybrid_pass else 1)


if __name__ == "__main__":
    main()
