import numpy as np
from Team import Team
from RecordGenerator import *

first_half_season_record = np.array([])

def winrate(team):
    team_total = team.win + team.lose
    return team.win / team_total if team_total != 0 else 0

def find_one_first_half_season_champion(teams):
    result = 0
    for i in range(len(teams)):
        if winrate(teams[i]) > winrate(teams[result]):
            result = i
    global first_half_season_record
    first_half_season_record = teams
    return result

def get_first_half_season_record():
    return first_half_season_record

def get_second_half_season_record(teams):
    result = deepcopy(teams)
    for i in range(len(teams)):
        result[i].win -= first_half_season_record[i].win
        result[i].lose -= first_half_season_record[i].lose
        result[i].draw -= first_half_season_record[i].draw
    return result

def get_all_second_half_champions(teams):
    second_half_season_record = get_second_half_season_record(teams)
    champions = []
    champion_winrate = -1
    for i in range(len(teams)):
        team_i_winrate = winrate(second_half_season_record[i])
        if team_i_winrate > champion_winrate:
            champion_winrate = team_i_winrate
            champions = [i]
        elif team_i_winrate == champion_winrate:
            champions.append(i)

    return champions

def find_one_playoff_teams(teams, first_half_season_champion):
    second_half_season_record = get_second_half_season_record(teams)
    second_half_season_champion = 0
    for i in range(len(teams)):
        if winrate(second_half_season_record[i]) > winrate(second_half_season_record[second_half_season_champion]):
            second_half_season_champion = i

    playoff_teams = np.zeros(len(teams))
    playoff_teams[first_half_season_champion] = 1
    playoff_teams[second_half_season_champion] = 1
    sorted_record = sorted(teams, key=lambda x: -winrate(x))
    if first_half_season_champion == second_half_season_champion:
        count = 1
        for team in sorted_record:
            if team.id != first_half_season_champion:
                playoff_teams[team.id] = 1
                count += 1
                if count == 3:
                    return playoff_teams
    else:
        count = 2
        for team in sorted_record:
            if team.id != first_half_season_champion and team.id != second_half_season_champion:
                playoff_teams[team.id] = 1
                return playoff_teams

def find_all_playoff_teams(teams, first_half_season_champion):
    second_half_season_champions = get_all_second_half_champions(teams)

    playoff_teams = np.zeros(len(teams))
    sorted_record = sorted(teams, key=lambda x: -winrate(x))

    for second_half_season_champion in second_half_season_champions:
        playoff_teams[first_half_season_champion] = 1
        playoff_teams[second_half_season_champion] = 1
        if first_half_season_champion == second_half_season_champion:
            count = 1
            for team in sorted_record:
                if team.id != first_half_season_champion:
                    playoff_teams[team.id] = 1
                    count += 1
                    if count == 3:
                        break
        else:
            count = 2
            for team in sorted_record:
                if team.id != first_half_season_champion and team.id != second_half_season_champion:
                    playoff_teams[team.id] = 1
                    break
    return playoff_teams

def IsRankFixed(teams, remaining_n_games):
    n = len(teams)

    second_half_champions = get_all_second_half_champions(teams)
    for champion in second_half_champions:
        champion_record = deepcopy(teams[champion])
        champion_record.lose += remaining_n_games[champion]
        for i in range(n):
            if i == champion:
                continue
            team_i_record = deepcopy(teams[i])
            team_i_record.win += remaining_n_games[i]
            if i in second_half_champions:
                if winrate(champion_record) < winrate(team_i_record):
                    return False
            else:
                if winrate(champion_record) <= winrate(team_i_record):
                    return False

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