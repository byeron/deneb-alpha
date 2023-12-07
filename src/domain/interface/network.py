from abc import ABC, abstractmethod


class INetwork(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError("Subclasses must implement run method")
