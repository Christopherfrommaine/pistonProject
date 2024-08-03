def toLayoutMove(m):
    if isinstance(m, tuple):
        # Observer Move
        observer, = m
        return [18 + observer]
    else:
        # Piston Move
        if -6 <= m <= -2:
            return [12 + m]
        else:
            if m % 2 == 0:
                return [(18 + m) // 2]
            else:
                raise Exception('Input move not supported for layout: odd-valued move for low pistons')


def toLayoutCommands(moves, xoffset=0, zoffset=0):
    o = []
    counter = 0
    xcoord, zcoord = None, None
    for m in moves:
        fillLevels = [m % 7 + 1, m // 7 + 1]

        for fl in fillLevels:
            index = counter + zoffset
            zcoord = -76 + index % 60
            xcoord = -103 - index // 60 + xoffset
            o.append(f'/setblock {xcoord} 250 {zcoord} composter[level={fl}]')

            counter += 1

    o.append(f'/setblock {xcoord} 250 {-76 + 60} gold_block')
    return o
