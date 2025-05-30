from abc import ABC, abstractmethod


class BaseScraper(ABC):

    @abstractmethod
    def scrape(self, keyword: str):
        pass
