from fileHelperFunctions import logString

numtodisc= ['stal', '13', 'cat', 'blocks', 'chirp', 'far', 'mall', 'mellohi', 'stal', 'strad', 'ward', '11', 'wait', 'pigstep', 'otherside', '5']


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
    valuePairs = [[m % 8, m //8] for m in moves]
    
    if logging:
        logString(f'valuePairs: {valuePairs}')
    
    # First Cart Begin
    cart = [0]
    
    cartLog = []
    minecarts = []
    i = 0
    while i < len(valuePairs):
        cart += [valuePairs[i]]
        i += 1

        if len(flatCart := flatten(cart)) >= 25:
            
            # Cart End
            flatCart += []

            minecarts.append(flatCart)
            cartLog.append(cart)

            # Cart Begin
            cart = [0, 0, 0, 0]
    
    if logging:
        logString(f'Cart Log: {cartLog}')
        logString(f'Minecarts: {minecarts}')

    o = []
    for minecartValues in minecarts:
        discList = [numtodisc[val] for val in minecartValues]

        nbt = ''
        for discIndex in range(len(discList)):
            nbt += '{' + f'id:"minecraft:music_disc_{discList[discIndex]}",Count:1b,Slot:{discIndex}' + '},'
        nbt = nbt[:-1]

        o.append('/summon minecraft:chest_minecart -272 -9 -80 {Items:[' + nbt + ']}')

    return o
