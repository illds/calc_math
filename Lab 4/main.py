import math
import sys
import matplotlib.pyplot as plt

import numpy as np


x, y = np.array([]), np.array([])  # Векторы x и y
n = 0  # Размер данных
coefficients = [[] for i in range(6)]


# Ввод с клавиатуры
def keyboard_input():
    global x, y, n
    n = int(input("Введите размер: "))

    print("Введите значения x, y через пробел:")
    for i in range(n):
        a, b = map(float, input().split())
        np.append(x, a)
        np.append(y, b)


# Ввод с файла
def file_input(file):
    global x, y, n
    values = np.loadtxt(file)
    x = np.array(values[:, 0])
    y = np.array(values[:, 1])
    n = len(x)


# Линейная аппроксимация
def linear_approximation():
    global coefficients
    SX, SXX = sum(x), sum(x * x)
    SY, SXY = sum(y), sum(x * y)

    delta = SXX * n - SX * SX
    delta1 = SXY * n - SX * SY
    delta2 = SXX * SY - SX * SXY

    try:
        a = delta1 / delta
        b = delta2 / delta
    except ZeroDivisionError:
        print('Деление на ноль.')
        sys.exit()

    coefficients[0] = [a, b]
    return lambda given_x: a * given_x + b


# Коэфф. кореляции
def correlation_coefficient(x, y):
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    numerator = sum((x - x_mean) * (y - y_mean))
    denominator = np.sqrt(sum((x - x_mean) * (x - x_mean)) * sum((y - y_mean) * (y - y_mean)))

    return numerator / denominator


# Квадратичная аппроксимация (полином 2 степени)
def quadratic_approximation():
    global coefficients
    A = np.array([  # Матрица (левая часть системы)
        [n, sum(x), sum(x * x)],
        [sum(x), sum(x ** 2), sum(x ** 3)],
        [sum(x ** 2), sum(x ** 3), sum(x ** 4)]
    ])
    b = np.array([sum(y), sum(x * y), sum(x ** 2 * y)])  # Вектор (правая часть системы)
    a0, a1, a2 = np.linalg.solve(A, b)

    coefficients[1] = [a2, a1, a0]
    return lambda x: a2 * x ** 2 + a1 * x + a0


# Кубическая аппроксимация (полином 3 степени)
def cubic_approximation():
    global coefficients
    A = np.array([  # Матрица (левая часть системы)
        [n, sum(x), sum(x ** 2), sum(x ** 3)],
        [sum(x), sum(x ** 2), sum(x ** 3), sum(x ** 4)],
        [sum(x ** 2), sum(x ** 3), sum(x ** 4), sum(x ** 5)],
        [sum(x ** 3), sum(x ** 4), sum(x ** 5), sum(x ** 6)]
    ])
    b = np.array([sum(y), sum(x * y), sum(x ** 2 * y), sum(x ** 3 * y)])  # Вектор (правая часть системы)
    a0, a1, a2, a3 = np.linalg.solve(A, b)

    coefficients[2] = [a3, a2, a1, a0]
    return lambda x: a3 * x ** 3 + a2 * x ** 2 + a1 * x + a0


# Экспоненциальная аппроксимация
def exp_approximation():
    global coefficients
    ln_y = np.array([])
    for yi in y:
        if yi <= 0:
            # print('Значение y меньше 0.')
            print('Экспоненциальная аппроксимация невозможна.')
            return None

        ln_y = np.append(ln_y, math.log(yi, math.e))

    A = np.array([  # Матрица (левая часть системы)
        [sum(x ** 2), sum(x)],
        [sum(x), n]
    ])
    b = np.array([sum(x * ln_y), sum(ln_y)])  # Вектор (правая часть системы)

    a0, a1 = np.linalg.solve(A, b)
    a1 = np.exp(a1)

    coefficients[3] = [a1, a0]
    return lambda x: a1 * np.exp(a0 * x)


# Логарифмическая аппроксимация
def log_approximation():
    global coefficients
    ln_x = np.array([])
    for xi in x:
        if xi <= 0:
            print('Логарифмическая аппроксимация невозможна.')
            return None
        ln_x = np.append(ln_x, math.log(xi, math.e))

    A = np.array([  # Матрица (левая часть системы)
        [sum(ln_x ** 2), sum(ln_x)],
        [sum(ln_x), n]
    ])
    b = np.array([sum(ln_x * y), sum(y)])  # Вектор (правая часть системы)

    a0, a1 = np.linalg.solve(A, b)

    coefficients[4] = [a0, a1]
    return lambda given_x: a0 * math.log(given_x, math.e) + a1


