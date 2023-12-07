from abc import ABC, abstractmethod

from domain.interface.dissimilarity_config import IDissimilarityConfig


class IDissimilarity(ABC):
    @abstractmethod
    def __init__(self, dissimilarity_config: IDissimilarityConfig):
        raise NotImplementedError("Should implement __init__")

    @abstractmethod
    def run(self, feature_data):
        raise NotImplementedError("Should implement run")
