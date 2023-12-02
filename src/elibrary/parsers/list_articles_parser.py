import re
from datetime import datetime
from functools import cached_property
from typing import Optional

from logger import logger
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from elibrary.schemas import Article


class ListArticlesParser:
    def __init__(self, page: WebElement, *, log_extra: dict):
        self.page = page
        self.log_extra = log_extra

    @cached_property
    def articles(self) -> list[Article]:
        result = []

        for row in self.page.find_elements(By.TAG_NAME, "tr"):
            if row.get_attribute("valign") != "middle":
                continue

            row = row.find_elements(By.TAG_NAME, "td")[1]

            title = self._get_title(row)
            authors = self._get_authors(row)
            url = self._get_url(row)
            date = self._get_date(row)

            if not title or not url or not date or not authors:
                logger.warning(
                    "Skip article with title: %s; url: %s; date: %s; authors: %s",
                    title,
                    url,
                    date,
                    authors,
                    extra=self.log_extra
                )
                continue

            result.append(Article(title=title, url=url, authors=authors, date=date))

        return result

    @staticmethod
    def _get_title(row: WebElement) -> Optional[str]:
        try:
            return row.find_element(By.TAG_NAME, "span").text
        except NoSuchElementException:
            return None

    @staticmethod
    def _get_authors(row: WebElement) -> Optional[list[str]]:
        author = row.find_elements(By.TAG_NAME, "i")
        if not author:
            return None
        author = author[-1].text
        return list(map(str.strip, author.split(',')))

    @staticmethod
    def _get_url(row: WebElement) -> Optional[str]:
        urls = row.find_elements(By.TAG_NAME, "a")
        if not urls:
            return None
        url = urls[0].get_attribute("href")
        if "http" in url:
            return url
        if "javascript" in url:
            id_ = url.split("(")[1].split(")")[0]
            return f"https://www.elibrary.ru/item.asp?id={id_}"
        return url

    @staticmethod
    def _get_date(row: WebElement) -> Optional[int]:
        dates = re.findall(r'\d{4}\.?', row.text)
        for date in dates:
            if '.' in date:
                date = date[:-1]
            date = int(date)
            if 1990 <= date <= datetime.now().year:
                return date
        return None
