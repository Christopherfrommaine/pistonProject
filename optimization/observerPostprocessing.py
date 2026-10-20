from copy import deepcopy
from algorithm.algorithm import State
from typing import List

def postprocessForObservers(door: State):
    for k in [-5]:
        original = door.originalState;
        moves = deepcopy(door.moves)
        n = len(moves)

        statelist: List[State] = []
        for move in moves:
            original.applyMove(move)
            statelist.append(deepcopy(original))
        original = door.originalState

        positionPairs = []
        seen = [-3]
        for i in range(n):
            if moves[i] == (k,):
                if k not in seen:
                    seen.append(k)
                else:
                    for j in range(i + 1, n):
                        if moves[j] == (k,):
                            positionPairs.append((i, j))
                            break
                        elif not isinstance(moves[j], int):
                            break
        print(positionPairs)

        for (i, j) in positionPairs:
            pi = i
            while pi and isinstance(moves[pi-1], int) and statelist[pi - 1].p[-3] != 'o':
                pi -= 1
            print("pi: ", pi)

            sj = j
            while sj < n - 1 and isinstance(moves[sj+1], int) and statelist[sj+1].p[-3] != 'o':
                sj += 1

            print("sj: ", sj)




    pass