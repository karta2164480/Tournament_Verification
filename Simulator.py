import numpy as np
from Team import Team
from RankingCalculator import *
from RecordGenerator import *

def IsRankFixed(teams, remaining_n_games):
    n = len(teams)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if winrate(teams[i]) > winrate(teams[j]):
                team_i_record = deepcopy(teams[i])
                team_i_record.lose += remaining_n_games[i]
                team_j_record = deepcopy(teams[j])
                team_j_record.win += remaining_n_games[j]
                if winrate(team_i_record) <= winrate(team_j_record):
                    return False
            elif winrate(teams[i]) < winrate(teams[j]):
                team_i_record = deepcopy(teams[i])
                team_i_record.win += remaining_n_games[i]
                team_j_record = deepcopy(teams[j])
                team_j_record.lose += remaining_n_games[j]
                if winrate(team_i_record) >= winrate(team_j_record):
                    return False
            else:
                if remaining_n_games[i] > 0 or remaining_n_games[j] > 0:
                    return False

    return True

def simulate(depth, teams, games, first_half_season_champions, stateDict, remaining_n_games):
    key = ""
    for team in teams:
        key += team.get_key()

    if key in stateDict:
        return stateDict[key]

    if depth == len(games) // 2:
        first_half_season_champions = find_one_first_half_season_champion(teams)
        # first_half_season_champions = find_all_first_half_season_champion(teams)
    elif depth == len(games):
        return find_one_playoff_teams(teams, first_half_season_champions)
        # return find_all_playoff_teams(teams, first_half_season_champions)
    elif IsRankFixed(teams, remaining_n_games):
        return find_one_playoff_teams(teams, first_half_season_champions)

    home = games[depth][0]
    guest = games[depth][1]
    remaining_n_games[home] -= 1
    remaining_n_games[guest] -= 1
    # home team wins
    playoff_chances_hw = simulate(depth + 1, gen_new_record(teams, home, guest), games, first_half_season_champions, stateDict, deepcopy(remaining_n_games))

    # guest team wins
    playoff_chances_gw = simulate(depth + 1, gen_new_record(teams, guest, home), games, first_half_season_champions, stateDict, deepcopy(remaining_n_games))

    # draw
    playoff_chances_d = simulate(depth + 1, gen_new_record_draw(teams, home, guest), games, first_half_season_champions, stateDict, deepcopy(remaining_n_games))

    # print(playoff_chances_hw)
    # print(playoff_chances_gw)
    # print(playoff_chances_d)
    if playoff_chances_gw[home] > playoff_chances_hw[home] or playoff_chances_hw[guest] > playoff_chances_gw[guest]:
        print("When records = %s\nGame %d may have teams intentionally lose." % (key, depth + 1))

    stateDict[key] = playoff_chances_hw + playoff_chances_gw + playoff_chances_d

    return playoff_chances_hw + playoff_chances_gw + playoff_chances_d