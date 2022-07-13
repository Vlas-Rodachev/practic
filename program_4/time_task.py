import time


def time_execution(some_function):
    time_code_one = time.perf_counter()
    a = some_function()
    time_code_two = time.perf_counter()
    return time_code_two - time_code_one
