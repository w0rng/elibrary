from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def options() -> Options:
    opt = Options()
    opt.add_argument('--no-sandbox')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--disable-dev-shm-usage')
    opt.add_argument('--headless')
    opt.add_argument('--start-maximized')

    return opt


def get_driver() -> Chrome:
    return Chrome(options=options())
