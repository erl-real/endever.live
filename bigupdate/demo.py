"""
Seed data for DEMO mode.

Shape-identical to what Supabase returns, so the frontend cannot tell the
difference. Thumbnails come from YouTube off video_id — no local art.

Creators mirror the existing public.profiles columns we read:
id, username, display_name, avatar_url, tagline, bio, primary_role,
primary_genre, color.
"""

from datetime import datetime, timedelta, timezone

NOW = datetime.now(timezone.utc)


def _iso(dt):
    return dt.isoformat()


def _slugify(value):
    import re
    import unicodedata
    text = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return re.sub(r"-{2,}", "-", text) or "vod"


CREATORS = [
    {
        "id": "11111111-1111-4111-8111-111111111111",
        "username": "neverendever",
        "display_name": "Never End Ever",
        "avatar_url": None,
        "tagline": "Radio host. Selector. Occasional producer.",
        "bio": "Running the room since the first stream.",
        "primary_role": "Host",
        "primary_genre": "Electronic",
        "color": "#00f5d4",
    },
    {
        "id": "22222222-2222-4222-8222-222222222222",
        "username": "hammeta",
        "display_name": "Hammeta",
        "avatar_url": None,
        "tagline": "Producer. Drum design. Loud opinions on low end.",
        "bio": "Mix engineer. Drum samples. Terrace house apologist.",
        "primary_role": "Producer",
        "primary_genre": "Electronic",
        "color": "#ff1744",
    },
    {
        "id": "33333333-3333-4333-8333-333333333333",
        "username": "dither",
        "display_name": "Dither",
        "avatar_url": None,
        "tagline": "Vocalist. Topline writer. Breath take champion.",
        "bio": "Leads the Friday vocal session.",
        "primary_role": "Vocalist",
        "primary_genre": "R&B",
        "color": "#b026ff",
    },
    {
        "id": "44444444-4444-4444-8444-444444444444",
        "username": "themighty808",
        "display_name": "TheMighty808",
        "avatar_url": None,
        "tagline": "Drum machine archivist. 909 evangelist.",
        "bio": "Explains the machines.",
        "primary_role": "Producer",
        "primary_genre": "Hip Hop",
        "color": "#ff6a00",
    },
    {
        "id": "55555555-5555-4555-8555-555555555555",
        "username": "lorelodge",
        "display_name": "Lore Lodge",
        "avatar_url": None,
        "tagline": "Field recording. Location scouts.",
        "bio": "Goes outside for the sound.",
        "primary_role": "Sound Designer",
        "primary_genre": "Ambient",
        "color": "#46d369",
    },
    {
        "id": "66666666-6666-4666-8666-666666666666",
        "username": "unitedunderground",
        "display_name": "United Underground",
        "avatar_url": None,
        "tagline": "UUG — interviews with the underground.",
        "bio": "United Underground. Interviews, sessions and the occasional rant.",
        "primary_role": "Collective",
        "primary_genre": "Hip Hop",
        "color": "#e50914",
    },
]

