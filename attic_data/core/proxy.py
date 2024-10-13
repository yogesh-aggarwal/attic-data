import itertools
import random

import requests

from .logging import logger
from .utils import prepare_headers


class ProxyProviders:
    @staticmethod
    def fetch_from_proxylist_geonode() -> list[str]:
        url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc"
        all_proxies = requests.get(url, headers=prepare_headers()).json()["data"]

        parsed_proxies = filter(lambda x: "http" in x["protocols"], all_proxies)
        parsed_proxies = list(
            map(lambda x: f"http://{x['ip']}:{x['port']}", parsed_proxies)
        )

        return list(set(parsed_proxies))

    @staticmethod
    def fetch_from_proxy_list() -> list[str]:
        url = "https://www.proxy-list.download/api/v1/get?type=http"
        all_proxies = requests.get(url, headers=prepare_headers()).text.split("\r\n")

        parsed_proxies = list(filter(None, all_proxies))

        return list(set(parsed_proxies))

    @staticmethod
    def fetch_proxy_list_from_random_provider() -> list[str]:
        logger.info("🐎 Fetching & caching proxies")

        providers = [
            ProxyProviders.fetch_from_proxylist_geonode,
            ProxyProviders.fetch_from_proxy_list,
        ]

        tries = 5
        while tries:
            tries -= 1
            try:
                proxies = random.choice(providers)()
                if proxies and len(proxies) > 5:
                    logger.info(f"🐑 Fetched {len(proxies)} proxies")
                    return proxies
            except Exception:
                pass

        raise Exception("Failed to fetch proxy list from any provider")


proxies = ProxyProviders.fetch_proxy_list_from_random_provider()
proxies_iter = itertools.cycle(proxies)


def get_proxy_ip():
    if not proxies or not proxies_iter:
        return None

    while True:
        yield next(proxies_iter)
