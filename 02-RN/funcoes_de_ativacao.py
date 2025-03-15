from math import e


def sigmoid(x):
    return 1 / (1 + e ** (-x))


def relu(x):
    return max(0, x)


def degrau(x):
    return 1 if x > 0 else 0
