from abc import ABC, abstractmethod
from domain.interface.feature_file_repository import IFeatureFileRepository


class IGetFile(ABC):
    @abstractmethod
    def __init__(self, repo: IFeatureFileRepository) -> None:
        raise NotImplementedError("Not implemented yet.")

    @abstractmethod
    def run(self, _id: str) -> str:
        raise NotImplementedError("Not implemented yet.")