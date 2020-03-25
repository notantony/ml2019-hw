import math
import copy


def assert_fail():
    while True:
        pass


def matrix_mul(a, b):
    N = len(a)
    M = len(a[0])
    K = len(b[0])
    c = [
        [
            sum(a[i][k] * b[k][j] for k in range(M))
            for j in range(K)
        ]
        for i in range(N)
    ]
    return c


def transpose(a):
    N = len(a)
    M = len(a[0])
    b = [
        [a[j][i] for j in range(N)]
        for i in range(M)
    ]
    return b


def read_vector(wrap=True):
    if not wrap:
        return list(map(float, input().split()))
    else:
        return list(map(lambda x: [float(x)], input().split()))


def read_matrix(n):
    return [read_vector(False) for _ in range(n)]


def print_vector(v):
    print(" ".join(map(lambda x: str(x[0]), v)))


def print_matrix(v):
    print("\n".join(map(
        lambda row: " ".join(
            map(str, row)
    ), v)))


class Node():
    def __init__(self):
        super().__init__()
        self.df = []
        self.data = None
        self.r = None
        self.c = None
        self.dfc = None

    def eval(self):
        raise NotImplementedError

    def eval_back(self):
        raise NotImplementedError

    def prepare_df(self):
        assert(self.df)
        # if self.dfc:
        #     return
        self.dfc = [[0] * self.c for _ in range(self.r)]
        for df_i in self.df:
            for i in range(self.r):
                for j in range(self.c):
                    self.dfc[i][j] += df_i[i][j]
        self.df = []


class Var(Node):
    def __init__(self, r, c):
        super().__init__()
        self.r = r
        self.c = c

    def eval(self):
        pass

    def eval_back(self):
        self.prepare_df()


class Tnh(Node):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.r = x.r
        self.c = x.c

    def eval(self):
        self.data = list(map(lambda row: list(map(math.tanh, row)), self.x.data))

    def eval_back(self):
        self.prepare_df()

        result = copy.deepcopy(self.dfc)
        for i in range(self.r):
            for j in range(self.c):
                x = self.data[i][j]
                f = lambda x: 1 - x * x
                result[i][j] *= f(x)
        self.x.df.append(result)


class Sigm(Node):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.r = x.r
        self.c = x.c

    def eval(self):
        f = lambda x: 1 / (1 + math.exp(-x))
        self.data = list(map(lambda row: list(map(f, row)), self.x.data))

    def eval_back(self):
        self.prepare_df()

        result = copy.deepcopy(self.dfc)
        for i in range(self.r):
            for j in range(self.c):
                x = self.data[i][j]
                f = lambda x: x * (1 - x)
                result[i][j] *= f(x)
        self.x.df.append(result)


class Mul(Node):
    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b
        self.r = a.r
        self.c = b.c


    def eval(self):
        self.data = matrix_mul(self.a.data, self.b.data)


    def eval_back(self):
        self.prepare_df()

        self.a.df.append(matrix_mul(self.dfc, transpose(self.b.data)))
        self.b.df.append(matrix_mul(transpose(self.a.data), self.dfc))


class Sum(Node):
    def __init__(self, u):
        super().__init__()
        self.u = u
        self.r = u[0].r
        self.c = u[0].c

    def eval(self):
        self.data = copy.deepcopy(self.u[0].data)
        for u_i in self.u[1:]:
            for i in range(self.r):
                for j in range(self.c):
                    self.data[i][j] += u_i.data[i][j]

    def eval_back(self):
        self.prepare_df()
        
        for u_i in self.u:
            u_i.df.append(self.dfc)


class Had(Node):
    def __init__(self, u):
        super().__init__()
        self.u = u
        self.r = u[0].r
        self.c = u[0].c

    def eval(self):
        self.data = copy.deepcopy(self.u[0].data)
        for u_i in self.u[1:]:
            for i in range(self.r):
                for j in range(self.c):
                    self.data[i][j] *= u_i.data[i][j]

    def eval_back(self):
        self.prepare_df()
        
        for i in range(len(self.u)):
            u_i = self.u[i]
            product = copy.deepcopy(self.dfc)
            for j in range(len(self.u)):
                u_j = self.u[j]
                for p in range(self.r):
                    for q in range(self.c):
                        if i != j:
                            product[p][q] *= u_j.data[p][q]
                        # product[i][j] *= self.dfc[i][j]
            
            u_i.df.append(product)
            

class Chain(Node):
    def __init__(self):
        super().__init__()
        self.chain = []

    def eval(self):
        for node in self.chain:
            node.eval()

    def eval_back(self):
        for node in reversed(self.chain):
            node.eval_back()


