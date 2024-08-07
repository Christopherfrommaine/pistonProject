from algorithm import State, moveBlockTo
from runLogic import runWithoutManualCorrection

lowerDoor = State('pppppppppppppp  f' + ' ' * 24)
# State doesn't really matter right now, as I will be manually changing it later

# Closing Sequence
lowerDoor.applyCustomMoves([i for i in range(64)])

if __name__ == '__main__':
    runWithoutManualCorrection(lowerDoor, 'new', logging=True)
