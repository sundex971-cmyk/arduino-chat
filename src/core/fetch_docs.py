"""
fetch_docs.py — universal documentation downloader for the Arduino RAG bot.

Usage:
    python fetch_docs.py                        # download everything
    python fetch_docs.py --only arduino esp32   # download specific categories
    python fetch_docs.py --list                 # show available categories

Output structure:
    data/docs/
        arduino/      ← sources/arduino.py
        esp32/        ← sources/esp32.py
        components/   ← sources/components.py
        projects/     ← sources/projects.py (empty — written manually)
        connections/  ← sources/connections.py (empty — written manually)
        rules/        ← sources/rules.py
"""

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# Добавляем src/ в путь, чтобы находить tools.sources из core/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.sources import DocumentSource
from tools.sources import arduino, esp32, components, projects, connections, rules

# ------------------------------------------------------------------ #
# Configuration                                                        #
# ------------------------------------------------------------------ #

REQUEST_TIMEOUT = 20
HEADERS = {"User-Agent": "arduino-chat-doc-downloader/1.0"}

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "docs"

# Registry: category name → module with SOURCES list
CATEGORIES: dict[str, list[DocumentSource]] = {
    "arduino":     arduino.SOURCES,
    "esp32":       esp32.SOURCES,
    "components":  components.SOURCES,
    "projects":    projects.SOURCES,
    "connections": connections.SOURCES,
    "rules":       rules.SOURCES,
}

# ------------------------------------------------------------------ #
# HTTP helpers                                                         #
# ------------------------------------------------------------------ #

def _describe_http_error(error: HTTPError) -> str:
    message = f"HTTP {error.code}: {error.reason}"
    if error.code == 404:
        message += " (source file not found)"
    elif error.code in {403, 429}:
        retry_after = error.headers.get("Retry-After")
        remaining = error.headers.get("X-RateLimit-Remaining")
        message += " (rate limit or access restriction)"
        if retry_after:
            message += f"; retry after {retry_after}s"
        if remaining is not None:
            message += f"; remaining: {remaining}"
    return message


def fetch_text(url: str) -> str | None:
    request = Request(url, headers=HEADERS)
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
            encoding = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(encoding, errors="replace")
    except HTTPError as e:
        print(f"  [ERROR] {_describe_http_error(e)}")
    except URLError as e:
        print(f"  [ERROR] {e.reason}")
    except TimeoutError:
        print("  [ERROR] request timed out")
    return None

# ------------------------------------------------------------------ #
# Text processing                                                      #
# ------------------------------------------------------------------ #

def clean_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def format_content(source: DocumentSource, content: str) -> str:
    return "\n".join([
        f"Category:    {source.category}",
        f"Section:     {source.section}",
        f"Source page: {source.page_url}",
        f"Source file: {source.raw_url}",
        "",
        clean_text(content),
        "",
    ])

# ------------------------------------------------------------------ #
# File I/O                                                             #
# ------------------------------------------------------------------ #

def source_to_path(source: DocumentSource) -> Path:
    """Return the full save path for a source, including category sub-folder."""
    parsed = urlparse(source.page_url)
    slug = parsed.path.strip("/").replace("/", "_")
    filename = f"{source.section}__{slug}.txt"
    return DATA_DIR / source.category / filename


def save_text(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(content, encoding="utf-8")
        print(f"  [OK] {path.relative_to(DATA_DIR)}")
        return True
    except OSError as e:
        print(f"  [ERROR] Could not save {path}: {e}")
        return False

# ------------------------------------------------------------------ #
# Core download logic                                                  #
# ------------------------------------------------------------------ #

def download_sources(sources: list[DocumentSource]) -> tuple[int, int]:
    """Download all sources. Returns (saved_count, skipped_count)."""
    saved = skipped = 0
    for source in sources:
        print(f"[FETCH] {source.page_url}")
        content = fetch_text(source.raw_url)
        if content is None:
            skipped += 1
            continue
        formatted = format_content(source, content)
        path = source_to_path(source)
        if save_text(path, formatted):
            saved += 1
        else:
            skipped += 1
    return saved, skipped

# ------------------------------------------------------------------ #
# CLI                                                                  #
# ------------------------------------------------------------------ #

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Arduino RAG documentation into data/docs/<category>/",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="CATEGORY",
        help="Download only these categories (space-separated). "
             f"Available: {', '.join(CATEGORIES)}",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available categories and source counts, then exit.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list:
        print("Available categories:")
        for name, sources in CATEGORIES.items():
            ready = sum(1 for s in sources)
            print(f"  {name:<12} {ready} source(s)")
        return

    # Determine which categories to run
    if args.only:
        unknown = set(args.only) - CATEGORIES.keys()
        if unknown:
            print(f"[ERROR] Unknown categories: {', '.join(sorted(unknown))}")
            print(f"        Available: {', '.join(CATEGORIES)}")
            raise SystemExit(1)
        selected = {k: CATEGORIES[k] for k in args.only}
    else:
        selected = CATEGORIES

    total_saved = total_skipped = 0

    for category, sources in selected.items():
        if not sources:
            print(f"\n[SKIP] {category} — no sources defined yet")
            continue

        print(f"\n{'='*60}")
        print(f"  Category: {category} ({len(sources)} sources)")
        print(f"{'='*60}")

        saved, skipped = download_sources(sources)
        total_saved += saved
        total_skipped += skipped

    print(f"\n[DONE] Saved: {total_saved} | Skipped: {total_skipped}")


if __name__ == "__main__":
    main()