import json
from copy import deepcopy
import pandas as pd
import time

# 讀取JSON檔案



for year in range(2018, 2024):
	with open(f'schedule{year}_unparse.json', 'r', encoding='utf-8') as file:
		data = json.load(file)


	team_dict = {
		"統一7-ELEVEn獅": 0,
		"中信兄弟": 1,
		"富邦悍將": 2,
		"味全龍": 4,
		"樂天桃猿": 3,
		"Lamigo": 3,
		"台鋼雄鷹": 5
	}

	# 解析 GameDatas 欄位的內容
	game_data_str = data['GameDatas']
	game_data_list = json.loads(game_data_str)

	# print(game_data_list)
	game_data_list.sort(key=lambda x: time.strptime(x['GameDateTimeS'], "%Y-%m-%dT%H:%M:%S"))


	# 使用集合來確保每個 GameSno 只保留一筆資料
	seen_game_snos = set()
	result = []
	win_lose =  [[0 for x in range(3)] for y in range(6)] 
	win_lose_dict = {}
	win_lose_list = []
	# index = 0

	for game in game_data_list:
		if game['PresentStatus'] == 1:
			game_sno = game['GameSno']
			if game_sno not in seen_game_snos:
				seen_game_snos.add(game_sno)
				visiting_team_number = team_dict.get(game['VisitingTeamName'], -1)  # 如果隊名不在字典中，用 -1 表示
				home_team_number = team_dict.get(game['HomeTeamName'], -1)
				visiting_score = game['VisitingScore']
				home_score = game['HomeScore']

				if visiting_score > home_score:
					win_lose[visiting_team_number][0] += 1
					win_lose[home_team_number][1] += 1
				elif visiting_score < home_score:
					win_lose[visiting_team_number][1] += 1
					win_lose[home_team_number][0] += 1
				elif visiting_score == home_score:
					win_lose[visiting_team_number][2] += 1
					win_lose[home_team_number][2] += 1
				else:
					raise Exception("weird bug")


				win_lose_dict[game_sno] = deepcopy(win_lose)
				win_lose_list.append(deepcopy(win_lose))
				print(game_sno, win_lose)
				game_info = f"{visiting_team_number} {home_team_number}"
				result.append(game_info)
			else:
				print(game)

	# 將結果寫入新檔案
	with open(f'schedule_{year}_re.txt', 'w', encoding='utf-8') as output_file:
		for game_info in result:
			output_file.write(game_info + '\n')

	# with open('win_lose_2017.json', 'w') as convert_file: 
	#      convert_file.write(json.dumps(win_lose_dict))

	with open(f'win_lose_{year}_re.json', 'w') as convert_file: 
		convert_file.write(json.dumps(win_lose_list))