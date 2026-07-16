from algorithm import State, moveBlockTo
from runLogic import runWithoutManualCorrection

door = State('ppppppppppppppppppppp  B                  ')

pos = 5

moveBlockTo(0, pos, door)
moveBlockTo(pos  -2, -3, door)
door.applyCustomMove(9 * 8)
moveBlockTo(pos , 0, door)
moveBlockTo(-1, -3, door)

# door.applyCustomMove(9 * 8)
# moveBlockTo(0, pos , door)
# moveBlockTo(pos - 2, -3, door)
# door.applyCustomMove(9 * 8)
# moveBlockTo(pos, 0, door)
# moveBlockTo(-1, -3, door)

print('len after lower opening 2: ', len1 := len(door.moves))
print('number of manual moves: ', sum(1 if isinstance(m, str) else 0 for m in door.moves))


print('len before optimization: ', len1)
finalstate = door.p
from simplify2 import *
# door.moves = repeatSimplification(door.moves, door.originalState, rmCommonPatterns)
# door.moves = repeatSimplification(door.moves, door.originalState, rmCommonPatternsNoK)
for i in range(3):
    print(f"simplification pass {i}")
    for j in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 50, 100]:
        print(f"_{j}", end="")
        door.moves = repeatSimplification(door.moves, door.originalState, nAtATime(j))
print('len after optimization: ', len2 := len(door.moves))
print(f'{100 * (1 - (len2 / len1)):.1f}% Improvement during optimization! ({len2}/{len1})')

from copy import deepcopy
os = deepcopy(door.originalState)
for m in door.moves:
    os.applyMove(m)
    print(os)

runWithoutManualCorrection(door, 'shulker', logging=True, rep=False, CARS=False)