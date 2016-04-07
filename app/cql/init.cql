DROP KEYSPACE IF EXISTS test;
CREATE KEYSPACE test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'};
USE test;

CREATE TABLE build_events (build_id uuid, clock int, event_type text, data text, PRIMARY KEY (build_id, clock));
