import contextlib
import os
import time
from typing import Callable

import nanoid
import requests
from fake_useragent import UserAgent

from attic_data.core.logging import logger


def generate_id() -> str:
    return nanoid.generate()


def get_timestamp() -> int:
    return int(time.time()) * 1000


def with_retry(tries: int):
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            for _ in range(tries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(e)
                    pass

            raise Exception("Failed to execute")

        return wrapper

    return decorator


@contextlib.contextmanager
def cd(path: str):
    try:
        os.makedirs(path, exist_ok=True)
        os.chdir(path)
        yield
    finally:
        if path != ".":
            os.chdir("..")


@contextlib.contextmanager
def logged_try_except(name: str = "default"):
    try:
        yield
    except Exception as e:
        logger.getChild(name).error(f"Error: {e}")


def prepare_headers():
    ua = UserAgent()

    headers = requests.utils.default_headers()
    headers.update({"User-Agent": ua.firefox})

    return headers
