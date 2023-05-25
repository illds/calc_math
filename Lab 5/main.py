import math
import sys
import matplotlib.pyplot as plt
import os

import numpy as np

x, y = np.array([]), np.array([])  # Векторы x и y
n = 0  # Размер данных
function_choice = 0


# Ввод с клавиатуры
def keyboard_input() -> None:
    global x, y, n
    n = int(input("Введите размер: "))

    print("Введите значения x, y через пробел:")
    for i in range(n):
        a, b = map(float, input().split())
        np.append(x, a)
        np.append(y, b)


# Ввод с файла
def file_input(file) -> None:
    global x, y, n
    values = np.loadtxt('./files/' + file)
    x = np.array(values[:, 0])
    y = np.array(values[:, 1])
    n = len(x)


def f(x, function_choice):
    if function_choice == 1:
        return np.sin(x)
    if function_choice == 2:
        return np.cos(x)
    if function_choice == 3:
        return x * x - 5 * x + 3


def function_input() -> None:
    global x, y, n, function_choice
    functions = ['sin(x)', 'cos(x)', 'x^2 - 5x + 3']
    print("Выберите функцию:")
    for i, function in enumerate(functions):
        print(f'({i + 1}) {function}')
    function_choice = int(input())

    a = float(input("Введите границы функций (a): "))
    b = float(input("Введите границы функций (b): "))
    n = int(input("Введите количество точек: "))
    x = np.linspace(a, b, n)
    y = f(x, function_choice)
    print("x:", x)
    print("y:", y)


def draw() -> None:
    interpolation_x = np.linspace(min(x), max(x), 100)
    interpolation_lagrange, interpolation_gaussian = np.zeros(100), np.zeros(100)
    for i, xi in enumerate(interpolation_x):
        interpolation_lagrange[i] = lagrange_polynomial(xi)
        interpolation_gaussian[i] = gaussian_polynomial(xi)

    plt.plot(x, y, 'o', label='Заданные точки')
    plt.plot(interpolation_x, interpolation_lagrange, label='Многочлен Лагранжа')
    plt.plot(interpolation_x, interpolation_gaussian, label='Многочлен Гаусса')
    plt.legend()
    plt.show()


def lagrange_polynomial(arg) -> float:
    lagrange_result = 0.0
    for i in range(n):
        term = y[i]
        for j in range(n):
            if i != j:
                try:
                    term *= (arg - x[j]) / (x[i] - x[j])
                except ZeroDivisionError:
                    print("Невозможно решение многочленом Лагранжа")
                    return 0
        lagrange_result += term
    return lagrange_result


def fact(x):
    if x <= 1:
        return 1
    return x * fact(x - 1)


def gaussian_polynomial(arg) -> float:  # Многочлен Гаусса
    j = len(table) // 2 - (1 if (len(table) % 2 == 0) else 0)
    initial_j = j
    gaussian_result = table[j][0]
    h = abs(x[0] - x[1])
    t = (arg - x[j]) / h
    production_t = 1

    for i in range(1, n):
        if i % 2 == 1:
            if arg < x[initial_j]:
                production_t *= (t - i // 2)
                j -= 1
            else:
                production_t *= (t + i // 2)
        else:
            if arg < x[initial_j]:
                production_t *= (t + i // 2)
            else:
                production_t *= (t - i // 2)
                j -= 1
        gaussian_result += production_t * table[j][i] / fact(i)
    return gaussian_result


def main():
    global table
    header = "Эрбаев Ильдус. Лабораторная работа №5."

    choice_input = 0
    while choice_input != 1 and choice_input != 2 and choice_input != 3:
        print(header)
        print("Ввести данные:\n(1) Из файла.\n(2) Из клавиатуры.\n(3) Из функции.")
        choice_input = int(input())

        if choice_input == 1:  # Ввод с файла
            files = os.listdir('files/')
            file_number = 0
            while file_number <= 0 or file_number > len(files):
                print("Выберите файл:")
                for i, file in enumerate(files):
                    print(f"({i + 1}) {file}")
                file_number = int(input())

                if 1 <= file_number <= len(files):
                    file = files[file_number - 1]
                    file_input(file)
        elif choice_input == 2:  # Ввод с клавиатуры
            keyboard_input()
        elif choice_input == 3:
            function_input()

        header = "Неверно введены данные. Попробуйте еще раз."

    arg = float(input("Введите значение аргумента: "))

    # Создание таблицы конечных разностей
    table = np.zeros((n, n))
    table[:, 0] = y

    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = (table[i + 1][j - 1] - table[i][j - 1])

    # Вывод таблицы разностей
    print("Таблица конечных разностей:")
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] != 0:
                print(round(table[i][j], 4), end="\t")
        print()

    lagrange_result = lagrange_polynomial(arg)
    gaussian_result = gaussian_polynomial(arg)
    if choice_input == 3:
        print('Значение функции:', f(arg, function_choice))
    print('Значение функции методом многочлена Лагранжа:', lagrange_result)
    print('Значение функции методом многочлена Гаусса:', gaussian_result)
    print('Модуль разности методов:', abs(lagrange_result - gaussian_result))
    draw()


if __name__ == '__main__':
    main()
