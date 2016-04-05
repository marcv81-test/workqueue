import fcntl
import os
import select
import shlex
import subprocess

class Process:
	"""Runs commands and captures stdout/stderr efficiently"""

	def __init__(self, on_stdout, on_stderr):
		"""Constructor"""
		self.on_stdout = on_stdout
		self.on_stderr = on_stderr

	def run(self, command):
		"""Run a command"""

		try:
			process = subprocess.Popen(
					shlex.split(str(command)), shell=False,
					stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		except Exception as e:
			self.on_stderr('An exception occurred\n')
			return 1

		stdout_fd = process.stdout.fileno()
		stderr_fd = process.stderr.fileno()

		# Configure stdout and stderr for non-blocking reads
		def configure_fd(fd):
			fl = fcntl.fcntl(fd, fcntl.F_GETFL)
			fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
		configure_fd(stdout_fd)
		configure_fd(stderr_fd)

		# Wait until stdout and/or stderr is available for reading.
		# An empty read on an available stream indicates its end.
		# Repeat until both streams end.
		read_fds = [stdout_fd, stderr_fd]
		while len(read_fds) > 0:
			fds = select.select(read_fds, [], [])
			for fd in fds[0]:

				# stdout is available for reading
				if fd == stdout_fd:
					read = process.stdout.read()
					if len(read) > 0:
						self.on_stdout(read)
					else:
						read_fds.remove(stdout_fd)
						process.stdout.close()

				# stderr is available for reading
				if fd == stderr_fd:
					read = process.stderr.read()
					if len(read) > 0:
						self.on_stderr(read)
					else:
						read_fds.remove(stderr_fd)
						process.stderr.close()

		process.wait()
		return process.poll()
