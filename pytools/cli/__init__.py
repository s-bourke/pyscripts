import os
import subprocess


# TODO: Add support for piped commands

def run_verbose(command, cwd=os.getcwd()):
	"""
	Run command line statement and print output to terminal
	:param command: The command to be run
	:param cwd: The directory to run the command, if not the current directors
	"""
	run(command, cwd=cwd)


def run_quiet(command, cwd=os.getcwd()):
	"""
	Run command line statement and suppress output
	:param command: The command to be run
	:param cwd: The directory to run the command, if not the current directors
	"""
	run(command, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def run_pipe(command, cwd=os.getcwd()):
	"""
	Run command line statement and return output as a string
	:param command: The command to be run
	:param cwd: The directoy to run the command, if not the current directors
	:rtype: str
	"""
	return str(run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout).strip()


def run(command, cwd=os.getcwd(), stdout=None, stderr=None):
	"""
	Run command line statement and return output as a string
	:param command: The command to be run
	:param cwd: The directoy to run the command, if not the current directors
	:param stdout Where to route stdout
	:param stderr Where to route stderr
	"""
	return subprocess.run(command.split(' '), cwd=cwd, stdout=stdout, stderr=stderr, universal_newlines=True)
