import time
from time import sleep

from selenium.webdriver.common.by import By

from elibrary.driver import get_driver
from elibrary.exceptions import CaptchaError
from logger import logger
from .parser import GoogleParser


class GoogleSearcher:
    URL = "https://scholar.google.com/"

    def __init__(self, text: str, page: int = 1, *, log_extra: dict):
        self.log_extra = log_extra
        self.driver = get_driver()
        self.driver.get(self.URL)

        self.driver.find_element(By.ID, 'gs_hdr_tsi').send_keys(text)
        logger.info(f"input text: {text}", extra=self.log_extra)
        self.driver.find_element(By.ID, "gs_hdr_tsb").click()
        self._go_to_page(page)
        self._check_capcha()

    def count_articles(self) -> int:
        raw_count = self.driver.find_element(By.XPATH, '//*[@id="gs_ab_md"]/div')
        raw_count = raw_count.text.split('(')[0].split('примерно ')[-1].strip()
        raw_count = raw_count.replace(' ', '')
        raw_count = raw_count.split(',')[0]
        raw_count = raw_count.split(':')[-1]
        count = int(raw_count)
        logger.info(f"count articles: {count}", extra=self.log_extra)
        return count

    def articles(self):
        try:
            page = self.driver.find_element(By.ID, "gs_res_ccl_mid")
            return GoogleParser(page, log_extra=self.log_extra).articles
        except Exception:
            logger.warning("some error", extra=self.log_extra)
            self.driver.save_screenshot(f'/screenshots/{time.time()}.png')
            return []

    def _go_to_page(self, page: int) -> None:
        logger.info(f"go to page: {page}", extra=self.log_extra)
        url = self.driver.current_url + f"&start={10 * (page - 1)}"
        self.driver.get(url)

    def _check_capcha(self):
        if "Докажите что вы не робот" in self.driver.find_element(By.TAG_NAME, "body").text:
            raise CaptchaError()
