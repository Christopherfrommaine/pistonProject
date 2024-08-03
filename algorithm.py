class State:
    def __init__(self, pistonState='pppppppppppppppppppppppp  f                  b ', observerState='oooo', zeroOffset=None):
        self._originalInputs = (pistonState, observerState, zeroOffset)
        
        if zeroOffset is None:
            for i in range(len(pistonState)):
                if pistonState[i] == 'f':
                    zeroOffset = -i
                    break

        self.p = {i + zeroOffset: pistonState[i] if pistonState[i] != 'f' else ' ' for i in range(len(pistonState))}
        self.p.update({max(self.p.keys()) + 1: ' '})  # Adding whitespace
        self.p.update({max(self.p.keys()) + 1: ' '})  # Adding whitespace

        self.observers = {-3 - oi: observerState[oi] for oi in range(len(observerState))}
        self.moves = []
        
    def basicRepr(self):
        return ''.join(self.p.values())

    def __repr__(self):
        return ''.join(self.p.values()) + 100 * ' ' + '\n' + (' ' * (min(self.observers.keys()) - min(self.p.keys()))) + ''.join(reversed(self.observers.values())) + '  f\n'
    
    @property
    def originalState(self):
        return State(*self._originalInputs)

    def applyMove(self, move):
        self.moves.append(move)
        if isinstance(move, tuple):
            # Observer move
            observer, = move
            if self.observers[observer] == 'o':
                assert self.p[observer] == ' '

                self.observers[observer] = ' '
                self.p[observer] = 'o'

                self.applyPowerPiston(observer + 1)
            else:
                assert self.p[observer] == 'o'

                self.observers[observer] = 'o'
                self.p[observer] = ' '

        else:
            # Piston Move
            assert isinstance(move, int)
            assert move <= -2
            self.applyPowerPiston(move)

    def applyPowerPiston(self, piston):
        if self.p[piston] == 'p':
            if self.p[piston + 1] == ' ':
                self.p[piston + 1], self.p[piston + 2] =self.p[piston + 2], self.p[piston + 1]
                return

            maxBlockMoved = piston
            for block in range(piston + 1, piston + 13):
                if self.p[block] == ' ':
                    maxBlockMoved = block - 1
                    break

            if maxBlockMoved == piston:
                # Push Limit
                return

            updates = []
            if self.p[piston + 1] == 'o':
                updates.append(piston + 1)  # Weird quirk I found with single-ticking pistons update order

            for b in range(maxBlockMoved, piston, -1):
                self.p[b + 1] = self.p[b]
                if self.p[b + 1] == 'o':
                    updates.append(b + 1)
            self.p[piston + 1] = ' '

            for update in updates:
                if self.p[update + 1] == 'p':
                    self.applyPowerPiston(update + 1)
                    break

    # Helper Functions

    def applyMoves(self, moves):
        for move in moves:
            self.applyMove(move)

    def getTopmostChar(self, char, below):
        o = float('-infinity')
        for i in self.p.keys():
            if self.p[i] == char and i < below:
                o = i
        return o

    def getTopmostPiston(self, below=float('infinity')):
        return self.getTopmostChar('p', below)
    def getTopmostObserver(self, below=float('infinity')):
        return self.getTopmostChar('o', below)
    def getTopUnusedObserver(self):
        return max(i for i in self.observers.keys() if self.observers[i] != ' ')


def moveBlockDown(b, state):
    assert isinstance(state, State)

    topmostObserver = state.getTopmostObserver(below=b)
    topmostPiston = state.getTopmostPiston(below=b)

    if topmostObserver > topmostPiston:
        while (topmostObserver := state.getTopmostObserver(below=b)) != state.getTopUnusedObserver() + 1:
            moveBlockDown(topmostObserver, state)
        state.applyMove((state.getTopUnusedObserver() + 1,))
        moveBlockDown(b, state)

    else:
        match b - topmostPiston:
            case 1:
                moveBlockDown(topmostPiston, state)
                moveBlockDown(b, state)
            case 2:
                powerPiston(topmostPiston, state)
            case _:
                while (topmostPiston := state.getTopmostPiston(below=b)) != b - 2:
                    moveBlockUp(topmostPiston, state)
                moveBlockDown(b, state)


def moveBlockUp(b, state):
    assert isinstance(state, State)
    topmostPiston = state.getTopmostPiston(below=b)

    match b - topmostPiston:
        case 1:
            powerPiston(topmostPiston, state)
        case _:
            topmostObserver = state.getTopmostObserver(below=b)
            if topmostObserver != float('-infinity') and topmostObserver > topmostPiston:
                while (topmostObserver := state.getTopmostObserver(below=b)) != state.getTopUnusedObserver() + 1:
                    moveBlockDown(topmostObserver, state)
                state.applyMove((state.getTopUnusedObserver() + 1,))

            while (topmostPiston := state.getTopmostPiston(below=b)) != b - 1:
                moveBlockUp(topmostPiston, state)
            powerPiston(topmostPiston, state)


