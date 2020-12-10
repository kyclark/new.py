#!/usr/bin/env python3
"""
Author : Ken Youens-Clark <kyclark@gmail.com>
Purpose: Python program to write a Python program
"""

import argparse
import os
import platform
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from typing import NamedTuple, Optional, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    program: str
    name: str
    email: str
    purpose: str
    overwrite: bool
    write_test: bool


# --------------------------------------------------
def get_args() -> Args:
    """ Get arguments """

    parser = argparse.ArgumentParser(
        prog='new.py',
        description='Create Python argparse program',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    rc_file = os.path.join(str(Path.home()), '.new.py')
    defaults = get_defaults(open(rc_file) if os.path.isfile(rc_file) else None)
    username = os.getenv('USER') or 'Anonymous'
    hostname = os.getenv('HOSTNAME') or 'localhost'

    parser.add_argument('program', help='Program name', type=str)

    parser.add_argument('-n',
                        '--name',
                        type=str,
                        default=defaults.get('name', username),
                        help='Name for docstring')

    parser.add_argument('-e',
                        '--email',
                        type=str,
                        default=defaults.get('email',
                                             f'{username}@{hostname}'),
                        help='Email for docstring')

    parser.add_argument('-p',
                        '--purpose',
                        type=str,
                        default=defaults.get('purpose', 'Rock the Casbah'),
                        help='Purpose for docstring')

    parser.add_argument('-t',
                        '--write_test',
                        help='Create basic test.py',
                        action='store_true')

    parser.add_argument('-f',
                        '--force',
                        help='Overwrite existing',
                        action='store_true')

    args = parser.parse_args()

    args.program = args.program.strip().replace('-', '_')

    if not args.program:
        parser.error(f'Not a usable filename "{args.program}"')

    return Args(program=args.program,
                name=args.name,
                email=args.email,
                purpose=args.purpose,
                overwrite=args.force,
                write_test=args.write_test)


# --------------------------------------------------
def main() -> None:
    """ Make a jazz noise here """

    args = get_args()
    program = args.program

    if os.path.isfile(program) and not args.overwrite:
        answer = input(f'"{program}" exists.  Overwrite? [yN] ')
        if not answer.lower().startswith('y'):
            sys.exit('Will not overwrite. Bye!')

    print(body(args), file=open(program, 'wt'), end='')

    if platform.system() != 'Windows':
        subprocess.run(['chmod', '+x', program], check=True)

    if args.write_test:
        test_dir = os.path.join(os.getcwd(), 'tests')
        if not os.path.isdir(test_dir):
            os.makedirs(test_dir)

        basename = os.path.splitext(args.program)[0] + '_test.py'
        test_file = os.path.join(test_dir, basename)
        if os.path.isfile(test_file):
            print(f'Will not overwrite "{test_file}"!')
        else:
            print(text_test(args.program), file=open(test_file, 'wt'))

        makefile_text = [
            '.PHONY: test', '', 'test:',
            '\tpython3 -m pytest -xv --flake8 --pylint'
        ]
        makefile = 'Makefile'
        if os.path.isfile(makefile):
            print(f'Will not overwrite "{makefile}"!')
        else:
            print('\n'.join(makefile_text), file=open('Makefile', 'wt'))

    print(f'Done, see new script "{program}".')


# --------------------------------------------------
def body(args: Args) -> str:
    """ The program template """

    today = str(date.today())

    return f"""#!/usr/bin/env python3
\"\"\"
Author : {args.name}{' <' + args.email + '>' if args.email else ''}
Date   : {today}
Purpose: {args.purpose}
\"\"\"

import argparse
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    \"\"\" Command-line arguments \"\"\"
    positional: str
    string_arg: str
    int_arg: int
    file: TextIO
    on: bool


# --------------------------------------------------
def get_args() -> Args:
    \"\"\" Get command-line arguments \"\"\"

    parser = argparse.ArgumentParser(
        description='{args.purpose}',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('positional',
                        metavar='str',
                        help='A positional argument')

    parser.add_argument('-a',
                        '--arg',
                        help='A named string argument',
                        metavar='str',
                        type=str,
                        default='')

    parser.add_argument('-i',
                        '--int',
                        help='A named integer argument',
                        metavar='int',
                        type=int,
                        default=0)

    parser.add_argument('-f',
                        '--file',
                        help='A readable file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        default=None)

    parser.add_argument('-o',
                        '--on',
                        help='A boolean flag',
                        action='store_true')

    args = parser.parse_args()

    return Args(args.positional, args.arg, args.int, args.file, args.on)


# --------------------------------------------------
def main() -> None:
    \"\"\" Make a jazz noise here \"\"\"

    args = get_args()
    str_arg = args.string_arg
    int_arg = args.int_arg
    file_arg = args.file
    flag_arg = args.on
    pos_arg = args.positional

    print(f'str_arg = "{{str_arg}}"')
    print(f'int_arg = "{{int_arg}}"')
    print('file_arg = "{{}}"'.format(file_arg.name if file_arg else ''))
    print(f'flag_arg = "{{flag_arg}}"')
    print(f'positional = "{{pos_arg}}"')


# --------------------------------------------------
if __name__ == '__main__':
    main()
"""


# --------------------------------------------------
def text_test(prg) -> str:
    """ Template for test.py """

    tmpl = """\
\"\"\" Tests \"\"\"

import os
from subprocess import getstatusoutput

PRG = './{}'


# --------------------------------------------------
def test_exists():
    \"\"\" Program exists \"\"\"

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage():
    \"\"\" Usage \"\"\"

    for flag in ['-h', '--help']:
        retval, out = getstatusoutput(f'{{PRG}} {{flag}}')
        assert retval == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_ok():
    \"\"\" OK \"\"\"

    retval, out = getstatusoutput(f'{{PRG}} foo')
    assert retval == 0
    assert out.splitlines()[-1] == 'positional = "foo"'
    """

    return tmpl.rstrip().format(prg)


# --------------------------------------------------
def get_defaults(file_handle: Optional[TextIO]):
    """ Get defaults from ~/.new.py """

    defaults = {}
    if file_handle:
        for line in file_handle:
            match = re.match('([^=]+)=([^=]+)', line)
            if match:
                key, val = map(str.strip, match.groups())
                if key and val:
                    defaults[key] = val

    return defaults


# --------------------------------------------------
if __name__ == '__main__':
    main()
