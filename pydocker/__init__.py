import os

from rich.console import Console

import pytools as _pt

_console = Console()


def build_docker_image(name, path=os.getcwd()):
	"""
	Build a docker image
	:param name: The name of the image to be built
	:param path: The path to the dockerfile directory if not current directory
	:return: Console output from docker build
	"""
	return _pt.cli.run_pipe(f'docker build -t={name} .', cwd=path)


def build_database_image(name):
	"""
	Build a databse image with pretty console output
	:param name: Name of the db project
	:return: Console output from docker build
	"""
	with _console.status(f"[bold yellow] Building image [blue]{name}[/blue]...[/bold yellow]"):
		output = build_docker_image('/home/sam/Workspace/' + name, name)
		_console.log(f"[bold green]Image [blue]{name}[/blue] built.")
	return output


def does_container_exist(name):
	"""
	Check if container exists
	:param name: Name of the container
	:return: True if container exists
	"""
	output = _pt.cli.run_pipe(f"docker ps --all --format {{{{.Names}}}}")
	return name in output.split('\n')


def is_container_running(name):
	"""
	Check if container is running
	:param name: Name of the container
	:return: True if container is running
	"""
	if does_container_exist(name):
		return _pt.cli.run_pipe(f"docker inspect -f '{{{{.State.Running}}}}' {name}") == "'true'"
	else:
		return False


def kill_container(name):
	"""
	Kill and remove container
	:param name: Name of the container
	"""
	if is_container_running(name):
		_pt.cli.run_pipe(f"docker kill {name}")
		_pt.cli.run_pipe(f"docker rm {name}")


def start_container(name, restart='no', ports=None):
	"""
	Start a container. If container is already running, kill it and start a new one
	:param name: Name of the container
	:param restart: Restart policy. By default "No". https://docs.docker.com/engine/reference/run/#restart-policies---restart
	TODO: Finish this
	:param ports: The ports to expose as list. E.g [""]
	"""
	ports_string = ' '.join('-p ' + port for port in ports)
	kill_container(name)
	_pt.cli.run_pipe(f"docker run --restart {restart} --name {name} {ports_string} -d {name}")


def remove_image(name):
	"""
	Remove an image
	:param name: Name of the image
	"""
	if _pt.cli.run_pipe(f'docker images -q {name}') == '':
		_console.log(f"[bold yellow]Image [blue]{name}[/blue] does not exist.[/bold yellow]")
	else:
		_pt.cli.run_quiet('docker rmi ' + name)
		_console.log(f"[bold red]Image [blue]{name}[/blue] removed.[/bold red]")
