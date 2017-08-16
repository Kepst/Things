import numpy as np
import time

sudoku_test = """673528491
584193627
129476358
791835204
362914875
845762139
937681542
416259783
258340910
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

def solve_rec(puzzle, zeros, show=True):
    puzzle = np.copy(puzzle)
    if show:
        show_puzzle(puzzle)
    if ready(puzzle):
        return puzzle
    x, y = zeros[0]
    possible = possibles(puzzle, y, x)
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

p, z = parse_puzzle(sudoku_hard)
solve = solve_rec(p, z)
show_puzzle(solve)
