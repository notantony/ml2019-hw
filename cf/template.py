import math


def main():
    k = int(input())
    n = int(input())
    
    x = [0] * n
    y = [0] * n 
    
    for i in range(n):
        _x, _y = map(int, (input().split()))
        print(_x, _y)
        x[i] = _x
        y[i] = _y


if __name__ == '__main__':
    main()
