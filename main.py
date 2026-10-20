from algorithm.algorithm import State, moveBlockTo
from algorithm.runLogic import runWithoutManualCorrection

door = State('ppppppppppppppppppppp  B                  ')

pos = 5

moveBlockTo(0, pos, door)
moveBlockTo(pos  -2, -3, door)
door.applyCustomMove(9 * 8)
moveBlockTo(pos , 0, door)
moveBlockTo(-1, -3, door)

from optimization.simplify3 import simplify3working
simplify3working(door)

runWithoutManualCorrection(door, 'shulker', logging=True, rep=False, CARS=False)