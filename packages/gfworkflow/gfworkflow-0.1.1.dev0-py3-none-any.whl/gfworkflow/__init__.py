import logging
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Union

from gfworkflow import R

logger: logging.Logger = logging.getLogger(R.string.package_name)
logger.setLevel(logging.DEBUG)


@contextmanager
def logger_handler(logger_: logging.Logger, handler: logging.Handler):
    logger_.addHandler(handler)
    try:
        yield None
    finally:
        handler.close()
        logger_.removeHandler(handler)


def clear_log():
    file_handlers = (
        tuple(filter(lambda x: isinstance(x, logging.FileHandler), logger.handlers))
    )
    if len(file_handlers) == 1:
        file_handlers[0].close()
    R.path.log_file.unlink(missing_ok=True)


def dump_log(dst: Union[str, Path]):
    if isinstance(dst, str):
        dst = Path(dst)
    if R.path.log_file.exists():
        logger.info(f'Dumping log file at: {dst.resolve()}')
        shutil.copy2(R.path.log_file, dst)
    else:
        logger.info('No log file to dump')
