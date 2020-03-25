import itertools
import operator
import functools
import math

eps = 1e-200
inf = float("inf")


def readint():
    return int(input())


n = readint()
a, b = [], []

for i in range(n):
    a_i, b_i = map(int, input().split())
    a.append((a_i, i))
    b.append((b_i, i))

r = [0] * n
s = [0] * n

for pos, (_, i) in enumerate(sorted(a)):
    r[i] = pos

for pos, (_, i) in enumerate(sorted(b)):
    s[i] = pos

spearman = 1 - 6 / (n * (n + 1) * (n - 1)) * sum([(r[i] - s[i]) ** 2 for i in range(n)])

print("{:.10f}".format(spearman))