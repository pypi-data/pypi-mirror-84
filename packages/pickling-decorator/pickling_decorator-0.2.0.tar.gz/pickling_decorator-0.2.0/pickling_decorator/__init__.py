"""pickling_decorator - pickle inputs and outputs of a function."""

__version__ = "0.1.0"
__author__ = "fx-kirin <fx.kirin@gmail.com>"
__all__ = []

import datetime
import functools
import inspect
import logging
import pickle
import random
import string
import types
from pathlib import Path

import kanilog

logger = kanilog.get_module_logger(__file__, 1)


def pickling(save_input=True, save_output=True, save_directory="/tmp/pickling_decorator"):
    def decorator(func, save_input=save_input, save_output=save_output, save_directory=save_directory):
        today = datetime.date.today()
        today = str(today)
        save_directory = Path(save_directory)
        rand_str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        save_directory = save_directory / today / rand_str
        if isinstance(func, classmethod):
            logger.info(f"[{func.__func__.__qualname__}]Pickling data will be saved to {save_directory}")

            @functools.wraps(func)
            def pickled_func(cls, *args, **kwargs):
                now = datetime.datetime.now()
                nowstr = now.strftime('%Y-%m-%d_%H-%M-%S.%f')
                if save_input:
                    input_path = save_directory / f"input-{func.__qualname__}-{nowstr}.pickle"
                    input_path.write_bytes(pickle.dumps((args, kwargs)))
                    logger.debug(f"Wrote input {input_path}")
                result = func(cls, *args, **kwargs)
                if save_output:
                    output_path = save_directory / f"output-{func.__qualname__}-{nowstr}.pickle"
                    output_path.write_bytes(pickle.dumps(result))
                    logger.debug(f"Wrote output {output_path}")
                return result
        else:
            logger.info(f"[{func.__qualname__}]Pickling data will be saved to {save_directory}")
            save_directory.mkdir(exist_ok=True, parents=True)

            @functools.wraps(func)
            def pickled_func(*args, **kwargs):
                now = datetime.datetime.now()
                nowstr = now.strftime('%Y-%m-%d_%H-%M-%S.%f')
                if len(args) > 0:
                    if getattr(args[0], func.__name__, False):
                        if save_input:
                            input_path = save_directory / f"input-{func.__qualname__}-{nowstr}.pickle"
                            input_path.write_bytes(pickle.dumps((args[1:], kwargs)))
                            logger.debug(f"Wrote input {input_path}")
                        result = func(*args, **kwargs)
                        if save_output:
                            output_path = save_directory / f"output-{func.__qualname__}-{nowstr}.pickle"
                            output_path.write_bytes(pickle.dumps(result))
                            logger.debug(f"Wrote output {output_path}")
                        return result

                if save_input:
                    input_path = save_directory / f"input-{func.__qualname__}-{nowstr}.pickle"
                    input_path.write_bytes(pickle.dumps((args[1:], kwargs)))
                    logger.debug(f"Wrote input {input_path}")
                result = func(*args, **kwargs)
                if save_output:
                    output_path = save_directory / f"output-{func.__qualname__}-{nowstr}.pickle"
                    output_path.write_bytes(pickle.dumps(result))
                    logger.debug(f"Wrote output {output_path}")
                return result
        return pickled_func
    return decorator
