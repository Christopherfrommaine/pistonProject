from copy import deepcopy
from fileHelperFunctions import moveFromFile, logString

OPTIMIZED = False
OPTIMIZED2 = False
OPTIMIZED3 = False
MANUAL_OPT = True

class State:
    def __init__(self, pistonState='pppppppppppppppppppppppp  f                  b ', observerState='ooooo', zeroOffset=None):
        self._originalInputs = deepcopy((pistonState, observerState, zeroOffset))
        
        if zeroOffset is None:
            for i in range(len(pistonState)):
                if pistonState[i] == 'f':
                    if zeroOffset is not None:
                        assert False
                    zeroOffset = -i
        if zeroOffset is None:
            for i in range(len(pistonState)):
                if pistonState[i].isupper():
                    if zeroOffset is not None:
                        assert False
                    zeroOffset = -i
        
        pistonState = pistonState.strip()
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

    def applyMove(self, move, strict=False):

        # Strincter Asserts
        if strict:
            assert not any(self.p[i] == 'o' and self.p[i + 1] == 'o' for i in range(min(self.p.keys()), max(self.p.keys()) - 1))
            if isinstance(move, tuple):
                observer, = move
                
                if self.p[observer + 1] != ' ':
                    assert False

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
    def applyMoves(self, moves, strict=False):
        for move in moves:
            self.applyMove(move, strict)
    
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
    def getBottommostChar(self, char, above):
        o = float('infinity')
        for i in reversed(self.p.keys()):
            if self.p[i] == char and i > above:
                o = i
        return o

    def getTopmostPiston(self, below=float('infinity')):
        return self.getTopmostChar('p', below)
    def getTopmostObserver(self, below=float('infinity')):
        return self.getTopmostChar('o', below)
    def getTopUnusedObserver(self):
        """Returns the position of the topmost unused (i.e. not in the main stack) observer"""
        return max(i for i in self.observers.keys() if self.observers[i] != ' ')
    def getTopUnusedObserverSpace(self):
        """Returns the position of the topmost unused (i.e. not in the main stack) observer"""
        return self.getTopUnusedObserver() + 1
    
    
    def isCompactPistonwise(self, below=float('infinity')):
        return all(self.p[i] == 'p' for i in range(min(self.p.keys()), self.getTopmostPiston(below)))
    def isCompact(self, below=float('infinity')):
        return self.isCompactPistonwise(below) and all(self.p[i] != 'o' for i in range(min(self.p.keys()), min(below, 1 + max(self.p.keys()))))

def compactify(state, below=float('infinity')):
        topmostPiston = state.getTopmostPiston(below)
        topmostObserver = state.getTopmostObserver(below)

        if topmostObserver > topmostPiston:
            if topmostObserver > -2:
                moveBlockDownTo(topmostObserver, -2, state)
            while (topmostObserver := state.getTopmostObserver(below)) > state.getTopUnusedObserver():
                moveBlockDown(topmostObserver, state)
        else:
            if topmostPiston > -2:
                moveBlockDownTo(topmostPiston, -2, state)
            while not state.isCompact(below):
                topmostPiston = state.getTopmostPiston(below)
                moveBlockDown(topmostPiston, state)
        
        if not state.isCompact(below):
            compactify(state, below)

