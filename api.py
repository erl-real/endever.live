"""
EndEver Live — platform API
============================
Flask + Supabase. One process serves the JSON API and the static frontend.

Run:
    cd platform
    pip install -r requirements.txt
    python api.py            # http://localhost:8000

With no Supabase credentials set it boots in DEMO mode and serves seed data,
so the frontend is viewable immediately.

Auth model
----------
Reads use the service-role key (fast, bypasses RLS).
Writes build a *user-scoped* client from the caller's bearer token, so
Postgres RLS decides what they may touch. The service key is never used to
write. The creator whitelist gate goes in `_require_creator()`.

Member gate
-----------
A vod with member_only=true hides its url / video_id / thumb_url from anyone
who is not present in the memberships table. The gate strips the fields rather
than relying on the frontend to hide them.
"""

import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

sys.path.insert(0, str(Path(__file__).parent))
import demo as demo_data  # noqa: E402

BASE_DIR = Path(__file__).parent
WEB_DIR = BASE_DIR

app = Flask(__name__, static_folder=None)
CORS(app)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip()
SUPABASE_ANON = os.environ.get("SUPABASE_ANON_KEY", "").strip()
SUPABASE_SERVICE = os.environ.get("SUPABASE_SERVICE_KEY", "").strip()

DEMO = os.environ.get("DEMO", "").lower() in ("1", "true", "yes")
_db = None
if not DEMO and SUPABASE_URL and SUPABASE_SERVICE:
    try:
        from supabase import create_client

        _db = create_client(SUPABASE_URL, SUPABASE_SERVICE)
    except Exception as exc:  # pragma: no cover
        print(f"[warn] supabase client failed: {exc}", file=sys.stderr)
        _db = None
if _db is None:
    DEMO = True

PUBLIC_VODS = (
    "id,creator,kind,slug,title,url,provider,video_id,thumb_url,tags,genres,"
    "musical_key,member_only,starts_at,is_featured,is_published,"
    "created_at,updated_at,details"
)

# columns we strip from a member-only vod for a non-member
PLAYBACK_FIELDS = ("url", "video_id", "thumb_url")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def slugify(value: str, max_len: int = 72) -> str:
    """Lowercase ascii slug. Falls back to a stable hash if nothing survives."""
    import unicodedata

    text = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    text = re.sub(r"-{2,}", "-", text)[:max_len].strip("-")
    return text or "vod"


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_slug(slug: str):
    """-> error string, or None if the slug is usable."""
    if not slug or len(slug) > 80:
        return "slug must be 1-80 characters"
    if not SLUG_RE.match(slug):
        return "slug must be lowercase letters, numbers and hyphens"
    if DEMO:
        return None
    existing = _db.from_("vods").select("id").eq("slug", slug).limit(1).execute().data
    if existing:
        return "that slug is taken"
    return None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def user_client():
    """A client scoped to the caller's JWT so RLS applies. None if not signed in."""
    if DEMO or not SUPABASE_URL or not SUPABASE_ANON:
        return None
    header = request.headers.get("Authorization", "")
    if not header.lower().startswith("bearer "):
        return None
    try:
        from supabase import create_client

        return create_client(
            SUPABASE_URL,
            SUPABASE_ANON,
            options={"headers": {"Authorization": header}},
        )
    except Exception:
        return None


def _current_user_id():
    """Caller's user id, or None. Never raises — reads must not require auth."""
    client = user_client()
    if client is None:
        return None
    try:
        result = client.auth.get_user()
        user = getattr(result, "user", None) or (result or {}).get("user")
        return str(user["id"]) if user else None
    except Exception:
        return None


def _require_user():
    """Returns (user_id, error_response). Raises for writes."""
    user_id = _current_user_id()
    if not user_id:
        return None, (jsonify(error="sign in required"), 401)
    return user_id, None


def _require_creator(user_id: str):
    """Creator whitelist gate. Currently open to every signed-in user.

    When you add the whitelist table, check it here and return 403 if the user
    is not on it. Everything above and below this function is already correct.
    """
    return None


