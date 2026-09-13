import time
from functools import wraps
from contextlib import contextmanager

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()

        elapsed_time = end_time - start_time

        print(f"{func.__name__} took {elapsed_time:.2f} seconds")

        return result

    return wrapper

@contextmanager
def step(label):
    print(f"Starting: {label}")

    yield

    print(f"Finished: {label}")