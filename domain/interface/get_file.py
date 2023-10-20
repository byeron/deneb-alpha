from abc import ABC, abstractmethod
from domain.interface.feature_data_repository import IFeatureDataRepository


class IGetFile(ABC):
    @abstractmethod
    def __init__(self, repo: IFeatureDataRepository) -> None:
        raise NotImplementedError("Not implemented yet.")

    @abstractmethod
    def run(self, _id: str) -> str:
        raise NotImplementedError("Not implemented yet.")