def powerPiston(piston, state):
    assert isinstance(state, State)

    if piston <= -2:
        state.applyMove(piston)
        return

    topmostObserver = state.getTopmostObserver(below=piston)
    topmostPiston = state.getTopmostPiston(below=piston)

    if topmostObserver > topmostPiston:
        match piston - topmostObserver:
            case 1:
                while (topmostObserver := state.getTopmostObserver(below=piston)) != state.getTopUnusedObserver() + 1:
                    moveBlockDown(topmostObserver, state)
                state.applyMove((state.getTopUnusedObserver() + 1,))
                powerPiston(piston, state)
            case 2:
                moveBlockUp(topmostObserver, state)
            case _:
                moveBlockUp(topmostObserver, state)
                powerPiston(piston, state)

    elif topmostPiston < state.getTopUnusedObserver():
        state.applyMove((state.getTopUnusedObserver(),))
        powerPiston(piston, state)

    elif topmostPiston > topmostObserver:
        # Moving pistons out of the way for observer
        moveBlockDown(topmostPiston, state)
        powerPiston(piston, state)


def moveBlockDownTo(bi, bf, state):
    for i in range(bi, bf, -1):
        moveBlockDown(i, state)

def moveBlockUpN(bi, bf, state):
    for i in range(bi, bf):
        moveBlockUp(i, state)

def moveBlockTo(bi, bf, state):
    if bf < bi:
        moveBlockDownTo(bi, bf, state)
    if bf > bi:
        moveBlockDownTo(bi, bf, state)


if __name__ == "__main__":
    # Testing Moves
    door = State()
    print(door)
    door.applyMove(-3)
    print(door)
    door.applyMove(-4)
    print(door)
    door.applyMove((-3,))
    print(door)
    door.applyMove((-3,))
    print(door)
    door.applyMove(-6)
    print(door)
    door.applyMove(-4)
    print(door)
    door.applyMove((-3,))
    print(door)

    print('longer sequence testing --------------')
    print('1 -> 0 move')
    door = State(pistonState='ppppp  fb  ')
    print(door)
    m = [8, 15, 8, 8, 15, 7, 9, 7, 8]
    modified = [-4, (-3,), -4, -4, (-3,), -5, -3, -5, -4]
    for move in modified:
        door.applyMove(move)
        print(door)

    print('2 -> 0 move')
    door = State(pistonState='pppppppp  f b  ')
    print(door)
    modified = [-4, (-3,), -5, -3, -3, -5, -4, (-3,), -6, -4, -2, -4, -6, -5, (-3,), -4]
    for move in modified:
        door.applyMove(move)
        print(door)

    print('4 -> 0 move')
    door = State(pistonState='pppppppp  f   b')
    print(door)
    modified = [
        -4, (-3,), -5, (-4,), -6, -4, -4, -4, -4, -6, -5, (-4,), -8, -5, -3, -5, -2, -4, -3, -8, -7, -6, -5, -4, (-3,),
        -8, -4, (-3,), -5, -3, -3, -5, -4, (-3,), -6, -4, -2, -4, -6, -3, -5, -4, -8, -7, -6, -5,
        (-3,), -6, -4, -2, -2, -4, -6, -3, -5, -4, (-3,),
        -8, -4, (-3,), -4, -4, (-3,),  # Works
        -5, -3, -5, -4, -8, -7, -6, -5, (-3,), -5, -3, -3, -5, -4, (-3,),
        -6, -4, -2, -4, -6, -5, (-3,), -4, -4, (-3,), -5, -3, -5, -4
    ]
    for m in modified:
        door.applyMove(m)
        print(door)

    print('programatically generated sequences --------')
    print('1 -> 0 move')
    door = State(pistonState='ppppp  fb  ')
    moveBlockDown(1, door)
    moves = door.moves
    door = State(pistonState='ppppp  fb  ')
    print(door)
    for m in moves:
        door.applyMove(m)
        print(door)

    print('2 -> 1 move')
    door = State(pistonState='ppppp  f b  ')
    moveBlockDown(2, door)
    moves = door.moves
    door = State(pistonState='ppppp  f b  ')
    print(door)
    for m in moves:
        door.applyMove(m)
        print(door)

    print('1 -> 0 move after 2 -> 1 move')
    door = State(pistonState='ppppp  f b  ')
    moveBlockDown(2, door)
    moveBlockDown(1, door)
    moves = door.moves
    door = State(pistonState='ppppp  f b  ')
    print(door)
    for m in moves:
        door.applyMove(m)
        print(door)

    print('4 -> 0 move')
    door = State(pistonState='ppppppppppp  f   b  ')
    moveBlockDown(5, door)
    moveBlockDown(4, door)
    moveBlockDown(3, door)
    moveBlockDown(2, door)
    moveBlockDown(1, door)
    moves = door.moves
    door = State(pistonState='ppppppppppp  f   b  ')
    print(door.basicRepr())
    for m in moves:
        door.applyMove(m)
        print(door.basicRepr())

