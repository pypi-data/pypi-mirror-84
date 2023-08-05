import os
from datetime import datetime
from typing import List, cast

from dfs.models import Game, Player
from dfs.version import get_version

import pickle


class State:
    def __init__(self, league: str, games: List[Game], players: List[Player]):
        self.__league = league
        self.__games = games
        self.__players = players
        self.__version = get_version()
        self.__date = datetime.utcnow()

    def save(self) -> None:
        pickle_dir = self.__get_pickle_dir()
        if not os.path.exists(pickle_dir):
            os.makedirs(pickle_dir)
        with open('%s/%s.pkl' % (pickle_dir, self.__league.lower()), 'wb') as pkl_out:
            pickle.dump(self, pkl_out)

    @staticmethod
    def load(league: str) -> 'State':
        with open('%s/%s.pkl' % (State.__get_pickle_dir(), league.lower()), 'rb') as pkl_in:
            return cast(State, pickle.load(pkl_in))

    @staticmethod
    def __get_pickle_dir() -> str:
        return '%s/%s' % (os.path.join(os.path.expanduser('~'), '.dfs-cache'), get_version())
