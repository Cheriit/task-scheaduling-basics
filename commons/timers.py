import time


def timer(timed_func):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = timed_func(*args, **kwargs)
        end_time = time.time()
        print(f'{timed_func.__name__} \t {(end_time - start_time)*1000}')
        return result
    return timed

