import math
import sys

INFINITY = 1000000000


def f(x, function):
    if function == 1:
        return 3 * x ** 3 - 2 * x ** 2 + 7 * x + 26
    elif function == 2:
        return math.sin(x)
    elif function == 3:
        if x == 0:
            print("Интеграл терпит бесконечный разрыв в точке x=0")
            sys.exit()
        return 1 / math.sqrt(x)
    elif function == 4:
        if x == 1 / 2:
            print("Интеграл терпит бесконечный разрыв в точке x=1/2")
            sys.exit()
        return 1 / (x - 1 / 2)


def fd(x, function):
    if function == 1:
        return x * (9 * x ** 3 - 8 * x ** 2 + 42 * x + 312) / 12
    elif function == 2:
        return math.cos(x) * -1
    elif function == 3:
        return 2 * math.sqrt(x)
    elif function == 4:
        return math.log(abs(2 * x - 1), math.e)


def integral(function, a, b):
    return fd(b, function) - fd(a, function)


def rectangle_function(function, a, b, n, method):
    h = (b - a) / n
    sum = 0

    for i in range(n):
        if method == 1:
            sum += f(a + (i * h) + h / 2, function) * h
        if method == 2:
            sum += f(a + i * h, function) * h
        if method == 3:
            sum += f(a + i * h + h, function) * h

        if (sum > INFINITY):
            print("Значение интеграла равно бесконечности или слишком велико.")
            sys.exit()

    return sum


def trapeze_function(function, a, b, n):
    h = (b - a) / n
    sum = 0

    for i in range(n):
        sum += f(a + (i * h), function) * h + ((f(a + (i + 1) * h, function) - f(a + i * h, function)) * h / 2)
    return sum


def simpson_function(function, a, b, n):
    h = (b - a) / n
    l = f(a, function) + f(b, function)

    for i in range(1, n):
        l += (2 + 2 * (i % 2)) * f(a + i * h, function)
    return l * h / 3
