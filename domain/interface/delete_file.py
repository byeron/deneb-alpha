from abc import ABC, abstractmethod


class IDeleteFile(ABC):
    @abstractmethod
    def __init__(self, path: str) -> None:
        raise NotImplementedError("Subclasses must implement __init__ method")

    @abstractmethod
    def run(self, _id: str) -> str:  # _id
        raise NotImplementedError("Subclasses must implement run method")
