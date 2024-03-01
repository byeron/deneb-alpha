from injector import Module

from domain.clustering_config import ClusteringConfig
from domain.interface.clustering import IClustering
from domain.interface.clustering_config import IClusteringConfig
from usecase.clustering import Clustering


class ClusteringFactory(Module):
    def __init__(
        self,
        cutoff,
        rank,
        linkage_method,
        criterion,
    ):
        self.cutoff = cutoff
        self.rank = rank
        self.linkage_method = linkage_method
        self.criterion = criterion

    def configure(self, binder):
        binder.bind(
            IClusteringConfig,
            to=ClusteringConfig(
                self.cutoff,
                self.rank,
                self.linkage_method,
                self.criterion,
            ),
        )
        binder.bind(IClustering, to=Clustering)
