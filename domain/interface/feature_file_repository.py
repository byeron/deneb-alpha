from abc import ABC, abstractmethod

from domain.interface.feature_file import IFeatureFile


class IFeatureFileRepository(ABC):
    @abstractmethod
    def save(self, feature_file: IFeatureFile) -> str:
        raise NotImplementedError("Subclasses must implement save method")

    @abstractmethod
    def find(self, _id: str) -> IFeatureFile:
        raise NotImplementedError("Subclasses must implement find method")

    @abstractmethod
    def find_all(self) -> list[IFeatureFile]:
        raise NotImplementedError("Subclasses must implement find_all method")

    @abstractmethod
    def delete(self, _id: str) -> str:
        raise NotImplementedError("Subclasses must implement delete method")
