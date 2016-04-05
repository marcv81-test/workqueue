import unittest
import util.process as p

class ProcessTestCase(unittest.TestCase):

	def test_return_code(self):

		process = p.Process(
				on_stdout = lambda data: None,
				on_stderr = lambda data: None)

		# "/bin/true" returns 0
		self.assertEqual(0, process.run('/bin/true'))

		# "/bin/false" returns 1
		self.assertEqual(1, process.run('/bin/false'))

	def test_stdout_stderr(self):

		storage = {}
		def store(stream, data):
			storage[stream] += str(data)
		process = p.Process(
				on_stdout = lambda data: store('stdout', data),
				on_stderr = lambda data: store('stderr', data))

		# "echo test" writes "test" to stdout (and nothing to stderr)
		storage = {'stdout': '', 'stderr': ''}
		process.run('/bin/sh -c "echo test"')
		self.assertEqual('test\n', storage['stdout'])
		self.assertEqual('', storage['stderr'])

		# ">&2 echo test" writes "test" to stderr (and nothing to stdout)
		storage = {'stdout': '', 'stderr': ''}
		process.run('/bin/sh -c ">&2 echo test"')
		self.assertEqual('', storage['stdout'])
		self.assertEqual('test\n', storage['stderr'])

	def test_exception(self):

		storage = {}
		def store(stream, data):
			storage[stream] += str(data)
		process = p.Process(
				on_stdout = lambda data: None,
				on_stderr = lambda data: store('stderr', data))

		# "/bin/crash_test" returns 1
		storage = {'stderr': ''}
		self.assertEqual(1, process.run('/bin/crash_test'))
		self.assertEqual('An exception occurred\n', storage['stderr'])
