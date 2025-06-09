from algorithm import State, moveBlockTo, retractCustom
from runLogic import runWithoutManualCorrection
from fileHelperFunctions import moveFromFile

# TODO: yo dawg, there ain't no wire for 46?

# Closing
door = State('pppppppppppppppppppppppppppppppp  f          b     ', 'ooooo')

moveFromFile(door, "closing/first_blocks.txt", State(
    'ppppp p p p p pofpo po po p bbbbbbbbbbbbb    ', '    o'
))

moveBlockTo(8, -3, door)

moveFromFile(door, "closing/optimized_top_piston.txt", State(
    'ppppp p p p po pO po po pp  bbbbbbbbbbbbb    ', '    o'
))

moveBlockTo(9, -3, door)

moveFromFile(door, "closing/last_blocks.txt", State(
    'pppppppppppppp  fbbbbbbbbbbbbbbbbbbbbbbbb    ', 'ooooo'
))

# Stop
door.applyMove(8 * 9)
print('len after closing: ', len(door.moves))

# Opening
## Unoptimized retractions
moveBlockTo(1, -1, door)
retractCustom([11, 17, 18], door)

moveBlockTo(2, -1, door)
retractCustom([11, 17, 18], door)

moveBlockTo(3, -1, door)
retractCustom([11, 17, 18], door)

moveBlockTo(4, -1, door)
retractCustom([11, 17, 18], door)

moveBlockTo(5, -1, door)
retractCustom([11, 17, 18], door)

moveBlockTo(6, -1, door)
retractCustom([11, 17, 18], door)

moveBlockTo(7, -1, door)
retractCustom([11, 17, 18, 19, 22], door)

moveBlockTo(8, -1, door)
retractCustom([11, 17, 18, 19, 22], door)

# 9th
moveFromFile(door, "opening/9th_piston_optimized.txt", State(
    'ppppppp p p p pofpo po pb bbbbbbbbbbbbbb    ', '   oo'
))
moveBlockTo(8, -1, door)
moveBlockTo(-2, -3, door)
retractCustom([11, 17, 18, 19, 22], door)

# 10th
moveFromFile(door, "opening/10th_piston_optimized.txt", State(
    'ppppppp p p po pO po po pb bbbbbbbbbbbbbb    ', '    o'
))
moveBlockTo(8, -3, door) # Move piston down
## 9th again
moveFromFile(door, "opening/9th_piston_optimized.txt", State(
    'ppppppp p p p pofpo po pb  bbbbbbbbbbbbb    ', '   oo'
))
moveBlockTo(8, -1, door)
moveBlockTo(-2, -3, door)
retractCustom([11, 17, 18, 19, 22], door)


# 11th
moveFromFile(door, "opening/11th_piston_optimized.txt", State(
    'ppppp p p pp po Po po po pb bbbbbbbbbbbbb    ', '    o'
))
moveBlockTo(9, -3, door) # Move piston down   # OOOOOF
# 10th again
moveFromFile(door, "opening/10th_piston_optimized.txt", State(
    'ppppppp p p po pO po po pb  bbbbbbbbbbbbb    ', '    o'
))
moveBlockTo(8, -3, door) # Move piston down
## 9th again
moveFromFile(door, "opening/9th_piston_optimized.txt", State(
    'ppppppp p p p pofpo po pb   bbbbbbbbbbbb    ', '   oo'
))
moveBlockTo(8, -1, door)
moveBlockTo(-2, -3, door)
retractCustom([11, 17, 18, 19, 22], door)


# 12th
moveFromFile(door, "opening/11th_piston_optimized.txt", State(
    'ppppp p p p p pofpo po po pb bbbbbbbbbbbb    ', '    o'
))
moveBlockTo(10, -3, door) # Move piston down   # OOOOOOOOOOOOF
# 11th again
moveFromFile(door, "opening/11th_piston_optimized.txt", State(
    'ppppp p p pp po Po po po pb bbbbbbbbbbbbb    ', '    o'
))
moveBlockTo(9, -3, door) # Move piston down   # OOOOOF
# 10th again
moveFromFile(door, "opening/10th_piston_optimized.txt", State(
    'ppppppp p p po pO po po pb  bbbbbbbbbbbbb    ', '    o'
))
moveBlockTo(8, -3, door) # Move piston down
## 9th again
moveFromFile(door, "opening/9th_piston_optimized.txt", State(
    'ppppppp p p p pofpo po pb   bbbbbbbbbbbb    ', '   oo'
))
moveBlockTo(8, -1, door)
moveBlockTo(-2, -3, door)
retractCustom([11, 17, 18, 19, 22], door)

