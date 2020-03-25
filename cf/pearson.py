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

for _ in range(n):
    a_i, b_i = map(int, input().split())
    a.append(a_i)
    b.append(b_i)

mean_a = sum(a) / n
mean_b = sum(b) / n
var_a = sum([(x - mean_a) ** 2 for x in a])
var_b = sum([(x - mean_b) ** 2 for x in b])
pearson = sum([(a[i] - mean_a) * (b[i] - mean_b) for i in range(n)]) / (math.sqrt(var_a * var_b)) if (math.sqrt(var_a * var_b)) > 0 else 0

print("{:.10f}".format(pearson))