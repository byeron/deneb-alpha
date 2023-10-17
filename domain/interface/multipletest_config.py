from abc import ABC, abstractmethod


class IMultipletestConfig(ABC):
    @abstractmethod
    def __init__(self):
        raise NotImplementedError("Subclasses must implement constructor")
