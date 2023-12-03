from itertools import combinations
import random
import numpy as np
from Team import Team
from RecordGenerator import *
from RankingCalculator import *

def create_schedule(n_teams, n_games):
    games = list(combinations(range(n_teams), 2)) * n_games
    random.shuffle(games)
    return games

def create_teams(n):
    teams = []
    for i in range(n):
        teams.append(Team(i))
    return np.array(teams)

def get_state(teams):
    state = ""
    for team in teams:
        state += team.get_key()
    return state

def simulate(depth, teams, games, first_half_season_champions, stateDict, remaining_n_games):
    global count
    count += 1

    state = get_state(teams)
    if state in stateDict:
        return stateDict[state]

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
    if remaining_n_games[home] == 0 or remaining_n_games[guest] == 0:
        print(remaining_n_games, games)
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
        print("When records = %s\nGame %d may have teams intentionally lose." % (state, depth + 1))

    stateDict[state] = playoff_chances_hw + playoff_chances_gw + playoff_chances_d

    return playoff_chances_hw + playoff_chances_gw + playoff_chances_d

count = 0
def main():
    n_teams = int(input("Input the number of teams: "))
    n_games = int(input("Input the number of games that each team plays against another in a half-season: "))
    first_half_season = create_schedule(n_teams, n_games)
    second_half_season = create_schedule(n_teams, n_games)
    games = first_half_season + second_half_season
    teams = create_teams(n_teams)
    # intentional_lose = np.zeros(len(games))
    stateDict = {}
    remaining_n_games = np.full(n_teams, n_games * (n_teams - 1))

    gen_first_half_season_record(teams, n_games)
    # first_half_season_champions = find_one_first_half_season_champion(teams)
    # first_half_season_champions = find_all_first_half_season_champion(teams)
    # simulate(0, teams, games, None, intentional_lose, stateDict)
    simulate(len(games) // 2, teams, games, None, stateDict, remaining_n_games)
    print(f'node count = {count}')
    # for i in range(len(games)):
    #     if intentional_lose[i] == 1:
    #         print("Game %d may have teams intentionally lose." % (i + 1))


if __name__ == "__main__":
    main()