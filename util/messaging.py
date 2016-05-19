import cluster
import pika

def open_channel():
	"""Open and configure an AMQP channel"""

	channel = cluster.get_rabbitmq_channel()
	channel.basic_qos(prefetch_count=1)

	# We publish all the build requests to a single exchange bound
	# to a single queue. All the workers subscribe to this queue to
	# share the workload.
	channel.exchange_declare(exchange='build_requests', type='fanout')
	channel.queue_declare(queue='build_requests')
	channel.queue_bind(
			exchange='build_requests',
			queue='build_requests')

	# We publish all the build events to a single exchange with the
	# build ID as the routing key.
	# We route all the events to a single queue regardless of the
	# routing key. All the database loggers subscribe to this queue
	# to share the workload.
	# When required, we also route the events with the appropriate
	# routing key to exclusive queues to track specific builds.
	channel.exchange_declare(exchange='build_events', type='topic')
	channel.queue_declare(queue='build_events')
	channel.queue_bind(
			exchange='build_events',
			queue='build_events',
			routing_key='*')

	return channel

class BuildRequestor():
	"""Submit build requests"""

	def __init__(self, channel):
		self._channel = channel

	def send(self, build_id, data):
		self._channel.basic_publish(
				exchange = 'build_requests',
				routing_key = '',
				properties = pika.BasicProperties(
					reply_to=str(build_id)),
				body = str(data))

class BuildResponder():
	"""Respond to build requests"""

	def __init__(self, channel):
		self._channel = channel
		self._channel.basic_consume(
				self.on_request, 'build_requests', no_ack=True)

	def on_request(self, channel, method, properties, data):
		build_id = properties.reply_to
		self.respond(build_id, data)

class BuildEventSender:
	"""Send build events"""

	def __init__(self, channel, build_id):
		self._channel = channel
		self._build_id = build_id
		self._clock = 0

	def send(self, event_type, data):
		self._channel.basic_publish(
				exchange = 'build_events',
				routing_key = str(self._build_id),
				properties = pika.BasicProperties(headers={
					'event_type': str(event_type),
					'clock': str(self._clock)}),
				body = str(data))
		self._clock += 1

class BuildEventReceiver:
	"""Receive build events"""

	def __init__(self, channel, build_id=None):
		self._channel = channel

		# By default, consume the database logging build events queue.
		if build_id == None:
			queue = 'build_events'

		# If a build ID is specified, then create an exclusive queue,
		# route the appropriate build events to it, and consume it.
		else:
			queue = self._channel.queue_declare(
					exclusive=True).method.queue
			self._channel.queue_bind(
					exchange='build_events',
					queue=queue,
					routing_key=build_id)

		self._channel.basic_consume(
				self.on_message, queue=queue, no_ack=True)

	def on_message(self, channel, method, properties, data):
		event_type = properties.headers['event_type']
		clock = int(properties.headers['clock'])
		build_id = method.routing_key
		self.receive(build_id, clock, event_type, data)
