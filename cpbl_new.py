from itertools import combinations
import random
import numpy as np
from Team import Team
from RecordGenerator import *
from RankingCalculator import *
import time
import sys
import json
import math 

# with open('win_lose_2017.json', 'r', encoding='utf-8') as file:
#     win_lose_dict_2017 = json.load(file)

year = int(sys.argv[4])

with open(f'win_lose_{year}_re.json', 'r', encoding='utf-8') as file:
    win_lose_dict_2017_re = json.load(file)

def create_schedule(n_teams, n_games):
    games = list(combinations(range(n_teams), 2)) * n_games
    random.shuffle(games)
    return games

def assign_schedule(path):
    schedule = []
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()  # 分割行並去除空白
            if len(parts) == 2:
                schedule.append((int(parts[0]), int(parts[1])))

    print(schedule)
    return schedule

def assign_win_lose(teams, game_sno):
    for i in range(len(teams)):
        # teams[i].win = win_lose_dict_2017[str(game_sno)][i][0]
        # teams[i].lose = win_lose_dict_2017[str(game_sno)][i][1]
        # teams[i].draw = win_lose_dict_2017[str(game_sno)][i][2]
        teams[i].win = win_lose_dict_2017_re[game_sno-1][i][0]
        teams[i].lose = win_lose_dict_2017_re[game_sno-1][i][1]
        teams[i].draw = win_lose_dict_2017_re[game_sno-1][i][2] 

def neighbor_schedule(games, num_game_assigned_second, most_loss_game):
    randomRate = 0.5
    dice = np.random.rand()
    print(most_loss_game)
    if dice > randomRate:
        print("choose most loss game")
        new_games = games.copy()
        i = random.sample(range(len(games)-num_game_assigned_second), 1)[0]
        i += num_game_assigned_second
        j = most_loss_game[1] - len(games)        
        while i == j :
            i =  random.sample(range(len(games)-num_game_assigned_second), 1)[0]
            i += num_game_assigned_second
        new_games[i], new_games[j] = new_games[j], new_games[i]
        return new_games    
    else:
        new_games = games.copy()
        i, j = random.sample(range(len(games)-num_game_assigned_second), 2)
        i += num_game_assigned_second
        j += num_game_assigned_second
        new_games[i], new_games[j] = new_games[j], new_games[i]
        return new_games

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

def find_most_loss_game(loss_list):
    most_loss = 0
    most_loss_game = None
    for i in range(len(loss_list)):
        if loss_list[i][0] > most_loss:
            most_loss = loss_list[i][0]
            most_loss_game = loss_list[i][1]

    return (most_loss, most_loss_game)


