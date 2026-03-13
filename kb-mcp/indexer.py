"""
Embeds KB chunks via Ollama mxbai-embed-large and stores in LanceDB.
Creates FTS index for BM25 search. Supports incremental re-indexing.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

import httpx
import lancedb
import pyarrow as pa

from chunker import TOPIC_FILES, chunk_all, chunk_file

OLLAMA_URL = "http://localhost:11434/api/embed"
EMBED_MODEL = "mxbai-embed-large"
EMBED_DIMS = 1024
BATCH_SIZE = 10
TABLE_NAME = "kb_chunks"


def get_kb_dir(override: str | None = None) -> Path:
    if override:
        return Path(override)
    return Path(__file__).parent.parent / "Knowledge Distillery"


def get_db_path(kb_dir: Path) -> Path:
    return kb_dir / ".vectordb"


def get_meta_path(kb_dir: Path) -> Path:
    return kb_dir / "_index_meta.json"


def file_hash(filepath: Path) -> str:
    return hashlib.sha256(filepath.read_bytes()).hexdigest()[:16]


MAX_CHUNK_CHARS = 2_000  # ~512 tokens max for mxbai-embed-large; full text still stored in DB


def embed_one(text: str) -> list[float]:
    """Embed a single text via Ollama. Retries with shorter text if context exceeded."""
    limit = MAX_CHUNK_CHARS
    while limit >= 200:
        truncated = text[:limit] if len(text) > limit else text
        resp = httpx.post(
            OLLAMA_URL,
            json={"model": EMBED_MODEL, "input": truncated},
            timeout=120.0,
        )
        if resp.status_code == 200:
            return resp.json()["embeddings"][0]
        if resp.status_code == 400 and "context length" in resp.text:
            limit = int(limit * 0.7)  # reduce by 30% and retry
            continue
        resp.raise_for_status()
    raise RuntimeError(f"Cannot embed text even at {limit} chars")


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """Add 'vector' field to each chunk via sequential embedding."""
    total = len(chunks)
    for i, chunk in enumerate(chunks):
        chunk["vector"] = embed_one(chunk["text"])
        if (i + 1) % 20 == 0 or i + 1 == total:
            print(f"  Embedded {i + 1}/{total} chunks")
    return chunks


def build_index(kb_dir: Path, chunks: list[dict]) -> None:
    """Create or overwrite the LanceDB table and FTS index."""
    db_path = get_db_path(kb_dir)
    db = lancedb.connect(str(db_path))

    # Drop existing table if present
    try:
        db.drop_table(TABLE_NAME)
    except Exception:
        pass

    if not chunks:
        print("No chunks to index.")
        return

    # Embed all chunks
    print(f"Embedding {len(chunks)} chunks...")
    chunks = embed_chunks(chunks)

    # Build table
    table = db.create_table(TABLE_NAME, data=chunks)
    print(f"Created table '{TABLE_NAME}' with {len(chunks)} rows")

    # Create FTS index on text column for BM25 search
    table.create_fts_index("text", replace=True)
    print("FTS index created on 'text' column")


def write_meta(kb_dir: Path) -> None:
    """Write _index_meta.json with file hashes for incremental reindex."""
    meta = {}
    for fname in TOPIC_FILES:
        fpath = kb_dir / fname
        if fpath.exists():
            meta[fname] = file_hash(fpath)
    get_meta_path(kb_dir).write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote _index_meta.json ({len(meta)} files)")


def read_meta(kb_dir: Path) -> dict:
    meta_path = get_meta_path(kb_dir)
    if meta_path.exists():
        return json.loads(meta_path.read_text(encoding="utf-8"))
    return {}


def full_index(kb_dir: Path) -> None:
    """Full re-index of all topic files."""
    start = time.time()
    chunks = chunk_all(kb_dir)
    print(f"Chunked {len(chunks)} sections from {len(TOPIC_FILES)} files")
    build_index(kb_dir, chunks)
    write_meta(kb_dir)
    elapsed = time.time() - start
    print(f"Full index complete in {elapsed:.1f}s")


def reindex_file(kb_dir: Path, filename: str) -> None:
    """Incrementally re-index a single file."""
    fpath = kb_dir / filename
    if not fpath.exists():
        print(f"File not found: {filename}")
        return

    db_path = get_db_path(kb_dir)
    db = lancedb.connect(str(db_path))

    try:
        table = db.open_table(TABLE_NAME)
    except Exception:
        print("No existing index found. Running full index instead.")
        full_index(kb_dir)
        return

    # Remove old chunks for this file
    table.delete(f'file = "{filename}"')

    # Chunk and embed the updated file
    new_chunks = chunk_file(fpath)
    if new_chunks:
        print(f"Re-indexing {filename}: {len(new_chunks)} chunks")
        new_chunks = embed_chunks(new_chunks)
        table.add(new_chunks)
        # Rebuild FTS index
        table.create_fts_index("text", replace=True)
        print(f"Updated FTS index")

    # Update meta
    meta = read_meta(kb_dir)
    meta[filename] = file_hash(fpath)
    get_meta_path(kb_dir).write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Re-index of {filename} complete")


def reindex_changed(kb_dir: Path) -> None:
    """Re-index only files whose hash has changed since last index."""
    old_meta = read_meta(kb_dir)
    changed = []
    for fname in TOPIC_FILES:
        fpath = kb_dir / fname
        if not fpath.exists():
            continue
        current_hash = file_hash(fpath)
        if old_meta.get(fname) != current_hash:
            changed.append(fname)

    if not changed:
        print("All files up to date. Nothing to re-index.")
        return

    print(f"Changed files: {', '.join(changed)}")
    for fname in changed:
        reindex_file(kb_dir, fname)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Index KB chunks into LanceDB")
    parser.add_argument("--kb-dir", help="Path to Knowledge Distillery directory")
    parser.add_argument("--file", help="Re-index a single file")
    parser.add_argument("--changed", action="store_true", help="Re-index only changed files")
    args = parser.parse_args()

    kb_dir = get_kb_dir(args.kb_dir)
    if args.file:
        reindex_file(kb_dir, args.file)
    elif args.changed:
        reindex_changed(kb_dir)
    else:
        full_index(kb_dir)
