from abc import ABC, abstractmethod

from domain.interface.fluctuation_config import IFluctuationConfig


class IFluctuation(ABC):
    @abstractmethod
    def __init__(self, config: IFluctuationConfig):
        raise NotImplementedError("Subclasses must implement constructor")

    @abstractmethod
    def run(self) -> list[list[float], list[bool]]:  # P-Values, Rejected
        raise NotImplementedError("Subclasses must implement run method")
