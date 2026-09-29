create extension if not exists pgcrypto;

create type public.app_role as enum ('reader','customer');
create type public.birth_time_precision as enum ('exact','approximate','unknown');
create type public.reading_status as enum ('draft','calculated','cards_drawn','synthesized','reviewed','published','archived');

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  role public.app_role not null default 'customer',
  full_name text not null,
  email text,
  phone text,
  gender text,
  current_city text,
  relationship_status text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.birth_profiles (
  id uuid primary key default gen_random_uuid(),
  owner_user_id uuid not null references auth.users(id) on delete cascade,
  subject_name text not null,
  date_of_birth date not null,
  birth_time time,
  birth_time_precision public.birth_time_precision not null,
  birthplace_label text not null,
  latitude double precision not null check (latitude between -90 and 90),
  longitude double precision not null check (longitude between -180 and 180),
  timezone text not null,
  optional_data jsonb not null default '{}'::jsonb,
  consent_record jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint birth_time_precision_guard check (
    (birth_time_precision = 'unknown' and birth_time is null)
    or (birth_time_precision <> 'unknown' and birth_time is not null)
  )
);

create table public.chart_snapshots (
  id uuid primary key default gen_random_uuid(),
  birth_profile_id uuid not null references public.birth_profiles(id) on delete cascade,
  calculation_version text not null,
  settings jsonb not null,
  chart_data jsonb not null,
  reliability jsonb not null default '{}'::jsonb,
  calculated_at timestamptz not null default now(),
  unique (birth_profile_id, calculation_version, settings)
);

create table public.reading_sessions (
  id uuid primary key default gen_random_uuid(),
  reader_user_id uuid not null references auth.users(id),
  customer_user_id uuid references auth.users(id),
  birth_profile_id uuid not null references public.birth_profiles(id),
  chart_snapshot_id uuid references public.chart_snapshots(id),
  question text,
  life_domain text,
  spread_key text,
  status public.reading_status not null default 'draft',
  current_astrology jsonb,
  final_report jsonb,
  published_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.card_draws (
  id uuid primary key default gen_random_uuid(),
  reading_session_id uuid not null references public.reading_sessions(id) on delete cascade,
  position_index integer not null check (position_index > 0),
  position_key text,
  card_id integer not null check (card_id between 1 and 108),
  orientation text not null default 'upright',
  selection_mode text not null check (selection_mode in ('physical','digital','customer')),
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique(reading_session_id, position_index)
);

create table public.interpretation_evidence (
  id uuid primary key default gen_random_uuid(),
  reading_session_id uuid not null references public.reading_sessions(id) on delete cascade,
  evidence_type text not null check (evidence_type in ('natal','dasha','transit','card','combination','reader_note','source')),
  evidence_key text not null,
  payload jsonb not null,
  confidence numeric(4,3) check (confidence between 0 and 1),
  created_at timestamptz not null default now()
);

create table public.reader_notes (
  id uuid primary key default gen_random_uuid(),
  reading_session_id uuid not null references public.reading_sessions(id) on delete cascade,
  author_user_id uuid not null references auth.users(id),
  note text not null,
  private boolean not null default true,
  created_at timestamptz not null default now()
);

create table public.audit_events (
  id bigint generated always as identity primary key,
  actor_user_id uuid references auth.users(id),
  entity_type text not null,
  entity_id text not null,
  action text not null,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create or replace function public.is_reader() returns boolean language sql stable security definer set search_path=public as $$
  select exists(select 1 from public.profiles p where p.id=auth.uid() and p.role='reader');
$$;

alter table public.profiles enable row level security;
alter table public.birth_profiles enable row level security;
alter table public.chart_snapshots enable row level security;
alter table public.reading_sessions enable row level security;
alter table public.card_draws enable row level security;
alter table public.interpretation_evidence enable row level security;
alter table public.reader_notes enable row level security;
alter table public.audit_events enable row level security;

create policy profiles_self_or_reader_select on public.profiles for select using (id=auth.uid() or public.is_reader());
create policy profiles_self_update on public.profiles for update using (id=auth.uid()) with check (id=auth.uid());

create policy birth_profiles_owner_or_reader on public.birth_profiles for select using (owner_user_id=auth.uid() or public.is_reader());
create policy birth_profiles_owner_insert on public.birth_profiles for insert with check (owner_user_id=auth.uid() or public.is_reader());
create policy birth_profiles_owner_update on public.birth_profiles for update using (owner_user_id=auth.uid() or public.is_reader()) with check (owner_user_id=auth.uid() or public.is_reader());

create policy charts_visible_with_birth_profile on public.chart_snapshots for select using (exists(select 1 from public.birth_profiles b where b.id=birth_profile_id and (b.owner_user_id=auth.uid() or public.is_reader())));
create policy charts_reader_write on public.chart_snapshots for all using (public.is_reader()) with check (public.is_reader());

create policy readings_visible on public.reading_sessions for select using (reader_user_id=auth.uid() or customer_user_id=auth.uid() or public.is_reader());
create policy readings_reader_write on public.reading_sessions for all using (reader_user_id=auth.uid() or public.is_reader()) with check (reader_user_id=auth.uid() or public.is_reader());

create policy draws_visible on public.card_draws for select using (exists(select 1 from public.reading_sessions r where r.id=reading_session_id and (r.reader_user_id=auth.uid() or r.customer_user_id=auth.uid() or public.is_reader())));
create policy draws_reader_write on public.card_draws for all using (public.is_reader()) with check (public.is_reader());

create policy evidence_visible on public.interpretation_evidence for select using (exists(select 1 from public.reading_sessions r where r.id=reading_session_id and (r.reader_user_id=auth.uid() or r.customer_user_id=auth.uid() or public.is_reader())));
create policy evidence_reader_write on public.interpretation_evidence for all using (public.is_reader()) with check (public.is_reader());

create policy notes_reader_only on public.reader_notes for all using (public.is_reader()) with check (public.is_reader());
create policy audit_reader_select on public.audit_events for select using (public.is_reader());
