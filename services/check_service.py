from abc import ABC, abstractmethod

from classes import Singleton


class CheckService(ABC):
    @abstractmethod
    def check(self, *args, **kwargs):
        pass