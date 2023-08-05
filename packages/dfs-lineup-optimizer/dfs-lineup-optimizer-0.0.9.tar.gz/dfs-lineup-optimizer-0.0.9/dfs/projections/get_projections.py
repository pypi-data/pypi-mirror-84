from typing import List, Tuple

import requests


def __scrape_projections(league: str) -> List[dict]:
    site = 'DraftKings'
    return requests.get(
        'https://www.rotowire.com/daily/tables/optimizer-soc.php?league=%s&site=%s&projections=&type=main&slate=all' % (
            league,
            site
        )
    ).json()


def __scrape_games(league: str) -> List[dict]:
    site = 'DraftKings'
    return requests.get(
        'https://www.rotowire.com/daily/tables/schedule-soc.php?sport=%s&site=%s&projections=&type=main&slate=all' % (
            league,
            site
        )
    ).json()


def __get_games(league: str) -> List[dict]:
    return [
        {
            'id': i + 1,
            'home': game['home_team'],
            'away': game['visit_team'],
            'date': game['date']
        } for i, game in enumerate(__scrape_games(league))
    ]


def get_projections(league: str) -> dict:
    games: List[dict] = __get_games(league)
    players: List[dict] = []

    for player in __scrape_projections(league):
        positions: List[str] = player['actual_position'].split('/')
        lineup_status = player['lineup_status'].lower()
        team = player['team']
        game = next((g for g in games if team in [g['home'], g['away']]), None)
        opponent = game['away'] if team == game['home'] else game['home']
        players.append({
            'id': int(player['id']),
            'name': player['player'],
            'positions': positions,
            'salary': player['salary'],
            'game': {
                'id': game['id'],
                'team': team,
                'opponent': opponent
            },
            'status': {
                'is_expected': lineup_status in ['yes', 'exp.'],
                'is_confirmed': lineup_status != 'exp.'
            },
            'projection': {
                'average': float(player['proj_points']),
                'floor': float(player['proj_floor']),
                'ceiling': float(player['proj_ceiling'])
            }
        })
    return {
        'games': games,
        'players': sorted(players, key=lambda x: x['id'])
    }
