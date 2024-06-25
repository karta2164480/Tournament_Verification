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
            n_draw = randint(0, n_games)
            n_wins = randint(0, n_games - n_draw)
            n_loses = n_games - n_draw - n_wins
            teams[i].win += n_wins
            teams[i].lose += n_loses
            teams[i].draw += n_draw
            teams[j].win += n_loses
            teams[j].lose += n_wins
            teams[j].draw += n_draw

    print("first half season records:")
    for team in teams:
        print("team %d: %d %d %d" % (team.id, team.win, team.lose, team.draw), flush=True)
    return

def assign_record(teams, record):
    for i in range(len(teams)):
        teams[i].win += record[i][0]
        teams[i].lose += record[i][1]
        teams[i].draw += record[i][2]



# assign some game results for the second half season 
def gen_some_second_half_season_record(teams, num_game_assigned_second, games, remaining_n_games):
    # print(games)
    second_half_season_start = len(games) // 2
    for i in range(num_game_assigned_second):
        first_team = games[i+second_half_season_start][0]
        second_team = games[i+second_half_season_start][1]
        remaining_n_games[first_team] -= 1
        remaining_n_games[second_team] -= 1
        winner = randint(0, 2)
        if winner == 2:
            teams[first_team].draw += 1
            teams[second_team].draw += 1
        elif winner == 1:
            teams[first_team].lose += 1
            teams[second_team].win += 1
        elif winner == 0:
            teams[first_team].win += 1
            teams[second_team].lose += 1
        else:
            raise Exception("winner should be 0, 1, or 2")

    return
