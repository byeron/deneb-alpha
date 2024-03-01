from abc import ABC, abstractmethod


class IMultipleCorrectionConfig(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError("Subclasses must implement constructor")
