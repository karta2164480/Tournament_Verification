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


def gen_first_half_season_record(teams, n_games):
    n = len(teams)
    for i in range(n - 1):
        for j in range(i + 1, n):
            n_wins = randint(0, n_games)
            n_loses = randint(0, n_games - n_wins)
            teams[i].win += n_wins
            teams[i].lose += n_loses
            teams[i].draw += n_games - n_wins - n_loses
            teams[j].win += n_loses
            teams[j].lose += n_wins
            teams[j].draw += n_games - n_wins - n_loses

    print("first half season records:")
    for team in teams:
        print("team %d: %d %d %d" % (team.id, team.win, team.lose, team.draw))
    return