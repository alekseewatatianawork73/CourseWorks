from math import *
import prettytable as prt
import numpy as np


# двумерная степенная функция
def f_power(x):
    return 5 * x[0]**2 - 4 * x[0] * x[1] + 5 * x[1]**2 - x[0] - x[1]

def df_power1(x):
    return 10 * x[0] - 4 * x[1] - 1

def df_power2(x):
    return -4 * x[0] + 10 * x[1] - 1

# двумерная тригонометрическо-степенная функция
def f_trig_pow(x):
    return 2 * x[0]**2 + 3 * x[1]**2 - 2 * np.sin((x[0] - x[1]) / 2) + x[1]

def df_trig_pow1(x):
    return 4 * x[0] - np.cos((x[0] - x[1]) / 2)

def df_trig_pow2(x):
    return 6 * x[1] + np.cos((x[0] - x[1]) / 2) + 1

# двумерная смешанная функция
def f_mix(x):
    return np.log(1 + 3 * x[0]**2 + 5 * x[1]**2 + np.cos(x[0] - x[1]))

def df_mix1(x):
    return (1 + 3 * x[0]**2 + 5 * x[1]**2 + np.cos(x[0] - x[1]))**(-1) * (6 * x[0] - np.sin(x[0] - x[1]))

def df_mix2(x):
    return (1 + 3 * x[0] ** 2 + 5 * x[1] ** 2 + np.cos(x[0] - x[1])) ** (-1) * (10 * x[1] + np.sin(x[0] - x[1]))


# одномерные функции
def f_trig(x):
    return x * sin(x) + 2 * cos(x)

def f_log(x):
    return x**2 + 3 * x * (log(x) - 1)

def f_pow(x):
    return x**5 - 5 * x**3 + 10 * x**2 - 5 * x


# ввод требуемой точности
def correction():
    while True:
        try:
            eps = float(input('\nВведите точность вычислений: '))
            if 10**(-16) < eps < 1:
                break
            elif eps < 10**(-16):
                print('С заданной точностью задачу решить невозможно!')
            else:
                print('Вы ввели некорректный ответ!')
                print('Требуется ввести вещественное число от 0 до 1.')
        except ValueError:
            print('Вы ввели некорректный ответ!')
            print('Пожалуйста, введите вещественное число.')
    return int(abs(log10(eps))) + 1, eps


# Меню для пользователя
def root_menu():
    print('\nВыберите метод минимизации функции:')
    print('1. Метод половинного деления')
    print('2. Комбинированный метод Брента')
    print('3. Метод наискорейшего спуска\n')
    while True:
        try:
            m = int(input('Введите номер метода >> '))
            if 0 < m < 4:
                break
            else:
                print('Вы ввели некорректный ответ!')
                print('Требуется ввести целое число от 1 до 3.')
        except ValueError:
            print('Вы ввели некорректный ответ!')
            print('Пожалуйста, введите целое число.')
    return m


def f1_menu():
    F = [f_pow, f_trig, f_log]
    print('Выберите одномерную функцию для минимизации:')
    print('1. Степенная функция')
    print('2. Тригонометрическая функция')
    print('3. Логарифмическая функция\n')
    while True:
        try:
            f = int(input('Введите номер функции >> '))
            if 0 < f < 4:
                break
            else:
                print('Вы ввели некорректный ответ!')
                print('Требуется ввести целое число от 1 до 3.')
        except ValueError:
            print('Вы ввели некорректный ответ!')
            print('Пожалуйста, введите целое число.')
    return F[f - 1]


def f2_menu():
    F = [(f_power, df_power1, df_power2), (f_trig_pow, df_trig_pow1, df_trig_pow2), (f_mix, df_mix1, df_mix2)]
    print('Выберите двумерную функцию для минимизации:')
    print('1. Степенная функция')
    print('2. Тригонометрическо-степенная функция')
    print('3. Смешанная (триг/лог/степ) функция\n')
    while True:
        try:
            f = int(input('Введите номер функции >> '))
            if 0 < f < 4:
                break
            else:
                print('Вы ввели некорректный ответ!')
                print('Требуется ввести целое число от 1 до 3.')
        except ValueError:
            print('Вы ввели некорректный ответ!')
            print('Пожалуйста, введите целое число.')
    return F[f - 1]


# Ввод с клавиатуры начального интервала
def segment(f):
    while True:
        try:
            a = float(input("\nВведите начало интервала поиска a = "))
            b = float(input("Введите конец интервала поиска b = "))
            if f == f_log and (a <= 0 or b <= 0):
                print('Ошибка: Логарифм неположительного числа! Введите числа больше нуля.')
            elif abs(b - a) < 50:
                break
            else:
                print(
                    "Слишком широкий интервал!"
                    "Введите заново границы отрезка."
                )
        except ValueError:
            print(
                "Ошибка: Некорректный ввод границ интервала."
                "Пожалуйста, введите число."
            )
    return a, b


# Ввод с клавиатуры начального приближения
def start():
    while True:
        try:
            x1 = float(input("\nВведите начальное приближение x1 = "))
            x2 = float(input("Введите начальное приближение x2 = "))
            break
        except ValueError:
            print(
                "Ошибка: Некорректный ввод начального приближения."
                "Пожалуйста, введите число."
            )
    return x1, x2


