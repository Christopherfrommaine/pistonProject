import fileHelperFunctions

t1 = fileHelperFunctions.readFromFile(fileHelperFunctions.minecraftDirectory + "logs/latest.log").split("\n")
t2 = [t.split(':')[-1] for t in t1 if t and t[0] == "["]
t3 = [t[5:] for t in t2 if len(t) > 4 and t[:4] == " [@]"]

t4 = []
started = False
for t in t3:
    if t == "start":
        started = True
        t4 = []
    elif started:
        t4.append(t)
if not started:
    t4 = t3

t5 = "".join(t + "," for t in t4).split("---,")
if '' in t5:
    t5.remove('')

o1 = []
for n in t5:
    summ = 0

    b = n.split(',')
    if '' in b:
        b.remove('')
    
    for p in b:
        try:
            i, v = p.split("; ")
            summ += int(v) * (1 << (int(i) - 1))
        except Exception:
            pass
    
    o1.append(summ)

olen = len(o1)
crop = len(o1)
# if crop > 100:
#     crop = 100 + crop % 100
final = o1[-crop:]

num63 = sum(i for i in o1 if i == 63)

print(olen, num63, final)