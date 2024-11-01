from math import *
import numpy as np
import matplotlib.pyplot as plt
import prettytable as prt


# ввод требуемой точности eps
def correction():
    while True:
        try:
            eps = float(input('Введите точность вычислений: '))
            if 10**(-11) < eps < 1:
                break
            elif eps <= 10**(-21):
                print('Ошибка: переполнение памяти.')
                print('Вы ввели слишком малую точность. Задача не может быть решена.')
            elif eps <= 10**(-15):
                print('Задача будет решаться дольше минуты.')
                ans = input('Введите "да", если хотите начать решение, иначе любой ответ.').lower()
                if ans == "да":
                    break
            elif eps <= 10**(-11):
                print('Задача будет решаться дольше 30 секунд.')
                ans = input('Введите "да", если хотите начать решение, иначе любой ответ.').lower()
                if ans == "да":
                    break
            else:
                print('Вы ввели некорректный ответ!')
                print('Требуется ввести вещественное число от 0 до 1.')
        except ValueError:
            print('Вы ввели некорректный ответ!')
            print('Пожалуйста, введите вещественное число.')
    return int(abs(log10(eps))) + 1, eps


# исходная функция; y(0) = 0, a = 0, b = 1
def f(x, y):
    return (2 * x * exp(x * y)) / ((1 + x*x) * exp(1 + x))


# поиск шага интегрирования
def found_step(a, b, x, y, eps):
    # так как метод рунге-кутты имеет точность 4 порядка относительно шага h, должно выполняться условие h^4 = eps
    h = eps**(1/4)
    # находим погрешность решения
    error = abs(runge_kutta(x + 2*h, y, h) - runge_kutta(x + 2*h, y, 2*h)) / 15

    # если error > eps, то шаг можно уменьшать в 2 раза; если error < eps, то шаг можно увеличивать в 2 раза
    if error > eps:
        while True:
            error = abs(runge_kutta(x + 2*h, y, h) - runge_kutta(x + 2*h, y, 2*h)) / 15
            if error <= eps:
                break
            h /= 2
    else:
        while True:
            error = abs(runge_kutta(x + 2*h, y, h) - runge_kutta(x + 2*h, y, 2*h)) / 15
            if error >= eps:
                break
            h *= 2

    # подбираем четное n и находим шаг h по формуле
    n = int((b - a) / h)
    n += n % 2
    h = (b - a) / n
    return h



# метод Рунге-Кутта 4 порядка (шаблон)
def runge_kutta(x0, y0, h):
    k1 = f(x0, y0)
    k2 = f(x0 + h/2, y0 + h/2*k1)
    k3 = f(x0 + h/2, y0 + h/2*k2)
    k4 = f(x0 + h, y0 + h*k3)
    return y0 + h/6*(k1 + 2*k2 + 2*k3 + k4)


# реализация метода Рунге-Кутта
def implementation_runge_kutta(x0, y0, b, h):
    x = np.arange(x0, b + h/2, h)  # последовательность точек в отрезке [a, b] с шагом h
    y = np.zeros(len(x))  # значения функции в точках (с шагом h)
    y[0] = y0  # задаём начальное значение

    for i in range(len(x) - 1):
        y[i + 1] = runge_kutta(x[i], y[i], h)

    return x, y

# реализация метода Адамса
def adams_method(x0, y0, b, h, eps):

    x = np.arange(x0, b + h/2, h)  # последовательность точек в отрезке [a, b] с шагом h
    y = np.zeros(len(x))  # значения функции в точках

    y[0] = y0  # задаём начальное значение

    # первые 4 точки находим по методу Рунге-Кутты
    for i in range(3):
        y[i + 1] = runge_kutta(x[i], y[i], h)

    for i in range(3, len(x) - 1):
        # экстраполяционная формула Адамса
        y_predictor = y[i] + h * (55 * f(x[i], y[i]) - 59 * f(x[i - 1], y[i - 1]) + 37 * f(x[i - 2], y[i - 2]) - 9 * f(x[i - 3], y[i - 3])) / 24

        h_new = h

        while True:
            # интерполяционная формула Адамса (для уточнения результата)
            y_corrector = y[i] + h_new * (9 * f(x[i + 1], y_predictor) + 19 * f(x[i], y[i]) - 5 * f(x[i - 1], y[i - 1]) + f(x[i - 2], y[i - 2])) / 24

            # вычисляем погрешность решения
            error = np.abs(y_corrector - y_predictor)

            # проверяем, что при заданном шаге погрешность не превышает заданную точность
            if error < eps:
                y[i + 1] = y_corrector
                h = h_new
                break
            else:
                h_new = h_new / 2

    return y


