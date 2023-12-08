import random
from urllib.request import urlopen, Request

from selenium.webdriver import Chrome, ChromeOptions, Proxy
from selenium.webdriver.common.proxy import ProxyType


def options(proxy: str = None) -> ChromeOptions:
    opt = ChromeOptions()
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument('--headless')
    opt.add_argument('--start-maximized')

    if proxy:
        opt.proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': proxy,
            'ftpProxy': proxy,
            'sslProxy': proxy,
            'noProxy': ''})
    return opt


def get_driver(use_proxy: bool = False) -> Chrome:
    if not use_proxy:
        options_ = options()
    else:
        request = Request("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
        with urlopen(request) as response:
            proxys = response.read().decode("utf-8")
        proxys = list(filter(str.strip, proxys.split("\r\n")))
        options_ = options(random.choice(proxys))
    return Chrome(options=options_)
