from abc import ABC, abstractmethod


class IFluctuationConfig(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError("Subclasses must implement constructor")
