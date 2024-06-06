# 差分法求解迪利克雷边值问题
# 计算精确解
import numpy as np


def y_exact(x):
    n = len(x)
    ye = np.empty((n, 1), dtype=float)
    for i in range(n):
        ye[i] = np.sin(x[i])
    return ye


# 计算数值解
def chafen(f, x, h, y0, yn, args=()):
    #     定义系数矩阵

    n = len(x)
    y = np.empty((n, 1), dtype=float)
    y[0] = y0
    y[n - 1] = yn
    A = np.zeros((n - 2, n - 2), dtype=float)
    for i in range(n - 2):
        A[i, i] = -2 + h ** 2 * (-(x[i + 1] - 1 / 2) ** 2)
    for i in range(n - 3):
        A[i, i + 1] = 1
        A[i + 1, i] = 1
    F = np.zeros((n - 2, 1), dtype=float)
    F[0, 0] = h ** 2 * f(x[1]) - y0
    F[n - 3, 0] = h ** 2 * f(x[n - 2]) - yn
    for i in range(1, n - 3):
        F[i, 0] = h ** 2 * f(x[i + 1])
    y[1:n - 1] = np.dot(np.linalg.inv(A), F)
    return y


# 计算误差
def err(h):
    x = np.linspace(0, np.pi / 2, num=int(np.pi / 2 / h + 1))
    y = chafen(lambda x: -(x ** 2 - x + 5 / 4) * np.sin(x), x, h, 0, 1)
    ye = y_exact(x)
    # 计算误差
    # err=np.empty((len(x), 1), dtype=float)
    err = np.abs(y - ye)
    return err


# 计算收敛阶
dh = [np.pi / 8, np.pi / 16, np.pi / 32, np.pi / 64, np.pi / 128]
m = len(dh)
e = []
for i in range(m):
    error = max(err(dh[i]))
    e.append(error)
for i in range(m - 1):
    rate = np.log2(e[i] / e[i + 1])
    print(rate)