# Степенная аппроксимация
def pow_approximation():
    global coefficients
    ln_x = np.array([])
    ln_y = np.array([])
    for i, xi in enumerate(x):
        if xi <= 0 or y[i] <= 0:
            print('Степенная аппроксимация невозможна.')
            return None
        ln_x = np.append(ln_x, math.log(xi, math.e))
        ln_y = np.append(ln_y, math.log(y[i], math.e))

    A = np.array([  # Матрица (левая часть системы)
        [sum(ln_x ** 2), sum(ln_x)],
        [sum(ln_x), n]
    ])
    b = np.array([sum(ln_x * ln_y), sum(ln_y)])  # Вектор (правая часть системы)

    a0, a1 = np.linalg.solve(A, b)
    a1 = np.exp(a1)

    coefficients[5] = [a1, a0]
    return lambda x: a1 * x ** a0


def draw(f, eps_name):
    plt.plot(x, y, 'o', label='Заданные точки')
    plt.plot(x, f(x), label=eps_name)
    plt.legend()
    plt.show()


def main():
    header = "Эрбаев Ильдус. Лабораторная работа №4."

    choice_input = 0
    files = ['linear', 'linear2', 'quadratic', 'cubic', 'exp', 'log', 'pow', 'task']
    while choice_input != 1 and choice_input != 2:
        print(header)
        print("Ввести данные:\n(1) Из файла.\n(2) Из клавиатуры.")
        choice_input = int(input())

        if choice_input == 1:
            file_number = 0
            while file_number <= 0 or file_number > len(files):
                print("Выберите файл:")
                for i, file in enumerate(files):
                    print(f"({i + 1}) {file}.txt")
                file_number = int(input())

                if 1 <= file_number <= len(files):
                    file = files[file_number - 1] + '.txt'
                    file_input(file)
        elif choice_input == 2:
            keyboard_input()

        header = "Неверно введены данные. Попробуйте еще раз."

    f_linear = linear_approximation()
    f_quadratic = quadratic_approximation()
    f_cubic = cubic_approximation()
    f_exp = exp_approximation()
    f_log = log_approximation()
    f_pow = pow_approximation()

    functions = np.array([f_linear, f_quadratic, f_cubic, f_exp, f_log, f_pow])
    eps = np.array([])
    for j in range(len(functions)):
        f = functions[j]
        if f == None:
            eps = np.append(eps, None)
            continue
        eps_value = 0
        for i in range(len(x)):
            eps_value += (f(x[i]) - y[i]) ** 2
        eps = np.append(eps, eps_value)

    eps_names = ['Линейная', 'Квадратичная', 'Кубическая',
                 'Экспоненциальная', 'Логарифмическая', 'Степенная']

    min_eps_index = 0
    min_value = eps[0]
    for i in range(len(functions)):
        if eps[i] == None:
            continue
        eps[i] = math.sqrt(eps[i] * eps[i] / n)
        if eps[i] < min_value:
            min_value = eps[i]
            min_eps_index = i

    for eps_i, eps_value in enumerate(eps):
        if eps_value is None:
            continue
        print(f"Среднеквадратичное отклонение {eps_names[eps_i][:-2].lower()}ой аппроксимации: {round(eps_value, 5)}")

    draw(np.vectorize(functions[min_eps_index]), eps_names[min_eps_index] + ' аппроксимация')

    print(
        f"\nМинимальное среднеквадратичное отклонение у {eps_names[min_eps_index][:-2].lower()}ой аппроксимации: " + str(
            round(min_value, 5)))
    if min_eps_index == 0:
        print("Коэффициент корреляции: " + str(correlation_coefficient(x, y)))

    print(f"Коэффициенты аппроксимации: {coefficients[min_eps_index]}")

    print("\nx\ty\tg(x)\t|g(x) - y|")
    for i, xi in enumerate(x):
        print(f"{round(xi, 4)} {round(y[i], 4)} {round(functions[min_eps_index](xi), 4)} {round(abs(functions[min_eps_index](xi)-y[i]), 4)}")


if __name__ == '__main__':
    main()
