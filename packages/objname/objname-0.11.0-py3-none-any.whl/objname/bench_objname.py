import time

import objname


def single_assignment():
    start = time.monotonic()
    for i in range(100_000):
        a = objname.AutoName()
        b = objname.AutoName()
        c = objname.AutoName()
    end = time.monotonic()
    print(f"single_assignment {end - start:0.4g} seconds")


def unpack_sequence():
    start = time.monotonic()
    for i in range(100_000):
        a, b, c = objname.AutoName()
    end = time.monotonic()
    print(f"unpack_sequence {end - start:0.4g} seconds")


if __name__ == '__main__':
    single_assignment()
    unpack_sequence()
