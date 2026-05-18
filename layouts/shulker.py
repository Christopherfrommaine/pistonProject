from fileHelperFunctions import logString

numtodisc = ['stal', '13', 'cat', 'blocks', 'chirp', 'far', 'mall', 'mellohi', 'stal', 'strad', 'ward', '11', 'wait',
             'pigstep', 'otherside', '5']
disctonum = {numtodisc[i]: i for i in range(len(numtodisc))}


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
    shulkerEndSeq = [0, 0]

    values = globalInitSeq
    for m in moves:
        values += [m // 8, m % 8]
        
        if m == 9 * 8:
            values += [0, 0] * 16
    
    if 9 not in values:
        print("Moves has no stop sequence 9. Appending [9, 0].")
        values += [9, 0]

    if logging:
        logString('values: ' + str(values))

    discs = [numtodisc[v] for v in values]

    BOX_INIT = [numtodisc[i] for i in shulkerBeginSeq]
    BOX_END = [numtodisc[i] for i in shulkerEndSeq]
    boxes = [BOX_INIT.copy()]
    disci = 0
    while disci < len(discs):
        boxes[-1].append(discs[disci])

        max_box_len = 1 + 2 * ((27 - len(BOX_INIT) - len(BOX_END)) // 2)

        # If going to stop
        # if discs[disci] == numtodisc[9]:
        #     # Finish off the box with [... 0, 9, 0, 0, 0, 0, END]
        #     if len(boxes) + 4 <= max_box_len:
        #         boxes[-1] += [numtodisc[8]] * 4
        #     boxes[-1] += BOX_END.copy()
            
        #     # # Add a new box with [INIT, 0, 0, ... 0, 0, END]
        #     # boxes.append(BOX_INIT.copy())
        #     # boxes[-1] += [numtodisc[8]] * 4
        #     # boxes[-1] += BOX_END.copy()

        #     # Add a new box
        #     boxes.append(BOX_INIT.copy())

        if len(boxes[-1]) == max_box_len:
            boxes[-1] += BOX_END.copy()
            boxes.append(BOX_INIT.copy())

        disci += 1
    
    while len(boxes[-1]) <= len(BOX_END + BOX_INIT):
        boxes.pop()
    thing = False
    while boxes[-1] == [numtodisc[8]] * len(boxes[-1]):
        thing = True
        boxes.pop()
    if thing:
        boxes.append([numtodisc[8]] * len(boxes[-1]))
    
    if len(boxes) >= 1:
        boxes[-1] = boxes[-1] + ([0] * (len(boxes[-1]) - len(boxes[1])))

    if logging:
        logString('boxes: ' + str(boxes))
    if logging:
        logunrawboxes = lambda boxes: logString('unraw boxes: \n   [' + '\n    '.join(str([disctonum.get(elem) for elem in box]) for box in boxes) + '\n]')
        logunrawboxes(boxes)
    
    small_carts_test = True
    if small_carts_test:
        print("SMALL CARTS TEST! INEFFICIENT PACKING.")
    

    assert(len(boxes) > 0)
    carts = [[]]
    boxi = 0
    while boxi < len(boxes):
        carts[-1].append(boxes[boxi])

        if numtodisc[9] in boxes[boxi]:
            # boxi += 1
            # carts[-1].append(boxes[boxi])
            # if len(carts[-1]) <= 2:
            #     carts[-1].append(boxes[boxi])
            # carts.append([boxes[boxi]] * 3)
            # carts.append([])
            carts[-1].append([numtodisc[8]] * (max_box_len + len(BOX_END)))
            carts.append([])
        elif len(carts[-1]) == 26 or (small_carts_test and len(carts[-1]) >= 4):
            carts.append([])

        boxi += 1

    if len(carts[-1]) == 0:
        carts.pop()
    if len(carts[-1]) == 1 and all(i == numtodisc[8] for i in carts[-1][0]):
        carts.pop()

    if logging:
        logString('carts: ' + str(carts))
    if logging:
        logString('unraw carts: \n')
        for cart in carts:
            logunrawboxes(cart)
        logString('unraw carts end')

    
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
