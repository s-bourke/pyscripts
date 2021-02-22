import os
from rich.console import Console

import pytools as _pt

_console = Console()


def build_docker_image(name, path=os.getcwd()):
	return _pt.cli.run_pipe(f'docker build -t={name} .', cwd=path)


def build_database_image(name):
	with _console.status(f"[bold yellow] Building image [blue]{name}[/blue]...[/bold yellow]"):
		output = build_docker_image('/home/sam/Workspace/' + name, name)
		_console.log(f"[bold green]Image [blue]{name}[/blue] built.")
	return output


def does_container_exist(name):
	output = _pt.cli.run_pipe(f"docker ps --all --format {{{{.Names}}}}")
	return name in output.split('\n')


def is_container_running(name):
	if does_container_exist(name):
		return _pt.cli.run_pipe(f"docker inspect -f '{{{{.State.Running}}}}' {name}") == "'true'"
	else:
		return False


def kill_container(name):
	if (is_container_running(name)):
		_pt.cli.run_pipe(f"docker kill {name}")
		_pt.cli.run_pipe(f"docker rm {name}")


def start_container(name, restart='no', ports=None):
	portsString = ' '.join('-p ' + port for port in ports)
	kill_container(name)
	_pt.cli.run_pipe(f"docker run --restart {restart} --name {name} -d {name}")
	output=pt.cli.run_pipe(f"docker run --restart {restart} --name {name} {portsString} -d {name}")


def remove_image(name):
	if _pt.cli.run_pipe(f'docker images -q {name}') == '':
		_console.log(f"[bold yellow]Image [blue]{name}[/blue] does not exist.[/bold yellow]")
	else:
		_pt.cli.run_quiet('docker rmi ' + name)
		_console.log(f"[bold red]Image [blue]{name}[/blue] removed.[/bold red]")
