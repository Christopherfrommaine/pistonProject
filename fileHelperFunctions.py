projectDirectory = 'C:/users/chris/pycharmProjects/pistonProject/'
minecraftDirectory = 'C:/users/chris/AppData/Roaming/.minecraft/'


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
        if char == '#':
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

    return [int(tok) for tok in o]

def writeToMinecraftDatapack(commands, worldName="24xInfinity Door 2-21-23"):
    o = ''.join(command + '\n' for command in commands).replace('/', '')
    path = minecraftDirectory + "saves/" + worldName + "/datapacks/sendcommands/data/send/functions/delayedcommands.mcfunction"
    writeToFile(o, path)
