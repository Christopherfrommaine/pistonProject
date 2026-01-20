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
            # o += [9 - observer]
            o += [{-3: 15, -4: 14, -5: 13, -6: 12}[observer]]
        elif isinstance(m, int):
            if m == 8 * 9:
                o += [m]
                continue

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
    o += [9 * 8]
    return o


def toLayoutCommands(moves, logging=False):

    globalInitSeq = [0, 0]
    shulkerBeginSeq = [0]
    shulkerEndSeq = [0, 0, 0]
    globalEndSeq = [0, 9, 0, 0, 0, 0, 0, 0, 0, 0]

    # print("POSSIBLY REPLACTING MOVES WITH RANGE")
    # moves = list(range(64)) * 8

    values = globalInitSeq
    for m in moves:
        values += [m % 8, m // 8]
        
        if m == 9 * 8:
            values += [0, 0] * 14
    
    if 9 not in values:
        print("Moves not ended in stop sequence [9]. Appending ", globalEndSeq)
        values += globalEndSeq

    if logging:
        logString('values: ' + str(values))

    discs = [numtodisc[v] for v in values]


    BOX_INIT = [numtodisc[i] for i in shulkerBeginSeq]
    BOX_END = [numtodisc[i] for i in shulkerEndSeq]
    boxes = [BOX_INIT.copy()]
    disci = 0
    while disci < len(discs):
        boxes[-1].append(discs[disci])

        if len(boxes[-1]) == 1 + 2 * ((27 - len(BOX_INIT) - len(BOX_END)) // 2):
            boxes[-1] += BOX_END.copy()
            boxes.append(BOX_INIT.copy())

        disci += 1
    
    if len(boxes[-1]) == 0:
        boxes.pop()

    if logging:
        logString('boxes: ' + str(boxes))
    
    small_carts_test = True
    if small_carts_test:
        print("SMALL CARTS TEST! INEFFICIENT PACKING.")

    carts = [[]]
    boxi = 0
    while boxi < len(boxes):

        carts[-1].append(boxes[boxi])

        if len(carts[-1]) == 27 or (small_carts_test and len(carts[-1]) >= 4) or (numtodisc[9] in carts[-1][-1]):
            if (numtodisc[9] in carts[-1][-1]):
                carts.append([BOX_INIT.copy() + [numtodisc[8] for i in range(8)] + BOX_END.copy()] * 3)
            carts.append([])
            

        boxi += 1
    
    # print("\n\n".join(str(i) for i in carts))

    if len(carts[-1]) == 0:
        carts.pop()
    
    # for cart in carts:
    #     if len(cart) <= 2:
    #         cart.append([numtodisc[8] for i in range(8)])
    #         cart.append([numtodisc[8] for i in range(8)])

    if logging:
        logString('carts: ' + str(carts))
    
    print(f"{len(moves)} input moves, {len(boxes)} raw boxes, {len(carts)} carts")
    print(f"{sum(sum(len(box) for box in cart) for cart in carts) // 2} moves, {sum(len(cart) for cart in carts)} boxes, {len(carts)} carts")

    if logging:
        logString("\n" + ("\n".join(str(i) for i in carts)) + "\n")

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
            assert 0 <= boxi < 27
            command += '{Slot:' + str(boxi) + 'b,id:"minecraft:shulker_box",Count:1b,tag:{BlockEntityTag: {Items: ['

            for disci, disc in enumerate(box):
                assert 0 <= disci < 27
                command += '{Slot:' + str(disci) + 'b,id:"minecraft:music_disc_' + disc + '",Count:1b},'

            command += ']}}},'

        command += ']}'

        o.append(command)

    return o