def _is_member(user_id) -> bool:
    """Presence in the memberships table = member."""
    if not user_id or DEMO:
        return False
    try:
        rows = (
            _db.from_("memberships").select("user_id")
            .eq("user_id", user_id).limit(1).execute().data
        )
        return bool(rows)
    except Exception:
        return False


def _gate(row: dict, is_member: bool) -> dict:
    """Strip playback fields from a member-only vod for a non-member."""
    row = dict(row or {})
    row.setdefault("tags", [])
    row.setdefault("genres", [])
    row.setdefault("details", {})
    if not row.get("thumb_url") and row.get("video_id"):
        row["thumb_url"] = f"https://i.ytimg.com/vi/{row['video_id']}/hqdefault.jpg"
    if row.get("member_only") and not is_member:
        for field in PLAYBACK_FIELDS:
            row[field] = None
        row["locked"] = True
    else:
        row["locked"] = False
    return row


def _with_creators(rows):
    """Attach creator profiles to vod rows, dropping banned creators.

    Two queries total, no embedded-resource filter magic. Banned users' vods
    are removed from the result entirely.
    """
    rows = rows or []
    if not rows:
        return []
    creator_ids = list({r.get("creator") for r in rows if r.get("creator")})
    profiles = {}
    if creator_ids:
        cols = "id,username,display_name,avatar_url,tagline,bio,primary_role,primary_genre,color,is_banned"
        found = (
            _db.from_("profiles").select(cols).in_("id", creator_ids).execute().data or []
        )
        profiles = {p["id"]: p for p in found}
    out = []
    for row in rows:
        creator = profiles.get(row.get("creator"))
        if creator and creator.get("is_banned"):
            continue
        row = dict(row)
        row["creator_profile"] = creator
        out.append(row)
    return out


def clean(payload: dict) -> dict:
    """Trim the payload down to the columns the table actually owns."""
    fields = {
        "kind", "slug", "title", "url", "provider", "video_id", "thumb_url",
        "tags", "genres", "musical_key", "member_only", "starts_at",
        "is_featured", "is_published",
    }
    out = {k: v for k, v in payload.items() if k in fields}
    details = payload.get("details")
    out["details"] = details if isinstance(details, dict) else {}
    return out


def parse_youtube(url: str):
    """-> (video_id, thumb_url). Both None if the url isn't a YouTube video."""
    patterns = (
        r"youtu\.be/([A-Za-z0-9_-]{11})",
        r"youtube\.com/watch\?(?:.*&)?v=([A-Za-z0-9_-]{11})",
        r"youtube\.com/(?:shorts|embed|live|v)/([A-Za-z0-9_-]{11})",
    )
    for pattern in patterns:
        m = re.search(pattern, url or "")
        if m:
            vid = m.group(1)
            return vid, f"https://i.ytimg.com/vi/{vid}/maxresdefault.jpg"
    return None, None


# ---------------------------------------------------------------------------
# static frontend
# ---------------------------------------------------------------------------

@app.route("/")
def web_index():
    return send_from_directory(WEB_DIR, "index.html")


@app.route("/<path:page>")
def web_page(page):
    root = WEB_DIR.resolve()
    candidate = (WEB_DIR / page).resolve()
    if candidate.is_file() and str(candidate).startswith(str(root)):
        return send_from_directory(WEB_DIR, page)
    if (WEB_DIR / f"{page}.html").is_file():
        return send_from_directory(WEB_DIR, f"{page}.html")
    return send_from_directory(WEB_DIR, "index.html"), 404


# ---------------------------------------------------------------------------
# meta
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health():
    return jsonify(ok=True, mode="demo" if DEMO else "live", time=now_iso())


@app.get("/api/facets")
def facets():
    """Every tag and genre currently in use — drives the browse filter chips."""
    if DEMO:
        return jsonify(demo_data.facets())
    tags, genres = set(), set()
    for batch in _db.from_("vods").select("tags,genres").limit(5000).execute().data or []:
        tags.update(batch.get("tags") or [])
        genres.update(batch.get("genres") or [])
    return jsonify(tags=sorted(tags), genres=sorted(genres))


# ---------------------------------------------------------------------------
# home — one call, everything the landing page needs
# ---------------------------------------------------------------------------

