#!/bin/bash
# AI Knowledge Distillery -- One-time setup
# Run this from the repo root: ./setup.sh

set -e

echo "=== AI Knowledge Distillery Setup ==="
echo ""

# 1. Python venv + deps
echo "[1/3] Setting up Python environment..."
cd kb-mcp
# Find a Python >= 3.10
PYTHON=""
for candidate in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" &>/dev/null; then
        ver=$("$candidate" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        major=$(echo "$ver" | cut -d. -f1)
        minor=$(echo "$ver" | cut -d. -f2)
        if [ "$major" -ge 3 ] && [ "$minor" -ge 10 ]; then
            PYTHON="$candidate"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo "  ERROR: Python 3.10+ is required but not found."
    echo "  Install it via Homebrew:  brew install python@3.12"
    echo "  Then re-run this script."
    exit 1
fi

echo "  Using $PYTHON ($($PYTHON --version))"
echo "  Creating fresh venv..."
rm -rf .venv
"$PYTHON" -m venv .venv
.venv/bin/python3 -m pip install --upgrade pip -q
.venv/bin/pip install -q -r requirements.txt
echo "  Done."

# 2. Check Ollama
echo ""
echo "[2/3] Checking Ollama..."
if ! curl -s http://localhost:11434/api/tags &>/dev/null; then
    echo "  Ollama is not running. Please start it:"
    echo "    ollama serve"
    echo "  Then pull the embedding model:"
    echo "    ollama pull mxbai-embed-large"
    echo "  Then re-run this script."
    exit 1
fi

# Check if the embedding model is available
if ! curl -s http://localhost:11434/api/tags | grep -q "mxbai-embed-large"; then
    echo "  Pulling mxbai-embed-large model..."
    ollama pull mxbai-embed-large
fi
echo "  Ollama ready."

# 3. Build the index
echo ""
echo "[3/3] Building search index..."
.venv/bin/python indexer.py
cd ..

echo ""
echo "=== Setup complete ==="
echo ""
echo "You now have:"
echo "  - Python venv with all deps in kb-mcp/.venv"
echo "  - LanceDB vector index in Knowledge Distillery/.vectordb"
echo "  - MCP server configured in .claude/settings.json"
echo "  - All slash commands in .claude/commands/"
echo ""
echo "Open Claude Code in this directory and try:"
echo "  /kickoff [your task]"
echo "  /kb-status"
echo "  /audit [path]"
