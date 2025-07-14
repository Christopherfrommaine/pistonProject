from copy import deepcopy
from algorithm import State
from time import time
from conversion import applyCorrections

cache = None

def worker_function(predicate, constargs, start, end):
        stepsize = max(1, round(0.01 * (end - start)))  # (end - start) is around 100,000 for full

        for n in range(start, end, stepsize):
            if predicate(*([n] + constargs)):
                return n
        return None

def parallelCompute(predicate, rngemax, constargs, threads=18):

    import multiprocessing

    chunk_size = rngemax // threads
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(threads)]

    if rngemax % threads != 0:
        ranges[-1] = (ranges[-1][0], rngemax)  # Adjust the last range

    with multiprocessing.Pool(processes=threads) as pool:
        results = pool.starmap(worker_function, [(predicate, constargs, start, end) for start, end in ranges])
    
    for result in results:
        if result is not None:
            return result

def repeatSimplification(moves, originalState: State, simpFunc, prnt=False, timeLimit=float('infinity')):
    finalState = deepcopy(originalState)
    finalState.applyMoves(moves)
    begin = time()

    oldMoves = None
    while oldMoves != moves and (time() - begin) < timeLimit:
        if prnt:
            print(f"step, {len(moves)}             ")

        oldMoves = moves
        try:
            moves = simpFunc(moves, deepcopy(originalState))

            odoor = deepcopy(originalState)
            odoor.applyMoves(moves)
            assert odoor.fullRepr() == finalState.fullRepr()
        except AssertionError:
            return oldMoves
    if prnt:
        print()

    return moves

def nAtATime(n):
    def outputFunction(moves, originalState: State):
        if len(moves) < n:
            return moves

        global cache

        if cache is None:
            cache = 0
        if cache > len(moves) - 2 * n:
            cache = 0

        finalState = deepcopy(originalState)
        finalState.applyMoves(moves)

        for i in range(cache, len(moves) - n, max(1, round(n / 1000))):
            if predicateStrict(i, moves, n, originalState, finalState):
                cache = i
                return moves[:i] + moves[i + n:]
        cache = len(moves) - n
        return moves
    return outputFunction

def predicate(i, moves, n, originalState, finalState):
    # Check for custom moves
    for j in range(i, i + n):
        if not isinstance(moves[j], int) and not isinstance(moves[j], tuple):
            return False

    newMoves = moves[:i] + moves[i + n:]

    odoor = deepcopy(originalState)
    try:
        odoor.applyMoves(newMoves)
        assert odoor.fullRepr() == finalState.fullRepr()

        applyCorrections(odoor.moves, odoor.originalState)

    except AssertionError:
        return False

    return True
def predicateStrict(i, moves, n, originalState, finalState):
    # Check for custom moves
    for j in range(i, i + n):
        if not isinstance(moves[j], int):
            return False

    newMoves = moves[:i] + moves[i + n:]

    odoor = deepcopy(originalState)
    try:
        odoor.applyMoves(newMoves, strict=True)
        assert odoor.fullRepr() == finalState.fullRepr()

        applyCorrections(odoor.moves, odoor.originalState)

    except AssertionError:
        return False

    return True
def nAtATimePar(n):
    def outputFunction(moves, originalState: State):
        if len(moves) < n:
            return moves

        finalState = deepcopy(originalState)
        finalState.applyMoves(moves)
        
        res = parallelCompute(predicateStrict, len(moves) - n, [moves, n, originalState, finalState])
        
        if res:
            moves = moves[:res] + moves[res + n:]

        return moves
    return outputFunction

def rmCommonPatterns(moves, originalState: State):
    BUFFER = 5
    
    testState = deepcopy(originalState)
    def strState(start, end):
        return ''.join(testState.p[i] for i in range(start, end))

    i = 0
    while i < len(moves) - BUFFER:
        changed = False
        print(i)

        # Example (first pattern):
        """
        if moves[i:i+3] == [i + k for i in [-4, -5, -3]]:
                if strState(-5 + k, -3 + k) == 'ppp':
                    changed = True
                    testState.applyMoves([-5 + k, -3 + k])
                    i += 3
                    break
        """

        patterns = [
            ([-4, -5, -3], -5, 'ppp', [-5, -3]),
            ([-6, -4, -8, -6, -4], -8, 'pppp', [-8, -6, -4]),
            ([-2, -3], -3, 'pp', [-3]),
            ([-2, -4], -4, 'ppp', [-4])
        ]
        
        for pat in patterns:
            originalMovesInput, originalStartInd, checkStr, originalMovesOutput = pat
            for k in range(0, min(originalState.p.keys()), -1):
                movesInput = [i + k for i in originalMovesInput]
                startInd = k + originalStartInd
                endInd = startInd + len(checkStr)
                movesOutput = [i + k for i in originalMovesOutput]
                ln = len(movesInput)

                if moves[i:i + ln] == movesInput and strState(startInd, endInd) == checkStr:
                    changed = True
                    testState.applyMoves(movesOutput)
                    i += ln
                    break
            if changed:
                break
            
        
        if not changed:
            testState.applyMove(moves[i])
            i += 1
    

    
    while i < len(moves):
        testState.applyMove(moves[i])
        i += 1
    
    return testState.moves



def contextAwareReplacementSimplification(moves, originalState: State):
    def firsteq(l1, l2):
        ln = min(len(l1), len(l2))
        return l1[:ln] == l2[:ln]

    state = originalState
    o = []
    mi = 0
    while mi < len(moves):
        mi += 1

        try:
            m = moves[mi]
            nextm = moves[mi:]

            if isinstance(nextm[0], int) and isinstance(nextm[1], int) and nextm[1] < nextm[0] and all(state.p[i] == 'p' for i in range(nextm[1], nextm[0] + 1)):
                o += [nextm[1]]
                mi += 1  # eliminate one move
            else:
                o += [m]
        
        except IndexError:
            break
    return o