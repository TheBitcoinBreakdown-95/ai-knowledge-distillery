"""
Bookmark Parser -- Converts Bird CLI output or bookmarked_tweets.json to individual .md files.
Enriches with full tweet/article text via fxtwitter API (no auth required).

Usage:
    pip install requests

    # Bird CLI plaintext (default):
    bird bookmarks --all --plain | python parse_bookmarks.py --bird
    python parse_bookmarks.py --bird --input bird_output.txt

    # GraphQL JSON (legacy):
    python parse_bookmarks.py --json bookmarked_tweets.json

    Common flags: [--outdir PATH] [--skip-existing] [--no-enrich]

Defaults:
    --outdir  Twitter Bookmarks/ (relative to this script)
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
FXTWITTER_API = "https://api.fxtwitter.com"


def slugify(text, max_len=60):
    """Convert text to a filename-safe slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s]+', '-', text.strip())
    text = re.sub(r'-+', '-', text)
    return text[:max_len].rstrip('-')


def parse_date(datetime_str):
    """Parse datetime string to date components. Handles ISO and Twitter formats."""
    if not datetime_str:
        return None, None
    try:
        # ISO format from GraphQL interception
        dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d'), dt.strftime('%d %B %Y')
    except (ValueError, TypeError):
        pass
    try:
        # Twitter's created_at format: "Wed Oct 10 20:19:24 +0000 2018"
        dt = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %z %Y')
        return dt.strftime('%Y-%m-%d'), dt.strftime('%d %B %Y')
    except (ValueError, TypeError):
        return None, None


def extract_status_id(url):
    """Extract the status ID from a tweet URL."""
    match = re.search(r'/status/(\d+)', url)
    return match.group(1) if match else None


def enrich_via_fxtwitter(handle, status_id):
    """Fetch full tweet data from fxtwitter API. Handle can be empty -- fxtwitter
    resolves by status ID alone (use 'i' as placeholder handle)."""
    lookup_handle = handle if handle else "i"
    try:
        resp = requests.get(
            f"{FXTWITTER_API}/{lookup_handle}/status/{status_id}",
            timeout=15
        )
        if resp.status_code == 200:
            return resp.json().get("tweet", {})
        return None
    except Exception:
        return None


def build_filename(date_str, handle, text):
    """Build filename matching Bird CLI convention: YYYY-MM-DD-handle-title-slug.md"""
    title_slug = slugify(text[:80]) if text else "untitled"
    handle_clean = handle.lstrip('@').rstrip('_')
    if date_str:
        return f"{date_str}-{handle_clean}-{title_slug}.md"
    return f"unknown-date-{handle_clean}-{title_slug}.md"


def clean_text(text, expanded_urls=None, keep_tco=False):
    """Replace t.co links with expanded URLs where possible.
    If keep_tco=True (Bird CLI mode), preserve unresolved t.co links instead of stripping."""
    if expanded_urls:
        for exp_url in expanded_urls:
            if exp_url not in text:
                text = text.rstrip() + f"\n{exp_url}"
    if not keep_tco:
        # Only strip t.co links when we have expanded URLs to replace them (JSON mode)
        text = re.sub(r'https://t\.co/\w+', '', text).strip()
    return text


def format_short_tweet(tweet, enriched):
    """Format a short tweet/thread as markdown."""
    handle = tweet.get('handle', 'unknown')
    display_name = tweet.get('displayName', handle)
    url = tweet.get('url', '')
    date_str, date_display = parse_date(tweet.get('datetime'))
    likes = tweet.get('likes', '0')
    retweets = tweet.get('retweets', '0')
    expanded_urls = tweet.get('urls', [])

    text = tweet.get('text', '')
    if enriched:
        enriched_text = enriched.get('text', '')
        if enriched_text and len(enriched_text) > len(text):
            text = enriched_text
    keep_tco = not expanded_urls
    text = clean_text(text, expanded_urls, keep_tco=keep_tco)

    lines = [
        f"# @{handle} -- {date_str or 'unknown date'}",
        "",
        f"**Source:** {url}",
        f"**Likes:** {likes} | **RTs:** {retweets}",
        "",
        "---",
        "",
        text,
        "",
    ]
    return '\n'.join(lines)


def parse_bird_plaintext(text):
    """Parse Bird CLI --plain output into tweet dicts matching the JSON format."""
    separator = '──────────────────────────────────────────────────'
    blocks = text.split(separator)
    tweets = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.split('\n')
        # First line: @handle (Display Name):
        header_match = re.match(r'^@(\S+)\s*\((.+?)\):', lines[0])
        if not header_match:
            continue

        handle = header_match.group(1)
        display_name = header_match.group(2)

        date_line = None
        url_line = None
        body_lines = []

        for line in lines[1:]:
            if line.startswith('date: '):
                date_line = line[6:]
            elif line.startswith('url: '):
                url_line = line[5:]
            elif line.startswith('VIDEO: ') or line.startswith('IMAGE: '):
                continue  # skip media refs in body
            else:
                body_lines.append(line)

        text_body = '\n'.join(body_lines).strip()
        status_id = extract_status_id(url_line) if url_line else None

        tweets.append({
            'handle': handle,
            'displayName': display_name,
            'text': text_body,
            'datetime': date_line or '',
            'url': url_line or '',
            'urls': [],
            'likes': 0,
            'retweets': 0,
            'isArticle': len(text_body) > 500,
            '_status_id': status_id,
        })

    return tweets


