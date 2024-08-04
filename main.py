from algorithm import State, moveBlockTo
from runLogic import runWithoutManualCorrection

door = State('pppppppppppppppppppppppppppppppp  f          b     ', 'ooooooooooooo')
moveBlockTo(11, 0, door)
moveBlockTo(-1, -3, door)  # Puts pistons back nicely
runWithoutManualCorrection(door, logging=True)
