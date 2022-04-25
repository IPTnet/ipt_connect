# Functions for calculating bonus points


def distribute_bonus_points(points_list):
    max_points = len(points_list)
    # 'equal_count' is a variable that contain the count of coincident elements in 'points_list'
    equal_count = points_list.count(points_list[0])
    if max_points == equal_count:
        return [1.0 for x in range(equal_count)]
    head = [(equal_count + 1.0) / equal_count for x in range(equal_count)]
    equal_count = points_list.count(points_list[max_points - 1])
    tail = [(equal_count - 1.0) / equal_count for x in range(equal_count)]
    return head + [1.0 for x in range(max_points - (len(head) + len(tail)))] + tail
