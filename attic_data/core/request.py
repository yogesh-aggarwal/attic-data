import requests

from .logging import logger
from .utils import prepare_headers
from .proxy import get_proxy_ip


def make_get_request_with_proxy(url: str, n_tries: int = 3) -> requests.Response | None:
    for _ in range(n_tries):
        try:
            proxy = next(get_proxy_ip())
            logger.info(f"🔌 Using proxy: {proxy}")
            res = requests.get(url, headers=prepare_headers(), proxies={"http": proxy})
            res.raise_for_status()

            return res
        except Exception as e:
            logger.error(f"🚫 Proxy failed: {proxy}, {n_tries - _ - 1} tries remaining")
            logger.error(e)

    return None
