from algorithm import State, moveBlockTo
from runLogic import runWithoutManualCorrection

door = State('ppppppppppppp  f       b')
moveBlockTo(5, 0, door)

runWithoutManualCorrection(door, logging=True)
