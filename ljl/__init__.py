'''
https://code.visualstudio.com/docs/editor/debugging#_launchjson-attributes
'''
import sys
import re
import pathlib
import subprocess
from typing import NamedTuple, List
# import json
import json5
HERE = pathlib.Path(__file__).absolute().parent

__version__ = '0.0.1'


class Configuration(NamedTuple):
    type: str
    request: str
    name: str
    program: str
    args: List[str]
    console: str

    def launch(self):
        # print(self)
        cmd = f'{self.program} {" ".join(self.args)}'
        print(cmd)
        subprocess.call(cmd, shell=True)


def launch(launch_json: pathlib.Path, index: int = 0) -> None:
    src = launch_json.read_text(encoding='utf-8')

    def repl(m):
        key = m.group(1)
        if key == 'workspaceFolder':
            return str(launch_json.parent.parent).replace('\\', '/')
        raise Exception(f'unknown variable ${{{key}}}')

    src = re.sub(r'\$\{([^}]+)\}', repl, src)

    parsed = json5.loads(src)

    selected = parsed['configurations'][index]
    conf = Configuration(**selected)

    conf.launch()


def main():
    index = 0
    if len(sys.argv) > 1:
        index = int(sys.argv[1])

    current = pathlib.Path('.').absolute()
    while True:
        dir = current / '.vscode'
        if dir.is_dir():
            launch_json = dir / 'launch.json'
            if launch_json.exists():
                launch(launch_json, index)
                sys.exit(0)
            else:
                # not found
                sys.exit(1)

        if current.parent == current:
            # not found
            sys.exit(1)

        current = current.parent


if __name__ == '__main__':
    main()
