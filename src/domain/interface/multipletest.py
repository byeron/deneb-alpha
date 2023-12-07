from abc import ABC, abstractmethod

from domain.interface.multipletest_config import IMultipletestConfig


class IMultipletest(ABC):
    @abstractmethod
    def __init__(self, config: IMultipletestConfig):
        raise NotImplementedError("Subclasses must implement constructor")

    @abstractmethod
    def run(
        self, pvalues: list[float]
    ) -> list[list[float], list[bool]]:  # P-Values, Rejected
        raise NotImplementedError("Subclasses must implement run method")
