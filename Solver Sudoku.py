import numpy as np
import time

puzzle = """073028090
504000600
109070050
701005060
300904005
040700109
030080502
006000703
050340910
""".split()

n = []
zeros = []
for x in range(9):
    nn = []
    for y in range(9):
        nn.append(int(puzzle[y][x]))
        if puzzle[y][x] == "0":
            zeros.append((y, x))
    n.append(nn)

n = np.array(n)


def show_puzzle(arr):
    for y in range(3):
        for part in range(3):
            for x in range(part*3, (part+1)*3):
                print(arr[y][x], end="")
            print("|", end="")
        print("\b")
    print("-"*11)
    for y in range(3, 6):
        for part in range(3):
            for x in range(part*3, (part+1)*3):
                print(arr[y][x], end="")
            print("|", end="")
        print("\b")
    print("-"*11)
    for y in range(6, 9):
        for part in range(3):
            for x in range(part*3, (part+1)*3):
                print(arr[y][x], end="")
            print("|", end="")
        print("\b")


def ready(arr):
    for line in arr:
        line = list(line)
        for num in range(1, 10):
            if line.count(num) != 1:
                return False
    for line in arr.T:
        line = list(line)
        for num in range(1, 10):
            if line.count(num) != 1:
                return False
    for blockx in range(3):
        for blocky in range(3):
            bx = arr[blockx*3:blockx*3+3]
            block = list(np.append(np.zeros(0), (bx[0][blocky*3:blocky*3+3], bx[1][blocky*3:blocky*3+3], bx[2][blocky*3:blocky*3+3])))
            print(block)
            for num in range(1, 10):
                if block.count(num) != 1:
                    return False


def lexicographical_order(s):
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


show_puzzle(n)
print()

unique, counts = np.unique(n, return_counts=True)
numbers = dict(zip(unique, counts))

test = ""
for num in range(1, 10):
    test += str(num)*numbers[num]

test = int(test)
rep = str(test)
rep = "1" * (len(zeros) - len(rep)) + rep
rep = lexicographical_order(rep)

t1 = time.time()

while not ready(n):
    test = next(rep)
    for x in range(9):
        for y in range(9):
            if (x, y) in zeros:
                n[y][x] = int(test[zeros.index((x, y))])

show_puzzle(n)
print()
print(time.time() - t1)
