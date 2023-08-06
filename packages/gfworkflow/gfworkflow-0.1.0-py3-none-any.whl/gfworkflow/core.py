import re
import subprocess as sp
from typing import Union, List

from gfworkflow.exceptions import RunCommandException


def run(command: Union[str, List[str]]):
    completed_process = sp.run(command, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
    if completed_process.returncode:
        raise RunCommandException(completed_process)
    return completed_process


def init():
    run('git flow init -d -f')
    run('git config gitflow.prefix.versiontag v')


def bump_version(part: str):
    run(f'bumpversion {part}')


def start_release(new_version: str):
    run(f'git flow release start {new_version}')


def get_new_version(part: str):
    output = run(f'bumpversion {part} --list -n --allow-dirty --no-configured-files').stdout
    return re.compile(r'new_version=(\S+)').search(output).group(1)


def get_current_branch_name():
    return run('git rev-parse --abbrev-ref HEAD').stdout.strip()


def finish_release(release_name):
    run(f'git flow release finish -m " - " {release_name}')
