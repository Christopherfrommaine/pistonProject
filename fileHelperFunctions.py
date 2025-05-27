projectDirectory = '/home/chris/Programming/Python/pistonProject/'
minecraftDirectory = '/home/chris/.minecraft/'


def writeToFile(string, path):
    with open(path, 'w') as file:
        file.write(str(string))

def readFromFile(path):
    with open(path, "r") as file:
        text = file.read()
    return text


def logString(string, path=projectDirectory + 'debugging/log.txt'):
    writeToFile(readFromFile(path) + string + '\n', path)


def readMovesFromFile(path):
    source = readFromFile(path)

    o = []
    temp = ''
    inComment = False
    for char in source:
        if char == '#' or (inComment and char == '\n'):
            inComment = not inComment
        elif not inComment:
            match char:
                case ' ':
                    pass
                case '\n':
                    pass
                case '[':
                    pass
                case ']':
                    o.append(temp)
                case ',':
                    o.append(temp)
                    temp = ''
                case _:
                    temp += char

    return [int(tok) for tok in o if tok != '']

def moveFromFile(door, filename, newState):
    newState.moves = door.moves
    newState.applyCustomMoves(readMovesFromFile("sequence/" + filename))
    return newState

def writeToMinecraftDatapack(commands, worldName):
    dppath = minecraftDirectory + "saves/" + worldName + "/datapacks/sendcommands/data/send/functions/"

    commandi = 0
    for command in commands:
        path = dppath + "f" + str(commandi) + ".mcfunction"
        writeToFile(command.replace('/', ''), path)
        commandi += 1

    o = ''.join(("schedule function send:f" + str(i) + " " + str(20 * 10 * i + 1) + "t\n") for i in range(commandi))
    path = dppath + "mycommands.mcfunction"
    writeToFile(o, path)

    o = ''.join(("schedule clear send:f" + str(i) + "\n") for i in range(commandi))
    path = dppath + "stop.mcfunction"
    writeToFile(o, path)
