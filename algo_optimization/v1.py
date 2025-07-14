from copy import deepcopy

class State:
    def __init__(self, pistonState='pppppppppppppppppppppppp  f                  b ', observerState='ooooo', zeroOffset=None):
        self._originalInputs = deepcopy((pistonState, observerState, zeroOffset))
        
        if zeroOffset is None:
            for i in range(len(pistonState)):
                if pistonState[i] == 'f':
                    zeroOffset = -i
                    break
        if zeroOffset is None:
            for i in range(len(pistonState)):
                if pistonState[i].isupper():
                    zeroOffset = -i
                    break

        self.p = {i + zeroOffset: pistonState[i].lower() if pistonState[i] != 'f' else ' ' for i in range(len(pistonState))}
        self.p.update({max(self.p.keys()) + 1: ' '})  # Adding whitespace
        self.p.update({max(self.p.keys()) + 1: ' '})  # Adding whitespace

        self.observers = {-3 - oi: observerState[oi] for oi in range(len(observerState))}
        self.moves = []
        
    def basicRepr(self):
        return ''.join(self.p.values())

    def basicReprWithF(self):
        newp = self.p.copy()
        if newp[0] == ' ':
            newp[0] = 'f'
        else:
            newp[0] = newp[0].upper()
        return ''.join(newp.values())

    def fullRepr(self):
        return ''.join(self.p.values()) + 100 * ' ' + '\n' + (
                    ' ' * (min(self.observers.keys()) - min(self.p.keys()))) + ''.join(
            reversed(self.observers.values())) + '  f\n'

    def __repr__(self):
        if self.moves and self.moves[-1] == -1:
            return '-----'
        return self.basicReprWithF()

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
        elif isinstance(move, int):
            if move == 8 * 9:
                return

            # Piston Move
            assert isinstance(move, int)
            assert move <= -2
            self.applyPowerPiston(move)
        elif isinstance(move, State):
            self.setNewState(deepcopy(move))
        elif isinstance(move, str):
            pass  # Custom Move
        else:
            assert False  # All moves should be one of the above types
    
    def applyPowerPiston(self, piston):
        if self.p[piston] == 'p':
            if self.p[piston + 1] == ' ':
                self.p[piston + 1], self.p[piston + 2] = self.p[piston + 2], self.p[piston + 1]
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
    
    def setNewState(self, newState):
        self.p = newState.p
        self.observers = newState.observers

    def applyCustomMove(self, move):
        self.applyMove(str(move))

    def applyCustomMoves(self, moves):
        for move in moves:
            self.applyCustomMove(move)

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
        """Returns the position of the topmost unused (i.e. not in the main stack) observer"""
        return max(i for i in self.observers.keys() if self.observers[i] != ' ')
    
    def isCompactPistonwise(self, below=float('infinity')):
        return all(self.p[i] == 'p' for i in range(min(self.p.keys()), self.getTopmostPiston(below)))
    def isCompact(self, below=float('infinity')):
        return self.isCompactPistonwise(below) and all(self.p[i] != 'o' for i in range(min(self.p.keys()), min(below, 1 + max(self.p.keys()))))


def moveBlockDown(b, state: State):
    assert state.p[b] != ' '

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
                moveBlockUpTo(topmostPiston, b - 2, state)
                moveBlockDown(b, state)

def moveBlockUp(b, state: State):
    assert state.p[b] != ' '

    topmostPiston = state.getTopmostPiston(below=b)
    topmostObserver = state.getTopmostObserver(below=b)
    if topmostObserver > topmostPiston:
        # Only need to move observers out of the way if they will do an unwanted pulse
        
        while (topmostObserver := state.getTopmostObserver(below=b)) != state.getTopUnusedObserver() + 1:
            moveBlockDown(topmostObserver, state)
        state.applyMove((topmostObserver,))
        moveBlockUp(b, state)
    
    else:
        match b - topmostPiston:
            case 1:
                powerPiston(topmostPiston, state)
            case 2:
                moveBlockUp(topmostPiston, state)
                powerPiston(topmostPiston + 1, state)

            case _:
                numPistons = 0
                i = None
                for i in range(b - 1, min(state.p.keys()), -1):
                    if state.p[i] == 'p':
                        numPistons += 1
                    if numPistons > (b - i) / 2:
                        break
                for j in range(i, b, 2):
                    powerPiston(j, state)

