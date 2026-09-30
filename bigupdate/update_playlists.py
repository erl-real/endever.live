"""
update_playlists.py

Fetches all video IDs from YouTube playlists and updates the ids arrays
in radio/playlists/index.html.

Usage:
    python update_playlists.py [--dry-run]

Requires: pip install yt-dlp
"""

import re
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("yt-dlp is required. Install with: pip install yt-dlp")
    sys.exit(1)


HERE = Path(__file__).resolve().parent
HTML_PATH = HERE / "index.html"

PLAYLIST_URLS = {
    "bass-test":      "PLwm3mn269PQg_5ltAWOXuH32eT3G96IuW",
    "lsd-radio":      "PLwm3mn269PQjYSp567_ls-nTJdemFggfd",
    "acid-drop":      "PLwm3mn269PQhm2Ml5nRuXwnXKrDGNl76U",
    "post-pop":       "PLwm3mn269PQgWjE_ZLbM1PRTIiuIIN0QC",
    "knock-out":      "PLwm3mn269PQiwvTXwnRxM-B2U09vwcTTG",
    "unsigned":       None,
    "backseat66":     "PLwm3mn269PQhSoLItIltGCyDdlePbPr3U",
    "hustle-nation":  "PLwm3mn269PQgNfB8Isk2_Px4w5ljFz06L",
    "hot-100":        None,
    "nevr":           None,
    "exe-obj":        "PLwm3mn269PQgFsGTF_l7210V8XUPFoeBR",
    "red":            "PLwm3mn269PQhgq34UB6vLE5rlz2u9V06f",
    "homesick":       "PLwm3mn269PQhCcqI8Hzul8GvGbHZD0_hV",
    "projects":       "PLLvvJwrcjWUg",
    "closing-time":   "PLdqTBzwxveq0",
    "dither":         "PLwm3mn269PQih_bzThGmEaBayLBaVO3Dg",
    "full-cds":       "PLwm3mn269PQisYFZrOhihhsprM2XtsFDN",
    "reload":         "PLwm3mn269PQimOh-ibjW-B_2_UvxwszJX",
    "the-end":        "PLwm3mn269PQh-dMYvYes9-aMUTJgQuzgu",
    "tomes":          "PLwm3mn269PQgOBvMgeHVny8oPFh_nDAsS",
}


def fetch_playlist_ids(list_id: str) -> list[str] | None:
    """Fetch all video IDs from a YouTube playlist using yt-dlp."""
    url = f"https://www.youtube.com/playlist?list={list_id}"
    print(f"  Fetching {list_id} ...", end=" ", flush=True)
    ydl_opts = {
        "extract_flat": True,
        "quiet": True,
        "no_warnings": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        entries = info.get("entries", [])
        ids = [e["id"] for e in entries if e.get("id")]
        print(f"{len(ids)} videos")
        return ids
    except Exception as e:
        print(f"\n  Error: {e}")
        return None


def format_ids_block(ids: list[str], indent: str = "      ") -> str:
    """Format video IDs into the JS array literal style: ~10 per line."""
    lines = []
    for i in range(0, len(ids), 10):
        chunk = ids[i : i + 10]
        lines.append(indent + ",".join(f'"{v}"' for v in chunk) + ",")
    return "\n".join(lines)


def replace_ids_in_html(html: str, pl_id: str, new_ids: list[str]) -> str:
    """Locate the playlist entry by id and replace its ids: [...] block."""
    id_pat = re.compile(r"id:\s*'" + re.escape(pl_id) + r"'")
    m = id_pat.search(html)
    if not m:
        print(f"  WARNING: playlist '{pl_id}' not found in HTML, skipping")
        return html

    ids_start = html.index("ids: [", m.end())
    bracket_start = html.index("[", ids_start)
    depth = 0
    i = bracket_start
    while i < len(html):
        if html[i] == "[":
            depth += 1
        elif html[i] == "]":
            depth -= 1
            if depth == 0:
                break
        i += 1

    if depth != 0:
        print(f"  WARNING: unbalanced brackets for '{pl_id}', skipping")
        return html

    ids_end = i + 1
    old_block = html[ids_start:ids_end]

    new_block = "ids: [\n" + format_ids_block(new_ids) + "\n    ]"
    return html[:ids_start] + new_block + html[ids_end:]


def main():
    dry_run = "--dry-run" in sys.argv

    print("=== EndEver Live — Playlist Updater ===")

    fetched: dict[str, list[str]] = {}
    for pl_id, list_id in PLAYLIST_URLS.items():
        if list_id:
            ids = fetch_playlist_ids(list_id)
            if ids is not None:
                fetched[pl_id] = ids
        else:
            print(f"  {pl_id}: no YouTube URL — keeping existing ids")

    print()
    for pl_id, ids in fetched.items():
        print(f"  {pl_id}: {len(ids)} videos")

    if dry_run:
        print("\nDry run — no files modified.")
        return

    html = HTML_PATH.read_text(encoding="utf-8")
    for pl_id, ids in fetched.items():
        html = replace_ids_in_html(html, pl_id, ids)

    HTML_PATH.write_text(html, encoding="utf-8")
    print(f"\nUpdated {HTML_PATH}")


if __name__ == "__main__":
    main()