def moveBlockDown(b, state: State, destination=None):
    if MANUAL_OPT:
        import re
        def extract_pattern_values(string, pattern):
            regex_pattern = pattern \
                .replace('*', '(.+?)') \
                .replace('~', '(.+)')

            match = re.match(regex_pattern, string)
            if match:
                return match.groups()
            else:
                return None


        manualMatches = [
            ('general/1-3.txt',      '*ppppp   fp~',          'o*',     'p pppo pP ',          ' ooo'),
            ('general/2-3.txt',      '*ppppp   f p~',         'o*',     'p pp po Pp ',         ' ooo'),
            ('general/3-3.txt',      '*ppppp   f  p~',        'o*',     'p p p pofpp ',        ' ooo'),
            ('general/4-3.txt',      '*ppppp   f   p~',       'o*',     'p p po pO pp ',       '  oo'),
            ('general/5-3.txt',    '*ppppppp   f    p~',      'o*',   'p p pp po Po pp ',      '  oo'),
            ('general/6-3.txt',    '*ppppppp   f     p~',     'o*',   'p p p p pofpo pp ',     '  oo'),
            ('general/7-3.txt',    '*ppppppp   f      p~',    'o*',   'p p p po pO po pp ',    '   o'),
            ('general/8-3.txt',  '*ppppppppp   f       p~',   'o*', 'p p p pp po Po po pp ',   '   o'),
            ('general/9-3.txt',  '*ppppppppp   f        p~',  'o*', 'p p p p p pofpo po pp ',  '   o'),
            ('general/10-3.txt', '*ppppppppp   f         p~', 'o*', 'p p p p po pO po po pp ', '    '),

            ('general/1-4.txt',        '*pppp    fp~',          ' o*',       'p p po pP ',          '  oo'),
            ('general/2-4.txt',      '*pppppp    f p~',         ' o*',     'p p pp po Pp ',         '  oo'),
            ('general/3-4.txt',      '*pppppp    f  p~',        ' o*',     'p p p p pofpp ',        '  oo'),
            ('general/4-4.txt',      '*pppppp    f   p~',       ' o*',     'p p p po pO pp ',       '   o'),
            ('general/5-4.txt',    '*pppppppp    f    p~',      ' o*',   'p p p pp po Po pp ',      '   o'),
            ('general/6-4.txt',    '*pppppppp    f     p~',     ' o*',   'p p p p p pofpo pp ',     '   o'),
            ('general/7-4.txt',    '*pppppppp    f      p~',    ' o*',   'p p p p po pO po pp ',    '    '),
            
            ('general/1-5.txt',        '*ppppp     fp~',          '  o*',       'p p p po pP ',          '   o'),
            # ('general/2-5.txt',      '*ppppppp     f p~',         '  o*',     'p p p p ppo Pp ',         '   o'),
            ('general/3-5.txt',      '*ppppppp     f  p~',        '  o*',     'p p p p p pofpp ',        '   o'),
            ('general/4-5.txt',      '*ppppppp     f   p~',       '  o*',     'p p p p po pO pp ',       '    '),
        ]

        obsState = ''.join(i for i in state.observers.values())
        for mm in manualMatches:
            filename, stateMatch, obsMatch, outputState, outputObs = mm
            
            assert len(stateMatch) - 2 == len(outputState)
            assert len(list(i for i in stateMatch if i.lower() == 'p')) == len(list(i for i in outputState if i.lower() == 'p'))

            if res := extract_pattern_values(str(state), stateMatch):
                prelude, postlude = res
                if extract_pattern_values(obsState, obsMatch):
                    
                    newState = State(prelude + outputState + postlude, outputObs + 'oooo')
                    moveFromFile(state, filename, newState)
                    return


    if OPTIMIZED3 and state.isCompact(b):
        i = b - 1
        neededPistons = 0
        neededObservers = 0
        existingPistons = -1

        observerPositions = []

        sequencePosition = 'o'

        while neededPistons > existingPistons or not neededPistons:
            i -= 1

            sequencePosition = {'o': 'p', 'p': ' ', ' ': ('o' if i > -2 else 'p')}[sequencePosition]

            match sequencePosition:
                case 'p':
                    neededPistons += 1
                case 'o':
                    neededObservers += 1
                    observerPositions.append(i)
                case ' ':
                    pass
                case _:
                    raise AssertionError
            
            match state.p[i]:
                case 'p':
                    existingPistons += 1
                case 'o':
                    raise AssertionError
                case ' ':
                    pass
                case _:
                    raise AssertionError

        existingPistons -= neededObservers
        # i -= 1

        while neededObservers:
            unusedObserver = state.getTopUnusedObserver()
            state.applyMove(unusedObserver - 1)
            state.applyMove((unusedObserver,))
            neededObservers -= 1
        
        while existingPistons:
            i += 1
            if state.p[i] == 'p':
                state.applyMove(i)
                existingPistons -= 1

        for _ in range(2 ** len(observerPositions) - 1):
            state.applyMove(i)
        
        while observerPositions:
            op = observerPositions.pop()
            moveBlockTo(op, state.getTopUnusedObserverSpace(), state)
            state.applyMove((state.getTopUnusedObserverSpace(),))
        
        assert state.isCompact(b - 1)
        return

    topmostObserver = state.getTopmostObserver(below=b)
    topmostPiston = state.getTopmostPiston(below=b)

    if topmostObserver > topmostPiston:
        while (topmostObserver := state.getTopmostObserver(below=b)) != state.getTopUnusedObserverSpace():
            moveBlockDown(topmostObserver, state)
        state.applyMove((state.getTopUnusedObserverSpace(),))
        moveBlockDown(b, state)

    else:

        # New Optimization
        if OPTIMIZED and (b > 0 or destination and destination > 0) and (topmostPiston <= state.getTopUnusedObserver() or destination):
            moveBlockUpTo(topmostPiston, state.getTopUnusedObserverSpace(), state)
            topmostPiston = state.getTopmostPiston(below=b)
        
            if state.p[topmostPiston - 1] != ' ':
                moveBlockDown(topmostPiston - 1, state)
            
            state.applyMove((state.getTopUnusedObserver(),))
            
            moveBlockUpTo(topmostPiston, b - 2, state)

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

                    # Optimization
                    # pushUpToThenPower(topmostPiston, b - 2, state)

