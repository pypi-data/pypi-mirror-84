from pathlib import Path
from typing import Union

import gfworkflow
from gfworkflow import R, logger, core


def version_method():
    logger.info(f'{R.string.program_name} v{R.string.version}')
    pass


def clear_log_method():
    gfworkflow.clear_log()


def dump_log_method(dst: Union[str, Path]):
    gfworkflow.dump_log(dst)


def init_method():
    core.init()


def bump_version_method(part: str):
    core.bump_version(part)


def start_release_method(part: str):
    new_version = core.get_new_version(part)
    core.start_release(new_version)
    pass


def finish_release_method():
    release_name = core.get_current_branch_name().replace('release/', '')
    core.finish_release(release_name)


def bump_release_method(part: str):
    new_version = core.get_new_version(part)
    core.start_release(new_version)
    core.bump_version(part)
    core.finish_release(new_version)