class Sigmator(Chain):
    def __init__(self, h, x, w, u, b, n, finisher):
        super().__init__()
        self.t3 = Var(n, n)
        self.t3.data = u
        self.t4 = Var(n, n)
        self.t4.data = w
        t5 = Mul(self.t3, h)
        t6 = Mul(self.t4, x)
        self.t7 = Var(n, 1)
        self.t7.data = b
        t8 = Sum([t5, t6, self.t7])
        self.fin = finisher(t8)
        self.chain = [self.t3, self.t4, t5, t6, self.t7, t8, self.fin]
        self.r = self.fin.r
        self.c = self.fin.c

    def eval(self):
        super().eval()
        self.data = self.fin.data

    def eval_back(self):
        self.fin.df = self.df
        super().eval_back()

    def dump(self):
        return self.t4.dfc, self.t3.dfc, self.t7.dfc


class Lstm(Chain):
    def __init__(self, w_f, u_f, b_f, w_i, u_i, b_i, w_o, u_o, b_o, w_c, u_c, b_c, n):
        self.h = Var(n, 1)
        self.x = Var(n, 1)
        self.c = Var(n, 1)

        self.f_t = Sigmator(self.h, self.x, w_f, u_f, b_f, n, Sigm)
        self.i_t = Sigmator(self.h, self.x, w_i, u_i, b_i, n, Sigm)
        self.o_t = Sigmator(self.h, self.x, w_o, u_o, b_o, n, Sigm)
        self.tmp1 = Sigmator(self.h, self.x, w_c, u_c, b_c, n, Tnh)

        tmp2 = Had([self.i_t, self.tmp1])
        tmp3 = Had([self.f_t, self.c])

        self.c_t = Sum([tmp2, tmp3])
        self.h_t = Had([self.o_t, self.c_t])

        self.chain = [self.h, self.x, self.c, self.f_t, self.i_t, self.o_t, self.tmp1, tmp2, tmp3, self.c_t, self.h_t]

    def dump(self):
        return self.f_t.dump() + self.i_t.dump() + self.o_t.dump() + self.tmp1.dump()



def main():
    n = int(input())

    w_f = read_matrix(n)
    u_f = read_matrix(n)
    b_f = read_vector()

    w_i = read_matrix(n)
    u_i = read_matrix(n)
    b_i = read_vector()

    w_o = read_matrix(n)
    u_o = read_matrix(n)
    b_o = read_vector()

    w_c = read_matrix(n)
    u_c = read_matrix(n)
    b_c = read_vector()
    
    
    # h = Var(n, 1)
    # x = Var(n, 1)
    # c = Var(n, 1)

    nodes = [Lstm(w_f, u_f, b_f, w_i, u_i, b_i, w_o, u_o, b_o, w_c, u_c, b_c, n)]

    m = int(input())
    nodes[0].h.data = read_vector()
    nodes[0].c.data = read_vector()

    # f_t = Sigmator(h, x, w_f, u_f, b_f, n, Sigm)
    # i_t = Sigmator(h, x, w_i, u_i, b_i, n, Sigm)
    # o_t = Sigmator(h, x, w_o, u_o, b_o, n, Sigm)
    # tmp1 = Sigmator(h, x, w_c, u_c, b_c, n, Tnh)

    # tmp2 = Had([i_t, tmp1])
    # tmp3 = Had([f_t, c])
    # c_t = Sum([tmp2, tmp3])
    # h_t = Had([o_t, c_t])

    # chain = [f_t, i_t, o_t, tmp1, tmp2, tmp3, c_t, h_t]

    for i in range(m):
        nodes[-1].x.data = read_vector()
        nodes[-1].eval()

        print_vector(nodes[-1].o_t.data)
        
        if i + 1 < m:
            nodes.append(Lstm(w_f, u_f, b_f, w_i, u_i, b_i, w_o, u_o, b_o, w_c, u_c, b_c, n))
            nodes[-1].c.data = nodes[-2].c_t.data
            nodes[-1].h.data = nodes[-2].h_t.data
    
    print_vector(nodes[-1].h_t.data)
    print_vector(nodes[-1].c_t.data)

    nodes[-1].h_t.df.append(read_vector())
    nodes[-1].c_t.df.append(read_vector())

    for i in range(m):
        nodes[-(i + 1)].o_t.df.append(read_vector())
        nodes[-(i + 1)].eval_back()

        print_vector(nodes[-(i + 1)].x.dfc)

        if i + 1 < m:
            nodes[-(i + 2)].h_t.df.append(nodes[-(i + 1)].h.dfc)
            nodes[-(i + 2)].c_t.df.append(nodes[-(i + 1)].c.dfc)
    
    print_vector(nodes[0].h.dfc)
    print_vector(nodes[0].c.dfc)

    res = [[[0] * n for _ in range(n)] for _ in range(12)]
    for i in range(m):
        dump = nodes[i].dump()
        for j in range(12):
            if j % 3 == 2:
                for a in range(n):
                    res[j][a][0] += dump[j][a][0]
            else:
                for a in range(n):
                    for b in range(n):
                        res[j][a][b] += dump[j][a][b]
    for i in range(12):
        if i % 3 == 2:
            print_vector(res[i])
        else:
            print_matrix(res[i])


def io():
    import sys
    sys.stdin = open("input.txt", "r")
    sys.stdout = open("output.txt", "w")


if __name__ == '__main__':
    io()
    main()
