import math


def main():
    k1, k2 = map(int, input().split())

    n = int(input())

    distr_y = [{} for _ in range(k1)]
    total_x_y = [0] * k1

    for _ in range(n):
        x, y = map(int, input().split())

        distr_y[x - 1].setdefault(y - 1, 0)
        distr_y[x - 1][y - 1] += 1

        total_x_y[x - 1] += 1

    ans = 0
    for x in range(k1):
        ys = distr_y[x]
        if ys:
            h = 0
            for y in ys.values():
                p = y / total_x_y[x]
                h += p * math.log(p)
            
            ans += -total_x_y[x] / n * h

    print("{:.12f}".format(ans))


def io():
    import sys
    sys.stdin = open("input.txt", "r")
    sys.stdout = open("output.txt", "w")

if __name__ == '__main__':
    # io()
    main()