import json
from unittest import TestCase
from os import path
from pathlib import Path

from src.dfslo.lineup.generate_lineup import generate_lineup


class GenerateLineupTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open(path.join(Path(__file__).parent.resolve(), 'test_input.json')) as test_input_json:
            cls.base_input = json.loads(test_input_json.read())

    def test_base_case(self):
        lineup = generate_lineup(self.base_input)
        with self.subTest('position limits'):
            for position, limit in self.base_input['roster_format'].items():
                with self.subTest(position=position, limit=limit):
                    self.assertEqual(limit, len(lineup[position]))

        with self.subTest('salary limit'):
            total_salary = 0
            salary_limit = self.base_input['salary_limit']
            for player_ids in lineup.values():
                for player_id in player_ids:
                    total_salary += next(
                        (p for p in self.base_input['players'] if p['id'] == player_id),
                        None
                    )['salary']
            self.assertLessEqual(total_salary, salary_limit)

        with self.subTest('one of each player'):
            player_ids = []
            for x in lineup.values():
                player_ids.extend(x)
            unique_player_ids = list(set(player_ids))
            self.assertEqual(len(player_ids), len(unique_player_ids))

        # with self.subTest('at least three different teams'):
        #     teams = []
        #     for players in lineup.values():
        #         teams.extend([x['team'] for x in players])
        #     unique_teams = list(set(teams))
        #     self.assertGreaterEqual(len(unique_teams), 3)