POSTS = [
    # ---------------------------------------------------------------- events
    {
        "id": "a0000001-0000-4000-8000-000000000001",
        "creator": CREATORS[0]["id"],
        "kind": "event",
        "slug": "midnight-sessions-vol-4",
        "title": "Midnight Sessions Vol. 4",
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "provider": "youtube",
        "video_id": "dQw4w9WgXcQ",
        "thumb_url": "/demoart/15.png",
        "tags": ["collab", "live", "late night"],
        "genres": ["electronic", "ambient"],
        "musical_key": "F minor",
        "member_only": False,
        "starts_at": _iso(NOW + timedelta(days=2, hours=4)),
        "is_featured": True,
        "is_published": True,
        "created_at": _iso(NOW - timedelta(days=6)),
        "updated_at": _iso(NOW - timedelta(days=6)),
        "details": {
            "description": "Four hours, four artists, one shared signal chain. Bring a track you have been sitting on and play it into the room.",
            "host": "Never End Ever",
            "format": "live stream + multi-track",
            "credits": [
                {"role": "Host", "name": "Never End Ever"},
                {"role": "Signal", "name": "Hammeta"},
            ],
            "gear": ["Neumann U87", "SSL Bus Compressor", "Tape delay into the desk"],
        },
    },
    {
        "id": "a0000001-0000-4000-8000-000000000002",
        "creator": CREATORS[4]["id"],
        "kind": "event",
        "slug": "field-recording-walk-tokyo",
        "title": "Field Recording Walk — Tokyo",
        "url": "https://www.youtube.com/watch?v=9bZkp7q19f0",
        "provider": "youtube",
        "video_id": "9bZkp7q19f0",
        "thumb_url": "/demoart/16.png",
        "tags": ["field recording", "tokyo", "day trip"],
        "genres": ["ambient", "sound design"],
        "musical_key": None,
        "member_only": False,
        "starts_at": _iso(NOW + timedelta(days=11)),
        "is_featured": False,
        "is_published": True,
        "created_at": _iso(NOW - timedelta(days=3)),
        "updated_at": _iso(NOW - timedelta(days=3)),
        "details": {
            "description": "A full day walking the city with recorders. Subway platforms, arcade cabinets, the underside of the expressway.",
            "host": "Lore Lodge",
            "format": "in person + stream",
            "credits": [{"role": "Guide", "name": "Lore Lodge"}],
            "gear": ["Zoom F3", "Contact mics", "Deadcats that are not mine"],
        },
    },
    {
        "id": "a0000001-0000-4000-8000-000000000003",
        "creator": CREATORS[2]["id"],
        "kind": "event",
        "slug": "open-vocal-booth-fridays",
        "title": "Open Vocal Booth — Fridays",
        "url": "https://www.youtube.com/watch?v=kJQP7kiw5Fk",
        "provider": "youtube",
        "video_id": "kJQP7kiw5Fk",
        "thumb_url": "/demoart/17.png",
        "tags": ["vocals", "open session", "weekly"],
        "genres": ["rnb", "soul", "pop"],
        "musical_key": None,
        "member_only": False,
        "starts_at": _iso(NOW - timedelta(days=1)),
        "is_featured": False,
        "is_published": True,
        "created_at": _iso(NOW - timedelta(days=20)),
        "updated_at": _iso(NOW - timedelta(days=20)),
        "details": {
            "description": "Recurring Friday booth session. Sing something, we record it, you take the take home.",
            "host": "Dither",
            "format": "live stream",
            "credits": [{"role": "Vocalist", "name": "Dither"}],
            "gear": ["Neumann U67", "Avalon VT-737sp", "Two inch of tape"],
        },
    },
    # ------------------------------------------------------------- feedback
    {
        "id": "a0000002-0000-4000-8000-000000000001",
        "creator": CREATORS[1]["id"],
        "kind": "feedback",
        "slug": "reacts-basstest-v3",
        "title": "Reacts: Bass Test v3 (master)",
        "url": "https://www.youtube.com/watch?v=3JZ_D3ELwOQ",
        "provider": "youtube",
        "video_id": "3JZ_D3ELwOQ",
        "thumb_url": "/demoart/18.png",
        "tags": ["low end", "mastering", "reacts"],
        "genres": ["electronic", "bass"],
        "musical_key": "G minor",
        "member_only": False,
        "starts_at": _iso(NOW - timedelta(hours=6)),
        "is_featured": True,
        "is_published": True,
        "created_at": _iso(NOW - timedelta(hours=7)),
        "updated_at": _iso(NOW - timedelta(hours=7)),
        "details": {
            "description": "Master is up. The stream is live elsewhere — this is the VOD. React between 1 and 5 on how the low end sits.",
            "host": "Hammeta",
            "format": "VOD of a live react window",
            "criteria": ["low end weight", "kick vs bass separation", "monitors at low level"],
        },
    },
    {
        "id": "a0000002-0000-4000-8000-000000000002",
        "creator": CREATORS[3]["id"],
        "kind": "feedback",
        "slug": "reacts-808-scratch-pack",
        "title": "Reacts: 808 scratch pack",
        "url": "https://www.youtube.com/watch?v=ZbZSe6N_BXs",
        "provider": "youtube",
        "video_id": "ZbZSe6N_BXs",
        "thumb_url": "/demoart/19.png",
        "tags": ["808", "drums", "samples"],
        "genres": ["hip hop", "trap"],
        "musical_key": None,
        "member_only": False,
        "starts_at": _iso(NOW - timedelta(days=2)),
        "is_featured": False,
        "is_published": True,
        "created_at": _iso(NOW - timedelta(days=3)),
        "updated_at": _iso(NOW - timedelta(days=1)),
        "details": {
            "description": "Two hundred kicks, none tuned. The react window has closed — this is the VOD.",
            "host": "TheMighty808",
            "format": "VOD of a closed react window",
            "results": {"count": 148, "average": 3.6},
        },
    },
    {
        "id": "a0000002-0000-4000-8000-000000000003",
        "creator": CREATORS[2]["id"],
        "kind": "feedback",
        "slug": "reacts-take-two-dither",
        "title": "Reacts: Take Two (Dither)",
        "url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ",
        "provider": "youtube",
        "video_id": "fJ9rUzIMcZQ",
        "thumb_url": "/demoart/20.png",
        "tags": ["vocals", "takes", "reacts"],
        "genres": ["rnb", "soul"],
        "musical_key": None,
        "member_only": False,
        "starts_at": _iso(NOW + timedelta(hours=20)),
        "is_featured": False,
        "is_published": True,
        "created_at": _iso(NOW - timedelta(hours=2)),
        "updated_at": _iso(NOW - timedelta(hours=2)),
        "details": {
            "description": "Second pass on the booth take. The stream opens tomorrow evening — this is the VOD.",
            "host": "Dither",
            "format": "VOD of an upcoming react window",
        },
    },
    # -------------------------------------------------------------- lessons
    {
        "id": "a0000003-0000-4000-8000-000000000001",
        "creator": CREATORS[1]["id"],
        "kind": "lesson",
        "slug": "why-your-kick-disappears-on-small-speakers",
        "title": "Why your kick disappears on small speakers",
        "url": "https://www.youtube.com/watch?v=hTWKbfoikeg",
        "provider": "youtube",
        "video_id": "hTWKbfoikeg",
        "thumb_url": "/demoart/21.png",
        "tags": ["mixing", "low end", "translation"],
        "genres": ["electronic", "production"],
        "musical_key": "A minor",
        "member_only": False,
        "starts_at": None,
        "is_featured": True,
        "is_published": True,
        "created_at": _iso(NOW - timedelta(days=9)),
        "updated_at": _iso(NOW - timedelta(days=9)),
        "details": {
            "description": "You mix on monitors. They play down at forty hertz. Your phone does not. This is the twelve minutes that explain the whole problem.",
            "teacher": "Hammeta",
            "level": "intermediate",
            "duration": "12:04",
            "chapters": [
                {"t": 0, "label": "The actual failure mode"},
                {"t": 214, "label": "Harmonic content, not volume"},
                {"t": 486, "label": "Three fixes that translate"},
            ],
            "gear": ["Genelec 8341", "A7X", "iPhone SE speaker"],
        },
    },
    {
        "id": "a0000003-0000-4000-8000-000000000002",
        "creator": CREATORS[2]["id"],
        "kind": "lesson",
        "slug": "diaphragm-and-distance",
        "title": "Diaphragm and distance: the first ten minutes of any session",
        "url": "https://www.youtube.com/watch?v=d1o9x8LaGmg",
        "provider": "youtube",
        "video_id": "d1o9x8LaGmg",
        "thumb_url": "/demoart/22.png",
        "tags": ["vocals", "technique", "mic placement"],
        "genres": ["rnb", "soul", "pop"],
        "musical_key": None,
        "member_only": False,
        "starts_at": None,
        "is_featured": False,
        "is_published": True,
        "created_at": _iso(NOW - timedelta(days=15)),
        "updated_at": _iso(NOW - timedelta(days=15)),
        "details": {
            "description": "Before you touch a compressor, decide what the mic is. Large diaphragm versus dynamic, close versus two feet.",
            "teacher": "Dither",
            "level": "beginner",
            "duration": "09:41",
            "chapters": [
                {"t": 0, "label": "Pick the mic for the voice"},
                {"t": 180, "label": "Distance is tone"},
                {"t": 402, "label": "The pop filter lie"},
            ],
            "gear": ["Neumann U67", "SM7B", "RE20"],
        },
    },
    {
        "id": "a0000003-0000-4000-8000-000000000003",
        "creator": CREATORS[3]["id"],
        "kind": "lesson",
        "slug": "808-tuning-from-scratch",
        "title": "808 tuning from scratch, no plugin talk",
        "url": "https://www.youtube.com/watch?v=YQHsXMglC9A",
        "provider": "youtube",
        "video_id": "YQHsXMglC9A",
        "thumb_url": "/demoart/23.png",
        "tags": ["808", "synthesis", "drums"],
        "genres": ["hip hop", "trap"],
        "musical_key": "C minor",
        "member_only": False,
        "starts_at": None,
        "is_featured": False,
        "is_published": True,
        "created_at": _iso(NOW - timedelta(days=22)),
        "updated_at": _iso(NOW - timedelta(days=22)),
        "details": {
            "description": "Slide, decay, pitch bend. Build the kick from three oscillators and no preset.",
            "teacher": "TheMighty808",
            "level": "intermediate",
            "duration": "18:22",
            "chapters": [
                {"t": 0, "label": "Oscillators and the slide"},
                {"t": 520, "label": "Decay is the whole sound"},
                {"t": 940, "label": "Hearing the fundamental"},
            ],
            "gear": ["Ableton Live", "808 sub by Nullsoft"],
        },
    },
    {
        "id": "a0000003-0000-4000-8000-000000000004",
        "creator": CREATORS[4]["id"],
        "kind": "lesson",
        "slug": "recording-a-subway-platform",
        "title": "Recording a subway platform without sounding like a tourist",
        "url": "https://www.youtube.com/watch?v=lp-EO5I60KA",
        "provider": "youtube",
        "video_id": "lp-EO5I60KA",
        "thumb_url": "/demoart/24.png",
        "tags": ["field recording", "foley", "technique"],
        "genres": ["ambient", "sound design"],
        "musical_key": None,
        "member_only": False,
        "starts_at": None,
        "is_featured": False,
        "is_published": True,
        "created_at": _iso(NOW - timedelta(days=31)),
        "updated_at": _iso(NOW - timedelta(days=31)),
        "details": {
            "description": "Angle, distance, and patience. How to get a platform that sits under a track instead of drowning it.",
            "teacher": "Lore Lodge",
            "level": "beginner",
            "duration": "14:08",
            "chapters": [
                {"t": 0, "label": "Angle before gear"},
                {"t": 300, "label": "Get out of the middle"},
                {"t": 700, "label": "Always record it twice"},
            ],
            "gear": ["Zoom F6", "DPA 4060", "Boring answer: patience"],
        },
    },
]

