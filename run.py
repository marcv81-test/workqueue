import sys
import util.messaging
import uuid

command = sys.argv[1]
build_id = str(uuid.uuid1())

print 'Build: ' + build_id

class DisplayBuildEventReceiver(
		util.messaging.BuildEventReceiver):
	"""Receive build events and display them"""

	def __init__(self, channel, build_id):
		util.messaging.BuildEventReceiver.__init__(self,
				channel, build_id)
		self.return_code = None

	def receive(self, build_id, clock, event_type, data):
		if event_type == 'stdout':
			sys.stdout.write('\033[0m' + data + '\033[0m')
		elif event_type == 'stderr':
			sys.stderr.write('\033[91m' + data + '\033[0m')
		elif event_type == 'exit':
			self.return_code = int(data)
			self._channel.stop_consuming()

channel = util.messaging.open_channel()

# Prepare to receive the build events
receiver = DisplayBuildEventReceiver(channel, build_id)

# Submit the build request
requestor = util.messaging.BuildRequestor(channel)
requestor.send(build_id, command)

# Receive the build events
channel.start_consuming()
exit(receiver.return_code)
