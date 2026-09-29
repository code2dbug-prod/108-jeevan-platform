create table if not exists public.report_versions (
  id uuid primary key default gen_random_uuid(),
  reading_session_id uuid not null references public.reading_sessions(id) on delete cascade,
  version integer not null check (version > 0),
  report_data jsonb not null,
  approved_by uuid references auth.users(id),
  created_at timestamptz not null default now(),
  unique(reading_session_id, version)
);

create table if not exists public.data_requests (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  request_type text not null check (request_type in ('export','delete','correct')),
  status text not null default 'open' check (status in ('open','processing','completed','rejected')),
  details jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  completed_at timestamptz
);

alter table public.report_versions enable row level security;
alter table public.data_requests enable row level security;

create policy report_versions_visible on public.report_versions for select using (
  exists(select 1 from public.reading_sessions r where r.id=reading_session_id and
    (r.reader_user_id=auth.uid() or r.customer_user_id=auth.uid() or public.is_reader()))
);
create policy report_versions_reader_write on public.report_versions for all
  using (public.is_reader()) with check (public.is_reader());

create policy data_requests_self on public.data_requests for select using (user_id=auth.uid() or public.is_reader());
create policy data_requests_self_insert on public.data_requests for insert with check (user_id=auth.uid());
create policy data_requests_reader_update on public.data_requests for update using (public.is_reader()) with check (public.is_reader());

create index if not exists idx_birth_profiles_owner on public.birth_profiles(owner_user_id);
create index if not exists idx_readings_customer on public.reading_sessions(customer_user_id, created_at desc);
create index if not exists idx_readings_birth_profile on public.reading_sessions(birth_profile_id, created_at desc);
create index if not exists idx_evidence_reading on public.interpretation_evidence(reading_session_id);
create index if not exists idx_draws_reading on public.card_draws(reading_session_id, position_index);
