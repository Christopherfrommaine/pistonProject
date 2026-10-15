from copy import deepcopy
from algorithm.algorithm import State
from time import time


def simplify3working(door):
    workingPasses = [passRmCommonPatternsNoK]
    simplifyWithPasses(door, workingPasses)

def simplifyWithPasses(door: State, passes):
    print("before optimization: ", len1 := len(door.moves))

    begin = time()
    for _ in range(10):
        for pss in passes:
            pss(door)
    end = time()
    
    print("after optimization:  ", len2 := len(door.moves))
    improvement = 100 * (len1 - len2) / len1
    print(f"{improvement:.2f}% improvement in {end - begin:.2f} seconds")


from optimization.simplify2 import rmCommonPatterns, rmCommonPatternsNoK

# Untested
def passRmCommonPatterns(door: State):
    door.moves = rmCommonPatterns(deepcopy(door.moves), door.originalState)

# Untested
def passRmCommonPatternsNoK(door: State):
    door.moves = rmCommonPatternsNoK(deepcopy(door.moves), door.originalState)






