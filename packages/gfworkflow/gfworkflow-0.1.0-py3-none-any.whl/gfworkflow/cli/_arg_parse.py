import argparse
from pathlib import Path
from typing import List, Optional

from gfworkflow import R


class Args(object):
    def __init__(self, args_list: List[str] = None):
        if args_list is None:
            args_list = []

        parser: argparse.ArgumentParser = argparse.ArgumentParser(
            prog=R.string.program_name,
            description=R.string.program_description,
        )
        parser.add_argument(R.param.version, action='store_true', help=R.param.version_help)

        def is_dir(string) -> Optional[Path]:
            path: Path = Path(string)
            if path.is_dir():
                return path
            else:
                type_error_message = f"{string} is not a directory"
                raise argparse.ArgumentTypeError(type_error_message)

        parser.add_argument(R.param.dump_log, metavar=R.param.dump_log_meta_var,
                            nargs='?', const='.', type=is_dir,
                            help=R.param.dump_log_help)

        parser.add_argument(R.param.clear_log, action='store_true', help=R.param.clear_log_help)

        parser.add_argument(R.param.init, action='store_true', help=R.param.init_help)

        parser.add_argument(R.param.bump_version, metavar='part', help=R.param.bump_version_help)

        parser.add_argument(R.param.start_release, metavar='part', help=R.param.start_release_help)

        parser.add_argument(R.param.finish_release, action='store_true', help=R.param.finish_release_help)

        parser.add_argument(R.param.bump_release, metavar='part', help=R.param.bump_release_help)

        self._args: argparse.Namespace = parser.parse_args(args_list)

    @property
    def version(self) -> bool:
        return self._args.version

    @property
    def dump_log(self) -> Optional[str]:
        return self._args.dump_log

    @property
    def clear_log(self) -> bool:
        return self._args.clear_log

    @property
    def init(self) -> bool:
        return self._args.init

    @property
    def bump_version(self) -> str:
        return self._args.bump_version

    @property
    def start_release(self) -> str:
        return self._args.start_release

    @property
    def finish_release(self):
        return self._args.finish_release

    @property
    def bump_release(self):
        return self._args.bump_release
