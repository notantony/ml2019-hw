import itertools
import operator
import functools
import math


eps = 1e-200
inf = float("inf")


def readint():
    return int(input())


k = readint()
n = readint()

v = []
total_c = dict()

for i in range(n):
    a_i, b_i = map(int, input().split())
    v.append((a_i, b_i))
    total_c[b_i] = total_c.get(b_i, 0) + 1

v = sorted(v)

s_in = 0
s_out = 0

last_x = dict()
last_i = dict()
total_last = 0
total = n
last = inf
for x, y in v:
    if y in last_x:
        s_in += (x - last_x[y]) * last_i[y] * (total_c[y] - last_i[y])
    if last != inf:
        s_out += (x - last) * total_last * (n - total_last)
    last_x[y] = x
    last_i[y] = last_i.get(y, 0) + 1
    total_last += 1
    last = x

s_out -= s_in
print("{:d}\n{:d}".format(s_in * 2, s_out * 2))