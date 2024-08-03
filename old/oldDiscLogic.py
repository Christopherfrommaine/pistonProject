for num in f2:
    if num <= 0:
        pass  # Possible custom control stuff eventually
        lowerBits = abs(num) % 16
        higherBits = math.floor(abs(num) / 16) % 16
        # f3 += [higherBits, lowerBits]
        f3 += [lowerBits, higherBits]
    else:
        if num == 25:
            pass
        lowerBits = num % 8
        higherBits = math.floor(num / 8) % 8
        # f3 += [higherBits, lowerBits]
        f3 += [lowerBits, higherBits]  # For original decoder
print(f3)

numtodisc= ['stal', '13', 'cat', 'blocks', 'chirp', 'far', 'mall', 'mellohi', 'stal', 'strad', 'ward', '11', 'wait', 'pigstep', 'otherside', '5']
f4 = ['stal'] + [numtodisc[num] for num in f3] + ['strad', 'strad']
print(f4)


f5 = [[]]
for _disc in f4:
    if len(f5[-1]) >= 27:
        f5 += [[]]
        counter = 0
    f5[-1].append(_disc)

f6 = []
for minecartList in f5:
    nbt = ''
    for discIndex in range(len(minecartList)):
        nbt += '{' + f'id:"minecraft:music_disc_{minecartList[discIndex]}",Count:1b,Slot:{discIndex}' + '},'
    nbt = nbt[:-1]
    f6.append('/summon minecraft:chest_minecart -245 306 -11 {Items:[' + nbt + ']}')


with open('output.txt', 'w') as file:
    file.write(f"f0 (Input):\n{f0}\n------\nf1 (New Line):\n{f1}\n------\nf2 (List):\n{f2}\n------\nf3 (Binary Encode):\n{f3}\n------\nf4 (Disc):\n{f4}\n------\nf6 (Minecart Commands):\n{f6}\n------\n")


if doDiscCommands:
    for _disc in f4:
        sendCommand(formatCommand(_disc))
if doMinecartCommands:
    sendCommand('/tick rate 20.0')
    sendCommand('/tp @p -251.5 307 -6.5 -90 60')
    pyautogui.keyDown('shift')
    pyautogui.keyUp('shift')
    for _command in f6:
        sendCommand(_command, commandBlock=True)
