import subprocess
import pyautogui
import time
import math


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.2


def copy2clip(txt):
    cmd = 'echo ' + txt.strip() + '|clip'
    return subprocess.check_call(cmd, shell=True)


def sendChatCommand(command, pauseTime=0.2):
    pyautogui.PAUSE = pauseTime
    copy2clip(command)
    pyautogui.hotkey('t')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')


def sendCommandBlockCommand(command, pauseTime=0.2):
    pyautogui.PAUSE = pauseTime
    copy2clip(command)
    pyautogui.rightClick()
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    pyautogui.keyDown('space')
    time.sleep(0.4 - pyautogui.PAUSE if 0.4 - pyautogui.PAUSE >= 0 else 0)
    pyautogui.keyUp('space')

def readCommandsFromFile(path='finalPistonCode.txt', raw=False):
    with open(path, "r") as file:
        source = file.read()
    
    if raw:
        return source

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


dectobin3 = ((0, 0, 0), (0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1))
dectobin4 = ((0, 0, 0, 0), (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 1, 1), (0, 1, 0, 0), (0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 1),
             (1, 0, 0, 0), (1, 0, 0, 1), (1, 0, 1, 0), (1, 0, 1, 1), (1, 1, 0, 0), (1, 1, 0, 1), (1, 1, 1, 0), (1, 1, 1, 1))

