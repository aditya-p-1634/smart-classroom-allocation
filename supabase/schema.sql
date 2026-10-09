create extension if not exists btree_gist;

create table if not exists public.bookings (
    booking_id text primary key,
    user_type text not null,
    user_id text not null,
    course_code text not null,
    semester text not null,
    resource_type text not null,
    resource_id text not null,
    booking_date date not null,
    start_time text not null,
    start_period smallint not null check (start_period between 1 and 8),
    periods smallint not null check (periods between 1 and 8),
    check (start_period + periods <= 9),
    status text not null,
    booking_timestamp text not null,
    created_by text not null,
    constraint bookings_no_overlapping_confirmed_slots
        exclude using gist (
            resource_id with =,
            booking_date with =,
            int4range(start_period, start_period + periods, '[)') with &&
        )
        where (status = 'Confirmed')
);

create table if not exists public.blocked_users (
    user_id text primary key,
    blocked boolean not null,
    reason text not null default '',
    updated_by text not null,
    updated_at text not null
);

alter table public.bookings enable row level security;
alter table public.blocked_users enable row level security;
