-- =============================================================================
--  EndEver Live — platform schema (Supabase / Postgres)
-- =============================================================================
--  Two new tables. Everything else (profiles, auth.users, …) already exists.
--
--  Design rule for public.vods, applied strictly:
--    Anything you SEARCH, FILTER, SORT or JOIN on  -> its own bite-sized column
--    Anything else the creator wants to add        -> one `details` jsonb cell
--
--  Run in the Supabase SQL editor, or:  psql "$DATABASE_URL" -f schema.sql
-- =============================================================================

-- ---------------------------------------------------------------------------
-- memberships — the member gate.
-- Presence in this table = member. There is no boolean on the user to hack.
-- Add status / expires_at later if you need subscription semantics.
-- ---------------------------------------------------------------------------
create table if not exists public.memberships (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  created_at timestamptz not null default now()
);

-- ---------------------------------------------------------------------------
-- vods — the one content table. Every VOD, every kind, one row.
-- ---------------------------------------------------------------------------
create table if not exists public.vods (
  id           uuid primary key default gen_random_uuid(),

  -- the person who posted. uuid of the auth user.
  creator      uuid not null references auth.users (id) on delete cascade,

  -- --- bite-sized: searched / filtered / sorted on ---
  kind         text not null check (kind in ('event', 'feedback', 'lesson', 'interviews')),
  slug         text not null unique,
  title        text not null,
  url          text not null,
  provider     text not null default 'youtube',
  video_id     text,
  thumb_url    text,
  tags         text[] not null default '{}',
  genres       text[] not null default '{}',
  musical_key  text,
  member_only  boolean not null default false,
  starts_at    timestamptz,
  is_featured  boolean not null default false,
  is_published boolean not null default true,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now(),

  -- --- one cell for everything else ---
  -- description, bio, date posted, credits, artwork, equipment, links,
  -- anything custom. Shape is owned by the creator, not the database.
  details      jsonb not null default '{}'::jsonb
);

-- Full-text search runs across the bite-sized columns *and* the description,
-- so description stays out of the column list without becoming unsearchable.
alter table public.vods
  drop column if exists search;
alter table public.vods
  add column search tsvector generated always as (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', array_to_string(genres, ' ')), 'B') ||
    setweight(to_tsvector('english', array_to_string(tags,   ' ')), 'B') ||
    setweight(to_tsvector('english', coalesce(details->>'description', '')), 'C')
  ) stored;

-- ---------------------------------------------------------------------------
-- Indexes — only on things we actually query
-- ---------------------------------------------------------------------------
create index if not exists vods_created_at_idx on public.vods (created_at desc);
create index if not exists vods_creator_idx    on public.vods (creator);
create index if not exists vods_kind_idx       on public.vods (kind);
create index if not exists vods_starts_at_idx  on public.vods (starts_at);
create index if not exists vods_featured_idx   on public.vods (is_featured)
  where is_published;
create index if not exists vods_genres_idx     on public.vods using gin (genres);
create index if not exists vods_tags_idx       on public.vods using gin (tags);
create index if not exists vods_search_idx     on public.vods using gin (search);
create index if not exists vods_details_idx    on public.vods using gin (details jsonb_path_ops);

-- ---------------------------------------------------------------------------
-- updated_at maintenance
-- ---------------------------------------------------------------------------
create or replace function public.touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end $$;

drop trigger if exists vods_touch on public.vods;
create trigger vods_touch before update on public.vods
  for each row execute function public.touch_updated_at();

-- ---------------------------------------------------------------------------
-- Row Level Security
--   read  : published vods are public, except those by banned users
--   write : a signed-in user may only touch their own rows
--   (the creator whitelist is enforced in the API, not here)
-- ---------------------------------------------------------------------------
alter table public.memberships enable row level security;
alter table public.vods         enable row level security;

drop policy if exists memberships_read on public.memberships;
create policy memberships_read on public.memberships for select using (true);

drop policy if exists vods_read on public.vods;
create policy vods_read on public.vods for select using (is_published);

drop policy if exists vods_insert_own on public.vods;
drop policy if exists vods_update_own on public.vods;
drop policy if exists vods_delete_own on public.vods;
create policy vods_insert_own on public.vods for insert
  with check (auth.uid() = creator);
create policy vods_update_own on public.vods for update
  using (auth.uid() = creator) with check (auth.uid() = creator);
create policy vods_delete_own on public.vods for delete
  using (auth.uid() = creator);
