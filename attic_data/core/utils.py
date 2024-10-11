import os
import requests
import contextlib

from fake_useragent import UserAgent


@contextlib.contextmanager
def cd(path: str):
    try:
        os.makedirs(path, exist_ok=True)
        yield os.chdir(path)
    finally:
        os.chdir("..")


def prepare_headers():
    ua = UserAgent()

    headers = requests.utils.default_headers()
    headers.update({"User-Agent": ua.firefox})

    return headers
