#Functions for calculating bonus points

def distribute_bonus_points(points_list):
	if len(points_list) == 3:
		return distribute_bonus_points_3(points_list)
	if len(points_list) == 4:
		return distribute_bonus_points_4(points_list)
	return [2.0, 1.0, 1.0, 0.0, 0.0]

def distribute_bonus_points_3(points_list):

	# If everyone is ex-aequo
	if points_list[0] == points_list[1] and points_list[0] == points_list[2]:
		return [1.0, 1.0, 1.0]

	# If 1 and 2 are ex-aequo
	if points_list[0] == points_list[1]:
		return [1.5, 1.5, 0.0]

	# If 2 and 3 are ex-aequo
	if points_list[1] == points_list[2]:
		return [2.0, 0.5, 0.5]

	# If no ex-aequo
	return [2.0, 1.0, 0.0]


def distribute_bonus_points_4(points_list):

	######################
	# 4 teams ex-aequo
	# If everyone is ex-aequo
	if points_list[0] == points_list[1] and points_list[1] == points_list[2] and points_list[2] == points_list[3]:
		return [1.0, 1.0, 1.0, 1.0]
	######################

	######################
	# 3 teams ex-aequo
	if points_list[0] == points_list[1] and points_list[1] == points_list[2]:
		return [4.0/3.0, 4.0/3.0, 4.0/3.0, 0.0]
	if points_list[1] == points_list[2] and points_list[2] == points_list[3]:
		return [2.0, 1.0/3.0, 1.0/3.0, 1.0/3.0]
	######################

	######################
	# 2 pairs of teams ex-aequo
	if points_list[0] == points_list[1] and points_list[2] == points_list[3]:
		return [1.5, 1.5, 0.5, 0.5]
	######################

	######################
	# One pair of teams ex-aequo
	if points_list[0] == points_list[1]:
		return [1.5, 1.5, 1.0, 0.0]
	if points_list[1] == points_list[2]:
		return [2.0, 1.0, 1.0, 0.0]  # Redundant, but let it be
	if points_list[2] == points_list[3]:
		return [2.0, 1.0, 0.5, 0.5]
	######################

	# No ex-aequo
	return [2.0, 1.0, 1.0, 0.0]

