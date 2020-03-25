import math


def main():
    m = int(input())

    res = [0] * (1 << m)
    
    for i in range(1 << m):
        res[i] = int(input())

    print("2")
    print("{} 1".format(1 << m))
    for i in range(1 << m):
        line = [0] * (m + 1)
        total = bin(i).count("1")
        for j in range(m):
            if i & (1 << j) == 0:
                line[j] = -100
            else:
                line[j] = 1
        line[m] = -total + 0.1
        print(" ".join(map(str, line)))
    
    res.append(-0.1)
    print(" ".join(map(str, res)))


def io():
    import sys
    sys.stdin = open("input.txt", "r")
    sys.stdout = open("output.txt", "w")


if __name__ == '__main__':
    io()
    main()