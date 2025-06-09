"""
This file contains extra decorators used in the project
"""

import functools
import time


def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        duration = end - start
        print(f"Function {func.__name__} took {duration:.4f} seconds to execute")
        return result

    return wrapper
