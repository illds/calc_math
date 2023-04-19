import methods


def difference(x, y):
    return round(abs(abs(x - y) / x * 100), 5)


def main():
    n = 4  # Начальное число разбиений
    header = "Лабораторная работа №3. Эрбаев Ильдус"
    function = 0
    method = 0

    while function > 4 or function < 1 or method > 5 or method < 1:
        print(header)
        print("Введите уравнение:\n(1) 3x^3 - 2x^2 + 7x + 26")
        print("(2) sin(x)")
        print("(3) 1 / sqrt(x)")
        print("(4) 1 / (x - 1/2)")
        function = int(input())  # Номер выбранной функции
        print("Введите метод:\n(1) Метод средних прямоугольников.")
        print("(2) Метод левых прямоугольников.")
        print("(3) Метод правых прямоугольников.")
        print("(4) Метод трапеций.")
        print("(5) Метод Симпсона.")
        method = int(input())  # Номер выбранного метода

        header = "Ошибка введенных данных. Попробуйте еще раз."

    # Пределы интегрирования
    print("\nВведите пределы интегрирования:")
    a = float(input("Введите a: "))
    b = float(input("Введите b: "))

    eps = float(input("Введите точность (eps):"))  # Точность вычисления

    ans1, ans2 = 0, 0
    if 1 <= method <= 3:
        ans1 = methods.rectangle_function(function, a, b, int(n / 2), method)
        ans2 = methods.rectangle_function(function, a, b, n, method)
    elif method == 4:
        ans1 = methods.trapeze_function(function, a, b, int(n / 2))
        ans2 = methods.trapeze_function(function, a, b, n)
    elif method == 5:
        ans1 = methods.simpson_function(function, a, b, int(n / 2))
        ans2 = methods.simpson_function(function, a, b, n)

    while abs((ans2 - ans1) / (2 ** (2 if method <= 4 else 4) - 1)) > eps:
        ans1 = ans2
        n *= 2
        if 1 <= method <= 3:
            ans2 = methods.rectangle_function(function, a, b, n, method)
        elif method == 4:
            ans2 = methods.trapeze_function(function, a, b, n)
        elif method == 5:
            ans2 = methods.simpson_function(function, a, b, n)

    print(f"\nТочное значение: {round(methods.integral(function, a, b), 5)}")
    print(f"Значение интеграла: {round(ans2, 5)}\nЧисло разбиения интервала интегрирования: {n}")
    print(f"Относительная погрешность: {difference(methods.integral(function, a, b), ans2)}%")


if __name__ == '__main__':
    main()
