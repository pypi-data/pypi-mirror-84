from argparse import Namespace

from dfs.command import Command


class Load(Command):

    def __init__(self):
        super().__init__('load')

    def add_parser(self, subparsers):
        load_parser = subparsers.add_parser(self._name, help='Load projections and schedules for a league')
        load_parser.add_argument('league', metavar='league', type=str,
                                 help='League abbreviation to load data for (eg. NFL, NBA, EPL)')

    def execute(self, args=Namespace):
        print('load: ', args)