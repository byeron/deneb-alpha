from abc import ABC, abstractmethod

from domain.interface.feature_data_repository import IFeatureDataRepository


class IRegisterFile(ABC):
    @abstractmethod
    def __init__(self, repo: IFeatureDataRepository) -> None:
        raise NotImplementedError("Subclasses must implement __init__ method")

    @abstractmethod
    def run(self, path: str) -> str:  # _id
        raise NotImplementedError("Subclasses must implement run method")
