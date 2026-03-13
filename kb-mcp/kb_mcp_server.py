"""
Knowledge Distillery MCP Server.
Provides semantic search over the KB via FastMCP with 3 tools:
  - search_kb: Hybrid BM25 + vector search with RRF merge
  - list_topics: All topic files with their H2 headings
  - get_section: Direct retrieval by file + heading
"""

import os
import re
from pathlib import Path

import httpx
import lancedb
from fastmcp import FastMCP

OLLAMA_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "mxbai-embed-large"
TABLE_NAME = "kb_chunks"

# Synonym map for query expansion (KB-specific terms)
SYNONYMS = {
    "MCP": "Model Context Protocol MCP",
    "hooks": "hooks PreToolUse PostToolUse",
    "skills": "skills slash commands",
    "slash commands": "skills slash commands",
    "CLAUDE.md": "CLAUDE.md project instructions always-loaded",
    "context window": "context window token budget compaction",
    "worklogs": "worklogs session continuity WORKLOG.md",
    "Ralph loop": "Ralph loop autonomous coding",
    "vibe coding": "vibe coding vibe engineering",
    "subagents": "subagents sub-agents agent tool",
    "OpenClaw": "OpenClaw autonomous agent",
    "brain muscles": "brain muscles architecture pattern",
    "plausible echo": "plausible echo hallucination",
    "invariants": "invariants binary pass fail verification",
}

KB_DIR = Path(os.environ.get("KB_DIR", str(Path(__file__).parent.parent / "Knowledge Distillery")))

mcp = FastMCP("kb-retrieval", instructions=(
    "Knowledge Distillery retrieval server. Use search_kb for semantic queries, "
    "list_topics for an overview, get_section for exact section retrieval."
))


def get_table():
    db = lancedb.connect(str(KB_DIR / ".vectordb"))
    return db.open_table(TABLE_NAME)


def expand_query(query: str) -> str:
    """Expand query with KB-specific synonyms."""
    expanded = query
    for term, expansion in SYNONYMS.items():
        if term.lower() in query.lower():
            expanded = f"{expanded} {expansion}"
            break  # one expansion per query to avoid noise
    return expanded


def embed_query(query: str) -> list[float] | None:
    """Embed query via Ollama. Returns None if Ollama is down."""
    try:
        resp = httpx.post(
            OLLAMA_URL,
            json={"model": EMBED_MODEL, "input": query},
            timeout=30.0,
        )
        if resp.status_code == 200:
            return resp.json()["embeddings"][0]
    except Exception:
        pass
    return None


def search_fts(table, query: str, top_k: int) -> list[dict]:
    try:
        return table.search(query, query_type="fts").limit(top_k).to_list()
    except Exception:
        return []


def search_vector(table, query_vec: list[float], top_k: int) -> list[dict]:
    return table.search(query_vec).limit(top_k).to_list()


def rrf_merge(lists: list[list[dict]], k: int = 60) -> list[dict]:
    """Reciprocal Rank Fusion. Returns deduplicated results ordered by RRF score."""
    scores = {}
    items = {}
    for result_list in lists:
        for rank, item in enumerate(result_list):
            cid = item["id"]
            scores[cid] = scores.get(cid, 0) + 1.0 / (k + rank + 1)
            items[cid] = item
    ranked = sorted(scores, key=scores.get, reverse=True)
    return [items[cid] for cid in ranked]


def format_result(item: dict, rank: int, full: bool = True) -> str:
    """Format a search result for display."""
    heading_path = item["heading_path"]
    lines = f"(lines {item['line_start']}-{item['line_end']})"
    text = item["text"] if full else item["text"][:500] + ("..." if len(item["text"]) > 500 else "")
    return f"### Result {rank}: {heading_path} {lines}\n\n{text}"


@mcp.tool()
def search_kb(query: str, top_k: int = 5) -> str:
    """Search the Knowledge Distillery for relevant sections.

    Uses hybrid BM25 + vector search with Reciprocal Rank Fusion.
    Returns full text for top 3 results, preview for the rest.
    Falls back to BM25-only if Ollama embedding is unavailable.

    Args:
        query: Natural language search query
        top_k: Number of results to return (default 5, max 10)
    """
    top_k = min(max(top_k, 1), 10)
    table = get_table()
    expanded = expand_query(query)

    # BM25 search
    fts_results = search_fts(table, expanded, top_k=15)

    # Vector search (with Ollama-down fallback)
    query_vec = embed_query(expanded)
    if query_vec:
        vec_results = search_vector(table, query_vec, top_k=15)
        merged = rrf_merge([fts_results, vec_results])
        mode = "hybrid (BM25 + vector)"
    else:
        merged = fts_results
        mode = "BM25-only (Ollama unavailable)"

    if not merged:
        return f"No results found for: {query}"

    results = merged[:top_k]
    parts = [f"**{len(results)} results** via {mode} for: *{query}*\n"]
    for i, item in enumerate(results):
        full_text = i < 3  # full text for top 3, preview for rest
        parts.append(format_result(item, i + 1, full=full_text))

    return "\n\n---\n\n".join(parts)


@mcp.tool()
def list_topics() -> str:
    """List all Knowledge Distillery topic files with their section headings.

    Returns a structured overview of the 12 topic files and their H2 sections,
    useful for understanding what the KB covers before searching.
    """
    table = get_table()
    arrow_table = table.to_arrow().select(["file", "heading"])
    files = arrow_table.column("file").to_pylist()
    headings = arrow_table.column("heading").to_pylist()

    # Group by file
    topics = {}
    for f, h in zip(files, headings):
        if f not in topics:
            topics[f] = []
        if h != "Preamble":
            topics[f].append(h)

    parts = ["# Knowledge Distillery Topics\n"]
    for fname in sorted(topics):
        stem = fname.replace(".md", "")
        headings = topics[fname]
        parts.append(f"## {stem}\n")
        for h in headings:
            parts.append(f"- {h}")
        parts.append("")

    return "\n".join(parts)


@mcp.tool()
def get_section(file: str, heading: str) -> str:
    """Get a specific section from a KB topic file by file name and heading.

    Supports fuzzy matching if the exact heading isn't found.

    Args:
        file: Topic filename (e.g. 'agent-design.md' or 'agent-design')
        heading: Section heading to retrieve (e.g. 'Subagents in Claude Code')
    """
    if not file.endswith(".md"):
        file = f"{file}.md"

    table = get_table()
    # Exact match first
    results = table.search().where(
        f'file = "{file}" AND heading = "{heading}"'
    ).limit(1).to_list()

    if results:
        item = results[0]
        return f"## {item['heading']}\n*Source: {item['heading_path']}*\n\n{item['text']}"

    # Fuzzy match: search within file for closest heading
    file_chunks = table.search().where(f'file = "{file}"').limit(50).to_list()
    if not file_chunks:
        return f"File not found: {file}"

    heading_lower = heading.lower()
    best_match = None
    best_score = 0
    for chunk in file_chunks:
        h = chunk["heading"].lower()
        # Simple containment scoring
        if heading_lower in h or h in heading_lower:
            score = len(heading_lower) / max(len(h), 1)
            if score > best_score:
                best_score = score
                best_match = chunk

    if best_match:
        return (f"## {best_match['heading']} (fuzzy match)\n"
                f"*Source: {best_match['heading_path']}*\n\n{best_match['text']}")

    # Last resort: list available headings
    headings = [c["heading"] for c in file_chunks if c["heading"] != "Preamble"]
    return f"Heading '{heading}' not found in {file}. Available sections:\n" + "\n".join(f"- {h}" for h in headings)


if __name__ == "__main__":
    mcp.run()
