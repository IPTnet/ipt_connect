# All functions for calculating mean value are independent of other models, so don't use import
import math

def mean(vec):
	if len(vec) != 0:
		return float(sum(vec)) / len(vec)
	else:
		return 0.0

def ipt_mean(vec):
    if len(vec) in [5, 6]:
        nreject = 1
    elif len(vec) in [7, 8]:
        nreject = 2
    else:
        nreject = int(math.ceil(len(vec) / 4.0))


    # TODO: the following code looks messy, but it works.
    # There was an unsuccessful attempt to refactor it.
    # The code should be refactored and tested.


    if round(nreject / 2.0) == nreject / 2.0:
        nlow = int(nreject / 2.0)
        nhigh = int(nlow)
    else:
        nlow = int(nreject / 2.0 + 0.5)
        nhigh = int(nreject / 2.0 - 0.5)

    if nhigh == 0:
        vec = vec[nlow : ]
    else:
        vec = vec[nlow : -nhigh]
    return mean(vec)

def iypt_mean(vec):
    if len(vec) > 1 :
        vec.append((vec.pop(0) + vec.pop()) / 2.0)
        return mean(vec)
    return mean(vec)

def ttn_mean(vec):
    if len(vec) <= 4:
        return mean(vec)
    return iypt_mean(vec)
