from abc import ABC, abstractmethod

from domain.interface.fluctuation import IFluctuation
from domain.interface.network import INetwork


class IDNBScore(ABC):
    def __init__(self, fluctuation: IFluctuation, network: INetwork):
        self.fluctuation = fluctuation
        self.network = network

    @abstractmethod
    def run(self):
        raise NotImplementedError("Subclasses must implement run method")
