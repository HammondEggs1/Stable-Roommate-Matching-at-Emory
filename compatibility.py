from collections import defaultdict

class Compatibility:
	def compareSchedule(schedule1, schedule2):
		matches = 0
		for i, time in enumerate(schedule1):
			if(schedule2[time]==1):
				matches = matches+1;
		return matches/len(schedule1)

	totalTimes = 40
	schedule1 = defaultdict(lambda: 0)
	schedule2 = defaultdict(lambda: 0)
	schedule1["4P"] = 1
	schedule2["6P"] = 1
	schedule1["7P"] = 1
	schedule2["7P"] = 1
	schedule1["8P"] = 1
	print(compareSchedule(schedule1, schedule2))