# ---------------------------------------------------------------------------
# UUG interview playlist — hardcoded for now.
# (video_id, artist name) pairs scraped from the existing interview list.
# ---------------------------------------------------------------------------
_UUG = CREATORS[-1]["id"]

_INTERVIEWS = [
    ("8HRpGtQJuTE", "Kairose"),
    ("TBZy2HnGfgk", "Finesselations"), ("WulmEg_sNPY", "Darii"),
    ("HFJKJAyS5AM", "ICYWYTE"), ("ebGx_2J0yms", "WhynotSev"),
    ("xSiDspmNGIc", "Kayla G"), ("opEaSiScaVg", "Ynfrmthe19th"),
    ("7Wv6qFnvUyI", "Dolovon"), ("LHiJIZ5C5sw", "Ziahfyah"),
    ("wddoVa-rlfY", "7fiends"), ("TOQ7Bh0TnqI", "Yung Solarflare"),
    ("6R1xqGA68RQ", "BlueMonday"), ("mtMXpfp_u7M", "YvngBandoBoy"),
    ("zP63BrxhjTM", "DreamCHLD"), ("oXVKelXimII", "0kzvch"),
    ("4kou5nDxy_Q", "Mula Staxks feature"), ("aHlOPq89Es4", "Mula Staxks"),
    ("VgPRVwNU0OM", "5k Moncler"), ("ONA58MB-bWY", "7sirens"),
    ("OM1ehsWsVdc", "Yvng MC"), ("FYQb6uLNkt8", "Baretta"),
    ("EbWT8XoaTak", "Vice"), ("YTi29F9QPxA", "22bk"),
    ("7TGJDeZHECQ", "Jnhygs"), ("rXYUjGwkkzE", "Zodiax"),
    ("ng1GV40GqR4", "Dkgmac"), ("4t6tTY94KgE", "2burbo"),
    ("nQraORx71xo", "Sopperior"), ("rn-CMYkNUZQ", "Jesusluvsshadow"),
    ("0zONsMhOwnA", "Cali Brat"), ("u8gk8rUhRV8", "Bossa"),
    ("PoHsC7_PCSE", "Jei"), ("EXqHlK6pJYc", "imprinceway"),
    ("KQrGYsbvhuQ", "XellaRed"), ("vmYYscSDwkI", "Deyluvkirby"),
    ("SWUOz6N8H5M", "HVP3RSREVENGE"), ("Rfs2p9KbHTA", "V777RHEES"),
    ("ILXCyXmfKGY", "VXJOKING"), ("MDnpDhkKWK8", "Sharpboi"),
    ("wU14eahn9mA", "YNLNAIS"), ("YhDN2hRxd6M", "Killing Vultures"),
    ("STg0Xg5k_Mc", "Pingmas"), ("wiPl8EfuC0I", "2400miri"),
    ("Eso0ry6M4o4", "nyloit"), ("f2Exaade38w", "saskr"),
    ("ptwcESrZP6s", "gaptoothv4mp"), ("0WbeHHNBMyQ", "iluvdes"),
    ("Q-NCU7qFdUE", "yungfrendi"), ("o8OTiYbAUL4", "mattbartkus"),
    ("Z85Kz_SzLf4", "musicbymilla"), ("dQkOWyTAD8Y", "badfazzo"),
    ("eA_zIBO1Jvs", "Tenkay"), ("baWmojcBWkc", "brodiebased"),
    ("zshyM_s38ks", "Lumi x iluvern"), ("sT8QthhY-X8", "Subiibabii"),
    ("bYYcr0_57LE", "9lives"), ("EPtWQ0aLDbw", "Kenesukoh"),
    ("YWYOs_NFhvo", "HeyOzbee"), ("Wdw83D0DZDU", "A-D"),
    ("fUwZmg7JhY8", "SuperTrap"), ("GT4xYZAreog", "marluxiam"),
    ("63PsNl6S9eI", "iluvern"), ("SXB_SK3OVvg", "artieasylum"),
    ("7Ga4mY-nUCY", "SLXMPED"), ("latKdVUtB84", "ksinkasdeya"),
    ("9q91S3_yVtM", "Wokedes"), ("Fp8ZCYXote0", "Rsieh Raxan"),
    ("247ZPTLcGmM", "808toofly"), ("vA6QrrUWV30", "Hr"),
    ("cB6qzgzGMXo", "Kaydehn"), ("l8tRntZBsa8", "Kempachii"),
    ("NNMFpbhzbkE", "Predayed"),
]


