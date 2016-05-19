import cassandra.auth
import cassandra.cluster
import pika
import ssl

def get_cassandra_session():

	# Cluster configuration
	nodes = ['192.168.56.101', '192.168.56.102', '192.168.56.103']
	username = 'test_user'
	password = 'password'
	keyspace = 'test'

	ssl_opts = {'ssl_version': ssl.PROTOCOL_TLSv1_2}
	auth_provider = cassandra.auth.PlainTextAuthProvider(
			username=username, password=password)
	cluster = cassandra.cluster.Cluster(
			contact_points=nodes,
			auth_provider=auth_provider,
			ssl_options=ssl_opts)
	return cluster.connect(keyspace)

def get_rabbitmq_channel():

	# Cluster configuration
	nodes = ['192.168.56.91', '192.168.56.92']
	username = 'user'
	password = 'user'

	for i in xrange(len(nodes)):
		try:
			connection = pika.BlockingConnection(pika.ConnectionParameters(
					host=nodes[i],
					credentials=pika.PlainCredentials(username, password)))
			return connection.channel()
		except pika.exceptions.ConnectionClosed, e:
			if i == len(nodes) - 1:
				raise e
