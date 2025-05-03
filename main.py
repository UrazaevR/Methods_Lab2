from typing import Callable, Any
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6 import QtCore
from Window import Ui_Window
import sys


def tipical_function_maker(a: float, b: float, c: float) -> Callable:
    def f(x: float, y: float) -> float:
        return a*x**2 + b*x*y + c*y**2
    return f


def derivative_maker(a: float, b: float, c: float) -> Callable:
    def f(x: float, y: float) -> tuple[float, float]:
        return 2*a*x + b*y, b*x + 2*c*y
    return f


def norma(x: list | tuple) -> float:
    ans = 0
    for elem in x:
        ans += elem**2
    return ans ** 0.5


def input_parameters():
    a, b, c = map(float, input("Введите коэффициенты a, b и c через пробел: ").split())
    x = tuple(map(float, input('Введите начальный вектор x (Числа через пробел): ').split()))
    e1 = float(input('Введите e1: '))
    e2 = float(input('Введите e2: '))
    M = int(input('Введите максимальное число итераций: '))
    return a, b, c, x, e1, e2, M


def half_division(f: callable, a: float, b: float, e: float, minimum: bool=True) -> tuple:
    k = 0

    xk = (a + b) / 2
    L = abs(b - a)

    while L > e:
        yk = a + L/4
        zk = b - L/4
        if minimum:
            if f(yk) < f(xk):
                b = xk
                xk = yk
            else:
                if f(zk) < f(xk):
                    a = xk
                    xk = zk
                else:
                    a = yk
                    b = zk
            L = abs(b - a)
            k += 1

        else:
            if f(yk) > f(xk):
                b = xk
                xk = yk
            else:
                if f(zk) > f(xk):
                    a = xk
                    xk = zk
                else:
                    a = yk
                    b = zk
            L = abs(b - a)
            k += 1
    return xk, f(xk), k


def fastest_gradient_method(a: float, b: float, c: float, x: tuple[float, float], e1: float, e2: float, M: int, t: Any=None) -> tuple[tuple[float, float], float, int]:
    f = tipical_function_maker(a, b, c)
    df = derivative_maker(a, b, c)
    k = 0
    fl = False
    while k < M:
        if norma(df(*x)) < e1:
            break

        def fi(t: float) -> float:
            x1 = x[0] - t*df(*x)[0]
            x2 = x[1] - t*df(*x)[1]
            return f(x1, x2)

        tk = half_division(fi, -1, 1, 0.001)[0]
        new_x = x[0] - tk*df(*x)[0], x[1] - tk*df(*x)[1]
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
    return x, f(*x), k+1


def gradient_method(a: float, b: float, c: float, x: tuple[float, float], e1: float, e2: float, M: int, t: float) -> tuple[tuple[float, float], float, int]:
    f = tipical_function_maker(a, b, c)
    df = derivative_maker(a, b, c)
    k = 0
    fl = False
    while True:
        if norma(df(*x)) < e1:
            break
        if k >= M:
            break
        new_x = x[0] - t * df(*x)[0], x[1] - t * df(*x)[1]
        while f(*new_x) - f(*x) >= 0:
            t /= 2
            new_x = x[0] - t * df(*x)[0], x[1] - t * df(*x)[1]
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
    return x, f(*x), k+1


class Win(QWidget, Ui_Window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.method_box.currentTextChanged.connect(self.show_hide_t)
        self.result_button.clicked.connect(self.get_result)

    def show_hide_t(self):
        if self.method_box.currentText() == 'Метод градиентного спуска':
            self.t_str.setVisible(True)
            self.label_10.setVisible(True)
        else:
            self.t_str.setVisible(False)
            self.label_10.setVisible(False)

    def get_result(self):
        try:
            if not self.a_str.text().strip():
                raise Exception('Коэффициент a не должен быть пустым')
            if not self.b_str.text().strip():
                raise Exception('Коэффициент b не должен быть пустым')
            if not self.c_str.text().strip():
                raise Exception('Коэффициент c не должен быть пустым')
            if not self.x_str.text().strip():
                raise Exception('Необходимо задать начальный вектор Х')
            if not self.e1_str.text().strip():
                raise Exception('Необходимо задать допустимую погрешность e1')
            if not self.e2_str.text().strip():
                raise Exception('Необходимо задать допустимую погрешность e2')
            if self.t_str.isVisible() and not self.t_str.text().strip():
                raise Exception('Необхоидмо задать шаг t')
            if self.t_str.isVisible() and float(self.t_str.text()) == 0:
                raise Exception('Шаг не должен быть равен 0')
            e1 = float(self.e1_str.text())
            e2 = float(self.e2_str.text())
            if e1 == 0 or e2 == 0:
                raise Exception('Погрешность не может быть равна нулю')
            # minimum = self.minimum_box.currentText() == 'Минимум'
            if self.method_box.currentText() == 'Метод градиентного спуска':
                method = gradient_method
            else:
                method = fastest_gradient_method
            x, fx, k = method(float(self.a_str.text()), float(self.b_str.text()), float(self.c_str.text()), tuple(map(float, self.x_str.text().split())), e1, e2, int(self.M_value.value()), float(self.t_str.text()))
            self.output.setText(f'x* = {x}\nf(x*) = {fx}\nЧисло итераций: {k}')
        except Exception as ex:
            self.output.setText(str(ex))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Win()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())