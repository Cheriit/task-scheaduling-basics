import time


def timer(timed_func):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = timed_func(*args, **kwargs)
        end_time = time.time()
        print(f'{timed_func.__name__} \t {args} \t {kwargs} \t {end_time - start_time}')
        return result
    return timed

