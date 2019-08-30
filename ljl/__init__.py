'''
https://code.visualstudio.com/docs/editor/debugging#_launchjson-attributes
'''
import sys
import os
import re
import pathlib
import subprocess
from typing import NamedTuple, List, Dict
# import json
import json5
HERE = pathlib.Path(__file__).absolute().parent

__version__ = '0.0.1'


class Configuration(NamedTuple):
    type: str
    request: str
    name: str
    program: str
    args: List[str] = []
    console: str = ''
    stopOnEntry: bool = False
    cwd: str = ''
    env: Dict[str, str] = {}

    def launch(self):
        # print(self)
        cmd = f'{self.program} {" ".join(self.args)}'
        if 'PATH' in self.env:
            self.env['PATH'] = self.env['PATH'].replace('/', '\\')
            # print(self.env['PATH'])
        env = os.environ
        env.update(self.env)
        print(cmd)
        subprocess.run(cmd, shell=True, cwd=self.cwd, env=env)


def launch(launch_json: pathlib.Path, index: int = 0, open_file: str = '') -> None:
    src = launch_json.read_text(encoding='utf-8')

    def repl(m):
        key = m.group(1)
        if key.startswith('env:'):
            return os.getenv(key[4:]).replace('\\', '/')
        else:
            if key == 'workspaceFolder':
                return str(launch_json.parent.parent).replace('\\', '/')
            if key == 'workspaceRoot':
                return str(launch_json.parent.parent).replace('\\', '/')
            elif key == 'file':
                return open_file
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
    open_file = ''
    if len(sys.argv) > 2:
        open_file = sys.argv[2]

    current = pathlib.Path('.').absolute()
    while True:
        dir = current / '.vscode'
        if dir.is_dir():
            launch_json = dir / 'launch.json'
            if launch_json.exists():
                launch(launch_json, index, open_file)
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
