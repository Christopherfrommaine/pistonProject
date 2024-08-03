import subprocess
import pyautogui
import time


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