def moveBlockUp(b, state: State, destination=None):

    topmostPiston = state.getTopmostPiston(below=b)
    topmostObserver = state.getTopmostObserver(below=b)
    if topmostObserver > topmostPiston:
        # Only need to move observers out of the way if they will do an unwanted pulse
        if OPTIMIZED and (state.p[b] != 'p' or (state.p[b + 1] == ' ' and state.p[b + 2] == ' ')):
            # like, whatever man
            # its chill
            pass

        else:
            while (topmostObserver := state.getTopmostObserver(below=b)) != state.getTopUnusedObserverSpace():
                moveBlockDown(topmostObserver, state)
            state.applyMove((topmostObserver,))
            moveBlockUp(b, state, destination)
            return
    

    numInterleaving = sum(int(state.p[i] != ' ') for i in range(topmostPiston + 1, b)) if OPTIMIZED else 0

    match b - topmostPiston - numInterleaving:
        case 1:
            powerPiston(topmostPiston, state)
        case 2:
            moveBlockUp(topmostPiston, state)
            powerPiston(topmostPiston + 1, state)

        case _:
            # Optimization
            if destination:
                if all(state.p[i] == 'p' or state.p[i] == ' ' for i in range(min(state.p.keys()), destination - 1)):
                    numPistons = 0
                    i = None
                    for i in range(destination - 1, min(state.p.keys()), -1):
                        if state.p[i] == 'p':
                            numPistons += 1
                        if numPistons > (destination - i) / 2:
                            break
                    for j in range(i, destination, 2):
                        powerPiston(j, state)
                    return

            # Normal
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

    if piston <= -2:
        if piston < -6 and piston % 2:
            if state.p[piston + 1] == ' ':
                state.applyMove(piston)
            else:
                state.applyMove(piston - 1)
        else:
            state.applyMove(piston)

        return

    if MANUAL_OPT:
        import re
        def extract_pattern_values(string, pattern):
            regex_pattern = pattern \
                .replace('*', '(.+?)') \
                .replace('~', '(.+)')
            
            match = re.match(regex_pattern, string)
            if match:
                return match.groups()
            else:
                return None


        manualMatches = [
            (1, 'general/power_1.txt',     '*ppp   f~',       'o*',     'p p pof',       ' ooo'),
            (2, 'general/power_2.txt',     '*ppp   f ~',      'o*',     'p po pO ',      '  oo'),
            (3, 'general/power_3.txt',   '*ppppp   f  ~',     'o*',   'p pp po Po ',     '  oo'),
            (4, 'general/power_4.txt',   '*ppppp   f   ~',    'o*',   'p p p pofpo ',    '  oo'),
            (5, 'general/power_5.txt',   '*ppppp   f    ~',   'o*',   'p p po pO po ',   '   o'),
            (6, 'general/power_6.txt', '*ppppppp   f     ~',  'o*', 'p p pp po Po po ',  '   o'),
            (7, 'general/power_7.txt', '*ppppppp   f      ~', 'o*', 'p p p p pofpo po ', '   o'),
        ]

        obsState = ''.join(i for i in state.observers.values())
        for mm in manualMatches:
            index, filename, stateMatch, obsMatch, outputState, outputObs = mm
            if piston == index and (res := extract_pattern_values(str(state), stateMatch)):
                prelude, postlude = res

                if extract_pattern_values(obsState, obsMatch):
                    
                    newState = State(prelude + outputState + postlude, outputObs + 'oooo')
                    newState.applyPowerPiston(piston)
                    moveFromFile(state, filename, newState)
                    return

    topmostObserver = state.getTopmostObserver(below=piston)
    topmostPiston = state.getTopmostPiston(below=piston)

    if topmostObserver > topmostPiston:
        match piston - topmostObserver:
            case 1:
                # while (topmostObserver := state.getTopmostObserver(below=piston)) != state.getTopUnusedObserverSpace():
                #     moveBlockDown(topmostObserver, state)
                # state.applyMove((state.getTopUnusedObserverSpace(),))
                # powerPiston(piston, state)

                moveBlockDown(topmostObserver, state)
                powerPiston(piston, state)
            case 2:
                moveBlockUp(topmostObserver, state)
            case _:
                # New Optimization
                if topmostObserver - topmostPiston == 1:
                    moveBlockUp(topmostPiston, state, destination=piston-3)
                else:
                    # Todo: could be optimized
                    # moveBlockUp(topmostObserver, state, destination=piston-1)

                    moveBlockUpTo(topmostPiston, topmostObserver - 1, state)
                powerPiston(piston, state)

    elif topmostPiston < state.getTopUnusedObserver():
        state.applyMove((state.getTopUnusedObserver(),))
        powerPiston(piston, state)

    elif topmostPiston > topmostObserver:
        # Moving pistons out of the way for observer
        moveBlockDown(topmostPiston, state)
        powerPiston(piston, state)

