from abc import ABC, abstractmethod


class IOutputCorrelation(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
