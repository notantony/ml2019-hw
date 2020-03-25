import math

EPS = 1e-7


def manhattan(v1, v2):
    s = 0
    for i in range(len(v1)):
        s += abs(v1[i] - v2[i])
    return s


def euclidean(v1, v2):
    s = 0
    for i in range(len(v1)):
        s += (v1[i] - v2[i]) ** 2
    return math.sqrt(s)


def chebyshev(v1, v2):
    s = float('-inf')
    for i in range(len(v1)):
        s = max(s, abs(v1[i] - v2[i]))
    return s


def uniform(d):
    if not -1 < d < 1:
        return 0
    return 0.5


def triangular(d):
    if not -1 < d < 1:
        return 0
    return 1 - abs(d)


def epanechnikov(d):
    if not -1 < d < 1:
        return 0
    return 0.75 * (1 - d ** 2)


def quartic(d):
    if not -1 < d < 1:
        return 0
    return 15 / 16 * (1 - d ** 2) ** 2


def triweight(d):
    if not -1 < d < 1:
        return 0
    return 35 / 32 * (1 - d ** 2) ** 3


def tricube(d):
    if not -1 < d < 1:
        return 0
    return 70 / 81 * (1 - abs(d) ** 3) ** 3


def gaussian(d):
    return 1 / math.sqrt(2 * math.pi) * math.exp(-0.5 * d ** 2)


def cosine(d):
    if not -1 < d < 1:
        return 0
    return math.pi / 4 * math.cos(math.pi / 2 * d)


def logistic(d):
    return 1 / (math.exp(d) + 2 + math.exp(-d))


def sigmoid(d):
    return 2 / math.pi / (math.exp(d) + math.exp(-d))


def main():
    n, m = map(int, input().split())

    x = []
    y = []
    for i in range(n):
        row = list(map(int, input().split()))
        y.append(row[-1])
        x.append(row[:-1])

    q = list(map(int, input().split()))
    dist_f = eval(str(input()))
    kernel_f = eval(str(input()))
    window_str = input()
    window_const = int(input())

    dsts = sorted([(dist_f(x[i], q), y[i]) for i in range(n)])

    if window_str == "fixed":
        d = window_const
    else:
        d = dsts[window_const][0]

    # dsts = list(filter(lambda p: p[0] <= d, dsts))

    s = 0.0
    s_w = 0.0
    if abs(d) > EPS:
        for (dst, y_i) in dsts:
            s += kernel_f(dst / d) * y_i
            s_w += kernel_f(dst / d)
    else:
        for (dst, y_i) in dsts:
            if abs(dst) < EPS:
                s += y_i
                s_w += 1
    s_r = s / s_w if s_w != 0 else sum([x for _, x in dsts]) / len(dsts)
    print("{:.12f}".format(s_r))



if __name__ == '__main__':
    main()