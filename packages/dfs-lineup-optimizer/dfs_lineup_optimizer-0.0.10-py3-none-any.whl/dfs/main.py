from argparse import ArgumentParser
from typing import List

from dfs.command import Command
from dfs.load.load import Load
from dfs.optimize.optimize import Optimize
from dfs.version import get_version


def main():
    parser = ArgumentParser(prog='dfs', description='DFS Lineup Optimizer v%s' % get_version())
    subparsers = parser.add_subparsers(
        metavar='command',
        dest='command',
        required=True
    )
    commands: List[Command] = [Load(), Optimize()]
    for command in commands:
        command.add_parser(subparsers)
    args = parser.parse_args()
    next(cmd for cmd in commands if cmd.name == args.command).execute(args)


if __name__ == '__main__':
    main()
