from algorithm import State, moveBlockTo
from runLogic import runWithoutManualCorrection

door = State('ppppppppppppppppppp  f   b  ')
moveBlockTo(4, 0, door)

runWithoutManualCorrection(door, logging=True)
