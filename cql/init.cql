DROP KEYSPACE IF EXISTS test;
CREATE KEYSPACE test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'};

DROP USER IF EXISTS test_user;
CREATE USER test_user WITH PASSWORD 'password';
GRANT ALL ON KEYSPACE test TO test_user;
