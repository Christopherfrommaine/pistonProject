from algorithm import State, moveBlockTo
from runLogic import runWithoutManualCorrection

door = State('ppppppppppppp  f       b')
moveBlockTo(6, 0, door)
moveBlockTo(-1, -3, door)  # Puts pistons back nicely
door.applyMoves(str(i) for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10])
runWithoutManualCorrection(door, logging=True)
