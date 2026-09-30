# Membership linking — YouTube, Twitch, Patreon

A user with an active membership on YouTube, Twitch or Patreon gets full
membership on EndEver Live. This document covers the design, the database
changes, the API endpoints and the frontend flow.

---

## 1. The membership model

`public.memberships` is the single source of truth. Presence = member.

```sql
create table if not exists public.memberships (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  created_at timestamptz not null default now()
);
```

The API's `_is_member(user_id)` checks this table. If the user is in it, they
see `member_only` content. Linking a provider that has an active membership
inserts the row. Unlinking or a lapsed membership removes it.

---

## 2. Provider accounts

A new table stores the OAuth tokens and provider user IDs for each linked
account.

```sql
create table if not exists public.linked_accounts (
  id              uuid primary key default gen_random_uuid(),
  user_id         uuid not null references auth.users (id) on delete cascade,
  provider        text not null check (provider in ('youtube', 'twitch', 'patreon')),
  provider_user_id text not null,
  access_token    text not null,
  refresh_token   text,
  expires_at      timestamptz,
  created_at      timestamptz not null default now(),
  updated_at      timestamptz not null default now(),
  unique (user_id, provider)
);

create index if not exists linked_accounts_user_idx on public.linked_accounts (user_id);
```

- `access_token` / `refresh_token` are stored encrypted at rest (Supabase
  Vault or application-level encryption with a key in the environment).
- `provider_user_id` is the platform's own user ID — used to query the
  membership status.
- One row per `(user_id, provider)`. Linking the same provider twice updates
  the existing row.

---

## 3. How each provider is checked

### 3.1 YouTube

**Scope:** `https://www.googleapis.com/auth/youtube.channel-memberships.app`

This is a restricted scope. The user authenticates with Google and grants it.
The app then calls:

```
GET https://www.googleapis.com/youtube/v3/memberships
  ?part=snippet
  &filterByMemberChannelId={OUR_CHANNEL_ID}
  &maxResults=1
  &access_token={USER_TOKEN}
```

If the response contains an item, the user is an active member of our channel.
If `items` is empty, they are not.

**Notes:**
- The scope is restricted by Google and may require app verification.
- The user's own token is sufficient — no channel-owner token needed for this
  check.
- Token refresh uses Google's OAuth refresh flow.

### 3.2 Twitch

**Scope:** `channel:read:subscriptions` (broadcaster token)

The broadcaster authorises once. Then for any user:

```
GET https://api.twitch.tv/helix/subscriptions/user
  ?broadcaster_id={OUR_BROADCASTER_ID}
  &user_id={TWITCH_USER_ID}
  headers: Authorization: Bearer {BROADCASTER_TOKEN}
           Client-Id: {CLIENT_ID}
```

A 200 with data means the user is subscribed. A 404 means they are not.

**Alternative:** the user authenticates with Twitch using
`user:read:subscriptions`, and the app checks their own sub status with their
token. This avoids needing the broadcaster token but requires every user to
authorise Twitch.

**Notes:**
- The broadcaster token approach is simpler — one authorisation, then check
  any user by ID.
- The user's Twitch user ID is obtained from the Twitch OAuth userinfo
  endpoint during linking.
- Twitch tokens expire and must be refreshed.

### 3.3 Patreon

**Scope:** `campaigns.members` (campaign owner token)

The campaign owner authorises once. Then:

```
GET https://www.patreon.com/api/oauth2/v2/campaigns/{CAMPAIGN_ID}/members
  ?include=currently_entitled_tiers
  &fields[user]=full_name,email
  &fields[member]=patron_status,last_charge_date
  headers: Authorization: Bearer {OWNER_TOKEN}
```

A member with `patron_status: "active_patron"` and a non-empty
`currently_entitled_tiers` is an active member.

**Notes:**
- Patreon's API is the most complex of the three. The owner token is required.
- The response is paginated — iterate through all pages or use the
  `?filter[user_id]=` parameter if the Patreon user ID is known.
- Patreon user IDs are obtained from the OAuth userinfo endpoint during
  linking.

---

## 4. API endpoints

### `POST /api/link/{provider}`

Body: `{ "code": "{oauth_code}", "redirect_uri": "..." }`

1. Exchange the OAuth code for tokens.
2. Fetch the provider user ID from the provider's userinfo endpoint.
3. Upsert into `public.linked_accounts`.
4. Check membership status (see §3).
5. If active → upsert into `public.memberships`.
6. Return `{ "linked": true, "member": true }`.

