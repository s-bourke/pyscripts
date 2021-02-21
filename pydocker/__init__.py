import os

from rich.console import Console
from rich.live import Live

import pytools as pt

console = Console()


def build_docker_image(name, path=os.getcwd()):
	return pt.cli.run_pipe(f'docker build -t={name} .', cwd=path)


def build_database_image(name):
	with console.status(f"[bold yellow] Building image [blue]{name}[/blue]...[/bold yellow]"):
		output = build_docker_image('/home/sam/Workspace/' + name, name)
		console.log(f"[bold green]Image [blue]{name}[/blue] built.")
	return output


def does_container_exist(name):
	output = pt.cli.run_pipe(f"docker ps --all --format {{{{.Names}}}}")
	return name in output.split('\n')


def is_container_running(name):
	if does_container_exist(name):
		return pt.cli.run_pipe(f"docker inspect -f '{{{{.State.Running}}}}' {name}") == "'true'"
	else:
		return False
	Live()


def kill_container(name):
	if (is_container_running(name)):
		pt.cli.run_pipe(f"docker kill {name}")
		pt.cli.run_pipe(f"docker rm {name}")


def start_container(name, restart='no'):
	kill_container(name)
	pt.cli.run_pipe(f"docker run --restart {restart} --name {name} -d {name}")


def remove_image(name):
	if pt.cli.run_pipe(f'docker images -q {name}') == '':
		console.log(f"[bold yellow]Image [blue]{name}[/blue] does not exist.[/bold yellow]")
	else:
		pt.cli.run_quiet('docker rmi ' + name)
		console.log(f"[bold red]Image [blue]{name}[/blue] removed.[/bold red]")
