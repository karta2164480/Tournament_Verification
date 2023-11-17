import numpy as np
from Team import Team
from simulator import gen_second_half_season_record

def find_first_half_season_champion(teams):
    result = 0
    for i in range(len(teams)):
        team_i_total = teams[i].win + teams[i].lose
        team_i_winrate = teams[i].win / team_i_total if team_i_total != 0 else 0
        result_total = teams[result].win + teams[result].lose
        result_winrate = teams[result].win / result_total if result_total != 0 else 0
        if team_i_winrate > result_winrate:
            result = i
    global first_half_season_record
    first_half_season_record = teams
    return result

def find_playoff_teams(teams, first_half_season_champion):
    second_half_season_record = gen_second_half_season_record(teams)
    second_half_season_champion = 0
    for i in range(len(teams)):
        team_i_total = second_half_season_record[i].win + second_half_season_record[i].lose
        team_i_winrate = second_half_season_record[i].win / team_i_total if team_i_total != 0 else 0
        second_champion_total = second_half_season_record[second_half_season_champion].win + second_half_season_record[second_half_season_champion].lose
        second_champion_winrate = second_half_season_record[second_half_season_champion].win / second_champion_total if second_champion_total != 0 else 0
        if team_i_winrate > second_champion_winrate:
            second_half_season_champion = i

    playoff_teams = np.zeros(len(teams))
    playoff_teams[first_half_season_champion] = 1
    playoff_teams[second_half_season_champion] = 1
    sorted_record = sorted(teams, key=lambda x:(x.win / (x.win + x.lose) if x.win + x.lose != 0 else 0))
    # print(first_half_season_champion)
    # print(second_half_season_champion)
    if first_half_season_champion == second_half_season_champion:
        count = 1
        for i in range(len(sorted_record)):
            if i != first_half_season_champion:
                playoff_teams[i] = 1
                count += 1
                if count == 3:
                    # print(playoff_teams)
                    return playoff_teams
    else:
        count = 2
        for i in range(len(sorted_record)):
            if i != first_half_season_champion and i != second_half_season_champion:
                playoff_teams[i] = 1
                # print(playoff_teams)
                return playoff_teams