def _build_interviews():
    rows = []
    for i, (vid, name) in enumerate(_INTERVIEWS):
        slug = _slugify(name) + f"-{i:03d}"
        rows.append({
            "id": f"b0000004-{i:04d}-4000-8000-000000000000",
            "creator": _UUG,
            "kind": "interviews",
            "slug": slug,
            "title": f"EndEver Interview — {name}" if name == "Kairose" else f"UUG Interview — {name}",
            "url": f"https://www.youtube.com/watch?v={vid}",
            "provider": "youtube",
            "video_id": vid,
            "thumb_url": None,
            "tags": ["interview", "endever"] if name == "Kairose" else ["interview", "uug"],
            "genres": ["hip hop"],
            "musical_key": None,
            "member_only": False,
            "starts_at": None,
            "is_featured": False,
            "is_published": True,
            "created_at": _iso(NOW - timedelta(days=60 - i)),
            "updated_at": _iso(NOW - timedelta(days=60 - i)),
            "details": {
                "description": f"United Underground sits down with {name}.",
                "interviewee": name,
                "series": "EndEver Interviews",
            },
        })
    return rows


POSTS = POSTS + _build_interviews()


# ---------------------------------------------------------------------------
# query helpers — mirror the shapes api.py expects back
# ---------------------------------------------------------------------------

