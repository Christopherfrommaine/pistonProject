from algorithm import State

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


def simplifyUncorrectedMoves(moves, state: State):
    # return moves


    originalrep = state.fullRepr()

    o = moves
    changed = True

    while changed:
        print("simplifying step...")

        changed = False

        for i in range(len(o)):
            for j in range(i + 1, min(len(o), i + 50)):
                new = o[:i] + o[j:]

                if not any(isinstance(n, str) for n in new):
                    s = state.originalState
                    try:
                        s.applyMoves(new)
                        if s.fullRepr() == originalrep:
                            o = new
                            changed = True
                    except Exception as e:
                        pass
    
    return o