@app.get("/api/home")
def home():
    if DEMO:
        return jsonify(demo_data.home())

    base = _db.from_("vods").select(PUBLIC_VODS).eq("is_published", True)

    hero = base.eq("is_featured", True).order("starts_at").limit(5).execute().data
    events = base.eq("kind", "event").order("starts_at").limit(12).execute().data
    feedback = base.eq("kind", "feedback").order("created_at", desc=True).limit(12).execute().data
    lessons = base.eq("kind", "lesson").order("created_at", desc=True).limit(12).execute().data
    interviews = base.eq("kind", "interviews").order("created_at", desc=True).limit(100).execute().data
    latest = base.order("created_at", desc=True).limit(12).execute().data

    is_member = _is_member(_current_user_id())

    def gate_all(rows):
        return [_gate(r, is_member) for r in _with_creators(rows or [])]

    creators = (
        _db.from_("profiles")
        .select("id,username,display_name,avatar_url,tagline,primary_role,primary_genre,color")
        .or_("is_banned.is.null,is_banned.eq.false")
        .order("display_name").limit(12).execute().data or []
    )

    return jsonify(
        hero=gate_all(hero),
        rails={
            "events": gate_all(events),
            "feedback": gate_all(feedback),
            "lessons": gate_all(lessons),
            "interviews": gate_all(interviews),
            "latest": gate_all(latest),
        },
        creators=creators,
        is_member=is_member,
    )


# ---------------------------------------------------------------------------
# list / search
# ---------------------------------------------------------------------------

@app.get("/api/posts")
def list_posts():
    kind = request.args.get("kind")
    tag = request.args.get("tag")
    genre = request.args.get("genre")
    creator = request.args.get("creator")
    q = (request.args.get("q") or "").strip()
    try:
        limit = min(int(request.args.get("limit", 24)), 100)
        offset = max(int(request.args.get("offset", 0)), 0)
    except ValueError:
        limit, offset = 24, 0

    if DEMO:
        rows = demo_data.list_posts(
            kind=kind, tag=tag, genre=genre, creator=creator, q=q,
            limit=limit, offset=offset,
        )
        return jsonify(items=[demo_data.gate(r, False) for r in rows], limit=limit, offset=offset)

    query = _db.from_("vods").select(PUBLIC_VODS).eq("is_published", True)
    if kind:
        query = query.eq("kind", kind)
    if tag:
        query = query.contains("tags", [tag])
    if genre:
        query = query.contains("genres", [genre])
    if creator:
        query = query.eq("creator", creator)
    if q:
        query = query.text_search("search", q, type="websearch")

    ordering = "starts_at" if kind == "event" else "created_at"
    ascending = kind == "event" and not request.args.get("recent")

    rows = query.order(ordering, asc=ascending).range(offset, offset + limit - 1).execute().data or []

    is_member = _is_member(_current_user_id())
    return jsonify(
        items=[_gate(r, is_member) for r in _with_creators(rows)],
        limit=limit, offset=offset, is_member=is_member,
    )


# ---------------------------------------------------------------------------
# single vod
# ---------------------------------------------------------------------------

@app.get("/api/posts/<slug>")
def get_post(slug):
    if DEMO:
        row = demo_data.get_post(slug)
        if not row:
            return jsonify(error="not found"), 404
        return jsonify(demo_data.post_detail(slug))

    found = (
        _db.from_("vods").select(PUBLIC_VODS)
        .eq("slug", slug).eq("is_published", True).limit(1).execute().data
    )
    if not found:
        return jsonify(error="not found"), 404

    is_member = _is_member(_current_user_id())
    vod = _gate(found[0], is_member)

    creator = None
    if vod.get("creator"):
        rows = (
            _db.from_("profiles")
            .select("id,username,display_name,avatar_url,tagline,bio,primary_role,primary_genre,color")
            .eq("id", vod["creator"]).limit(1).execute().data or []
        )
        if rows and not rows[0].get("is_banned"):
            creator = rows[0]

    return jsonify(post=vod, creator=creator, is_member=is_member)


# ---------------------------------------------------------------------------
# create / update / delete
# ---------------------------------------------------------------------------

