from fileHelperFunctions import logString

numtodisc = ['stal', '13', 'cat', 'blocks', 'chirp', 'far', 'mall', 'mellohi', 'stal', 'strad', 'ward', '11', 'wait',
             'pigstep', 'otherside', '5']


def flatten(l):
    o = []
    for i in l:
        if isinstance(i, list):
            o += i
        else:
            o.append(i)
    return o


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

    values = [0, 0, 0, 0]
    for m in moves:
        values += [m // 8, m % 8]

    discs = [numtodisc[v] for v in values]

    boxes = [[]]
    disci = 0
    while disci < len(discs):
        boxes[-1].append(discs[disci])

        if len(boxes[-1]) == 26:
            boxes[-1].append(numtodisc[0])
            boxes.append([])

        disci += 1

    carts = [[]]
    boxi = 0
    while boxi < len(boxes):
        carts[-1].append(boxes[boxi])

        if len(boxes[-1]) == 27:
            carts.append([])

        boxi += 1

    o = []
    for cart in carts:
        # Example:
        '''
        / summon
        minecraft: chest_minecart ~ ~ ~ {Items: [
            {Slot: 0b, id: "minecraft:shulker_box", Count: 1b, tag: {BlockEntityTag: {Items: [
                {Slot: 0b, id:"minecraft:music_disc_stal", Count: 1b},
                {Slot: 1b, id: "minecraft:music_disc_stal", Count: 1b}
            ]}}}
        ]}
        '''

        command = '/summon minecraft:chest_minecart -272 -9 -80 {Items:['

        for boxi, box in enumerate(cart):
            command += '{Slot:' + str(boxi) + 'b,id:"minecraft:shulker_box",Count:1b,tag:{BlockEntityTag: {Items: ['

            for disci, disc in enumerate(box):
                command += '{Slot:' + str(disci) + 'b,id:"minecraft:music_disc_' + disc + '",Count:1b},'

            command += ']}}},'

        command += ']}'

        o.append(command)

    return o
