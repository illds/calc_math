import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

function_number = 0
eps = 0


def solve_ode(x, y):
    # Точное решение
    return solve_ivp(f, [x[0], x[-1]], [y], t_eval=x).y[0]


def f(x, y):
    if function_number == 1:
        return x * x - 2 * y
    elif function_number == 2:
        return 1 - 3 * x + (0.5 * y) / (x + 2)
    elif function_number == 3:
        return x + np.sin(3 * y / 2)


def euler_method(x, y, h, n):
    # Метод Эйлера
    xn, yn, fn = np.array([]), np.array([]), np.array([])
    for i in range(n):
        fxy = f(x, y)
        hfxy = h * fxy
        xn = np.append(xn, x)
        yn = np.append(yn, y)
        fn = np.append(fn, f(x, y))
        x += h
        y = y + hfxy
    xn = np.append(xn, x)
    yn = np.append(yn, y)
    fn = np.append(fn, f(x, y))
    return xn, yn, fn


def upgraded_euler_method(x, y, h, n):
    # Модифицированный метод Эйлера
    xn, yn, fn = np.array([]), np.array([]), np.array([])
    for i in range(n):
        delta_y = h * f(x + h / 2, y + h / 2 * f(x, y))

        xn = np.append(xn, x)
        yn = np.append(yn, y)
        fn = np.append(fn, f(x, y))
        x += h
        y = y + delta_y
    xn = np.append(xn, x)
    yn = np.append(yn, y)
    fn = np.append(fn, f(x, y))
    return xn, yn, fn


def adams_method(x0, y0, h, n):
    # Метод Адамса
    y = y0
    xn, yn, fn = upgraded_euler_method(x0, y, h, 3)

    index = 3
    while index < n:

        predictor = yn[-1] + h / 24 * (55 * fn[-1] - 59 * fn[-2] + 37 * fn[-3] - 9 * fn[-4])
        corrector = yn[-1] + h / 24 * (9 * f(xn[-1] + h, predictor) + 19 * fn[-1] - 5 * fn[-2] + fn[-3])

        while abs(predictor - corrector) > eps:
            predictor = corrector
            corrector = yn[-1] + h / 24 * (9 * f(xn[-1] + h, predictor) + 19 * fn[-1] - 5 * fn[-2] + fn[-3])

        xn = np.append(xn, xn[-1] + h)
        yn = np.append(yn, corrector)
        fn = np.append(fn, f(xn[-1], yn[-1]))
        index += 1
    return xn, yn, fn

def print_result(x, y, label):
    print(f"{label}\nx: {x}\ny: {y}\n")


def main():
    global eps
    global function_number
    print("Эрбаев Ильдус. Лабораторная работа №6.")
    header = "Выберите функцию:"

    function_number = 0
    functions = ["x^2 - 2y", "1 - 3x + (0.5y) / (x + 2)", "x + sin(3y/2)"]
    while function_number <= 0 or function_number > len(functions):
        print(header)
        for i, function in enumerate(functions):
            print(f"({i + 1}) y' = {function}")
        function_number = int(input())

        header = "Неверно введены данные. Попробуйте еще раз."

    x = float(input("Введите x0: "))
    y = float(input("Введите y0: "))
    h = float(input("Введите h: "))
    n = int(input("Введите n: "))
    eps = float(input("Точность eps: "))

    x_values = np.linspace(x, x + h * n, 100)
    y_values = solve_ode(x_values, y)

    x1, y1, _ = euler_method(x, y, h, n)
    x2, y2, _ = euler_method(x, y, h/2, n*2)
    h_save, n_save = h, n
    while (y1[-1] - y2[-1]) / 2 ** 2 - 1 >= eps: # Правило Рунге (p = 2)
        h_save /= 2
        n_save *= 2
        x1, y1, _ = euler_method(x, y, h_save, n_save)
        x2, y2, _ = euler_method(x, y, h_save / 2, n_save * 2)
    x_euler, y_euler = x2, y2

    x1, y1, _ = upgraded_euler_method(x, y, h, n)
    x2, y2, _ = upgraded_euler_method(x, y, h/2, n*2)
    h_save, n_save = h, n
    while (y1[-1] - y2[-1]) / 2 ** 4 - 1 >= eps: # Правило Рунге (p = 4)
        h_save /= 2
        n_save *= 2
        x1, y1, _ = upgraded_euler_method(x, y, h_save, n_save)
        x2, y2, _ = upgraded_euler_method(x, y, h_save / 2, n_save * 2)
    x_upg_euler, y_upg_euler = x2, y2

    x_adams, y_adams, _ = adams_method(x, y, h, n)

    x_ex = np.linspace(x, x + h * n, n + 1)
    y_ex = solve_ode(x_ex, y)
    print_result(x_ex, y_ex, 'Точное решение')
    print_result(x_euler, y_euler, 'Метод Эйлера')
    print_result(x_upg_euler, y_upg_euler, 'Модифицированный метод Эйлера')
    print_result(x_adams, y_adams, 'Метод Адамса')

    plt.plot(x_values, y_values, label='Точное решение')
    plt.plot(x_adams, y_adams, label='Метод Адамса')
    plt.plot(x_euler, y_euler, label='Метод Эйлера')
    plt.plot(x_upg_euler, y_upg_euler, label='Модифицированный метод Эйлера')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()