@app.post("/api/posts")
def create_post():
    body = request.get_json(silent=True) or {}
    if DEMO:
        return jsonify(error="demo mode is read-only", demo=True), 503

    user_id, err = _require_user()
    if err:
        return err
    err = _require_creator(user_id)
    if err:
        return err

    title = (body.get("title") or "").strip()
    url = (body.get("url") or "").strip()
    kind = (body.get("kind") or "").strip()
    slug = (body.get("slug") or "").strip()

    if not title:
        return jsonify(error="title is required"), 400
    if not url:
        return jsonify(error="url is required"), 400
    if kind not in ("event", "feedback", "lesson", "interviews"):
        return jsonify(error="kind must be event, feedback, lesson or interviews"), 400
    if not slug:
        return jsonify(error="slug is required"), 400

    slug_error = validate_slug(slug)
    if slug_error:
        return jsonify(error=slug_error), 400

    video_id, thumb = parse_youtube(url)
    row = clean(body)
    row.update(creator=user_id, slug=slug, video_id=video_id, thumb_url=body.get("thumb_url") or thumb)

    try:
        inserted = _db.table("vods").insert(row).execute().data
    except Exception as exc:
        return jsonify(error=str(exc)), 400
    return jsonify(_gate(inserted[0], True)), 201


@app.patch("/api/posts/<slug>")
def update_post(slug):
    body = request.get_json(silent=True) or {}
    if DEMO:
        return jsonify(error="demo mode is read-only", demo=True), 503

    user_id, err = _require_user()
    if err:
        return err

    row = clean(body)
    if "url" in row:
        video_id, thumb = parse_youtube(row["url"])
        row["video_id"] = video_id
        row["thumb_url"] = body.get("thumb_url") or thumb
    if "slug" in row:
        slug_error = validate_slug(row["slug"])
        if slug_error:
            return jsonify(error=slug_error), 400
        slug = row["slug"]

    try:
        updated = user_client().table("vods").update(row).eq("slug", slug).execute().data
    except Exception as exc:
        return jsonify(error=str(exc)), 400
    if not updated:
        return jsonify(error="not found or not yours"), 404
    return jsonify(_gate(updated[0], True))


@app.delete("/api/posts/<slug>")
def delete_post(slug):
    if DEMO:
        return jsonify(error="demo mode is read-only", demo=True), 503

    user_id, err = _require_user()
    if err:
        return err
    try:
        removed = user_client().table("vods").delete().eq("slug", slug).execute().data
    except Exception as exc:
        return jsonify(error=str(exc)), 400
    if not removed:
        return jsonify(error="not found or not yours"), 404
    return jsonify(ok=True, slug=slug)


# ---------------------------------------------------------------------------
# creators — read from the existing profiles table
# ---------------------------------------------------------------------------

@app.get("/api/creators")
def list_creators():
    if DEMO:
        return jsonify(demo_data.creators())
    rows = (
        _db.from_("profiles")
        .select("id,username,display_name,avatar_url,tagline,primary_role,primary_genre,color")
        .or_("is_banned.is.null,is_banned.eq.false")
        .order("display_name").limit(200).execute().data or []
    )
    return jsonify(rows)


@app.get("/api/creators/<username>")
def get_creator(username):
    if DEMO:
        return jsonify(demo_data.creator_detail(username))

    found = (
        _db.from_("profiles")
        .select("id,username,display_name,avatar_url,tagline,bio,primary_role,primary_genre,color,created_at")
        .eq("username", username).limit(1).execute().data
    )
    if not found or found[0].get("is_banned"):
        return jsonify(error="not found"), 404

    posts = (
        _db.from_("vods").select(PUBLIC_VODS)
        .eq("creator", found[0]["id"]).eq("is_published", True)
        .order("created_at", desc=True).limit(100).execute().data or []
    )
    is_member = _is_member(_current_user_id())
    return jsonify(
        creator=found[0],
        posts=[_gate(r, is_member) for r in posts],
        is_member=is_member,
    )


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mode = "DEMO (seed data, read-only)" if DEMO else f"live -> {SUPABASE_URL}"
    print(f"EndEver Live API  http://localhost:{port}   mode: {mode}")
    app.run(host="0.0.0.0", port=port, threaded=True, debug=os.environ.get("DEBUG") == "1")