### `DELETE /api/link/{provider}`

1. Delete the `linked_accounts` row.
2. Re-evaluate membership: if no other linked provider grants membership,
   delete from `public.memberships`.
3. Return `{ "linked": false, "member": false }`.

### `GET /api/membership`

Return the current membership status:

```json
{
  "is_member": true,
  "providers": [
    { "provider": "youtube", "linked": true, "active": true },
    { "provider": "twitch", "linked": false, "active": false }
  ]
}
```

### `POST /api/membership/sync`

Re-check all linked providers. Useful for a cron job or a manual refresh.
Updates `public.memberships` based on the combined result.

---

## 5. Membership evaluation logic

```python
def evaluate_membership(user_id):
    """Re-check all linked providers and update public.memberships."""
    accounts = get_linked_accounts(user_id)
    is_member = False

    for account in accounts:
        if account.provider == "youtube":
            is_member = is_member or check_youtube_membership(account)
        elif account.provider == "twitch":
            is_member = is_member or check_twitch_subscription(account)
        elif account.provider == "patreon":
            is_member = is_member or check_patreon_membership(account)

    if is_member:
        upsert_membership(user_id)
    else:
        delete_membership(user_id)

    return is_member
```

Called after linking, unlinking, and on a schedule (e.g. daily cron).

---

## 6. Frontend flow

### Link button

On the membership page, show a button per provider:

```
[ Link YouTube ]  [ Link Twitch ]  [ Link Patreon ]
```

Clicking starts the OAuth redirect flow for that provider. After the provider
redirects back, the frontend calls `POST /api/link/{provider}` with the code.

### Status display

```
Membership: Active via YouTube
[ Unlink YouTube ]
```

Or, if no membership:

```
Membership: Not active
Link your YouTube, Twitch or Patreon account to get access.
```

### OAuth redirect URIs

Each provider needs a redirect URI configured in its developer console:

| Provider | Redirect URI |
|---|---|
| YouTube | `https://endever.live/auth/youtube/callback` |
| Twitch | `https://endever.live/auth/twitch/callback` |
| Patreon | `https://endever.live/auth/patreon/callback` |

---

## 7. Security considerations

- **Tokens at rest:** encrypt `access_token` and `refresh_token` before
  storing. Use Supabase Vault or application-level encryption with a key in
  the environment variable `TOKEN_ENCRYPTION_KEY`.
- **Token in transit:** never log tokens. Never return them to the frontend.
- **CSRF:** use the OAuth `state` parameter to prevent CSRF on the redirect.
- **Scope minimisation:** request only the scopes needed for membership
  checking. Do not request broader scopes.
- **Rate limiting:** the membership check endpoints should be rate-limited
  to prevent abuse.
- **Patreon owner token:** this is a server-side secret. Never expose it to
  the frontend. Store it in the environment.

---

## 8. Environment variables

```
# Existing
SUPABASE_URL=
SUPABASE_SERVICE_KEY=

# YouTube
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_CHANNEL_ID=

# Twitch
TWITCH_CLIENT_ID=
TWITCH_CLIENT_SECRET=
TWITCH_BROADCASTER_ID=
TWITCH_BROADCASTER_TOKEN=

# Patreon
PATREON_CLIENT_ID=
PATREON_CLIENT_SECRET=
PATREON_CAMPAIGN_ID=
PATREON_OWNER_TOKEN=

# Encryption
TOKEN_ENCRYPTION_KEY=
```

---

## 9. Edge cases

| Case | Handling |
|---|---|
| User links YouTube, is a member, then lapses | Cron job removes them from `public.memberships` on the next sync. |
| User links two providers, one lapses | They keep membership as long as at least one provider is active. |
| User unlinks the only active provider | `evaluate_membership` removes them from `public.memberships`. |
| Provider API is down | Do not remove membership. Log the error and retry on the next sync. |
| User has a free Patreon tier | `currently_entitled_tiers` is empty → not a member. |
| YouTube scope is denied | The link fails gracefully. Show "YouTube membership check requires additional permissions." |
| Token refresh fails | Prompt the user to re-link the provider. |

---

## 10. Open questions

1. Should membership be checked on every page load, or only on a schedule?
   - On load is more accurate but adds latency. A daily cron is simpler.
2. Should we cache the membership status in `public.memberships` with a
   `verified_at` timestamp so the frontend can show "last checked"?
3. Patreon's API is the most complex — is it worth supporting initially, or
   start with YouTube and Twitch only?
4. Do we need a admin dashboard to manually grant/revoke membership?
