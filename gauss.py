import numpy as np
from math import inf
from math import gcd


def get_lcm(a, b):
    return abs((a * b) // gcd(a, b))


def add(i, j, col, mat, file, log):
    lcm = get_lcm(mat[i, col], mat[j, col])
    coef_i = abs(lcm // mat[i, col])
    coef_j = abs(lcm // mat[j, col])
    mat[j] = mat[j] * coef_j + mat[i] * coef_i
    if log:
        add_print(i, j, coef_i, coef_j, mat, file)


def add_print(i, j, coef_i, coef_j, mat, file):
    file.write("\n\n\n" + "К " + str(j + 1) + " строке")
    if abs(coef_j) != 1:
        file.write(", умноженной на " + str(coef_j) + ",")
    file.write(" прибавили " + str(i + 1) + " строку")
    if abs(coef_i) != 1:
        file.write(", умноженную на " + str(coef_i))
    file.write(":" + "\n")
    file.write(str(mat))


def subtract(i, j, col, mat, file, log):
    lcm = get_lcm(mat[i, col], mat[j, col])
    coef_i = lcm // mat[i, col]
    coef_j = lcm // mat[j, col]
    mat[j] = mat[j] * coef_j - mat[i] * coef_i
    if log:
        subtract_print(i, j, coef_i, coef_j, mat, file)


def subtract_print(i, j, coef_i, coef_j, mat, file):
    file.write("\n\n\n" + "Из " + str(j + 1) + " строки")
    if abs(coef_j) != 1:
        file.write(", умноженной на " + str(coef_j) + ",")
    file.write(" вычли " + str(i + 1) + " строку")
    if abs(coef_i) != 1:
        file.write(", умноженную на " + str(coef_i))
    file.write(":" + "\n")
    file.write(str(mat))


def simplify_row(row, start, mat, file, log):
    divisor = mat[row, start]
    if divisor == 0:
        return 0
    for i in range(start + 1, np.shape(mat)[1]):
        divisor = gcd(divisor, mat[row, i])
        if divisor == 1:
            return 0
    mat[row] = mat[row] / divisor
    if log:
        simplify_print(row, divisor, mat, file)


def simplify_print(i, divisor, mat, file):
    file.write("\n\n\n" + "Сократили " + str(i + 1) + " строку на " + str(divisor) + ":" + "\n" + str(mat))


def smallest_leading_elem(start_row, col, mat, file, log):
    cur_min = (inf, -1)
    for i in range(start_row, np.shape(mat)[0]):
        if mat[i, col] != 0 and abs(mat[i, col]) < cur_min[0]:
            cur_min = (abs(mat[i, col]), i)
    if cur_min[1] == -1:
        return 0
    min_row = cur_min[1]
    if min_row != start_row:
        mat[start_row], mat[min_row] = np.copy(mat[min_row]), np.copy(mat[start_row])
        if log:
            swap_print(start_row, min_row, mat, file)
    return cur_min[0]


def swap_print(i, j, mat, file):
    file.write("\n\n\n" + "Поменяли местами " + str(i + 1) + " и " + str(j + 1) + " строки:" + "\n")
    file.write(str(mat))


def make_positive(row, col, mat, file, log):
    if mat[row, col] < 0:
        mat[row] *= -1
        if log:
            file.write("\n\n\n" + "Умножили " + str(row + 1) + " строку на -1:" + "\n")
            file.write(str(mat))


def get_start(mat):
    i = np.size(mat, 0) - 1
    while not np.any(mat[i]):
        i -= 1

    j = 0
    while mat[i, j] == 0:
        j += 1

    return i, j


def gauss(mat, file, log):
    if log:
        file.write("Исходная матрица:" + "\n" + str(mat))
    col = 0
    row = 0

    while row + 1 != np.shape(mat)[0] and col != np.shape(mat)[1]:
        if smallest_leading_elem(row, col, mat, file, log) != 0:
            make_positive(row, col, mat, file, log)
            simplify_row(row, col, mat, file, log)
            for j in range(row + 1, np.shape(mat)[0]):
                if mat[j, col] != 0:
                    if mat[j, col] * mat[row, col] > 0:
                        subtract(row, j, col, mat, file, log)
                    else:
                        add(row, j, col, mat, file, log)
            row += 1
            col += 1
        else:
            col += 1

    make_positive(row, col, mat, file, log)
    simplify_row(row, col, mat, file, log)


def reverse_gauss(mat, file, log):
    row, col = get_start(mat)

    while row != 0 and col != 0:
        simplify_row(row, col, mat, file, log)
        for j in range(row - 1, -1, -1):
            if mat[j, col] != 0:
                if mat[j, col] * mat[row, col] > 0:
                    subtract(row, j, col, mat, file, log)
                else:
                    add(row, j, col, mat, file, log)
        row -= 1
        while col > 0 and mat[row, col - 1] != 0:
            col -= 1

    simplify_row(row, col, mat, file, log)


def full_gauss(mat, log=True, file=open("output.txt", "w", encoding="utf-8")):
    gauss(mat, file, log)
    file.write("\n\n\nОбратный ход Гаусса:")
    reverse_gauss(mat, file, log)
    file.close()
