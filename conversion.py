def fixQuasiconnectivity(moves, originalState):
    o = []
    for m in moves:
        if isinstance(m, tuple):
            # Observer move
            observer, = m
            for i in range(observer, -2):
                if originalState.p[i] == ' ':
                    o += [(i,)]
                else:
                    break
        else:
            # Piston Moves
            o += [m]
    return o


def translateToPistonLayoutOriginal(m, originalState):
    if isinstance(m, tuple):
        # Observer Move
        observer, = m
        return 18 + observer
    else:
        # Piston Move
        if -6 <= m <= -2:
            return 12 + m
        else:
            # TODO: May not work in cases where the non-quasi piston powers first.
            # state is passed in, so I should be able to do checks, but idk. Itll probably be hard to figure out
            print("The lower piston translation isnt really working right. IDK you should probably work on it")
            
            # -7 -> 6
            # -8 -> 5
            # -9 -> 5
            # -10 -> 4
            # -11 -> 4
            
            return (19 + m) // 2



def translateToPistonLayout(moves, originalState, layout='original'):
    o = []
    for m in moves:
        match layout:
            case 'original':
                o.append(translateToPistonLayoutOriginal(m, originalState))
            case _:
                raise Exception("Nonexistent Layout Specified")
    return o

def writeToFile(string, path='output.txt'):
    with open(path, "w") as file:
        source_code = file.write(str(string))



def fullTranslation(moves, state, layout='original', filePath='output.txt'):
    writeToFile(translateToPistonLayout(fixQuasiconnectivity(moves, state.originalState, layout), state.originalState), filePath)


if __name__ == "__main__":
    from algorithm import State, moveBlockTo
    door = State('ppppppppppp   f   b  ')
    print(door)
    moveBlockTo(4, 0, door)
    moves = door.moves
    print('original moves: ', moves)
    moves = fixQuasiconnectivity(moves, door.originalState)
    print('fixed quasiconnectivity: ', moves)
    moves = translateToPistonLayout(moves, door.originalState)
    print('original layout: ', moves)
    writeToFile(moves)