def continue_working():
    while True:
        try:
            ans = input('\nХотите ещё раз воспользоваться методами оптимизации? Введите "да" для продолжения работы программы. Для завершения работы нажмите Enter >> ').lower()
            if ans != 'да' and ans != '':
                raise ValueError('\nВы ввели некорректный ответ! Введите "да" или нажмите Enter.')
            if ans == '':
                print('\nРабота программы завершена. Благодарим за использование!')
                break
            elif ans == 'да':
                break
        except ValueError as d:
            print(d)
    return ans



# метод половинного деления
def dichotomy_method(f, a, b):
    d = eps / 2
    n = 0
    dx = 10.0
    tab = prt.PrettyTable()
    tab.title = 'Метод половинного деления'
    tab.field_names = ['n', 'an', 'bn', 'eps', 'x1', 'x2', 'f(x1)', 'f(x2)']
    while dx > eps:
        dx = (b - a) / 2
        x1 = (a + b) / 2 - d
        x2 = (a + b) / 2 + d
        tab.add_row([n, round(a, count_sign), round(b, count_sign),
                     round(dx, count_sign), round(x1, count_sign), round(x2, count_sign),
                     round(f(x1), count_sign), round(f(x2), count_sign)])
        if f(x1) > f(x2):
            a = x1
        else:
            b = x2
        n += 1
    x_min = (a + b) / 2
    print(tab)
    return x_min, f(x_min)


# комбинированный метод Брента
def brent_method(f, a, b):
    gold = (3 - 5 ** 0.5) / 2  # коэффициент из метода золотого сечения
    x = w = v = a + gold * (b - a)  # три наилучших приближения к точке минимума
    cur = prv = b - a  # вспомогательные величины

    tab = prt.PrettyTable()
    tab.title = 'Комбинированный метод Брента'
    tab.field_names = ['n', 'an', 'bn', 'un', 'xn', 'f(un)', 'f(xn)', 'eps']
    n = 0
    tab.add_row([n, round(a, count_sign), round(b, count_sign), "-", round(x, count_sign), "-", round(f(x), count_sign), round(cur, count_sign)])

    while cur > eps:
        if max(x - a, b - x) < eps:
            break

        g, prv = prv / 2, cur  # то есть prv - это предыдущее значение cur, а cur = |u - x| - погрешность

        # находим вершину параболы, построенной по точкам x, w, v
        div = (2 * ((w - x) * (f(w) - f(v)) - (w - v) * (f(w) - f(x))))
        if div == 0:
            u = None
        else:
            u = w - ((w - x)**2 * (f(w) - f(v)) - (w - v)**2 * (f(w) - f(x))) / div

        if u == None or (not (a <= u <= b)) or abs(u - x) > g:
            # проверяем, слева или справа от отрезка находится точка u и преносим её внутрь отрезка
            if x < (a + b) / 2:
                u = x + gold * (b - x)
                prv = b - x
            else:
                u = x - gold * (x - a)
                prv = x - a

        cur = abs(u - x)
        if f(u) > f(x):
            # изменяем границы отрезка, включающего точку минимума x
            if u < x:
                a = u
            else:
                b = u
            # изменяем тройку удачных точек
            if f(u) <= f(w) or w == x:
                v = w
                w = u
            elif f(u) <= f(v) or v == x or v == w:
                v = u
        else:
            # изменяем границы отрезка, включающего точку минимума u
            if u < x:
                b = x
            else:
                a = x
            # изменяем тройку удачных точек
            v = w
            w = x
            x = u
        n += 1
        tab.add_row([n, round(a, count_sign), round(b, count_sign), round(u, count_sign), round(x, count_sign), round(f(u), count_sign), round(f(x), count_sign), round(cur, count_sign)])

    print(tab)
    return x, f(x)


# метод наискорейшего спуска
def steepest_descent(f, df1, df2, x1, x2):
    x = np.array([x1, x2])
    dx = 10.0
    k = 0
    tab = prt.PrettyTable()
    tab.title = 'Метод наискорейшего спуска'
    tab.field_names = ["k", "x1", "x2", "f(x1, x2)", "alpha", "max(|df(x1, x2)|)"]
    tab.add_row([k, round(x[0], count_sign), round(x[1], count_sign), round(f(x), count_sign), 0.5, "-"])

    while dx > eps:
        grad = np.array([df1(x), df2(x)])
        alpha = 0.5
        while f(x - alpha * grad) >= f(x):
            alpha /= 2
        x -= alpha * grad
        dx = max(abs(grad))
        k += 1
        tab.add_row([k, round(x[0], count_sign), round(x[1], count_sign), round(f(x), count_sign), round(alpha, count_sign), round(dx, count_sign)])

    print(tab)
    return x, f(x)


print('Методы одномерной и многомерной оптимизации')

while True:
    method = root_menu()
    count_sign, eps = correction()

    if method == 3:
        f, df1, df2 = f2_menu()
        x1, x2 = start()
        x_min, f_min = steepest_descent(f, df1, df2, x1, x2)
        print(f'x_min = ({round(x_min[0], count_sign - 1)}, {round(x_min[1], count_sign - 1)})   f(x_min) = {round(f_min, count_sign - 1)}')

    else:
        f = f1_menu()
        a, b = segment(f)
        x_min, f_min = dichotomy_method(f, a, b) if method == 1 else brent_method(f, a, b)
        print(f'x_min = {round(x_min, count_sign - 1)},   f(x_min) = {round(f_min, count_sign - 1)}')

    ans = continue_working()
    if ans == '':
        break

input('\nНажмите Enter для выхода из программы...')
