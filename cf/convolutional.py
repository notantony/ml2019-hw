import math
import copy


def assert_fail():
    while True:
        pass


def arr(n, m, d):
    return [[[0] * d for j in range(n)] for i in range(m)] 

def arr4(n, m, d, p):
    return [[[[0] * p for _ in range(d)] for _ in range(m)] for _ in range(n)] 


class Node():
    def __init__(self):
        super().__init__()
        self.data = None
        self.dims = None
        self.dfc = None

    def eval(self):
        raise NotImplementedError

    def eval_back(self):
        raise NotImplementedError


class Var(Node):
    def __init__(self, dims):
        super().__init__()
        self.dims = dims

    def eval(self):
        pass

    def eval_back(self):
        pass


class Relu(Node):
    def __init__(self, alpha, x):
        super().__init__()
        self.alpha = alpha
        self.x = x
        self.dims = x.dims

    def eval(self):
        n, m, d = self.dims
        self.data = arr(n, m, d)
        f = lambda x: self.alpha * x if x < 0 else x
        for i in range(n):
            for j in range(m):
                for k in range(d):
                    self.data[i][j][k] = f(self.x.data[i][j][k])

    def eval_back(self):
        n, m, d = self.dims

        result = copy.deepcopy(self.dfc)
        f = lambda x: self.alpha if x < 0 else 1
        for i in range(n):
            for j in range(m):
                for k in range(d):
                    x = self.x.data[i][j][k]
                    result[i][j][k] *= f(x)
        self.x.dfc = result


class Pool(Node):
    def __init__(self, s, x):
        super().__init__()
        self.s = s
        self.x = x
        self.dims = (x.dims[0] + s - 1) // s, (x.dims[1] + s - 1) // s, x.dims[2]
        self.mx_i = arr(*self.dims)


    def eval(self):
        n, m, d = self.dims
        self.data = arr(*self.dims)
        for k in range(d):
            for i in range(n):
                for j in range(m):
                    mx = None
                    mx_c = None
                    for shift_i in range(self.s):
                        for shift_j in range(self.s):
                            x_real = i * self.s + shift_i
                            y_real = j * self.s + shift_j
                            if x_real < self.x.dims[0] and y_real < self.x.dims[1]:
                                val = self.x.data[x_real][y_real][k]
                                if mx is None or val > mx:
                                    mx = val
                                    mx_c = [(x_real, y_real)]
                                elif val == mx:
                                    mx_c.append((x_real, y_real))
                    self.data[i][j][k] = mx
                    self.mx_i[i][j][k] = mx_c


    def eval_back(self):
        n, m, d = self.dims
        result = arr(*self.x.dims)
        for i in range(n):
            for j in range(m):
                for k in range(d):
                    for x_real, y_real in self.mx_i[i][j][k]:
                        result[x_real][y_real][k] = self.dfc[i][j][k]
        
        self.x.dfc = result



class Bias(Node):
    def __init__(self, b, x):
        super().__init__()
        self.b = b
        self.x = x
        self.dims = self.x.dims
        self.res = None

    def eval(self):
        n, m, d = self.dims
        self.data = copy.deepcopy(self.x.data)
        for i in range(n):
            for j in range(m):
                for k in range(d):
                    self.data[i][j][k] += self.b[k]

    def eval_back(self):
        n, m, d = self.dims
        self.x.dfc = copy.deepcopy(self.dfc)

        self.res = [0] * d
        for i in range(n):
            for j in range(m):
                for k in range(d):
                    self.res[k] += self.dfc[i][j][k]
        


class Cnv(Node):
    def __init__(self, h, k, s, p, a, x):
        super().__init__()
        self.h = h
        self.k = k
        self.s = s
        self.p = p
        self.a = a
        self.x = x
        self.d = x.dims[2]
        o_x = (self.x.dims[0] + 2 * p - k) // s + 1 
        o_y = (self.x.dims[1] + 2 * p - k) // s + 1 
        self.dims = o_x, o_y, h
        self.ext = None
        self.res = None
        self.origs = None

    def extend(self):
        raise NotImplementedError()

    def eval(self):
        self.extend()
        n, m, d = self.dims
        self.data = arr(*self.dims)
        for res_d in range(d):
            for i in range(n):
                for j in range(m):
                    sm = 0
                    for shift_i in range(self.k):
                        for shift_j in range(self.k):
                            real_i = i * self.s + shift_i
                            real_j = j * self.s + shift_j
                            for dim in range(self.d):
                                sm += self.ext[real_i][real_j][dim] * self.a[res_d][dim][shift_i][shift_j]
                    self.data[i][j][res_d] = sm

    def eval_back(self):
        n, m, d = self.dims
        
        self.x.dfc = arr(self.x.dims[0], self.x.dims[1], self.x.dims[2])
        for res_d in range(d):
            for i in range(n):
                for j in range(m):
                    for shift_i in range(self.k):
                        for shift_j in range(self.k):
                            real_i = i * self.s + shift_i
                            real_j = j * self.s + shift_j
                            for dim in range(self.d):
                                trg_i, trg_j = self.origs[real_i][real_j]
                                self.x.dfc[trg_i][trg_j][dim] += self.dfc[i][j][res_d] * self.a[res_d][dim][shift_i][shift_j]

        self.res = arr4(self.h, self.d, self.k, self.k) # TODO
        for res_d in range(d):
            for i in range(n):
                for j in range(m):
                    for shift_i in range(self.k):
                        for shift_j in range(self.k):
                            real_i = i * self.s + shift_i
                            real_j = j * self.s + shift_j
                            for dim in range(self.d):
                                self.res[res_d][dim][shift_i][shift_j] += \
                                    self.ext[real_i][real_j][dim] * self.dfc[i][j][res_d]



