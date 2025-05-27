from algorithm import State, moveBlockTo
from runLogic import runWithoutManualCorrection
from fileHelperFunctions import moveFromFile

door = State('pppppppppppppppppppppppppppppppp  f          b     ', 'ooooooooooooo')

door = moveFromFile(door, "closing/first_blocks.txt", State(
    'ppppp p p p p pofpo po po p b', '    ooooooooo'))

moveBlockTo(12, 0, door)

runWithoutManualCorrection(door, 'shulker', logging=True)