"""
Splits Knowledge Distillery topic files into H2-level chunks.
Each chunk = content between two ## headers (includes nested H3s, tables, code blocks).
Content before the first ## becomes a "Preamble" chunk.
"""

import hashlib
import re
from pathlib import Path

# The 12 synthesized topic files -- excludes meta-docs, sources/, README
TOPIC_FILES = [
    "agent-design.md",
    "autonomous-agents.md",
    "community-insights.md",
    "context-engineering.md",
    "failure-patterns.md",
    "memory-persistence.md",
    "project-setup.md",
    "prompt-engineering.md",
    "skills.md",
    "testing-verification.md",
    "tools-and-integrations.md",
    "workflow-patterns.md",
]


def slugify(text: str) -> str:
    """Convert heading text to a URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def chunk_file(filepath: Path) -> list[dict]:
    """Split a single markdown file into H2-level chunks."""
    lines = filepath.read_text(encoding="utf-8").splitlines()
    file_stem = filepath.stem
    chunks = []
    current_heading = "Preamble"
    current_lines = []
    current_start = 1  # 1-indexed

    for i, line in enumerate(lines, start=1):
        if re.match(r"^## ", line):
            # Flush previous chunk
            text = "\n".join(current_lines).strip()
            if text:
                chunks.append(_make_chunk(
                    file_stem, filepath.name, current_heading,
                    current_start, i - 1, text
                ))
            current_heading = line.lstrip("# ").strip()
            current_lines = [line]
            current_start = i
        else:
            current_lines.append(line)

    # Flush last chunk
    text = "\n".join(current_lines).strip()
    if text:
        chunks.append(_make_chunk(
            file_stem, filepath.name, current_heading,
            current_start, len(lines), text
        ))

    return chunks


def _make_chunk(file_stem: str, filename: str, heading: str,
                line_start: int, line_end: int, text: str) -> dict:
    slug = slugify(heading)
    chunk_id = f"{file_stem}__{slug}"
    return {
        "id": chunk_id,
        "file": filename,
        "heading": heading,
        "heading_path": f"{filename} > {heading}",
        "line_start": line_start,
        "line_end": line_end,
        "text": text,
        "hash": hashlib.sha256(text.encode("utf-8")).hexdigest()[:16],
    }


def chunk_all(kb_dir: Path) -> list[dict]:
    """Chunk all 12 topic files in the Knowledge Distillery."""
    all_chunks = []
    for fname in TOPIC_FILES:
        fpath = kb_dir / fname
        if fpath.exists():
            all_chunks.extend(chunk_file(fpath))
        else:
            print(f"WARNING: {fname} not found in {kb_dir}")
    return all_chunks


if __name__ == "__main__":
    import sys
    kb_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent / "Knowledge Distillery"
    chunks = chunk_all(kb_dir)
    print(f"Total chunks: {len(chunks)}")
    for c in chunks:
        print(f"  {c['id']}  ({c['line_start']}-{c['line_end']}, {len(c['text'])} chars)")
