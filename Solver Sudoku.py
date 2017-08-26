import numpy as np
import time
from random import shuffle

sudoku_brute = """000000000
000003085
001020000
000507000
004000100
090000000
500000073
002010000
000040009
"""

sudoku_test = """000000000
000000000
000000000
000000000
000000000
000000000
000000000
000000000
000000000
"""

sudoku_easy = """073028090
504000600
109070050
701005060
300904005
040700109
030080502
006000703
050340910
"""

sudoku_medium = """640280000
030006004
090350100
105920000
300000009
000068301
009031060
400500010
000042095
"""

sudoku_hard = """020050009
000730500
640010000
000001700
508000902
009500000
000070064
002065000
700020050
"""

sudoku_hardest = """800000000
003600000
070090200
050007000
000045700
000100030
001000068
008500010
090000400
"""


def parse_puzzle(puzzle: str):
    puzzle = puzzle.split()
    n = []
    zeros = []
    for x in range(9):
        nn = []
        for y in range(9):
            nn.append(int(puzzle[x][y]))
            if puzzle[y][x] == "0":
                zeros.append((x, y))
        n.append(nn)
    n = np.array(n)
    return n, zeros


def show_puzzle(puzzle: np.ndarray):
    for y in range(3):
        for part in range(3):
            for x in range(part*3, (part+1)*3):
                print(puzzle[y][x], end="")
            print("|", end="")
        print("\b")
    print("-"*11)
    for y in range(3, 6):
        for part in range(3):
            for x in range(part*3, (part+1)*3):
                print(puzzle[y][x], end="")
            print("|", end="")
        print("\b")
    print("-"*11)
    for y in range(6, 9):
        for part in range(3):
            for x in range(part*3, (part+1)*3):
                print(puzzle[y][x], end="")
            print("|", end="")
        print("\b")
    print()


def ready(puzzle: np.ndarray):
    for line in puzzle:
        line = list(line)
        for num in range(1, 10):
            if line.count(num) != 1:
                return False
    for line in puzzle.T:
        line = list(line)
        for num in range(1, 10):
            if line.count(num) != 1:
                return False
    for blockx in range(3):
        for blocky in range(3):
            bx = puzzle[blockx*3:blockx*3+3]
            block = list(np.append(np.zeros(0), (bx[0][blocky*3:blocky*3+3], bx[1][blocky*3:blocky*3+3], bx[2][blocky*3:blocky*3+3])))
            for num in range(1, 10):
                if block.count(num) != 1:
                    return False
    return True


def lexicographical_order(s: str):
    s = list(s)
    while True:
        for i in range(len(s)-1):
            if s[i] < s[i+1]:
                k = i
        for i in range(k+1, len(s)):
            if s[k] < s[i]:
                l = i
        s[k], s[l] = s[l], s[k]
        s[k+1:] = s[k+1:][::-1]
        yield ''.join(s)


def solve_dumb(puzzle: np.ndarray, zeros: list):
    show_puzzle(puzzle)
    unique, counts = np.unique(puzzle, return_counts=True)
    numbers = dict(zip(unique, counts))

    test = ""
    for num in range(1, 10):
        test += str(num)*numbers[num]

    test = int(test)
    rep = str(test)
    rep = "1" * (len(zeros) - len(rep)) + rep
    rep = lexicographical_order(rep)

    t1 = time.time()

    while not ready(puzzle):
        test = next(rep)
        for y, x in zeros:
            puzzle[y][x] = int(test[zeros.index((y, x))])

    show_puzzle(puzzle)
    print()
    print(time.time() - t1)


def possibles(puzzle, y, x):
    possible = list(range(1, 10))
    for xx in range(9):
        flag = puzzle[y][xx]
        if puzzle[y][xx] in possible:
            possible.pop(possible.index(puzzle[y][xx]))
    for yy in range(9):
        flag = puzzle[yy][x]
        if puzzle[yy][x] in possible:
            possible.pop(possible.index(puzzle[yy][x]))
    x, y = x//3, y//3
    for xx in range(x*3, x*3 + 3):
        for yy in range(y*3, y*3 + 3):
            flag = puzzle[yy][xx]
            if puzzle[yy][xx] in possible:
                possible.pop(possible.index(puzzle[yy][xx]))
    return possible

t = 0
def solve_rec(puzzle: nd.array, zeros: list, show: bool = True) -> list:
    global t
    t += 1
    puzzle = np.copy(puzzle)
    if show:
        show_puzzle(puzzle)
    if ready(puzzle):
        return puzzle
    x, y = zeros[0]
    possible = possibles(puzzle, y, x)
    shuffle(possible)
    #print(y, x, possible)
    if len(possible) == 0:
        return puzzle
    for num in possible:
        puzzle[y][x] = num
        solve = solve_rec(puzzle, zeros[1:], False)
        if solve.all():
            return solve
    else:
        return puzzle


def solve_human_1(puzzle, zeros):
    running = True
    while running:
        running = False
        for x, y in zeros:
            possible = possibles(puzzle, y, x)
            if len(possible) == 1:
                zeros.pop(zeros.index((x, y)))
                puzzle[y][x] = possible[0]
                running = True
                #print(x, y, possible)
    return puzzle, zeros

def solve_human_2(puzzle, zeros):
    running = True
    while running:
        if len(zeros) == 0:
            break
        running = False
        for x in range(9):
            poss = {}
            count = dict([(n, 0) for n in range(1, 10)])
            for y in range(9):
                if (x, y) in zeros:
                    poss[y] = possibles(puzzle, y, x)
            for key in poss:
                for num in poss[key]:
                    count[num] += 1
            for num in count:
                if count[num] == 1:
                    running = True
                    for l in poss:
                        if num in poss[l]:
                            y = l
                            break
                    zeros.pop(zeros.index((x, y)))
                    puzzle[y][x] = num
        for y in range(9):
            poss = {}
            count = dict([(n, 0) for n in range(1, 10)])
            for x in range(9):
                if (x, y) in zeros:
                    poss[x] = possibles(puzzle, y, x)
            for key in poss:
                for num in poss[key]:
                    count[num] += 1
            for num in count:
                if count[num] == 1:
                    running = True
                    for l in poss:
                        if num in poss[l]:
                            x = l
                            break
                    zeros.pop(zeros.index((x, y)))
                    puzzle[y][x] = num
        for square_x in range(3):
            for square_y in range(3):
                poss = {}
                count = dict([(n, 0) for n in range(1, 10)])
                for xx in range(square_x * 3, square_x * 3 + 3):
                    for yy in range(square_y * 3, square_y * 3 + 3):
                        if (xx, yy) in zeros:
                            poss[xx+3*yy] = possibles(puzzle, yy, xx)
                for key in poss:
                    for num in poss[key]:
                        count[num] += 1
                for num in count:
                    if count[num] == 1:
                        running = True
                        for l in poss:
                            if num in poss[l]:
                                x = l % 3
                                y = l // 3
                                break
                        zeros.pop(zeros.index((x, y)))
                        puzzle[y][x] = num
    return puzzle, zeros

t1 = time.time()
p, z = parse_puzzle(sudoku_hardest)
nflag = 0
while True:
    flag = len(z)
    print(flag)
    if flag == nflag or flag == 0:
        break
    solved, z = solve_human_2(p, z)
    solved, z = solve_human_1(p, z)
    nflag = flag
solved = solve_rec(p, z)
show_puzzle(solved)
print(t)
print(time.time() - t1)
