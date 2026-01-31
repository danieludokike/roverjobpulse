
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, source_name):
        self.source_name = source_name

    @abstractmethod
    def fetch_jobs(self):
        """Return a list of job dictionaries"""
        pass