def _creator_by_id(creator_id):
    for c in CREATORS:
        if c["id"] == creator_id:
            return c
    return {"id": creator_id, "username": "unknown", "display_name": "Unknown",
            "avatar_url": None, "tagline": "", "bio": "", "primary_role": "",
            "primary_genre": "", "color": None}


def gate(row, is_member):
    """Strip playback fields from a member-only vod for a non-member."""
    row = dict(row or {})
    row.setdefault("tags", [])
    row.setdefault("genres", [])
    row.setdefault("details", {})
    if not row.get("thumb_url") and row.get("video_id"):
        row["thumb_url"] = f"https://i.ytimg.com/vi/{row['video_id']}/hqdefault.jpg"
    if row.get("member_only") and not is_member:
        for field in ("url", "video_id", "thumb_url"):
            row[field] = None
        row["locked"] = True
    else:
        row["locked"] = False
    return row


def list_posts(kind=None, tag=None, genre=None, creator=None, q=None, limit=24, offset=0):
    rows = [dict(p) for p in POSTS]
    if kind:
        rows = [r for r in rows if r["kind"] == kind]
    if tag:
        rows = [r for r in rows if tag in r["tags"]]
    if genre:
        rows = [r for r in rows if genre in r["genres"]]
    if creator:
        rows = [r for r in rows if r["creator"] == creator]
    if q:
        needle = q.lower()
        rows = [r for r in rows if needle in r["title"].lower()
                or any(needle in t.lower() for t in r["tags"])
                or any(needle in g.lower() for g in r["genres"])
                or needle in (r["details"].get("description") or "").lower()]
    if kind == "event":
        rows.sort(key=lambda r: r["starts_at"] or "")
    else:
        rows.sort(key=lambda r: r["created_at"], reverse=True)
    return [gate(r, False) for r in rows[offset:offset + limit]]


