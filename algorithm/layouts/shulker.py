from algorithm.fileHelperFunctions import logString

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
    globalEndSeq = []
    shulkerInitSeq = [0]
    shulkerEndSeq = []
    afterPauseSeq = [0, 0] * 1

    # Create value list
    values = globalInitSeq
    for m in moves:
        values += [m // 8, m % 8]

        # After pause, add some space
        if m == 9 * 8:
            values += afterPauseSeq
    values += globalEndSeq

    # Ending pause insertion
    if 9 not in values:
        print("Moves has no stop sequence 9. Appending [9, 0].")
        values += [9, 0]

    if logging:
        logString('values: ' + str(values))

    # convert values to discs
    discs = [numtodisc[v] for v in values]

    # Generate disc shulker init and end sequences
    BOX_INIT = [numtodisc[i] for i in shulkerInitSeq]
    BOX_END = [numtodisc[i] for i in shulkerEndSeq]

    # Calculate maximum number of discs per box before the ending (MUST BE EVEN to ensure pairs are added)
    max_box_len = 2 * ((25   - len(BOX_END)) // 2)
    
    # Separate discs into boxes
    boxes = [BOX_INIT.copy()]
    disci = 0
    while disci < len(discs):
        # Add single disc
        boxes[-1].append(discs[disci])

        if discs[disci] == numtodisc[9] and discs[disci + 1] == numtodisc[8]:
            disci += 1
            boxes[-1] += [numtodisc[0]] * (27 - len(boxes[-1]))
            boxes.append(BOX_INIT.copy())
        
        # Box is full! Add new empty box
        if len(boxes[-1]) > max_box_len:
            boxes[-1] += BOX_END.copy()
            boxes.append(BOX_INIT.copy())

        disci += 1

    for box in boxes:
        assert 0 <= len(box) <= 27, f"{box}, {len(box)}"

    # Remove empty boxes
    while len(boxes[-1]) <= len(BOX_END + BOX_INIT):
        boxes.pop()

    for boxi in range(len(boxes)):
        boxes[boxi] += [discs[0]] * (27 - len(boxes[boxi]))

    for box in boxes:
        assert len(box) == 27, f"{box}, {len(box)}"

    
    if logging:
        logString('boxes: ' + str(boxes))
        logunrawboxes = lambda boxes: logString('unraw boxes: \n   [' + '\n    '.join(str([disctonum.get(elem) for elem in box]) for box in boxes) + '\n]')
        logunrawboxes(boxes)

    # Set small carts test
    small_carts_test = False
    if small_carts_test:
        print("SMALL CARTS TEST! INEFFICIENT PACKING.")
    

    assert(len(boxes) > 0)

    # Generate carts from boxes
    carts = [[]]
    boxi = 0
    while boxi < len(boxes):

        # Add single box
        carts[-1].append(boxes[boxi])

        # If pausing, fill the rest of the box with zeros
        if numtodisc[9] in boxes[boxi]:
            carts[-1].append([numtodisc[8]] * 27)
            carts[-1].append([numtodisc[8]] * 27)
            carts.append([])

        # If full, add new cart
        if len(carts[-1]) >= 26 or (small_carts_test and len(carts[-1]) >= 4):
            carts.append([])

        boxi += 1

    # # Remove zero boxes from beginnging of carts
    # for cart in carts:
    #     while cart and all(disc == numtodisc[8] for disc in cart[0]):
    #         del cart[0]

    # Remove empty/trivial carts
    carts = [cart for cart in carts if len(cart)]

    if len(carts[-1]) == 1 and all(i == numtodisc[8] for i in carts[-1][0]):
        carts.pop()

    if logging:
        logString('carts: ' + str(carts))

        logString('unraw carts: \n')
        for cart in carts:
            logunrawboxes(cart)
        logString('unraw carts end')

    
    print(f"{len(moves)} input moves, {len(boxes)} raw boxes, {len(carts)} carts")
    print(f"{sum(sum(len(box) for box in cart) for cart in carts) // 2} moves, {sum(len(cart) for cart in carts)} boxes, {len(carts)} carts")

    if logging:
        logString("\n" + ("\n".join(str(i) for i in carts)) + "\n")

    totalOutputDiscs = 0
    totalOutputZeros = 0
    thing = False
    for cart in carts:
        for box in cart:
            totalOutputDiscs += len(box)
            for i in range(0, len(box) - 1, 2):
                if box[i] == 'stal' and box[i + 1] == 'stal':
                    totalOutputZeros += 1
                
    print(f"Total output discs: {totalOutputDiscs}, {(100*totalOutputZeros/totalOutputDiscs):.2f}% are Padding")
    
    if totalOutputDiscs > 30000:
        print(f"Reduced from naive by {100*((205011-totalOutputDiscs)/205011):.2f}%")

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
            command += '{Slot:' + str(boxi) + 'b,id:"minecraft:shulker_box",count:1,components:{"minecraft:container":['

            for disci, disc in enumerate(box):
                assert 0 <= disci < 27
                command += '{slot:' + str(disci) + ',item:{id:"minecraft:music_disc_' + disc + '",count:1}},'

            command += ']}},'

        command += ']}'

        o.append(command)

    return o
