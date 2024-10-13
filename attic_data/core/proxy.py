import itertools
import random

import requests

from .logging import logger
from .utils import prepare_headers


class ProxyProviders:
    @staticmethod
    def fetch_from_proxylist_geonode() -> list[str]:
        final_proxies = []
        for i in range(1, 6):
            url = f"https://proxylist.geonode.com/api/proxy-list?protocols=http&limit=500&page={i}&sort_by=lastChecked&sort_type=desc"
            all_proxies = requests.get(url, headers=prepare_headers()).json()["data"]
            if not all_proxies:
                break

            parsed_proxies = list(
                map(lambda x: f"http://{x['ip']}:{x['port']}", all_proxies)
            )

            final_proxies.extend(parsed_proxies)

        return list(set(final_proxies))

    @staticmethod
    def fetch_from_proxy_list() -> list[str]:
        url = "https://www.proxy-list.download/api/v1/get?type=http"
        all_proxies = requests.get(url, headers=prepare_headers()).text.split("\r\n")

        parsed_proxies = list(filter(None, all_proxies))

        return list(set(parsed_proxies))

    @staticmethod
    def fetch_from_all_providers() -> list[str]:
        logger.info("🐎 Fetching & caching proxies")

        providers = [
            ProxyProviders.fetch_from_proxylist_geonode,
            ProxyProviders.fetch_from_proxy_list,
        ]

        final_proxies: list[str] = []
        for provider in providers:
            try:
                for _ in range(5):
                    proxies = provider()
                    if proxies and len(proxies) > 5:
                        final_proxies.extend(proxies)
                        break
            except Exception:
                pass

        if len(final_proxies) < 5:
            raise Exception("Failed to fetch proxies from all providers")

        logger.info(f"🐑 Fetched {len(proxies)} proxies")

        return final_proxies


proxies = ProxyProviders.fetch_from_all_providers()
proxies_iter = itertools.cycle(proxies)


def get_proxy_ip():
    if not proxies or not proxies_iter:
        return None

    while True:
        yield next(proxies_iter)
