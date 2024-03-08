from abc import ABC, abstractmethod


class IOutputHeatmap(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    def run(self, features: list[str], pvals: list[float], reject: list[bool]):
        raise NotImplementedError
