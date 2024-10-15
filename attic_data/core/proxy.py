import itertools
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

import requests

from .logging import logger
from .utils import prepare_headers, with_retry

from attic_data.core.constants import USE_PROXY


class ProxyProviders:
    @staticmethod
    @with_retry(3)
    def fetch_from_proxylist_geonode() -> list[str]:
        final_proxies = []
        for i in range(1, 6):
            url = f"https://proxylist.geonode.com/api/proxy-list?protocols=http&limit=500&page={i}&sort_by=lastChecked&sort_type=desc"
            all_proxies = requests.get(url, headers=prepare_headers()).json()["data"]
            if not all_proxies:
                break

            parsed_proxies = map(lambda x: f"http://{x['ip']}:{x['port']}", all_proxies)

            final_proxies.extend(parsed_proxies)

        return list(set(final_proxies))

    @staticmethod
    @with_retry(3)
    def fetch_from_proxylist() -> list[str]:
        url = "https://www.proxy-list.download/api/v1/get?type=http"
        all_proxies = requests.get(url, headers=prepare_headers()).text.split("\r\n")

        parsed_proxies = filter(None, all_proxies)

        return list(set(parsed_proxies))

    @staticmethod
    @with_retry(3)
    def fetch_from_proxyscrape() -> list[str]:
        url = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&protocol=http&proxy_format=protocolipport&format=text&timeout=20000"
        all_proxies = requests.get(url, headers=prepare_headers()).text.split("\r\n")

        parsed_proxies = filter(None, all_proxies)

        return list(set(parsed_proxies))

    @staticmethod
    @with_retry(3)
    def fetch_from_thespeedx_github() -> list[str]:
        url = "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
        all_proxies = requests.get(url, headers=prepare_headers()).text.split("\n")

        parsed_proxies = list(filter(None, all_proxies))
        parsed_proxies = map(lambda x: x.strip(), parsed_proxies)

        return list(set(parsed_proxies))

    @staticmethod
    @with_retry(3)
    def fetch_from_all_providers() -> list[str]:
        logger.info("🐎 Fetching & caching proxies")

        providers = [
            ProxyProviders.fetch_from_proxylist_geonode,
            ProxyProviders.fetch_from_proxylist,
            ProxyProviders.fetch_from_proxyscrape,
            # ProxyProviders.fetch_from_thespeedx_github,
        ]

        final_proxies: list[str] = []

        def fetch_provider(provider: Callable[[], list[str]]):
            try:
                proxies = provider()
                if len(proxies) < 5:
                    raise Exception("Failed to fetch proxies from provider")
                final_proxies.extend(proxies)
            except Exception:
                pass

        with ThreadPoolExecutor() as executor:
            for provider in providers:
                executor.submit(fetch_provider, provider)

        if len(final_proxies) < 5:
            raise Exception("Failed to fetch proxies from all providers")

        logger.info(f"🐑 Fetched {len(final_proxies)} proxies")

        return final_proxies


proxies = ProxyProviders.fetch_from_all_providers() if USE_PROXY else []
proxies_iter = itertools.cycle(proxies)


def get_proxy_ip():
    while True:
        yield next(proxies_iter) if USE_PROXY else None
