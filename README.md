# Pyscripts
## Pytools
### Cli
<p>def build_docker_image(name, path=os.getcwd()):
    return _pt.cli.run_pipe(f'docker build -t={name} .', cwd=path)</p>