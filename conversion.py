import layouts.original


def toLayoutMoves(moves, layout):
    o = []
    for m in moves:
        match layout:
            case 'original':
                o.append(layouts.original.toLayoutMove(m))
            case _:
                raise Exception('unsupported layout')
    return o


def toLayoutCommands(moves, layout, *args):
    match layout:
        case 'original':
            return layouts.original.toLayoutCommands(moves, *args)
        case _:
            raise Exception('unsupported layout')


def applyCorrections(moves, originalState):
    state = originalState
    o = []
    for mi, m in enumerate(moves):
        if isinstance(m, tuple):
            # Observer move
            observer, = m
            for i in range(observer, -2):
                if state.p[i] == ' ':
                    o += [(i,)]
                else:
                    break
        else:
            # Piston Moves TODO
            if m >= -6 or m % 2 == 0:
                o += [m]
            else:
                if state.p[m + 1] == ' ':
                    o += [m + 1]
                else:
                    o += [m - 1, m - 1]

        state.applyMove(m)
    return o
