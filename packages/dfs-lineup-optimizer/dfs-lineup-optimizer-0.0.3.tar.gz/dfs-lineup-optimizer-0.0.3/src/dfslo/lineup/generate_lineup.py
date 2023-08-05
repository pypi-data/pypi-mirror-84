from typing import Dict, List

import pulp


class LineupGenerator:
    def __init__(self, roster_format: Dict[str, int], flex_position_mapping: Dict[str, List[str]], salary_limit: int,
                 players: List[dict]):
        self.__roster_format = roster_format
        self.__flex_position_mapping = flex_position_mapping
        self.__salary_limit = salary_limit
        self.__players = players

    def generate(self) -> Dict[str, List[int]]:
        flattened_players = self.__flatten_players_to_single_positions()
        linear_problem = pulp.LpProblem('lineup', pulp.LpMaximize)
        player_variables = [
            pulp.LpVariable('p_%s' % i, 0, 1, pulp.LpInteger)
            for i in range(len(flattened_players))
        ]
        self.__apply_constraints(linear_problem, player_variables, flattened_players)
        self.__define_objective_function(linear_problem, player_variables, flattened_players)
        linear_problem.solve()
        return self.__get_lineup_from_player_variables(player_variables, flattened_players)

    def __flatten_players_to_single_positions(self) -> List[dict]:
        flattened_players: List[dict] = []
        for player in self.__players:
            positions = list(player['positions'])
            for flex_position, sub_positions in self.__flex_position_mapping.items():
                if any(p in sub_positions for p in positions):
                    positions.append(flex_position)
            for position in positions:
                flattened_players.append({
                    **dict(player),
                    **{
                        'position': position
                    }
                })
        return flattened_players

    def __apply_constraints(self, linear_problem, player_variables, players: List[dict]) -> None:
        self.__apply_positional_limits_constraint(linear_problem, player_variables, players)
        self.__apply_salary_cap_constraint(linear_problem, player_variables, players)
        self.__apply_only_one_of_each_player_constraint(linear_problem, player_variables, players)
        self.__apply_three_different_teams_constraint(linear_problem, player_variables, players)

    def __apply_positional_limits_constraint(self, linear_problem, player_variables, players):
        positions_matrix = {}
        for position in self.__roster_format:
            positions_matrix[position] = []
            for projection in players:
                positions_matrix[position].append(1 if position == projection['position'] else 0)

        for position, limit in self.__roster_format.items():
            linear_problem += (
                    pulp.lpSum(
                        positions_matrix[position][i] * player_variables[i]
                        for i in range(len(player_variables))
                    ) == limit
            )

    # TODO: implement (use LpVariables http://benalexkeen.com/linear-programming-with-python-and-pulp-part-2/)
    def __apply_three_different_teams_constraint(self, linear_problem, player_variables, players):
        pass

    def __apply_salary_cap_constraint(self, linear_problem, player_variables, players):
        linear_problem += (
                pulp.lpSum(
                    players[i]['salary'] * player_variables[i]
                    for i in range(len(players))
                ) <= self.__salary_limit
        )

    @staticmethod
    def __apply_only_one_of_each_player_constraint(linear_problem, player_variables, players):
        players_matrix = {}
        for player in players:
            players_matrix[player['id']] = []
        for player in players:
            for player_key in players_matrix.keys():
                players_matrix[player_key].append(1 if player['id'] == player_key else 0)
        for player_key in players_matrix.keys():
            linear_problem += (pulp.lpSum(
                players_matrix[player_key][i] * player_variables[i]
                for i in range(len(player_variables))
            ) <= 1)

    @staticmethod
    def __define_objective_function(linear_problem, player_variables, players):
        linear_problem += pulp.lpSum(
            pulp.lpSum(
                players[i]['projection']['average'] * player_variables[i]
                for i in range(len(players))
            )
        )

    @staticmethod
    def __get_lineup_from_player_variables(player_variables, flat_players) -> Dict[str, List[int]]:
        lineup: Dict[str, List[int]] = {}
        for i, player_variable in enumerate(player_variables):
            if round(player_variable.varValue or 0) != 1:
                continue
            flat_player = flat_players[i]
            position = flat_player['position']
            lineup[position] = lineup.get(position, []) + [flat_player['id']]
        return lineup


def generate_lineup(roster_format: dict, flex_position_mapping: dict, salary_limit: int,
                    players: List[dict]) -> Dict[str, List[int]]:
    return LineupGenerator(roster_format, flex_position_mapping, salary_limit, players).generate()
