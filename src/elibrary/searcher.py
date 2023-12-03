from time import sleep

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from elibrary.driver import get_driver
from elibrary.exceptions import CaptchaError, ELibraryProblem
from logger import logger
from .parsers.list_articles_parser import ListArticlesParser


class ELibrarySearcher:
    URL = "https://www.elibrary.ru/"

    def __init__(self, text: str, page: int = 1, *, log_extra: dict):
        self.log_extra = log_extra
        self.driver = get_driver()
        self.driver.get("https://www.elibrary.ru/")

        self._raise_problem()

        self.driver.find_element(By.ID, 'ftext').send_keys(text)
        logger.info(f"input text: {text}", extra=self.log_extra)
        self.driver.find_elements(By.CLASS_NAME, "butblue")[0].click()
        self._go_to_page(page)
        sleep(1)

    def count_articles(self) -> int:
        couns = self.driver.find_element(
            By.CSS_SELECTOR,
            "#thepage > table > tbody > tr > td > table > tbody > tr > td:nth-child(2) > "
            "table > tbody > tr:nth-child(2) > td > b > font:nth-child(2)")
        logger.info(f"count articles: {couns.text}", extra=self.log_extra)
        return int(couns.text)

    def articles(self):
        table = self.driver.find_element(By.CSS_SELECTOR, "#restab > tbody")
        return ListArticlesParser(table, log_extra=self.log_extra).articles

    def _go_to_page(self, page: int) -> None:
        logger.info(f"start go to page: {page}", extra=self.log_extra)
        if page == 1:
            return

        for _ in range(page - 1):
            self._raise_problem()

            menu = self.driver.find_element(By.CLASS_NAME, "menus")
            if str(page) in menu.text:
                break
            elements = menu.find_elements(By.TAG_NAME, "a")
            logger.info(f"go to page: {elements[-3].text}", extra=self.log_extra)
            elements[-3].click()  # последняя страница в меню

        self.driver.find_element(By.CLASS_NAME, "menus").find_element(By.LINK_TEXT, str(page)).click()
        self._raise_problem()

    def _raise_problem(self):
        if "HTTP/1.1 500 Server Error" in self.driver.page_source:
            raise ELibraryProblem()
        if self._check_captcha():
            raise CaptchaError()

    def _check_captcha(self) -> bool:
        try:
            self.driver.find_element(By.CLASS_NAME, "g-recaptcha")
            logger.info("Captcha detected", extra=self.log_extra)
            return True
        except NoSuchElementException:
            return False