class Cnvm(Cnv):
    def __init__(self, h, k, s, p, a, x):
        super().__init__(h, k, s, p, a, x)

    def extend(self):
        n, m, d = self.x.dims
        ext_n = n + self.p * 2
        ext_m = m + self.p * 2
        result = arr(ext_n, ext_m, d)
        self.origs = [[None] * ext_n for _ in range(ext_m)]

        for i in range(ext_n):
            for j in range(ext_m):
                for k in range(d):
                    real_i = i - self.p
                    real_j = j - self.p
                    if real_i < 0:
                        real_i = -real_i
                    if real_i >= n:
                        real_i = 2 * n - 2 - real_i
                    if real_j < 0:
                        real_j = -real_j
                    if real_j >= m:
                        real_j = 2 * m - 2 - real_j

                    self.origs[i][j] = (real_i, real_j)
                    result[i][j][k] = self.x.data[real_i][real_j][k]
        self.ext = result

class Cnve(Cnv):
    def __init__(self, h, k, s, p, a, x):
        super().__init__(h, k, s, p, a, x)

    def extend(self):
        n, m, d = self.x.dims
        ext_n = n + self.p * 2
        ext_m = m + self.p * 2
        result = arr(ext_n, ext_m, d)
        self.origs = [[None] * ext_n for _ in range(ext_m)]

        for i in range(ext_n):
            for j in range(ext_m):
                for k in range(d):
                    real_i = i - self.p
                    real_j = j - self.p
                    if real_i < 0:
                        real_i = 0
                    if real_i >= n:
                        real_i = n - 1
                    if real_j < 0:
                        real_j = 0
                    if real_j >= m:
                        real_j = m - 1

                    self.origs[i][j] = (real_i, real_j)
                    result[i][j][k] = self.x.data[real_i][real_j][k]
        self.ext = result


class Cnvc(Cnv):
    def __init__(self, h, k, s, p, a, x):
        super().__init__(h, k, s, p, a, x)

    def extend(self):
        n, m, d = self.x.dims
        ext_n = n + self.p * 2
        ext_m = m + self.p * 2
        result = arr(ext_n, ext_m, d)
        self.origs = [[None] * ext_n for _ in range(ext_m)]

        for i in range(ext_n):
            for j in range(ext_m):
                for k in range(d):
                    real_i = i - self.p
                    real_j = j - self.p
                    real_i = (real_i + n * 2) % n
                    real_j = (real_j + m * 2) % m

                    self.origs[i][j] = (real_i, real_j)
                    result[i][j][k] = self.x.data[real_i][real_j][k]
        self.ext = result

# TODO: little padding
def main():
    ss = list(map(int, input().split()))
    n = ss[0]
    d = ss[1]
    ss = ss[2:]
    xx = [[[ss[i * n * n + j * n + k] for k in range(n)] for j in range(n)] for i in range(d)]
    x = [[[0 for k in range(d)] for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(d):
                x[i][j][k] = xx[k][i][j]
    
    el  = int(input())    
    nodes = [None] * (el + 1)
    nodes[0] = Var((n, n, d))
    nodes[0].data = x


    for i in range(1, el + 1):
        ss = input().split()
        node_type = ss[0]

        if node_type == "relu":
            nodes[i] = Relu(1 / int(ss[1]), nodes[i - 1])
        elif node_type == "pool":
            nodes[i] = Pool(int(ss[1]), nodes[i - 1])
        elif node_type == "bias":
            nodes[i] = Bias(list(map(int, ss[1:])), nodes[i - 1])
        else:
            d = nodes[i - 1].dims[2]
            h, k, s, p = map(int, ss[1:5])
            ss = list(map(int, ss[5:]))
            x = [
                [
                    [
                        [
                            ss[a * d * k * k + b * k * k + c * k + e]
                            for e in range(k)
                        ]
                        for c in range(k)
                    ]
                    for b in range(d)
                ]
                for a in range(h)
            ]
            if node_type == "cnvm":
                nodes[i] = Cnvm(h, k, s, p, x, nodes[i - 1])
            elif node_type == "cnve":
                nodes[i] = Cnve(h, k, s, p, x, nodes[i - 1])
            elif node_type == "cnvc":
                nodes[i] = Cnvc(h, k, s, p, x, nodes[i - 1])                

    n, m, d = nodes[-1].dims
    ss = list(map(int, input().split()))

    xx = [[[ss[i * n * n + j * n + k] for k in range(n)] for j in range(n)] for i in range(d)]
    x = [[[0 for k in range(d)] for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(d):
                x[i][j][k] = xx[k][i][j]

    nodes[-1].dfc = x

    for node in nodes:
        node.eval()
    
    for node in reversed(nodes):
        node.eval_back()

    node = nodes[-1]
    s = " ".join(map(str, [
        node.data[i][j][k]
        for k in range(node.dims[2])
        for i in range(node.dims[0])
        for j in range(node.dims[1])
    ]))
    print(s)

    node = nodes[0]
    s = " ".join(map(str, [
        node.dfc[i][j][k]
        for k in range(node.dims[2])
        for i in range(node.dims[0])
        for j in range(node.dims[1])
    ]))
    print(s)
    
    for node in nodes:
        if isinstance(node, Cnv):
            s = " ".join(map(str, [
                node.res[p][i][j][k]
                for p in range(node.h)
                for i in range(node.d)
                for j in range(node.k)
                for k in range(node.k)
            ]))
            print(s)
        if isinstance(node, Bias):
            s = " ".join(map(str, [
                node.res[k]
                for k in range(node.dims[2])
            ]))
            print(s)




def io():
    import sys
    sys.stdin = open("input.txt", "r")
    sys.stdout = open("output.txt", "w")


if __name__ == '__main__':
    io()
    main()
