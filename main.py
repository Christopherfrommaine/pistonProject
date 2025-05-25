from algorithm import State, moveBlockTo
from runLogic import runWithoutManualCorrection

door = State('pppppppppppppppppppppppppppppppp  f          b     ', 'ooooooooooooo')
moveBlockTo(11, 0, door)
moveBlockTo(-1, -3, door)  # Puts pistons back nicely
runWithoutManualCorrection(door, 'shulker', logging=True)


# TODO! After the move sequence is finalized, go through and check that each move has 
# an effect on the final state.
# e.g. 8 7 9 in the starting state is equivalent to 7 9
# so go through, run with one missing until the states match up or dont. If they do, great!