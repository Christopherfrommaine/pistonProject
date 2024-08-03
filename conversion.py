import layouts.original


def toLayoutMoves(moves, layout):
    match layout:
        case 'original':
            return layouts.original.toLayoutMove(moves)
        case _:
            raise Exception('unsupported layout')


def toLayoutCommands(moves, layout, *args):
    match layout:
        case 'original':
            return layouts.original.toLayoutCommands(moves, *args)
        case _:
            raise Exception('unsupported layout')


def applyCorrections(moves, state):
    o = []
    for m in moves:
        if isinstance(m, tuple):
            # Observer move
            observer, = m
            if observer != -3:
                pass
            for i in range(observer, -2):
                if state.p[i] == ' ' or i == observer:
                    o += [(i,)]
                else:
                    o += [(i,)]
                    break
        else:
            # Piston Moves TODO
            if m >= -6 or m % 2 == 0:
                o += [m]
            else:
                if state.p[m + 1] == ' ':
                    o += [m + 1]
                else:
                    if state.p[m - 1] == 'p':
                        o += [m - 1, m - 1]
                    elif state.p[m - 2] == 'p' and state.p[m - 3] == 'p':
                        o += [m - 3, m - 1, m - 1, m - 3]
                    else:
                        o += 'manualinterventionneededhere'
                        print(f'shoot! the lower piston pushing doesnt work out easily. Manual intervention needed around {len(o)}\nwell... um, here is you piston state: {state.fullRepr()}, \n and here are your output moves so far: {o}')

        state.applyMove(m)
    return o
