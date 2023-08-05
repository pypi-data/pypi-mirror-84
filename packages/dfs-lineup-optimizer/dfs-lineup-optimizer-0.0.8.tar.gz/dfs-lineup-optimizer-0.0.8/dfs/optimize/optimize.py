from argparse import Namespace

from dfs.command import Command


class Optimize(Command):
    def __init__(self):
        super().__init__('optimize')

    def add_parser(self, subparsers):
        optimize_parser = subparsers.add_parser(self._name, help='Generate an optimal lineup')

    def execute(self, args=Namespace):
        print('optimize: ', args)