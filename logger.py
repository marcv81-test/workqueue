import ssl
import threading
import time
import util.cluster
import util.messaging
import uuid

class DatabaseBuildEventReceiver(
		util.messaging.BuildEventReceiver, threading.Thread):
	"""Receive build events and insert them into the database"""

	def __init__(self):
		threading.Thread.__init__(self)

		# RabbitMQ setup
		util.messaging.BuildEventReceiver.__init__(self,
				util.messaging.open_channel())

		# Cassandra setup
		self._session = util.cluster.get_cassandra_session()
		self._statement = self._session.prepare(
				'INSERT INTO '
				'build_events (build_id, clock, event_type, data) '
				'VALUES (?, ?, ?, ?)')

	def receive(self, build_id, clock, event_type, data):
		self._session.execute(self._statement,
				(uuid.UUID(build_id), clock, event_type, data))
		if clock == 0:
			print 'Starting ' + build_id
		if event_type == 'exit':
			print 'Stopping ' + build_id

	def run(self):
		self._channel.start_consuming()

# Start threads
for i in xrange(20):
	thread = DatabaseBuildEventReceiver()
	thread.daemon = True
	thread.start()
while True:
	time.sleep(60)
