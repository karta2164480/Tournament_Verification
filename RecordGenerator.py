from copy import deepcopy
import numpy as np

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
