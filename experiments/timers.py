import time
import functools

def print_time(time: float, message: str):
    if time > 1:
        print(f"{message}{time:.2f}s")
    elif time > 0.001:
        time_ms = time * 1000
        print(f"{message}{time_ms:.2f}ms")
    else:
        time_ns = time * 1000000
        print(f"{message}{time_ns:.2f}ns")

def simple_timer(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        print_time(elapsed, "Time elapsed: ")
        return result
    return wrapper

def repeat_timer(iterations: int = 10, print_each: bool = False):
    def actual_decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            total_time = 0
            for i in range(iterations):
                start_time = time.perf_counter()
                result = fn(*args, **kwargs)
                elapsed = time.perf_counter() - start_time
                total_time += elapsed
                if print_each:
                    print_time(elapsed, "Time elapsed: ")
            average_time = total_time / iterations
            print_time(average_time, "Average time: ")
            return result
        return wrapper
    return actual_decorator