import sys
import time

time_out = open('data/time_py.txt', 'w')
mem_out = open('data/mem_py.txt', 'w')


def current_milli_time():
    return time.time() * 1000


def test_map(n: int):
    tested_map = {}

    t1 = current_milli_time()

    for i in range(n):
        tested_map[i] = i

    t2 = current_milli_time()

    elapsed = t2 - t1

    time_out.write(f'{n} {elapsed}\n')

    memory = sys.getsizeof(tested_map)

    mem_out.write(f'{n} {memory}\n')


for i in range(0, 8):
    n = pow(10, i)
    test_map(n)

