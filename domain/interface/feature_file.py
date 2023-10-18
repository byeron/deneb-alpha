from abc import ABC, abstractmethod


class IFeatureFile(ABC):
    @abstractmethod
    def __init__(self, path: str) -> None:
        raise NotImplementedError("Subclasses must implement __init__ method")

    @abstractmethod
    def src_path(self) -> str:
        raise NotImplementedError("Subclasses must implement src_path method")

    @abstractmethod
    def file_id(self) -> str:
        raise NotImplementedError("Subclasses must implement id method")
