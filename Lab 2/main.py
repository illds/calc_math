import sys
import math
import numpy as np
import matplotlib.pyplot as plt

def welcome():
    global choice
    global method
    choice = 0
    method = 0

    header = "Лабораторная работа №2. Автор: Эрбаев Ильдус."
    while choice > 4 or choice <= 0 or method > 5 or method <= 0:
        print(header)
        print("Введите уравнение:\n(1) 1.62x^3 - 8.15x^2 + 4.39x + 4,29")
        print("(2) x^2 - 6x + 2 = 0")
        print("(3) sin(x) + x = 0")
        print("(4) | sin(y + 2) - x = 15")
        print("    | y + cos(x - 2) = 0.5")
        print("(5) | x - y = 7")
        print("    | x * y = 18")
        choice = int(input())

        if choice == 4 or choice == 5:
            print("Автоматически выбран метод простых итераций.")
            method = 4
            break

        print("Введите метод:\Для нелийнейных уравнений:")
        print("(1) Метод половинного деления.")
        print("(2) Метод Ньютона.")
        print("(3) Метод секущих.")
        print("Для систем нелийнейных уравнений:")
        print("(4) Метод простых итераций.")
        method = int(input())

        header = "\nОшибка валидации введенных данных. Попробуйте еще раз."

    return choice, method

# Функция
def f(x):
    if choice == 1:
        return 1.62*x*x*x-8.15*x*x+4.39*x+4.29
    elif choice == 2:
        return x*x - 6*x + 2
    elif choice == 3:
        return math.sin(x) + x
    else:
        print("Error: f(x).")
        sys.exit()

# Производная от функции
def fd(x):
    if choice == 1:
        return 4.86*x*x-16.3*x+4.39
    elif choice == 2:
        return 2*x - 6
    elif choice == 3:
        return math.cos(x) + 1
    else:
        print("Error: f'(x).")
        sys.exit()

# Двойная производная от функции
def fdd(x):
    if choice == 1:
        return 9.72*x-16.3
    elif choice == 2:
        return 2
    elif choice == 3:
        return -math.sin(x)
    else:
        print("Error: f''(x).")
        sys.exit()

# φ функция (фи)
def g(x):
    if choice == 1:
        return -4.29/(1.62*x*x-8.15*x+4.39)
    elif choice == 2:
        return x*x - 5*x + 2
    else:
        print("Error: g(x)")
        sys.exit()

# Выбор начального приближения
def initial_x(a, b):
    if method == 2 or method == 3:
        if f(a) * fdd(a) > 0:
            return a
        elif f(b) * fdd(b) > 0:
            return b
        return a
    elif method == 4:
        return (a + b) / 2
    else:
        print("Error: initial x.")
        sys.exit()

# Метод половинного деления
def bisection_method(a, b, eps):
    n = 0
    x = (a + b) / 2
    while abs(a-b) > eps or abs(f(x)) > eps:
        x = (a + b) / 2
        if f(a) * f(x) > 0:
            a = x
        else:
            b = x
        n += 1

        print(a-b)
    return [x, f(x), n]

# Метод Ньютона
def newtons_method(a, eps):
    x0 = a
    x = x0 - f(x0)/fd(x0)
    n = 0
    while abs(x - x0) > eps and abs(f(x) / fd(x)) > eps and abs(f(x)) > eps:
        x0, x = x, (x - f(x) / fd(x))
        n += 1

    return [x, f(x), n]

# Метод секущих
def secant_method(a, eps):
    x0 = a
    x1 = a + (0.01 if x0 > 0 else -0.01)
    x = x1 - ((x1-x0)/(f(x1)-f(x0)))*f(x1)

    n = 0
    while abs(x - x1) > eps and abs(f(x)) > eps:
        x0, x1 = x1, x
        x = x1 - ((x1 - x0) / (f(x1) - f(x0))) * f(x1)
        n += 1

    return [x, f(x), n]

# Метод простых итераций
def fixed_point_method(x0, eps):
    x = g(x0)
    n = 0

    while abs(x - x0) > eps:
        x0 = x
        x = g(x0)
        n += 1


    return [x, f(x), n]