def pushUpToThenPower(bi, bf, state: State):
    assert state.p[bi] == 'p'

    moveBlockUpTo(bi, bf, state)
    powerPiston(bf, state)
    return

    def basicCase():
        moveBlockUp(bi, state, destination=bf)
        if bi + 1 < bf:
            pushUpToThenPower(bi + 1, bf, state)
        else:
            powerPiston(bf, state)
    
    testState = State()
    testState.p = deepcopy(state.p)
    testState.observers = deepcopy(state.observers)

    # Optimized Case
    powerPiston(bi, testState)
    # There hopefully is now a
    # .....p op
    #         ^ bi      ^ bf

    # Goal:
    # .....          pop 
    #         ^ bi      ^ bf
    # Then:
    # .....          p op
    #         ^ bi      ^ bf

    # Check that the goal was actually acheived
    if ''.join(testState.p[i] for i in range(bi - 3, bi)) == 'p o':

        state.setNewState(testState)
        state.moves += testState.moves

        pushUpToThenPower(bi - 3, bf - 3, state)

    else:
        basicCase()


def moveBlockDownTo(bi, bf, state: State):

    topmostPiston = state.getTopmostPiston(below=bi)
    topmostObserver = state.getTopmostObserver(below=bi)

    if OPTIMIZED2:  # Tune the zero value. May work better with different cutoff
        if topmostPiston <= state.getTopUnusedObserverSpace() and topmostObserver < -100000:
            
            i = bi - 1  # Starts two below due to decrementation later
            necesaryPistons = []
            necesaryObservers = []
            existingPistons = []
            
            sequencePosition = 2  # Prev state is space below the block

            while len(necesaryPistons) > len(existingPistons) or not necesaryPistons:
                i -= 1

                # Inditect power with observer stack
                sequencePosition = ((sequencePosition + 1) % 3) if i > -2 else [1, 0, 0][sequencePosition]
                match sequencePosition:
                    case 0:
                        necesaryPistons.append(i)
                    case 1:
                        pass  # Space in between
                    case 2:
                        necesaryObservers.append(i)
                
                match state.p[i]:
                    case ' ':
                        pass
                    case 'p':
                        existingPistons.append(i)
                    case _:
                        raise AssertionError  # A "hopefully not" error
                    
            # -10v
            # ppppppppppp  f        b
            # ppppp p p p pfpo po p b

            existingPistons = list(reversed(existingPistons))
            
            # i is at a position such that extending all pistons works
            numObservers = 0
            while numObservers < len(necesaryObservers):
                nextPiston = existingPistons.pop()
                moveBlockTo(nextPiston, state.getTopUnusedObserverSpace(), state)
                state.applyMove((state.getTopUnusedObserver(),))
                numObservers += 1
            
            # All observers are in place
            i -= 1
            numPistons = 0
            while numPistons <= len(existingPistons) and not i > bi:
                i += 1
                if state.p[i] == 'p' and state.p[i + 1] != ' ':
                    powerPiston(i, state)
                    numPistons += 1

            
            for _ in range(2, 2 ** len(necesaryObservers)):
                powerPiston(i, state)

            moveBlockDownTo(bi - 1, bf, state)
        else:
            compactify(state, bi)
            moveBlockDownTo(bi - 1, bf, state)
    else:
        # Normal handling
        for i in range(bi, bf, -1):
            moveBlockDown(i, state, destination=bf)

def moveBlockUpTo(bi, bf, state):
    for i in range(bi, bf):
        moveBlockUp(i, state, destination=bf)

def moveBlockTo(bi, bf, state):
    if bf < bi:
        moveBlockDownTo(bi, bf, state)
    if bf > bi:
        moveBlockUpTo(bi, bf, state)

def retractCustom(customRetractionMoves, state: State, assrt=True):
    if assrt:
        assert state.p[-1] == 'b'
    state.applyCustomMoves(customRetractionMoves)

    # essentially doing this:
    # state.p[-1] = ' '
    newState = State(state.basicReprWithF(), ''.join(state.observers.values()))
    newState.p[-1] = ' '
    state.applyMove(newState)


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

