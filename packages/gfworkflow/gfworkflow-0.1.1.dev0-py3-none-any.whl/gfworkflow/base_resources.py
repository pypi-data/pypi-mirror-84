from pathlib import Path

import pkg_resources


class string:
    package_name: str = 'gfworkflow'
    package_path = pkg_resources.resource_filename(package_name, '')
    res_folder_name: str = 'res'
    res_folder_path = pkg_resources.resource_filename(package_name, res_folder_name)
    version: str = 'version: 0.1.1-dev'.replace('version: ', '')
    program_name: str = 'gfworkflow'
    program_name_cli: str = 'gfworkflow'
    program_description: str = ''
    log_file_name: str = f'{package_name}.log'


class path:
    log_folder = Path.home() / '.logs' / string.package_name
    log_file = log_folder / string.log_file_name


class param:
    version = '--version'
    version_help = 'show program version'
    dump_log = '--dump-log'
    dump_log_meta_var = 'dir'
    dump_log_help = 'dump log to dir'
    clear_log = '--clear-log'
    clear_log_help = 'clear log'