def fixed_point_method_system(x0, y0, eps):
    if choice == 4:
        x = math.sin(y0 + 2) - 15
        y = 0.5 - math.cos(x0 - 2)
        x0, y0 = x, y
        d1 = math.sin(y+2) - x - 15
        d2 = y + math.cos(x-2)-0.5
    if choice == 5:
        x = 7 + y0
        y = 18/x0
        x0, y0 = x, y
        d1 = 7 + y - x
        d2 = 18 - x * y

    n = 0
    while abs(d1) > eps or abs(d2) > eps:
        if choice == 4:
            x, x0 = math.sin(y0 + 2) - 15, x
            y, y0 = 0.5 - math.cos(x0 - 2), y
            d1 = math.sin(y + 2) - x - 15
            d2 = y + math.cos(x - 2) - 0.5
        elif choice == 5:
            x = 7 + y0
            y = 18 / x0
            x0, y0 = x, y
            d1 = 7 + y - x
            d2 = 18 - x * y
        else:
            print("Error: system choice.")
            sys.exit()

        n += 1

    return [x, y, n]

def f1(x, y):
    return np.sin(y + 2) - x - 15

def f2(x, y):
    return y + np.cos(x - 2) - 0.5

def printer(a):
    if choice <= 3:
        print("Неизвестное x:", a[0])
        print("Значение f(x):", a[1])
        print("Количество итераций:", a[2])
    else:
        print("Значение x:", a[0])
        print("Значение y:", a[1])
        print(f1(a[0], a[1]))
        print(f2(a[0], a[1]))
        print("Количество итераций:", a[2])
    sys.exit()

# Главная функция
def main():
    choice, method = welcome()

    if choice == 1:
        x = np.linspace(-2, 5, 100)
        plt.plot(x, f(x))
        plt.grid()
        plt.axhline(y=0, color='k')
        plt.show()
    elif choice == 2:
        x = np.linspace(-5, 10, 100)
        plt.plot(x, f(x))
        plt.grid()
        plt.axhline(y=0, color='k')
        plt.show()
    elif choice == 3:
        x = np.linspace(-10, 10, 1000)
        plt.plot(x, np.sin(x)+x)
        plt.grid()
        plt.axhline(y=0, color='k')
        plt.show()
    elif choice == 4:
        # Задаем диапазон значений x и y
        x = np.linspace(-20, 20, 1000)
        y = np.linspace(-20, 20, 1000)

        X, Y = np.meshgrid(x, y)

        Z1 = f1(X, Y)
        Z2 = f2(X, Y)

        fig, ax = plt.subplots()
        ax.contour(X, Y, Z1, levels=[0], colors='r')
        ax.contour(X, Y, Z2, levels=[0], colors='b')
        plt.show()

    elif choice == 5:
        x = np.linspace(-50, 50, 100)
        plt.plot(x, x - 7)
        plt.plot(x, 18 / x)
        plt.grid()
        plt.axhline(y=0, color='k')
        plt.show()

    if choice != 4 and choice != 5:
        a = float(input("Введите a: "))
        b = float(input("Введите b: "))

        sign = (False if f(a) < 0 else True)
        g = abs(b - a)/1000
        k = 0
        for i in range(1000):
            if f(a+i*g) < 0 and sign:
                k += 1
                sign = False
            elif f(a+i*g) >= 0 and not sign:
                k += 1
                sign = True
        if k == 0:
            print("Error: на интервале нет корней.")
            sys.exit()
        elif k > 1:
            print("Error: на интервале больше 1 корня.")
            sys.exit()
        else:
            print("На интервале 1 корень.")

        eps = float(input("Введите точность (eps): "))

    else:
        x0 = float(input("Начальное приблежение x: "))
        y0 = float(input("Начальное приблежение y: "))
        eps = float(input("Введите точность (eps): "))

        printer(fixed_point_method_system(x0, y0, eps))
        sys.exit()

    if method == 1:
        printer(bisection_method(a, b, eps))
    elif method == 2:
        a = initial_x(a, b)
        printer(newtons_method(a, eps))
    elif method == 3:
        a = initial_x(a, b)
        printer(secant_method(a, eps))
    elif method == 4:
        a = initial_x(a, b)
        printer(fixed_point_method(a, eps))
    else:
        print("Error: method.")
        sys.exit()

if __name__ == "__main__":
    main()