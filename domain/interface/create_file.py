from abc import ABC, abstractmethod


class ICreateFile(ABC):
    @abstractmethod
    def __init__(self, path: str) -> None:
        raise NotImplementedError("Subclasses must implement __init__ method")

    @abstractmethod
    def run(self) -> str:  # _id
        raise NotImplementedError("Subclasses must implement run method")
