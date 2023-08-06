import re
from subprocess import CompletedProcess


class RunCommandException(Exception):
    def __init__(self, completed_process: CompletedProcess):
        dashes = '-' * 100
        lines = (
            dashes,
            f'args: {completed_process.args}',
            dashes,
            completed_process.stderr.strip(),
            dashes,
        )
        message = '\n'.join(lines)
        message = re.sub('^', '# ', message, flags=re.MULTILINE)
        super().__init__(f'\n{message}\n')
