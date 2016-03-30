import threading
import time
import util.messaging
import util.process

class WorkerBuildResponder(
		util.messaging.BuildResponder, threading.Thread):
	"""Receive build requests and execute them"""

	def __init__(self):
		threading.Thread.__init__(self)

		# RabbitMQ setup
		util.messaging.BuildResponder.__init__(self,
				util.messaging.open_channel())

	def respond(self, build_id, data):
		command = data
		print build_id + ' Command: ' + command
		sender = util.messaging.BuildEventSender(self._channel, build_id)
		process = util.process.Process(
				on_stdout = lambda data: sender.send('stdout', data),
				on_stderr = lambda data: sender.send('stderr', data))
		return_code = str(process.run(command))
		print build_id + ' Return code: ' + return_code
		sender.send('exit', return_code)

	def run(self):
		self._channel.start_consuming()

# Start threads
for i in xrange(1):
	thread = WorkerBuildResponder()
	thread.daemon = True
	thread.start()
while True:
	time.sleep(60)
