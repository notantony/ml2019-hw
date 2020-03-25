import math
import copy
import sys

n = None

class Node():
    def __init__(self, data):
        self.data = data
        self.index = None

    def draw(self, storage):
        raise NotImplementedError()

    def put_index(self, ttl):
        raise NotImplementedError()


class Leaf(Node):
    def __init__(self, data):
        super().__init__(data)

    def get_max(self):
        y = self.data[1]
        cnts = {}

        for y_i in y:
            cnts.setdefault(y_i, 0)
            cnts[y_i] += 1
        
        return max(cnts.keys(), key=lambda x: cnts[x])

    def draw(self, storage):
        storage[self.index] = "C {}".format(self.get_max())

    def put_index(self, ttl):
        self.index = ttl
        return ttl + 1

    def split(self, f, h, force=False):
        global n
        if h == 0:
            return self
        if len(self.data[0]) <= 1: 
        # if len(self.data[0]) <= max(n / 200, 1):
            return self
        # if self.get_max() / len(self.data[0]) >= 0.95:
        #     return self
        
        x, y = self.data
        n_samples = len(x)

        if not force:
            param, border, mx = None, None, None
            for j in range(len(x[0])):
                params_i = list(sorted(range(len(x)), key=lambda i: x[i][j]))
                left = []
                right = list([y[i] for i in params_i])
                x_queue = list(x[i][j] for i in params_i)

                new_f, dt = f(left, right)
                # while x_queue:
                # for i in range(n_samples):
                i = 0
                while i < n_samples:
                    tr = []
                    cur_x = x_queue[i]
                    tr.append(right[i])
                    i += 1
                    while i < n_samples and cur_x == x_queue[i]:
                        tr.append(right[i])
                        i += 1
                    new_f, dt = f(i, n_samples - i, dt, tr)
                    if mx is None or new_f > mx:
                        mx = new_f
                        param = j
                        border = cur_x + 0.5
        else:
            param = 0
            border = x[0][param] + 0.5
            
        l_data_i = list(filter(lambda i: x[i][param] < border, range(len(x))))
        r_data_i = list(filter(lambda i: x[i][param] >= border, range(len(x))))
        if len(l_data_i) == 0 or len(r_data_i) == 0:
            return self

        l = Leaf(([x[i] for i in l_data_i], [y[i] for i in l_data_i])).split(f, h - 1)
        r = Leaf(([x[i] for i in r_data_i], [y[i] for i in r_data_i])).split(f, h - 1)
        return Rule(self.data, param, border, l, r)


class Rule(Node):
    def __init__(self, data, param, border, l, r):
        super().__init__(data)
        self.param = param
        self.border = border
        self.l = l
        self.r = r

    def draw(self, storage):
        storage[self.index] = "Q {} {} {} {}".format(self.param + 1, self.border, self.l.index, self.r.index)
        self.l.draw(storage)
        self.r.draw(storage)

    def put_index(self, ttl):
        self.index = ttl
        ttl = self.l.put_index(ttl + 1)
        ttl = self.r.put_index(ttl)
        return ttl


def entropy(a, b):
    pass


def gini(a, b, dt=None, trans=None):
    if not dt:
        distr_a, distr_b = {}, {}
        for x in a:
            distr_a.setdefault(x, 0)
            distr_a[x] += 1

        for x in b:
            distr_b.setdefault(x, 0)
            distr_b[x] += 1

        sa = 0
        sb = 0
        for x in distr_a.keys():
            sa += (distr_a[x]) ** 2
        for x in distr_b.keys():
            sb += (distr_b[x]) ** 2
        
        sa_ = sa
        if len(a) > 0:
            sa /= len(a)
        sb_ = sb
        if len(b) > 0:
            sb /= len(b)

        return (sa + sb), (sa_, sb_, distr_a, distr_b)
    
    sa, sb, distr_a, distr_b = dt

    strans = set(trans)

    for x in strans:
        sa -= (distr_a.get(x, 0)) ** 2
        sb -= (distr_b[x]) ** 2

    for x in trans:
        distr_b[x] -= 1
        distr_a.setdefault(x, 0)
        distr_a[x] += 1

    for x in strans:
        sa += distr_a[x] ** 2
        sb += distr_b[x] ** 2

    sa_ = sa
    if a > 0:
        sa /= a
    sb_ = sb
    if b > 0:
        sb /= b

    return (sa + sb), (sa_, sb_, distr_a, distr_b)



def main():
    global n
    _, _, h = map(int, sys.stdin.readline().split())
    n = int(sys.stdin.readline())

    x, y = [], []
    ss = [list(map(int, input().split())) for _ in range(n)]

    # ss = list(map(lambda x: list(map(int, x.split())), sys.stdin.readlines()))

    for s_i in ss:
        x.append(s_i[:-1])
        y.append(s_i[-1])
    
    # import random
    # ind = list(range(n))
    # random.shuffle(ind)
    # ind = ind[:850]
    
    # x = [x[i] for i in ind]
    # y = [y[i] for i in ind]
    tree = Leaf((x, y)).split(gini, h, True)

    ttl = tree.put_index(1)

    result = [None] * ttl
    tree.draw(result)
    print(ttl - 1)
    for s in result[1:]:
        print(s)


def io():
    import sys
    sys.stdin = open("input.txt", "r")
    sys.stdout = open("output.txt", "w")


if __name__ == '__main__':
    # io()
    main()
