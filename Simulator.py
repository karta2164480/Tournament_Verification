from copy import deepcopy
import numpy as np
from Team import Team
from RankingCalculator import *
from RecordGenerator import *




def simulate(depth, teams, games, first_half_season_champion, intentional_lose):
    if depth == len(games) // 2:
        first_half_season_champion = find_first_half_season_champion(teams)
    elif depth == len(games):
        return find_playoff_teams(teams, first_half_season_champion)

    home = games[depth][0]
    guest = games[depth][1]
    # home team wins
    playoff_chances_hw = simulate(depth + 1, gen_new_record(teams, home, guest), games, first_half_season_champion, intentional_lose)

    # guest team wins
    playoff_chances_gw = simulate(depth + 1, gen_new_record(teams, guest, home), games, first_half_season_champion, intentional_lose)

    # draw
    playoff_chances_d = simulate(depth + 1, gen_new_record_draw(teams, home, guest), games, first_half_season_champion, intentional_lose)

    # print(playoff_chances_hw)
    # print(playoff_chances_gw)
    # print(playoff_chances_d)
    if playoff_chances_gw[home] > playoff_chances_hw[home] or playoff_chances_hw[guest] > playoff_chances_gw[guest]:
        # global intentional_lose
        intentional_lose[depth] = 1
    # else:
    #     print("game %d is ok." % depth)

    return playoff_chances_hw + playoff_chances_gw + playoff_chances_d