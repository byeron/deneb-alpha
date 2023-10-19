from abc import ABC, abstractmethod

from domain.interface.feature_file_repository import IFeatureFileRepository


class IDeleteFile(ABC):
    @abstractmethod
    def __init__(self, repo: IFeatureFileRepository) -> None:
        raise NotImplementedError("Subclasses must implement __init__ method")

    @abstractmethod
    def run(self, _id: str) -> str:  # _id
        raise NotImplementedError("Subclasses must implement run method")
