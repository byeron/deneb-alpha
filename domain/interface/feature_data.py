from abc import ABC, abstractmethod


class IFeatureData(ABC):
    @abstractmethod
    def __init__(self, path: str) -> None:
        raise NotImplementedError("Subclasses must implement __init__ method")

    @abstractmethod
    def src_path(self) -> str:
        raise NotImplementedError("Subclasses must implement src_path method")

    @abstractmethod
    def file_id(self) -> str:
        raise NotImplementedError("Subclasses must implement id method")

    @abstractmethod
    def file_name(self) -> str:
        raise NotImplementedError("Subclasses must implement file_name method")

    @abstractmethod
    def hash(self) -> str:
        raise NotImplementedError("Subclasses must implement hash method")

    @abstractmethod
    def created_at(self) -> str:
        raise NotImplementedError("Subclasses must implement created_at method")