def format_article(tweet, enriched):
    """Format a long article as markdown (Bird CLI article style)."""
    handle = tweet.get('handle', 'unknown')
    display_name = tweet.get('displayName', handle)
    url = tweet.get('url', '')
    expanded_urls = tweet.get('urls', [])

    text = tweet.get('text', '')
    if enriched:
        enriched_text = enriched.get('text', '')
        if enriched_text and len(enriched_text) > len(text):
            text = enriched_text
    keep_tco = not expanded_urls
    text = clean_text(text, expanded_urls, keep_tco=keep_tco)

    title = text.split('\n')[0][:120] if text else 'Untitled'

    lines = [
        f"> Source: X Article by @{handle}. Extracted via bookmark export.",
        "",
        f"@{handle} ({display_name}):",
        f"Article: {title}",
        "",
        text,
        "",
    ]
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="Convert bookmarks to .md files")
    parser.add_argument('--bird', action='store_true',
                        help='Parse Bird CLI --plain output (default mode)')
    parser.add_argument('--input', type=str,
                        help='Input file (Bird plaintext or JSON). Reads stdin if omitted with --bird')
    parser.add_argument('--json', type=str,
                        help='Path to bookmarked_tweets.json (legacy GraphQL mode)')
    parser.add_argument('--outdir', type=str, default=str(SCRIPT_DIR / 'Twitter Bookmarks'),
                        help='Output directory for .md files')
    parser.add_argument('--skip-existing', action='store_true',
                        help='Skip tweets whose .md file already exists')
    parser.add_argument('--no-enrich', action='store_true',
                        help='Skip fxtwitter enrichment (faster, less data)')
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Determine input mode
    if args.json:
        # Legacy JSON mode
        json_path = Path(args.json)
        if not json_path.exists():
            print(f"JSON file not found: {json_path}")
            sys.exit(1)
        with open(json_path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        if isinstance(raw, dict) and 'bookmarks' in raw:
            bookmarks = raw['bookmarks']
        elif isinstance(raw, list):
            bookmarks = raw
        else:
            print(f"Unexpected JSON structure. Expected array or {{ bookmarks: [...] }}")
            sys.exit(1)
        print(f"Loaded {len(bookmarks)} bookmarks from {json_path.name}")
    else:
        # Bird CLI plaintext mode (default)
        if args.input:
            input_path = Path(args.input)
            if not input_path.exists():
                print(f"Input file not found: {input_path}")
                sys.exit(1)
            with open(input_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
        else:
            raw_text = sys.stdin.read()
        bookmarks = parse_bird_plaintext(raw_text)
        print(f"Parsed {len(bookmarks)} bookmarks from Bird CLI output")
    print(f"Output: {outdir}")
    print(f"Enrich: {'off' if args.no_enrich else 'on (fxtwitter)'}")
    print("=" * 50)

    created = 0
    skipped = 0
    failed = 0
    existing_files = {f.name for f in outdir.glob('*.md')}

    for i, tweet in enumerate(bookmarks, 1):
        handle = tweet.get('handle', '') or ''
        display_name = tweet.get('displayName', '') or ''
        text = tweet.get('text', '')
        url = tweet.get('url', '')
        date_str, _ = parse_date(tweet.get('datetime'))
        status_id = tweet.get('_status_id') or extract_status_id(url)

        # Deduplicate: check if a file for this status_id already exists
        if status_id:
            already_exists = any(status_id in f for f in existing_files)
            if already_exists:
                skipped += 1
                continue

        # Enrich via fxtwitter (also resolves missing handle/displayName)
        enriched = None
        if not args.no_enrich and status_id:
            enriched = enrich_via_fxtwitter(handle, status_id)
            time.sleep(0.3)

        # Resolve handle from fxtwitter if GraphQL export didn't capture it
        if not handle and enriched:
            handle = enriched.get('author', {}).get('screen_name', '') or ''
            if not display_name:
                display_name = enriched.get('author', {}).get('name', '') or ''
            tweet['handle'] = handle
            tweet['displayName'] = display_name
            tweet['url'] = f"https://x.com/{handle}/status/{status_id}"

        if not handle:
            handle = 'unknown'

        filename = build_filename(date_str, handle, text)

        if args.skip_existing and filename in existing_files:
            skipped += 1
            continue

        print(f"  [{i}/{len(bookmarks)}] @{handle}: {text[:50]}...")

        try:
            is_article = tweet.get('isArticle', False)
            if is_article or len(text) > 500:
                content = format_article(tweet, enriched)
            else:
                content = format_short_tweet(tweet, enriched)

            filepath = outdir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            created += 1
            existing_files.add(filename)
        except Exception as e:
            print(f"    FAIL: {e}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"Created: {created} | Skipped: {skipped} | Failed: {failed}")
    print(f"Total files in {outdir.name}/: {len(list(outdir.glob('*.md')))}")


if __name__ == "__main__":
    main()
