from argparse import ArgumentParser
from typing import List

from src.dfs.command import Command
from src.dfs.load.load import Load
from src.dfs.optimize.optimize import Optimize


def main():
    parser = ArgumentParser(description='Generate an optimal DFS lineup')
    subparsers = parser.add_subparsers(metavar='command', dest='command', required=True)
    commands: List[Command] = [Load(), Optimize()]
    map(lambda cmd: cmd.add_parser(subparsers), commands)
    args = parser.parse_args()
    next(cmd for cmd in commands if cmd.name == args.command).execute()


if __name__ == '__main__':
    main()
