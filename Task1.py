from typing import Callable


# 6*x**2 + 0.5*x*y + 2*y**2
def function_maker_2(str_f: str) -> Callable:
    def f(x: float, y: float) -> float:
        s = str_f.replace("x", "(" + str(x) + ")").replace("^", "**").replace("y", "(" + str(y) + ")")
        return eval(s)
    return f


def derivative(x: float, y: float) -> tuple[float, float]:
    return 12*x + 0.5*y, 0.5*x + 4*y


def norma(x: list | tuple) -> float:
    ans = 0
    for elem in x:
        ans += elem**2
    return ans ** 0.5


def gradient_method():
    f = function_maker_2(input("Введите функцию: F(x, y) = "))
    x = tuple(map(float, input('Введите начальный вектор x (Числа через пробел): ').split()))
    t = float(input('Введите шаг: '))
    e1 = float(input('Введите e1: '))
    e2 = float(input('Введите e2: '))
    M = int(input('Введите максимальное число итераций: '))
    k = 0
    fl = False
    while True:
        if norma(derivative(*x)) < e1:
            break
        if k >= M:
            break
        new_x = x[0] - t * derivative(*x)[0], x[1] - t * derivative(*x)[1]
        while f(*new_x) - f(*x) >= 0:
            t /= 2
            new_x = x[0] - t * derivative(*x)[0], x[1] - t * derivative(*x)[1]
        if norma((new_x[0] - x[0], new_x[1] - x[1])) < e2 and abs(f(*new_x) - f(*x)) < e2:
            if fl:
                x = new_x
                break
            else:
                fl = True
        else:
            fl = False
        x = new_x
        k += 1
    print(f"x = {x}")
    print(f"f(x) = {f(*x)}")
    print("Число итераций:", k+1)


if __name__ == '__main__':
    gradient_method()