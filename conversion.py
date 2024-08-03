import layouts.original


def toLayoutMoves(moves, layout):
    o = []
    for m in moves:
        match layout:
            case 'original':
                o.append(layouts.original.toLayoutMove(m))
            case _:
                raise Exception('unsupported layout')


def toLayoutCommands(moves, layout, *args):
    match layout:
        case 'original':
            return layouts.original.toLayoutCommands(moves, *args)
        case _:
            raise Exception('unsupported layout')


def applyCorrections(moves, originalState):
    pass  # TODO


def fixQuasiconnectivity(moves, originalState):
    o = []
    for mi, m in enumerate(moves):
        if isinstance(m, tuple):
            # Observer move
            observer, = m
            for i in range(observer, -2):
                state = originalState.originalState
                state.applyMoves(moves[:mi])
                if state.p[i] == ' ':
                    o += [(i,)]
                else:
                    break
        else:
            # Piston Moves
            o += [m]
    return o
