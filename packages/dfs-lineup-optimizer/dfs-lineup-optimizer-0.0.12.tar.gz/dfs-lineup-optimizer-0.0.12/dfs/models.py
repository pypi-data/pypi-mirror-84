from typing import List


class Game:
    def __init__(self, _id: int, home: str, away: str, date: str):
        self.__id = _id
        self.__home = home
        self.__away = away
        self.__date = date

    def featured(self, team: str) -> bool:
        return team in [self.__home, self.__away]

    def opponent_of(self, team: str) -> str:
        return self.__away if team == self.__home else self.__home

    @property
    def id(self) -> int:
        return self.__id

    @property
    def date(self) -> str:
        return self.__date


class StartStatus:
    def __init__(self, is_expected: bool, is_confirmed: bool):
        self.__is_expected = is_expected
        self.__is_confirmed = is_confirmed


class Projection:
    def __init__(self, average: float, floor: float, ceiling: float):
        self.__average = average
        self.__floor = floor
        self.__ceiling = ceiling


class PlayerGame:
    def __init__(self, team: str, game: Game):
        self.__id = game.id
        self.__team = team
        self.__opponent = game.opponent_of(team)
        self.__date = game.date


class Player:
    def __init__(self, _id: int, name: str, positions: List[str], salary: int, player_game: PlayerGame,
                 start_status: StartStatus, projection: Projection):
        self.__id = _id
        self.__name = name
        self.__positions = positions
        self.__salary = salary
        self.__game = player_game
        self.__start_status = start_status
        self.__projection = projection

    @property
    def id(self) -> int:
        return self.__id
