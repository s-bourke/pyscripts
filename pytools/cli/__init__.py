import os
import subprocess


# Functions

def run_verbose(command, cwd=os.getcwd()):
	run(command, cwd=cwd)


def run_quiet(command, cwd=os.getcwd()):
	run(command, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def run_pipe(command, cwd=os.getcwd()):
	return str(run(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout).strip()


def run(command, cwd=os.getcwd(), stdout=None, stderr=None):
	return subprocess.run(command.split(' '), cwd=cwd, stdout=stdout, stderr=stderr, universal_newlines=True)