def simulate(depth, teams, games, first_half_season_champion, first_half_season_record, stateDict, remaining_n_games, weights = [1, 1, 1]):
    global count
    count += 1

    state = get_state(teams)
    if state in stateDict:
        return stateDict[state][0], teams, stateDict[state][1], stateDict[state][2]

    if depth == len(games) // 2:
        first_half_season_champion, first_half_season_record = find_one_first_half_season_champion_n_record(teams)
    elif depth == len(games):
        return find_all_playoff_teams(teams, first_half_season_champion, first_half_season_record), teams, 0, (0, None)
    # elif IsRankFixed(teams, remaining_n_games):
    #     total_remain_games = len(games) - depth - 1
    #     return find_all_playoff_teams(teams, first_half_season_champion) * (3 ** total_remain_games), teams

    home = games[depth][0]
    guest = games[depth][1]
    remaining_n_games[home] -= 1
    remaining_n_games[guest] -= 1
    # home team wins
    playoff_chances_hw, hw_final_state, hw_loser_benefit, hw_most_loss = simulate(depth + 1, gen_new_record(teams, home, guest), games, first_half_season_champion, first_half_season_record, stateDict, deepcopy(remaining_n_games), weights)

    # guest team wins
    playoff_chances_gw, gw_final_state, gw_loser_benefit, gw_most_loss = simulate(depth + 1, gen_new_record(teams, guest, home), games, first_half_season_champion, first_half_season_record, stateDict, deepcopy(remaining_n_games), weights)

    # draw
    playoff_chances_d, d_final_state, d_loser_benefit, d_most_loss = simulate(depth + 1, gen_new_record_draw(teams, home, guest), games, first_half_season_champion, first_half_season_record, stateDict, deepcopy(remaining_n_games), weights)

    playoff_chances_hw = np.array(playoff_chances_hw) * weights[0]
    playoff_chances_gw = np.array(playoff_chances_gw) * weights[1]
    playoff_chances_d = np.array(playoff_chances_d) * weights[2]

    playoff_chances_diff = playoff_chances_hw - playoff_chances_gw
    home_gain = playoff_chances_diff[home]
    guest_gain = -playoff_chances_diff[guest]

    # print(home_gain, guest_gain)
    loser_benefit = 0
    loser_benefit_gain = 0

    if(sys.argv[1] == 'weight'):
        loser_benefit = (hw_loser_benefit + gw_loser_benefit + d_loser_benefit)/3
        if playoff_chances_gw[home] > playoff_chances_hw[home] or playoff_chances_hw[guest] > playoff_chances_gw[guest]:
            loser_benefit_gain = 1
            loser_benefit += loser_benefit_gain
    
    elif(sys.argv[1] == 'slope'):
        loser_benefit = hw_loser_benefit + gw_loser_benefit + d_loser_benefit

        loser_benefit_gain = 0
        if home_gain < 0:
            loser_benefit_gain += -home_gain
        if guest_gain < 0:
            loser_benefit_gain += -guest_gain
        
        loser_benefit += loser_benefit_gain
    elif(sys.argv[1] == 'mix'):
        loser_benefit = (hw_loser_benefit + gw_loser_benefit + d_loser_benefit)/3

        loser_benefit_gain = 0
        if home_gain < 0:
            loser_benefit_gain += -home_gain
        if guest_gain < 0:
            loser_benefit_gain += -guest_gain
        
        loser_benefit += loser_benefit_gain
    else:
        raise Exception("No mode set")
    # print(playoff_chances_hw)
    # print(playoff_chances_gw)
    # print(playoff_chances_d)

    most_loss = find_most_loss_game([(loser_benefit_gain, depth), hw_most_loss, gw_most_loss, d_most_loss])

    final_state = hw_final_state
    if (playoff_chances_gw[home] > playoff_chances_hw[home] and first_half_season_champion != home) \
    or ( playoff_chances_hw[guest] > playoff_chances_gw[guest] and first_half_season_champion != guest):
        
        
        if playoff_chances_gw[home] > playoff_chances_hw[home]:
            final_state = gw_final_state
        if playoff_chances_hw[guest] > playoff_chances_gw[guest]:
            final_state = hw_final_state

        # if depth >= 35: # for debug
        #     print('---')
        #     print(f'state =              {state}')
        #     print(f'second half record = {get_state(get_second_half_season_record(teams, first_half_season_record))}')
        #     if playoff_chances_gw[home] > playoff_chances_hw[home]:
        #         print(f'game {depth+1} ({home},{guest}), team {home} may intentionally lose')
        #         print(f'{guest} win chances = {round(playoff_chances_gw[home], 2)}, {home} win chanes = {round(playoff_chances_hw[home], 2)}')
        #     if playoff_chances_hw[guest] > playoff_chances_gw[guest]:
        #         print(f'game {depth+1} ({home},{guest}), team {guest} may intentionally lose')
        #         print(f'{home} win chances = {round(playoff_chances_hw[guest], 2)}, {guest} win chances = {round(playoff_chances_gw[guest], 2)}')
        #     print(f'state if {guest} win =     {get_state(gen_new_record(teams, guest, home))}')
        #     print(f's2 record if {guest} win = {get_state(get_second_half_season_record(gen_new_record(teams, guest, home), first_half_season_record))}')
        #     print(f'state if {home} win =     {get_state(gen_new_record(teams, home, guest))}')
        #     print(f's2 record if {home} win = {get_state(get_second_half_season_record(gen_new_record(teams, home, guest), first_half_season_record))}')

            
        #     print(f'schedule = {games[depth:]}')
        #     print(f's1 champion = {first_half_season_champion}')
        #     print(f'one of final state = {get_state(final_state)}, playoff teams = {find_all_playoff_teams(final_state, first_half_season_champion, first_half_season_record)}')
        #     print(f'one of final s2 record = {get_state(get_second_half_season_record(final_state, first_half_season_record))}, playoff teams = {get_all_second_half_champions(final_state, first_half_season_record)}')
        #     print(f'one of s2 champions = {get_all_second_half_champions(final_state, first_half_season_record)}')
        #     print('---')

    stateDict[state] = (playoff_chances_hw + playoff_chances_gw + playoff_chances_d, loser_benefit, most_loss)

    return playoff_chances_hw + playoff_chances_gw + playoff_chances_d, final_state, loser_benefit, most_loss




