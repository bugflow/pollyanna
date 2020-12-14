from pathlib import Path

from pie import *
from pie_docker import *


ROOT_DIR=Path('.').absolute()
DOCS_BUILDER_IMAGE_NAME='pollyanna/docs_builder'


def _run_docs_builder(c,listen_port=False):
    run_options=['--rm','-it',f'-v "{ROOT_DIR}:/app"','--name pollyanna__docs_builder']
    if listen_port:
        run_options.append('-p 8999:80')
    Docker().run(DOCS_BUILDER_IMAGE_NAME,c,run_options)


@task
def create_docker_image():
    """Create the docker image that can build the docs"""
    Docker().build('.',['-f docker/Dockerfile',f'-t {DOCS_BUILDER_IMAGE_NAME}','--no-cache','--rm'])


@task
def build():
    """Build the docs and exit"""
    sphinx_args = [
        '-a',
        '-v',
        '-b html',
        '.',
        '_build/html',
    ]
    _run_docs_builder('python -m sphinx {}'.format(' '.join(sphinx_args)))


@task
def autobuild():
    """Build the docs and run a server that hosts the docs and will automatically rebuild them on changes"""
    sphinx_args = [
        '-a',
        '-v',
        '-b html',
        '-p 80',
        '-H 0.0.0.0',
        '--ignore docs/_build/*',
        '.',
        '_build/html',
    ]
    _run_docs_builder('sphinx-autobuild {}'.format(' '.join(sphinx_args)),listen_port=True)


@task
def sphinx_help():
    """Get sphinx help"""
    _run_docs_builder('python -m sphinx --help')


@task
def bash():
    """Bash terminal within the doc builder container"""
    _run_docs_builder('bash')
