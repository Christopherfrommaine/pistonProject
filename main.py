from algorithm import State, moveBlockTo
from runLogic import runWithoutManualCorrection

door = State('ppppppppppppppppppppp  B                  ')

pos = 3

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

# from simplify2 import repeatSimplification, rmCommonPatterns
# door.moves = repeatSimplification(door.moves, door.originalState, rmCommonPatterns)

runWithoutManualCorrection(door, 'shulker', logging=True, rep=False, CARS=False)