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
        if self.dfc:
            return
        self.dfc = [[0] * self.c for _ in range(self.r)]
        for df_i in self.df:
            for i in range(self.r):
                for j in range(self.c):
                    self.dfc[i][j] += df_i[i][j]


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


class Rlu(Node):
    def __init__(self, alpha, x):
        super().__init__()
        self.alpha = alpha
        self.x = x
        self.r = x.r
        self.c = x.c

    def eval(self):
        self.data = list(map(lambda row: list(map(lambda x: self.alpha * x if x < 0 else x, row)), self.x.data))

    def eval_back(self):
        self.prepare_df()

        result = copy.deepcopy(self.dfc)
        for i in range(self.r):
            for j in range(self.c):
                x = self.x.data[i][j]
                f = lambda x: self.alpha if x < 0 else 1
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
        if len(u) == 0:  # TODO
            while True:
                pass
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
            

def main():
    n, m, k = map(int, input().split())
    
    nodes = [None] * n

    for i in range(n):
        s = input().split()
        node_type = s[0]

        if node_type == "var":
            nodes[i] = Var(int(s[1]), int(s[2]))
        elif node_type == "tnh":
            nodes[i] = Tnh(nodes[int(s[1]) - 1])
        elif node_type == "rlu":
            nodes[i] = Rlu(1 / int(s[1]), nodes[int(s[2]) - 1])
        elif node_type == "mul":
            nodes[i] = Mul(nodes[int(s[1]) - 1], nodes[int(s[2]) - 1])
        elif node_type == "sum":
            nodes[i] = Sum([nodes[int(u_i) - 1] for u_i in s[2:]])
        elif node_type == "had":
            nodes[i] = Had([nodes[int(u_i) - 1] for u_i in s[2:]])

    for i in range(m):
        node = nodes[i]
        node.data = [list(map(float, input().split())) for _ in range(node.r)]
    
    for i in range(k):
        node = nodes[n - k + i]
        node.df.append([list(map(float, input().split())) for _ in range(node.r)])

    for i in range(n):
        nodes[i].eval()

    for i in range(n):
        nodes[-(i + 1)].eval_back()

    for i in range(k):
        for row in nodes[n - k + i].data:
            print(" ".join(map(str, row)))
    
    for i in range(m):
        for row in nodes[i].dfc:
            print(" ".join(map(str, row)))


def io():
    import sys
    sys.stdin = open("input.txt", "r")
    sys.stdout = open("output.txt", "w")


if __name__ == '__main__':
    io()
    main()
