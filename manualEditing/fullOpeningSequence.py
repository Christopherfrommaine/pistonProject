from algorithm import State, moveBlockTo
from runLogic import runWithoutManualCorrection

lowerDoor = State('pppppppppppppp  f' + ' ' * 24)
# State doesn't really matter right now, as I will be manually changing it later

# Closing Sequence
lowerDoor.applyCustomMoves([  # Put first 12 blocks into place
    8,
    16, 10,
    17, 16, 10,
    20, 17, 16, 10,
    23, 20, 17, 16, 10,
    25, 23, 20, 17, 16, 10,
    28, 25, 23, 20, 17, 16, 10,
    29, 28, 25, 23, 20, 17, 16, 10,
    29, 28, 25, 23, 20, 17, 16, 10,
    29, 28, 25, 23, 20, 17, 16, 10,
    27, 28, 25, 23, 20, 17, 16, 10,
    26, 23, 20, 17, 16, 10])

lowerDoor.applyCustomMoves([  # More Efficient Large Piston Movement
    15,
    7, 14, 15,
    6, 13, 14, 15,
    5, 5, 12, 13, 14, 15,

    3, 4, 5, 6, 8] + [10] * 30)

# lowerDoor.applyCustomMoves([  # More Efficient Large Piston Movement
#     12,
#     7, 13, 12,
#     6, 14, 13, 12,
#     5, 5, 15, 14, 13, 12,
#
#     3, 4, 5, 6, 8] + [10] * 30)


# lowerDoor.applyCustomMove(72)  # Debugging Pause

# Remaking Door from Custom State
lowerDoorOld = lowerDoor
lowerDoor = State('ppppp p p p p pofpo po po p bbbbbbbbbbbb ', '    o')  # Extra 'o' added cuz it breaks otherwise
lowerDoor.moves = lowerDoorOld.moves

moveBlockTo(10, -2, lowerDoor)

firstMoves = lowerDoor.moves[:200]
lowerDoor = lowerDoor.originalState
lowerDoor.applyMoves(firstMoves)

if __name__ == '__main__':
    runWithoutManualCorrection(lowerDoor, 'new', logging=True)
