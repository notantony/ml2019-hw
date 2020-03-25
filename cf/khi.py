import math


def main():
    k1, k2 = map(int, input().split())

    n = int(input())

    distr = {}
    sum_x = [0] * k1
    sum_y = [0] * k2

    for _ in range(n):
        x, y = map(int, input().split())

        sum_x[x - 1] += 1
        sum_y[y - 1] += 1
        
        point = (x - 1, y - 1)
        distr.setdefault(point, 0)
        distr[point] += 1

    ans = 0
    for (x, y), p in distr.items():
        p_real = (sum_x[x] * sum_y[y]) / n
        ans += (p_real - p) ** 2 / p_real
        ans -= sum_x[x] * sum_y[y] / n
    ans += n

    print(ans)


def io():
    import sys
    sys.stdin = open("input.txt", "r")
    sys.stdout = open("output.txt", "w")

if __name__ == '__main__':
    io()
    main()