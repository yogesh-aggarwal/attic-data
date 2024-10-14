import requests

from attic_data.core.constants import PROXY_RETRY_LIMIT

from .logging import logger
from .proxy import get_proxy_ip
from .utils import prepare_headers

    
def make_get_request_with_proxy(
    url: str, n_tries: int = PROXY_RETRY_LIMIT
) -> requests.Response | None:
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
