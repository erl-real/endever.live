# EndEver Live — platform

A music-oriented platform for posting VODs. Events, feedback sessions and
lessons from producers, vocalists and other creators. YouTube-powered to
start; the streams themselves live elsewhere.

## Run it

```bash
cd platform
pip install -r requirements.txt
python api.py          # http://localhost:8000
```

With no Supabase credentials set it boots in **demo mode** and serves seed
data, so the frontend is viewable immediately. Demo mode is read-only.

## Connect Supabase

1. Copy `.env.example` to `.env` and fill in your project URL + keys.
2. Run the schema in the Supabase SQL editor (or `psql "$DATABASE_URL" -f schema.sql`).
3. Restart the API.

## The schema

Two new tables. Everything else (`profiles`, `auth.users`, …) already exists.

### `public.memberships`

The member gate. Presence in this table = member. There is no boolean on the
user to hack. Add `status` / `expires_at` later if you need subscription
semantics.

### `public.vods`

The one content table. Every VOD, every kind, one row.

Design rule, applied strictly:

> Anything you SEARCH, FILTER, SORT or JOIN on → its own bite-sized column.
> Anything else the creator wants to add → one `details` jsonb cell.

| Column | Why it's a column |
|---|---|
| `creator` | uuid of the posting user — joined for display |
| `kind` | event / feedback / lesson — filtered on the home page and in browse |
| `slug` | unique, user-chosen — the URL |
| `title` | searched |
| `url` | the VOD link |
| `video_id` | parsed from url — drives the embed and thumbnail |
| `tags`, `genres` | filtered in browse |
| `musical_key` | filtered |
| `member_only` | gates the embed for non-members |
| `starts_at` | sorted (events, upcoming first) |
| `is_featured` | drives the home hero |
| `is_published` | public vs draft |
| `created_at`, `updated_at` | sorted / displayed |

Everything else — description, bio, date posted, credits, gear, chapters,
links, anything custom — goes in `details` jsonb.

A generated `search` tsvector column makes the jsonb `description` full-text
searchable without promoting it to a real column.

## The member gate

A vod with `member_only = true` hides its `url` / `video_id` / `thumb_url`
from anyone not present in `memberships`. The API strips the fields rather
than relying on the frontend to hide them.

## Banned users

Vods by banned users (`profiles.is_banned`) are excluded from every public
listing and from the creator page.

## API

| Endpoint | Description |
|---|---|
| `GET /api/health` | mode + time |
| `GET /api/facets` | every tag and genre in use |
| `GET /api/home` | hero + all rails + creators, one call |
| `GET /api/posts` | list. Filters: `kind`, `tag`, `genre`, `q`, `creator`, `limit`, `offset` |
| `GET /api/posts/<slug>` | one vod + creator profile |
| `POST /api/posts` | create (auth required, custom slug) |
| `PATCH /api/posts/<slug>` | update own |
| `DELETE /api/posts/<slug>` | delete own |
| `GET /api/creators` | list from existing `profiles` |
| `GET /api/creators/<username>` | profile + their vods |

Reads use the service-role key. Writes build a user-scoped client from the
caller's bearer token, so Postgres RLS decides what they may touch.

## Creator whitelist

`_require_creator()` in `api.py` is the gate. It is currently open to every
signed-in user. When you add the whitelist table, check it there and return
403 if the user is not on it. Everything above and below that function is
already correct.

## Pages

| Page | File |
|---|---|
| Home | `web/index.html` |
| Browse / search | `web/browse.html` |
| Single VOD | `web/postvod.html` |
| Post a VOD | `web/submit.html` |
| Creator profile | `web/creator.html` |

Shared assets: `web/assets/tokens.css` (design tokens), `web/assets/app.css`
(components), `web/assets/api.js` (API client), `web/assets/ui.js` (rendering).
