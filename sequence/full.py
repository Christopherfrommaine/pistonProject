from algorithm import State, moveBlockTo
from runLogic import runWithoutManualCorrection
from fileHelperFunctions import moveFromFile

# Closing
door = State('pppppppppppppppppppppppppppppppp  f          b     ', 'ooooooooooooo')

# door = moveFromFile(door, "closing/first_blocks.txt", State(
#     'ppppp p p p p pofpo po po p bbbbbbbbbbbbb    ', '    ooooooooo'
# ))
# 
# moveBlockTo(8, -3, door)
# door.applyMove((-3,))

# door = moveFromFile(door, "closing/optimized_top_piston.txt", State(
#     'ppppp p p p po pO po po pp  bbbbbbbbbbbbb    ', '    ooooooooo'
# ))

# moveBlockTo(9, -3, door)


# door.moves = door.moves[:10000]  # For debugging
runWithoutManualCorrection(door, 'shulker', logging=True)