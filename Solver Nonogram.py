import itertools
import time
import multiprocessing as mp


nonogram_10x10 = [
    [[6], [1, 1, 1, 1], [2, 1, 2], [1, 1, 2, 1], [1, 1, 4], [1, 2, 1], [8], [1, 1], [1, 4], [2]],  # rows
    [[1], [4, 2], [1, 2], [6, 1], [1, 2, 1], [5, 1, 1], [1, 2, 1, 1], [3, 1, 2], [1, 5], [2]]      # columns
    ]

nonogram_8x8 = [
    [[4, 3], [1, 1, 1], [6], [1, 3, 1], [2, 3, 1], [4, 3], [2], [6, 1]],
    [[6, 1], [1, 1, 2, 1], [1, 2, 3], [8], [3, 1], [3, 2, 1], [1, 1, 1], [1, 2, 1]]
    ]

nonogram_5x5 = [
    [[3], [4], [3], [1, 1], [4]],
    [[1], [4], [3, 1], [2, 2], [2, 1]]
    ]


def partitions(n, k):
    """
    :param n: number of 'balls'
    :param k: number of partitions
    :yield: each partition
    """
    for c in itertools.combinations(range(n+k-1), k-1):
        yield [b-a-1 for a, b in zip((-1,)+c, c+(n+k-1,))]


def set_row(clue, size):
    black = sum(clue)
    white = size + 1 - black - len(clue)
    n = white
    k = len(clue) + 1
    for part in partitions(n, k):
        ans = "0"*part[0]
        for each in range(len(clue)):
            ans += "1"*clue[each]
            ans += "0"*(part[each+1]+1)
        ans = ans[:-1]
        yield ans


def check_row(line, sol):
    line = line[:]
    err = abs(sum(line) - sol.count("1"))
    while len(line) > 0:
        n = line.pop(0)
        for s in range(n):
            s0 = sol[0]
            sol = sol[1:]
            if s0 == 0:
                err += n - s + 1
                break
    return err


def transpose(l):
    return [[j[i] for j in l] for i in range(len(l[0]))]


def show_puzzle(puzzle):
    s = [" ", "█"]
    for line in puzzle:
        l = ""
        for k in line:
            l += s[int(k)]
        print(l)


def check_puzzle(possible_solution, rows, solq):
    while True:
        sol = transpose(possible_solution.get().split())
        for row in range(len(sol)):
            if check_row(rows[row], sol[row]) != 0:
                break
        else:
            solq.put(transpose(sol))
            return transpose(sol)


def build_nonogram_rec(lines, size, q, sol=""):
    if len(lines) == 0:
        q.put(sol)
    else:
        for row in set_row(lines[0], size):
            build_nonogram_rec(lines[1:], size, q, sol+row+"\n")


if __name__ == "__main__":
    t1 = time.time()
    solve = nonogram_10x10
    print(len(solve[0]), len(solve[1]))
    queue = mp.Queue(1000)
    solution = mp.Queue()
    p1 = mp.Process(target=build_nonogram_rec, args=(solve[0], len(solve[1]), queue))
    p2 = mp.Process(target=check_puzzle, args=(queue, solve[1], solution))
    p1.start()
    p2.start()
    p2.join()
    solution = solution.get()
    print(solution)
    print()
    show_puzzle(solution)
    print(time.time() - t1)
    p1.terminate()
