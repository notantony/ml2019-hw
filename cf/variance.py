import math


def main():
    k = int(input())
    n = int(input())
    
    x_distr = [[] for _ in range(k)]
    
    for _ in range(n):
        _x, _y = map(int, (input().split()))
        x_distr[_x - 1].append(_y)

    s = 0
    for distr in x_distr:
        if len(distr) > 0:
            ex = sum(distr) / len(distr)
            ex_2 = sum([x ** 2 for x in distr]) / len(distr)
            dx = ex_2 - ex ** 2
            s += len(distr) / n * dx

    print("{:.8f}".format(s))


def io():
    import sys
    sys.stdin = open("input.txt", "r")
    sys.stdout = open("output.txt", "w")

if __name__ == '__main__':
    io()
    main()