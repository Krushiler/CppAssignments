import sys

import matplotlib.pyplot as plt
import numpy as np


def get_data(filename):
    data = [[], []]
    file = open(filename, 'r')
    while line := file.readline().rstrip():
        if line.strip() == '':
            break

        (n, el) = line.split(' ')
        n = int(n)
        el = float(el)

        data[0].append(n)
        data[1].append(el)

    return data


def plot(data_cpp, data_py, name):
    plt.plot(np.log10(data_cpp[0]), data_cpp[1], label='C++')
    plt.plot(np.log10(data_py[0]), data_py[1], label='Python')

    plt.title(name)
    plt.legend()

    plt.xlabel('10^x map elements')
    plt.ylabel(name)

    plt.show()


if __name__ == '__main__':
    data_cpp_name = sys.argv[1]
    data_py_name = sys.argv[2]
    name = sys.argv[3]

    print(data_cpp_name)

    data_cpp = get_data(data_cpp_name)
    data_py = get_data(data_py_name)
    plot(data_cpp, data_py, name)
