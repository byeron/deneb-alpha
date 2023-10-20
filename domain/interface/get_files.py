from abc import ABC, abstractmethod

from domain.interface.feature_data_repository import IFeatureDataRepository


class IGetFiles(ABC):
    @abstractmethod
    def __init__(self, repo: IFeatureDataRepository) -> None:
        raise NotImplementedError("Subclasses must implement __init__ method")

    @abstractmethod
    def run(self):
        raise NotImplementedError("Subclasses must implement run method")