def get_post(slug):
    for p in POSTS:
        if p["slug"] == slug:
            return p
    return None


def post_detail(slug):
    post = get_post(slug)
    return {
        "post": gate(post, False),
        "creator": _creator_by_id(post["creator"]),
        "is_member": False,
    }


def facets():
    tags, genres = set(), set()
    for p in POSTS:
        tags.update(p["tags"])
        genres.update(p["genres"])
    return {"tags": sorted(tags), "genres": sorted(genres)}


def creators():
    return [dict(c) for c in CREATORS]


def creator_detail(username):
    for c in CREATORS:
        if c["username"] == username:
            posts = [p for p in POSTS if p["creator"] == c["id"]]
            posts.sort(key=lambda r: r["created_at"], reverse=True)
            return {"creator": c, "posts": [gate(p, False) for p in posts], "is_member": False}
    return None


def home():
    return {
        "hero": [p for p in POSTS if p.get("is_featured")],
        "rails": {
            "events": list_posts(kind="event", limit=12),
            "feedback": list_posts(kind="feedback", limit=12),
            "lessons": list_posts(kind="lesson", limit=12),
            "interviews": list_posts(kind="interviews", limit=12),
            "latest": list_posts(limit=12),
        },
        "creators": [dict(c) for c in CREATORS],
        "is_member": False,
    }
