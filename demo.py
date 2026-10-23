"""
Seed data for DEMO mode.
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
    {"id": "11111111-1111-4111-8111-111111111111", "username": "neverendever", "display_name": "Never End Ever", "avatar_url": None, "tagline": "Radio host. Selector. Occasional producer.", "bio": "Running the room since the first stream.", "primary_role": "Host", "primary_genre": "Electronic", "color": "#00f5d4"},
    {"id": "22222222-2222-4222-8222-222222222222", "username": "hammeta", "display_name": "Hammeta", "avatar_url": None, "tagline": "Producer. Drum design. Loud opinions on low end.", "bio": "Mix engineer. Drum samples. Terrace house apologist.", "primary_role": "Producer", "primary_genre": "Electronic", "color": "#ff1744"},
    {"id": "66666666-6666-4666-8666-666666666666", "username": "drumeo", "display_name": "Drumeo", "avatar_url": None, "tagline": "Drum lessons from the world's best drummers.", "bio": "Drumeo - the biggest name in drum education.", "primary_role": "Educator", "primary_genre": "Rock", "color": "#c21807"},
    {"id": "77777777-7777-4777-8777-777777777777", "username": "thecharismaticvoice", "display_name": "The Charismatic Voice", "avatar_url": None, "tagline": "Vocal analysis and reaction videos.", "bio": "Elizabeth Zharoff - vocal coach and analyst.", "primary_role": "Vocal Coach", "primary_genre": "Vocal", "color": "#9c27b0"},
    {"id": "88888888-8888-4888-8888-888888888888", "username": "rickbeato", "display_name": "Rick Beato", "avatar_url": None, "tagline": "Music theory, interviews, and what makes songs great.", "bio": "Rick Beato - music producer, educator, and YouTuber.", "primary_role": "Educator", "primary_genre": "Rock", "color": "#e65100"},
    {"id": "99999999-9999-4999-8999-999999999999", "username": "synthet7", "display_name": "Synthet7", "avatar_url": None, "tagline": "Music production, synthesis, and sound design.", "bio": "Synthet7 - deep dives into music production.", "primary_role": "Producer", "primary_genre": "Electronic", "color": "#00bcd4"},
    {"id": "aa000000-0000-4a00-8a00-000000000001", "username": "martymusic", "display_name": "Marty Music", "avatar_url": None, "tagline": "Guitar lessons and music theory.", "bio": "Marty Music - guitar lessons.", "primary_role": "Educator", "primary_genre": "Rock", "color": "#4caf50"},
    {"id": "aa000000-0000-4a00-8a00-000000000002", "username": "pauldavids", "display_name": "Paul Davids", "avatar_url": None, "tagline": "Guitar lessons, music theory, and gear.", "bio": "Paul Davids - guitar educator.", "primary_role": "Educator", "primary_genre": "Rock", "color": "#2196f3"},
    {"id": "aa000000-0000-4a00-8a00-000000000003", "username": "producelikeapro", "display_name": "Produce Like A Pro", "avatar_url": None, "tagline": "Music production interviews and lessons.", "bio": "Produce Like A Pro - interviews and lessons.", "primary_role": "Educator", "primary_genre": "Production", "color": "#ff9800"},
    {"id": "aa000000-0000-4a00-8a00-000000000004", "username": "yousuckatproducing", "display_name": "You Suck At Producing", "avatar_url": None, "tagline": "Music production lessons with humor.", "bio": "You Suck At Producing - music production lessons.", "primary_role": "Educator", "primary_genre": "Electronic", "color": "#f44336"},
    {"id": "aa000000-0000-4a00-8a00-000000000005", "username": "inthemix", "display_name": "In The Mix", "avatar_url": None, "tagline": "Music production and mixing.", "bio": "In The Mix - music production, mixing, and mastering.", "primary_role": "Educator", "primary_genre": "Electronic", "color": "#9c27b0"},
    {"id": "aa000000-0000-4a00-8a00-000000000006", "username": "theneedledrop", "display_name": "The Needle Drop", "avatar_url": None, "tagline": "Music reviews and reactions.", "bio": "The Needle Drop - music reviews, reactions, and analysis.", "primary_role": "Reviewer", "primary_genre": "Various", "color": "#795548"},
    {"id": "aa000000-0000-4a00-8a00-000000000007", "username": "blakemclain", "display_name": "Blake McLain", "avatar_url": None, "tagline": "Music production feedback and reactions.", "bio": "Blake McLain - music production feedback and reactions.", "primary_role": "Educator", "primary_genre": "Production", "color": "#607d8b"},
    {"id": "aa000000-0000-4a00-8a00-000000000008", "username": "andrewhuang", "display_name": "Andrew Huang", "avatar_url": None, "tagline": "Music production experiments and lessons.", "bio": "Andrew Huang - music production, experiments, and lessons.", "primary_role": "Producer", "primary_genre": "Electronic", "color": "#e91e63"},
    {"id": "aa000000-0000-4a00-8a00-000000000009", "username": "emilyharpist", "display_name": "Emily Harpist", "avatar_url": None, "tagline": "Harp lessons and performances.", "bio": "Emily Harpist - harp lessons and performances.", "primary_role": "Educator", "primary_genre": "Classical", "color": "#3f51b5"},
    {"id": "aa000000-0000-4a00-8a00-000000000010", "username": "8bitmusictheory", "display_name": "8-bit Music Theory", "avatar_url": None, "tagline": "Music theory in video games.", "bio": "8-bit Music Theory - music theory analysis of video game music.", "primary_role": "Educator", "primary_genre": "Theory", "color": "#7c4dff"},
    {"id": "aa000000-0000-4a00-8a00-000000000011", "username": "12tone", "display_name": "12tone", "avatar_url": None, "tagline": "Music theory and analysis.", "bio": "12tone - music theory and analysis.", "primary_role": "Educator", "primary_genre": "Theory", "color": "#009688"},
    {"id": "aa000000-0000-4a00-8a00-000000000012", "username": "davidbennettpiano", "display_name": "David Bennett Piano", "avatar_url": None, "tagline": "Piano lessons and music theory.", "bio": "David Bennett Piano - piano lessons and music theory.", "primary_role": "Educator", "primary_genre": "Classical", "color": "#8bc34a"},
    {"id": "aa000000-0000-4a00-8a00-000000000013", "username": "marcrebillet", "display_name": "Marc Rebillet", "avatar_url": None, "tagline": "Live looping and improv sets.", "bio": "Marc Rebillet - live looping, improv, and sets.", "primary_role": "Performer", "primary_genre": "Electronic", "color": "#ff5722"},
    {"id": "aa000000-0000-4a00-8a00-000000000014", "username": "mrwobbles", "display_name": "Mr Wobbles", "avatar_url": None, "tagline": "Live sets and performances.", "bio": "Mr Wobbles - live sets and performances.", "primary_role": "Performer", "primary_genre": "Electronic", "color": "#673ab7"},
    {"id": "bb000000-0000-4b00-8b00-000000000001", "username": "flstudio", "display_name": "FL Studio", "avatar_url": None, "tagline": "Official FL Studio tutorials.", "bio": "FL Studio - official tutorials and guides.", "primary_role": "Educator", "primary_genre": "Electronic", "color": "#ff6600"},
]

POSTS = [
    {"id": "a0000003-0000-4000-8000-000000000005", "creator": CREATORS[2]["id"], "kind": "lesson", "slug": "drumeo-el-estepario-nin", "title": "El Estepario Siberiano Hears Nine Inch Nails For The First Time", "url": "https://www.youtube.com/watch?v=eb01q2oPSEM", "provider": "youtube", "video_id": "eb01q2oPSEM", "thumb_url": None, "tags": ["drums", "nine inch nails", "hearing songs"], "genres": ["rock", "industrial"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": True, "is_published": True, "created_at": _iso(NOW - timedelta(days=0)), "updated_at": _iso(NOW - timedelta(days=0)), "details": {"description": "El Estepario Siberiano hears Nine Inch Nails for the first time, live in the Drumeo studio.", "teacher": "Drumeo", "level": "intermediate", "duration": "15:39", "gear": ["Drum kit"]}},
    {"id": "a0000003-0000-4000-8000-000000000006", "creator": CREATORS[2]["id"], "kind": "lesson", "slug": "drumeo-aaron-gillespie-nin-challenge", "title": "Aaron Gillespie vs. The Nine Inch Nails Drum Challenge", "url": "https://www.youtube.com/watch?v=eVorXW7UjTY", "provider": "youtube", "video_id": "eVorXW7UjTY", "thumb_url": None, "tags": ["drums", "nine inch nails", "challenge"], "genres": ["rock", "industrial"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=2)), "updated_at": _iso(NOW - timedelta(days=2)), "details": {"description": "Aaron Gillespie takes on the Nine Inch Nails drum challenge in the Drumeo studio.", "teacher": "Drumeo", "level": "intermediate", "duration": "14:00", "gear": ["Drum kit"]}},
    {"id": "a0000003-0000-4000-8000-000000000007", "creator": CREATORS[2]["id"], "kind": "lesson", "slug": "drumeo-paul-mccartney-drums", "title": "Why Paul McCartney Doesn't Drum Like A Drummer", "url": "https://www.youtube.com/watch?v=Y7diIhSG6eA", "provider": "youtube", "video_id": "Y7diIhSG6eA", "thumb_url": None, "tags": ["drums", "paul mccartney", "technique"], "genres": ["rock", "pop"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=6)), "updated_at": _iso(NOW - timedelta(days=6)), "details": {"description": "Why Paul McCartney's drumming doesn't sound like a drummer's.", "teacher": "Drumeo", "level": "intermediate", "duration": "12:00", "gear": ["Drum kit"]}},
    {"id": "a0000002-0000-4000-8000-000000000004", "creator": CREATORS[3]["id"], "kind": "feedback", "slug": "tcv-tonic-if-you-could-only-see", "title": "I Did NOT See This Coming! First Time Hearing Tonic", "url": "https://www.youtube.com/watch?v=U2jY7_NYa5s", "provider": "youtube", "video_id": "U2jY7_NYa5s", "thumb_url": None, "tags": ["reacts", "vocals", "first time hearing"], "genres": ["rock", "vocal"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=3)), "updated_at": _iso(NOW - timedelta(days=3)), "details": {"description": "First time hearing Tonic - vocal analysis by The Charismatic Voice.", "host": "The Charismatic Voice", "format": "VOD of a react"}},
    {"id": "a0000002-0000-4000-8000-000000000005", "creator": CREATORS[3]["id"], "kind": "feedback", "slug": "tcv-house-of-rising-sun", "title": "Vocal ANALYSIS of House of the Rising Sun by The Animals", "url": "https://www.youtube.com/watch?v=9umt0NxeNmA", "provider": "youtube", "video_id": "9umt0NxeNmA", "thumb_url": None, "tags": ["reacts", "vocals", "analysis"], "genres": ["rock", "vocal"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=4)), "updated_at": _iso(NOW - timedelta(days=4)), "details": {"description": "Vocal analysis of House of the Rising Sun.", "host": "The Charismatic Voice", "format": "VOD of a react"}},
    {"id": "a0000002-0000-4000-8000-000000000006", "creator": CREATORS[3]["id"], "kind": "feedback", "slug": "tcv-paradise-city", "title": "First Time Digging Into Paradise City by Guns N' Roses", "url": "https://www.youtube.com/watch?v=rB2uLZxsmM0", "provider": "youtube", "video_id": "rB2uLZxsmM0", "thumb_url": None, "tags": ["reacts", "vocals", "first time hearing"], "genres": ["rock", "vocal"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=7)), "updated_at": _iso(NOW - timedelta(days=7)), "details": {"description": "First time hearing Guns N' Roses Paradise City.", "host": "The Charismatic Voice", "format": "VOD of a react"}},
    {"id": "a0000003-0000-4000-8000-000000000011", "creator": CREATORS[3]["id"], "kind": "lesson", "slug": "tcv-throat-camera", "title": "OPERATION: Throat Camera", "url": "https://www.youtube.com/watch?v=Ua8SuWNPrLE", "provider": "youtube", "video_id": "Ua8SuWNPrLE", "thumb_url": None, "tags": ["vocals", "throat camera", "technique"], "genres": ["rock", "vocal"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=10)), "updated_at": _iso(NOW - timedelta(days=10)), "details": {"description": "Throat camera footage of Will Ramos performing harsh vocals.", "teacher": "The Charismatic Voice", "level": "advanced", "duration": "15:00", "gear": []}},
    {"id": "a0000003-0000-4000-8000-000000000012", "creator": CREATORS[3]["id"], "kind": "lesson", "slug": "tcv-vocal-distortion", "title": "The Science Behind Vocal Distortion", "url": "https://www.youtube.com/watch?v=JkBV8GoPWXY", "provider": "youtube", "video_id": "JkBV8GoPWXY", "thumb_url": None, "tags": ["vocals", "distortion", "technique"], "genres": ["rock", "vocal"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=12)), "updated_at": _iso(NOW - timedelta(days=12)), "details": {"description": "The science behind vocal distortion.", "teacher": "The Charismatic Voice", "level": "advanced", "duration": "20:00", "gear": []}},
    {"id": "a0000003-0000-4000-8000-000000000013", "creator": CREATORS[3]["id"], "kind": "lesson", "slug": "tcv-straw-glissando", "title": "Straw Glissando (Vocal Exercises Series)", "url": "https://www.youtube.com/watch?v=ubh4p7Y2ZuE", "provider": "youtube", "video_id": "ubh4p7Y2ZuE", "thumb_url": None, "tags": ["vocals", "exercise", "technique"], "genres": ["vocal"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=14)), "updated_at": _iso(NOW - timedelta(days=14)), "details": {"description": "Straw glissando vocal exercise.", "teacher": "The Charismatic Voice", "level": "beginner", "duration": "10:00", "gear": []}},
    {"id": "a0000002-0000-4000-8000-000000000007", "creator": CREATORS[4]["id"], "kind": "feedback", "slug": "rick-beato-just-like-heaven", "title": "What Makes This Song Great? Just Like Heaven - The Cure", "url": "https://www.youtube.com/watch?v=LPNHwwXh3Ks", "provider": "youtube", "video_id": "LPNHwwXh3Ks", "thumb_url": None, "tags": ["reacts", "music theory", "song analysis"], "genres": ["rock", "pop"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=5)), "updated_at": _iso(NOW - timedelta(days=5)), "details": {"description": "What Makes This Song Great? - Just Like Heaven by The Cure.", "host": "Rick Beato", "format": "VOD of a song analysis"}},
    {"id": "a0000002-0000-4000-8000-000000000008", "creator": CREATORS[4]["id"], "kind": "feedback", "slug": "rick-beato-bohemian-rhapsody", "title": "What Makes This Song Great? Bohemian Rhapsody - QUEEN", "url": "https://www.youtube.com/watch?v=3Ym7X_wCsPQ", "provider": "youtube", "video_id": "3Ym7X_wCsPQ", "thumb_url": None, "tags": ["reacts", "music theory", "song analysis"], "genres": ["rock", "classic rock"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=8)), "updated_at": _iso(NOW - timedelta(days=8)), "details": {"description": "What Makes This Song Great? - Bohemian Rhapsody by QUEEN.", "host": "Rick Beato", "format": "VOD of a song analysis"}},
    {"id": "a0000002-0000-4000-8000-000000000009", "creator": CREATORS[4]["id"], "kind": "feedback", "slug": "rick-beato-black-pearl-jam", "title": "What Makes This Song Great? Black - Pearl Jam", "url": "https://www.youtube.com/watch?v=9k55l7LMA7w", "provider": "youtube", "video_id": "9k55l7LMA7w", "thumb_url": None, "tags": ["reacts", "music theory", "song analysis"], "genres": ["rock", "grunge"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=10)), "updated_at": _iso(NOW - timedelta(days=10)), "details": {"description": "What Makes This Song Great? - Black by Pearl Jam.", "host": "Rick Beato", "format": "VOD of a song analysis"}},
    {"id": "a0000002-0000-4000-8000-000000000010", "creator": CREATORS[4]["id"], "kind": "feedback", "slug": "rick-beato-master-of-puppets", "title": "What Makes This Song Great? Master of Puppets - Metallica", "url": "https://www.youtube.com/watch?v=5EOHKfoDyrI", "provider": "youtube", "video_id": "5EOHKfoDyrI", "thumb_url": None, "tags": ["reacts", "music theory", "song analysis"], "genres": ["metal", "rock"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=12)), "updated_at": _iso(NOW - timedelta(days=12)), "details": {"description": "What Makes This Song Great? - Master of Puppets by Metallica.", "host": "Rick Beato", "format": "VOD of a song analysis"}},
    {"id": "a0000003-0000-4000-8000-000000000016", "creator": CREATORS[5]["id"], "kind": "lesson", "slug": "synthet7-rhythm-everyone-knows", "title": "the rhythm everyone knows", "url": "https://www.youtube.com/watch?v=F6tz5TduutI", "provider": "youtube", "video_id": "F6tz5TduutI", "thumb_url": None, "tags": ["music production", "rhythm", "synthesis"], "genres": ["electronic", "production"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=2)), "updated_at": _iso(NOW - timedelta(days=2)), "details": {"description": "Deep dive into the rhythm everyone knows.", "teacher": "Synthet7", "level": "intermediate", "duration": "12:00", "gear": []}},
    {"id": "a0000003-0000-4000-8000-000000000017", "creator": CREATORS[5]["id"], "kind": "lesson", "slug": "synthet7-greatest-chord", "title": "the greatest chord to put between chords", "url": "https://www.youtube.com/watch?v=Z7yLSapKKg4", "provider": "youtube", "video_id": "Z7yLSapKKg4", "thumb_url": None, "tags": ["music theory", "chords", "harmony"], "genres": ["electronic", "production"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=4)), "updated_at": _iso(NOW - timedelta(days=4)), "details": {"description": "The greatest chord to put between chords.", "teacher": "Synthet7", "level": "intermediate", "duration": "10:00", "gear": []}},
    {"id": "a0000003-0000-4000-8000-000000000018", "creator": CREATORS[6]["id"], "kind": "lesson", "slug": "martymusic-crazy-train", "title": "Crazy Train Guitar Lesson - Ozzy Osbourne", "url": "https://www.youtube.com/watch?v=61YCfNHZuHE", "provider": "youtube", "video_id": "61YCfNHZuHE", "thumb_url": None, "tags": ["guitar", "lesson", "ozzy"], "genres": ["rock", "metal"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=1)), "updated_at": _iso(NOW - timedelta(days=1)), "details": {"description": "Crazy Train guitar lesson by Marty Music.", "teacher": "Marty Music", "level": "intermediate", "duration": "15:00", "gear": ["Guitar"]}},
    {"id": "a0000003-0000-4000-8000-000000000019", "creator": CREATORS[7]["id"], "kind": "lesson", "slug": "pauldavids-getting-good", "title": "My philosophy on GETTING GOOD at guitar", "url": "https://www.youtube.com/watch?v=0CumD2ipiRA", "provider": "youtube", "video_id": "0CumD2ipiRA", "thumb_url": None, "tags": ["guitar", "practice", "technique"], "genres": ["rock"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=2)), "updated_at": _iso(NOW - timedelta(days=2)), "details": {"description": "Paul Davids' philosophy on getting good at guitar.", "teacher": "Paul Davids", "level": "intermediate", "duration": "12:00", "gear": ["Guitar"]}},
    {"id": "a0000003-0000-4000-8000-000000000020", "creator": CREATORS[8]["id"], "kind": "lesson", "slug": "producelikeapro-saturation", "title": "5 Quick Saturation Mixing Tricks", "url": "https://www.youtube.com/watch?v=97e-0TxuOKI", "provider": "youtube", "video_id": "97e-0TxuOKI", "thumb_url": None, "tags": ["mixing", "saturation", "production"], "genres": ["production"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=3)), "updated_at": _iso(NOW - timedelta(days=3)), "details": {"description": "5 quick saturation mixing tricks by Produce Like A Pro.", "teacher": "Produce Like A Pro", "level": "intermediate", "duration": "10:00", "gear": []}},
    {"id": "a0000003-0000-4000-8000-000000000021", "creator": CREATORS[9]["id"], "kind": "lesson", "slug": "yousuckatproducing-roasting", "title": "Roasting tracks from my discord", "url": "https://www.youtube.com/watch?v=uls-hfqoqZA", "provider": "youtube", "video_id": "uls-hfqoqZA", "thumb_url": None, "tags": ["production", "feedback", "roasting"], "genres": ["electronic", "production"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=4)), "updated_at": _iso(NOW - timedelta(days=4)), "details": {"description": "Roasting tracks from discord.", "teacher": "You Suck At Producing", "level": "intermediate", "duration": "15:00", "gear": []}},
    {"id": "a0000003-0000-4000-8000-000000000022", "creator": CREATORS[10]["id"], "kind": "lesson", "slug": "inthemix-fixing-bad-advice", "title": "Fixing Bad Music Production and Mixing Advice EP.1", "url": "https://www.youtube.com/watch?v=KjG8QHo2KIM", "provider": "youtube", "video_id": "KjG8QHo2KIM", "thumb_url": None, "tags": ["mixing", "production", "advice"], "genres": ["electronic", "production"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=5)), "updated_at": _iso(NOW - timedelta(days=5)), "details": {"description": "Fixing bad music production and mixing advice.", "teacher": "In The Mix", "level": "intermediate", "duration": "18:00", "gear": []}},
    {"id": "a0000002-0000-4000-8000-000000000011", "creator": CREATORS[11]["id"], "kind": "feedback", "slug": "theneedledrop-bandcamp", "title": "IT CAME FROM BANDCAMP (JULY 2016)", "url": "https://www.youtube.com/watch?v=3QuLKmZB5lg", "provider": "youtube", "video_id": "3QuLKmZB5lg", "thumb_url": None, "tags": ["reacts", "music review", "bandcamp"], "genres": ["various"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=6)), "updated_at": _iso(NOW - timedelta(days=6)), "details": {"description": "Music review and reactions from The Needle Drop.", "host": "The Needle Drop", "format": "VOD of a review"}},
    {"id": "a0000002-0000-4000-8000-000000000012", "creator": CREATORS[12]["id"], "kind": "feedback", "slug": "blakemclain-noah-kahan", "title": "No one makes music like THIS anymore - Noah Kahan Reaction", "url": "https://www.youtube.com/watch?v=0Bp2groftRc", "provider": "youtube", "video_id": "0Bp2groftRc", "thumb_url": None, "tags": ["reacts", "analysis", "noah kahan"], "genres": ["folk", "pop"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=7)), "updated_at": _iso(NOW - timedelta(days=7)), "details": {"description": "Noah Kahan reaction and analysis by Blake McLain.", "host": "Blake McLain", "format": "VOD of a react"}},
    {"id": "a0000003-0000-4000-8000-000000000023", "creator": CREATORS[13]["id"], "kind": "lesson", "slug": "andrewhuang-song-generator", "title": "Song Generator: Slide Whistle, Rhodes, Ballad", "url": "https://www.youtube.com/watch?v=_oOo0ohJkJM", "provider": "youtube", "video_id": "_oOo0ohJkJM", "thumb_url": None, "tags": ["production", "experiment", "song generator"], "genres": ["electronic", "production"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=8)), "updated_at": _iso(NOW - timedelta(days=8)), "details": {"description": "Song generator experiment by Andrew Huang.", "teacher": "Andrew Huang", "level": "intermediate", "duration": "15:00", "gear": []}},
    {"id": "a0000003-0000-4000-8000-000000000024", "creator": CREATORS[15]["id"], "kind": "lesson", "slug": "8bit-wind-waker", "title": "Wind Waker's Boss Themes are the Best in the Series", "url": "https://www.youtube.com/watch?v=WTj9cL48a2A", "provider": "youtube", "video_id": "WTj9cL48a2A", "thumb_url": None, "tags": ["music theory", "video game", "zelda"], "genres": ["theory", "game music"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=9)), "updated_at": _iso(NOW - timedelta(days=9)), "details": {"description": "Music theory analysis of Wind Waker's boss themes.", "teacher": "8-bit Music Theory", "level": "intermediate", "duration": "20:00", "gear": []}},
    {"id": "a0000003-0000-4000-8000-000000000025", "creator": CREATORS[16]["id"], "kind": "lesson", "slug": "12tone-under-pressure", "title": "Understanding Under Pressure", "url": "https://www.youtube.com/watch?v=rhd-pMT4mSk", "provider": "youtube", "video_id": "rhd-pMT4mSk", "thumb_url": None, "tags": ["music theory", "analysis", "queen"], "genres": ["theory"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=10)), "updated_at": _iso(NOW - timedelta(days=10)), "details": {"description": "Music theory analysis of Under Pressure.", "teacher": "12tone", "level": "intermediate", "duration": "15:00", "gear": []}},
    {"id": "a0000003-0000-4000-8000-000000000026", "creator": CREATORS[17]["id"], "kind": "lesson", "slug": "davidbennett-pachelbel", "title": "21 Songs that use Pachelbel's Canon chord progression", "url": "https://www.youtube.com/watch?v=_PC6jwoHyOk", "provider": "youtube", "video_id": "_PC6jwoHyOk", "thumb_url": None, "tags": ["music theory", "piano", "chords"], "genres": ["classical", "theory"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=11)), "updated_at": _iso(NOW - timedelta(days=11)), "details": {"description": "21 songs that use Pachelbel's Canon chord progression.", "teacher": "David Bennett Piano", "level": "intermediate", "duration": "20:00", "gear": []}},
    {"id": "b0000004-0000-4000-8000-000000000000", "creator": CREATORS[0]["id"], "kind": "interviews", "slug": "kairose-000", "title": "EndEver Interview - Kairose", "url": "https://www.youtube.com/watch?v=8HRpGtQJuTE", "provider": "youtube", "video_id": "8HRpGtQJuTE", "thumb_url": None, "tags": ["interview", "endever"], "genres": ["hip hop"], "musical_key": None, "member_only": False, "starts_at": None, "is_featured": False, "is_published": True, "created_at": _iso(NOW - timedelta(days=60)), "updated_at": _iso(NOW - timedelta(days=60)), "details": {"description": "EndEver sits down with Kairose.", "interviewee": "Kairose", "series": "EndEver Interviews"}},
]

POSTS.append({
    "id": "a0000005-0000-4000-8000-000000000001",
    "creator": CREATORS[18]["id"],
    "kind": "set",
    "slug": "marc-rebillet-dallas-highlights",
    "title": "STREAM HIGHLIGHTS: LAST SHOW IN DALLAS",
    "url": "https://www.youtube.com/watch?v=MOQp8TNiOF8",
    "provider": "youtube",
    "video_id": "MOQp8TNiOF8",
    "thumb_url": None,
    "tags": ["set", "live", "improv"],
    "genres": ["electronic", "funk"],
    "musical_key": None,
    "member_only": False,
    "starts_at": None,
    "is_featured": False,
    "is_published": True,
    "created_at": _iso(NOW - timedelta(days=5)),
    "updated_at": _iso(NOW - timedelta(days=5)),
    "details": {"description": "Marc Rebillet live set highlights from the last show in Dallas.", "host": "Marc Rebillet", "format": "live set"},
})

POSTS.append({
    "id": "a0000005-0000-4000-8000-000000000002",
    "creator": CREATORS[19]["id"],
    "kind": "set",
    "slug": "mr-wobbles-harmony-park",
    "title": "Mr. Wobbles LIVE SET @ Harmony Park Family Campout",
    "url": "https://www.youtube.com/watch?v=-uFDzd9GeDk",
    "provider": "youtube",
    "video_id": "-uFDzd9GeDk",
    "thumb_url": None,
    "tags": ["set", "live", "campout"],
    "genres": ["electronic", "reggae"],
    "musical_key": None,
    "member_only": False,
    "starts_at": None,
    "is_featured": False,
    "is_published": True,
    "created_at": _iso(NOW - timedelta(days=3)),
    "updated_at": _iso(NOW - timedelta(days=3)),
    "details": {"description": "Mr. Wobbles live set at Harmony Park Family Campout.", "host": "Mr Wobbles", "format": "live set"},
})

POSTS.append({
    "id": "a0000003-0000-4000-8000-000000000027",
    "creator": CREATORS[20]["id"],
    "kind": "lesson",
    "slug": "fl-studio-automation",
    "title": "Make it move with Automation - Learn FL Studio",
    "url": "https://www.youtube.com/watch?v=Su7Zvxib2kw",
    "provider": "youtube",
    "video_id": "Su7Zvxib2kw",
    "thumb_url": None,
    "tags": ["fl studio", "automation", "production"],
    "genres": ["electronic", "production"],
    "musical_key": None,
    "member_only": False,
    "starts_at": None,
    "is_featured": False,
    "is_published": True,
    "created_at": _iso(NOW - timedelta(days=1)),
    "updated_at": _iso(NOW - timedelta(days=1)),
    "details": {"description": "Learn FL Studio automation.", "teacher": "FL Studio", "level": "beginner", "duration": "10:00", "gear": ["FL Studio"]},
})

POSTS.append({
    "id": "a0000003-0000-4000-8000-000000000028",
    "creator": CREATORS[20]["id"],
    "kind": "lesson",
    "slug": "fl-studio-recording",
    "title": "The easiest way to record - Learn FL Studio",
    "url": "https://www.youtube.com/watch?v=qTh4COvhIs0",
    "provider": "youtube",
    "video_id": "qTh4COvhIs0",
    "thumb_url": None,
    "tags": ["fl studio", "recording", "production"],
    "genres": ["electronic", "production"],
    "musical_key": None,
    "member_only": False,
    "starts_at": None,
    "is_featured": False,
    "is_published": True,
    "created_at": _iso(NOW - timedelta(days=2)),
    "updated_at": _iso(NOW - timedelta(days=2)),
    "details": {"description": "Learn the easiest way to record in FL Studio.", "teacher": "FL Studio", "level": "beginner", "duration": "8:00", "gear": ["FL Studio"]},
})


def _creator_by_id(creator_id):
    for c in CREATORS:
        if c["id"] == creator_id:
            return c
    return {"id": creator_id, "username": "unknown", "display_name": "Unknown", "avatar_url": None, "tagline": "", "bio": "", "primary_role": "", "primary_genre": "", "color": None}


def gate(row, is_member):
    row = dict(row or {})
    row.setdefault("tags", [])
    row.setdefault("genres", [])
    row.setdefault("details", {})
    if not row.get("thumb_url") and row.get("video_id"):
        row["thumb_url"] = f"https://i.ytimg.com/vi/{row['video_id']}/maxresdefault.jpg"
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
        rows = [r for r in rows if needle in r["title"].lower() or any(needle in t.lower() for t in r["tags"]) or any(needle in g.lower() for g in r["genres"]) or needle in (r["details"].get("description") or "").lower()]
    if kind == "event":
        rows.sort(key=lambda r: r["starts_at"] or "")
    elif kind == "lesson":
        priority = {"tcv-throat-camera": 0, "tcv-vocal-distortion": 1}
        rows.sort(key=lambda r: (priority.get(r["slug"], 99), ))
        rest = [r for r in rows if r["slug"] not in priority]
        rest.sort(key=lambda r: r["created_at"], reverse=True)
        rows = [r for r in rows if r["slug"] in priority] + rest
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
    return {"post": gate(post, False), "creator": _creator_by_id(post["creator"]), "is_member": False}


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
            "sets": list_posts(kind="set", limit=12),
            "interviews": list_posts(kind="interviews", limit=12),
            "latest": list_posts(limit=12),
        },
        "creators": [dict(c) for c in CREATORS],
        "is_member": False,
    }


def youtube_feed(channel_id=None):
    return {"items": [], "channel": channel_id}

YOUTUBE_FEED = []
YOUTUBE_FEEDS = {}