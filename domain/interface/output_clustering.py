from abc import ABC, abstractmethod


class IOutputClustering(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError
