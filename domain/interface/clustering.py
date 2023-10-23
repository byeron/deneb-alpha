from abc import ABC, abstractmethod

from domain.interface.clustering_config import IClusteringConfig


class IClustering(ABC):
    def __init__(self, clustering_config: IClusteringConfig):
        self.config = clustering_config

    def run(self, feature_data):
        raise NotImplementedError
