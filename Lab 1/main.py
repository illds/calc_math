import math
from os import system
import numpy as np

# Ввод с файла
def file_input():
    A = np.loadtxt('input1.txt', unpack=True, dtype=float) # Распаковка матрицы в A
    A = np.transpose(A) # Транспонирование матрицы

    b = A[len(A)-1]
    A = np.delete(A, (len(A)-1), axis=0)

    return A, b

# Ввод с клавиатуры
def keyboard_input():
    n = int(input("Введите размерность матрицы: "))
    A = []
    print("Введите матрицу:")
    for i in range(n):
        print(f"Введите {i+1}-й ряд: ", end = '')
        row = [float(i) for i in input().split(' ', n - 1)]
        A.append(row)

    print("Введите столбец свободных членов:\n", end = '')
    b = [float(i) for i in input().split(' ', n - 1)]

    return np.array(A, float), np.array(b, float)

def gauss(A, b):
    n = len(b)

    s = 0
    # Прямой ход метода Гаусса
    for k in range(n):
        # Поиск максимального элемента в столбце
        max_row = k

        if A[k, k] == 0:
            for i in range(k+1, n):
                if A[i, k] != 0:
                    max_row = i
                    break
            s += 1

        # Перестановка строк
        A[[k, max_row], :] = A[[max_row, k], :]
        b[k], b[max_row] = b[max_row], b[k]

        # Приведение матрицы к верхнетреугольному виду
        for i in range(k + 1, n):
            c = A[i, k] / A[k, k]
            A[i, k:n] -= c * A[k, k:n]
            b[i] -= c * b[k]

    # Обратный ход метода Гаусса
    x = np.zeros(n)
    for k in range(n - 1, -1, -1):
        x[k] = (b[k] - np.dot(A[k, k + 1:], x[k + 1:])) / A[k, k] # numpy.dot - скалярное произведение

    # Вычисление вектора невязок
    r = b - np.dot(A, x) # numpy.dot - скалярное произведение

    # Вычисление определителя матрицы
    det = np.prod(np.diag(A)) * math.pow(-1, s)

    return x, r, det

# Приветствие и ввод матрицы и столбца свободных членов
def start():
    print("Добро пожаловать в программу решения СЛАУ методом Гаусса")
    print("Как вы хотите ввести данные?")
    print("(1) С клавиатуры.")
    print("(2) С файла (input.txt).")

    choice = str(input("Выбор: "))
    while choice != "1" and choice != "2":
        print("Некорректный ввод!")
        choice = str(input("Выбор: "))

    system('cls')  # Очистка консоли

    return choice

def main():
    if start() == "1":
        A, b = keyboard_input()
    else:
        A, b = file_input()

    det_lib = np.linalg.det(A)

    # Решение системы уравнений методом Гаусса
    x, r, det = gauss(A, b)

    # Вывод результатов
    print("Матрица коэффициентов:\n", A)
    print("Столбец свободных членов:\n", b)

    if math.isnan(det) or det == 0:
        print("Определитель матрицы равен нулю.")
    else:
        print("Вычисленный определитель матрицы по главной диагонали:", det)
        print("Вычисленный определитель матрицы с помощью библиотеки:", det_lib)

    print("Вектор неизвестных:\n", x)
    print("Вектор невязок:\n", r)

if __name__ == "__main__":
    main()