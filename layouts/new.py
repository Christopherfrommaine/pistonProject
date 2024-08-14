numtodisc= ['stal', '13', 'cat', 'blocks', 'chirp', 'far', 'mall', 'mellohi', 'stal', 'strad', 'ward', '11', 'wait', 'pigstep', 'otherside', '5']


def toLayoutMoves(moves):
    o = []
    for m in moves:
        if isinstance(m, tuple):
            # Observer Move
            observer, = m
            o += [9 - observer]
        elif isinstance(m, int):
            # Piston Move
            if -6 <= m <= -2:
                o += [12 + m]
            else:
                if m % 2 == 0:
                    o += [(18 + m) // 2]
                else:
                    raise Exception('Input move not supported for layout: odd-valued move for low pistons')
        elif isinstance(m, str):
            try:
                o += [int(m)]
            except Exception:
                pass
    return o


def toLayoutCommands(moves, logging=False):
    log = []

    # At begin of first cart
    discs = [numtodisc[0], numtodisc[0]]

    for m in moves:
        log += [[m % 8, m // 8]]
        discs += [numtodisc[m % 8], numtodisc[m // 8]]

    if logging:
        from fileHelperFunctions import logString
        logString('Disc Signal Strength Pairs: ' + str(log))
        logString('Discs: ' + str(discs))

    minecarts = [[]]

    disci = 0
    while disci != len(discs):
        if len(minecarts[-1]) >= 26:

            # At end of each cart
            # minecarts[-1] += [numtodisc[0]]

            # At begin of each cart
            minecarts += [[numtodisc[0], numtodisc[0]]]
        minecarts[-1].append(discs[disci])
        disci += 1

    # First Minecart
    minecarts[0].pop(0)

    if logging:
        from fileHelperFunctions import logString
        logString('Minecarts: ' + str(minecarts))

    o = []
    for minecartList in minecarts:
        nbt = ''
        for discIndex in range(len(minecartList)):
            nbt += '{' + f'id:"minecraft:music_disc_{minecartList[discIndex]}",Count:1b,Slot:{discIndex}' + '},'
        nbt = nbt[:-1]

        o.append('/summon minecraft:chest_minecart -272 -9 -80 {Items:[' + nbt + ']}')

    return o
