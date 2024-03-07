from abc import ABC, abstractmethod


class IOutputDNBScore(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
