import logging
import sys
from typing import List

from gfworkflow import logger, R, logger_handler
from gfworkflow.cli import cli


def _create_file_handler() -> logging.FileHandler:
    R.path.log_folder.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(filename=R.path.log_file, mode='a')

    file_handler.setLevel(logging.DEBUG)

    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(threadName)s - %(name)s - %(levelname)s\n%(message)s',
            '%Y-%m-%d %H:%M:%S'
        )
    )
    return file_handler


def main(params: List[str] = None):
    with logger_handler(logger, _create_file_handler()):
        cli(params)
    pass


def console_script_entry():
    main(sys.argv[1:])
    pass


if __name__ == '__main__':
    console_script_entry()
