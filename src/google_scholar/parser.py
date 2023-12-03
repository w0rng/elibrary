from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from logger import logger
from .schemas import Article


class GoogleParser:
    def __init__(self, page: WebElement, *, log_extra: dict):
        self.page = page
        self.log_extra = log_extra

    @property
    def articles(self) -> list[Article]:
        rows = self.page.find_elements(By.CLASS_NAME, "gs_ri")
        result = []
        for row in rows:
            try:
                result.append(Article(
                    title=row.find_element(By.CLASS_NAME, "gs_rt").find_element(By.TAG_NAME, "a").text,
                    url=row.find_element(By.CLASS_NAME, "gs_rt").find_element(By.TAG_NAME, "a").get_attribute("href"),
                    authors=self._parse_authors(row),
                    date=0
                ))
            except NoSuchElementException:
                logger.info(f"skip row {row.text}", extra=self.log_extra)
                continue
        return result

    @staticmethod
    def _parse_authors(row: WebElement) -> list[str]:
        raw_authors = row.find_element(By.CLASS_NAME, "gs_a").text
        raw_authors = raw_authors.replace("…", "")
        raw_authors = raw_authors.split('-')[0]
        raw_authors = raw_authors.split(",")
        authors = list(filter(str, map(str.strip, raw_authors)))

        def normalize(author: str) -> str:
            io, family = author.split(" ")
            if len(io) != 2:
                return author
            return f"{family} {io[0]}.{io[1]}."

        return list(map(normalize, authors))
