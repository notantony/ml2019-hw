import itertools
import operator
import functools
import math


eps = 1e-200
inf = float("inf")

def readint():
    return int(input())


def my_log(x):
    return math.log(x) if x > 0 else -inf

messages_in_class = dict()
messages_with_word_in_class = dict()
words_in_class = dict()
different_words_in_class = dict()


k = readint()
lams = list(map(int, input().split()))
alpha = readint()
n = readint()
cs = []
for i in range(n):
    tmp = input().split()
    c_class = int(tmp[0])
    cs.append(c_class)
    messages_in_class[c_class] = messages_in_class.get(c_class, 0) + 1
    
    c_words = set(tmp[2:])
    for c_word in c_words:
        messages_with_word_in_class[(c_word, c_class)] = messages_with_word_in_class.get((c_word, c_class), 0) + 1

    words_in_class[c_class] = words_in_class.get(c_class, set()) | c_words

for c_class, c_words in words_in_class.items():
    different_words_in_class[c_class] = len(c_words)


def p(w, c):
    return my_log(messages_with_word_in_class.get((w, c), 0) + alpha) - \
           (my_log(messages_in_class.get(c, 0) + alpha * different_words_in_class.get(c, 0)) if messages_in_class.get(c, 0) + alpha * different_words_in_class.get(c, 0) > 0 else inf)

def p_class(c):
    return (messages_in_class.get(c, 0)) / sum(messages_in_class.values())


def solve(words_test):
    result = []
    count = 0
    for c in range(1, k + 1):
        log_s = 0
        for w in set(words_test):
           log_s += p(w, c)
        log_s += my_log(p_class(c)) + my_log(lams[c - 1])
        result.append(log_s)
    #if count == 1:
    result = [math.exp(x - max(result)) for x in result]  # result
    return [x / sum(result) for x in result]

    # else:  # T3
    #     result = [lams[c - 1] for c in range(1, c + 1)]
    #     return [x / sum(result) for x in result]  # result
    #     # while True:
        #     assert False


m = readint()
for i in range(m):
    tmp = input().split()
    words_test = tmp[1:]
    result = solve(words_test)
    print(" ".join(["{:.12f}".format(x) for x in result]))