def powerPiston(piston, state: State):
    assert state.p[piston] == 'p'

    # Direct Powering
    if piston <= -2:
        if piston < -6 and piston % 2:
            if state.p[piston + 1] == ' ':
                state.applyMove(piston)
            else:
                state.applyMove(piston - 1)
        else:
            state.applyMove(piston)
        return

    topmostObserver = state.getTopmostObserver(below=piston)
    topmostPiston = state.getTopmostPiston(below=piston)

    if topmostObserver > topmostPiston:
        match piston - topmostObserver:
            case 1:
                moveBlockDownTo(topmostObserver, -2, state)
                while (topmostObserver := state.getTopmostObserver(below=piston)) != state.getTopUnusedObserver() + 1:
                    moveBlockDown(topmostObserver, state)
                state.applyMove((state.getTopUnusedObserver() + 1,))
                powerPiston(piston, state)
            case 2:
                moveBlockUp(topmostObserver, state)
            case _:
                # Todo: could be optimized
                moveBlockUp(topmostObserver, state)
                powerPiston(piston, state)

    elif topmostPiston < state.getTopUnusedObserver():
        state.applyMove((state.getTopUnusedObserver(),))
        powerPiston(piston, state)

    elif topmostPiston > topmostObserver:
        # Moving pistons out of the way for observer
        moveBlockDownTo(topmostPiston, -2, state)
        while (topmostPiston := state.getTopmostPiston(piston)) >= state.getTopUnusedObserver():
            moveBlockDown(topmostPiston, state)
        powerPiston(piston, state)


def moveBlockDownTo(bi, bf, state: State):
    # Normal handling
    for i in range(bi, bf, -1):
        moveBlockDown(i, state)

def moveBlockUpTo(bi, bf, state):
    for i in range(bi, bf):
        moveBlockUp(i, state)

def moveBlockTo(bi, bf, state):
    if bf < bi:
        moveBlockDownTo(bi, bf, state)
    if bf > bi:
        moveBlockUpTo(bi, bf, state)

def moveUpToAndPower(bi, bf, state):
    for i in range(bi, bf):
        moveBlockUp(i, state)
    powerPiston(bf, state)


if __name__ == "__main__":
    from fileHelperFunctions import logString
    from time import time_ns
    import simplify2
    from rust_simplify import run_moves_through_rust

    begin1 = time_ns()
    door1 = State('pppppppppp  f    b  ')
    moveBlockDownTo(5, -2, door1)

    door1.moves = run_moves_through_rust(door1.moves)
    end1 = time_ns()

    # Display
    odoor = door1.originalState
    for m in door1.moves:
        odoor.applyMove(m)
        print(f'{odoor} | {m}\n')
    
    # Large
    begin2 = time_ns()
    door2 = State('pppppppppppppppppppppppppp  f         b  ')
    moveBlockDownTo(10, -2, door2)
    # door2.moves = simplify2.repeatSimplification(door2.moves, door2.originalState, simplify2.oneAtATime, prnt=True, timeLimit=100)
    door2.moves = run_moves_through_rust(door2.moves)
    end2 = time_ns()

    l1 = len(door1.moves)
    l2 = len(door2.moves)
    print('---')
    print(f'{l1}/386, {l2}/16595')
    print(f'{100*(1-(l1 + l2)/(386+16595)):.2f}% Improvement!')
    print(f'Took {0.000001 * (end1 - begin1):.2f}ms, {0.000001 * (end2 - begin2):.2f}ms')

