import numpy as np
import math

def manhattan(v1, v2):
    return np.sum(np.abs(v1 - v2))


def euclidean(v1, v2):
    return np.sqrt(np.sum((v1 - v2) ** 2))


def chebyshev(v1, v2):
    return np.max(abs(v1 - v2))


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
 
def f_score(m):
    n = m.shape[0]
    tp = np.zeros((n,))
    fp = np.zeros((n,))
    fn = np.zeros((n,))
    p = np.zeros((n,))
    p_res = np.zeros((n,))
    
    tp_all = 0.0
    all_s = 0.0

    for i in range(n):
        for j in range(n):
            if i != j:
                fp[i] += m[(j, i)]
                fn[i] += m[(i, j)]

            all_s += m[(i, j)]

        tp_all += m[(i, i)]
        tp[i] = m[(i, i)]
 
    for i in range(n):
        p[i] = tp[i] + fn[i]
        p_res[i] = tp[i] + fp[i]
 
    macro_f = 0.0
    micro_recall = 0.0
    micro_prec = 0.0
    for i in range(n):
        recall_i = tp[i] / p[i]
        prec_i = tp[i] / p_res[i]

        if tp[i] != 0:
            macro_f += 2.0 * recall_i * prec_i / (recall_i + prec_i) * (p[i] / all_s)

            micro_recall += recall_i * p[i] / all_s
            micro_prec += prec_i * p[i] / all_s
 
 
    micro_f = micro_prec * micro_recall * 2.0 / (micro_prec + micro_recall)
    return micro_f, macro_f