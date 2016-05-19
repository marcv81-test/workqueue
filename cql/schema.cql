USE test;
CREATE TABLE build_events (build_id uuid, clock int, event_type text, data text, PRIMARY KEY (build_id, clock));