count = 0

def main():
    n_teams = 4#int(input("Input the number of teams: "))
    n_games = 20#int(input("Input the number of games that each team plays against another in a half-season: "))
    num_game_assigned_second = int(sys.argv[3])#int(input("Input the number of games that are assigned results in the second half-season: "))
    weights = [1, 1, 1]#list(map(float, input("Input the weights of home win, guest win, and draw: ").split()))
    test_num = 1#int(input("Input the number of tests: ")) 
    sum_count = 0
    sum_time = 0
    most_loss_game = (0, None)

    if year >= 2021:
        n_teams = 5
        n_games = 15
    if year >= 2024:
        n_teams = 6
        n_games = 12

    half_season_games_count = math.comb(n_teams, 2) * n_games

    for i in range(test_num):
        time_start = time.time()
        global count
        count = 0
        teams = create_teams(n_teams)

        if len(sys.argv) >= 3:
            random.seed(int(sys.argv[2]))

        season_2017 = assign_schedule(f"schedule_{year}_re.txt")
        first_half_season = season_2017[0:half_season_games_count]
        # gen_first_half_season_record(teams, n_games)
        assign_win_lose(teams, half_season_games_count)

        first_half_season_champion, first_half_season_record = None, None 

        # support assigned some second half record
        if num_game_assigned_second > 0: 
            first_half_season_champion, first_half_season_record = find_one_first_half_season_champion_n_record(teams)
            # gen_some_second_half_season_record(teams, num_game_assigned_second, games, remaining_n_games)
            assign_win_lose(teams, half_season_games_count+num_game_assigned_second)

        max_annealing_time = 1
        annealing_time = 0
        T = 0
        if(sys.argv[1] == 'weight'):
            T = 1
        elif(sys.argv[1] == 'slope'):
            T = 100000
        elif(sys.argv[1] == 'mix'):
            T = 1000
        else:
            raise Exception("No mode set")
        Rt = T/max_annealing_time
        
        best_loss = float("inf")
        previous_loss = float("inf")
        best_schedule = None
        previous_schedule = None

        while best_loss != 0 and annealing_time < max_annealing_time:
            
            if annealing_time == 0:
                second_half_season = season_2017[half_season_games_count:2*half_season_games_count]
            else:
                second_half_season = neighbor_schedule(previous_schedule, num_game_assigned_second, most_loss_game)
            games = first_half_season + second_half_season
        
            stateDict = {}
            remaining_n_games = np.full(n_teams, n_games * (n_teams - 1))
        
            _, _, loss, most_loss_game = simulate(len(games) // 2 + num_game_assigned_second, teams, games, first_half_season_champion, first_half_season_record, stateDict, remaining_n_games, weights)
            print("annealing_time: ", annealing_time)
            print("schedule: ", second_half_season)
            print("loss: ", loss)
            

            loss_diff = loss - previous_loss 

            threshold = np.exp(-loss_diff/(T))
            dice = np.random.rand()
            
            print("threshold: ", threshold)
            print("dice: ", dice, flush=True)

            if dice < threshold:
                previous_schedule = second_half_season
                previous_loss = loss
                print("move", flush=True)
            
            if loss < best_loss:
                best_schedule = second_half_season
                best_loss = loss

            T -= Rt
            annealing_time += 1
            # if annealing_time == max_annealing_time:
            #     max_annealing_time += 50
            #     if(sys.argv[1] == 'weight'):
            #         T = 0.1
            #     elif(sys.argv[1] == 'slope'):
            #         T = 10000
            #     elif(sys.argv[1] == 'mix'):
            #         T = 100
            #     else:
            #         raise Exception("No mode set")
                
            #     Rt = T/50
        
        time_now = time.time()
        print(f'node count = {count}')
        print(f'time = {time_now - time_start}')
        sum_count += count
        sum_time += time_now - time_start

    print("best schedule: ", best_schedule)
    print("best loss: ", best_loss)
    print(f'average node count = {sum_count / test_num}')
    print(f'average time = {sum_time / test_num}')


if __name__ == "__main__":
    main()
    