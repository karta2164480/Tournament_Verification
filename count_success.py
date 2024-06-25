import os
import re

def search_string_in_file(file_path, search_string):
	"""Search for a specific string in a file."""
	max_annealing_time = 0
	found_best_loss = False
	try:
		with open(file_path, 'r', encoding='utf-8') as file:
			for line in file:
				if search_string in line:
					found_best_loss = True
				if 'annealing_time:' in line:
					# Extract the annealing time value
					annealing_time = float(re.search(r'annealing_time:\s+(\d+\.?\d*)', line).group(1))
					if annealing_time > max_annealing_time:
						max_annealing_time = annealing_time
	except Exception as e:
		print(f"Error reading file {file_path}: {e}")
	return found_best_loss, max_annealing_time

def search_string_in_directory(directory, search_string):
	"""Search for a specific string in all files within a directory."""
	results = {}

	for root, dirs, files in os.walk(directory):
		for file in files:
			file_path = os.path.join(root, file)
			file_type = None
			
			if file.startswith("mix_"):
				file_type = "mix"
			elif file.startswith("slope_"):
				file_type = "slope"
			elif file.startswith("weight_"):
				file_type = "weight"
			elif file.startswith("4games_"):
				file_type = "4games_"
			elif file.startswith("nonrandom_"):
				file_type = "nonrandom"

			
			if file_type:
				found, max_annealing_time = search_string_in_file(file_path, search_string)
				if found:
					file_number = int(re.search(r'_(\d+)', file).group(1))
					if file_number not in results:
						results[file_number] = {"mix": -1, "slope": -1, "weight": -1, "4games_": -1, "nonrandom": -1}
					results[file_number][file_type] = max_annealing_time

	total_times = {"mix": 0, "slope": 0, "weight": 0, "4games_": 0, "nonrandom": 0}
	
	mix_less_100 = 0
	slope_less_100 = 0
	weight_less_100 = 0
	_4games_less_100 = 0
	nonrandom_less_100 = 0

	for number, times in results.items():
		if times['mix'] >= 0 and times['mix'] < 100:
			mix_less_100 += 1
		if times['slope'] >= 0 and times['slope'] < 100:
			slope_less_100 += 1
		if times['weight'] >= 0 and times['weight'] < 100:
			weight_less_100 += 1
		if times['4games_'] >= 0 and times['4games_'] < 100:
			_4games_less_100 += 1
		if times['nonrandom'] >= 0 and times['nonrandom'] < 100:
			nonrandom_less_100 += 1

	print("mix_less_100: ", mix_less_100)
	print("slope_less_100: ", slope_less_100)
	print("weight_less_100: ", weight_less_100)
	print("4games_less_100: ", _4games_less_100)
	print("nonrandom_less_100: ", nonrandom_less_100)

	mix_success = 0
	slope_success = 0
	weight_success = 0
	_4games_success = 0
	nonrandom_success = 0	


	for number, times in results.items():
		if times['mix'] >= 0:
			mix_success += 1
		if times['slope'] >= 0:
			slope_success += 1
		if times['weight'] >= 0:
			weight_success += 1
		if times['4games_'] >= 0:
			_4games_success += 1
		if times['nonrandom'] >= 0:
			nonrandom_success += 1

	print("mix_success: ", mix_success)
	print("slope_success: ", slope_success)
	print("weight_success: ", weight_success)
	print("_4games_success: ", _4games_success)
	print("nonrandom_success: ", nonrandom_success)



	# for number, times in results.items():
	# 	if all(times.values()):
	# 		for key in total_times.keys():
	# 			total_times[key] += times[key]

	# for key, value in total_times.items():
	# 	print(f"Total annealing time for {key}: {value}")

	# min_time_type = min(total_times, key=total_times.get)
	# print(f"The method with the least annealing time is {min_time_type} with a total time of {total_times[min_time_type]}")

# 設定要搜尋的資料夾和字串
directory_path = './result'
search_string = 'best loss:'

# 執行搜尋
search_string_in_directory(directory_path, search_string)