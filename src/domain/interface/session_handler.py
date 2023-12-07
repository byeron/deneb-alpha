from abc import ABC, abstractmethod


class ISessionHandler(ABC):
    @abstractmethod
    def __init__(self, url: str):
        raise NotImplementedError("Subclasses must implement constructor")
