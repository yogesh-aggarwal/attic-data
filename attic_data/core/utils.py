import os
import requests

from fake_useragent import UserAgent


def cd(path: str):
    try:
        os.makedirs(path, exist_ok=True)
    except:
        pass
    os.chdir(path)


def prepare_headers():
    ua = UserAgent()

    headers = requests.utils.default_headers()
    headers.update({"User-Agent": ua.firefox})

    return headers
