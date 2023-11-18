from itertools import combinations
import random
import numpy as np
from Team import Team
from Simulator import simulate

# class node:
#     def __init__(self, home, guest, teams):
#         self.home = home
#         self.guest = guest
#         self.teams = teams
#         self.home_win_child = None
#         self.guest_win_child = None
#         self.draw_child = None
#         self.first_half_season_champion = None

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
    intentional_lose = np.zeros(len(games))
    simulate(0, teams, games, None, intentional_lose)
    for i in range(len(games)):
        if intentional_lose[i] == 1:
            print("Game %d may have teams intentionally lose." % (i + 1))


if __name__ == "__main__":
    main()