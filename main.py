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

def simulate(depth, teams, games, first_half_season_champion, stateDict, remaining_n_games):
    global count
    count += 1

    state = get_state(teams)
    if state in stateDict:
        return stateDict[state], teams

    if depth == len(games) // 2:
        first_half_season_champion = find_one_first_half_season_champion(teams)
    elif depth == len(games):
        return find_all_playoff_teams(teams, first_half_season_champion), teams
    # elif IsRankFixed(teams, remaining_n_games):
    #     total_remain_games = len(games) - depth # not sure
    #     return find_all_playoff_teams(teams, first_half_season_champion) * (3 ** total_remain_games), teams

    home = games[depth][0]
    guest = games[depth][1]
    remaining_n_games[home] -= 1
    remaining_n_games[guest] -= 1
    # home team wins
    playoff_chances_hw, hw_final_state = simulate(depth + 1, gen_new_record(teams, home, guest), games, first_half_season_champion, stateDict, deepcopy(remaining_n_games))

    # guest team wins
    playoff_chances_gw, gw_final_state = simulate(depth + 1, gen_new_record(teams, guest, home), games, first_half_season_champion, stateDict, deepcopy(remaining_n_games))

    # draw
    playoff_chances_d, d_final_state = simulate(depth + 1, gen_new_record_draw(teams, home, guest), games, first_half_season_champion, stateDict, deepcopy(remaining_n_games))

    # print(playoff_chances_hw)
    # print(playoff_chances_gw)
    # print(playoff_chances_d)
    final_state = hw_final_state
    if (playoff_chances_gw[home] > playoff_chances_hw[home] and first_half_season_champion != home) \
    or ( playoff_chances_hw[guest] > playoff_chances_gw[guest] and first_half_season_champion != guest):
        if playoff_chances_gw[home] > playoff_chances_hw[home]:
            final_state = gw_final_state
        if playoff_chances_hw[guest] > playoff_chances_gw[guest]:
            final_state = hw_final_state

        if depth >= 22: # for debug
            print('---')
            print(f'state = {state}')
            print(f'second half record = {get_state(get_second_half_season_record(teams))}')
            if playoff_chances_gw[home] > playoff_chances_hw[home]:
                print(f'game {depth+1} ({home},{guest}), team {home} may intentionally lose')
                print(f'{guest} win chances = {int(playoff_chances_gw[home])}, {home} win chanes = {int(playoff_chances_hw[home])}')
            if playoff_chances_hw[guest] > playoff_chances_gw[guest]:
                print(f'game {depth+1} ({home},{guest}), team {guest} may intentionally lose')
                print(f'{home} win chances = {int(playoff_chances_hw[guest])}, {guest} win chances = {int(playoff_chances_gw[guest])}')
            print(f'state if {guest} win = {get_state(gen_new_record(teams, guest, home))}')
            print(f's2 record if {guest} win = {get_state(get_second_half_season_record(gen_new_record(teams, guest, home)))}')
            print(f'state if {home} win = {get_state(gen_new_record(teams, home, guest))}')
            print(f's2 record if {home} win = {get_state(get_second_half_season_record(gen_new_record(teams, home, guest)))}')

            
            print(f'schedule = {games[depth:]}')
            print(f's1 champion = {first_half_season_champion}')
            print(f'one of final state = {get_state(final_state)}, playoff teams = {find_all_playoff_teams(final_state, first_half_season_champion)}')
            print(f'one of final s2 record = {get_state(get_second_half_season_record(final_state))}, playoff teams = {get_all_second_half_champions(final_state)}')
            print(f'one of s2 champions = {get_all_second_half_champions(final_state)}')
            print('---')

    stateDict[state] = playoff_chances_hw + playoff_chances_gw + playoff_chances_d

    return playoff_chances_hw + playoff_chances_gw + playoff_chances_d, final_state

count = 0
def main():
    n_teams = 4#int(input("Input the number of teams: "))
    n_games = 2#int(input("Input the number of games that each team plays against another in a half-season: "))
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