import random


def new_id():
    """
    Generate a GLXCurses ID like 'E59E8457', two chars by two chars it's a random HEX

    **Default size:** 8
    **Default chars:** 'ABCDEF0123456789'

    **Benchmark**
       +----------------+---------------+----------------------------------------------+
       | **Iteration**  | **Duration**  | **CPU Information**                          |
       +----------------+---------------+----------------------------------------------+
       | 10000000       | 99.114s       | Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz    |
       +----------------+---------------+----------------------------------------------+
       | 1000000        | 9.920s        | Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz    |
       +----------------+---------------+----------------------------------------------+
       | 100000         | 0.998s        | Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz    |
       +----------------+---------------+----------------------------------------------+
       | 10000          | 0.108s        | Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz    |
       +----------------+---------------+----------------------------------------------+

    :return: a string it represent a unique ID
    :rtype: str
    """
    return "%02x%02x%02x%02x".upper() % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )
