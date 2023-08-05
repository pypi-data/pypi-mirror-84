from typing import List

import requests

from dfs.models import Game, Player, PlayerGame, StartStatus, Projection
from dfs.state import State


def __scrape_projections(league: str) -> List[dict]:
    site = 'DraftKings'
    url = 'https://www.rotowire.com/daily/tables/optimizer-soc.php?league=%s&site=%s&projections=&type=main&slate=all' % (
        league.upper(),
        site
    )
    print('Scraping players from %s' % url)
    return requests.get(url).json()


def __scrape_games(league: str) -> List[dict]:
    site = 'DraftKings'
    url = 'https://www.rotowire.com/daily/tables/schedule-soc.php?sport=%s&site=%s&projections=&type=main&slate=all' % (
        league.upper(),
        site
    )
    print('Scraping games from %s' % url)
    return requests.get(url).json()


def __get_games(league: str) -> List[Game]:
    return [
        Game(i + 1, game['home_team'], game['visit_team'], game['date'])
        for i, game in enumerate(__scrape_games(league))
    ]


def scrape(league: str) -> State:
    games: List[Game] = __get_games(league)
    players: List[Player] = []

    for player in __scrape_projections(league):
        positions: List[str] = player['actual_position'].split('/')
        lineup_status = player['lineup_status'].lower()
        team = player['team']
        game = next(g for g in games if g.featured(team))
        players.append(
            Player(
                int(player['id']),
                player['player'],
                positions,
                player['salary'],
                PlayerGame(team, game),
                StartStatus(lineup_status in ['yes', 'exp.'], lineup_status != 'exp.'),
                Projection(
                    float(player['proj_points']),
                    float(player['proj_floor']),
                    float(player['proj_ceiling'])
                )
            )
        )
    return State(
        league,
        games,
        sorted(players, key=lambda x: x.id)
    )
