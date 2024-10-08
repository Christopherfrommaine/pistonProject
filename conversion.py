from layouts import original, new, shulker


def toLayoutMoves(moves, layout):
    match layout:
        case 'original':
            return original.toLayoutMoves(moves)
        case 'new':
            return new.toLayoutMoves(moves)
        case 'shulker':
            return shulker.toLayoutMoves(moves)
        case _:
            raise Exception('unsupported layout')


def toLayoutCommands(moves, layout, *args):
    match layout:
        case 'original':
            return original.toLayoutCommands(moves, *args)
        case 'new':
            return new.toLayoutCommands(moves, *args)
        case 'shulker':
            return shulker.toLayoutCommands(moves, *args)
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
                    if state.p[i + 1] == ' ':
                        break
                else:
                    o += [(i,)]
                    break
        elif isinstance(m, int):
            if m >= -6 or m % 2 == 0:
                o += [m]
            else:
                if state.p[m + 1] == ' ':
                    o += [m + 1]
                else:
                    o += ['manualinterventionneededhere']
                    print(f'shoot! the lower piston pushing doesnt work out easily. Manual intervention needed around {len(o)}\nwell... um, here is you piston state: {state.fullRepr()}, \n and here are your output moves so far: {o}')
        elif isinstance(m, str):
            o += [m]
        state.applyMove(m)
    return o
