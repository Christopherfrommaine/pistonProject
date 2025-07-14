from copy import deepcopy
from algorithm import State
from time import time
from conversion import applyCorrections

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
    def oneAtATime(moves, originalState: State):
        if len(moves) < n:
            return moves

        finalState = deepcopy(originalState)
        finalState.applyMoves(moves)

        for i in range(0, len(moves) - n, step=max(1, round(n / 1000))):
            cont = False
            for j in range(i, i + n):
                if not isinstance(moves[j], int) and not isinstance(moves[j], tuple):
                    cont = True
                    break
            if cont:
                continue

            newMoves = moves[:i] + moves[i + n:]

            odoor = deepcopy(originalState)
            try:
                odoor.applyMoves(newMoves)
                assert odoor.fullRepr() == finalState.fullRepr()

                applyCorrections(odoor.moves, odoor.originalState)

            except AssertionError:
                continue

            return newMoves
        return moves
    return oneAtATime

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
def nAtATimePar(n):
    def outputFunction(moves, originalState: State):
        if len(moves) < n:
            return moves

        finalState = deepcopy(originalState)
        finalState.applyMoves(moves)
        
        res = parallelCompute(predicate, len(moves) - n, [moves, n, originalState, finalState])
        
        if res:
            moves = moves[:res] + moves[res + n:]

        return moves
    return outputFunction


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