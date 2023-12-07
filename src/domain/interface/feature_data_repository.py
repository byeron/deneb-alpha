from abc import ABC, abstractmethod

from domain.interface.feature_data import IFeatureData


class IFeatureDataRepository(ABC):
    @abstractmethod
    def save(self, feature_file: IFeatureData) -> str:
        raise NotImplementedError("Subclasses must implement save method")

    @abstractmethod
    def find(self, _id: str) -> IFeatureData:
        raise NotImplementedError("Subclasses must implement find method")

    @abstractmethod
    def find_all(self) -> list[IFeatureData]:
        raise NotImplementedError("Subclasses must implement find_all method")

    @abstractmethod
    def delete(self, _id: str) -> str:
        raise NotImplementedError("Subclasses must implement delete method")
