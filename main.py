from itertools import combinations
import random
import numpy as np
from Team import Team
from Simulator import simulate
from RecordGenerator import gen_first_half_season_record
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

def main():
    n_teams = int(input("Input the number of teams: "))
    n_games = int(input("Input the number of games that each team plays against another in a half-season: "))
    first_half_season = create_schedule(n_teams, n_games)
    second_half_season = create_schedule(n_teams, n_games)
    games = first_half_season + second_half_season
    teams = create_teams(n_teams)
    # intentional_lose = np.zeros(len(games))
    stateDict = {}
    remaining_n_games = np.full(n_teams, n_games)

    gen_first_half_season_record(teams, n_games)
    # first_half_season_champions = find_one_first_half_season_champion(teams)
    # first_half_season_champions = find_all_first_half_season_champion(teams)
    # simulate(0, teams, games, None, intentional_lose, stateDict)
    simulate(len(games) // 2, teams, games, None, stateDict, remaining_n_games)
    # for i in range(len(games)):
    #     if intentional_lose[i] == 1:
    #         print("Game %d may have teams intentionally lose." % (i + 1))


if __name__ == "__main__":
    main()