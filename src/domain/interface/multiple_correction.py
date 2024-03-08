from abc import ABC, abstractmethod

from domain.interface.multiple_correction_config import \
    IMultipleCorrectionConfig


class IMultipleCorrection(ABC):
    @abstractmethod
    def __init__(self, config: IMultipleCorrectionConfig):
        raise NotImplementedError("Subclasses must implement constructor")

    @abstractmethod
    def run(
        self, pvalues: list[float]
    ) -> list[list[float], list[bool]]:  # P-Values, Rejected
        raise NotImplementedError("Subclasses must implement run method")
