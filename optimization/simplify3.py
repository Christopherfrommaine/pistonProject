from copy import deepcopy
from algorithm.algorithm import State
from time import time


def simplify3working(door):
    workingPasses = [passRmCommonPatternsNoK, passRmCommonPatterns]
    simplifyWithPasses(door, workingPasses)

def simplifyWithPasses(door: State, passes):
    print("before optimization: ", len1 := len(door.moves))

    begin = time()
    for _ in range(3):
        for pss in passes:
            pss(door)
    end = time()
    
    print("after optimization:  ", len2 := len(door.moves))
    improvement = 100 * (len1 - len2) / len1
    print(f"{improvement:.2f}% improvement in {end - begin:.2f} seconds")


from optimization.simplify2 import rmCommonPatterns, rmCommonPatternsNoK

# Tested, trusted
def passRmCommonPatterns(door: State):
    door.moves = rmCommonPatterns(deepcopy(door.moves), door.originalState)

# Tested, untrusted
# tested on 4, 
def passRmCommonPatternsNoK(door: State):
    door.moves = rmCommonPatternsNoK(deepcopy(door.moves), door.originalState)

def passThign(door: State):
    from optimization.observerPostprocessing import postprocessForObservers
    postprocessForObservers(deepcopy(door))






