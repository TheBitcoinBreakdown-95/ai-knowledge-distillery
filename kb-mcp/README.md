# kb-mcp — Knowledge Distillery retrieval stack

Local semantic search over the 15 KB topic files: H2-level chunks embedded via
Ollama (`mxbai-embed-large`, 1024 dims) into LanceDB with a BM25 FTS index,
served to Claude Code as the `kb-retrieval` MCP server (tools: `search_kb`,
`list_topics`, `get_section`).

## Files

| File | Role |
|---|---|
| `chunker.py` | Splits topic files into H2 chunks; owns `TOPIC_FILES` |
| `indexer.py` | Embeds chunks, writes LanceDB at `../Knowledge-Distillery/.vectordb` + `_index_meta.json` (per-file content hashes) |
| `kb_mcp_server.py` | FastMCP server; hybrid BM25+vector search with RRF |
| `eval.py` | 30-case retrieval regression harness (imports the server's search pipeline) |
| `requirements.txt` | Direct deps (lancedb, fastmcp, httpx, pyarrow) |
| `requirements.lock.txt` | `pip freeze` of the known-working venv |

## Rebuild from scratch

All commands from this directory (`AI/AI-Notes/kb-mcp/`), Windows paths.

1. **Python venv** (Python 3.13):

   ```bash
   python -m venv .venv
   .venv/Scripts/python.exe -m pip install -r requirements.lock.txt
   ```

2. **Ollama + embedding model** (Ollama serves on `localhost:11434`):

   ```bash
   ollama pull mxbai-embed-large
   ```

3. **Full index build** (~470 chunks):

   ```bash
   .venv/Scripts/python.exe indexer.py
   ```

   Incremental variants: `indexer.py --changed` (hash-diff against
   `_index_meta.json`) or `indexer.py --file <topic>.md`.

4. **Eval gate**:

   ```bash
   .venv/Scripts/python.exe eval.py
   ```

   Exits 0 when hybrid search meets the ratified baseline thresholds
   (see eval.py header). Run after `/consolidate-kb` — consolidation
   renames H2 sections, which is what breaks fixtures.

5. **MCP wiring** — `.mcp.json` at the workspace root points the
   `kb-retrieval` server at this venv's python, `kb_mcp_server.py`, and sets
   `KB_DIR` to the Knowledge-Distillery directory. Absolute paths; update all
   three if the workspace moves.

## Auto-reindex path

Editing a topic file fires `.claude/hooks/reindex-kb.py` (PostToolUse), which
launches `indexer.py --file <name>` in the background and appends output to
`.claude/.tmp/reindex.log`. The hook derives its topic list from
`_index_meta.json`; a brand-new topic file is only hook-covered after its
first index run — the `/kb-status` freshness probe catches that gap.
`reindex_file` embeds replacement chunks BEFORE deleting old rows, so an
Ollama outage cannot erase a topic from search.
