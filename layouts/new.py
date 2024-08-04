# TODO

def toLayoutMove(moves):
    o = []
    for m in moves:
        if isinstance(m, tuple):
            # Observer Move
            observer, = m
            o += [18 + observer]
        else:
            # Piston Move
            if -6 <= m <= -2:
                o += [12 + m]
            else:
                if m % 2 == 0:
                    o += [(18 + m) // 2]
                else:
                    raise Exception('Input move not supported for layout: odd-valued move for low pistons')
    o += [48]  # End run code
    return o


def toLayoutCommands(moves, xoffset=0, zoffset=0):
    o = []
    counter = 0
    xcoord, zcoord = None, None
    for m in moves:
        fillLevels = [m % 7 + 1, m // 7 + 1]

        # print(fillLevels)

        for fl in fillLevels:
            index = counter + zoffset
            zcoord = -76 + index % 60
            xcoord = -103 - index // 60 + xoffset
            o.append(f'/setblock {xcoord} 250 {zcoord} composter[level={fl}]')

            counter += 1

    o.append(f'/setblock {xcoord} 250 {-76 + 60} gold_block')
    o.append('/setblock -8 90 -62 minecraft:redstone_block')
    return o
