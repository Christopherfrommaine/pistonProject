from algorithm import State, moveBlockTo
from runLogic import runWithoutManualCorrection

door = State('ppppppppppppppppppppp  f        b         ', 'ooooooooooooo')

moveBlockTo(9, 0, door)
moveBlockTo(-1, -3, door)  # Puts pistons back nicely


print('len before optimization: ', len1 := len(door.moves))
from simplify2 import repeatSimplification, rmCommonPatterns
door.moves = repeatSimplification(door.moves, door.originalState, rmCommonPatterns, prnt=True, timeLimit=600)
len1 = 5491
print('len after optimization: ', len2 := len(door.moves))
print(f'{100 * (1 - (len2 / len1)):.1f}% Improvement during optimization! ({len2}/{len1})')

runWithoutManualCorrection(door, 'shulker', logging=True, rep=False, CARS=False)