# основная программа
def main():
    print('Численные методы решения задачи Коши\n')

    # начальные данные
    a, b = 0, 1
    count_sign, eps = correction()
    x0, y0 = 0, 0

    h = found_step(a, b, x0, y0, eps)
    print(f'\nИнтегрируем с шагом h = {h:.{count_sign - 1}f}\n')

    # таблицы решений для каждого метода
    adams_tab = prt.PrettyTable(['n', 'xn', 'yn', 'yn^', '|yn^ - yn|'])
    runge_tab = prt.PrettyTable(['n', 'xn', 'yn', 'yn^', '|yn^ - yn|'])
    comp_tab = prt.PrettyTable(['n', 'xn', 'м. Рунге-Кутта', 'м. Адамса', '|yRunge - yAdams|'])

    x, y_rng = implementation_runge_kutta(x0, y0, b, h)
    x2, y2_rng = implementation_runge_kutta(x0, y0, b, 2*h)
    dy_rng = []

    y_ad = adams_method(x0, y0, b, h, eps)
    y2_ad = adams_method(x0, y0, b, 2*h, eps)
    dy_ad = []

    dy_comp = []

    # заполняем таблицы
    for i in range(len(x)):
        if i % 2 == 0:
            runge_tab.add_row([i, round(x[i], count_sign), round(y_rng[i], count_sign), round(y2_rng[i // 2], count_sign), round(abs(y2_rng[i // 2] - y_rng[i]), 15)])
            adams_tab.add_row([i, round(x[i], count_sign), round(y_ad[i], count_sign), round(y2_ad[i // 2], count_sign), round(abs(y2_ad[i // 2] - y_ad[i]), 15)])
            dy_rng.append(abs(y2_rng[i//2] - y_rng[i]) / 15)
            dy_ad.append(abs(y2_ad[i // 2] - y_ad[i]) / 15)

        else:
            runge_tab.add_row([i, round(x[i], count_sign), round(y_rng[i], count_sign), '-', '-'])
            adams_tab.add_row([i, round(x[i], count_sign), round(y_ad[i], count_sign), '-', '-'])

        comp_tab.add_row([i, round(x[i], count_sign), round(y_rng[i], count_sign), round(y_ad[i], count_sign), round(abs(y_rng[i] - y_ad[i]), 15)])
        dy_comp.append(abs(y_rng[i] - y_ad[i]))

    # вывод таблиц с решением и сравнением методов
    print('Реализация метода Рунге-Кутта 4 порядка')
    print(runge_tab)
    print(f'Погрешность решения: dy = max(|yn^ - yn| / 15) = {max(dy_rng):.15f}\n')

    print('Реализация метода Адамса')
    print(adams_tab)
    print(f'Погрешность решения: dy = max(|yn^ - yn| / 15) = {max(dy_ad):.15f}\n')

    print('Сравнение методов Рунге-Кутта и Адамса')
    print(comp_tab)
    print(f'Погрешность решений: dy = max(|yRunge - yAdams|) = {max(dy_comp):.15f}\n')

    # вывод на графике приближённой интегральной кривой
    plt.figure(figsize=[15, 5])
    plt.suptitle('Приближённые интегральные кривые')

    plt.subplot(1, 2, 1)
    plt.plot(x, y_rng, color='red')
    plt.title('Метод Рунге-Кутта')
    plt.xlabel("x")
    plt.ylabel("y(x)")
    plt.xticks(np.arange(min(x), max(x) + 0.1, 0.1))

    plt.subplot(1, 2, 2)
    plt.plot(x, y_ad, color='green')
    plt.title('Метод Адамса')
    plt.xlabel("x")
    plt.ylabel("y(x)")
    plt.xticks(np.arange(min(x), max(x) + 0.1, 0.1))

    plt.show()


main()

input('Введите Enter для выхода...')
