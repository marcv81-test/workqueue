import cassandra.cluster
import sys
import uuid

build_id = sys.argv[1]
return_code = 1

# Cassandra setup
cluster = cassandra.cluster.Cluster(
		['192.168.56.101', '192.168.56.101'])
session = cluster.connect('test')

select_statement = session.prepare(
		'SELECT event_type, data '
		'FROM build_events '
		'WHERE build_id=? ORDER BY clock')
for row in session.execute(select_statement, [uuid.UUID(build_id)]):
	if row.event_type == 'stdout':
		sys.stdout.write('\033[0m' + row.data + '\033[0m')
	elif row.event_type == 'stderr':
		sys.stderr.write('\033[91m' + row.data + '\033[0m')
	elif row.event_type == 'exit':
		return_code = int(row.data)
exit(return_code)
