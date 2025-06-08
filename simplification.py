from copy import deepcopy
from algorithm import State
from conversion import applyCorrections

def matchAndReplaceAll(moves, dict):
    i = 0
    while i < len(moves):
        cont = True
        for (patt, rep) in dict:
            if moves[i:(i + len(patt))] == patt:
                moves = moves[:i] + rep + moves[(i + len(patt)):]
                cont = False
        if cont:
            i += 1
    return moves

def simplifyCorrectedMoves(moves):
    # Original: 34901

    return matchAndReplaceAll(moves, [
        ([-4, -5], [-5]),
        ([-5, -6], [-6]),

        ([-5, -3, -6], [-6]),
        ([-6, -4, -2, -7], [-7]),
    ])

def repLayoutMoves(moves):
    return matchAndReplaceAll(moves, [
        ([7, 9], [49]),
        ([6, 8, 10], [50]),
    ])

def simplifyUncorrectedMoves(moves, state: State):
    o = []
    segstart = 0
    for mi, m in enumerate(moves):
        if isinstance(m, State):
            o.extend(simplifyUncorrectedMoves_uselessExpandableSections2(state, segstart, mi - 1))
            segstart = mi
            o.append(m)
    
    # Asseertion
    odoor = state.originalState
    odoor.applyMoves(o)
    assert odoor.fullRepr() == state.fullRepr()

    return o

from typing import List, Tuple

def merge_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not intervals:
        return []

    # Sort intervals by their start time
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for current in intervals[1:]:
        prev_start, prev_end = merged[-1]
        curr_start, curr_end = current

        # If intervals overlap or touch, merge them
        if curr_start <= prev_end:
            merged[-1] = (prev_start, max(prev_end, curr_end))
        else:
            merged.append(current)

    return merged
def remove_intervals(lst, intervals):
    """
    Remove sections from lst specified by intervals.
    Each interval is a tuple (start, end) and removes lst[start:end].
    Assumes intervals are non-overlapping and sorted by start.
    """
    # Sort intervals by start index
    intervals = sorted(intervals, key=lambda x: x[0])
    
    result = []
    prev_end = 0
    
    for start, end in intervals:
        # Add elements before the current interval
        result.extend(lst[prev_end:start])
        prev_end = end
    
    # Add remaining elements after the last interval
    result.extend(lst[prev_end:])
    
    return result

def simplifyUncorrectedMoves_uselessExpandableSections(state: State, obegin, oend):
    assert obegin == 0 or isinstance(state.moves[obegin], State)
    assert not any(isinstance(m, State) for m in state.moves[obegin + 1:oend])

    originalDoor = state.originalState if obegin == 0 else state.moves[obegin]
    getOriginalDoor = lambda: deepcopy(originalDoor)

    moves = state.moves[obegin:oend]

    odoor = getOriginalDoor()
    odoor.applyMoves(moves)
    originalDoorRepr = odoor.fullRepr()

    def testSlice(begin, end):
        newMoves = moves[:begin] + moves[end:]

        if any(isinstance(m, str) for m in moves[begin:end]):
            return False

        try:
            odoor = getOriginalDoor()
            odoor.applyMoves(newMoves)
        except AssertionError:
            return False

        if odoor.fullRepr() != originalDoorRepr:
            return False

        return True

    positionsPossible = []
    maxWidth = 3
    for i in range(len(moves) - maxWidth):
        print('[' + round(50 * i / len(moves)) * '#' + round(50 * (1 - i / len(moves))) * ' ' + '] ' + str(100 * i / len(moves))[:4] + '%', end='\r')
        for j in range(i + 1, i + maxWidth):
            if testSlice(i, j):
                positionsPossible.append((i, j))
    print()
    
    counter = 0
    while True:
        counter += 1
        if counter % 5 == 0:
            maxWidth += 1

        print(f"simplifying step... {len(positionsPossible)}")
        
        newPositionsPossible = []
        for (pi, (a, b)) in enumerate(positionsPossible):
            print('[' + round(50 * pi / len(positionsPossible)) * '#' + round(50 * (1 - pi / len(positionsPossible))) * ' ' + '] ' + str(100 * pi / len(positionsPossible))[:4] + '%', end='\r')

            bestMag = 0
            best = (a, b)
            for i in range(-maxWidth, 1):
                for j in range(0, maxWidth):
                    if a + i >= 0 and b + j < len(moves):
                        if testSlice((a + i), (b + j)):
                            mag = abs(i) + abs(j)
                            if mag > bestMag:
                                bestMag = mag
                                best = (a + i, b + j)
            newPositionsPossible.append(best)
        print()
        
        newPositionsPossible = merge_intervals(newPositionsPossible)
        newPositionsPossible = [npp for npp in newPositionsPossible if npp[0] != npp[1]]
        
        if newPositionsPossible == positionsPossible:
            break

        positionsPossible = newPositionsPossible
        
        print(positionsPossible)
    
    o = remove_intervals(moves, positionsPossible)
    print(o)

    # Asseertion
    odoor = getOriginalDoor()
    odoor.applyMoves(o)

    return o
    

def simplifyUncorrectedMoves_uselessExpandableSections2(state: State, obegin, oend):
    assert obegin == 0 or isinstance(state.moves[obegin], State)
    assert not any(isinstance(m, State) for m in state.moves[obegin + 1:oend])
    maxWidth = 2

    originalDoor = state.originalState if obegin == 0 else state.moves[obegin]
    getOriginalDoor = lambda: deepcopy(originalDoor)

    moves = state.moves[obegin:oend]

    odoor = getOriginalDoor()
    odoor.applyMoves(moves)
    originalDoorRepr = odoor.fullRepr()

    def testSlice(begin, end):
        newMoves = moves[:begin] + moves[end:]

        if any(isinstance(m, str) for m in moves[begin:end]):
            return False

        try:
            odoor = getOriginalDoor()
            odoor.applyMoves(newMoves)
        except AssertionError:
            return False

        if odoor.fullRepr() != originalDoorRepr:
            return False
        
        try:
            applyCorrections(newMoves, getOriginalDoor())
        except AssertionError:
            return False

        return True

    changed = True
    hotspots = set(range(len(moves)))

    counter = 2
    while changed:
        counter += 1
        changed = False

        print(f"simplifying step... {len(moves)} {len(hotspots)}")

        newHotspots = set()
        for i in hotspots:
            if i < 0 or i > len(moves) - maxWidth:
                continue

            print('[' + round(50 * i / len(moves)) * '#' + round(50 * (1 - i / len(moves))) * ' ' + '] ' + str(100 * i / len(moves))[:4] + '%', end='\r')
            # for j in range(i + 1, i + maxWidth):
            j = i + 2
            if testSlice(i, j):
                moves = moves[:i] + moves[j:]
                changed = True
                newHotspots.update(i + offset for offset in range(-counter, counter))
                # break
        print()

        hotspots = newHotspots

    return moves
    

