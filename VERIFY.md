# Verification checklist — not started yet

We are **not** at the testing stage. This is the list to work through when we
are. Nothing here has been run.

## 1. Run the API

```bash
cd platform
python api.py          # http://localhost:8000
```

With no Supabase keys set it boots in **demo mode** (read-only). Confirm
`GET /api/health` returns `{"mode": "demo"}`.

## 2. Smoke-test endpoints

| Endpoint | Expect |
|---|---|
| `GET /api/health` | `{"ok": true, "mode": "demo", "time": ...}` |
| `GET /api/facets` | `{tags: [...], genres: [...]}` |
| `GET /api/home` | `hero` (3), `rails` (events/feedback/lessons/interviews/latest), `creators` (6) |
| `GET /api/posts` | 82 items |
| `GET /api/posts?kind=event` | 3 |
| `GET /api/posts?kind=feedback` | 3 |
| `GET /api/posts?kind=lesson` | 4 |
| `GET /api/posts?kind=interviews&tag=endever` | 1 (Kairose) |
| `GET /api/posts?kind=interviews&tag=uug` | 71 |
| `GET /api/posts?limit=6&offset=6` | paging works |
| `GET /api/posts/<slug>` | one post + creator |
| `POST /api/posts` | 503 `demo mode is read-only` |
| `PATCH /api/posts/<slug>` | 503 |
| `DELETE /api/posts/<slug>` | 503 |
| `GET /api/creators` | 6 |
| `GET /api/creators/unitedunderground` | profile + 72 vods |

## 3. Headless Chrome render check

Serve the static demo and load each page. Check for console errors on all of them.

| Page | File | Check |
|---|---|---|
| Home | `web/index.html` | hero rotates, 7 rows render, logo has red underline + glow, nav links plain |
| Browse | `web/browse.html` | search filters, kind chips, `?tag=uug` shows 71 |
| Creator | `web/creator.html` | avatar, tagline, their vods |
| VOD | `web/postvod.html?slug=...` | title, embed/thumb, tags |
| Submit | `web/submit.html` | form fields, auth gate |
| Playlist | `web/playlist.html` | standalone, logo links to `/` |

### Specific things to look at

- **Header seam** — no line under the nav at scroll top; white hairline appears only when scrolled.
- **Active underline** — one red line per active item, no second line under it, no black band.
- **Glow** — breathes 0.42 → 0.8 on an 8s loop, no flicker, no pop.
- **Rails** — 6 cards load, arrow appears only when the row overflows, scrolling pages a full row, more cards load on scroll.
- **Encoding** — no `â` mojibake anywhere in the UI.
- **Mobile (≤780px)** — nav scrolls horizontally, arrows hidden, cards 2-up.
- **Images** — non-interview cards show `demoart` art, interviews show YouTube thumbs.

## 4. Known open items (not verification, just pending)

- Footer links are all `href="#"` — waiting on real URLs.
- `playlist.html` art paths assume `art/` is deployed alongside.
- Member gate is written but deferred.
- Creator whitelist in `_require_creator()` is open to everyone.
- `data.js` must be regenerated whenever `demo.py` changes.
- `demoart` PNGs are 1400×1400 / 2–4.5 MB each — optimize when demo data is replaced.
