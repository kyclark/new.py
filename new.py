#!/usr/bin/env python3
"""
Python program to write a Python program
Forked from: https://github.com/kyclark/new.py
"""


import argparse
import configparser
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import NamedTuple


class Args(NamedTuple):
    program: str
    name: str
    email: str
    purpose: str
    overwrite: bool
    write_test: bool


def get_args() -> Args:
    """Get arguments."""

    parser = argparse.ArgumentParser(
        prog="new.py",
        description="Create Python argparse program",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    defaults = get_defaults()
    username = os.getenv("USER") or "Anonymous"
    hostname = os.getenv("HOSTNAME") or "localhost"

    parser.add_argument("program", help="Program name", type=str)

    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default=defaults.get("name", username),
        help="Name for docstring",
    )

    parser.add_argument(
        "-e",
        "--email",
        type=str,
        default=defaults.get("email", f"{username}@{hostname}"),
        help="Email for docstring",
    )

    parser.add_argument(
        "-p",
        "--purpose",
        type=str,
        default=defaults.get("purpose", "Rock the Casbah"),
        help="Purpose for docstring",
    )

    parser.add_argument(
        "-t", "--write_test", help="Create basic test.py", action="store_true"
    )

    parser.add_argument("-f", "--force", help="Overwrite existing", action="store_true")

    args = parser.parse_args()

    args.program = args.program.strip().replace("-", "_")

    if not args.program:
        parser.error(f'Not a usable filename "{args.program}"')

    return Args(
        program=args.program,
        name=args.name,
        email=args.email,
        purpose=args.purpose,
        overwrite=args.force,
        write_test=args.write_test,
    )


def main() -> None:
    """Make a jazz noise here."""

    args = get_args()
    program = args.program

    if Path(program).is_file() and not args.overwrite:
        answer = input(f'"{program}" exists.  Overwrite? [yN] ')
        if not answer.lower().startswith("y"):
            sys.exit("Will not overwrite. Bye!")

    Path(program).write_text(body(args))
    if not sys.platform.startswith("win32"):
        subprocess.run(["chmod", "+x", program])

    if args.write_test:
        test_dir = Path.cwd() / "tests"
        test_dir.mkdir(exist_ok=True)

        basename = "test_" + args.program
        test_file = Path(test_dir) / Path(basename)
        Path(test_file).write_text(text_test(args.program))
        makefile = [".PHONY: test", "", "test:", "\tpython3 -m pytest -xv"]
        Path("Makefile").write_text("\n".join(makefile))

    print(f'Done, see new script "{program}."')


def body(args: Args) -> str:
    """The program template."""

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
    positional: str
    string_arg: str
    int_arg: int
    file: TextIO
    on: bool


def get_args() -> Args:
    \"\"\"Get command-line arguments.\"\"\"

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


def main() -> None:
    \"\"\"Make a jazz noise here.\"\"\"

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


if __name__ == '__main__':
    main()
"""


def text_test(prg) -> str:
    """Template for test.py."""

    tmpl = """import os
from subprocess import getstatusoutput

PRG = './{}'


def test_exists():
    \"\"\"Program exists.\"\"\"

    assert os.path.isfile(PRG)


def test_usage():
    \"\"\"Usage.\"\"\"

    for flag in ['-h', '--help']:
        exitcode, output = getstatusoutput(f'{{PRG}} {{flag}}')
        assert exitcode == 0
        assert output.lower().startswith('usage')


def test_ok():
    \"\"\"OK.\"\"\"

    exitcode, output = getstatusoutput(f'{{PRG}} foo')
    assert exitcode == 0
    assert output.splitlines()[-1] == 'positional = "foo"'
    """

    return tmpl.rstrip().format(prg)


def get_defaults():
    """Get defaults from ~/defaults.ini"""

    rc = Path.home() / "defaults.ini"
    config = configparser.ConfigParser()
    config.read(rc)

    return config["new"]


if __name__ == "__main__":
    main()
