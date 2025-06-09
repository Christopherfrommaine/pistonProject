from copy import deepcopy
from algorithm import State


def repeatSimplification(moves, originalState: State, simpFunc):
    finalState = deepcopy(originalState)
    finalState.applyMoves(moves)

    oldMoves = None
    while oldMoves != moves:
        print(f"step, {len(moves)}             ", end='')

        oldMoves = moves
        moves = simpFunc(moves, deepcopy(originalState))
        try:
            odoor = deepcopy(originalState)
            odoor.applyMoves(moves)
            assert odoor.fullRepr() == finalState.fullRepr()
        except:
            return oldMoves
    print()

    return moves


def contextAwareReplacementSimplification(moves, originalState: State):
    def firsteq(l1, l2):
        ln = min(len(l1), len(l2))
        return l1[:ln] == l2[:ln]

    state = originalState
    o = []
    mi = 0
    while mi < len(moves) - 1:
        mi += 1
        m = moves[mi]
        nextm = moves[mi:]
        
        if isinstance(nextm[0], int) and isinstance(nextm[1], int) and nextm[1] < nextm[0] and all(state.p[i] == 'p' for i in range(nextm[1], nextm[0] + 1)):
            o += [nextm[1]]
            mi += 1  # eliminate one move
        else:
            o += [m]
    return o