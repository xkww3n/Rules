import logging
from time import time_ns


def log(func):
    def wrapper(desc, *args, **kwargs):
        logging.info(f"Build {desc}")
        start_time = time_ns()
        result = func(*args, **kwargs)
        end_time = time_ns()
        logging.info(f"Done ({format((end_time - start_time) / 1e9, '.3f')}s)\n")
        return result
    return wrapper