print('len after lower opening 1: ', len(door.moves))

# UPPER
moveFromFile(door, 'opening/upper_full.txt', State(
    'pppppppppppppp  f bbbbbbbbbbb            ', 'ooooo'
))  # omg this took so long and its all manual

print('len after upper opening: ', len(door.moves))

# Lower again
# First is omitted, no first piston
# ## Unoptimized retractions
# moveBlockTo(1, -1, door)
# retractCustom([*], door)

moveBlockTo(2, -1, door)
retractCustom([11, 17, 18, 19, 22, 24, 27], door)

moveBlockTo(3, -1, door)
retractCustom([11, 17, 18, 19, 22, 24, 27], door)

moveBlockTo(4, -1, door)
retractCustom([11, 17, 18, 19, 22, 24, 27], door)

moveBlockTo(5, -1, door)
retractCustom([11, 17, 18, 19, 22, 24, 27], door)

moveBlockTo(6, -1, door)
retractCustom([11, 17, 18, 19, 22, 24], door)

moveBlockTo(7, -1, door)
retractCustom([11, 17, 18, 19, 22], door)

moveBlockTo(8, -1, door)
retractCustom([11, 17, 18, 19], door)

# 9th
moveFromFile(door, "opening/9th_piston_optimized.txt", State(
    'ppppppp p p p pofpo po pb bbbbbbbbbbbbbb    ', '   oo'
))
moveBlockTo(8, -1, door)
moveBlockTo(-2, -3, door)
retractCustom([11, 17, 18], door)

# 10th
moveFromFile(door, "opening/10th_piston_optimized.txt", State(
    'ppppppp p p po pO po po pb bbbbbbbbbbbbbb    ', '    o'
))
moveBlockTo(8, -3, door) # Move piston down
## 9th again
moveFromFile(door, "opening/9th_piston_optimized.txt", State(
    'ppppppp p p p pofpo po pb  bbbbbbbbbbbbb    ', '   oo'
))
moveBlockTo(8, -1, door)
moveBlockTo(-2, -3, door)
retractCustom([11, 17], door)


# 11th
moveFromFile(door, "opening/11th_piston_optimized.txt", State(
    'ppppp p p pp po Po po po pb bbbbbbbbbbbbb    ', '    o'
))
moveBlockTo(9, -3, door) # Move piston down   # OOOOOF
# 10th again
moveFromFile(door, "opening/10th_piston_optimized.txt", State(
    'ppppppp p p po pO po po pb  bbbbbbbbbbbbb    ', '    o'
))
moveBlockTo(8, -3, door) # Move piston down
## 9th again
moveFromFile(door, "opening/9th_piston_optimized.txt", State(
    'ppppppp p p p pofpo po pb   bbbbbbbbbbbb    ', '   oo'
))
moveBlockTo(8, -1, door)
moveBlockTo(-2, -3, door)
retractCustom([11], door)


# 12th
moveFromFile(door, "opening/11th_piston_optimized.txt", State(
    'ppppp p p p p pofpo po po pb bbbbbbbbbbbb    ', '    o'
))
moveBlockTo(10, -3, door) # Move piston down   # OOOOOOOOOOOOF
# 11th again
moveFromFile(door, "opening/11th_piston_optimized.txt", State(
    'ppppp p p pp po Po po po pb bbbbbbbbbbbbb    ', '    o'
))
moveBlockTo(9, -3, door) # Move piston down   # OOOOOF
# 10th again
moveFromFile(door, "opening/10th_piston_optimized.txt", State(
    'ppppppp p p po pO po po pb  bbbbbbbbbbbbb    ', '    o'
))
moveBlockTo(8, -3, door) # Move piston down
## 9th again
moveFromFile(door, "opening/9th_piston_optimized.txt", State(
    'ppppppp p p p pofpo po pb   bbbbbbbbbbbb    ', '   oo'
))
moveBlockTo(8, 0, door)
moveBlockTo(-1, -3, door)
retractCustom([], door, assrt=False)

print('len after lower opening 2: ', len(door.moves))

print('number of manual moves: ', sum(1 if isinstance(m, str) else 0 for m in door.moves))


runWithoutManualCorrection(door, 'shulker', logging=True, rep=False, CARS=False)