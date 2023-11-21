from copy import deepcopy
import numpy as np
from random import randint

def gen_new_record(teams, winner, loser):
    new_teams = deepcopy(teams)
    new_teams[winner].win += 1
    new_teams[loser].lose += 1
    return new_teams

def gen_new_record_draw(teams, team1, team2):
    new_teams = deepcopy(teams)
    new_teams[team1].draw += 1
    new_teams[team2].draw += 1
    return new_teams

def gen_second_half_season_record(teams, first_half_season_record):
    result = deepcopy(teams)
    for i in range(len(teams)):
        result[i].win -= first_half_season_record[i].win
        result[i].lose -= first_half_season_record[i].lose
        result[i].draw -= first_half_season_record[i].draw
    return result

def gen_first_half_season_record(teams, n_games):
    n = len(teams)
    for i in range(n):
        remaining_games = n_games * (n - i - 1)
        temp = randint(0, remaining_games)
        teams[i].win += temp
        teams[i].lose += randint(0, remaining_games - temp)
        teams[i].draw = n_games * (n - 1) - teams[i].win - teams[i].lose

        remaining_wins = teams[i].win
        remaining_loses = teams[i].lose
        for j in range(i + 1, n - 1):
            n_wins = randint(0, min(remaining_loses, n_games))
            teams[j].win += n_wins
            remaining_loses -= n_wins
            n_loses = randint(0, min(remaining_wins, n_games - n_wins))
            teams[j].lose += n_loses
            remaining_wins -= n_loses
        teams[n - 1].win += remaining_loses
        teams[n - 1].lose += remaining_wins
    return